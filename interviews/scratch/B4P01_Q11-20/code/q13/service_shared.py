"""Service path after the fix: no feature logic here, only a call into the shared module."""
import pandas as pd
from features import RawRow, build_features


def predict_features(rows: list[dict]) -> list[list[float]]:
    rows = [RawRow(**{**r, "income": None if r["income"] != r["income"] else r["income"]}).model_dump() for r in rows]  # schema check
    return build_features(pd.DataFrame(rows)).values.tolist()
