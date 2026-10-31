import pandas as pd, pandera, pandera.pandas as pa
print("pandera", pandera.__version__, "pandas", pd.__version__)
df = pd.DataFrame({"loan_id": [1, 2, 3, 4, 5],
                   "age": [25, 40, None, 17, 130],
                   "status": ["open", "closed", "open", "paid", "open"]})
schema = pa.DataFrameSchema(
    {"age": pa.Column(float, [pa.Check.in_range(18, 100)], nullable=False),       # non-null + range
     "status": pa.Column(str, pa.Check.isin(["open", "closed"]))},               # allowed set
    checks=pa.Check(lambda d: len(d) >= 100, error="row count must be >= 100"),  # table-level check
    coerce=True)
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(e.failure_cases[["schema_context", "column", "check", "failure_case", "index"]].to_string())
