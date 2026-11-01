import warnings

def make_features(df_rows, *, fill=0):
    """New API (1.2+)."""
    return [fill if v is None else v for v in df_rows]

def build_features(df_rows):
    """Old name, kept as a shim for one minor series, removed in 2.0."""
    warnings.warn(
        "build_features() is deprecated since 1.2 and will be removed in 2.0; use make_features()",
        DeprecationWarning,
        stacklevel=2,          # point at the CALLER's line, not this file
    )
    return make_features(df_rows)
