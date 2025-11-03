"""Experiments to quantify lift from key behavioral drivers on churn and spend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    r2_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "clean_dataset.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "model_driver_lift.json"


def engineer_driver_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create driver-oriented features for modeling experiments."""
    engineered = df.copy()
    engineered["has_app"] = engineered["has_app"].astype(int)

    engineered["support_intensity"] = pd.cut(
        engineered["support_tickets_per_month"],
        bins=[-0.01, 0.2, 0.5, 1.5, np.inf],
        labels=["0-0.2", "0.2-0.5", "0.5-1.5", "1.5+"],
        include_lowest=True,
    )

    province_churn = (
        engineered.groupby("province")["churned"].mean().rename("province_churn_rate")
    )
    engineered = engineered.merge(
        province_churn, on="province", how="left", validate="many_to_one"
    )

    return engineered


def make_preprocessor(
    numeric_features: list[str], categorical_features: list[str]
) -> ColumnTransformer:
    """Build a reusable column transformer."""
    transformers = []
    if numeric_features:
        transformers.append(("num", StandardScaler(), numeric_features))
    if categorical_features:
        transformers.append(
            (
                "cat",
                OneHotEncoder(drop="first", handle_unknown="ignore"),
                categorical_features,
            )
        )
    return ColumnTransformer(transformers)


def run_churn_experiment(df: pd.DataFrame) -> Dict[str, float]:
    """Compare baseline vs driver-informed churn models."""
    baseline_features = ["monthly_charges", "tenure_months", "avg_session_minutes"]
    driver_features = baseline_features + [
        "has_app",
        "support_intensity",
        "province",
        "support_tickets_per_month",
        "province_churn_rate",
    ]

    X = df
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    baseline_preprocessor = make_preprocessor(
        numeric_features=baseline_features, categorical_features=[]
    )
    driver_preprocessor = make_preprocessor(
        numeric_features=[
            "monthly_charges",
            "tenure_months",
            "avg_session_minutes",
            "support_tickets_per_month",
            "province_churn_rate",
        ],
        categorical_features=["has_app", "support_intensity", "province"],
    )

    baseline_model = Pipeline(
        steps=[
            ("preprocess", baseline_preprocessor),
            ("clf", LogisticRegression(max_iter=200, solver="lbfgs")),
        ]
    )
    driver_model = Pipeline(
        steps=[
            ("preprocess", driver_preprocessor),
            ("clf", LogisticRegression(max_iter=500, solver="lbfgs")),
        ]
    )

    baseline_model.fit(X_train, y_train)
    driver_model.fit(X_train, y_train)

    baseline_preds = baseline_model.predict_proba(X_test)[:, 1]
    driver_preds = driver_model.predict_proba(X_test)[:, 1]

    results = {
        "baseline_auc": roc_auc_score(y_test, baseline_preds),
        "driver_auc": roc_auc_score(y_test, driver_preds),
        "baseline_accuracy": accuracy_score(y_test, (baseline_preds >= 0.5).astype(int)),
        "driver_accuracy": accuracy_score(y_test, (driver_preds >= 0.5).astype(int)),
    }
    results["auc_lift"] = results["driver_auc"] - results["baseline_auc"]
    results["accuracy_lift"] = results["driver_accuracy"] - results["baseline_accuracy"]
    return results


def run_spend_experiment(df: pd.DataFrame) -> Dict[str, float]:
    """Assess impact of driver features on next-month spend prediction."""
    baseline_features = ["monthly_charges", "tenure_months", "avg_session_minutes"]
    driver_features = baseline_features + [
        "has_app",
        "support_tickets_per_month",
        "support_intensity",
        "province",
    ]

    X = df
    y = df["next_month_spend"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    baseline_preprocessor = make_preprocessor(
        numeric_features=baseline_features, categorical_features=[]
    )
    driver_preprocessor = make_preprocessor(
        numeric_features=[
            "monthly_charges",
            "tenure_months",
            "avg_session_minutes",
            "support_tickets_per_month",
        ],
        categorical_features=["has_app", "support_intensity", "province"],
    )

    baseline_model = Pipeline(
        steps=[("preprocess", baseline_preprocessor), ("reg", LinearRegression())]
    )
    driver_model = Pipeline(
        steps=[("preprocess", driver_preprocessor), ("reg", LinearRegression())]
    )

    baseline_model.fit(X_train, y_train)
    driver_model.fit(X_train, y_train)

    baseline_preds = baseline_model.predict(X_test)
    driver_preds = driver_model.predict(X_test)

    results = {
        "baseline_r2": r2_score(y_test, baseline_preds),
        "driver_r2": r2_score(y_test, driver_preds),
        "baseline_mae": mean_absolute_error(y_test, baseline_preds),
        "driver_mae": mean_absolute_error(y_test, driver_preds),
    }
    results["r2_lift"] = results["driver_r2"] - results["baseline_r2"]
    results["mae_delta"] = results["driver_mae"] - results["baseline_mae"]
    return results


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["signup_date", "last_seen"])
    df = engineer_driver_features(df)

    churn_results = run_churn_experiment(df)
    spend_results = run_spend_experiment(df)

    payload = {
        "churn_model": churn_results,
        "spend_model": spend_results,
        "rows_used": len(df),
        "features_engineered": [
            "support_intensity",
            "province_churn_rate",
            "has_app (binary)",
        ],
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
