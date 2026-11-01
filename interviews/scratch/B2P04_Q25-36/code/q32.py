# TOY multi-adapter serving: ONE frozen base layer, two LoRA adapters, adapter chosen per request.
# Not a real serving stack: it shows the idea (shared base matmul + small per-request low-rank delta).
import torch
torch.manual_seed(0)
d, r, alpha = 16, 4, 8
W = torch.randn(d, d) / d**0.5                       # frozen base weight, shared by everyone
def make_adapter():
    return {"A": torch.randn(r, d) * 0.5, "B": torch.randn(d, r) * 0.5}   # random stand-ins for trained adapters
adapters = {"support-v1": make_adapter(), "legal-v1": make_adapter()}

def forward(x, names):
    """x: (batch, d); names[i] = adapter for request i. Base matmul is batched across ALL requests."""
    base = x @ W.T
    out = base.clone()
    for i, n in enumerate(names):
        if n is None: continue                       # None = plain base model
        a = adapters[n]
        out[i] += (alpha / r) * (x[i] @ a["A"].T) @ a["B"].T     # per-request low-rank delta
    return out

x = torch.randn(1, d)
batch = x.repeat(4, 1)                               # same input, 4 requests with different adapters
y = forward(batch, ["support-v1", "legal-v1", None, "support-v1"])
print("same input, different adapter -> different output?")
print(" support vs legal :", not torch.allclose(y[0], y[1]))
print(" support vs base  :", not torch.allclose(y[0], y[2]))
print(" same adapter twice gives identical output:", torch.allclose(y[0], y[3]))
# merged-weights equivalence for one adapter
a = adapters["support-v1"]
W_merged = W + (alpha / r) * a["B"] @ a["A"]
print(" merged W matches adapter path:", torch.allclose(x @ W_merged.T, y[0:1], atol=1e-5))
# versioning/rollback toy: adapter registry
adapters["support-v2"] = make_adapter()
active = {"support": "support-v2"}
active["support"] = "support-v1"                     # rollback is a pointer change, no base reload
print(" active support adapter after rollback:", active["support"])
