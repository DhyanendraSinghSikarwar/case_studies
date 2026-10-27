"""Q14: series count, rows per day and platform cost shape for three modelling choices (abstract units)."""
stores, skus, horizon = 3000, 40000, 14
cells = stores * skus
print("store x SKU cells:", f"{cells:,}")
for ranged in (0.10, 0.25):   # invented share of SKUs actually ranged (sold) in a given store
    series = int(cells * ranged)
    rows = series * horizon
    print(f"ranged {ranged:.0%}: series={series:,}  forecast rows/day (14 days)={rows:,}")
assert 3000 * 40000 == 120_000_000
series = int(cells * 0.10)

# platform cost shape, abstract units. Invented: each model fit has a fixed overhead (load data, start, register)
FIXED, PER_SERIES_COMPUTE = 5.0, 0.01           # units per fit; units per series of actual learning work
regions, classes = 12, 4                        # invented: per-group model = region x item class
options = {
  "one global model":      dict(models=1,                  series_fitted=series),
  "per-group models":      dict(models=regions * classes,  series_fitted=series),
  "per-series models":     dict(models=series,             series_fitted=series),
}
print(f"\n{'option':20s}{'models to manage':>18s}{'fit cost (units)':>20s}")
base = None
for k, v in options.items():
    cost = v["models"] * FIXED + v["series_fitted"] * PER_SERIES_COMPUTE
    base = base or cost
    print(f"{k:20s}{v['models']:18,d}{cost:20,.0f}  x{cost/base:.1f} vs global")
