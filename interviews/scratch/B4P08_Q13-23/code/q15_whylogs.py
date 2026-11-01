import sys, pandas as pd, whylogs as why
from whylogs.viz.drift.column_drift_algorithms import calculate_drift_scores
ref = pd.read_csv(sys.argv[1] + "/ref.csv"); cur = pd.read_csv(sys.argv[1] + "/cur.csv")
print("whylogs", why.__version__, "pandas", pd.__version__)
ref["city"] = ref["city"].astype(object); cur["city"] = cur["city"].astype(object)  # pandas 3 str dtype breaks whylogs 1.6.4 type matching
pr = why.log(ref).view(); pc = why.log(cur).view()
print(pc.to_pandas()[["counts/n", "counts/null", "types/fractional", "distribution/mean", "distribution/stddev"]].round(1).to_string())
scores = calculate_drift_scores(target_view=pc, reference_view=pr, with_thresholds=True)
for col, s in scores.items():
    print(col, s["algorithm"], round(s["statistic"], 4), "p=", round(s["pvalue"], 6), s["drift_category"])
