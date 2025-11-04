# Deployment Checklist

Use this guide to publish the case study so recruiters can explore the code, dashboards, and narrative with one click.

---

## 1. Publish to GitHub
1. Create a new repository (e.g., `data-science-case-study`) on GitHub.
2. Push the contents of `data_science_project/` to the repo root:
   ```bash
   git init
   git remote add origin git@github.com:<your-username>/<your-repo>.git
   git add .
   git commit -m "Initial commit: telecom retention case study"
   git push -u origin main
   ```
3. Update the README fast links (replace `your-username/your-repo` and fill the LinkedIn/Streamlit URLs).
4. Pin `requirements.txt`, `README.md`, and `reports/insight_summary.pdf` to keep them prominent.

## 2. Deploy the Streamlit Dashboard
1. Duplicate `streamlit_app.py` to your repo root, or confirm it sits next to `requirements.txt`.
2. Create a free [Streamlit Cloud](https://streamlit.io/cloud) account.
3. Add a new app pointing to your GitHub repo and `streamlit_app.py`.
4. Add `data/processed/clean_dataset.csv`, `segmented.csv`, and `reports/segment_summary.csv` to the Streamlit “Secrets / Files” if private, or rely on repo versions.
5. After deployment, copy the live URL and paste it into the README “Live Dashboard” link.

## 3. Notebook Sharing
- **nbviewer:** Replace the placeholders with `https://nbviewer.org/github/<your-username>/<your-repo>/blob/main/notebooks/<notebook>.ipynb`.
- **Binder (optional):** Update the badge link with your GitHub coordinates so viewers can run notebooks in the cloud.
- **Alternative:** Enable GitHub Codespaces or provide JupyterLite if desired.

## 4. GitHub Pages (Project Hub)
1. Create a `docs/` folder at repo root (already included in this project).
2. Ensure `docs/index.html` (landing page) and `docs/eda_report.html` are present; they link to the Streamlit app, PDF, and raw EDA report.
3. In **Settings → Pages**, choose branch `master` and folder `/docs`, then save.
4. After GitHub Pages publishes (https://<username>.github.io/<repo>/), update README and Streamlit links if necessary.

## 5. Publish LinkedIn Article
1. Open `reports/linkedin_article.md`, copy the content to LinkedIn article editor.
2. Embed key figures (`reports/figures/...`) as images (upload screenshots to LinkedIn).
3. Link back to the GitHub repo and Streamlit dashboard.
4. Share the article link in README Fast Links and across your social channels.

## 6. Highlight Downloads
- Ensure `reports/insight_summary.pdf` and `data/processed/segmented.csv` remain in the repo.
- Mention them in the README “Fast Links” for easy recruiter access.

## 7. Optional Enhancements
- Create a short Loom/YouTube walkthrough of the dashboard and add the link to README.
- Build a Canva/Google Slides deck summarizing the case study for interviews.
- Stand up a GitHub Pages or Notion landing page summarizing the project with CTAs to the repo, dashboard, and article.

---

Once these steps are complete, your analytics portfolio will feel production-ready and easy for hiring teams to explore. Good luck! 🚀
