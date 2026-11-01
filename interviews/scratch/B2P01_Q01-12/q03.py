import torch, torch.nn as nn
torch.manual_seed(0)
B, T, D, H = 2, 10, 64, 8
dh = D // H
x = torch.randn(B, T, D)
qkv = nn.Linear(D, 3*D, bias=False); o = nn.Linear(D, D, bias=False)
q, k, v = qkv(x).chunk(3, -1)
split = lambda t: t.view(B, T, H, dh).transpose(1, 2)   # (B,H,T,dh)
q, k, v = map(split, (q, k, v))
att = (q @ k.transpose(-2, -1)) / dh**0.5               # (B,H,T,T)
att = att.softmax(-1)
y = (att @ v).transpose(1, 2).reshape(B, T, D)          # concat heads
y = o(y)
print(q.shape, att.shape, y.shape)
print("params:", sum(p.numel() for p in [*qkv.parameters(), *o.parameters()]), "4*D*D =", 4*D*D)
