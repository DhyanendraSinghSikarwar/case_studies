import torch
torch.manual_seed(0)
PAD = 0
seqs = [[5, 6, 7, 8], [9, 10]]
def batch(seqs, side):
    L = max(map(len, seqs)); ids, mask = [], []
    for s in seqs:
        p = [PAD]*(L-len(s))
        ids.append(p+s if side=="left" else s+p)
        mask.append([0]*len(p)+[1]*len(s) if side=="left" else [1]*len(s)+[0]*len(p))
    return torch.tensor(ids), torch.tensor(mask)
for side in ("right", "left"):
    ids, mask = batch(seqs, side)
    print(side, ids.tolist(), mask.tolist())
    # last-position index used to read next-token logits: for decode we take position -1
    print("  token at position -1:", ids[:, -1].tolist(), "(PAD means the model continues from padding)" if (ids[:, -1]==PAD).any() else "(real last tokens)")
# position ids from mask, and attention bias = causal AND key-is-real
ids, mask = batch(seqs, "left")
pos = (mask.cumsum(-1) - 1).clamp(min=0)
print("position_ids", pos.tolist())
T = ids.shape[1]
allowed = torch.tril(torch.ones(T, T, dtype=torch.bool))[None] & mask.bool()[:, None, :]
print("row 1 (short seq) attention, query pos 3 sees keys:", allowed[1, 3].int().tolist())
# check: padded short sequence gives the same last-token output as unpadded one
d = 8; emb = torch.nn.Embedding(20, d); Wq, Wk, Wv = (torch.randn(d, d) for _ in range(3))
def attn_last(ids, allowed, pos):
    x = emb(ids)
    q, k, v = x@Wq, x@Wk, x@Wv
    s = (q@k.transpose(-1, -2))/d**0.5
    s = s.masked_fill(~allowed, float("-inf"))
    return (s.softmax(-1)@v)[:, -1]
out_pad = attn_last(ids, allowed, pos)[1]
solo = torch.tensor([[9, 10]]); al = torch.tril(torch.ones(2, 2, dtype=torch.bool))[None]
out_solo = attn_last(solo, al, None)[0]
print("padded == unpadded:", torch.allclose(out_pad, out_solo, atol=1e-6))
