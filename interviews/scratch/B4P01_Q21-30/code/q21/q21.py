# Q21: validate(df) that reports ALL violations at once (plain pandas), plus a pandera lazy cross-check.
import pandas as pd
import pandera.pandas as pa

from pandas.api import types as T
# dtype FAMILIES, not exact strings: pandas 3 uses "str" for text, older pandas used "object"
EXPECTED = {"loan_id": ("integer", T.is_integer_dtype), "age": ("integer", T.is_integer_dtype),
            "income": ("float", T.is_float_dtype), "segment": ("string", T.is_string_dtype)}
SEGMENTS = {"retail", "sme", "corporate"}

def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of human-readable violations. Empty list = valid."""
    errs = []
    # 1) columns and dtypes: if a column is missing we cannot check it further
    missing = [c for c in EXPECTED if c not in df.columns]
    errs += [f"missing column: {c}" for c in missing]
    for c, (family, is_ok) in EXPECTED.items():
        if c in df.columns and not is_ok(df[c].dtype):
            errs.append(f"dtype of {c}: expected {family}, got {df[c].dtype}")
    # 2) non-null key
    if "loan_id" in df.columns:
        n = int(df["loan_id"].isna().sum())
        if n:
            errs.append(f"loan_id has {n} null(s)")
        # 3) uniqueness of the id (ignore nulls, already reported)
        dup = df["loan_id"].dropna()
        dup = dup[dup.duplicated(keep=False)].unique().tolist()
        if dup:
            errs.append(f"loan_id not unique: {sorted(dup)}")
    # 4) value range
    if "age" in df.columns:
        bad = df.index[(df["age"] < 18) | (df["age"] > 100)].tolist()
        if bad:
            errs.append(f"age outside [18, 100] at rows {bad}")
    # 5) allowed categories
    if "segment" in df.columns:
        bad = sorted(set(df["segment"].dropna()) - SEGMENTS)
        if bad:
            errs.append(f"segment has unknown values: {bad}")
    return errs

good = pd.DataFrame({"loan_id": [1, 2, 3], "age": [25, 40, 61],
                     "income": [5.0, 7.5, 6.1], "segment": ["retail", "sme", "corporate"]})
# four planted problems: null key, duplicate id, age 17 / 130, unknown segment 'vip'
bad = pd.DataFrame({"loan_id": pd.array([1, 1, None, 4], dtype="Int64"), "age": [25, 17, 130, 40],
                    "income": [5.0, 7.5, 6.1, 4.0], "segment": ["retail", "vip", "sme", "sme"]})
print("good frame ->", validate(good))
errs = validate(bad)
print("bad frame  ->", len(errs), "violations")
for e in errs:
    print("  -", e)

# same idea with pandera, lazy=True collects every failure (version printed below)
schema = pa.DataFrameSchema({
    "loan_id": pa.Column("Int64", nullable=False, unique=True),
    "age": pa.Column(int, pa.Check.in_range(18, 100)),
    "income": pa.Column(float),
    "segment": pa.Column(str, pa.Check.isin(sorted(SEGMENTS))),
})
try:
    schema.validate(bad, lazy=True)
except pa.errors.SchemaErrors as e:
    print("pandera lazy failure cases:", len(e.failure_cases))
    print(e.failure_cases[["column", "check", "failure_case"]].to_string(index=False))
import importlib.metadata as md
print("pandera", md.version("pandera"), "pandas", pd.__version__)
assert validate(good) == [] and len(errs) == 4
