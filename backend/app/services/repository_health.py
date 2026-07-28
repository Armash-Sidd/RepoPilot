"""Deterministic, evidence-backed repository health scoring."""

from __future__ import annotations

from app.schemas.analysis import (
    DetectedFile,
    HealthCategoryScore,
    HealthHighlight,
    RepositoryEvidence,
    RepositoryHealth,
    RepositoryStructure,
)


class RepositoryHealthService:
    """Score repository health using only material collected by RepoPilot."""

    def score(
        self,
        evidence: RepositoryEvidence,
        structure: RepositoryStructure,
        technology_signals: list[DetectedFile],
    ) -> RepositoryHealth:
        """Return weighted category scores and their traceable highlights."""
        evidence_paths = {file.path for file in evidence.files}
        root_directories = set(structure.root_directories)
        tree_paths = evidence.directory_tree

        readme_paths = sorted(path for path in evidence_paths if path.rsplit("/", 1)[-1].lower().startswith("readme"))
        documentation = HealthCategoryScore(
            name="Documentation",
            score=100 if readme_paths else 25,
            weight=20,
            explanation="A root README was collected." if readme_paths else "No root README was collected from the repository.",
            evidence_paths=readme_paths or ["repository root contents"],
            recommendation=None if readme_paths else "Add a root README with setup, usage, and project orientation.",
        )

        test_paths = sorted(path for path in tree_paths if path.startswith(("tests/", "test/")))
        has_test_directory = bool(test_paths) or bool(root_directories & {"tests", "test"})
        testing = HealthCategoryScore(
            name="Testing",
            score=100 if has_test_directory else 0,
            weight=25,
            explanation="A test directory is present in collected repository structure." if has_test_directory else "No test directory was observed in collected repository structure.",
            evidence_paths=test_paths[:3] or sorted(root_directories & {"tests", "test"}) or ["repository root contents"],
            recommendation=None if has_test_directory else "Add a test directory and automate the project’s core checks.",
        )

        workflow_paths = sorted(path for path in evidence_paths if path.lower().startswith(".github/workflows/"))
        continuous_integration = HealthCategoryScore(
            name="CI/CD",
            score=100 if workflow_paths else 0,
            weight=20,
            explanation="GitHub Actions workflow files were collected." if workflow_paths else "No GitHub Actions workflow files were collected.",
            evidence_paths=workflow_paths or ["repository directory tree"],
            recommendation=None if workflow_paths else "Add a GitHub Actions workflow for tests and quality checks.",
        )

        source_like_directories = {"src", "app", "backend", "frontend", "server", "client", "lib", "packages"}
        structure_evidence = sorted(root_directories)
        has_source_layout = bool(root_directories & source_like_directories)
        structure_score = 100 if has_test_directory and (has_source_layout or len(root_directories) >= 3) else 70 if len(root_directories) >= 2 else 40 if root_directories else 0
        project_structure = HealthCategoryScore(
            name="Project Structure",
            score=structure_score,
            weight=15,
            explanation="The repository has separated top-level project areas, including tests." if structure_score == 100 else "The repository has multiple observed top-level directories." if structure_score == 70 else "Only limited top-level project structure was observed.",
            evidence_paths=structure_evidence or ["repository root contents"],
            recommendation=None if structure_score >= 70 else "Separate application code, tests, and supporting project assets into clear directories.",
        )

        manifest_paths = sorted(
            signal.file_name
            for signal in technology_signals
            if signal.category in {"package_manifest", "dependency_manifest", "dependency_lockfile"}
        )
        config_paths = sorted(path for path in evidence_paths if path in {".gitignore", ".editorconfig", ".nvmrc", "Makefile"})
        configuration_score = 100 if manifest_paths else 40 if config_paths else 0
        configuration = HealthCategoryScore(
            name="Configuration",
            score=configuration_score,
            weight=15,
            explanation="A package or dependency manifest was detected." if manifest_paths else "Project configuration files were collected, but no supported package or dependency manifest was detected." if config_paths else "No supported project configuration file was collected.",
            evidence_paths=manifest_paths or config_paths or ["repository root contents"],
            recommendation=None if manifest_paths else "Add and document a supported dependency or package manifest.",
        )

        container_paths = sorted(path for path in evidence_paths if path.rsplit("/", 1)[-1] in {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"})
        containerization = HealthCategoryScore(
            name="Containerization",
            score=100 if container_paths else 0,
            weight=5,
            explanation="Container configuration was collected." if container_paths else "No Dockerfile or Docker Compose configuration was collected.",
            evidence_paths=container_paths or ["repository root contents"],
            recommendation=None if container_paths else "Add container configuration if reproducible container-based development or deployment is a project goal.",
        )

        categories = [documentation, testing, continuous_integration, project_structure, configuration, containerization]
        overall_score = round(sum(category.score * category.weight for category in categories) / 100)
        strengths = [
            HealthHighlight(category=category.name, title=f"Strong {category.name}", detail=category.explanation, evidence_paths=category.evidence_paths)
            for category in sorted(categories, key=lambda category: (-category.score, category.name))
            if category.score >= 70
        ][:3]
        improvements = [
            HealthHighlight(category=category.name, title=f"Improve {category.name}", detail=category.recommendation or category.explanation, evidence_paths=category.evidence_paths)
            for category in sorted(categories, key=lambda category: (category.score, category.name))
            if category.score < 70
        ][:3]
        label = "Excellent" if overall_score >= 85 else "Good" if overall_score >= 70 else "Fair" if overall_score >= 50 else "Needs Improvement"
        return RepositoryHealth(
            overall_score=overall_score,
            label=label,
            categories=categories,
            top_strengths=strengths,
            highest_priority_improvements=improvements,
        )