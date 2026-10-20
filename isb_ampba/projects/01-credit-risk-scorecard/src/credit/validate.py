"""Schema and range checks: fail loudly on bad data."""
from __future__ import annotations

import pandas as pd

from .data import BILL_COLS, PAY_COLS, PAYAMT_COLS, RAW_COLUMNS, TARGET


def validate_raw(df: pd.DataFrame, expected_rows: int | None = 30000) -> dict:
    """Assert schema/range invariants; return a small data-quality report."""
    missing = [c for c in RAW_COLUMNS if c not in df.columns]
    assert not missing, f"missing columns: {missing}"
    if expected_rows is not None:
        assert len(df) == expected_rows, f"expected {expected_rows} rows, got {len(df)}"
    assert df[RAW_COLUMNS].isna().sum().sum() == 0, "unexpected nulls"
    assert set(df[TARGET].unique()) <= {0, 1}, "target must be in {0,1}"
    assert df["LIMIT_BAL"].gt(0).all(), "LIMIT_BAL must be positive"
    assert df["AGE"].between(18, 100).all(), "AGE out of range"
    assert df["SEX"].isin([1, 2]).all(), "SEX must be 1 or 2"
    assert df[PAY_COLS].apply(lambda s: s.between(-2, 9)).all().all(), "PAY_* out of [-2, 9]"
    assert df[PAYAMT_COLS].ge(0).all().all(), "PAY_AMT must be >= 0"
    # BILL_AMT can legitimately be negative (credit balance): report, do not fail
    return {"rows": int(len(df)), "default_rate": float(df[TARGET].mean()),
            "neg_bill_rows": int((df[BILL_COLS] < 0).any(axis=1).sum()),
            "neg_bill1_rows": int((df["BILL_AMT1"] < 0).sum()),
            "duplicate_rows": int(df.duplicated().sum())}
