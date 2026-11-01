import torch
x = torch.tensor([-200., -50., -5., 0., 5., 50., 200.])
cap = 30.0
print("soft-cap(30):", (cap * torch.tanh(x / cap)).round(decimals=2).tolist())
# z-loss: penalise log-sum-exp of the logits so the softmax normaliser stays near 1
logits = torch.randn(4, 100) * 3
lse = torch.logsumexp(logits, -1)
print("logsumexp:", lse.round(decimals=2).tolist(), " z-loss (1e-4 coef):", (1e-4 * lse.pow(2).mean()).item())
# QK-norm: normalise q and k per head -> q.k bounded by learnable scale regardless of weight growth
q, k = torch.randn(64) * 50, torch.randn(64) * 50          # exploded activations
rms = lambda t: t / t.pow(2).mean().sqrt()
print("raw q.k/sqrt(d):", round((q @ k / 8).item(), 1), "| after RMS-normalising q and k:", round((rms(q) @ rms(k) / 8).item(), 2))
