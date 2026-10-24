# SYNTHETIC illustration: offline headline score rises while the score on CURRENT traffic falls, and a length-biased judge.
import random
random.seed(21)
cats = ["billing", "how_to", "new_feature"]
offline_mix = {"billing": 0.60, "how_to": 0.30, "new_feature": 0.10}     # eval set frozen from last year's traffic (assumed)
prod_mix_now = {"billing": 0.35, "how_to": 0.30, "new_feature": 0.35}    # traffic today (assumed)
# true per-category accuracy of 4 releases (assumed): tuning targets billing, new_feature quietly degrades
acc = {"r1": {"billing": .70, "how_to": .75, "new_feature": .60}, "r2": {"billing": .80, "how_to": .75, "new_feature": .55},
       "r3": {"billing": .88, "how_to": .74, "new_feature": .45}, "r4": {"billing": .95, "how_to": .73, "new_feature": .35}}
print("release  offline(frozen mix)  reweighted to today's traffic")
for r, a in acc.items():
    off = sum(offline_mix[c] * a[c] for c in cats); now = sum(prod_mix_now[c] * a[c] for c in cats)
    print(f"{r}       {off:.3f}              {now:.3f}")
# judge with length bias: score = quality + 0.08 * extra_words/10 ; users prefer concise. Longer answers win with the judge.
def judge_score(quality, words): return quality + 0.08 * (words - 40) / 10
def user_sat(quality, words): return quality - 0.05 * max(0, words - 60) / 10
rows = []
for _ in range(2000):
    q = random.gauss(0, 1); w = random.choice([30, 60, 120, 200]); rows.append((judge_score(q, w), user_sat(q, w), w, q))
def corr(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** .5
js = [r[0] for r in rows]; us = [r[1] for r in rows]; ws = [r[2] for r in rows]
print(f"\ncorr(judge score, length) = {corr(js, ws):+.2f}   corr(user satisfaction, length) = {corr(us, ws):+.2f}   corr(judge, user) = {corr(js, us):+.2f}")
for w in (30, 60, 120, 200):
    sel = [r for r in rows if r[2] == w]
    print(f"  {w:3d} words: mean judge {sum(r[0] for r in sel)/len(sel):+.2f}   mean user sat {sum(r[1] for r in sel)/len(sel):+.2f}")
