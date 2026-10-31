import yaml

LAYERS = """
layers:
  - {name: serving_health,  owner: platform/SRE,  cadence: realtime,  needs_labels: false, catches: latency, errors, saturation (Part 6)}
  - {name: data_quality,    owner: data eng,      cadence: per batch, needs_labels: false, catches: nulls, schema, range, freshness, volume}
  - {name: feature_drift,   owner: ML eng,        cadence: daily,     needs_labels: false, catches: input distribution change}
  - {name: prediction_drift,owner: ML eng,        cadence: hourly,    needs_labels: false, catches: score or positive-rate change}
  - {name: performance,     owner: DS / ML eng,   cadence: weekly,    needs_labels: true,  catches: real accuracy, AUC, calibration loss}
  - {name: fairness,        owner: DS + risk,     cadence: monthly,   needs_labels: true,  catches: gap between groups}
  - {name: business_outcome,owner: product,       cadence: weekly,    needs_labels: true,  catches: conversion, loss, revenue effect}
"""
cfg = yaml.safe_load(LAYERS)
rows = cfg["layers"]
print("layers parsed:", len(rows))
print("need labels :", [r["name"] for r in rows if r["needs_labels"]])
print("no labels   :", [r["name"] for r in rows if not r["needs_labels"]])
print("realtime or per-batch or hourly (no labels):",
      [r["name"] for r in rows if not r["needs_labels"] and r["cadence"] in ("realtime", "per batch", "hourly")])
for r in rows:
    print(f"{r['name']:<17} {r['cadence']:<10} owner={r['owner']}")
