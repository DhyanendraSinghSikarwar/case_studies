# Q41: why a bare 90% accuracy number means nothing before baseline and label quality
import numpy as np
print("majority-class baseline accuracy by positive rate:")
for p in (0.01, 0.05, 0.10, 0.50, 0.90):
    base = max(p, 1 - p)
    print(f"  positive rate {p:>4.0%} -> baseline {base:.0%}")
assert max(0.10, 0.90) == 0.90          # at 10% prevalence the 'no' model already scores 90%
assert max(0.90, 0.10) == 0.90
# label noise ceiling: a perfect model scored against labels that are 8% wrong
rng = np.random.default_rng(41)
n = 100_000
truth = rng.random(n) < 0.3
flip = rng.random(n) < 0.08
labels = truth ^ flip
perfect_pred = truth
acc = (perfect_pred == labels).mean()
print(f"perfect model vs labels with 8% noise: measured accuracy = {acc:.3f}")
assert abs(acc - 0.92) < 0.005
