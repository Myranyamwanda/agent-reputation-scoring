# Data Preparation

## Dataset
Name: Sample Sales CRM Dataset
Source: Kaggle-style Salesforce CRM export (provided dataset)
File format: CSV

## Tables/Files in scope
1. user.csv - 275 rows, 0 missing values, 0 duplicates
2. lead.csv - 14,000 rows, 0 duplicates
3. tasks.csv - 110,000 rows, 0 duplicates

The archive also contains account.csv, contact.csv, event.csv,
opportunity.csv, order.csv and order_items.csv. These are outside the
project's documented Delimitations and are not used.

## Records
user.csv: 275
lead.csv: 14,000
tasks.csv: 110,000

## Important identifiers
Agent identifier: user.id (role in {AE, SDR, BDR, Manager, Director})
  - AE: 98, SDR: 74, BDR: 74, Manager: 28, Director: 1
Lead identifier: lead.id ; lead.owner_id -> user.id (14,000/14,000 match)
Activity/task identifier: tasks.id ; tasks.owner_id -> user.id (110,000/110,000 match)

## Task polymorphic references (Salesforce-style)
tasks.who_id: 60,372 rows prefixed "003" (Contact - out of scope),
              49,628 rows prefixed "00Q" (Lead - in scope)
tasks.what_id: 49,596 rows prefixed "006" (Opportunity - out of scope),
               49,555 rows prefixed "001" (Account - out of scope),
               10,849 missing
Decision: who_id/what_id are treated generically for behavioural
counting (was this task linked to something) rather than resolved to
a specific Lead/Account/Opportunity, consistent with the project's
Delimitations (contact.csv, opportunity.csv, account.csv excluded).

## Temporal fields
Date: tasks.activity_date (when the task occurred - use this for all
      time-based features)
Also present: tasks.created_date (record-creation date - not used for
      behavioural timing)

## Data quality
Missing values: tasks.what_id has 10,849 nulls; user.csv and lead.csv
      have no missing values
Duplicate records: none found in any of the three files
Invalid records: none identified so far

## Agent population scope - decided
AE (Account Executive) is included in the scored agent population,
alongside SDR and BDR. AE is the largest single role group (98/275,
~36%), and there is no data-quality or relational reason to exclude
it - AE rows have the same owner_id linkage to lead.csv and
tasks.csv as every other role. Manager (28) and Director (1) are
excluded: they are supervisory roles, not individual sales agents
generating the CRM activity this framework scores.

Scored population: AE (98) + SDR (74) + BDR (74) = 246 agents.

Action: the Methodology and Delimitations text must be updated to
read "Sales Development Representatives (SDR), Business Development
Representatives (BDR), and Account Executives (AE)" wherever it
currently says "SDR and BDR" only.

## Planned transformations
1. Filter the agent population to role in {AE, SDR, BDR} (Manager
   and Director excluded per the decision above)
2. Aggregate tasks by owner_id (agent) using activity_date for all
   temporal features
3. Engineer behavioural features: activity_volume, task_frequency,
   active_days, activity_velocity, leads_handled, temporal_concentration
4. Apply synthetic suspicious-behaviour labels to a controlled subset
