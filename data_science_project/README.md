# From Raw Data to Insight - A Full-Stack Data Science Exploration

> **Fast Links**
> - **Live Dashboard:** https://datascienceproject01churn-87qsxh7zalazvu6bvwnyg7.streamlit.app
> - **Project Hub (GitHub Pages):** https://Theoldmanname.github.io/data_science_project01_churn/
> - **Insight Summary PDF:** https://Theoldmanname.github.io/data_science_project01_churn/insight_summary.pdf
> - **LinkedIn Article:** https://www.linkedin.com/pulse/data-science-case-study-from-data-audit-decision-insights-*
> - **Segmented Dataset:** https://Theoldmanname.github.io/data_science_project01_churn/segmented.csv
> - [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Theoldmanname/data_science_project01_churn/HEAD?labpath=data_science_project%2Fnotebooks%2F03_eda_descriptive.ipynb) &nbsp; [View on nbviewer](https://nbviewer.org/github/Theoldmanname/data_science_project01_churn/blob/master/data_science_project/notebooks/03_eda_descriptive.ipynb)

## Problem Context
Zimbabwean telecom operator facing multi-faceted churn risk across digital and support channels. Goal: audit data assets, understand churn drivers, segment the base, and deliver an actionable retention playbook.

## Data Sources
- `data/raw/training_master_dataset.csv` – 20k subscriber-level records (demographics, billing, usage, sentiment, credit posture, churn flags).
- Processed assets in `data/processed/` (cleaned dataset, propensity scores, clustering labels, pilot targets).

## What Was Done
1. **Phase 1-2** – Repo scaffolding, data card, Pandera contract, profiling.
2. **Phase 3** – Cleaning, imputation, consistency checks, feature engineering.
3. **Phase 4-5** – Exploratory analysis, statistical testing (chi-square, ANOVA, correlations).
4. **Phase 6** – Propensity scoring, clustering personas, retention segmentation.
5. **Phase 7-8** – Plotly dashboard, executive PDF, LinkedIn-ready story, recommendations.
6. **Phase 9** – Reproducibility polish (requirements, validation notebook, README update).

## Main Insights
- App adoption cuts churn from 33.7% to 23.0%; support-heavy cohorts churn ~50% more.
- 5.5k customers fall into high-risk retention segments combining support load and low app usage.
- Premium Data Power Users (19%) deliver the highest ARPU/spend ($70+ next month) yet remain moderate churn risk—protect with concierge incentives.
- Matabeleland North & Manicaland show hotspot churn requiring localized action.


## Repository Structure
```
data_science_project/
|-- README.md
|-- requirements.txt
|-- data/
|   |-- raw/                       # raw training dataset
|   `-- processed/                 # cleaned, scored, segmented assets
|-- notebooks/
|   |-- 01_data_dictionary.ipynb   # data dictionary & definitions
|   |-- 02_data_quality.ipynb      # schema validation / quality CI
|   |-- 03_eda_descriptive.ipynb   # exploratory visuals + narrative
|   |-- 04_statistical_analysis.ipynb
|   |-- 05_segmentation_profiles.ipynb
|   `-- 06_dashboard_reporting.ipynb
|-- reports/
|   |-- data_card.md
|   |-- eda_report.html
|   |-- segment_summary.csv
|   |--linkedin_article.md
|   `-- insight_summary.pdf
|-- src/
|   |-- models/                    # driver experiments, pipelines
|   `-- utils/                     # io, plotting, stats helpers
```

## Reproducibility
- Python 3.10+ with dependencies in `requirements.txt`.
- Run `pip install -r requirements.txt`.
- Validate schema via `notebooks/02_data_quality.ipynb` (suitable for CI).
- Clean dataset generated through `src/pipelines/preprocessing.py`.
- Ready-to-launch steps documented in [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md).

## How to Reproduce
1. `python -m venv .venv && .venv\\Scripts\\activate` (Windows) or `source .venv/bin/activate`.  
2. `pip install -r requirements.txt`.  
3. Execute notebooks in order (`01` â†’ `06`) or run scripts in `src/` for automation (`python src/pipelines/preprocessing.py`).  
4. For clustering/retention scores run `python src/models/driver_experiments.py` and the segmentation notebook.  
5. Review final assets: dashboard notebook, `reports/insight_summary.pdf`, and `reports/linkedin_article.md`.
