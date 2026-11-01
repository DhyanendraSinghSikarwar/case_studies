import numpy as np, pandas as pd
from scipy.stats import ks_2samp

rng = np.random.default_rng(32)
def make(n, shift=0.0, null_rate=0.01):
    df = pd.DataFrame({"id": np.arange(n), "amount": rng.lognormal(8, 0.5, n), "tenure": rng.integers(1, 120, n)})
    df.loc[rng.random(n) < null_rate, "tenure"] = np.nan
    df["score"] = np.clip(rng.beta(2, 5, n) + shift, 0, 1)
    return df

ref = make(10_000)
prev = {"rows_in": 10_000, "rows_out": 10_000, "runtime_s": 610, "scores": make(10_000)["score"].to_numpy()}
batches = {
    "night-1 normal":    dict(inp=make(10_200), out_rows=10_200, runtime=640),
    "night-2 truncated": dict(inp=make(4_100), out_rows=4_100, runtime=250),
    "night-3 shifted":   dict(inp=make(10_050, shift=0.25), out_rows=10_050, runtime=620),
}

def validate(inp, scores, out_rows, runtime):
    why = []
    if not 0.7 <= len(inp) / prev["rows_in"] <= 1.3: why.append(f"input rows {len(inp)} vs last run {prev['rows_in']}")
    if set(ref.columns) - set(inp.columns): why.append("schema: missing columns")
    nulls = inp.isna().mean()
    if (nulls > 0.05).any(): why.append(f"null rate high in {nulls[nulls > 0.05].index.tolist()}")
    if out_rows != len(inp): why.append(f"output rows {out_rows} != input rows {len(inp)}")
    if runtime > 2 * prev["runtime_s"]: why.append(f"runtime {runtime}s more than 2x last run")
    d = ks_2samp(scores, prev["scores"])
    if d.statistic > 0.1: why.append(f"score distribution moved vs last run (KS D={d.statistic:.2f})")
    d_ref = ks_2samp(scores, ref["score"])
    if d_ref.statistic > 0.1: why.append(f"score distribution moved vs reference (KS D={d_ref.statistic:.2f})")
    return why

for name, b in batches.items():
    inp = b["inp"]
    scores = inp["score"].to_numpy()
    why = validate(inp, scores, b["out_rows"], b["runtime"])
    print(f"{name:20s} {'PASS' if not why else 'FAIL'}")
    for w in why: print("    -", w)
