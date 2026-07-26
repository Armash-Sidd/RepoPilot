"""Application factory for the RepoPilot API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router


def create_app() -> FastAPI:
    """Create the API application and attach its HTTP interfaces."""
    app = FastAPI(title="RepoPilot API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=False,
        allow_methods=["POST"],
        allow_headers=["Content-Type"],
    )
    app.include_router(api_router)
    return app
