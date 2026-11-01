import great_expectations as gx, pandas as pd
print("great_expectations", gx.__version__, "pandas", pd.__version__)
df = pd.DataFrame({"loan_id": [1, 2, 3, 4, 5],
                   "age": [25, 40, None, 17, 130],
                   "status": ["open", "closed", "open", "paid", "open"]})
ctx = gx.get_context(mode="ephemeral")
asset = ctx.data_sources.add_pandas("src").add_dataframe_asset("loans")
batch = asset.add_batch_definition_whole_dataframe("whole").get_batch(batch_parameters={"dataframe": df})
exps = {
 "non-null age":   gx.expectations.ExpectColumnValuesToNotBeNull(column="age"),
 "age range 18-100": gx.expectations.ExpectColumnValuesToBeBetween(column="age", min_value=18, max_value=100),
 "status allowed": gx.expectations.ExpectColumnValuesToBeInSet(column="status", value_set=["open", "closed"]),
 "row count 100+": gx.expectations.ExpectTableRowCountToBeBetween(min_value=100),
}
for name, e in exps.items():
    r = batch.validate(e)
    res = r.result
    print(f"{name:18s} success={r.success!s:5s} unexpected_count={res.get('unexpected_count', res.get('observed_value'))} "
          f"values={res.get('partial_unexpected_list', '')} idx={res.get('partial_unexpected_index_list', '')}")
