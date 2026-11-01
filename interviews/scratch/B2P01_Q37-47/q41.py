import torch, math, torch.nn.functional as F
torch.manual_seed(0)
B, T, D, H = 2, 6, 16, 4
dh = D // H
x = torch.randn(B, T, D)
Wq, Wk, Wv, Wo = [torch.randn(D, D) / math.sqrt(D) for _ in range(4)]

def buggy_mha(x):
    B, T, D = x.shape
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    # BUG 4: view as (B, H, T, dh) directly mixes time and head dims
    q = q.view(B, H, T, dh); k = k.view(B, H, T, dh); v = v.view(B, H, T, dh)
    scores = q @ k.transpose(-2, -1)            # BUG 3: no / sqrt(dh)
                                                # BUG 2: no causal mask
    w = torch.softmax(scores, dim=-2)           # BUG 1: normalises over queries, not keys
    out = w @ v
    return out.transpose(1, 2).reshape(B, T, D) @ Wo

def fixed_mha(x, causal=True):
    B, T, D = x.shape
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    q, k, v = [t.view(B, T, H, dh).transpose(1, 2) for t in (q, k, v)]   # (B,H,T,dh)
    scores = q @ k.transpose(-2, -1) / math.sqrt(dh)
    if causal:
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)
        scores = scores.masked_fill(mask, float("-inf"))
    w = torch.softmax(scores, dim=-1)
    return (w @ v).transpose(1, 2).reshape(B, T, D) @ Wo

def ref(x):
    q, k, v = [(x @ W).view(B, T, H, dh).transpose(1, 2) for W in (Wq, Wk, Wv)]
    o = F.scaled_dot_product_attention(q, k, v, is_causal=True)
    return o.transpose(1, 2).reshape(B, T, D) @ Wo

r = ref(x)
print("buggy vs torch SDPA, max abs diff :", (buggy_mha(x) - r).abs().max().item())
print("fixed vs torch SDPA, max abs diff :", (fixed_mha(x) - r).abs().max().item())

# --- demonstrate each bug in isolation
q, k, v = [(x @ W).view(B, T, H, dh).transpose(1, 2) for W in (Wq, Wk, Wv)]
s = q @ k.transpose(-2, -1)
# bug 1: softmax dim
w_bad = torch.softmax(s / math.sqrt(dh), dim=-2)
print("bug1 row sums (should be 1):", w_bad.sum(-1)[0, 0, :3].tolist(), "| col sums:", w_bad.sum(-2)[0, 0, :3].tolist())
# bug 2: no mask -> future leaks. change last token only, see if earlier outputs move
x2 = x.clone(); x2[:, -1] += 5.0
def nomask(x): return fixed_mha(x, causal=False)
print("bug2 no mask: earlier outputs change when only last token changes:", (nomask(x2)[:, :-1] - nomask(x)[:, :-1]).abs().max().item())
print("      with mask:                                                   ", (fixed_mha(x2)[:, :-1] - fixed_mha(x)[:, :-1]).abs().max().item())
# bug 3: scaling. Use dh=64 random q,k to show softmax saturating
qq, kk = torch.randn(1000, 64), torch.randn(1000, 64)
for name, sc in (("unscaled", 1.0), ("scaled", 1 / 8)):
    p = torch.softmax(qq @ kk.T * sc, dim=-1)
    print(f"bug3 {name}: mean max-weight per row = {p.max(-1).values.mean():.3f}, score std = {(qq @ kk.T * sc).std():.2f}")
# bug 4: wrong reshape
good = q                                       # correct (B,H,T,dh)
bad = (x @ Wq).view(B, H, T, dh)
print("bug4 reshape: same shape?", good.shape == bad.shape, "| values equal?", torch.allclose(good, bad))
print("      bad head 0, token 0 comes from tokens:", "0 and 1 (dh=4 of 16 dims each... ) -> mixes", 
      "token 0 dims 0-3 then token 0 dims 4-7?" )
