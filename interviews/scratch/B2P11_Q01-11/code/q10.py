# SYNTHETIC layered-defence model. Every catch rate below is ASSUMED, not measured on any real system.
# Probabilistic layers: input screen, delimiting/hierarchy, output filter. Deterministic layer: egress allowlist (covers ONE harm channel only).
import numpy as np
rng = np.random.default_rng(3)
N = 200000
catch = {"input screen": 0.80, "delimiting+hierarchy": 0.70, "output filter": 0.70}
print("assumed per-layer catch rates:", catch)
indep = 1.0
for c in catch.values(): indep *= (1 - c)
print(f"A) independent layers: expected fraction of attacks that get past all three = {indep:.4f}")
# B) correlated layers: each attack has a hidden 'subtlety' s~U(0,1); a layer catches it with prob = clip(base_catch - strength*(s-0.5)) so subtle attacks beat ALL layers more often.
def sim(strength):
    s = rng.random(N); passed = np.ones(N, bool)
    for c in catch.values():
        p = np.clip(c - strength * (s - 0.5), 0, 1)
        passed &= rng.random(N) >= p
    return passed, s
for strength in (0.0, 1.0, 2.0):
    passed, s = sim(strength)
    print(f"B) subtlety effect {strength:.1f}: past all three = {passed.mean():.4f}   (compare independent {indep:.4f}; the top-10% subtlest attacks pass {passed[s > .9].mean():.3f})")
# C) deterministic egress allowlist: attacks whose harm is 'send data to an outside address' (assume 60% of attacks) are blocked 100%.
passed, s = sim(1.0)
exfil = rng.random(N) < 0.60
residual = passed & ~exfil
print(f"C) add egress allowlist (assume 60% of attacks need an outside address): residual = {residual.mean():.4f}")
print("   -> deterministic layer shrinks the attack surface; it does not touch in-scope misuse (e.g. wrong refund within the allowed tool).")
