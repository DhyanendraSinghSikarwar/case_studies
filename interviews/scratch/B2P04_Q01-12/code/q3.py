import math, torch
torch.manual_seed(0)
class LoRALinear(torch.nn.Module):
    def __init__(self, d_in, d_out, r=8, alpha=16):
        super().__init__()
        self.W = torch.nn.Parameter(torch.randn(d_out, d_in) / d_in**0.5, requires_grad=False)  # frozen
        self.A = torch.nn.Parameter(torch.empty(r, d_in))
        torch.nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))   # A: Kaiming-uniform
        self.B = torch.nn.Parameter(torch.zeros(d_out, r))       # B: zeros
        self.scale = alpha / r
    def forward(self, x):
        return x @ self.W.T + self.scale * (x @ self.A.T) @ self.B.T
m = LoRALinear(64, 64, r=8, alpha=16)
x = torch.randn(4, 64)
print("same as base at init:", torch.allclose(m(x), x @ m.W.T))
opt = torch.optim.SGD([p for p in m.parameters() if p.requires_grad], lr=0.1)
target = torch.randn(4, 64)
for _ in range(50):
    loss = ((m(x) - target) ** 2).mean(); opt.zero_grad(); loss.backward(); opt.step()
print("loss after 50 steps:", round(loss.item(), 4), "| W unchanged grad:", m.W.grad is None)
trainable = sum(p.numel() for p in m.parameters() if p.requires_grad)
print("trainable", trainable, "of", trainable + m.W.numel())
with torch.no_grad():
    Wm = m.W + m.scale * m.B @ m.A      # merge
print("merged matches:", torch.allclose(m(x), x @ Wm.T, atol=1e-5))
