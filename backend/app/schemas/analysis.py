"""Request and response schemas for repository inspection."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.services.repository_url import normalize_repository_url


class AnalyzeRepositoryRequest(BaseModel):
    """Payload accepted by the repository intake endpoint."""

    repository_url: str = Field(
        min_length=1,
        description="HTTPS URL of a public GitHub repository.",
        examples=["https://github.com/owner/repository"],
    )

    @field_validator("repository_url")
    @classmethod
    def validate_repository_url(cls, value: str) -> str:
        """Trim and validate GitHub repository URLs at the API boundary."""
        return normalize_repository_url(value)


class RepositoryDetails(BaseModel):
    """Normalized GitHub repository identity."""

    owner: str
    repository: str
    repository_url: str


class RepositoryMetadata(BaseModel):
    """Selected repository metadata normalized from GitHub."""

    description: str | None
    default_branch: str
    topics: list[str]
    license: str | None
    is_archived: bool
    stargazers_count: int
    forks_count: int
    watchers_count: int
    last_updated_at: datetime


class LanguageUsage(BaseModel):
    """A language and its relative share of repository bytes."""

    name: str
    bytes: int
    percentage: float


class RepositoryStructure(BaseModel):
    """Root-level repository structure observed through GitHub."""

    has_readme: bool
    root_files: list[str]
    root_directories: list[str]


class DetectedFile(BaseModel):
    """A recognized root-level technology or configuration file."""

    file_name: str
    category: str
    label: str


class EvidenceFile(BaseModel):
    """A bounded repository file collected to support the engineering review."""

    path: str
    category: str
    content: str


class RepositoryEvidence(BaseModel):
    """Repository material explicitly collected for review generation."""

    directory_tree: list[str]
    files: list[EvidenceFile]
    tree_was_truncated: bool


class ReviewFinding(BaseModel):
    """An engineering observation tied to one or more evidence paths."""

    category: str
    title: str
    detail: str
    severity: str
    evidence_paths: list[str]
    recommendation: str | None = None
    priority: int | None = None


class EngineeringReview(BaseModel):
    """Evidence-backed engineering review for a repository."""

    architecture_summary: str
    architecture_evidence_paths: list[str]
    technology_stack: list[str]
    technology_stack_evidence_paths: list[str]
    findings: list[ReviewFinding]


class RepositoryInspection(BaseModel):
    """Lightweight repository insights safe to return to the frontend."""

    metadata: RepositoryMetadata
    languages: list[LanguageUsage]
    structure: RepositoryStructure
    technology_signals: list[DetectedFile]
    evidence: RepositoryEvidence
    engineering_review: EngineeringReview


class AnalyzeRepositoryResponse(RepositoryDetails):
    """Successful lightweight repository inspection response."""

    success: bool
    analysis: RepositoryInspection
