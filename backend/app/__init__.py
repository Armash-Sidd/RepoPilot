"""Application factory for the RepoPilot API."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.router import api_router
from app.services.github_repository_client import GitHubRepositoryClient

logger = logging.getLogger(__name__)
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Load local configuration and report whether GitHub authentication is active."""
    load_dotenv(ENV_FILE)
    authentication_status = "enabled" if GitHubRepositoryClient().authenticated else "disabled"
    logger.info("GitHub authentication: %s", authentication_status)
    yield


def create_app() -> FastAPI:
    """Create the API application and attach its HTTP interfaces."""
    app = FastAPI(title="RepoPilot API", version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app
