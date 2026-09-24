# Chapter 5 Implementation Evidence Log

Record one entry per significant development step. This becomes the
raw material for Chapter 5.3 (Implementation) - capture it as you go,
not from memory later.

## Template

  ### [DATE] - Sprint N

  What I implemented:

  How I implemented it:

  Screenshot:

  Git commit:

  Result:

  Problem/error encountered:

  How I fixed it:

---

### 24 September 2026 - Sprint 1

What I implemented: Project directory structure, Python virtual
environment, initial FastAPI application, and the CRM dataset
inspection script. Configured Git version control and created the
initial repository commits.

How I implemented it: Created the backend/ml/data/database/dashboard/
tests/docs/scripts layout; wrote ml/src/data_preprocessing.py to
inspect user.csv, lead.csv and tasks.csv (shape, dtypes, missing
values, duplicates, and the owner_id/who_id/what_id relationships);
wrote backend/main.py with a health-check endpoint.

Screenshot: [add FastAPI /docs screenshot and terminal output of the
inspection script]

Git commit: [fill in after committing]

Result: Inspection confirmed 275 users (AE 98, SDR 74, BDR 74,
Manager 28, Director 1), 14,000 leads (100% owner_id match to
user.id), and 110,000 tasks (100% owner_id match to user.id). No
duplicates in any of the three files. tasks.what_id has 10,849 nulls.
who_id/what_id are Salesforce-style polymorphic references spanning
Lead/Contact and Opportunity/Account respectively.

Problem/error encountered: The provided archive contains six
additional CRM tables (account, contact, event, opportunity, order,
order_items) beyond the three named in the Delimitations.

How I fixed it: Confirmed scope stays to user.csv/lead.csv/tasks.csv
per the existing Delimitations; documented the polymorphic reference
handling decision in docs/data-preparation.md rather than expanding
scope to resolve Contact/Account/Opportunity records.
