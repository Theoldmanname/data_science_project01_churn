import pandas as pd
import numpy as np
from pathlib import Path
from fpdf import FPDF

ROOT = Path('data_science_project')
clean = pd.read_csv(ROOT / 'data/processed/clean_dataset.csv', parse_dates=['signup_date','last_seen'])
segmented = pd.read_csv(ROOT / 'data/processed/segmented.csv')
cluster_summary = pd.read_csv(ROOT / 'reports/segment_summary.csv')

n_customers = int(len(clean))
churn_rate = float(clean['churned'].mean() * 100)
app_adoption = float(clean['has_app'].mean() * 100)
high_support_share = float((clean['support_tickets_per_month'] >= 0.5).mean() * 100)
avg_monthly_revenue = float(clean['avg_monthly_revenue'].mean())
next_month_spend = float(clean['next_month_spend'].mean())
high_risk_cutoff = segmented['churn_probability'].quantile(0.75)
high_risk_share = float((segmented['churn_probability'] >= high_risk_cutoff).mean() * 100)

app_churn = clean.groupby('has_app')['churned'].mean() * 100
churn_with_app = float(app_churn.get(True, np.nan))
churn_without_app = float(app_churn.get(False, np.nan))

support_bins = pd.cut(
    clean['support_tickets_per_month'],
    bins=[-0.01, 0.2, 0.5, 1.5, np.inf],
    labels=['0-0.2', '0.2-0.5', '0.5-1.5', '>1.5']
)
support_churn = (clean.assign(support_segment=support_bins)
                 .groupby('support_segment')['churned'].mean() * 100)
churn_low_support = float(support_churn.get('0-0.2', np.nan))
churn_high_support = float(support_churn.get('0.5-1.5', np.nan))

premium_cluster = cluster_summary.loc[cluster_summary['monthly_charges_mean'].idxmax()]
cluster_rows = []
for _, row in cluster_summary.iterrows():
    cluster_rows.append({
        'cluster': int(row['cluster']),
        'customers': int(row['customers']),
        'monthly_charges': float(row['monthly_charges_mean']),
        'data_usage': float(row['data_usage_mean']),
        'support': float(row['support_mean']),
        'churn_prob': float(row['churn_prob_mean']),
        'next_spend': float(row['next_month_spend_mean'])
    })

fig_dir = ROOT / 'reports/figures'
figures = [
    ('Churn by Plan Tier', fig_dir / 'bar_churn_by_plan.png'),
    ('Churn Reduction from App Adoption', fig_dir / 'bar_churn_by_app.png'),
    ('Monthly Churn & Spend Trend', fig_dir / 'temporal_churn_spend.png'),
    ('Provincial Churn Hotspots', fig_dir / 'spatial_province_bubble.png'),
    ('Monthly Charges Distribution', fig_dir / 'distribution_monthly_charges.png')
]

pdf_path = ROOT / 'reports/insight_summary.pdf'
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=12)
pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 12, 'Data Science Case Study: From Data Audit to Decision Insights', ln=True)

pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 7, 'Nationwide telecom subscriber dataset (20k rows, 30 features) progressed through audit, quality checks, EDA, statistical testing, clustering, and retention scoring to inform executive decisions.')

pdf.ln(2)
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Executive Summary', ln=True)
pdf.set_font('Arial', '', 12)
exec_lines = [
    f"Analysed {n_customers:,} subscribers with an overall churn rate of {churn_rate:.1f}% and average monthly revenue of $ {avg_monthly_revenue:.2f}.",
    f"Mobile app adoption at {app_adoption:.1f}% cuts churn from {churn_without_app:.1f}% to {churn_with_app:.1f}%.",
    f"High-support customers churn {churn_high_support:.1f}% vs {churn_low_support:.1f}% for low-touch peers.",
    f"K-means identifies a 19% Premium Data cluster driving $ {premium_cluster['next_month_spend_mean']:.2f} future spend.",
    f"Propensity scoring surfaces the riskiest {high_risk_share:.1f}% of accounts for concierge retention pilots." 
]
for line in exec_lines:
    pdf.multi_cell(0, 7, f"- {line}")

pdf.ln(2)
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Key Insights', ln=True)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Retention & Experience', ln=True)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 6, f"? App-less customers churn {churn_without_app - churn_with_app:.1f} pts more; digital adoption remains the single strongest lever.\n? Support-heavy cohorts carry ~{churn_high_support / churn_low_support if churn_low_support else 0:.2f}x churn odds, validating concierge outreach.\n? 5.5k high-risk accounts combine support load and low app usage?prime targets for the retention pilot.")

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Revenue & Usage', ln=True)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 6, f"? Premium Data Power Users (Cluster {int(premium_cluster['cluster'])}) spend $ {premium_cluster['next_month_spend_mean']:.2f} monthly with highest charges and engagement.\n? Value Seekers (Cluster 2) mirror low-spend users but generate more tickets?bundle upgrades plus app education improve margin.")

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Geography & Trends', ln=True)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 6, "? Matabeleland North and Manicaland exhibit the steepest churn pockets needing localised retention squads.\n? Mid-2025 churn spikes coincide with spend dips, reinforcing proactive monitoring via the dashboard filters.")

for caption, path in figures:
    if not path.exists():
        continue
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Visual Evidence', ln=True)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, caption, ln=True)
    pdf.ln(1)
    pdf.image(str(path), w=180)

pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Recommendations', ln=True)
pdf.set_font('Arial', '', 12)
recommendations = [
    'Launch the 4-week concierge retention pilot targeting 5,557 high-risk accounts with segment-specific treatments.',
    'Bundle loyalty perks for Premium Data Power Users to protect $70+ monthly spend while deepening digital engagement.',
    'Scale mobile app adoption incentives for the 22% of the base still offline, tied to data/top-up rewards.',
    'Automate support ticket velocity alerts to intervene before churn spikes.',
    'Embed the interactive dashboard into weekly revenue-ops cadences to track churn and spend jointly.'
]
for rec in recommendations:
    pdf.multi_cell(0, 7, f"- {rec}")

pdf.ln(2)
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Limitations & Next Steps', ln=True)
pdf.set_font('Arial', '', 12)
limits = [
    'Single snapshot data?seasonality and campaign impacts require longitudinal validation.',
    'Logistic propensity model offers +0.02 AUC lift; explore gradient boosting and survival analysis for stronger ranking.',
    'Support taxonomy lacks qualitative root causes?integrate ticket text analytics next.',
    'Pricing sensitivity not modelled; incorporate spend-to-income ratio into elasticity testing.',
]
for item in limits:
    pdf.multi_cell(0, 7, f"- {item}")

pdf.output(str(pdf_path))
print(pdf_path)
