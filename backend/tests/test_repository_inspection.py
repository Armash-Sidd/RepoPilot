"""Unit tests for lightweight repository inspection normalization."""

import unittest

from app.services.repository_inspection import RepositoryInspectionService
from app.services.repository_url import ParsedRepositoryUrl


class FakeGitHubRepositoryClient:
    def get_repository(self, owner: str, repository: str):
        return {"description": "Example repository", "default_branch": "main", "topics": ["fastapi"], "license": {"spdx_id": "MIT"}, "archived": False, "stargazers_count": 10, "forks_count": 2, "watchers_count": 10, "updated_at": "2026-07-26T00:00:00Z"}

    def get_languages(self, owner: str, repository: str):
        return {"Python": 75, "TypeScript": 25}

    def get_root_contents(self, owner: str, repository: str):
        return [{"name": "README.md", "type": "file"}, {"name": "requirements.txt", "type": "file"}, {"name": "app", "type": "dir"}]


class RepositoryInspectionServiceTests(unittest.TestCase):
    def test_inspection_normalizes_github_responses(self):
        inspection = RepositoryInspectionService(FakeGitHubRepositoryClient()).inspect(ParsedRepositoryUrl(owner="owner", repository="repository", repository_url="https://github.com/owner/repository"))
        self.assertEqual(inspection.metadata.license, "MIT")
        self.assertEqual(inspection.metadata.stargazers_count, 10)
        self.assertEqual(inspection.languages[0].percentage, 75.0)
        self.assertTrue(inspection.structure.has_readme)
        self.assertEqual(inspection.technology_signals[0].file_name, "requirements.txt")


if __name__ == "__main__":
    unittest.main()
