"""Top-level route registration for the RepoPilot API."""

from fastapi import APIRouter

from app.api.routes.analyze import router as analyze_router

api_router = APIRouter(prefix="/api")
api_router.include_router(analyze_router)
