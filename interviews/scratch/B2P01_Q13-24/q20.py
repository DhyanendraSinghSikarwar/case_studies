import torch
torch.manual_seed(0)
x = torch.randn(2, 5, 4096) * 3 + 1.5
ln = torch.nn.LayerNorm(4096, eps=1e-6)
def rmsnorm(x, w, eps=1e-6):
    return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * w
y_ln, y_rms = ln(x), rmsnorm(x, torch.ones(4096))
print("LN out mean/std:", y_ln.mean().item().__round__(4), y_ln.std().item().__round__(3))
print("RMS out mean (not 0):", y_rms.mean().item().__round__(3), "rms:", y_rms.pow(2).mean().sqrt().item().__round__(3))
xc = x - x.mean(-1, keepdim=True)   # if input already zero-mean, RMSNorm == LayerNorm (no affine)
print("equal on zero-mean input:", torch.allclose(ln(xc), rmsnorm(xc, torch.ones(4096)), atol=1e-4))
print("params LN:", sum(p.numel() for p in ln.parameters()), " RMSNorm:", 4096)
import time
a = torch.randn(64, 2048, 1024); w = torch.ones(1024); l2 = torch.nn.LayerNorm(1024)
for name, f in [("LayerNorm", lambda: l2(a)), ("RMSNorm (naive py)", lambda: rmsnorm(a, w))]:
    f(); t = time.perf_counter(); [f() for _ in range(3)]; print(name, round((time.perf_counter()-t)/3*1000, 1), "ms")
