import torch, math, torch.nn.functional as F
torch.manual_seed(0)
B, T, D, H = 2, 6, 16, 4
dh = D // H
x = torch.randn(B, T, D)
Wq, Wk, Wv, Wo = [torch.randn(D, D) / math.sqrt(D) for _ in range(4)]

def buggy_mha(x):
    B, T, D = x.shape
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    q = q.view(B, H, T, dh); k = k.view(B, H, T, dh); v = v.view(B, H, T, dh)   # BUG 4
    scores = q @ k.transpose(-2, -1)                                            # BUG 3 (no scale), BUG 2 (no mask)
    w = torch.softmax(scores, dim=-2)                                           # BUG 1
    return (w @ v).transpose(1, 2).reshape(B, T, D) @ Wo

def mha(x, softmax_dim=-1, mask=True, scale=True, split="correct"):
    B, T, D = x.shape
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    if split == "correct": q, k, v = [t.view(B, T, H, dh).transpose(1, 2) for t in (q, k, v)]
    else:                  q, k, v = [t.view(B, H, T, dh) for t in (q, k, v)]
    s = q @ k.transpose(-2, -1)
    if scale: s = s / math.sqrt(dh)
    if mask: s = s.masked_fill(torch.triu(torch.ones(T, T, dtype=torch.bool), 1), float("-inf"))
    out = torch.softmax(s, dim=softmax_dim) @ v
    return out.transpose(1, 2).reshape(B, T, D) @ Wo

def ref(x):
    q, k, v = [(x @ W).view(B, T, H, dh).transpose(1, 2) for W in (Wq, Wk, Wv)]
    return F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, D) @ Wo

r = ref(x)
d = lambda y: f"{(y - r).abs().max().item():.2e}"
print("whole buggy snippet      :", d(buggy_mha(x)))
print("fixed (all four fixed)   :", d(mha(x)))
print("only softmax dim wrong   :", d(mha(x, softmax_dim=-2)))   # note: -2 with a mask gives NaN risk? check
print("only mask missing        :", d(mha(x, mask=False)))
print("only scaling missing     :", d(mha(x, scale=False)))
print("only reshape wrong       :", d(mha(x, split="bad")))
# reshape bug: what does head 0 'token 0' really contain?
flat = (x @ Wq)                       # (B,T,D)
bad = flat.view(B, H, T, dh)
print("bad head0 'token1' == flat[0,0,4:8]  (dims 4-7 of token 0):", torch.equal(bad[0,0,1], flat[0,0,4:8]))
print("bad head0 'token4' == flat[0,1,0:4]  (token 1 dims 0-3)   :", torch.equal(bad[0,0,4], flat[0,1,0:4]))
