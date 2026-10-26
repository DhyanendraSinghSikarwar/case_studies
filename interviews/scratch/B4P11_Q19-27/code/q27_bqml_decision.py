"""Q27: decision rule BigQuery ML vs Vertex custom job. Pure Python; no BigQuery call was made."""
def decide(p: dict) -> tuple[str, list[str]]:
    why = []
    # hard blockers for in-warehouse training first
    if p["needs_custom_framework_or_gpu"]: return "vertex_custom_job", ["needs custom code, framework or GPU beyond built-in model types"]
    if p["needs_custom_features_in_python"]: return "vertex_custom_job", ["feature logic does not fit SQL"]
    if p["strict_realtime_latency_ms"] is not None and not p["will_export_model"]:
        return "vertex_custom_job", ["tight online latency: score outside the warehouse (or export and host)"]
    if p["data_in_warehouse"] and p["model_family_supported_in_bqml"]:
        why.append("data already in the warehouse, model family is built in")
        if p["batch_scoring_only"]: why.append("batch scoring in SQL is enough")
        if p["must_register_in_vertex"]: why.append("register to Vertex Model Registry so governance is shared (check current docs)")
        return "bqml", why
    return "vertex_custom_job", ["default: data not in warehouse or model family unsupported"]

base = dict(needs_custom_framework_or_gpu=False, needs_custom_features_in_python=False, strict_realtime_latency_ms=None,
            will_export_model=False, data_in_warehouse=True, model_family_supported_in_bqml=True, batch_scoring_only=True,
            must_register_in_vertex=False)
cases = {
 "weekly churn scores, data in BQ, logistic regression": base,
 "image model on GPUs": {**base, "needs_custom_framework_or_gpu": True},
 "fraud score at 50 ms online, no export plan": {**base, "strict_realtime_latency_ms": 50, "batch_scoring_only": False},
 "same fraud case but plan to export model": {**base, "strict_realtime_latency_ms": 50, "will_export_model": True, "batch_scoring_only": False, "must_register_in_vertex": True},
 "data lives in Blob storage, not BQ": {**base, "data_in_warehouse": False},
}
expected = ["bqml", "vertex_custom_job", "vertex_custom_job", "bqml", "vertex_custom_job"]
for (name, p), exp in zip(cases.items(), expected):
    got, why = decide(p); assert got == exp, (name, got)
    print(f"{got:17s} <- {name}: {'; '.join(why)}")
print("5 cases, all as expected")
