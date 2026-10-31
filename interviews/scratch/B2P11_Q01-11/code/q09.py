# Trifecta review by brute force. Tool list and leg tags are a made-up assistant design (SYNTHETIC).
import itertools, random
P, U, E = "private_data", "untrusted_content", "external_comms"
TOOLS = {"read_inbox": {P, U}, "search_web": {U}, "read_crm": {P}, "send_email": {E}, "render_markdown_images": {E},
         "calendar_read": {P}, "run_sql_readonly": {P}, "fetch_url": {U, E}, "write_note_local": set()}
names = list(TOOLS)
def legs(subset): return set().union(*(TOOLS[t] for t in subset)) if subset else set()
full = [s for r in range(len(names) + 1) for s in itertools.combinations(names, r) if legs(s) == {P, U, E}]
print(f"{len(full)} of {2 ** len(names)} possible tool subsets contain all three legs")
# closed form check by inclusion-exclusion over which leg is missing (subsets of tools that avoid a leg: only tools w/o that leg)
def avoid(*L): return 2 ** sum(1 for t in names if not (TOOLS[t] & set(L)))
cf = 2 ** len(names) - avoid(P) - avoid(U) - avoid(E) + avoid(P, U) + avoid(P, E) + avoid(U, E) - avoid(P, U, E)
print(f"inclusion-exclusion count: {cf}  (matches: {cf == len(full)})")
shipping = tuple(names[:8])   # a plausible first design: everything except write_note_local
print("proposed design legs:", sorted(legs(shipping)))
fixes = []
for t in shipping:            # smallest single-tool removals that break a leg
    rest = tuple(x for x in shipping if x != t)
    if legs(rest) != {P, U, E}: fixes.append(t)
print("single-tool removals that break the trifecta:", fixes or "none (need to remove several)")
# minimum number of tools to remove, by search
for k in range(1, len(shipping) + 1):
    ok = [c for c in itertools.combinations(shipping, k) if legs(tuple(x for x in shipping if x not in c)) != {P, U, E}]
    if ok: print(f"smallest removal size: {k}; sets: {ok}"); break
# why not just a smarter filter: ASSUMED 95% catch rate per attempt, attacker retries (independent attempts is itself an assumption)
random.seed(1)
for n in (1, 10, 50):
    sim = sum(any(random.random() > 0.95 for _ in range(n)) for _ in range(20000)) / 20000
    print(f"filter assumed 95% effective, attacker tries {n:2d} variants: P(at least one gets through) closed form {1 - 0.95 ** n:.3f}, simulated {sim:.3f}")
