# ANALOGY, not an LLM: an over-sized MLP memorises 40 noisy points (y = sin(x) + noise).
# Train loss goes towards 0 while validation loss rises. Compare: no regularisation, weight decay, early stopping.
import torch, torch.nn as nn
torch.set_num_threads(1)   # tiny model: threads only add overhead
torch.manual_seed(0)
def make(n):
    x = torch.rand(n, 1) * 6 - 3
    return x, torch.sin(x) + 0.3 * torch.randn(n, 1)
xtr, ytr = make(40); xva, yva = make(400)

def run(wd, epochs=2000, patience=None):
    torch.manual_seed(1)
    m = nn.Sequential(nn.Linear(1, 128), nn.Tanh(), nn.Linear(128, 128), nn.Tanh(), nn.Linear(128, 1))
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3, weight_decay=wd)
    best, best_ep, hist, last_t, last_v = 1e9, 0, {}, 0, 0
    for ep in range(1, epochs + 1):
        opt.zero_grad(); l = nn.functional.mse_loss(m(xtr), ytr); l.backward(); opt.step()
        with torch.no_grad():
            v = nn.functional.mse_loss(m(xva), yva).item()
        if ep in (50, 200, 500, 2000): hist[ep] = (l.item(), v)
        if v < best: best, best_ep = v, ep
        if patience and ep - best_ep >= patience:       # early stopping: stop when val has not improved for `patience` epochs
            hist["stopped"] = ep; break
    return hist, best, best_ep

h, best, bep = run(0.0)
print("no regularisation (epoch: train, val):")
for ep, (t, v) in h.items(): print(f"  {ep:5d}: train {t:.4f}  val {v:.4f}")
print(f"  best val {best:.4f} at epoch {bep}")
h3, b3, e3 = run(0.0, patience=100)
print(f"early stopping (patience 100): stopped at epoch {h3['stopped']}, best val {b3:.4f} at epoch {e3}")
h2, best2, bep2 = run(1.0)
print("AdamW weight_decay=1.0 (epoch: train, val):")
for ep, (t, v) in h2.items(): print(f"  {ep:5d}: train {t:.4f}  val {v:.4f}")
print(f"  best val {best2:.4f} at epoch {bep2}")
print("noise floor of the data (0.3^2) = 0.09")
