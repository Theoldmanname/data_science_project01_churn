# From Raw Data to Insight - A Full-Stack Data Science Exploration

> **Fast Links**
> - **Live Dashboard:** https://datascienceproject01churn-87qsxh7zalazvu6bvwnyg7.streamlit.app
> - **Project Hub (GitHub Pages):** https://Theoldmanname.github.io/data_science_project01_churn/
> - **Insight Summary PDF:** https://Theoldmanname.github.io/data_science_project01_churn/insight_summary.pdf
> - **LinkedIn Article:** https://www.linkedin.com/pulse/data-science-case-study-from-data-audit-decision-insights-*
> - **Segmented Dataset:** https://Theoldmanname.github.io/data_science_project01_churn/segmented.csv
> - [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Theoldmanname/data_science_project01_churn/HEAD?labpath=data_science_project%2Fnotebooks%2F03_eda_descriptive.ipynb) &nbsp; [View on nbviewer](https://nbviewer.org/github/Theoldmanname/data_science_project01_churn/blob/master/data_science_project/notebooks/03_eda_descriptive.ipynb)

## Problem Context
I analysed a nationwide Zimbabwean telecom subscriber base to understand churn and monetisation levers. The project documents how I audited raw feeds, engineered reliable data assets, and built an executive-ready retention story.

## Data Sources
- `data/raw/training_master_dataset.csv`: 20k subscriber-level records covering demographics, billing, usage, sentiment, credit posture, and churn outcomes.
- Processed artefacts in `data/processed/` store my cleaned dataset, churn propensity scores, cluster labels, and pilot targeting files.

## What I Did
1. **Phase 1-2** – Structured the repository, authored the data card, and locked schema expectations with Pandera plus automated profiling.
2. **Phase 3** – Cleaned the feed, imputed targeted attributes, enforced consistency checks, and engineered modelling features.
3. **Phase 4-5** – Ran exploratory analysis and statistical tests (chi-square, ANOVA, correlation CIs) to quantify churn drivers.
4. **Phase 6** – Built churn propensity scores, performed customer clustering, and designed retention segments.
5. **Phase 7-8** – Crafted the Plotly/Streamlit dashboard, packaged insights in an executive PDF, and wrote the LinkedIn case study.
6. **Phase 9** – Finalised reproducibility (requirements file, validation notebook, documentation polish).

## Key Insights
- Mobile app adoption drops churn from 33.7% to 23.0%, while support-heavy cohorts churn about 50% more.
- 5.5k customers fall into high-risk segments defined by heavy support needs and low digital adoption.
- Premium Data Power Users (19% of the base) forecast $70+ in monthly spend yet sit at moderate churn risk, warranting loyalty perks.
- Matabeleland North and Manicaland exhibit hotspot churn requiring provincial retention squads.

## Repository Structure
```
data_science_project/
|-- README.md
|-- requirements.txt
|-- data/
|   |-- raw/
|   `-- processed/
|-- notebooks/
|   |-- 01_data_dictionary.ipynb
|   |-- 02_data_quality.ipynb
|   |-- 03_eda_descriptive.ipynb
|   |-- 04_statistical_analysis.ipynb
|   |-- 05_segmentation_profiles.ipynb
|   `-- 06_dashboard_reporting.ipynb
|-- reports/
|   |-- data_card.md
|   |-- eda_report.html
|   |-- segment_summary.csv
|   |-- linkedin_article.md
|   `-- insight_summary.pdf
|-- src/
|   |-- models/
|   `-- utils/
```

## Reproducibility Notes
- I developed against Python 3.10+ with dependencies captured in `requirements.txt`.
- Install with `pip install -r requirements.txt` and validate schema via `notebooks/02_data_quality.ipynb`.
- I regenerate the clean dataset via `src/pipelines/preprocessing.py`; deployment notes live in [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md).

## Re-running the Analysis
1. Create a virtual environment (`python -m venv .venv`) and activate it.
2. Install dependencies: `pip install -r requirements.txt`.
3. Execute notebooks sequentially or run the scripts in `src/` for automation (`python src/pipelines/preprocessing.py`, `python src/models/driver_experiments.py`).
4. Review the final assets: dashboard notebook, `reports/insight_summary.pdf`, and `reports/linkedin_article.md`.
