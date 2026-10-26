from dataclasses import dataclass

@dataclass
class Evidence:
    pipeline_bug: bool            # null spike, schema/unit change, late data, version mismatch
    known_event: bool             # festival, campaign, holiday, planned change
    feature_important: bool       # importance or attribution share is material
    prediction_shift: bool        # score or positive-rate moved beyond its band
    labels_matured: bool
    perf_drop: bool | None        # None when labels not matured

def triage(e: Evidence):
    if e.pipeline_bug:
        return "FIX_PIPELINE", "data or code problem; fix upstream, do not retrain on bad data (roll back if the bad data is already served)"
    if e.known_event:
        return "NO_ACTION_WATCH", "explained by a known event; compare with same-period baseline and re-check after it ends"
    if not e.feature_important and not e.prediction_shift:
        return "NO_ACTION", "feature does not matter to the model and outputs are stable; log and tune the alert"
    if e.labels_matured and e.perf_drop:
        return "RETRAIN_OR_ROLLBACK", "matured labels confirm a drop; retrain on fresh data, roll back if a recent release caused it"
    if e.labels_matured and not e.perf_drop:
        return "NO_ACTION", "matured labels show no drop; drift is harmless for now"
    if e.prediction_shift:
        return "RECALIBRATE_AND_WATCH", "outputs moved but no labels yet; check calibration, estimate performance without labels, wait for labels"
    return "WATCH", "important feature moved, outputs stable, labels not matured; keep watching"

cases = {
 "A null spike after a schema change": Evidence(True, False, True, True, False, None),
 "B Diwali week traffic":              Evidence(False, True, True, True, False, None),
 "C minor feature, outputs stable":    Evidence(False, False, False, False, True, False),
 "D key feature, labels show drop":    Evidence(False, False, True, True, True, True),
}
for name, ev in cases.items():
    a, r = triage(ev)
    print(f"{name:38s} -> {a:22s} | {r}")
