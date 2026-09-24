# A Supervised Machine Learning-Based Reputation Scoring Framework for Fraud Detection in Distributed Sales Agent Networks

## Project Description

This project implements a machine learning-based reputation scoring
framework for analysing sales-agent behavioural activity recorded in
Sales CRM data, targeting the Kenyan agency banking, insurance, and
fintech context.

The system derives agent-level behavioural features from CRM activity
records, applies synthetically injected suspicious-behaviour labels,
trains supervised machine learning models, and generates agent-level
risk and reputation scores for review by compliance officers.

## Machine Learning Models

- Logistic Regression
- Random Forest

## Technology Stack

- Python
- Pandas / Scikit-Learn
- FastAPI
- PostgreSQL
- Amazon S3
- Amazon SageMaker
- HTML / CSS / JavaScript (dashboard)

## System Users

- Administrator
- Compliance Officer

## Dataset

Sample Sales CRM Dataset (`user.csv`, `lead.csv`, `tasks.csv`), with
synthetically injected fraud labels. See `docs/data-preparation.md`
for the full inspection findings.

## Project Structure

```text
backend/     FastAPI application (routes, services, models)
ml/          Data preprocessing, feature engineering, training, scoring
data/
  raw/       Original CRM extracts (not committed to Git)
  processed/ Cleaned / feature-engineered datasets (not committed to Git)
database/    Schema and migration scripts
dashboard/   Frontend (HTML/CSS/JS)
tests/       Unit and integration tests
docs/        Data preparation notes, Chapter 5 evidence log
scripts/     Automation scripts (setup, run backend, prepare data)
```

## Getting Started

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Then visit `http://127.0.0.1:8000/docs`.

## Current Development Stage

**Sprint 1 — Data Preparation and Development Environment Setup**

| Task | Status |
| --- | --- |
| Create project repository | done |
| Create project folder structure | done |
| Create Python virtual environment | pending |
| Install dependencies | pending |
| Create requirements.txt | done |
| Create .gitignore | done |
| Create .env.example | done |
| Create README | done |
| Initialise Git | pending |
| Prepare CRM dataset | pending |
| Inspect CRM columns | pending |
| Check missing values | pending |
| Check duplicates | pending |
| Identify agent/lead/activity relationships | pending |
| Create initial FastAPI application | pending |
| Verify /health endpoint | pending |
| Create basic automation scripts | pending |
| Commit progress to Git | pending |
| Create GitHub repository | pending |
| Prepare PostgreSQL | pending |
| Prepare S3 / SageMaker | pending |
