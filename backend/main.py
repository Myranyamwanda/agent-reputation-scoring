from fastapi import FastAPI

app = FastAPI(
    title="Agent Reputation Scoring Framework",
    description="Machine learning-based reputation scoring system for sales agents",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Agent Reputation Scoring Framework API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
