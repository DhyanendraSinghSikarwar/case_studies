"""Q39: check a team's GPU request against its quota and the cluster total. Numbers are the design example: 16 GPUs, 4 teams."""
CLUSTER_GPUS = 16
QUOTA = {"team-vision": 4, "team-nlp": 5, "team-speech": 3, "team-research": 2}   # sum 14; 2 left as shared burst/reserve
USED  = {"team-vision": 3, "team-nlp": 5, "team-speech": 0, "team-research": 1}
assert sum(QUOTA.values()) <= CLUSTER_GPUS

def check(team, want, borrow_ok=False):
    if team not in QUOTA: return "DENY: unknown team"
    if want <= 0: return "DENY: request must be positive"
    free_quota = QUOTA[team] - USED[team]
    if want <= free_quota: return f"ADMIT: {want} of {free_quota} free quota GPUs"
    spare = CLUSTER_GPUS - sum(USED.values())          # idle GPUs anywhere
    if borrow_ok and want - free_quota <= spare:
        return f"ADMIT as preemptible: {free_quota} in quota + {want - free_quota} borrowed (spare={spare})"
    return f"QUEUE/DENY: wants {want}, quota free {free_quota} (hard limit {QUOTA[team]})"

for team, want, b in [("team-vision", 1, False), ("team-vision", 2, False), ("team-vision", 2, True),
                      ("team-nlp", 1, False), ("team-nlp", 1, True), ("team-ghost", 1, False), ("team-speech", 0, False)]:
    print(f"{team:14} wants {want} borrow={b!s:5} -> {check(team, want, b)}")
