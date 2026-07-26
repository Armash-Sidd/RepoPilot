"""Repository intake endpoint."""

from fastapi import APIRouter

from app.schemas.analysis import AnalyzeRepositoryRequest, AnalyzeRepositoryResponse
from app.services.repository_url import parse_repository_url

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeRepositoryResponse)
def analyze_repository(payload: AnalyzeRepositoryRequest) -> AnalyzeRepositoryResponse:
    """Validate a public GitHub repository URL and return its normalized identity."""
    repository = parse_repository_url(payload.repository_url)
    return AnalyzeRepositoryResponse(success=True, **repository.model_dump())
