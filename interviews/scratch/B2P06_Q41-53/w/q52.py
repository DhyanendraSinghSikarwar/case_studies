# Standalone, torch (CPU, single thread). SYNTHETIC: a hidden "domain" mapping makes queries and relevant passages differ in a way the
# generic (identity) embedder does not know. A linear embedding is trained with InfoNCE. Not a real text model.
import torch, torch.nn.functional as F
torch.set_num_threads(1); torch.manual_seed(0)
D, NTR, NTE, NDIST = 32, 2000, 500, 3000
A = torch.eye(D) + 0.9 * torch.randn(D, D) / D ** 0.5            # hidden mapping: relevant passage ~ A q (domain-specific relation)
def make(n):
    q = torch.randn(n, D); p = q @ A.T + 0.3 * torch.randn(n, D); return q, p
qtr, ptr = make(NTR); qte, pte = make(NTE)
pool = torch.cat([pte, torch.randn(NDIST, D) @ A.T])             # held-out corpus: 500 positives + 3000 distractor passages
class Emb(torch.nn.Module):
    def __init__(s): super().__init__(); s.Wq = torch.nn.Linear(D, D, bias=False); s.Wp = torch.nn.Linear(D, D, bias=False); torch.nn.init.eye_(s.Wq.weight); torch.nn.init.eye_(s.Wp.weight)
    def q(s, x): return F.normalize(s.Wq(x), dim=-1)
    def p(s, x): return F.normalize(s.Wp(x), dim=-1)
def recall(m, k_list=(1, 10)):
    with torch.no_grad(): S = m.q(qte) @ m.p(pool).T                # query i's positive is pool[i]
    rank = (S > S.diag().unsqueeze(1) if False else (S > S[torch.arange(NTE), torch.arange(NTE)].unsqueeze(1))).sum(1)
    return {k: (rank < k).float().mean().item() for k in k_list}
def train(hard=False, epochs=30, bs=128, tau=0.05):
    m = Emb(); opt = torch.optim.Adam(m.parameters(), lr=3e-3)
    for _ in range(epochs):
        perm = torch.randperm(NTR)
        for i in range(0, NTR, bs):
            b = perm[i:i + bs]; q, p = m.q(qtr[b]), m.p(ptr[b]); S = q @ p.T / tau          # in-batch negatives: other rows' passages
            if hard:                                                                      # one mined hard negative per query: top-scoring wrong passage in the TRAIN set
                with torch.no_grad(): sc = m.q(qtr[b]) @ m.p(ptr).T; sc[torch.arange(len(b)), b] = -9; hn = sc.argmax(1)
                S = torch.cat([S, (q * m.p(ptr[hn])).sum(1, keepdim=True) / tau], 1)
            loss = F.cross_entropy(S, torch.arange(len(b))); opt.zero_grad(); loss.backward(); opt.step()   # InfoNCE
    return m
m0 = Emb(); print("before training (generic identity embedder):", {k: round(v, 3) for k, v in recall(m0).items()})
m1 = train(False); print("after InfoNCE, in-batch negatives:         ", {k: round(v, 3) for k, v in recall(m1).items()})
m2 = train(True);  print("after InfoNCE, + 1 mined hard negative:    ", {k: round(v, 3) for k, v in recall(m2).items()})
print("held-out: 500 queries vs a pool of 3500 passages; training used 2000 other pairs. SYNTHETIC; single run, single seed.")
