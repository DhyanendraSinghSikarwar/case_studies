import math
def lr_at(step, total, peak=3e-4, warmup_frac=0.02, min_ratio=0.1, kind="cosine", decay_frac=0.1):
    w = int(total * warmup_frac); lo = peak * min_ratio
    if step < w: return peak * (step + 1) / w
    if kind == "cosine":
        p = (step - w) / (total - w)
        return lo + 0.5 * (peak - lo) * (1 + math.cos(math.pi * p))
    d0 = int(total * (1 - decay_frac))            # WSD: warmup, stable, short decay
    if step < d0: return peak
    return peak + (lo - peak) * (step - d0) / (total - d0)
T = 1000
print("step   cosine     wsd")
for s in [0, 10, 19, 20, 250, 500, 750, 899, 900, 950, 999]:
    print(f"{s:4d} {lr_at(s,T):.2e} {lr_at(s,T,kind='wsd'):.2e}")
