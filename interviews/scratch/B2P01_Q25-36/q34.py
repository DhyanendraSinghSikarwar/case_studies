import torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)
class MoE(nn.Module):
    def __init__(s, d=16, E=8, k=2, hid=32):
        super().__init__()
        s.k, s.E = k, E
        s.router = nn.Linear(d, E, bias=False)
        s.experts = nn.ModuleList(nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, d)) for _ in range(E))
    def forward(s, x):                                   # x: (tokens, d)
        probs = F.softmax(s.router(x), -1)               # (tokens, E)
        topv, topi = probs.topk(s.k, -1)
        topv = topv / topv.sum(-1, keepdim=True)         # renormalise the k gates
        out = torch.zeros_like(x)
        for e in range(s.E):
            tok, slot = (topi == e).nonzero(as_tuple=True)
            if len(tok):
                out[tok] += topv[tok, slot, None] * s.experts[e](x[tok])
        # Switch-style balance loss: E * sum_e (fraction routed to e) * (mean prob of e)
        frac = F.one_hot(topi, s.E).float().sum(1).mean(0) / s.k
        aux = s.E * (frac * probs.mean(0)).sum()
        return out, aux, frac
m = MoE(); x = torch.randn(1000, 16)
y, aux, frac = m(x)
print("out", tuple(y.shape), "aux loss %.3f (1.0 = perfectly balanced)" % aux.item())
print("token share per expert:", [round(v, 3) for v in frac.tolist()])
tot = sum(p.numel() for p in m.parameters()); one = sum(p.numel() for p in m.experts[0].parameters())
act = tot - 6*one
print("total params", tot, "active per token", act)
