import torch, torch.nn as nn, torch.nn.functional as F
class RMSNorm(nn.Module):
    def __init__(s, d, eps=1e-6): super().__init__(); s.g = nn.Parameter(torch.ones(d)); s.eps = eps
    def forward(s, x): return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + s.eps) * s.g
class SwiGLU(nn.Module):
    def __init__(s, d, h): super().__init__(); s.w1 = nn.Linear(d, h, bias=False); s.w3 = nn.Linear(d, h, bias=False); s.w2 = nn.Linear(h, d, bias=False)
    def forward(s, x): return s.w2(F.silu(s.w1(x)) * s.w3(x))
x = torch.randn(2, 5, 4096)
print(RMSNorm(4096)(x).pow(2).mean(-1)[0,:2])
m = SwiGLU(4096, 11008); print(m(x).shape, sum(p.numel() for p in m.parameters())/1e6)
print(2*4096*16384/1e6, 8/3*4096)
