import torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)
V, D, H, L, T, B = 100, 32, 4, 2, 7, 1
dh = D // H
def rms(x, w, eps=1e-6): return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * w
def rope(x, base=10000.0):                     # x: (B,H,T,dh)
    T, dh = x.shape[-2], x.shape[-1]
    inv = base ** (-torch.arange(0, dh, 2).float() / dh)
    ang = torch.arange(T).float()[:, None] * inv[None]       # (T, dh/2)
    c, s = ang.cos(), ang.sin()
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.stack([x1*c - x2*s, x1*s + x2*c], -1).flatten(-2)
emb = nn.Embedding(V, D)
layers = [dict(wqkv=nn.Linear(D, 3*D, bias=False), wo=nn.Linear(D, D, bias=False),
               g=nn.Linear(D, 4*D, bias=False), u=nn.Linear(D, 4*D, bias=False), d=nn.Linear(4*D, D, bias=False),
               n1=torch.ones(D), n2=torch.ones(D)) for _ in range(L)]
nf = torch.ones(D); head = nn.Linear(D, V, bias=False)
ids = torch.randint(0, V, (B, T)); print("token ids      ", tuple(ids.shape))
x = emb(ids); print("embeddings     ", tuple(x.shape))
for l in layers:
    h = rms(x, l["n1"])
    q, k, v = l["wqkv"](h).chunk(3, -1)
    q, k, v = (t.view(B, T, H, dh).transpose(1, 2) for t in (q, k, v))
    q, k = rope(q), rope(k)
    a = F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, D)
    x = x + l["wo"](a)
    h = rms(x, l["n2"])
    x = x + l["d"](F.silu(l["g"](h)) * l["u"](h))
print("after blocks   ", tuple(x.shape))
logits = head(rms(x, nf)); print("logits         ", tuple(logits.shape))
p = logits[:, -1].softmax(-1); print("next-token probs", tuple(p.shape), "sum =", round(p.sum().item(), 4))
