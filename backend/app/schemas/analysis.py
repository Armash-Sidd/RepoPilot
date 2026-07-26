"""Request and response schemas for repository intake."""

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


class AnalyzeRepositoryResponse(RepositoryDetails):
    """Successful repository intake response."""

    success: bool
