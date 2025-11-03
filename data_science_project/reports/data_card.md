# Data Card

## Dataset Snapshot
- **Asset name:** `training_master_dataset.csv`
- **Rows:** 20,040 subscribers (Zimbabwe telecom market)
- **Columns:** 30 features spanning demographics, billing, usage, sentiment, and financial risk
- **Primary key candidate:** `customer_id` (noting 40 duplicate records requiring remediation)

## Source and Lineage
- **System of record:** Consolidated export from telecom CRM (subscriber profiles), billing platform (charges, payment history), network analytics warehouse (usage, engagement), and customer support ticketing.
- **Collection cadence:** Snapshotted monthly on the first business day; each extract contains all active and recently churned customers for the rolling 24 months.
- **Data engineering path:** Raw feeds land in the enterprise data lake, undergo standardization (field naming, currency conversion to USD equivalent, geocoding), and are joined on customer_id prior to this CSV export.
- **Reliability:** High for structured metrics (billing, usage, churn); medium for self-reported attributes (income, satisfaction). Text reviews are lightly cleaned (stop-word removal, offensive language masked).

## Usage Guidance
- Apply deduplication on `customer_id` before modeling or aggregate analysis.
- Impute or exclude features with missingness (see table) based on analysis context.
- Dates are in `YYYY-MM-DD` ISO format after parsing; ingest as timezone-naive local dates.
- Monetary values (charges, income, spend) are denominated in USD equivalents.

## Data Dictionary
| Field | Description | Type | Expected Values / Range | Data Quality Notes |
| --- | --- | --- | --- | --- |
| `customer_id` | Unique subscriber identifier from CRM | integer | 1 to 20,000 | 40 duplicate ids detected (0.2%); no nulls |
| `signup_date` | Date customer activated first service | date (object) | 2014-01-01 to 2025-01-31 | No nulls; convert to datetime |
| `last_seen` | Most recent interaction or billing date captured | date (object) | 2020-01-01 to 2025-01-31 | No nulls; parse to datetime |
| `age` | Customer age in completed years | integer | 18 to 77 | No nulls; values within adult range |
| `gender` | Self-reported gender | categorical | Female, Male, Other | Complete coverage |
| `province` | Province of primary residence (Zimbabwe) | categorical | Bulawayo, Harare, Manicaland, Mashonaland Central, Mashonaland East, Mashonaland West, Masvingo, Matabeleland North, Matabeleland South, Midlands | No nulls |
| `lat` | Latitude of residence centroid | float | -21.63 to -16.15 | No nulls; matches Zimbabwe bounds |
| `lng` | Longitude of residence centroid | float | 26.79 to 33.35 | No nulls; matches Zimbabwe bounds |
| `plan_type` | Marketing package tier | categorical | Prepaid, Premium, Postpaid | No nulls |
| `contract` | Contract commitment term | categorical | Month-to-Month, One Year, Two Year | No nulls |
| `payment_method` | Preferred billing payment channel | categorical | Cash, Credit Card, Debit Card, EcoCash | 399 nulls (1.99%) |
| `device_type` | Primary device ecosystem used | categorical | Android, iOS, Web | No nulls |
| `has_app` | Indicator if mobile app is installed | binary integer | 0 or 1 | No nulls |
| `has_international_plan` | Flag for international calling bundle | binary integer | 0 or 1 | No nulls |
| `tenure_months` | Months elapsed since signup | integer | 0 to 36 | No nulls; capped at 3-year window |
| `monthly_charges` | Latest monthly service charges (USD) | float | 5.00 to 685.08 | No nulls |
| `total_charges` | Cumulative lifetime charges (USD) | float | 0.00 to 4,214.07 | No nulls |
| `support_tickets_last_6mo` | Support cases filed in past 6 months | integer | 0 to 8 | No nulls |
| `data_usage_gb` | Average monthly data consumption | float | 0.21 to 223.52 GB | 778 nulls (3.88%) |
| `calls_per_month` | Voice calls per month | integer | 16 to 90 | No nulls |
| `messages_per_month` | SMS/MMS messages per month | integer | 43 to 139 | No nulls |
| `avg_session_minutes` | Mean session length in minutes | float | 1.00 to 58.35 | 658 nulls (3.28%) |
| `credit_score` | Credit bureau score | float | 334 to 850 | 969 nulls (4.84%); numeric but can be cast to int |
| `income` | Annual household income (USD) | float | 953 to 170,382 | 1,576 nulls (7.87%); positively skewed |
| `late_payments` | Historical late payment count | integer | 0 to 8 | No nulls |
| `satisfaction_score` | Likert satisfaction (1=Low, 5=High) | integer | 2 to 5 | No nulls; scale truncated at 2-5 |
| `churned` | Indicator of churn in prior month | binary integer | 0 or 1 | No nulls |
| `defaulted_loan` | Flag for default on device financing | binary integer | 0 or 1 | No nulls |
| `next_month_spend` | Forecasted spend for next month (USD) | float | 0.00 to 137.04 | No nulls; subset at zero |
| `review_text` | Latest customer review verbatim | text | 12 templated phrases | 204 nulls (1.02%); moderate repetition |

## Known Data Quality Considerations
- Missingness concentrated in financial posture (`income`, `credit_score`) and engagement telemetry (`data_usage_gb`, `avg_session_minutes`); assess imputation strategies per use case.
- Payment method blanks likely indicate cash walk-in payments not captured digitally.
- Review text is templated with limited vocabulary; enrich with additional sources for NLP tasks.
- Total of 40 exact duplicate records (entire row) suggest upstream export duplication around reporting cut-over; deduplicate prior to modeling.

## Validation and Monitoring
- Automated Pandera schema (`src/utils/schema.py`) enforces data types, categorical domains, ranges, and uniqueness on `customer_id`; current run flags 40 duplicate identifiers for remediation.
- The ydata-profiling audit (`reports/eda_report.html`) captures completeness, distributional drift signals, correlations, and text token insights for this extract.
- Re-run validation and profiling as part of every ingestion cycle to maintain auditable lineage and detect changes early.

## Compliance and Privacy
- Dataset contains personally identifiable combinations (location + usage). Apply masking and aggregation before external sharing.
- Credit score and income data should follow internal governance for financial attributes; ensure audits prior to deployment.
