import torch, torch.nn.functional as F
torch.manual_seed(0)
B, T, V = 2, 5, 11
logits = torch.randn(B, T, V)            # model output at each position
ids = torch.randint(0, V, (B, T))        # input tokens x_1..x_T
# position t predicts token t+1: drop last logit row, drop first label
loss = F.cross_entropy(logits[:, :-1].reshape(-1, V), ids[:, 1:].reshape(-1))
# manual: -(1/N) sum log p(x_t | x_<t)
logp = logits[:, :-1].log_softmax(-1)
nll = -logp.gather(-1, ids[:, 1:, None]).squeeze(-1)
print("F.cross_entropy:", loss.item(), " manual:", nll.mean().item(), " N =", nll.numel())
# wrong (no shift) for contrast
wrong = F.cross_entropy(logits.reshape(-1, V), ids.reshape(-1))
print("unshifted (wrong) :", wrong.item())
# ignore_index for padding
lab = ids.clone(); lab[1, 3:] = -100
l2 = F.cross_entropy(logits[:, :-1].reshape(-1, V), lab[:, 1:].reshape(-1), ignore_index=-100)
print("with 2 padded labels ignored:", l2.item(), " ln(V) =", torch.log(torch.tensor(float(V))).item())
