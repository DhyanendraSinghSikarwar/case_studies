# Q41: 14 of 60 pickled models fail to load after an image refresh (invented numbers)
import importlib, os, pickle, sys, tempfile
import numpy as np

total, bad, no_env = 60, 14, 5
print("failing share of fleet:", round(bad / total, 3), "| still loading:", total - bad,
      "| failing but env known:", bad - no_env)
assert round(bad / total, 3) == 0.233 and total - bad == 46 and bad - no_env == 9

d = tempfile.mkdtemp()
sys.path.insert(0, d)

# 'Old library' that the model was pickled under.
open(os.path.join(d, "toylib.py"), "w").write(
    "import numpy as np\n"
    "class LinearScorer:\n"
    "    def __init__(self, w, b): self.w = np.asarray(w); self.b = b\n"
    "    def predict(self, X): return X @ self.w + self.b\n")
import toylib
model = toylib.LinearScorer([0.5, -1.0, 2.0], 0.1)
blob = pickle.dumps(model)
X = np.random.default_rng(1).normal(size=(5, 3))
golden = model.predict(X)                       # golden inputs and outputs recorded at release time

# The 'refreshed image': the class was renamed in the new library version.
open(os.path.join(d, "toylib.py"), "w").write(
    "import numpy as np\n"
    "class Estimator:\n"
    "    def __init__(self, coef, intercept): self.coef = np.asarray(coef); self.intercept = intercept\n"
    "    def predict(self, X): return X @ self.coef + self.intercept\n")
del sys.modules["toylib"]; importlib.invalidate_caches()
try:
    pickle.loads(blob)
    failed = False
except Exception as e:
    failed = True; print("load under new library fails with:", type(e).__name__)
assert failed

# Recovery 1: roll the base image back (previous digest) -> same code path as release time.
open(os.path.join(d, "toylib.py"), "w").write(
    "import numpy as np\n"
    "class LinearScorer:\n"
    "    def __init__(self, w, b): self.w = np.asarray(w); self.b = b\n"
    "    def predict(self, X): return X @ self.w + self.b\n")
del sys.modules["toylib"]; importlib.invalidate_caches()
loaded = pickle.loads(blob)                      # trusted artifact only: pickle can run code
assert np.array_equal(loaded.predict(X), golden)
print("old image loads it; predictions equal golden:", True)

# Recovery 2 (inside the old image): export to a plain format with no library classes.
npz = os.path.join(d, "model.npz")
np.savez(npz, w=loaded.w, b=np.array(loaded.b), schema_version=np.array(1))
z = np.load(npz)                                 # allow_pickle is False by default
new_pred = X @ z["w"] + float(z["b"])
parity = float(np.abs(new_pred - golden).max())
print("exported weights parity (max abs diff):", parity)
assert parity < 1e-12

# Pickle can execute code on load: show it harmlessly.
ran = []
def side_effect(msg): ran.append(msg)
class Evil:
    def __reduce__(self): return (side_effect, ("code ran during load",))
pickle.loads(pickle.dumps(Evil()))
print("pickle.loads executed code:", ran == ["code ran during load"])
assert ran == ["code ran during load"]
