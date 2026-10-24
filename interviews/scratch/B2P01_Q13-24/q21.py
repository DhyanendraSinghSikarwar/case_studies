import torch, torch.nn as nn, torch.nn.functional as F
d = 4096
gelu_ffn = 2 * d * (4*d)                    # up + down, hidden 4d
swi_hidden = 11008
swiglu = 3 * d * swi_hidden                 # gate, up, down
print("GELU FFN (4d) params:", f"{gelu_ffn:,}", " SwiGLU (11008) params:", f"{swiglu:,}")
print("8/3 * d =", round(8/3*d), "-> Llama rounds to 11008 (multiple of 256)")
attn = 4 * d * d
print("per layer attn:", f"{attn:,}", "ffn share:", round(swiglu/(attn+swiglu), 3))
class SwiGLU(nn.Module):
    def __init__(s, d, h):
        super().__init__(); s.gate = nn.Linear(d, h, bias=False); s.up = nn.Linear(d, h, bias=False); s.down = nn.Linear(h, d, bias=False)
    def forward(s, x): return s.down(F.silu(s.gate(x)) * s.up(x))
m = SwiGLU(64, 172); print(m(torch.randn(2, 5, 64)).shape, sum(p.numel() for p in m.parameters()))
