# Q6: four ways to build a training set from the same tiny data. Run in the misc venv (pandas, polars, duckdb).
import warnings; warnings.filterwarnings("ignore")
import duckdb, pandas as pd, polars as pl
feat = pd.DataFrame({
    "user_id": [1, 1, 1, 2, 2],
    "ts": pd.to_datetime(["2026-01-01", "2026-01-03", "2026-01-06", "2026-01-02", "2026-01-05"]),
    "txn_count_7d": [3, 5, 9, 1, 4]})
lab = pd.DataFrame({
    "user_id": [1, 1, 2, 2],
    "label_ts": pd.to_datetime(["2026-01-02", "2026-01-04", "2026-01-03", "2026-01-01"]),
    "label": [0, 1, 0, 1]}).sort_values("label_ts").reset_index(drop=True)

# 1. NAIVE: join the latest value per user, ignoring time. Leaks the future.
latest = feat.sort_values("ts").groupby("user_id", as_index=False).last()[["user_id", "txn_count_7d"]]
naive = lab.merge(latest, on="user_id", how="left")

# 2. pandas merge_asof: latest feature row with ts <= label_ts, per user.
pm = pd.merge_asof(lab, feat.sort_values("ts"), left_on="label_ts", right_on="ts", by="user_id", direction="backward")

# 3. DuckDB ASOF LEFT JOIN
con = duckdb.connect()
con.register("lab", lab); con.register("feat", feat)
dd = con.sql("""SELECT l.user_id, l.label_ts, l.label, f.txn_count_7d
                FROM lab l ASOF LEFT JOIN feat f ON l.user_id = f.user_id AND l.label_ts >= f.ts
                ORDER BY l.label_ts, l.user_id""").df()

# 4. Polars join_asof
pl_out = (pl.from_pandas(lab).sort("label_ts")
          .join_asof(pl.from_pandas(feat).sort("ts"), left_on="label_ts", right_on="ts", by="user_id")
          .to_pandas())

key = ["user_id", "label_ts"]
res = lab[key + ["label"]].sort_values(key).reset_index(drop=True)
for name, df, col in [("naive latest-value", naive, "txn_count_7d"), ("pandas merge_asof", pm, "txn_count_7d"),
                      ("duckdb ASOF", dd, "txn_count_7d"), ("polars join_asof", pl_out, "txn_count_7d")]:
    res[name] = df.sort_values(key).reset_index(drop=True)[col].astype("Float64").to_numpy()
pd.set_option("display.width", 200)
print(res.to_string(index=False))
asof = ["pandas merge_asof", "duckdb ASOF", "polars join_asof"]
print("\nthree as-of methods agree:", all(res[asof[0]].equals(res[c]) for c in asof[1:]))
leaks = res[res["naive latest-value"] != res["pandas merge_asof"]]
print("rows where naive differs from as-of (leaked or wrong):", len(leaks), "of", len(res))
