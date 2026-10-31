import math
words = 150
en_tok, hi_tok = words * 1.3, words * 4
ratio = hi_tok / en_tok
print(f"tokens per answer: English {en_tok:.0f}, Hindi {hi_tok:.0f}; cost ratio {ratio:.2f}x")
assert en_tok == 195 and hi_tok == 600 and round(ratio, 2) == 3.08
n = 200
hi_ok, en_ok = 148, 176
ph, pe = hi_ok / n, en_ok / n
assert (ph, pe) == (0.74, 0.88)
gap_abs = pe - ph
print(f"absolute gap {gap_abs*100:.0f} points; relative gap {gap_abs/pe*100:.1f}% of English; error rate {1-ph:.0%} vs {1-pe:.0%} = {(1-ph)/(1-pe):.2f}x")
assert round(gap_abs * 100) == 14 and round(gap_abs / pe * 100, 1) == 15.9 and round((1 - ph) / (1 - pe), 2) == 2.17
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
for nm, k in (("Hindi", hi_ok), ("English", en_ok)):
    lo, hi = wilson(k, n); print(f"{nm} 95% Wilson interval {lo*100:.1f}% to {hi*100:.1f}%")
se = math.sqrt(ph * (1 - ph) / n + pe * (1 - pe) / n)
z = gap_abs / se
print(f"difference SE {se*100:.2f} pts, z = {z:.2f}, 95% CI of gap {(gap_abs-1.96*se)*100:.1f} to {(gap_abs+1.96*se)*100:.1f} pts")
assert round(z, 2) == 3.63 and (gap_abs - 1.96 * se) > 0
cpc_h, cpc_e = hi_tok / ph, en_tok / pe
print(f"output tokens per correct answer: Hindi {cpc_h:.1f}, English {cpc_e:.1f}, ratio {cpc_h/cpc_e:.2f}x")
assert round(cpc_h / cpc_e, 2) == 3.66
