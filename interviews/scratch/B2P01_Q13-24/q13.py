import math, torch
import torch.nn.functional as F

class CausalMHA(torch.nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.h, self.dh = n_heads, d_model // n_heads
        self.qkv = torch.nn.Linear(d_model, 3 * d_model, bias=False)
        self.out = torch.nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):                       # x: (B, T, D)
        B, T, D = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)  # each (B, T, D)
        # (B, T, D) -> (B, H, T, dh)
        q, k, v = (t.view(B, T, self.h, self.dh).transpose(1, 2) for t in (q, k, v))
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.dh)      # (B, H, T, T)
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), 1)
        scores = scores.masked_fill(mask, float("-inf"))           # block the future
        w = scores.softmax(dim=-1)                                 # over keys
        o = w @ v                                                  # (B, H, T, dh)
        o = o.transpose(1, 2).contiguous().view(B, T, D)           # merge heads
        return self.out(o)

torch.manual_seed(0)
B, T, D, H = 2, 6, 32, 4
m = CausalMHA(D, H); x = torch.randn(B, T, D)
y = m(x)
# reference with SDPA using the same weights
q, k, v = m.qkv(x).chunk(3, -1)
q, k, v = (t.view(B, T, H, D // H).transpose(1, 2) for t in (q, k, v))
ref = m.out(F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, D))
print("shape", tuple(y.shape), "max abs diff vs SDPA:", (y - ref).abs().max().item())
# causality check: change last token, earlier outputs must not move
x2 = x.clone(); x2[:, -1] += 10
print("earlier positions unchanged:", torch.allclose(m(x2)[:, :-1], y[:, :-1]))
print("last position changed:", not torch.allclose(m(x2)[:, -1], y[:, -1]))
