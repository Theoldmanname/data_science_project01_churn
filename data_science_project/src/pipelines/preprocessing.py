"""Data cleaning and preprocessing pipeline for the telecom subscriber dataset."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


RAW_DATA_PATH = Path("data/raw/training_master_dataset.csv")
PROCESSED_DATA_PATH = Path("data/processed/clean_dataset.csv")


NUMERIC_OUTLIER_COLUMNS: Iterable[str] = (
    "monthly_charges",
    "total_charges",
    "data_usage_gb",
    "calls_per_month",
    "messages_per_month",
    "avg_session_minutes",
    "credit_score",
    "income",
    "late_payments",
    "next_month_spend",
)


def load_raw_dataset(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw dataset with appropriate parsing."""
    return pd.read_csv(path, parse_dates=["signup_date", "last_seen"], dayfirst=True)


def drop_duplicate_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate customer_id entries keeping the latest last_seen record."""
    deduped = df.sort_values("last_seen", ascending=False).drop_duplicates("customer_id")
    return deduped.sort_values("customer_id").reset_index(drop=True)


def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values with segment-aware imputations."""
    filled = df.copy()

    filled["payment_method"] = filled["payment_method"].fillna("Unspecified")
    filled["review_text"] = filled["review_text"].fillna("No review provided")

    plan_usage_median = filled.groupby("plan_type")["data_usage_gb"].transform("median")
    filled["data_usage_gb"] = filled["data_usage_gb"].fillna(plan_usage_median)
    filled["data_usage_gb"] = filled["data_usage_gb"].fillna(filled["data_usage_gb"].median())

    device_session_median = filled.groupby("device_type")["avg_session_minutes"].transform("median")
    filled["avg_session_minutes"] = filled["avg_session_minutes"].fillna(device_session_median)
    filled["avg_session_minutes"] = filled["avg_session_minutes"].fillna(
        filled["avg_session_minutes"].median()
    )

    contract_credit_median = filled.groupby("contract")["credit_score"].transform("median")
    filled["credit_score"] = filled["credit_score"].fillna(contract_credit_median)
    filled["credit_score"] = filled["credit_score"].fillna(filled["credit_score"].median())

    province_income_median = filled.groupby("province")["income"].transform("median")
    filled["income"] = filled["income"].fillna(province_income_median)
    filled["income"] = filled["income"].fillna(filled["income"].median())

    return filled


def enforce_consistency(df: pd.DataFrame) -> pd.DataFrame:
    """Apply logical data integrity checks and corrections."""
    consistent = df.copy()

    mask_last_before_signup = consistent["last_seen"] < consistent["signup_date"]
    if mask_last_before_signup.any():
        consistent.loc[mask_last_before_signup, ["signup_date", "last_seen"]] = (
            consistent.loc[mask_last_before_signup, ["last_seen", "signup_date"]].to_numpy()
        )

    tenure_calculated = (
        (consistent["last_seen"] - consistent["signup_date"]).dt.days / 30.4375
    ).clip(lower=0)
    tenure_adjustment_mask = (consistent["tenure_months"] - tenure_calculated).abs() > 3
    consistent.loc[tenure_adjustment_mask, "tenure_months"] = tenure_calculated[
        tenure_adjustment_mask
    ].round().astype(int)
    consistent["tenure_months"] = consistent["tenure_months"].clip(lower=0)

    return consistent


def cap_outliers(df: pd.DataFrame, columns: Iterable[str] = NUMERIC_OUTLIER_COLUMNS) -> pd.DataFrame:
    """Winsorize specified numeric columns using IQR fences."""
    capped = df.copy()
    for col in columns:
        if col not in capped.columns:
            continue
        series = capped[col]
        if series.isna().all():
            continue
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        capped[col] = series.clip(lower=lower, upper=upper)
    return capped


def cast_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure appropriate datatypes for downstream modeling."""
    casted = df.copy()

    categorical_columns = [
        "gender",
        "province",
        "plan_type",
        "contract",
        "payment_method",
        "device_type",
    ]
    for col in categorical_columns:
        casted[col] = casted[col].astype("category")

    casted["satisfaction_score"] = pd.Categorical(
        casted["satisfaction_score"], categories=[1, 2, 3, 4, 5], ordered=True
    )

    bool_columns = ["has_app", "has_international_plan", "churned", "defaulted_loan"]
    for col in bool_columns:
        casted[col] = casted[col].astype(bool)

    integer_columns = ["customer_id", "age", "tenure_months", "support_tickets_last_6mo", "late_payments"]
    for col in integer_columns:
        casted[col] = casted[col].astype(int)

    numeric_columns = [
        "monthly_charges",
        "total_charges",
        "data_usage_gb",
        "calls_per_month",
        "messages_per_month",
        "avg_session_minutes",
        "credit_score",
        "income",
        "next_month_spend",
    ]
    for col in numeric_columns:
        casted[col] = pd.to_numeric(casted[col], errors="coerce")

    return casted


def derive_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create value-add analytics features."""
    enriched = df.copy()

    enriched["tenure_years"] = (enriched["tenure_months"] / 12).round(2)
    enriched["support_tickets_per_month"] = (enriched["support_tickets_last_6mo"] / 6).round(3)
    enriched["avg_monthly_revenue"] = np.where(
        enriched["tenure_months"] > 0,
        enriched["total_charges"] / enriched["tenure_months"].clip(lower=1),
        enriched["monthly_charges"],
    )
    enriched["spend_to_income_ratio"] = np.where(
        enriched["income"] > 0,
        (enriched["monthly_charges"] * 12) / enriched["income"],
        np.nan,
    )
    enriched["charges_per_gb"] = np.where(
        enriched["data_usage_gb"] > 0,
        enriched["monthly_charges"] / enriched["data_usage_gb"],
        np.nan,
    )
    enriched["engagement_intensity"] = (
        enriched["avg_session_minutes"]
        + enriched["calls_per_month"] * 0.1
        + enriched["messages_per_month"] * 0.05
    )
    enriched["lifetime_value_projection"] = (
        enriched["total_charges"] + enriched["next_month_spend"] * np.where(enriched["churned"], 0, 12)
    )

    return enriched


def run_pipeline(
    raw_path: Path = RAW_DATA_PATH,
    output_path: Path = PROCESSED_DATA_PATH,
) -> pd.DataFrame:
    """Execute the full preprocessing pipeline and persist the cleaned dataset."""
    df = load_raw_dataset(raw_path)
    df = drop_duplicate_customers(df)
    df = impute_missing(df)
    df = enforce_consistency(df)
    df = cap_outliers(df)
    df = cast_dtypes(df)
    df = derive_features(df)

    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    cleaned = run_pipeline()
    print(f"Saved cleaned dataset with {len(cleaned):,} rows to {PROCESSED_DATA_PATH}")
