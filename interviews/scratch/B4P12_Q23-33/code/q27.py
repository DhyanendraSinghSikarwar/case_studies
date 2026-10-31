# Q27: storage tiering on an invented access log. Relative cost units per TB-month; NOT prices.
import random
rng = random.Random(27)
HOT, IA, ARC = 1.00, 0.50, 0.15            # storage cost per TB-month (relative units, assumed)
RET_IA, RET_ARC = 0.10, 1.00               # retrieval cost per TB read from that tier (assumed)
EGRESS = 0.60                              # cross-Region transfer per TB (assumed)
# 3 groups sized as in the prompt: 400 TB raw features, 60 TB snapshots, 5 TB artefacts
GROUPS = {"raw": (400, 800), "snap": (60, 120), "art": (5, 50)}
objs = []
for g, (tb, n) in GROUPS.items():
    for i in range(n):
        size = tb / n
        age = rng.randint(1, 400)                       # days since last access, from the log
        if g == "raw":   fut = rng.random() < (0.30 if age < 30 else 0.04 if age < 120 else 0.02)  # a few old files get re-read for retraining
        elif g == "snap": fut = rng.random() < (0.50 if age < 60 else 0.10)
        else:             fut = rng.random() < 0.90      # model artefacts: rollback needs them fast
        objs.append((g, size, age, fut))
def cost(policy):
    s = r = pen = 0.0
    for g, size, age, fut in objs:
        tier = policy(g, age)
        rate, ret = {"hot": (HOT, 0), "ia": (IA, RET_IA), "arc": (ARC, RET_ARC)}[tier]
        s += size * rate
        if fut: r += size * ret                         # one read in the next month
    return s, r, s + r
pols = {
 "all hot":                     lambda g, a: "hot",
 "IA>30d, archive>120d":        lambda g, a: "hot" if g == "art" or a <= 30 else "ia" if a <= 120 else "arc",
 "IA>30d only (no archive)":    lambda g, a: "hot" if g == "art" or a <= 30 else "ia",
 "aggressive: archive>30d":     lambda g, a: "hot" if g == "art" or a <= 30 else "arc",
 "oracle (knows future reads)": None,
}
print(f"{'policy':<30}{'storage':>9}{'retrieval':>10}{'total':>8}")
for k, p in pols.items():
    if p is None:
        s = r = 0.0
        for g, size, age, fut in objs:
            s += size * (HOT if fut else ARC)
        print(f"{k:<30}{s:>9.1f}{0:>10.1f}{s:>8.1f}"); continue
    s, r, t = cost(p); print(f"{k:<30}{s:>9.1f}{r:>10.1f}{t:>8.1f}")
# wrong guesses: archived objects that were read
wrong = [(g, size) for g, size, age, fut in objs if fut and pols["IA>30d, archive>120d"](g, age) == "arc"]
print("archived-then-read objects:", len(wrong), "TB:", round(sum(s for _, s in wrong), 1), "retrieval units:", round(sum(s for _, s in wrong) * RET_ARC, 1))
# egress: training Region differs from data Region, one 60 TB snapshot read per run, 12 runs a month
print("cross-Region read of one 60 TB snapshot:", 60 * EGRESS, "units; 12 runs a month:", 12 * 60 * EGRESS, "units; copy once, then read local:", 60 * EGRESS, "units")
print("break-even monthly read probability: archive beats IA only if P(read) <", round((IA - ARC) / RET_ARC, 2), "; IA beats hot if P(read) <", round((HOT - IA) / RET_IA, 1), "(above 1 means always)")
print("total TB:", round(sum(o[1] for o in objs), 1))
