from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = BASE_DIR / "dashboard"

app = FastAPI(
    title="Agent Reputation Scoring Framework",
    description="Machine learning-based reputation scoring system for sales agents",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(DASHBOARD_DIR)), name="static")


@app.get("/")
def root():
    return FileResponse(DASHBOARD_DIR / "index.html")


@app.get("/login")
def login_page():
    return FileResponse(DASHBOARD_DIR / "index.html")


@app.get("/signup")
def signup_page():
    return FileResponse(DASHBOARD_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
