"""Lightweight, read-only inspection of public GitHub repositories."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.schemas.analysis import (
    DetectedFile,
    EngineeringReview,
    EvidenceFile,
    LanguageUsage,
    RepositoryEvidence,
    RepositoryInspection,
    RepositoryMetadata,
    RepositoryStructure,
    ReviewFinding,
)
from app.services.github_repository_client import GitHubRepositoryClient, GitHubRepositoryNotFoundError, GitHubUpstreamError
from app.services.repository_health import RepositoryHealthService
from app.services.repository_intelligence import RepositoryIntelligenceService
from app.services.repository_url import ParsedRepositoryUrl

TECHNOLOGY_FILE_SIGNALS = {
    "package.json": ("package_manifest", "Node.js package manifest"),
    "requirements.txt": ("dependency_manifest", "Python dependencies"),
    "pyproject.toml": ("package_manifest", "Python project configuration"),
    "Pipfile": ("dependency_manifest", "Python dependency manifest"),
    "poetry.lock": ("dependency_lockfile", "Poetry dependency lockfile"),
    "Dockerfile": ("container", "Docker container configuration"),
    "docker-compose.yml": ("container", "Docker Compose configuration"),
    "docker-compose.yaml": ("container", "Docker Compose configuration"),
    "go.mod": ("package_manifest", "Go module manifest"),
    "Cargo.toml": ("package_manifest", "Rust package manifest"),
    "Gemfile": ("dependency_manifest", "Ruby dependency manifest"),
    "pom.xml": ("package_manifest", "Maven project configuration"),
    "build.gradle": ("package_manifest", "Gradle build configuration"),
}

EVIDENCE_FILE_NAMES = set(TECHNOLOGY_FILE_SIGNALS) | {
    "README.md",
    "README.rst",
    ".gitignore",
    ".editorconfig",
    ".nvmrc",
    "Makefile",
}
MAX_EVIDENCE_FILES = 12
MAX_WORKFLOW_FILES = 3
MAX_FILE_CHARACTERS = 20_000
MAX_EVIDENCE_CHARACTERS = 100_000
MAX_TREE_PATHS = 250


class RepositoryInspectionService:
    """Compose normalized repository insights from GitHub REST responses."""

    def __init__(self, github_client: GitHubRepositoryClient | None = None) -> None:
        self.github_client = github_client or GitHubRepositoryClient()

    def inspect(self, repository: ParsedRepositoryUrl) -> RepositoryInspection:
        """Inspect metadata, languages, and root-level structure without cloning."""
        metadata_payload = self.github_client.get_repository(repository.owner, repository.repository)
        languages_payload = self.github_client.get_languages(repository.owner, repository.repository)
        try:
            contents_payload = self.github_client.get_root_contents(repository.owner, repository.repository)
        except GitHubRepositoryNotFoundError:
            # GitHub returns 404 for root contents in an empty repository after metadata succeeds.
            contents_payload = []

        metadata = self._normalize_metadata(metadata_payload)
        evidence = self._collect_evidence(repository, metadata.default_branch)
        technology_signals = self._detect_technology_signals(contents_payload)
        structure = self._normalize_structure(contents_payload)

        health = RepositoryHealthService().score(evidence, structure, technology_signals)
        return RepositoryInspection(
            metadata=metadata,
            languages=self._normalize_languages(languages_payload),
            structure=structure,
            technology_signals=technology_signals,
            evidence=evidence,
            engineering_review=self._generate_review(evidence, technology_signals, languages_payload),
            health=health,
            intelligence=RepositoryIntelligenceService().analyze(evidence, structure, technology_signals, health),
        )

    def _collect_evidence(self, repository: ParsedRepositoryUrl, branch: str) -> RepositoryEvidence:
        """Build a small, explicit evidence package from high-signal public files."""
        try:
            tree_entries, tree_was_truncated = self.github_client.get_repository_tree(repository.owner, repository.repository, branch)
        except GitHubRepositoryNotFoundError:
            return RepositoryEvidence(directory_tree=[], files=[], tree_was_truncated=False)
        file_paths = sorted(
            entry["path"]
            for entry in tree_entries
            if entry.get("type") == "blob" and isinstance(entry.get("path"), str)
        )
        selected_paths = self._select_evidence_paths(file_paths)
        files: list[EvidenceFile] = []
        remaining_characters = MAX_EVIDENCE_CHARACTERS

        for path, category in selected_paths:
            if remaining_characters <= 0:
                break
            try:
                content = self.github_client.get_file_content(repository.owner, repository.repository, path)
            except GitHubRepositoryNotFoundError:
                continue
            content = content[: min(MAX_FILE_CHARACTERS, remaining_characters)]
            files.append(EvidenceFile(path=path, category=category, content=content))
            remaining_characters -= len(content)

        return RepositoryEvidence(
            directory_tree=file_paths[:MAX_TREE_PATHS],
            files=files,
            tree_was_truncated=tree_was_truncated,
        )

    @staticmethod
    def _select_evidence_paths(file_paths: list[str]) -> list[tuple[str, str]]:
        """Choose repository-defining files with fixed, reviewable collection limits."""
        selected: list[tuple[str, str]] = []
        workflow_count = 0
        for path in file_paths:
            name = path.rsplit("/", 1)[-1]
            lower_path = path.lower()
            is_root_file = "/" not in path
            if lower_path.startswith(".github/workflows/") and lower_path.endswith((".yml", ".yaml")):
                if workflow_count < MAX_WORKFLOW_FILES:
                    selected.append((path, "workflow"))
                    workflow_count += 1
            elif is_root_file and (name in EVIDENCE_FILE_NAMES or name.lower().startswith("readme")):
                category = "readme" if name.lower().startswith("readme") else "configuration"
                selected.append((path, category))
            if len(selected) >= MAX_EVIDENCE_FILES:
                break
        return selected

    @staticmethod
    def _generate_review(
        evidence: RepositoryEvidence,
        technology_signals: list[DetectedFile],
        languages_payload: dict[str, Any],
    ) -> EngineeringReview:
        """Create deterministic review findings supported only by collected evidence."""
        paths = {file.path for file in evidence.files}
        root_directories = sorted({path.split("/", 1)[0] for path in evidence.directory_tree if "/" in path})
        architecture_evidence = root_directories[:6] or [file.path for file in evidence.files[:3]]
        if root_directories:
            architecture_summary = "Observed top-level project areas: " + ", ".join(root_directories[:6]) + "."
        elif architecture_evidence:
            architecture_summary = "The repository structure is represented by the collected root-level project files."
        else:
            architecture_summary = "No repository structure could be collected for an architecture summary."

        technology_stack = [signal.label for signal in technology_signals]
        technology_stack.extend(name for name, size in sorted(languages_payload.items(), key=lambda item: item[1], reverse=True) if isinstance(name, str) and isinstance(size, int) and size > 0)
        technology_stack = list(dict.fromkeys(technology_stack))

        findings: list[ReviewFinding] = []
        readmes = [path for path in paths if path.rsplit("/", 1)[-1].lower().startswith("readme")]
        if readmes:
            findings.append(ReviewFinding(category="documentation", title="Repository documentation is present", detail="A README was collected as part of the review evidence.", severity="info", evidence_paths=readmes))
        else:
            findings.append(ReviewFinding(category="documentation", title="No root README was collected", detail="The bounded evidence scan found no root README file to establish onboarding guidance.", severity="medium", evidence_paths=["repository directory tree"], recommendation="Add a root README with setup, usage, and architecture orientation.", priority=1))

        workflows = [path for path in paths if path.lower().startswith(".github/workflows/")]
        if workflows:
            findings.append(ReviewFinding(category="development_workflow", title="Automation workflow configuration is present", detail="GitHub Actions workflow files were collected for the review.", severity="info", evidence_paths=workflows))
        else:
            findings.append(ReviewFinding(category="development_workflow", title="No GitHub Actions workflow was collected", detail="The bounded evidence scan found no workflow files under .github/workflows.", severity="low", evidence_paths=["repository directory tree"], recommendation="Add a CI workflow that runs the project’s tests and checks on pull requests.", priority=3))

        manifest_paths = [path for path in paths if path.rsplit("/", 1)[-1] in TECHNOLOGY_FILE_SIGNALS]
        if manifest_paths:
            findings.append(ReviewFinding(category="technology", title="Project technology configuration is explicit", detail="Dependency, package, or container configuration files were collected and used to identify the stack.", severity="info", evidence_paths=manifest_paths))
        else:
            findings.append(ReviewFinding(category="maintainability", title="No recognized dependency or runtime manifest was collected", detail="The bounded evidence scan did not find a supported root-level package, dependency, or container manifest.", severity="low", evidence_paths=["repository directory tree"], recommendation="Document the project runtime and dependency-management entry point.", priority=2))

        docker_paths = [path for path in paths if path.rsplit("/", 1)[-1] in {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}]
        if docker_paths:
            findings.append(ReviewFinding(category="deployment", title="Container configuration is present", detail="Container-related configuration was collected as review evidence.", severity="info", evidence_paths=docker_paths))

        technology_evidence = manifest_paths or ["GitHub language statistics"]
        return EngineeringReview(
            architecture_summary=architecture_summary,
            architecture_evidence_paths=architecture_evidence or ["repository directory tree"],
            technology_stack=technology_stack,
            technology_stack_evidence_paths=technology_evidence,
            findings=findings,
        )

    @staticmethod
    def _normalize_metadata(payload: dict[str, Any]) -> RepositoryMetadata:
        license_payload = payload.get("license")
        license_name = license_payload.get("spdx_id") or license_payload.get("name") if isinstance(license_payload, dict) else None
        updated_at = payload.get("updated_at")
        try:
            last_updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        except (AttributeError, ValueError) as error:
            raise GitHubUpstreamError("GitHub returned invalid repository metadata.") from error
        default_branch = payload.get("default_branch")
        if not isinstance(default_branch, str):
            raise GitHubUpstreamError("GitHub returned invalid repository metadata.")

        return RepositoryMetadata(
            description=payload.get("description") if isinstance(payload.get("description"), str) else None,
            default_branch=default_branch,
            topics=[topic for topic in payload.get("topics", []) if isinstance(topic, str)],
            license=license_name if isinstance(license_name, str) else None,
            is_archived=bool(payload.get("archived", False)),
            stargazers_count=RepositoryInspectionService._count(payload, "stargazers_count"),
            forks_count=RepositoryInspectionService._count(payload, "forks_count"),
            watchers_count=RepositoryInspectionService._count(payload, "watchers_count"),
            last_updated_at=last_updated_at,
        )

    @staticmethod
    def _normalize_languages(payload: dict[str, Any]) -> list[LanguageUsage]:
        languages = {name: size for name, size in payload.items() if isinstance(name, str) and isinstance(size, int) and size >= 0}
        total_bytes = sum(languages.values())
        if total_bytes == 0:
            return []
        return [LanguageUsage(name=name, bytes=size, percentage=round(size / total_bytes * 100, 1)) for name, size in sorted(languages.items(), key=lambda item: item[1], reverse=True)]

    @staticmethod
    def _normalize_structure(contents: list[dict[str, Any]]) -> RepositoryStructure:
        root_files = sorted(entry["name"] for entry in contents if entry.get("type") == "file" and isinstance(entry.get("name"), str))
        root_directories = sorted(entry["name"] for entry in contents if entry.get("type") == "dir" and isinstance(entry.get("name"), str))
        return RepositoryStructure(has_readme=any(name.lower().startswith("readme") for name in root_files), root_files=root_files, root_directories=root_directories)

    @staticmethod
    def _detect_technology_signals(contents: list[dict[str, Any]]) -> list[DetectedFile]:
        file_names = {entry["name"] for entry in contents if entry.get("type") == "file" and isinstance(entry.get("name"), str)}
        return [DetectedFile(file_name=name, category=category, label=label) for name, (category, label) in TECHNOLOGY_FILE_SIGNALS.items() if name in file_names]

    @staticmethod
    def _count(payload: dict[str, Any], field_name: str) -> int:
        value = payload.get(field_name, 0)
        return value if isinstance(value, int) and value >= 0 else 0