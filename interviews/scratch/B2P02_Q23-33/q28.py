import torch
torch.manual_seed(0)
X, y = torch.randn(32, 8), torch.randn(32)
w = torch.randn(8, requires_grad=True)
loss = ((X @ w - y) ** 2).mean(); loss.backward(); g_big = w.grad.clone(); w.grad = None
for xb, yb in zip(X.chunk(4), y.chunk(4)):           # 4 micro-batches of 8
    (((xb @ w - yb) ** 2).mean() / 4).backward()      # divide by accumulation steps
print("accumulated == big batch:", torch.allclose(w.grad, g_big, atol=1e-6))
w.grad = None
for xb, yb in zip(X.chunk(4), y.chunk(4)):           # forgot the /4
    ((xb @ w - yb) ** 2).mean().backward()
print("without /4, grad is", round((w.grad.norm()/g_big.norm()).item(), 3), "x too large")
B, S = 1024, 4096
print("tokens/step:", B * S, "=", B*S/2**20, "M (2^20)")
