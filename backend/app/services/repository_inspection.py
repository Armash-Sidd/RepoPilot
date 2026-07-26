"""Lightweight, read-only inspection of public GitHub repositories."""

from datetime import datetime
from typing import Any

from app.schemas.analysis import DetectedFile, LanguageUsage, RepositoryInspection, RepositoryMetadata, RepositoryStructure
from app.services.github_repository_client import GitHubRepositoryClient, GitHubRepositoryNotFoundError, GitHubUpstreamError
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

        return RepositoryInspection(
            metadata=self._normalize_metadata(metadata_payload),
            languages=self._normalize_languages(languages_payload),
            structure=self._normalize_structure(contents_payload),
            technology_signals=self._detect_technology_signals(contents_payload),
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
