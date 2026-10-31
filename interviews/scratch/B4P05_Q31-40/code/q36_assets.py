import dagster as dg

@dg.asset
def training_table() -> list[dict]:
    return [{"x": i, "y": 2 * i} for i in range(5)]

@dg.asset
def churn_model(training_table: list[dict]) -> dict:
    # fit y = w * x by least squares through the origin
    w = sum(r["x"] * r["y"] for r in training_table) / sum(r["x"] ** 2 for r in training_table)
    return {"w": w, "rows": len(training_table)}

defs = dg.Definitions(assets=[training_table, churn_model])

if __name__ == "__main__":
    result = dg.materialize([training_table, churn_model])
    print("success:", result.success)
    print("model value:", result.output_for_node("churn_model"))
    for e in result.get_asset_materialization_events():
        print("materialized:", e.asset_key.to_user_string())
