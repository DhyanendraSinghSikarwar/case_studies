import pandas as pd


def impute_and_scale(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Fill NaN with the column median, then standardise (mean 0, std 1, population std).

    Returns a NEW frame; the input is never changed.
    Raises ValueError for: missing columns, all-NaN column, zero-variance column.
    An empty frame (no rows) is returned as an empty float frame for those columns.
    """
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    out = df.copy()
    if len(out) == 0:
        out[cols] = out[cols].astype("float64")
        return out
    for c in cols:
        s = out[c].astype("float64")
        if s.isna().all():
            raise ValueError(f"column {c!r} is all NaN: no median to impute")
        s = s.fillna(s.median())
        std = s.std(ddof=0)
        if std == 0:
            raise ValueError(f"column {c!r} is constant: cannot standardise (std = 0)")
        out[c] = (s - s.mean()) / std
    return out
