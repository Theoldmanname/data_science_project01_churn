# Deployment Log

I recorded the steps I followed to make the project discoverable online.

## GitHub Publication
- Initialised the repository locally, committed the telecom case study artefacts, and pushed to `master`.
- Updated the README fast links once Streamlit, GitHub Pages, and LinkedIn URLs were live.

## Streamlit Cloud
- Deployed `streamlit_app.py` from `master` with the assets tracked in the repo (clean dataset, segmented targets, segment summary).
- Whenever I ship code changes, I simply reboot the Streamlit app so it rebuilds from the latest commit.

## Notebook Sharing
- Added nbviewer and Binder links to the README so notebooks render without cloning.
- Codespaces/JupyterLite remain optional but are ready if stakeholders prefer a hosted environment.

## GitHub Pages Hub
- Placed a `docs/` directory at repo root containing `index.html` and the embedded EDA report.
- Enabled GitHub Pages (`master` branch, `/docs` folder) creating https://Theoldmanname.github.io/data_science_project01_churn/ as the project hub.
- The landing page links back to the Streamlit dashboard and hosts the PDF, segmentation outputs, and EDA report directly.

## LinkedIn Article
- Copied `reports/linkedin_article.md` into LinkedIn, embedded key figures, and linked back to the GitHub repo plus Streamlit app.
- The article now acts as a portfolio narrative referencing the same assets.

## Downloads & Artefacts
- Hosted the insight PDF, segmented dataset, and cluster summary both in the repo and via GitHub Pages for easy access.
- Any updates to the source files simply require `git add`, `git commit`, and `git push` to refresh both Streamlit Cloud and GitHub Pages.

## Optional Enhancements
- Loom/YouTube walkthroughs can be added later for live demos.
- Canva/Slides deck is ready for interviews if deeper storytelling is required.
- A custom GitHub Pages/Notion landing page could extend the hub with richer CTAs if desired.
