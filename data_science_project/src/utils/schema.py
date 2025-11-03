"""Pandera schema definitions for the training master dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Check, Column, DataFrameSchema


training_master_schema = DataFrameSchema(
    {
        "customer_id": Column(int, checks=Check.ge(1)),
        "signup_date": Column(pa.DateTime, coerce=True),
        "last_seen": Column(pa.DateTime, coerce=True),
        "age": Column(int, checks=[Check.ge(15), Check.le(100)]),
        "gender": Column(str, checks=Check.isin(["Female", "Male", "Other"])),
        "province": Column(
            str,
            checks=Check.isin(
                [
                    "Bulawayo",
                    "Harare",
                    "Manicaland",
                    "Mashonaland Central",
                    "Mashonaland East",
                    "Mashonaland West",
                    "Masvingo",
                    "Matabeleland North",
                    "Matabeleland South",
                    "Midlands",
                ]
            ),
        ),
        "lat": Column(float, checks=[Check.ge(-22.0), Check.le(-15.0)]),
        "lng": Column(float, checks=[Check.ge(25.0), Check.le(34.0)]),
        "plan_type": Column(str, checks=Check.isin(["Prepaid", "Premium", "Postpaid"])),
        "contract": Column(str, checks=Check.isin(["Month-to-Month", "One Year", "Two Year"])),
        "payment_method": Column(
            str,
            nullable=True,
            checks=Check.isin(["Cash", "Credit Card", "Debit Card", "EcoCash"]),
        ),
        "device_type": Column(str, checks=Check.isin(["Android", "iOS", "Web"])),
        "has_app": Column(int, checks=Check.isin([0, 1])),
        "has_international_plan": Column(int, checks=Check.isin([0, 1])),
        "tenure_months": Column(int, checks=[Check.ge(0), Check.le(120)]),
        "monthly_charges": Column(float, checks=[Check.ge(0), Check.le(1000)]),
        "total_charges": Column(float, checks=Check.ge(0)),
        "support_tickets_last_6mo": Column(int, checks=[Check.ge(0), Check.le(24)]),
        "data_usage_gb": Column(float, nullable=True, checks=Check.ge(0)),
        "calls_per_month": Column(int, checks=[Check.ge(0), Check.le(200)]),
        "messages_per_month": Column(int, checks=[Check.ge(0), Check.le(400)]),
        "avg_session_minutes": Column(float, nullable=True, checks=[Check.ge(0), Check.le(240)]),
        "credit_score": Column(float, nullable=True, checks=[Check.ge(250), Check.le(900)]),
        "income": Column(float, nullable=True, checks=Check.ge(0)),
        "late_payments": Column(int, checks=[Check.ge(0), Check.le(36)]),
        "satisfaction_score": Column(int, checks=Check.isin([1, 2, 3, 4, 5])),
        "churned": Column(int, checks=Check.isin([0, 1])),
        "defaulted_loan": Column(int, checks=Check.isin([0, 1])),
        "next_month_spend": Column(float, checks=[Check.ge(0), Check.le(500)]),
        "review_text": Column(str, nullable=True),
    },
    strict=True,
    coerce=True,
    unique=["customer_id"],
)


def load_and_validate(path: Path) -> pd.DataFrame:
    """Load the raw CSV and validate against the training master schema."""
    df = pd.read_csv(
        path,
        parse_dates=["signup_date", "last_seen"],
        dayfirst=True,
        keep_default_na=True,
    )
    return training_master_schema.validate(df, lazy=True)
