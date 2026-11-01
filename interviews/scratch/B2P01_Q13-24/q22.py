import math, torch
import torch.nn.functional as F
torch.manual_seed(0)
B, Tq, Tk, D, H = 2, 3, 10, 32, 4
dh = D // H
Wq, Wk, Wv = (torch.nn.Linear(D, D, bias=False) for _ in range(3))
dec = torch.randn(B, Tq, D)      # queries come from the decoder / text side
enc = torch.randn(B, Tk, D)      # keys, values come from encoder / image / audio side
sp = lambda t, T: t.view(B, T, H, dh).transpose(1, 2)
q, k, v = sp(Wq(dec), Tq), sp(Wk(enc), Tk), sp(Wv(enc), Tk)
w = (q @ k.transpose(-2, -1) / math.sqrt(dh)).softmax(-1)      # (B,H,Tq,Tk): no causal mask
out = (w @ v).transpose(1, 2).reshape(B, Tq, D)
print("attn weights", tuple(w.shape), "out", tuple(out.shape), "rows sum to 1:", torch.allclose(w.sum(-1), torch.ones(B, H, Tq)))
print("matches SDPA:", torch.allclose(out, F.scaled_dot_product_attention(q, k, v).transpose(1, 2).reshape(B, Tq, D), atol=1e-6))
