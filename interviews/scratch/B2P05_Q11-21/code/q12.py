import torch
torch.set_num_threads(1)
torch.manual_seed(0)

def ppo_clip_loss(logp_new, logp_old, adv, eps=0.2):
    ratio = torch.exp(logp_new - logp_old)
    unclipped = ratio * adv
    clipped = torch.clamp(ratio, 1 - eps, 1 + eps) * adv
    return -torch.min(unclipped, clipped).mean()      # negative: we maximise the surrogate

def kl_shaped_reward(reward, logp, logp_ref, beta=0.1):
    # per-token reward: r - beta * (logp - logp_ref); sequence reward added on the last token
    r = -beta * (logp - logp_ref)
    r[..., -1] = r[..., -1] + reward
    return r

def gae(rewards, values, gamma=1.0, lam=0.95):
    T = rewards.shape[-1]
    adv = torch.zeros_like(rewards); last = 0.0
    for t in reversed(range(T)):
        nv = values[..., t + 1] if t + 1 < T else 0.0
        delta = rewards[..., t] + gamma * nv - values[..., t]
        last = delta + gamma * lam * last
        adv[..., t] = last
    return adv, adv + values

# test 1: ratio == 1 -> surrogate equals mean advantage
lp = torch.randn(8); adv = torch.randn(8)
print("ratio=1:", torch.allclose(-ppo_clip_loss(lp, lp.clone(), adv), adv.mean()))

# test 2: gradients vanish on the clipped side
eps = 0.2
for A, name in [(1.0, "A>0"), (-1.0, "A<0")]:
    for r in [0.5, 1.0, 1.5]:
        lpn = torch.tensor([r]).log().requires_grad_(True)
        loss = ppo_clip_loss(lpn, torch.zeros(1), torch.tensor([A]), eps)
        loss.backward()
        print(f"{name} ratio={r}: grad={lpn.grad.item():+.3f}")

# test 3: autograd matches the hand formula inside the range (d/dlogp = -ratio*A)
lpn = torch.tensor([0.1], requires_grad=True)
ppo_clip_loss(lpn, torch.zeros(1), torch.tensor([2.0])).backward()
print("grad inside range matches -ratio*A:", torch.allclose(lpn.grad, -torch.exp(torch.tensor([0.1])) * 2.0))

# test 4: advantage normalisation
a = torch.tensor([3.0, 1.0, -2.0, 4.0]); an = (a - a.mean()) / (a.std() + 1e-8)
print("normalised mean/std:", round(an.mean().item(), 6), round(an.std().item(), 4))

# KL-shaped reward and GAE on a toy 4-token response
logp = torch.tensor([[-1.0, -0.5, -2.0, -1.5]]); ref = torch.tensor([[-1.2, -0.9, -1.0, -1.5]])
r = kl_shaped_reward(torch.tensor(1.0), logp.clone(), ref, beta=0.1)
print("shaped rewards:", [round(x, 3) for x in r[0].tolist()])
vals = torch.tensor([[0.2, 0.3, 0.4, 0.5]])
adv_g, ret = gae(r, vals)
print("GAE adv:", [round(x, 3) for x in adv_g[0].tolist()])
# lam=1, gamma=1 -> advantage = return-to-go minus value
adv1, _ = gae(r, vals, gamma=1.0, lam=1.0)
print("lam=1 equals return-to-go - V:", torch.allclose(adv1, r.flip(-1).cumsum(-1).flip(-1) - vals))
