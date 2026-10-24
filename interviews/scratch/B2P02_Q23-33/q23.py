import torch
torch.manual_seed(0)
vocab = ["the", "cat", "sat", "mat", "dog"]
logits = torch.tensor([[2.0, 1.0, 0.1, 0.0, -1.0],   # position 0 logits
                       [0.2, 2.5, 0.3, 0.1, 1.0],
                       [0.0, 0.1, 3.0, 0.2, 0.3]])
tokens = torch.tensor([0, 1, 2])                       # chosen tokens: the cat sat
logp = torch.log_softmax(logits, dim=-1)
tok_lp = logp[torch.arange(3), tokens]
print("token logprobs:", [round(x, 3) for x in tok_lp.tolist()])
print("sequence logprob:", round(tok_lp.sum().item(), 3))
print("length-normalised (mean):", round(tok_lp.mean().item(), 3))
print("top-2 at pos 0:", [(vocab[i], round(v, 3)) for v, i in zip(*[t.tolist() for t in logp[0].topk(2)])])
# logit_bias: +5 on "dog" at every position, added to logits BEFORE softmax
bias = torch.tensor([0, 0, 0, 0, 5.0])
p0, p1 = logp[0].exp(), torch.log_softmax(logits[0] + bias, -1).exp()
print("P(dog) before/after bias:", round(p0[4].item(), 3), round(p1[4].item(), 3))
