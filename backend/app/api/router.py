"""Top-level route registration for the RepoPilot API."""

from fastapi import APIRouter

from app.api.routes.analyze import router as analyze_router
from app.api.routes.github import router as github_router

api_router = APIRouter(prefix="/api")
api_router.include_router(analyze_router)
api_router.include_router(github_router)
