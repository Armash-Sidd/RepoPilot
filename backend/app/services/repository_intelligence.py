"""Deterministic interpretation of bounded repository evidence."""

from __future__ import annotations

import re

from app.schemas.analysis import (
    DetectedFile,
    IntelligenceInsight,
    ProjectTypeInsight,
    RepositoryEvidence,
    RepositoryHealth,
    RepositoryIntelligence,
    RepositoryStructure,
)


README_SECTION_RULES = {
    "Installation or setup guidance": ("install", "installation", "setup", "getting started", "quickstart"),
    "Usage or examples": ("usage", "example", "tutorial", "how to use"),
    "Contribution guidance": ("contributing", "contribution"),
    "License information": ("license", "licensed"),
}

WORKFLOW_CAPABILITY_RULES = {
    "Automated tests": ("pytest", "npm test", "pnpm test", "yarn test", "go test", "cargo test", "unittest", "tox"),
    "Documentation build": ("mkdocs", "sphinx", "build docs", "docs/"),
    "Linting or formatting": ("ruff", "flake8", "eslint", "prettier", "black", "mypy", "lint"),
    "Publish or deploy": ("publish", "deploy", "release", "github pages", "pypi", "npm publish", "docker push"),
}

TECHNOLOGY_PURPOSES = {
    "fastapi": ("FastAPI", "FastAPI is declared in dependency configuration, indicating it is used as the web framework."),
    "pydantic": ("Pydantic", "Pydantic is declared in dependency configuration, indicating it is used for data validation and typed models."),
    "pytest": ("Pytest", "Pytest is declared in dependency configuration, indicating it is used for automated testing."),
    "uvicorn": ("Uvicorn", "Uvicorn is declared in dependency configuration, indicating it is used as an ASGI application server."),
    "next": ("Next.js", "Next.js is declared in dependency configuration, indicating it is used as the web application framework."),
    "react": ("React", "React is declared in dependency configuration, indicating it is used for the user interface."),
    "typescript": ("TypeScript", "TypeScript is declared in dependency configuration, indicating typed JavaScript development."),
    "tailwindcss": ("Tailwind CSS", "Tailwind CSS is declared in dependency configuration, indicating utility-first interface styling."),
    "torch": ("PyTorch", "PyTorch is declared in dependency configuration, indicating machine-learning model development."),
    "scikit-learn": ("scikit-learn", "scikit-learn is declared in dependency configuration, indicating machine-learning utilities or models."),
}


def contains_dependency_term(content: str, term: str) -> bool:
    """Match a dependency name without treating it as an arbitrary substring."""
    return re.search(rf"(?<![A-Za-z0-9_-]){re.escape(term)}(?![A-Za-z0-9_-])", content) is not None


