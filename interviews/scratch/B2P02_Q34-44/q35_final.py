import torch

def buggy_sample(logits, temperature=0.8, top_p=0.9):      # logits: (B, V)
    probs = torch.softmax(logits, dim=-1)                   # BUG 2: softmax before temperature
    probs = probs / temperature                             #        (divides probabilities)
    sorted_p, idx = torch.sort(probs, descending=True)      # (sorts along last dim: ok)
    cum = torch.cumsum(sorted_p, dim=-1)
    cutoff = int((cum < top_p).sum())                       # BUG 5: one count for the whole batch
    sorted_p[:, cutoff:] = 0                                # BUG 1: off-by-one, drops crossing token
                                                            # BUG 3: no renormalisation
    logits.zero_()                                          # BUG 4: stands in for in-place edits
    return idx[:, 0]                                        #        (placeholder, not the point)

def sample_top_p(logits, temperature=0.8, top_p=0.9, generator=None):
    scaled = logits / temperature                           # out-of-place, on logits
    probs = torch.softmax(scaled, dim=-1)
    sorted_p, idx = torch.sort(probs, dim=-1, descending=True)
    cum = torch.cumsum(sorted_p, dim=-1)
    keep = (cum - sorted_p) < top_p                         # mass BEFORE token < top_p
    keep[:, 0] = True                                       # never empty
    sorted_p = sorted_p * keep
    sorted_p = sorted_p / sorted_p.sum(dim=-1, keepdim=True)
    choice = torch.multinomial(sorted_p, 1, generator=generator)
    return idx.gather(-1, choice).squeeze(-1)

def nucleus_ref(row, temperature, top_p):                   # independent pure-python reference
    import math
    z = [v / temperature for v in row]; m = max(z)
    e = [math.exp(v - m) for v in z]; s = sum(e); p = [v / s for v in e]
    kept, mass = [], 0.0
    for i in sorted(range(len(p)), key=lambda i: -p[i]):
        kept.append(i); mass += p[i]
        if mass >= top_p: break
    tot = sum(p[i] for i in kept)
    return [p[i] / tot if i in kept else 0.0 for i in range(len(p))]

torch.manual_seed(0)
l = torch.log(torch.tensor([[0.5, 0.3, 0.15, 0.05]]))
cum = torch.cumsum(torch.softmax(l, -1), -1)
print("Bug1 cum:", [round(v, 2) for v in cum[0].tolist()], "| top_p=0.7: buggy keeps", int((cum < 0.7).sum()), "token, correct nucleus has 2")
print("Bug2 right:", [round(v, 4) for v in torch.softmax(l / 0.5, -1)[0].tolist()],
      "| wrong:", [round(v, 4) for v in (torch.softmax(l, -1) / 0.5)[0].tolist()], "(sums to 2.0)")
print("Bug3 kept mass 0.8 -> renormalised", (torch.tensor([0.5, 0.3]) / 0.8).tolist())
x = torch.randn(2, 5); x0 = x.clone(); buggy_sample(x)
print("Bug4 buggy changed caller logits:", not torch.equal(x, x0))
x = torch.randn(2, 5); x0 = x.clone(); sample_top_p(x)
print("     fixed leaves them alone:", torch.equal(x, x0))
b = torch.tensor([[3., 0, 0, 0, 0], [1., 1, 1, 1, 1]])
cm = torch.cumsum(torch.sort(torch.softmax(b, -1), descending=True)[0], -1)
print("Bug5 per-row counts:", (cm < 0.9).sum(-1).tolist(), "| buggy single scalar:", int((cm < 0.9).sum()))

B, V, N = 3, 8, 40000
logits = torch.randn(B, V) * 2
g = torch.Generator().manual_seed(1)
s = sample_top_p(logits.repeat(N, 1), 0.8, 0.9, generator=g).view(N, B)
for r in range(B):
    emp = torch.bincount(s[:, r], minlength=V).float() / N
    ref = torch.tensor(nucleus_ref(logits[r].tolist(), 0.8, 0.9))
    print(f"row {r}: max|empirical-reference| = {(emp-ref).abs().max():.4f}, sampled outside nucleus: {bool(((emp>0)&(ref==0)).any())}")
