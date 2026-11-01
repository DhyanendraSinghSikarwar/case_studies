"""CI data gate: returns a list of failure strings. Empty list = pass."""
import pandas as pd

# dtype families, not exact names: pandas 3 reads text as "str", older pandas as "object"
SCHEMA = {"customer_id": "integer", "age": "integer", "plan": "text", "monthly_spend": "float", "churned": "integer"}
CHECKS = {
    "integer": pd.api.types.is_integer_dtype,
    "float": pd.api.types.is_float_dtype,
    "text": lambda s: pd.api.types.is_string_dtype(s) or pd.api.types.is_object_dtype(s),
}
PLANS = {"basic", "plus", "pro"}
SERVING_FEATURES = ["age", "plan", "monthly_spend"]  # what the serving API sends


def check_frame(df, min_rows=5, feature_contract=SERVING_FEATURES):
    f = []
    # schema: columns and dtypes
    for col, dt in SCHEMA.items():
        if col not in df.columns:
            f.append(f"missing column: {col}")
        elif not CHECKS[dt](df[col]):
            f.append(f"dtype {col}: expected {dt}, got {df[col].dtype}")
    if f:
        return f  # later checks need the right columns
    if len(df) < min_rows:
        f.append(f"row count {len(df)} < {min_rows}")
    if df["customer_id"].duplicated().any():
        f.append("customer_id not unique")
    if not df["age"].between(18, 100).all():
        f.append("age out of range 18-100")
    if (df["monthly_spend"] < 0).any():
        f.append("monthly_spend negative")
    null_rate = df["monthly_spend"].isna().mean()
    if null_rate > 0.1:
        f.append(f"monthly_spend null rate {null_rate:.0%} > 10%")
    bad = set(df["plan"].dropna().unique()) - PLANS
    if bad:
        f.append(f"plan has unknown values: {sorted(bad)}")
    if not set(df["churned"].unique()) <= {0, 1}:
        f.append("churned not in {0,1}")
    for c in feature_contract:  # train-serving contract
        if c not in df.columns:
            f.append(f"serving feature missing from training data: {c}")
    return f
