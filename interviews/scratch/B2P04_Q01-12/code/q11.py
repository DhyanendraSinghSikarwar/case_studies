import torch, torch.nn.functional as F
torch.manual_seed(0)
V, PAD, IGN = 50, 0, -100
# batch of (prompt, response) token ids (made-up ids); response ends with EOS=2
ex = [([5, 6, 7, 8], [11, 12, 13, 2]), ([9, 10], [14, 2])]
L = max(len(p) + len(r) for p, r in ex)
ids = torch.full((len(ex), L), PAD); lab = torch.full((len(ex), L), IGN); lab_nomask = lab.clone()
for i, (p, r) in enumerate(ex):
    s = p + r; ids[i, :len(s)] = torch.tensor(s)
    lab[i, len(p):len(s)] = torch.tensor(r)          # train on response only
    lab_nomask[i, :len(s)] = torch.tensor(s)         # prompt too, pad still ignored
print("input_ids\n", ids); print("labels (masked)\n", lab)
logits = torch.randn(len(ex), L, V)                  # stand-in for model output
def loss(lab):
    sl, sy = logits[:, :-1], lab[:, 1:]              # shift: position t predicts token t+1
    return F.cross_entropy(sl.reshape(-1, V), sy.reshape(-1), ignore_index=IGN)
def manual(lab):
    sl, sy = logits[:, :-1].reshape(-1, V), lab[:, 1:].reshape(-1); keep = sy != IGN
    return -F.log_softmax(sl, -1)[keep, sy[keep]].mean()
print("tokens counted: masked", int((lab[:, 1:] != IGN).sum()), "| unmasked-prompt", int((lab_nomask[:, 1:] != IGN).sum()))
print("loss response-only:", round(loss(lab).item(), 4), "manual:", round(manual(lab).item(), 4))
print("loss incl. prompt :", round(loss(lab_nomask).item(), 4))
# packing: two examples in one row, labels still masked per example; position ids restart
packed = ex[0][0] + ex[0][1] + ex[1][0] + ex[1][1]
pos = list(range(8)) + list(range(4))
print("packed ids", packed); print("position_ids restart per example:", pos)
