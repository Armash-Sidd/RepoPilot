# Architecture

RepoPilot separates its Next.js frontend from its FastAPI backend.

The landing-page repository form sends `POST /api/analyze` to the FastAPI service. The API validates and normalizes the GitHub URL through a Pydantic schema and repository URL service. `GitHubRepositoryClient` retrieves public repository metadata, language data, and root-level contents through GitHub's REST API. `RepositoryInspectionService` normalizes those responses into RepoPilot's inspection schema before the frontend renders a repository overview.

For local development, the backend permits requests from `http://localhost:3000`. The integration is read-only and uses no authentication: repositories are not cloned, source code is not executed, and only root-level entry names are inspected. Persistence, background workers, AI analysis, deep static analysis, reports, and job orchestration remain deferred.
