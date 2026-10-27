"""Q22: WAPE, bias and forecast value added (FVA) on an invented, seeded table of 50 items. Stdlib only."""
import random
random.seed(22)
# class: (count, typical level, model noise, model bias, override rate, planner skill: share of error the planner removes; negative = adds error)
SPEC = {"fast": (20, 100, 0.06, 0.00, 0.04, -0.3), "slow": (10, 12, 0.35, 0.05, 0.08, 0.2),
        "promo": (12, 150, 0.20, -0.20, 0.22, 0.7), "intermittent": (8, 3, 0.9, -0.10, 0.10, 0.0)}
rows = []
for cls, (n, lvl, noise, b, orate, skill) in SPEC.items():
    for k in range(n):
        a = max(0, round(random.gauss(lvl, lvl * 0.25)))
        m = max(0.0, a * (1 + b) + random.gauss(0, noise * max(a, 1)))
        ov = None
        if random.random() < orate:
            ov = a + (m - a) * (1 - skill) + random.gauss(0, 0.02 * max(a, 1))   # planner moves the forecast toward (or away from) the truth
        rows.append((f"{cls[:2]}{k}", cls, a, round(m, 1), None if ov is None else round(max(ov, 0), 1)))
def wape(pairs): return sum(abs(a - f) for a, f in pairs) / max(sum(a for a, f in pairs), 1e-9)
def bias(pairs): return sum(f - a for a, f in pairs) / max(sum(a for a, f in pairs), 1e-9)   # + = over-forecast
assert abs(wape([(100, 104), (120, 112)]) - 12 / 220) < 1e-12      # hand check: (4+8)/220
no = sum(r[4] is not None for r in rows)
print(f"items {len(rows)}, overridden {no} = {100*no/len(rows):.0f}%  overall WAPE model {100*wape([(r[2], r[3]) for r in rows]):.1f}%  bias {100*bias([(r[2], r[3]) for r in rows]):+.1f}%")
print(f"\n{'class':14s}{'WAPE':>7s}{'bias':>8s}{'n':>4s}{'ovr':>4s}{'FVA on overridden (pts)':>25s}  decision")
for cls in SPEC:
    rs = [r for r in rows if r[1] == cls]; ov = [r for r in rs if r[4] is not None]
    w, b = wape([(r[2], r[3]) for r in rs]), bias([(r[2], r[3]) for r in rs])
    fva = 100 * (wape([(r[2], r[3]) for r in ov]) - wape([(r[2], r[4]) for r in ov])) if ov else None
    if len(ov) < 3: dec = "too few overrides to judge FVA; " + ("automate" if abs(b) < 0.1 and w < 0.15 else "keep review, fix model")
    elif fva <= 0: dec = "automate: overrides do not help"
    elif abs(b) > 0.1: dec = "overrides help because model is biased: fix the model bias, keep review till then"
    else: dec = "keep review"
    print(f"{cls:14s}{100*w:6.1f}%{100*b:+7.1f}%{len(rs):4d}{len(ov):4d}{'n/a' if fva is None else f'{fva:+.1f}':>25s}  {dec}")
by = {}
for r in rows: by.setdefault(r[1], []).append(r)
tot_a, tot_f = sum(r[2] for r in rows), sum(r[3] for r in rows)
print(f"\nwhole-portfolio total: actual {tot_a}, model {tot_f:.0f} -> total error {100*abs(tot_f-tot_a)/tot_a:.1f}% (cancelling) vs item-level WAPE above")
