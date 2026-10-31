import torch
torch.manual_seed(0)
B, T, H, dh = 2, 6, 8, 16
def gqa(q, k, v, Hkv):          # q:(B,H,T,dh) k,v:(B,Hkv,T,dh)
    g = q.shape[1] // Hkv
    k = k.repeat_interleave(g, 1); v = v.repeat_interleave(g, 1)   # (B,H,T,dh)
    s = q @ k.transpose(-2, -1) / dh**0.5
    s = s.masked_fill(torch.triu(torch.ones(T, T, dtype=torch.bool), 1), float('-inf'))
    return s.softmax(-1) @ v
q = torch.randn(B, H, T, dh)
for Hkv in (8, 2, 1):
    k = torch.randn(B, Hkv, T, dh); v = torch.randn(B, Hkv, T, dh)
    print("kv_heads", Hkv, "out", tuple(gqa(q, k, v, Hkv).shape), "cache floats/token/layer", 2*Hkv*dh)
# check: Hkv==H equals plain MHA via torch SDPA
k = torch.randn(B, H, T, dh); v = torch.randn(B, H, T, dh)
ref = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=True)
print("matches SDPA:", torch.allclose(gqa(q, k, v, H), ref, atol=1e-5))
