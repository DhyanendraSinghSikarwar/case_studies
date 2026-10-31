import json
import numpy as np, pandas as pd

rng = np.random.default_rng(31)
train = pd.DataFrame({"age": rng.integers(21, 66, 3000), "income": rng.lognormal(10.5, 0.4, 3000).round(),
                      "channel": rng.choice(["app", "web", "branch"], 3000, p=[.5, .3, .2])})
train.loc[rng.choice(3000, 60, replace=False), "income"] = np.nan

def baseline(df):
    """Own constraints-style file: a baseline summary plus allowed bounds. Field names are mine, not any vendor schema."""
    c = {}
    for col in df:
        e = {"type": "numeric" if pd.api.types.is_numeric_dtype(df[col]) else "string",
             "max_null_ratio": round(float(df[col].isna().mean()) * 2 + 0.01, 3)}
        if e["type"] == "numeric":
            e["min"], e["max"] = float(df[col].min()), float(df[col].max())
            e["mean_ref"], e["mean_tolerance_pct"] = round(float(df[col].mean()), 1), 15
        else:
            e["allowed_values"] = sorted(df[col].dropna().unique().tolist())
            e["max_new_value_ratio"] = 0.01
        c[col] = e
    return {"version": 1, "row_count_min": int(len(df) * 0.1), "columns": c}

def check(df, cons):
    v = []
    if len(df) < cons["row_count_min"]: v.append(f"row count {len(df)} below {cons['row_count_min']}")
    for col, e in cons["columns"].items():
        if col not in df: v.append(f"{col}: column missing"); continue
        nr = df[col].isna().mean()
        if nr > e["max_null_ratio"]: v.append(f"{col}: null ratio {nr:.3f} > {e['max_null_ratio']}")
        if e["type"] == "numeric":
            s = df[col].dropna()
            if s.min() < e["min"] or s.max() > e["max"]: v.append(f"{col}: range [{s.min():.0f}, {s.max():.0f}] outside [{e['min']:.0f}, {e['max']:.0f}]")
            dev = abs(s.mean() - e["mean_ref"]) / e["mean_ref"] * 100
            if dev > e["mean_tolerance_pct"]: v.append(f"{col}: mean moved {dev:.0f}% (> {e['mean_tolerance_pct']}%)")
        else:
            bad = (~df[col].dropna().isin(e["allowed_values"])).mean()
            if bad > e["max_new_value_ratio"]: v.append(f"{col}: {bad:.1%} unseen values")
    return v

cons = baseline(train)
open("constraints.json", "w").write(json.dumps(cons, indent=1))
print(json.dumps(cons["columns"]["income"]), "\n")

ok = train.sample(500, random_state=1)
bad = pd.DataFrame({"age": rng.integers(21, 66, 500), "income": (rng.lognormal(10.5, 0.4, 500) * 1.4).round(),
                    "channel": rng.choice(["app", "web", "branch", "agent"], 500, p=[.4, .3, .15, .15])})
bad.loc[rng.choice(500, 100, replace=False), "age"] = np.nan
for name, d in (("clean serving sample", ok), ("bad serving sample", bad)):
    v = check(d, cons)
    print(name, "->", "PASS" if not v else "FAIL")
    for x in v: print("   -", x)
