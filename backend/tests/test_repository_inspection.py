"""Unit tests for lightweight repository inspection normalization."""

import unittest
from email.message import Message
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError

from app.api.routes.github import get_github_rate_limit
from app.services.github_repository_client import GitHubRepositoryClient
from app.services.repository_inspection import RepositoryInspectionService
from app.services.repository_url import ParsedRepositoryUrl, normalize_repository_url, parse_repository_url


class FakeGitHubRepositoryClient:
    def get_repository(self, owner: str, repository: str):
        return {"description": "Example repository", "default_branch": "main", "topics": ["fastapi"], "license": {"spdx_id": "MIT"}, "archived": False, "stargazers_count": 10, "forks_count": 2, "watchers_count": 10, "updated_at": "2026-07-26T00:00:00Z"}

    def get_languages(self, owner: str, repository: str):
        return {"Python": 75, "TypeScript": 25}

    def get_root_contents(self, owner: str, repository: str):
        return [{"name": "README.md", "type": "file"}, {"name": "requirements.txt", "type": "file"}, {"name": "app", "type": "dir"}, {"name": "tests", "type": "dir"}]

    def get_repository_tree(self, owner: str, repository: str, branch: str):
        return [
            {"path": "README.md", "type": "blob"},
            {"path": "requirements.txt", "type": "blob"},
            {"path": "app/main.py", "type": "blob"},
            {"path": "tests/test_example.py", "type": "blob"},
            {"path": ".github/workflows/test.yml", "type": "blob"},
        ], False

    def get_file_content(self, owner: str, repository: str, path: str):
        return {
            "README.md": "# Example\n\n## Installation\n\n## Usage\n\n## Contributing\n\n## License",
            "requirements.txt": "fastapi\npydantic\npytest\nuvicorn",
            ".github/workflows/test.yml": "name: test\nsteps:\n  - run: pytest\n  - run: ruff check .",
        }[path]


class RepositoryInspectionServiceTests(unittest.TestCase):
    def test_repository_url_normalizes_common_github_formats(self):
        expected_url = "https://github.com/owner/repository"
        for repository_url in (
            "https://github.com/owner/repository",
            "https://github.com/owner/repository/",
            "https://github.com/owner/repository.git",
            "  https://github.com/owner/repository.git/  ",
        ):
            with self.subTest(repository_url=repository_url):
                self.assertEqual(normalize_repository_url(repository_url), expected_url)
                parsed = parse_repository_url(repository_url)
                self.assertEqual(parsed.owner, "owner")
                self.assertEqual(parsed.repository, "repository")
                self.assertEqual(parsed.repository_url, expected_url)

    def test_github_client_uses_optional_token_and_anonymous_fallback(self):
        self.assertNotIn("Authorization", GitHubRepositoryClient(token="")._headers())
        self.assertEqual(GitHubRepositoryClient(token="configured-token")._headers()["Authorization"], "Bearer configured-token")
        with patch.dict("os.environ", {"GITHUB_TOKEN": "environment-token"}, clear=True):
            self.assertEqual(GitHubRepositoryClient()._headers()["Authorization"], "Bearer environment-token")
            self.assertTrue(GitHubRepositoryClient().authenticated)

    def test_github_client_distinguishes_rate_limit_from_other_forbidden_responses(self):
        exhausted_headers = Message()
        exhausted_headers["X-RateLimit-Remaining"] = "0"
        exhausted = HTTPError("https://api.github.com", 403, "Forbidden", exhausted_headers, BytesIO(b'{"message":"API rate limit exceeded"}'))
        forbidden = HTTPError("https://api.github.com", 403, "Forbidden", Message(), BytesIO(b'{"message":"Resource not accessible by integration"}'))

        self.assertTrue(GitHubRepositoryClient._is_rate_limit_error(exhausted, GitHubRepositoryClient._read_error_body(exhausted)))
        self.assertFalse(GitHubRepositoryClient._is_rate_limit_error(forbidden, GitHubRepositoryClient._read_error_body(forbidden)))

    def test_rate_limit_endpoint_reports_the_active_client_mode(self):
        fake_client = type("FakeClient", (), {"authenticated": True, "get_rate_limit": lambda self: {"limit": 5000, "remaining": 4999, "reset": 1234567890}})()
        with patch("app.api.routes.github.GitHubRepositoryClient", return_value=fake_client):
            response = get_github_rate_limit()

        self.assertEqual(response.model_dump(), {"authenticated": True, "limit": 5000, "remaining": 4999, "reset": 1234567890})

    def test_inspection_normalizes_github_responses(self):
        inspection = RepositoryInspectionService(FakeGitHubRepositoryClient()).inspect(ParsedRepositoryUrl(owner="owner", repository="repository", repository_url="https://github.com/owner/repository"))
        self.assertEqual(inspection.metadata.license, "MIT")
        self.assertEqual(inspection.metadata.stargazers_count, 10)
        self.assertEqual(inspection.languages[0].percentage, 75.0)
        self.assertTrue(inspection.structure.has_readme)
        self.assertEqual(inspection.technology_signals[0].file_name, "requirements.txt")
        self.assertEqual(inspection.evidence.files[0].path, ".github/workflows/test.yml")
        self.assertTrue(all(finding.evidence_paths for finding in inspection.engineering_review.findings))
        self.assertEqual(inspection.health.overall_score, 95)
        self.assertEqual(inspection.health.label, "Excellent")
        self.assertTrue(all(category.evidence_paths for category in inspection.health.categories))
        self.assertEqual(inspection.health.highest_priority_improvements[0].category, "Containerization")
        self.assertEqual(inspection.intelligence.project_type.project_type, "FastAPI backend")
        self.assertTrue(all(insight.status == "present" for insight in inspection.intelligence.documentation))
        self.assertEqual(inspection.intelligence.development_workflow[0].title, "Automated tests")
        self.assertEqual(inspection.intelligence.development_workflow[0].status, "present")
        self.assertEqual(inspection.intelligence.technology_understanding[0].title, "FastAPI")


if __name__ == "__main__":
    unittest.main()
