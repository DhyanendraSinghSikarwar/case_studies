import torch
torch.set_num_threads(1)
torch.manual_seed(0)

def group_advantages(rewards, eps=1e-6):
    r = torch.as_tensor(rewards, dtype=torch.float32)
    return (r - r.mean()) / (r.std(unbiased=False) + eps)

for g in ([1, 0, 0, 1], [1, 1, 1, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0.2, 0.5, 0.9, 0.4]):
    print(g, "->", [round(x, 3) for x in group_advantages(g).tolist()])

# Toy verifiable bandit: 6 candidate answers, answer 4 is correct (reward 1 by exact match), else 0.
# Softmax policy, REINFORCE with a group-mean/std baseline (no value network), KL to uniform reference.
K, correct, G, beta = 6, 4, 8, 0.02
def run(seed, use_std=True, steps=150):
    torch.manual_seed(seed)
    logits = torch.zeros(K, requires_grad=True)
    ref = torch.full((K,), 1.0 / K)
    opt = torch.optim.Adam([logits], lr=0.1)
    for _ in range(steps):
        probs = torch.softmax(logits, 0)
        a = torch.multinomial(probs.detach(), G, replacement=True)
        r = (a == correct).float()
        adv = (r - r.mean()) / (r.std(unbiased=False) + 1e-6) if use_std else (r - r.mean())
        logp = torch.log(probs[a])
        kl = (probs * (probs.log() - ref.log())).sum()
        loss = -(adv.detach() * logp).mean() + beta * kl
        opt.zero_grad(); loss.backward(); opt.step()
    return torch.softmax(logits, 0)[correct].item()
res = [run(s) for s in range(5)]
print("P(correct) after training, 5 seeds:", [round(x, 3) for x in res])
