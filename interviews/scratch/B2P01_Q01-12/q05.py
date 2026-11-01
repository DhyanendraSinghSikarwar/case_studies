import torch
torch.manual_seed(0)
T, d = 5, 4
q = torch.randn(T, d); k = torch.randn(T, d); v = torch.randn(T, d)
mask = torch.tril(torch.ones(T, T, dtype=torch.bool))
def attn(q, k, v):
    s = (q @ k.T) / d**0.5
    s = s.masked_fill(~mask, float('-inf'))
    return s.softmax(-1) @ v
out = attn(q, k, v)
k2, v2 = k.clone(), v.clone(); k2[4] += 10; v2[4] += 10   # change only the LAST token
out2 = attn(q, k2, v2)
print("rows 0-3 unchanged:", torch.allclose(out[:4], out2[:4]), "| row 4 changed:", not torch.allclose(out[4], out2[4]))
print(mask.int())
