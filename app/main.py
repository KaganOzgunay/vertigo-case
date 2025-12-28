from fastapi import FastAPI
from app.routers import clans
from app.database import engine, Base
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="REST API for managing game clans"
)


@app.on_event("startup")
def startup():
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


app.include_router(clans.router)
