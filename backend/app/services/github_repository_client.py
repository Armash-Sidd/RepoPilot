"""Small HTTP client for GitHub's public repository REST endpoints."""

import json
import base64
from socket import timeout as SocketTimeout
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GitHubRepositoryNotFoundError(Exception):
    """Raised when a public repository cannot be retrieved from GitHub."""


class GitHubRateLimitError(Exception):
    """Raised when GitHub's unauthenticated API rate limit is exhausted."""


class GitHubTimeoutError(Exception):
    """Raised when GitHub does not respond before the configured timeout."""


class GitHubUpstreamError(Exception):
    """Raised when GitHub returns an unusable response or cannot be reached."""


class GitHubRepositoryClient:
    """Read public repository data from GitHub without authentication."""

    API_BASE_URL = "https://api.github.com"

    def __init__(self, timeout_seconds: float = 10.0) -> None:
        self.timeout_seconds = timeout_seconds

    def get_repository(self, owner: str, repository: str) -> dict[str, Any]:
        """Return the repository metadata payload."""
        return self._get_json(f"/repos/{owner}/{repository}")

    def get_languages(self, owner: str, repository: str) -> dict[str, Any]:
        """Return GitHub's language-to-byte mapping."""
        return self._get_json(f"/repos/{owner}/{repository}/languages")

    def get_root_contents(self, owner: str, repository: str) -> list[dict[str, Any]]:
        """Return root-level repository entries without reading file contents."""
        payload = self._get_json(f"/repos/{owner}/{repository}/contents/")
        if not isinstance(payload, list):
            raise GitHubUpstreamError("GitHub returned an unexpected repository structure response.")
        return payload

    def get_repository_tree(self, owner: str, repository: str, branch: str) -> tuple[list[dict[str, Any]], bool]:
        """Return a recursive path index without fetching repository source."""
        payload = self._get_json(f"/repos/{owner}/{repository}/git/trees/{branch}?recursive=1")
        if not isinstance(payload, dict) or not isinstance(payload.get("tree"), list):
            raise GitHubUpstreamError("GitHub returned an unexpected repository tree response.")
        return payload["tree"], bool(payload.get("truncated", False))

    def get_file_content(self, owner: str, repository: str, path: str) -> str:
        """Read a single, explicitly selected public repository file."""
        payload = self._get_json(f"/repos/{owner}/{repository}/contents/{path}")
        if not isinstance(payload, dict) or payload.get("encoding") != "base64" or not isinstance(payload.get("content"), str):
            raise GitHubUpstreamError("GitHub returned an unreadable repository file.")
        try:
            return base64.b64decode(payload["content"].replace("\n", "")).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise GitHubUpstreamError("GitHub returned a non-text repository file.") from error

    def _get_json(self, path: str) -> Any:
        request = Request(
            f"{self.API_BASE_URL}{path}",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "RepoPilot/0.1",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code == 404:
                raise GitHubRepositoryNotFoundError from error
            if error.code == 429 or error.headers.get("X-RateLimit-Remaining") == "0":
                raise GitHubRateLimitError from error
            raise GitHubUpstreamError("GitHub returned an unexpected response.") from error
        except (SocketTimeout, TimeoutError) as error:
            raise GitHubTimeoutError from error
        except URLError as error:
            if isinstance(error.reason, SocketTimeout):
                raise GitHubTimeoutError from error
            raise GitHubUpstreamError("GitHub could not be reached.") from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise GitHubUpstreamError("GitHub returned an unreadable response.") from error
