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


## Feature engineering - implemented

ml/src/feature_engineering.py aggregates tasks.csv and lead.csv up to
one row per agent (246 rows, matching the AE/SDR/BDR scoring
population - confirmed independently, since Manager and Director
generate zero task activity in the raw data).

Features produced:
- activity_volume: total task count for the agent
- active_days: distinct calendar days with task activity
- task_frequency: activity_volume / active_days (tasks per active day)
- activity_velocity: activity_volume / full tenure span in days
  (tasks per calendar day, including idle stretches)
- leads_handled: count of leads owned by the agent (lead.csv)
- temporal_concentration: coefficient of variation (std/mean) of
  weekly task counts - measures burstiness of activity over time

Output: data/processed/agent_features.csv (not committed - gitignored)


## Time-windowed features - added for sample size

The agent-lifetime feature set (246 rows) falls short of standard
events-per-variable guidance for reliable model training (Peduzzi et
al.: ~10-20 minority-class events per predictor; with 6 features that
is 60-120 minimum, requiring 300-600+ total agents at a realistic
15-20% injection rate - more than the 246 available).

To address this without needing more real agents, features are also
computed at agent-month granularity: one row per agent per month they
had CRM activity, instead of one row per agent for their whole
history. This produces 12,003 rows (AE 4,751 / SDR 3,626 / BDR 3,626),
comfortably clearing the EPV threshold even at conservative injection
rates, and better matches how fraud detection typically works - as a
change in an agent's own behaviour over time, not a single lifetime
average.

activity_velocity is redefined at this granularity as
activity_volume / calendar days in that month (rather than the
agent's full observed date-range), since each row is already scoped
to one month.

Both feature sets are produced by ml/src/feature_engineering.py:
- data/processed/agent_features.csv (agent-lifetime, 246 rows)
- data/processed/agent_month_features.csv (agent-month, 12,003 rows -
  primary dataset for model training)

## Synthetic suspicious-behaviour labels - added for Sprint 2

No ground-truth fraud label exists in the source data (user.csv,
lead.csv, tasks.csv). This is expected for this kind of academic
fraud-detection project - real investigated-fraud outcomes are not
available. Following standard practice in fraud/anomaly-detection
research (e.g. the CERT Insider Threat Dataset, which also relies on
synthetically injected malicious behaviour), a synthetic
`is_suspicious` label was derived on the agent-month feature set
(see ml/src/label_generation.py) using two named behavioural rules:

1. Bursty behaviour: activity_velocity and temporal_concentration
   both at or above their 80th percentile.
2. Padding behaviour: activity_volume at or above its 75th
   percentile, with zero leads_handled in that month.

The two rules are combined with OR logic, giving a combined flag rate
of approximately 9.2% of agent-month rows. A random 3% label-noise
step was then applied (fixed seed, independent of the rules) to avoid
a label that is a deterministic function of the features, and to more
realistically simulate imperfect real-world fraud labeling. The final
positive rate is approximately 11.5%.

This is an explicit, documented scope limitation: the labels reflect
a behavioural heuristic, not real investigated fraud outcomes, and
this will be stated plainly in the Chapter 5/6 write-up.
