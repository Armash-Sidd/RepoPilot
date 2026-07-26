# RepoPilot

> Project-level guide for the RepoPilot repository scaffold.

RepoPilot inspects public GitHub repositories and presents lightweight engineering signals without cloning or executing repository code. The current milestone retrieves repository metadata, language data, and root-level structure through the public GitHub REST API.

## Structure

- `backend/` contains the FastAPI service scaffold.
- `frontend/` contains the Next.js interface scaffold.
- `docs/` contains product and engineering documentation.

## Current capability

Submit a public GitHub repository URL to receive its metadata, language distribution, root-level files and directories, and detected technology/configuration files. Deeper static analysis and engineering reports are deferred to later milestones.

## Local setup

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for service-specific setup instructions.
