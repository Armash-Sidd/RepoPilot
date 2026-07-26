"""Repository intake endpoint."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.analysis import AnalyzeRepositoryRequest, AnalyzeRepositoryResponse
from app.services.github_repository_client import GitHubRateLimitError, GitHubRepositoryNotFoundError, GitHubTimeoutError, GitHubUpstreamError
from app.services.repository_inspection import RepositoryInspectionService
from app.services.repository_url import parse_repository_url

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeRepositoryResponse)
def analyze_repository(payload: AnalyzeRepositoryRequest) -> AnalyzeRepositoryResponse:
    """Inspect a public GitHub repository without cloning or executing it."""
    repository = parse_repository_url(payload.repository_url)
    try:
        inspection = RepositoryInspectionService().inspect(repository)
    except GitHubRepositoryNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The public GitHub repository could not be found.") from error
    except GitHubRateLimitError as error:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="GitHub's public API rate limit has been reached. Please try again later.") from error
    except GitHubTimeoutError as error:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="GitHub took too long to respond. Please try again.") from error
    except GitHubUpstreamError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="GitHub could not provide repository information right now.") from error
    return AnalyzeRepositoryResponse(success=True, **repository.model_dump(), analysis=inspection)
