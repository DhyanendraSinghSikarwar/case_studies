import numpy as np, pandas as pd
import pandera.pandas as pa

NOW = pd.Timestamp("2026-10-26 12:00")
rng = np.random.default_rng(2)

def batch(n=1000, bad=False):
    df = pd.DataFrame({
        "user_id": np.arange(n),
        "age": rng.integers(18, 80, n),
        "income": rng.lognormal(10, 0.4, n),
        "country": rng.choice(["IN", "US", "UK"], n),
        "event_ts": NOW - pd.to_timedelta(rng.integers(0, 3600, n), unit="s"),
    })
    if bad:
        df.loc[:149, "income"] = np.nan                  # 15 percent nulls
        df.loc[10:14, "age"] = [-1, 200, 150, 17, 999]   # out of range
        df.loc[20, "country"] = "XX"                     # not in allowed set
        df.loc[31, "user_id"] = 30                       # duplicate id
        df["event_ts"] = df["event_ts"] - pd.Timedelta(hours=9)   # stale feed
        df = df.iloc[:400]                               # volume drop
    return df

BASE_ROWS, BASE_NULL = 1000, 0.00

def plain_checks(df):
    f = []
    if df["income"].isna().mean() > BASE_NULL + 0.02: f.append(f"null rate income {df['income'].isna().mean():.2f}")
    if not df["age"].between(18, 80).all():           f.append(f"age out of 18-80: {(~df['age'].between(18, 80)).sum()} rows")
    if not df["country"].isin(["IN", "US", "UK"]).all(): f.append(f"bad country values: {sorted(set(df['country']) - {'IN','US','UK'})}")
    if df["user_id"].duplicated().any():              f.append(f"duplicate user_id: {df['user_id'].duplicated().sum()}")
    if (NOW - df["event_ts"].max()) > pd.Timedelta(hours=2): f.append(f"stale: newest row {(NOW - df['event_ts'].max())} old")
    if len(df) < 0.7 * BASE_ROWS:                     f.append(f"volume {len(df)} vs baseline {BASE_ROWS}")
    return f

schema = pa.DataFrameSchema({
    "user_id": pa.Column(int, unique=True),
    "age": pa.Column(int, pa.Check.in_range(18, 80)),
    "income": pa.Column(float, nullable=True, checks=pa.Check(lambda s: s.isna().mean() <= 0.02, element_wise=False, ignore_na=False, error="null rate above 2 percent")),
    "country": pa.Column(str, pa.Check.isin(["IN", "US", "UK"])),
    "event_ts": pa.Column("datetime64[ns]", pa.Check(lambda s: (NOW - s.max()) <= pd.Timedelta(hours=2), error="stale: newest row older than 2h")),
}, checks=pa.Check(lambda d: len(d) >= 0.7 * BASE_ROWS, error="volume below 70 percent of baseline"))

for name, df in (("good", batch()), ("corrupted", batch(bad=True))):
    print(f"--- {name} batch, plain pandas: {plain_checks(df) or 'no failures'}")
    try:
        schema.validate(df, lazy=True)
        print(f"--- {name} batch, pandera: passed")
    except pa.errors.SchemaErrors as e:
        fc = e.failure_cases[["column", "check", "failure_case"]].copy()
        fc["failure_case"] = fc["failure_case"].astype(str).str.slice(0, 28)
        print(f"--- {name} batch, pandera: {len(fc)} failure rows")
        print(fc.head(12).to_string(index=False))
