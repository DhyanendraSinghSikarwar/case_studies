# Q27: classify postmortem action items and rewrite the vague ones. Illustrative items, plain Python.
vague_words = ("be more careful", "add a review", "remind", "double-check", "pay more attention")
items = [
 "Be more careful when changing feature code",
 "Add a review for every model deploy",
 "Remind the team to check the holdout before promoting",
 "Double-check the config before merge",
 "Add a review for schema changes",
 "Be more careful with the canary percentage",
 "Add a review step for rollback decisions",
 "Pay more attention to the dashboard after a deploy",
 "Add a review of alert thresholds",
 "Be more careful to run the replay test",
 "Add a review for data-source changes",
 "Block promotion in CI when holdout AUC is more than 0.02 below the champion (owner: MLOps, due 2026-11-30)",
 "Auto-rollback when the canary error z-score is 3 or more (owner: platform, due 2026-12-15)",
 "Alert when feature null-rate changes by more than 5 points in an hour (owner: data eng, due 2026-11-20)",
]
vague = [i for i in items if any(w in i.lower() for w in vague_words)]
print(f"{len(vague)} of {len(items)} items are vague = {len(vague)/len(items):.1%}")
assert len(items) == 14 and len(vague) == 11 and round(100 * 11 / 14) == 79
# rewrite table: vague item -> mechanism that does not depend on memory
rewrite = {
 0:  ("Contract test on the feature code in CI", "CI blocks merge when feature definitions differ between train and serve"),
 1:  ("Required status check plus CODEOWNERS on deploy config", "merge button disabled without model-owner approval and a green gate"),
 2:  ("Promotion pipeline step compares holdout AUC with champion", "promotion fails if AUC is more than 0.02 below champion"),
 3:  ("Config schema validation in CI", "unknown or out-of-range keys fail the build"),
 4:  ("Schema and unit contract check on upstream tables", "ingest fails loudly on a changed type, range or unit"),
 5:  ("Rollout tool enforces stage sizes", "stages fixed at 5, 25, 50, 100 percent; larger jumps rejected"),
 6:  ("Written rollback rule in the runbook and the deploy tool", "rollback triggers fire automatically on the stated thresholds"),
 7:  ("Post-deploy watch as an automatic 30-minute gate", "deploy marked complete only after dashboards stay green for 30 minutes"),
 8:  ("Alert thresholds stored as code with tests", "a threshold change needs a replay of 8 weeks of history in CI"),
 9:  ("Shadow replay test runs on every release candidate", "release candidate blocked if replay differs by more than a stated tolerance"),
 10: ("Data-source registry with owners and change notices", "unregistered source in a pipeline fails validation"),
}
def good(item):
    """An action item is good when it has an owner, a date, a mechanism and a way to check it is done."""
    return all(k in item for k in ("owner", "due", "mechanism", "done_when"))
rewritten = []
for idx, (mech, done_when) in rewrite.items():
    rewritten.append({"from": items[idx], "owner": "role: platform/MLOps/data eng", "due": "within 90 days", "mechanism": mech, "done_when": done_when})
assert len(rewritten) == 11 and all(good(r) for r in rewritten)
assert not any(w in r["mechanism"].lower() + r["done_when"].lower() for r in rewritten for w in vague_words)
assert not any(good({"item": i}) for i in vague)                  # the vague wording alone fails the test
print(f"after rewrite: {len(rewritten)} items now have an owner role, a date, a mechanism and a done-when test")
# an illustrative timeline: detection delay and time to mitigate
deploy, detect, rollback_start, rollback_done = 14*60, 14*60+47, 14*60+52, 15*60+5     # minutes after midnight
print(f"detection delay {detect-deploy} min, decision to rollback done {rollback_done-detect} min, total harm window {rollback_done-deploy} min")
assert (detect - deploy, rollback_done - detect, rollback_done - deploy) == (47, 18, 65)