class RepositoryIntelligenceService:
    """Produce conservative, source-linked repository intelligence."""

    def analyze(
        self,
        evidence: RepositoryEvidence,
        structure: RepositoryStructure,
        technology_signals: list[DetectedFile],
        health: RepositoryHealth,
    ) -> RepositoryIntelligence:
        """Interpret evidence without extending collection or executing repository code."""
        files_by_path = {file.path: file.content for file in evidence.files}
        readmes = {path: content for path, content in files_by_path.items() if path.rsplit("/", 1)[-1].lower().startswith("readme")}
        workflows = {path: content for path, content in files_by_path.items() if path.lower().startswith(".github/workflows/")}
        documentation = self._analyze_documentation(readmes)
        development_workflow = self._analyze_workflows(workflows)
        project_type = self._infer_project_type(files_by_path, technology_signals)
        technology_understanding = self._explain_technologies(files_by_path)
        best_practices = self._best_practices(health)
        return RepositoryIntelligence(
            documentation=documentation,
            development_workflow=development_workflow,
            project_type=project_type,
            technology_understanding=technology_understanding,
            best_practices=best_practices,
        )

    @staticmethod
    def _analyze_documentation(readmes: dict[str, str]) -> list[IntelligenceInsight]:
        if not readmes:
            return [IntelligenceInsight(title="README analysis unavailable", detail="No README was collected, so documentation sections cannot be evaluated.", status="insufficient_evidence", evidence_paths=["repository evidence package"])]

        path, content = next(iter(sorted(readmes.items())))
        normalized_content = content.lower()
        insights = []
        for title, terms in README_SECTION_RULES.items():
            detected = any(term in normalized_content for term in terms)
            insights.append(IntelligenceInsight(
                title=title,
                detail="Relevant section keywords were detected in the collected README." if detected else "No matching section keywords were detected in the collected README.",
                status="present" if detected else "not_detected",
                evidence_paths=[path],
            ))
        return insights

    @staticmethod
    def _analyze_workflows(workflows: dict[str, str]) -> list[IntelligenceInsight]:
        if not workflows:
            return [IntelligenceInsight(title="Workflow capability analysis unavailable", detail="No GitHub Actions workflow file was collected, so workflow behavior cannot be determined.", status="insufficient_evidence", evidence_paths=["repository evidence package"])]

        insights = []
        for title, terms in WORKFLOW_CAPABILITY_RULES.items():
            matching_paths = sorted(path for path, content in workflows.items() if any(term in content.lower() for term in terms))
            insights.append(IntelligenceInsight(
                title=title,
                detail="This capability is supported by commands or configuration in the collected workflow files." if matching_paths else "This capability was not detected in the collected workflow files.",
                status="present" if matching_paths else "not_detected",
                evidence_paths=matching_paths or sorted(workflows),
            ))
        return insights

    @staticmethod
    def _infer_project_type(files_by_path: dict[str, str], technology_signals: list[DetectedFile]) -> ProjectTypeInsight:
        manifest_content = "\n".join(content.lower() for path, content in files_by_path.items() if path.rsplit("/", 1)[-1] in {"pyproject.toml", "requirements.txt", "package.json", "Pipfile"})
        manifest_paths = sorted(path for path in files_by_path if path.rsplit("/", 1)[-1] in {"pyproject.toml", "requirements.txt", "package.json", "Pipfile"})
        if contains_dependency_term(manifest_content, "fastapi"):
            return ProjectTypeInsight(project_type="FastAPI backend", detail="FastAPI appears in collected dependency configuration.", evidence_paths=manifest_paths)
        if contains_dependency_term(manifest_content, "next"):
            return ProjectTypeInsight(project_type="Next.js application", detail="Next.js appears in collected dependency configuration.", evidence_paths=manifest_paths)
        if contains_dependency_term(manifest_content, "torch") or contains_dependency_term(manifest_content, "scikit-learn"):
            return ProjectTypeInsight(project_type="Machine learning project", detail="A machine-learning dependency appears in collected configuration.", evidence_paths=manifest_paths)
        if any(signal.file_name in {"pyproject.toml", "requirements.txt", "Pipfile"} for signal in technology_signals):
            return ProjectTypeInsight(project_type="Python project", detail="Python dependency or package configuration was collected, but the bounded evidence does not establish a narrower project type.", evidence_paths=manifest_paths)
        if any(signal.file_name == "package.json" for signal in technology_signals):
            return ProjectTypeInsight(project_type="Node.js project", detail="A Node.js package manifest was collected, but the bounded evidence does not establish a narrower project type.", evidence_paths=manifest_paths)
        return ProjectTypeInsight(project_type="Undetermined", detail="The collected evidence is insufficient to infer a project type.", evidence_paths=["repository evidence package"])

    @staticmethod
    def _explain_technologies(files_by_path: dict[str, str]) -> list[IntelligenceInsight]:
        configuration_files = {path: content.lower() for path, content in files_by_path.items() if path.rsplit("/", 1)[-1] in {"pyproject.toml", "requirements.txt", "package.json", "Pipfile"}}
        insights = []
        for term, (title, detail) in TECHNOLOGY_PURPOSES.items():
            matching_paths = sorted(path for path, content in configuration_files.items() if contains_dependency_term(content, term))
            if matching_paths:
                insights.append(IntelligenceInsight(title=title, detail=detail, status="detected", evidence_paths=matching_paths))
        return insights or [IntelligenceInsight(title="Technology purpose analysis unavailable", detail="No recognized dependency names were found in the collected configuration files.", status="insufficient_evidence", evidence_paths=sorted(configuration_files) or ["repository evidence package"])]

    @staticmethod
    def _best_practices(health: RepositoryHealth) -> list[IntelligenceInsight]:
        insights = []
        for category in health.categories:
            status = "present" if category.score == 100 else "partial" if category.score > 0 else "not_detected"
            detail = category.explanation if category.score == 100 else category.recommendation or category.explanation
            insights.append(IntelligenceInsight(title=category.name, detail=detail, status=status, evidence_paths=category.evidence_paths))
        return insights