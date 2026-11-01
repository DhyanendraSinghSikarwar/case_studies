import torch
torch.manual_seed(0)

def rope(x, pos, base=10000.0):
    """x: (..., T, d) with d even; pos: (T,) integer positions. Rotates each (x[2i], x[2i+1]) pair by pos*theta_i."""
    d = x.shape[-1]
    theta = base ** (-torch.arange(0, d, 2, dtype=x.dtype) / d)       # (d/2,)
    ang = pos[:, None].to(x.dtype) * theta[None, :]                   # (T, d/2)
    cos, sin = ang.cos(), ang.sin()
    x1, x2 = x[..., 0::2], x[..., 1::2]
    out = torch.empty_like(x)
    out[..., 0::2] = x1 * cos - x2 * sin
    out[..., 1::2] = x1 * sin + x2 * cos
    return out

d = 64
q = torch.randn(d, dtype=torch.float64); k = torch.randn(d, dtype=torch.float64)
def score(m, n):   # q at position m, k at position n (same content vectors every time)
    qm = rope(q[None], torch.tensor([m]))[0]; kn = rope(k[None], torch.tensor([n]))[0]
    return (qm @ kn).item()

print("no-position score q.k            :", round((q @ k).item(), 6))
for off in (0, 3, 17):
    vals = [score(m + off, m) for m in (0, 5, 100, 1000, 5000)]
    print(f"offset m-n={off:2d}, m=0,5,100,1000,5000 ->", [round(v, 6) for v in vals])
print("max spread across absolute positions for offset 3:", max(score(m+3, m) for m in range(0, 2000, 37)) - min(score(m+3, m) for m in range(0, 2000, 37)))
print("different offsets give different scores:", [round(score(10+o, 10), 4) for o in (0, 1, 2, 5, 50)])

# full attention-score matrix: S[m,n] should be a function of m-n only IF q and k rows are the same vector at every position
T = 8
Q = q.expand(T, d).clone(); K = k.expand(T, d).clone()
S = rope(Q, torch.arange(T)) @ rope(K, torch.arange(T)).T
print("S[m,n] constant along diagonals:", all(torch.allclose(S.diagonal(o), S.diagonal(o)[0].expand_as(S.diagonal(o))) for o in range(-T+1, T)))
# norm preservation and identity at position 0
print("norm preserved:", torch.allclose(rope(q[None], torch.tensor([777]))[0].norm(), q.norm()))
