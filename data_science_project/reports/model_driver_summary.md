# Driver Feature Validation Summary

- **Dataset:** `clean_dataset.csv` (20,000 subscribers) with engineered features `support_intensity`, `province_churn_rate`, and binary `has_app` flag.
- **Churn uplift:** Logistic baseline (usage + tenure) posted ROC-AUC **0.517**. Adding driver signals lifted AUC to **0.537** (+0.020). Accuracy held at **74.6%**, indicating lift is primarily in ranking power rather than classification threshold.
- **Spend uplift:** Linear baseline delivered **R? 0.905** with MAE **$5.17**. Driver-aware model nudged R? to **0.905** (+0.0003) and trimmed MAE by **$0.01**, showing spend is already well-explained by billing history.
- **Interpretation:** Support intensity and app adoption add incremental predictive value for churn, while province risk stabilises ranking across geographies. Revenue prediction is largely governed by current charges, so leverage driver features for churn models and customer health scoring.
- **Artifacts:** Full results stored at `reports/model_driver_lift.json`; feature engineering logic lives in `src/models/driver_experiments.py`.
