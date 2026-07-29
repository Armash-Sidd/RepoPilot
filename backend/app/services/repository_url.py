"""Validation and parsing for supported repository URLs."""

import re

from pydantic import BaseModel

GITHUB_REPOSITORY_URL_PATTERN = re.compile(
    r"^https://(?:www\.)?github\.com/"
    r"(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))/"
    r"(?P<repository>[A-Za-z0-9][A-Za-z0-9._-]*)/?$"
)


class ParsedRepositoryUrl(BaseModel):
    """Repository coordinates extracted from a validated GitHub URL."""

    owner: str
    repository: str
    repository_url: str


def normalize_repository_url(value: str) -> str:
    """Return a canonical GitHub repository URL or raise a validation error."""
    normalized_url = value.strip()
    if not normalized_url:
        raise ValueError("Repository URL cannot be empty.")

    match = GITHUB_REPOSITORY_URL_PATTERN.fullmatch(normalized_url)
    if not match:
        raise ValueError(
            "Repository URL must be an HTTPS GitHub repository URL such as "
            "https://github.com/owner/repository."
        )

    repository = match.group("repository")
    if repository.endswith(".git"):
        repository = repository[:-4]

    return f"https://github.com/{match.group('owner')}/{repository}"


def parse_repository_url(repository_url: str) -> ParsedRepositoryUrl:
    """Normalize a GitHub URL before extracting its owner and repository."""
    normalized_url = normalize_repository_url(repository_url)
    match = GITHUB_REPOSITORY_URL_PATTERN.fullmatch(normalized_url)
    if match is None:
        raise ValueError("Repository URL must be a valid GitHub repository URL.")

    return ParsedRepositoryUrl(
        owner=match.group("owner"),
        repository=match.group("repository"),
        repository_url=normalized_url,
    )
