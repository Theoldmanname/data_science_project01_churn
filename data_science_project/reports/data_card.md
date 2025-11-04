# Data Card

## Dataset Snapshot
- **Asset name:** `training_master_dataset.csv`
- **Rows:** 20,040 subscribers
- **Columns:** 30 (demographics, billing, usage, sentiment, credit posture, churn outcomes)
- **Primary key candidate:** `customer_id` (I observed 40 exact duplicates in the raw feed and deduplicated downstream)

## Source and Lineage
- **System of record:** Joined extracts from telecom CRM, billing, network analytics, support ticketing, and credit systems.
- **Collection cadence:** Monthly snapshot on the first business day capturing active and recently churned subscribers for a rolling 24 months.
- **Engineering path:** Feeds land in the enterprise lake, align on naming, currency, geocoding, then publish to this CSV. I relocated the file to `data/raw/` and track processing outputs in `data/processed/`.
- **Reliability:** High for structured metrics (billing, usage, churn); medium for self-reported attributes (income, satisfaction). Text reviews are lightly cleaned.

## Usage Guidance
- Deduplicate `customer_id` before modelling or aggregation.
- Handle missingness explicitly (see table below) according to the analytical context.
- Parse `signup_date` and `last_seen` as day-first dates.
- Monetary values (charges, income, spend) are denominated in USD equivalents.

## Data Dictionary
| Field | Description | Type | Expected Values / Range | Notes |
| --- | --- | --- | --- | --- |
| `customer_id` | Subscriber identifier | integer | 1 to 20,000 | 40 duplicated rows in raw export |
| `signup_date` | Service activation date | date | 2014-01-01 to 2025-01-31 | No nulls |
| `last_seen` | Most recent billing/support activity | date | 2020-01-01 to 2025-01-31 | No nulls |
| `age` | Age in years | integer | 18 to 77 | Adult population |
| `gender` | Gender | categorical | Female, Male, Other | Complete coverage |
| `province` | Province of residence | categorical | Zimbabwe provinces | Used for geo clustering |
| `lat`, `lng` | Lat/lon centroid | float | -21.63 to -16.15 / 26.79 to 33.35 | Matches provincial bounds |
| `plan_type` | Marketing package tier | categorical | Prepaid, Premium, Postpaid | |
| `contract` | Contract commitment | categorical | Month-to-Month, One Year, Two Year | |
| `payment_method` | Billing channel | categorical | Cash, Credit Card, Debit Card, EcoCash, missing | 399 blanks |
| `device_type` | Primary ecosystem | categorical | Android, iOS, Web | |
| `has_app` | Mobile app installed | binary int | 0/1 | |
| `has_international_plan` | International calling bundle | binary int | 0/1 | |
| `tenure_months` | Tenure in months | integer | 0 to 36 | Capped at 3 years |
| `monthly_charges` | Latest monthly charge (USD) | float | 5.00 to 78.45 | |
| `total_charges` | Lifetime charges (USD) | float | 0.00 to 1476.66 | |
| `support_tickets_last_6mo` | Tickets in last 6 months | integer | 0 to 8 | |
| `data_usage_gb` | Avg monthly data usage | float | 0.21 to 23.28 GB | 778 nulls |
| `calls_per_month` | Voice calls per month | integer | 19 to 67 | |
| `messages_per_month` | Messages per month | integer | 58 to 114 | |
| `avg_session_minutes` | Avg session length | float | 4.6 to 48.3 | 658 nulls |
| `credit_score` | Credit bureau score | float | 418.5 to 822.5 | 969 nulls |
| `income` | Annual income (USD) | float | 952.57 to 14364.00 | 1,576 nulls |
| `late_payments` | Historical late payments | integer | 0 to 8 | |
| `satisfaction_score` | Likert score (1-5) | integer | 2 to 5 | |
| `churned` | Churn indicator | binary int | 0/1 | |
| `defaulted_loan` | Device loan default flag | binary int | 0/1 | |
| `next_month_spend` | Forecast spend (USD) | float | 0.00 to 85.65 | |
| `review_text` | Latest customer review | text | 12 templated phrases | 204 nulls |

## Data Quality Observations
- Missingness concentrates in financial posture (`income`, `credit_score`) and engagement telemetry (`data_usage_gb`, `avg_session_minutes`).
- Payment method blanks likely indicate offline cash payments.
- Review text is templated; NLP enrichment would require external data.
- 40 duplicated rows in raw export were deduplicated before modelling.

## Validation and Monitoring
- Pandera schema lives in `src/utils/schema.py` and enforces data types, categorical domains, ranges, and uniqueness on `customer_id`.
- `data_science_project/notebooks/02_data_quality.ipynb` re-runs validations and profiling as part of my quality CI.
- I refresh the profiling report (`reports/eda_report.html`) alongside new ingests to monitor drift.

## Compliance and Privacy
- Location plus usage metrics can identify individuals; any external sharing should anonymise or aggregate.
- Credit score and income fields follow internal governance; deployments should respect financial data policies.
