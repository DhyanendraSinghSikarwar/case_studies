import math
acc = {"start": 0.92, "middle": 0.71, "end": 0.85}
n = 100
overall = sum(acc.values()) / 3
print(f"overall = {overall:.4f}")
assert abs(overall - 0.826667) < 1e-5
gap = acc["start"] - acc["middle"]
print(f"start - middle gap = {gap*100:.0f} points")
assert round(gap*100) == 21
def z2(p1, p2, n1=n, n2=n):
    se = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    return (p1-p2)/se, se
z, se = z2(0.92, 0.71)
lo, hi = gap - 1.96*se, gap + 1.96*se
print(f"gap 95% CI (unpaired normal approx): {lo*100:.1f} to {hi*100:.1f} points, z = {z:.2f}")
assert z > 3.5 and lo > 0.08
z_e, se_e = z2(0.92, 0.85)
print(f"start - end gap = 7 points, z = {z_e:.2f}, 95% CI {(0.07-1.96*se_e)*100:.1f} to {(0.07+1.96*se_e)*100:.1f}")
assert z_e < 1.96
# illustrative cost of long context vs retrieval at 3 per million input tokens
price = 3
ctx_tokens, rag_tokens = 100_000, 4_000
c_long = ctx_tokens * price / 1e6; c_rag = rag_tokens * price / 1e6
print(f"per call: long context {c_long:.3f}, retrieved passages {c_rag:.3f}, ratio {c_long/c_rag:.0f}x")
assert abs(c_long-0.30) < 1e-12 and abs(c_rag-0.012) < 1e-12 and c_long/c_rag == 25
# placing best passage first or last, with a 70/30 mix of start/end for the top passage
mix = 0.7*acc["start"] + 0.3*acc["end"]
print(f"if top passage always sits at the start or end (70/30): expected accuracy {mix:.3f}")
assert abs(mix - 0.899) < 1e-9
