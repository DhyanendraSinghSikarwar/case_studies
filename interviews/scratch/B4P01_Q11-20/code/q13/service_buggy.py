"""A re-implementation written by someone else for the API. Looks fine, is not."""
import math
from features import COLUMNS


def predict_features(rows: list[dict]) -> list[list[float]]:
    out = []
    for r in rows:
        income = r["income"] if r["income"] is not None and r["income"] == r["income"] else 0.0  # BUG 1: fills 0
        ph = round(income / r["household"], 1)                                                    # BUG 2: 1 decimal
        out.append([r["age"], income, r["household"], ph, round(math.log1p(income), 4), int(r["age"] >= 60)])
    return out
