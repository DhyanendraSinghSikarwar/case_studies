import numpy as np, yaml
p = yaml.safe_load(open("params.yaml"))["prepare"]
rng = np.random.default_rng(p["seed"])
X = rng.normal(size=(400, 3))
y = (X[:, 0] + 0.5 * X[:, 1] + rng.normal(scale=0.5, size=400) > 0).astype(int)
cut = int(400 * (1 - p["test_frac"]))
np.savez("prepared.npz", Xtr=X[:cut], ytr=y[:cut], Xte=X[cut:], yte=y[cut:])
print("prepared", cut, "train rows")
