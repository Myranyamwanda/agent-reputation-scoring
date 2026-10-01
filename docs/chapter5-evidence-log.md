# Chapter 5 Implementation Evidence Log

Record one entry per significant development step. This becomes the
raw material for Chapter 5.3 (Implementation) - capture it as you go,
not from memory later.


### 19 September 2026 - Sprint 1

What I implemented: Project directory structure, Python virtual
environment, initial FastAPI application, and the CRM dataset
inspection script. Configured Git version control and created the
initial repository commits.

How I implemented it: Created the backend/ml/data/database/dashboard/
tests/docs/scripts layout; wrote ml/src/data_preprocessing.py to
inspect user.csv, lead.csv and tasks.csv (shape, dtypes, missing
values, duplicates, and the owner_id/who_id/what_id relationships);
wrote backend/main.py with a health-check endpoint.

Screenshot: FastAPI /docs Swagger UI and /health endpoint verified
in browser; terminal output of the inspection script captured below.

Git commit: 4208042 "Set up project structure and development
environment"; d479c97 "Add CRM dataset inspection findings and
Chapter 5 evidence log"

Result: Inspection confirmed 275 users (AE 98, SDR 74, BDR 74,
Manager 28, Director 1), 14,000 leads (100% owner_id match to
user.id), and 110,000 tasks (100% owner_id match to user.id). No
duplicates in any of the three files. tasks.what_id has 10,849 nulls.
who_id/what_id are Salesforce-style polymorphic references spanning
Lead/Contact and Opportunity/Account respectively. FastAPI backend
verified running locally (GET / and GET /health both returned
successfully; /docs Swagger UI confirmed in browser).

Problem/error encountered: The provided archive contains six
additional CRM tables (account, contact, event, opportunity, order,
order_items) beyond the three named in the Delimitations.

How I fixed it: Confirmed scope stays to user.csv/lead.csv/tasks.csv
per the existing Delimitations; documented the polymorphic reference
handling decision in docs/data-preparation.md rather than expanding
scope to resolve Contact/Account/Opportunity records.

---

### 20 September 2026 - Sprint 1 (environment preparation)

What I implemented: PostgreSQL 18 database and an Amazon S3 bucket,
completing the "relevant data, databases, APIs, files or other
resources prepared as applicable" requirement for Sprint 1.

How I implemented it: Installed PostgreSQL 18 locally and created the
agent_reputation database; created an S3 bucket
(agent-reputation-scoring-myra) in the eu-north-1 region via the AWS
Console; updated .env with the real DATABASE_URL, AWS_REGION and
S3_BUCKET values (kept out of Git via .gitignore).

Screenshot: AWS S3 console showing successful bucket creation;
psql -l output showing the agent_reputation database.

Git commit: N/A - .env and local database/bucket configuration are
not committed (secrets and environment-specific values are
intentionally excluded per .gitignore).

Result: DATABASE_URL, AWS_REGION and S3_BUCKET are all live and
verified. No table schemas or SageMaker training jobs yet - both are
Sprint 2+ work once feature engineering and model training begin.

Problem/error encountered: Initial PostgreSQL installation via
winget failed with a 403 error from the vendor's download server.

How I fixed it: Installed PostgreSQL 18 directly from the official
installer at postgresql.org/download/windows instead of via winget.
