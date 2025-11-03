# Data Science Case Study: From Data Audit to Decision Insights

**TL;DR (Executive Summary)**  
- Audited and cleaned a 20k-row telecom dataset, uplifting data trust and documentation from scratch.  
- Quantified churn drivers: mobile app adoption reduces churn by ~11 pts; heavy support usage lifts risk by ~50%.  
- Combined statistical tests, clustering, and propensity scoring to spotlight 5.5k at-risk subscribers.  
- Built executive dashboards and a retention playbook with concierge outreach, app incentives, and loyalty perks.  
- Delivered an insight pack (PDF + interactive visuals) that translates analytics into a 4-week pilot roadmap.

---

## The Journey

### Phase 1–2: Foundation and Data Contracts  
I repositioned a raw CSV into a professional project structure, documented lineage in a data card, created a profiling report, and built Pandera schema checks so stakeholders could trust every field.

### Phase 3–4: Cleaning & Statistical Evidence  
Segment-aware imputations, consistency fixes, and feature engineering produced a clean 37-column dataset. Statistical testing (chi-square, ANOVA, z-tests, correlation CIs) quantified where churn really diverges—mobile app usage, support load, and province clusters.

### Phase 5–6: Modeling, Clustering, Personas  
A logistic baseline vs driver model highlighted actionable lift (+0.02 AUC via support/app signals). K-means clustering (k=3) revealed three personas: Premium Data Power Users, Low-Spend Stable Users, and Value Seekers—each with conversion plays.

### Phase 7: Dashboard Storytelling  
The Plotly-powered notebook dashboard surfaces KPIs (churn, app adoption, high-risk cohort size) with interactive plan/province filters. Visuals include churn-by-plan, app adoption impact, churn/spend timelines, and geospatial hotspots.

### Phase 8: Recommendation Pack  
An insight PDF distills the narrative: 5-line TL;DR, thematic insights, embedded figures, and a playbook (concierge outreach, app campaigns, ticket deflection, dashboard cadences). Limitations and next steps keep the story honest and forward-looking.

---

## Key Insights

- **Retention:** Mobile app users churn 23.0% vs 33.7% for non-app customers; high-support customers churn 34.2% vs 25.2% otherwise.  
- **Revenue:** Premium Data Power Users (~19% of base) forecast $70+ next-month spend, demanding loyalty protection.  
- **Operations:** Matabeleland North & Manicaland show hotspot churn; mid-2025 exhibited churn/spend swings highlighting monitoring needs.  
- **Segments:** 5,557 accounts fall into high-risk retention segments (low app adoption, high ticket volume) ready for targeted concierge pilots.

---

## Recommended Actions

1. **Launch a 4-week concierge retention pilot** for the 5.5k high-risk customers; track retention vs control weekly.  
2. **Expand mobile app incentives** (data/top-up rewards) to convert the remaining 22% of offline customers.  
3. **Deploy proactive support alerts** leveraging ticket velocity to intervene before churn spikes.  
4. **Protect Premium Data Power Users** with loyalty bundles and personalised care to safeguard $70+ ARPU.  
5. **Operationalise the dashboard** inside revenue-ops cadences to monitor churn/spend, cluster mix, and pilot KPIs.

---

## Limitations & Next Steps

- Current modeling is snapshot-based; build longitudinal pipelines to capture seasonality and campaign effects.  
- Logistic propensity lift (+0.02 AUC) is modest—evaluate gradient boosting or survival models for stronger ranking.  
- Ticket taxonomy lacks qualitative root causes; integrate NLP on support notes for deeper insights.  
- Pricing elasticity isn’t modeled yet—blend spend-to-income ratio into future offers/testing.

---

## Explore the Assets

- **Interactive Dashboard Notebook:** `notebooks/06_dashboard_reporting.ipynb`  
- **Retention Segmentation Notebook:** `notebooks/05_segmentation_profiles.ipynb`  
- **Insight Summary PDF:** `reports/insight_summary.pdf` (executive-ready)  
- **Segmented Dataset:** `data/processed/segmented.csv` (clusters + propensity + recommended actions)

Let’s connect if you’d like a live walkthrough or to adapt this approach to your customer base.
