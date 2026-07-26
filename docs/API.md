# API Reference

## `POST /api/analyze`

Validates and normalizes a public GitHub repository URL. This endpoint does not contact GitHub, clone a repository, or run analysis.

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
  "repository_url": "https://github.com/owner/repository"
}
```

Invalid requests return FastAPI's standard `422` validation response. Supported URLs must use HTTPS, the `github.com` host, and contain an owner and repository path.

When the backend runs locally, its interactive OpenAPI documentation is available at `/docs`.
