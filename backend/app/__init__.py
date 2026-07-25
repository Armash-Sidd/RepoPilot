"""Application factory for the FastAPI service scaffold."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create the application without attaching business capabilities yet."""
    return FastAPI(title="RepoPilot API", version="0.1.0")

