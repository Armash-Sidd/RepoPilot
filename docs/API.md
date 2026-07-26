# API Reference

## `POST /api/analyze`

Inspects a public GitHub repository through the unauthenticated GitHub REST API. It does not clone repositories, read source-file contents, execute code, or use authentication.

Request body:

```json
{
  "repository_url": "https://github.com/owner/repository"
}
```

Successful response (`200`):

```json
{
  "success": true,
  "owner": "owner",
  "repository": "repository",
  "repository_url": "https://github.com/owner/repository",
  "analysis": {
    "metadata": { "description": "Example project", "default_branch": "main", "topics": ["fastapi"], "license": "MIT", "is_archived": false, "stargazers_count": 42, "forks_count": 5, "watchers_count": 42, "last_updated_at": "2026-07-26T00:00:00Z" },
    "languages": [{ "name": "Python", "bytes": 1000, "percentage": 100.0 }],
    "structure": { "has_readme": true, "root_files": ["README.md", "requirements.txt"], "root_directories": ["app"] },
    "technology_signals": [{ "file_name": "requirements.txt", "category": "dependency_manifest", "label": "Python dependencies" }]
  }
}
```

Invalid requests return FastAPI's standard `422` validation response. Supported URLs must use HTTPS, the `github.com` host, and contain an owner and repository path. A repository that cannot be accessed publicly returns `404`; GitHub rate limits return `429`; upstream failures return `502` or `504`.

When the backend runs locally, its interactive OpenAPI documentation is available at `/docs`.
