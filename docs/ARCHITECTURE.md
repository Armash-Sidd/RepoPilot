# Architecture

RepoPilot separates its Next.js frontend from its FastAPI backend.

The landing-page repository form sends `POST /api/analyze` to the FastAPI service. The API validates and normalizes the GitHub URL through a Pydantic schema and repository URL service, then returns the extracted owner and repository metadata. The frontend renders either the returned repository details or a validation error.

For local development, the backend permits requests from `http://localhost:3000`. Background analysis, GitHub API access, repository cloning, persistence, authentication, and job orchestration remain deferred to later milestones.
