import torch, torch.nn as nn
torch.manual_seed(0)
class Block(nn.Module):
    def __init__(s, D=64, H=4, pre=True):
        super().__init__(); s.pre = pre
        s.ln1, s.ln2 = nn.LayerNorm(D), nn.LayerNorm(D)
        s.attn = nn.MultiheadAttention(D, H, batch_first=True)
        s.ffn = nn.Sequential(nn.Linear(D, 4*D), nn.GELU(), nn.Linear(4*D, D))
    def forward(s, x):
        T = x.shape[1]; m = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)
        if s.pre:       # GPT-2 / Llama style: norm inside the residual branch
            h = s.ln1(x); x = x + s.attn(h, h, h, attn_mask=m, need_weights=False)[0]
            return x + s.ffn(s.ln2(x))
        x = s.ln1(x + s.attn(x, x, x, attn_mask=m, need_weights=False)[0])   # original 2017 style
        return s.ln2(x + s.ffn(x))
b = Block(); x = torch.randn(2, 10, 64)
print(b(x).shape, "params:", sum(p.numel() for p in b.parameters()), "~12*D^2 =", 12*64*64)
