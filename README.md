# 🚀 RepoPilot

<div align="center">

**An intelligent GitHub repository analysis platform that generates engineering insights, repository health metrics, and technology detection without cloning or executing repository code.**

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-black?logo=next.js)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-2088FF?logo=github-actions)

</div>

---

# 📖 Overview

RepoPilot is a full-stack software engineering tool that analyzes **public GitHub repositories** using the **GitHub REST API** to generate structured engineering insights.

Unlike traditional repository analysis tools, RepoPilot **never clones repositories and never executes repository code**. Instead, it performs a **read-only inspection** by collecting repository metadata and selected high-signal files to generate deterministic engineering reviews.

The platform helps developers quickly understand a repository's architecture, technology stack, documentation quality, CI/CD readiness, containerization support, maintainability, and overall engineering health.

---

# ✨ Features

## 🔍 Repository Analysis

- Analyze any public GitHub repository
- Repository metadata extraction
- Programming language distribution
- Repository structure visualization
- Default branch detection
- Repository statistics

---

## 🏗 Engineering Review

Automatically generates:

- Architecture summary
- Technology stack detection
- Repository health score
- Engineering findings
- Improvement recommendations
- Evidence-backed observations

---

## 🧠 Technology Detection

Automatically detects technologies using repository evidence such as:

- package.json
- requirements.txt
- pyproject.toml
- Dockerfile
- docker-compose.yml
- GitHub Actions workflows
- README
- Cargo.toml
- Go modules
- Maven
- Gradle
- Ruby Gemfiles

---

## 📊 Repository Health Assessment

Evaluates engineering quality based on:

- Documentation
- Project structure
- Configuration
- Containerization
- CI/CD
- Testing

---

## ⚡ GitHub API Integration

Secure integration with GitHub REST API including:

- Repository metadata
- Languages
- Repository tree
- Root contents
- Selected evidence files
- Authenticated requests
- Rate limit monitoring

---

## 🔐 Secure Authentication

Supports authenticated GitHub API access using Personal Access Tokens.

Benefits include:

- Increased API quota (typically 5,000 requests/hour)
- Secure environment-based configuration
- Better reliability for repository analysis

---

## 🐳 Docker Support

Fully containerized application using:

- Docker
- Docker Compose

Run the complete project with a single command.

---

## ⚙ CI/CD

Integrated GitHub Actions workflow for:

- Backend tests
- Frontend build
- Dependency caching
- Continuous Integration

---

# 🏛 System Architecture

```
                    +-----------------------+
                    |     Next.js Client    |
                    +-----------+-----------+
                                |
                                |
                         REST API Request
                                |
                                ▼
                    +-----------------------+
                    |   FastAPI Backend     |
                    +-----------+-----------+
                                |
                                |
                     Repository Inspection
                                |
                                ▼
                    +-----------------------+
                    | GitHub REST API       |
                    +-----------------------+
```

---

# ⚙ How It Works

RepoPilot follows a deterministic inspection pipeline:

1. Validate GitHub repository URL
2. Normalize repository URLs (supports `.git` and trailing slashes)
3. Retrieve repository metadata
4. Fetch programming language statistics
5. Read repository structure
6. Traverse repository tree
7. Collect high-signal evidence files
8. Detect technologies
9. Generate engineering review
10. Calculate repository health
11. Return structured analysis

---

# 🛠 Tech Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## Backend

- Python
- FastAPI
- Uvicorn

## APIs

- GitHub REST API

## DevOps

- Docker
- Docker Compose
- GitHub Actions

---

# 📁 Project Structure

```
RepoPilot
│
├── backend
│   ├── api
│   ├── services
│   ├── schemas
│   ├── tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── app
│   ├── components
│   ├── public
│   ├── Dockerfile
│   └── package.json
│
├── .github
│   └── workflows
│
├── docker-compose.yml
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker Desktop (optional)
- GitHub Personal Access Token (recommended)

---

## Clone Repository

```bash
git clone https://github.com/Armash-Sidd/RepoPilot.git

cd RepoPilot
```

---

# Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```
GITHUB_TOKEN=your_personal_access_token
```

Run

```bash
uvicorn main:app --reload
```

---

# Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# Docker Setup

Run the complete application:

```bash
docker compose up --build
```

Frontend

```
http://localhost:3000
```

Backend

```
http://localhost:8000
```

API Documentation

```
http://localhost:8000/docs
```

---

# API Endpoint

### Analyze Repository

```
POST /api/analyze
```

Example Request

```json
{
  "repository_url": "https://github.com/octocat/Hello-World"
}
```

---

# Error Handling

RepoPilot gracefully handles:

| Status | Meaning |
|---------|---------|
| 404 | Repository not found |
| 429 | GitHub API rate limit exceeded |
| 502 | GitHub upstream error |
| 504 | GitHub timeout |

---

# Engineering Highlights

- Read-only repository inspection
- No repository cloning
- No code execution
- Deterministic engineering review
- Modular service architecture
- Layered backend design
- Typed API schemas
- Secure environment configuration
- Dockerized deployment
- Continuous Integration

---

# Future Improvements

- Repository comparison
- Organization-level analysis
- Repository history insights
- Exportable engineering reports
- Repository trend analysis
- AI-assisted code quality recommendations

---

# Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

# License

This project is licensed under the MIT License.

---

# Author

**Armash Siddiqui**

Computer Science Engineering Student

Passionate about Software Engineering, AI, and Developer Tools.
