# TOY (synthetic) eval-suite lifecycle: capability suite -> graduate stable passes to a regression suite -> saturation -> add harder cases.
# The "model" is a mock: P(pass) = logistic(skill - difficulty). No LLM, no network.
import math, random
random.seed(7)
def p_pass(skill, diff): return 1 / (1 + math.exp(-(skill - diff)))
def run(skill, cases, trials=5):
    return {cid: sum(random.random() < p_pass(skill, d) for _ in range(trials)) for cid, d in cases.items()}
# v1 suite: 60 cases, difficulty from -1 (easy) to 5 (hard)
suite = {f"c{i:02d}": -1 + 6 * i / 59 for i in range(60)}
regression, capability = {}, dict(suite)
print("version  skill  capability_cases  mean_pass(cap)  graduated_total")
for ver, skill in [("v1", 1.0), ("v2", 2.0), ("v3", 3.5), ("v4", 5.0), ("v5", 8.0)]:
    res = run(skill, capability)
    mean = sum(res.values()) / (5 * len(capability))
    grads = [c for c, k in res.items() if k == 5]          # passed 5/5 trials -> stable -> graduate
    for c in grads: regression[c] = capability.pop(c)
    print(f"{ver}      {skill:4.1f}   {len(capability)+len(grads):3d}               {mean:5.2f}           {len(regression):3d}")
    if mean > 0.9 and len(capability) < 15:             # saturated: add harder tasks
        for j in range(20): capability[f"h{j:02d}"] = 5 + 3 * j / 19
        print(f"        capability suite near saturation (mean {mean:.2f}); added 20 harder cases")
# regression run: candidate keeps skill 8 overall; the "bad" one breaks one category (cases c10-c19). Gate = fail if any case is not 5/5.
def cand_run(cases, broken_block, trials=5):
    out = {}
    for cid, d in cases.items():
        s = 8.0 - (9.0 if broken_block and "c10" <= cid <= "c19" else 0)
        out[cid] = sum(random.random() < p_pass(s, d) for _ in range(trials))
    return out
for label, brk in [("healthy candidate", False), ("candidate that breaks c10-c19", True)]:
    res = cand_run(regression, brk)
    bad = sorted(c for c, k in res.items() if k < 5)
    in_block = sum("c10" <= c <= "c19" for c in bad)
    hard_fail = sorted(c for c, k in res.items() if k <= 2)       # looser gate: a case failing at least 3 of 5 trials
    print(f"{label:30} regression cases {len(regression)}; not 5/5: {len(bad)} (in c10-c19: {in_block}) -> strict gate {'FAIL' if bad else 'PASS'}; "
          f"cases passing <=2/5: {len(hard_fail)} -> loose gate {'FAIL' if hard_fail else 'PASS'}")
print("pass^3 check, 75% per-trial success:", round(0.75 ** 3, 4), "(0.75^3 = 0.421875)")
