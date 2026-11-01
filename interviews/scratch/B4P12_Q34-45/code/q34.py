# Q34: invented maturity rubric (0-2 per dimension) and a 6-month roadmap. Abstract, hand-checkable.
dims = ["training", "deploy", "monitoring", "registry", "tests", "data_versioning"]
team = {"training": 0, "deploy": 0, "monitoring": 0, "registry": 0, "tests": 0, "data_versioning": 0}
# 0 = manual, 1 = automated pipeline, 2 = automated + gated (Google-style levels 0/1/2, simplified)
def level(score, n):
    pct = score / (2 * n)
    return 0 if pct < 0.34 else 1 if pct < 0.75 else 2
roadmap = [
    ("Q1", "registry", "Part 4 Q25 style: log runs and register models in a tracker; stop the shared folder",
     "100% of prod models have a registered version id"),
    ("Q1", "training", "move notebook to a script with fixed seed and pinned deps (Part 1)",
     "one command reproduces last model"),
    ("Q2", "deploy", "one CI job: tests + build + deploy to staging (Part 7 Q9)",
     "manual deploys per month falls to 0 for staging"),
    ("Q1", "tests", "add 5 unit tests for feature code and one data-schema check (Part 1)", "CI red on a deliberately broken column"),
    ("Q2", "data_versioning", "pin training data by hash or snapshot id (Part 4)", "every model record names its data version"),
    ("Q2", "monitoring", "replace spreadsheet with 3 automated checks and one alert (Part 8 Q2)",
     "time-to-detect drops from days to hours"),
]
def run(state):
    s = sum(state.values()); return s, level(s, len(dims))
s, l = run(team); print(f"start: score {s}/12, level {l}")
for q, d, step, ind in roadmap:
    team[d] = 1
    s, l = run(team)
    print(f"{q} step on {d}: score {s}/12, level {l}\n    do: {step}\n    indicator: {ind}")
assert run(team) == (6, 1), run(team)
print("trap: no feature store or Kubeflow until every dimension is at 1 and the pain is named")
print("final:", run(team))
