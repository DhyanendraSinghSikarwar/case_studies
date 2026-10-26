import io
import pandas as pd

# Simulated incident: on 2026-03-02 the upstream income feed switched from rupees to thousands of rupees.
LOG = """ts,event,who
2026-03-02 02:00,fault_start: upstream feed changes income unit,upstream-team
2026-03-02 02:30,first bad scores served,model-service
2026-03-04 09:15,business user notices approval rate fell,ops-analyst
2026-03-05 10:40,ticket opened to ml team,ops-analyst
2026-03-05 11:20,drift dashboard confirms income mean 1000x lower,ml-engineer
2026-03-05 12:05,mitigation: model switched to fallback rule,ml-engineer
2026-03-05 16:30,feed fixed upstream and unit converted,upstream-team
2026-03-06 09:00,model switched back after check,ml-engineer
"""
ev = pd.read_csv(io.StringIO(LOG), parse_dates=["ts"])
t = {k: ev.loc[ev.event.str.startswith(k), "ts"].iloc[0] for k in ("fault_start", "first bad", "business user", "ticket", "drift dashboard", "mitigation", "feed fixed", "model switched back")}
h = lambda a, b: round((t[b] - t[a]).total_seconds() / 3600, 1)
rows = [("time to first human notice (from fault start)", h("fault_start", "business user")),
        ("time to detect by ML team (from fault start)", h("fault_start", "drift dashboard")),
        ("time to mitigate (detect to fallback)", h("drift dashboard", "mitigation")),
        ("time to mitigate (from fault start)", h("fault_start", "mitigation")),
        ("time to resolve (fault start to switched back)", h("fault_start", "model switched back")),
        ("handoff delay (notice to ML ticket)", h("business user", "ticket"))]
for k, v in rows: print(f"{k:50s} {v:6.1f} h  ({v/24:.1f} d)")
print("bad predictions served for", round((t["mitigation"] - t["first bad"]).total_seconds() / 3600, 1), "hours")

gaps = pd.DataFrame([
    ("No input range or unit check on income", "Add a range and null check at feature ingestion; page on failure", "data-engineering", "2026-03-20"),
    ("Drift alert was not wired to a page or a ticket; dashboard only", "Alert on income mean and PSI-style score with a runbook (Q27, Q30)", "ml-platform", "2026-03-27"),
    ("No contract or change notice with the upstream team", "Schema and unit contract test in the feed's CI; change announcements", "upstream-team", "2026-04-10"),
], columns=["gap", "action", "owner", "due"])
print()
print(gaps.to_string(index=False))
