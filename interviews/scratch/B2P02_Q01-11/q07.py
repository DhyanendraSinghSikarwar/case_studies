import math, torch, torch.nn.functional as F
torch.manual_seed(0)
V, N = 50, 2000
uniform = torch.zeros(N, V); y = torch.randint(0, V, (N,))
nll = F.cross_entropy(uniform, y); print("uniform: loss", round(nll.item(),4), "ppl", round(math.exp(nll.item()),3), "V", V)
logits = torch.randn(N, V) * 2; logits[torch.arange(N), y] += 3
nll = F.cross_entropy(logits, y); print("peaked model: loss", round(nll.item(),3), "ppl", round(nll.exp().item(),2), "bits/token", round(nll.item()/math.log(2),3))
# illustrative: same 1000-byte text, two hypothetical tokenizers
nbytes = 1000
for name, ntok, mean_nll in [("A (250 tok)", 250, 3.0), ("B (400 tok)", 400, 1.9)]:
    total = ntok * mean_nll
    print(name, "ppl", round(math.exp(mean_nll), 2), "total nats", total, "bpb", round(total/math.log(2)/nbytes, 3))
