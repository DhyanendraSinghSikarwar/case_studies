# SYNTHETIC canary. Quality = per-request pass/fail from a MOCK judge. Baseline pass rate 0.90 (ASSUMED).
import hashlib, math
import numpy as np
rng = np.random.default_rng(5)
def bucket(user_id, salt="qa-v3-canary"):             # sticky, deterministic assignment: same user always same arm
    return int(hashlib.sha256((salt + user_id).encode()).hexdigest(), 16) % 10000 / 10000
share = np.mean([bucket(f"user{i}") < 0.05 for i in range(100000)])
print(f"hash split check: {share:.4f} of 100000 users land in a 5% canary; sticky: {bucket('user7') == bucket('user7')}")
def run(frac, p_base, p_cand, rpm=200, look_every=15, max_min=240, zcut=-2.33, min_cand=150):
    """each minute: rpm requests; frac go to candidate. Look every `look_every` minutes; roll back if one-sided z < zcut."""
    nb = sb = nc = sc = 0
    for minute in range(1, max_min + 1):
        k = rng.binomial(rpm, frac); nc += k; sc += rng.binomial(k, p_cand)
        nb += rpm - k; sb += rng.binomial(rpm - k, p_base)
        if minute % look_every == 0 and nc >= min_cand:
            pp = (sb + sc) / (nb + nc); se = math.sqrt(pp * (1 - pp) * (1 / nb + 1 / nc))
            if (sc / nc - sb / nb) / se < zcut: return minute, nc
    return None, nc
print("canary share | candidate truly worse (0.84 vs 0.90): rolled back / median minutes | candidate equal (0.90): false rollbacks   [300 sims each]")
for frac in (0.02, 0.05, 0.20):
    bad = [run(frac, .90, .84) for _ in range(300)]; good = [run(frac, .90, .90) for _ in range(300)]
    rb = [m for m, _ in bad if m]
    print(f"   {frac:4.0%}      |  {len(rb):3d}/300  median {np.median(rb) if rb else float('nan'):5.0f} min                 |  {sum(m is not None for m, _ in good):3d}/300")
