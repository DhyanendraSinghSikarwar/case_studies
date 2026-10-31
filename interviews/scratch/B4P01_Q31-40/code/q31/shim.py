"""Rollout step 1: ship 1.5 with the new API AND the old one, the old one warns."""
import warnings
def scale(x, *, unit=None):
    if unit is None:
        warnings.warn("scale(x) without unit is deprecated; pass unit= (removed in 2.0)", DeprecationWarning, stacklevel=2)
        unit = 100
    return x / unit
warnings.simplefilter("always")
print(scale(250, unit=100))      # new style, silent
print(scale(250))                # old style, still works, warns
