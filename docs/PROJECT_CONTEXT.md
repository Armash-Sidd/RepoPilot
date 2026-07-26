# RepoPilot Project Context

## Project Overview

RepoPilot is an engineering intelligence platform for public GitHub repositories. It helps developers understand unfamiliar codebases through structured, evidence-based repository inspection.

- **Purpose:** reduce the manual effort required to understand a repository's structure, technologies, and engineering context.
- **Users:** developers, maintainers, engineering teams, and technical reviewers.
- **Hackathon:** developed for the ChatGPT Codex Hackathon.

## Vision and Engineering Approach

RepoPilot will evolve into an AI-powered repository analysis platform covering architecture, security, documentation, technology choices, and improvement roadmaps. The MVP first establishes reliable engineering workflows and structured data before advanced AI capabilities are introduced.

The project is milestone-driven, modular, incremental, and production-focused. Each milestone is tested before the next begins.

## Technology Stack

### In use

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: FastAPI and Pydantic
- External data: unauthenticated GitHub REST API for public repositories
- Documentation: Markdown in `docs/`
- Version control: Git and GitHub

### Planned later

- Deployment target selection
- Deep static analysis, reports, job orchestration, and AI integration using free or low-cost options where practical

## Current Architecture

- `frontend/` contains the Next.js interface and reusable UI components.
- `backend/app/api/` contains HTTP routers.
- `backend/app/schemas/` contains Pydantic API models.
- `backend/app/services/` contains reusable business logic.
- `docs/` contains product, API, architecture, roadmap, and onboarding documentation.

The current flow is: frontend URL form -> `POST /api/analyze` -> URL validation -> GitHub REST client -> repository inspection service -> normalized API result -> repository overview UI.

`GitHubRepositoryClient` reads public metadata, languages, and root-level entries only. `RepositoryInspectionService` normalizes these responses and detects configuration signals. Repositories are never cloned or executed.

## Completed Milestones

### Milestone 1 - Foundation

- Project scaffold, FastAPI, Next.js, Git, and documentation structure

### Milestone 2 - Landing Experience

- Landing page, repository URL form, responsive UI, and frontend validation

### Milestone 3 - Repository Intake Pipeline

- Frontend-backend communication, `POST /api/analyze`, Pydantic validation, URL parsing, CORS, and API/architecture documentation

### Milestone 4 - Lightweight Repository Inspection

- Public GitHub REST integration
- Repository metadata, language data, root-level structure, and technology signals
- Repository overview UI including stars, forks, watchers, and last-updated time
- Read-only inspection without cloning, authentication, persistence, or background workers

## Remaining Roadmap

1. **Static Analysis:** produce deeper repository-level engineering observations.
2. **Engineering Reports:** present findings as actionable engineering reports.
3. **Job Orchestration:** coordinate analysis if work becomes long-running.
4. **Deployment:** run RepoPilot outside local development.

## Engineering Principles

- Implement one approved milestone at a time; never jump ahead.
- Keep routers, schemas, services, and UI components modular.
- Prefer reusable components and clean, type-safe code.
- Do not introduce paid APIs unless explicitly requested.
- Keep documentation accurate as behavior changes.
- Never commit automatically; suggest a commit message and wait for approval.
- Verify implementation before considering a milestone complete.

## Coding Standards

- **Frontend:** typed API data, focused React components, accessible responsive Tailwind UI, explicit network states.
- **Backend:** thin FastAPI routes, Pydantic contracts, isolated services, clear errors, and meaningful tests.
- **Documentation:** concise Markdown aligned with implemented behavior.

## Current Limitations

RepoPilot does not yet provide repository cloning, source-code execution, authentication, persistence, background workers, AI analysis, deep static analysis, engineering reports, or deployment configuration. The GitHub integration is read-only and only inspects public metadata, language counts, and root-level entry names.

## Instructions for Future Codex Sessions

Before making changes, every new session must:

1. Read this file first.
2. Read `README.md`, `docs/API.md`, `docs/ARCHITECTURE.md`, and `docs/ROADMAP.md`.
3. Analyze the repository and summarize its understanding.
4. Wait for user approval before implementing the next milestone.

Maintain this file as the canonical onboarding reference throughout the project lifecycle.
