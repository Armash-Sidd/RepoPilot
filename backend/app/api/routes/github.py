"""GitHub integration status endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.analysis import GitHubRateLimitResponse
from app.services.github_repository_client import GitHubRateLimitError, GitHubTimeoutError, GitHubUpstreamError, GitHubRepositoryClient

router = APIRouter(prefix="/github", tags=["github"])


@router.get("/rate-limit", response_model=GitHubRateLimitResponse)
def get_github_rate_limit() -> GitHubRateLimitResponse:
    """Return the active GitHub API quota without exposing credentials."""
    client = GitHubRepositoryClient()
    try:
        quota = client.get_rate_limit()
    except GitHubRateLimitError as error:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="GitHub's API rate limit has been reached. Please try again later.") from error
    except GitHubTimeoutError as error:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="GitHub took too long to respond. Please try again.") from error
    except GitHubUpstreamError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="GitHub could not provide rate-limit information right now.") from error

    return GitHubRateLimitResponse(authenticated=client.authenticated, **quota)
