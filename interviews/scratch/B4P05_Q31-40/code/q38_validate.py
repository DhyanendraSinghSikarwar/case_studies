import pandas as pd

RULES = {"cols": {"user_id": "int", "amount": "float", "country": "text"},
         "max_null_rate": {"amount": 0.10, "country": 0.05},
         "min_rows": 5, "max_rows": 1000}

class DataContractError(Exception): pass

def kind(series):                     # pandas 3 shows text as 'str', older pandas as 'object'
    if pd.api.types.is_integer_dtype(series): return "int"
    if pd.api.types.is_float_dtype(series): return "float"
    if pd.api.types.is_string_dtype(series): return "text"
    return str(series.dtype)

def validate(df, rules=RULES):
    errs = []
    for c, dt in rules["cols"].items():
        if c not in df.columns: errs.append(f"missing column {c}")
        elif kind(df[c]) != dt: errs.append(f"{c} is {kind(df[c])}, expected {dt}")
    for c, mx in rules["max_null_rate"].items():
        if c in df.columns and df[c].isna().mean() > mx:
            errs.append(f"{c} null rate {df[c].isna().mean():.2f} > {mx}")
    if not rules["min_rows"] <= len(df) <= rules["max_rows"]:
        errs.append(f"row count {len(df)} outside [{rules['min_rows']}, {rules['max_rows']}]")
    if errs: raise DataContractError("; ".join(errs))
    return True

def train(df): return f"trained on {len(df)} rows"

def pipeline(df):
    validate(df)                      # raising here means train() never runs
    return train(df)

good = pd.DataFrame({"user_id": range(1, 9), "amount": [10.0, 5.5, 7, 3, 9, 4, 8, 2], "country": list("INUSINUS")})
nulls = good.assign(amount=[None, None, None, 3, 9, 4, 8, 2])
schema = good.assign(amount=good["amount"].astype(str))
small = good.head(3)
for name, df in [("good", good), ("many nulls", nulls), ("schema drift", schema), ("too few rows", small)]:
    try: print(f"{name:13s} -> {pipeline(df)}")
    except DataContractError as e: print(f"{name:13s} -> BLOCKED: {e}")
