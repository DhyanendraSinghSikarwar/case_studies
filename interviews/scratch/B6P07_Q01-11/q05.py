harm, benign = 2_000, 98_000
tp, fp = 1_800, 3_000
fn = harm - tp
fpr = fp / benign; recall = tp / harm; precision = tp / (tp + fp)
print(f"benign block rate {fpr:.2%}; recall {recall:.0%}; precision {precision:.1%}; missed harmful {fn}; total blocks {tp+fp}")
assert round(fpr, 4) == 0.0306 and recall == 0.9 and precision == 0.375 and fn == 200 and harm + benign == 100_000
print(f"prevalence {harm/(harm+benign):.0%}; benign users blocked per harmful caught: {fp/tp:.2f}")
assert round(fp/tp, 2) == 1.67
# Tuning: compare two illustrative operating points on the same 100,000 queries
def point(name, rec, fpr_):
    t = rec*harm; f = fpr_*benign
    print(f"{name:22} recall {rec:.0%} fpr {fpr_:.2%} blocks {t+f:,.0f} precision {t/(t+f):.1%} missed {harm-t:.0f} benign blocked {f:,.0f}")
    return t, f
point("current", 0.90, 3000/98000)
a = point("stricter on benign", 0.85, 0.01)
b = point("looser", 0.95, 0.08)
assert round(a[0]/(a[0]+a[1]), 3) == 0.634 and round(b[1]) == 7840
# Cost-weighted choice: the best point depends on the cost ratio (illustrative: one miss = 50 or 10 wrongly blocked benign queries)
pts = {"current": (0.90, 3000/98000), "stricter": (0.85, 0.01), "looser": (0.95, 0.08)}
def cost(rec, fpr_, cm): return (1-rec)*harm*cm + fpr_*benign
for cm in (50, 10):
    c = {k: round(cost(r, f, cm)) for k, (r, f) in pts.items()}
    print(f"miss costs {cm}x a wrong block:", c, "-> best:", min(c, key=c.get))
assert {k: round(cost(r, f, 50)) for k, (r, f) in pts.items()} == {"current": 13000, "stricter": 15980, "looser": 12840}
assert {k: round(cost(r, f, 10)) for k, (r, f) in pts.items()} == {"current": 5000, "stricter": 3980, "looser": 8840}
# Two-tier idea: block only above a high score; mid band goes to a soft-refuse / human review (illustrative split)
hi_tp, hi_fp = 1500, 200; mid_tp, mid_fp = 300, 2800
print(f"two-tier: auto-block {hi_tp+hi_fp} (precision {hi_tp/(hi_tp+hi_fp):.1%}); review band {mid_tp+mid_fp} (precision {mid_tp/(mid_tp+mid_fp):.1%})")
assert hi_tp + mid_tp == tp and hi_fp + mid_fp == fp and round(hi_tp/(hi_tp+hi_fp), 3) == 0.882
