import torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(1); torch.manual_seed(0)
# SYNTHETIC demo: one small MLP, two toy tasks. Input = 10 features + 2-dim task flag; labels from different random teachers.
d, k = 10, 4
tG, tT = torch.randn(d, k), torch.randn(d, k)
def data(t, flag, n):
    X = torch.randn(n, d); f = torch.zeros(n, 2); f[:, flag] = 1
    return torch.cat([X, f], 1), (X @ t).argmax(1)
G_tr, G_te = data(tG, 0, 3000), data(tG, 0, 2000)
T_tr, T_te = data(tT, 1, 3000), data(tT, 1, 2000)
def acc(m, ds): return (m(ds[0]).argmax(1) == ds[1]).float().mean().item()
def fit(m, X, y, steps, lr):
    opt = torch.optim.Adam(m.parameters(), lr=lr)
    for _ in range(steps):
        loss = F.cross_entropy(m(X), y); opt.zero_grad(); loss.backward(); opt.step()
def fresh():
    return nn.Sequential(nn.Linear(d + 2, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, k))
base = fresh(); fit(base, *G_tr, 1500, 3e-3)
def show(name, m): print(f"{name:34s} general acc {acc(m, G_te):.2f}   new-task acc {acc(m, T_te):.2f}")
show("base (trained on general only)", base)
import copy
m1 = copy.deepcopy(base); fit(m1, *T_tr, 1500, 3e-3); show("fine-tune on new task only", m1)
Xr = torch.cat([T_tr[0], G_tr[0][:600]]); yr = torch.cat([T_tr[1], G_tr[1][:600]])
m2 = copy.deepcopy(base); fit(m2, Xr, yr, 1500, 3e-3); show("new task + 600 general replay", m2)
m3 = copy.deepcopy(base); fit(m3, *T_tr, 100, 1e-4); show("new task only, tiny LR, few steps", m3)
