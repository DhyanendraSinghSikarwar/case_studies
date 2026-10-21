import torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)

class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.h, s.dh = h, d // h
        s.qkv = nn.Linear(d, 3 * d, bias=False)
        s.o = nn.Linear(d, d, bias=False)
        s.n1, s.n2 = nn.LayerNorm(d), nn.LayerNorm(d)
        s.ff = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(s, x, cache=None):
        B, T, D = x.shape
        q, k, v = s.qkv(s.n1(x)).view(B, T, 3, s.h, s.dh).permute(2, 0, 3, 1, 4)
        if cache is not None:                      # append new K,V to cached K,V
            if "k" in cache:
                k = torch.cat([cache["k"], k], dim=2)
                v = torch.cat([cache["v"], v], dim=2)
            cache["k"], cache["v"] = k, v
        S = k.shape[2]                             # total length so far
        # query i sits at absolute position S-T+i; it may see keys j <= S-T+i
        mask = torch.ones(T, S, dtype=torch.bool).tril(diagonal=S - T)
        a = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
        x = x + s.o(a.transpose(1, 2).reshape(B, T, D))
        return x + s.ff(s.n2(x))

class TinyLM(nn.Module):
    def __init__(s, V=50, d=32, h=4, L=2, maxlen=64):
        super().__init__()
        s.emb, s.pos = nn.Embedding(V, d), nn.Embedding(maxlen, d)
        s.blocks = nn.ModuleList(Block(d, h) for _ in range(L))
        s.nf, s.head = nn.LayerNorm(d), nn.Linear(d, V, bias=False)
    def forward(s, ids, caches=None, start=0):
        T = ids.shape[1]
        x = s.emb(ids) + s.pos(torch.arange(start, start + T))
        for i, b in enumerate(s.blocks):
            x = b(x, None if caches is None else caches[i])
        return s.head(s.nf(x))

@torch.no_grad()
def generate_nocache(m, ids, n):
    for _ in range(n):
        nxt = m(ids)[:, -1].argmax(-1, keepdim=True)   # recompute everything each step
        ids = torch.cat([ids, nxt], 1)
    return ids

@torch.no_grad()
def generate_cache(m, ids, n):
    caches = [dict() for _ in m.blocks]
    logits = m(ids, caches, start=0)                   # prefill: whole prompt at once
    out = ids
    for _ in range(n):
        nxt = logits[:, -1].argmax(-1, keepdim=True)
        out = torch.cat([out, nxt], 1)
        logits = m(nxt, caches, start=out.shape[1] - 1)  # decode: 1 token, reuse cache
    return out

m = TinyLM().eval()
prompt = torch.randint(0, 50, (2, 7))
a, b = generate_nocache(m, prompt, 20), generate_cache(m, prompt, 20)
print("tokens equal:", torch.equal(a, b))

# compare logits (not just argmax tokens) at the last step
with torch.no_grad():
    full = m(a[:, :-1])[:, -1]
    caches = [dict() for _ in m.blocks]
    m(a[:, :7], caches, 0)
    for t in range(7, a.shape[1] - 1):
        step = m(a[:, t:t+1], caches, start=t)[:, -1]
print("max abs logit diff:", (full - step).abs().max().item())
print("cache K shape per layer:", tuple(caches[0]["k"].shape))
