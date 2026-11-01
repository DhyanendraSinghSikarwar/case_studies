# Standalone, numpy only. SYNTHETIC queries, SYNTHETIC router confidences and ASSUMED per-stage effects. Shows the gating skeleton and how to read ablation metrics.
import numpy as np
rng = np.random.default_rng(3)
TYPES = ["identifier", "conversational", "multipart", "plain"]; MIX = [0.30, 0.20, 0.15, 0.35]
BASE = {"identifier": 0.85, "conversational": 0.45, "multipart": 0.35, "plain": 0.75}            # ASSUMED hit@5 of the plain pipeline
REWRITE = {"identifier": -0.25, "conversational": +0.25, "multipart": 0.0, "plain": -0.03}      # ASSUMED effect of a rewrite on hit rate
DECOMP = {"identifier": -0.10, "conversational": 0.0, "multipart": +0.30, "plain": -0.05}       # ASSUMED effect of decomposition
CALLS = {"rewrite": 1, "decompose": 1}                                                          # extra LLM calls per stage (ASSUMED)

def router(true_type):                           # SYNTHETIC router: right label 85 percent of the time, with a confidence score
    right = rng.random() < 0.85
    label = true_type if right else rng.choice([t for t in TYPES if t != true_type])
    conf = float(np.clip(rng.normal(0.85 if right else 0.55, 0.12), 0, 1)); return label, conf

def plan(label, conf, tau=0.7, mode="gated"):    # which stages run; the ORIGINAL query is ALWAYS searched (fallback)
    if mode == "none": return set()
    if mode == "rewrite_all": return {"rewrite"}
    if mode == "decompose_all": return {"decompose"}
    if mode == "all": return {"rewrite", "decompose"}
    if conf < tau: return set()                  # not confident: run the safe path, original query only
    return {"rewrite"} if label == "conversational" else {"decompose"} if label == "multipart" else set()

def run_mode(mode, n=4000, tau=0.7):
    log = []
    for _ in range(n):
        t = rng.choice(TYPES, p=MIX); label, conf = router(t); stages = plan(label, conf, tau, mode)
        p = BASE[t] + (REWRITE[t] if "rewrite" in stages else 0) + (DECOMP[t] if "decompose" in stages else 0)
        # original query is also searched and fused, so a harmful stage costs only part of its effect (ASSUMED: harm halved when fused with the original)
        if p < BASE[t]: p = BASE[t] + (p - BASE[t]) * 0.5
        log.append({"type": t, "label": label, "conf": conf, "stages": sorted(stages), "hit": bool(rng.random() < min(max(p, 0), 1)), "calls": sum(CALLS[s] for s in stages)})
    return log
def summarise(log):
    hit = np.mean([r["hit"] for r in log]); calls = np.mean([r["calls"] for r in log])
    by = {t: np.mean([r["hit"] for r in log if r["type"] == t]) for t in TYPES}
    return hit, calls, by

print(f"{'variant':16s}{'hit@5':>8s}{'extra calls/q':>15s}" + "".join(f"{t[:6]:>9s}" for t in TYPES))
res = {}
for mode in ["none", "rewrite_all", "decompose_all", "all", "gated"]:
    lg = run_mode(mode); h, c, by = summarise(lg); res[mode] = (h, c, lg)
    print(f"{mode:16s}{h:>8.3f}{c:>15.2f}" + "".join(f"{by[t]:>9.3f}" for t in TYPES))

lg = res["gated"][2]
acc = np.mean([r["label"] == r["type"] for r in lg]); ran = [r for r in lg if r["stages"]]
print(f"\nrouter accuracy vs true labels (synthetic): {acc:.3f} | share of queries where any stage ran: {len(ran) / len(lg):.2f}")
for tau in (0.5, 0.7, 0.85):                    # confidence threshold sweep from logs
    lg2 = run_mode("gated", tau=tau); h, c, _ = summarise(lg2); print(f"  tau={tau}: hit@5 {h:.3f}, extra calls/q {c:.2f}")
# ablation value of each stage inside the gated system (switch one off, keep the rest)
def value_of(stage, n=20000):
    on = []; off = []
    for _ in range(n):
        t = rng.choice(TYPES, p=MIX); label, conf = router(t); st = plan(label, conf)
        p = BASE[t] + (REWRITE[t] if "rewrite" in st else 0) + (DECOMP[t] if "decompose" in st else 0); p = BASE[t] + (p - BASE[t]) * 0.5 if p < BASE[t] else p
        st2 = st - {stage}; q = BASE[t] + (REWRITE[t] if "rewrite" in st2 else 0) + (DECOMP[t] if "decompose" in st2 else 0); q = BASE[t] + (q - BASE[t]) * 0.5 if q < BASE[t] else q
        on.append(p); off.append(q)
    return np.mean(on) - np.mean(off)
print("\nablation inside the gated system (expected hit@5 gain from having the stage; synthetic):", {s: round(float(value_of(s)), 3) for s in ["rewrite", "decompose"]})
assert res["gated"][0] > res["all"][0] and res["gated"][1] < res["all"][1]            # gating beats always-on and costs fewer calls
assert all(r["stages"] == [] or r["conf"] >= 0.7 for r in lg)                           # low-confidence queries always take the safe path
