# Standalone, torch + numpy only. Tiny tensors: policy = one table of logits over a 5-token vocab.
# Each bug is run in isolation against the same setup, then the fixed versions are checked against an independent numpy reference.
import math, numpy as np, torch, torch.nn.functional as F
torch.set_num_threads(1); torch.manual_seed(0)
V = 5
def seq_logps(theta, toks, how="sum"):                       # log-prob of a response under the "policy" theta
    lp = F.log_softmax(theta, -1)[torch.tensor(toks)]
    return lp.sum() if how == "sum" else lp.mean()

# ---------- DPO ----------
def dpo_fixed(pc, pr, rc, rr, beta=0.5):                      # inputs: sequence log-probs (sums)
    return -F.logsigmoid(beta * ((pc - rc) - (pr - rr)))
def dpo_sign_bug(pc, pr, rc, rr, beta=0.5):
    return F.logsigmoid(beta * ((pc - rc) - (pr - rr)))       # BUG: sign flipped

chosen, rejected = [0, 1, 2], [3, 4, 3]
def run_dpo(loss_fn, freeze_ref=True, steps=60, lr=0.5):
    theta = torch.zeros(V, requires_grad=True)
    ref = torch.zeros(V, requires_grad=not freeze_ref)
    params = [theta] if freeze_ref else [theta, ref]          # BUG 2 variant: reference ends up in the optimizer
    opt = torch.optim.SGD(params, lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        if freeze_ref:
            with torch.no_grad(): rc, rr = seq_logps(ref, chosen), seq_logps(ref, rejected)
        else: rc, rr = seq_logps(ref, chosen), seq_logps(ref, rejected)
        loss_fn(seq_logps(theta, chosen), seq_logps(theta, rejected), rc, rr).backward(); opt.step()
    with torch.no_grad():
        m = (seq_logps(theta, chosen) - seq_logps(ref, chosen)) - (seq_logps(theta, rejected) - seq_logps(ref, rejected))
    return m.item(), (ref.detach() - 0).abs().sum().item(), theta.detach()

print("== DPO bug 1: loss sign flipped ==")
print(f"  fixed: implicit-reward margin after 60 steps {run_dpo(dpo_fixed)[0]:+.2f} (chosen up, rejected down)")
print(f"  buggy: margin {run_dpo(dpo_sign_bug)[0]:+.2f} (model is trained to prefer the rejected answer)")

print("== DPO bug 2: reference model not frozen ==")
m_ok, drift_ok, _ = run_dpo(dpo_fixed, True); m_bug, drift_bug, _ = run_dpo(dpo_fixed, False)
print(f"  frozen ref: ref logits change {drift_ok:.2f}, margin {m_ok:+.2f}")
print(f"  ref in graph and optimizer: ref logits change {drift_bug:.2f}, margin {m_bug:+.2f} (anchor moves with the policy, so the KL constraint is gone)")

print("== DPO bug 3: summed log-prob for chosen, mean for rejected ==")
lc = torch.randn(12, requires_grad=True); lr_ = torch.randn(4, requires_grad=True)   # per-token logs for lengths 12 and 4
zero = torch.tensor(0.)
dpo_fixed(lc.sum(), lr_.sum(), zero, zero).backward()
print("  fixed (both sum): gradient weight per chosen token", round(lc.grad[0].item(), 3), "| per rejected token", round(lr_.grad[0].item(), 3))
lc.grad = lr_.grad = None
dpo_fixed(lc.sum(), lr_.mean(), zero, zero).backward()
print("  buggy (sum vs mean): per chosen token", round(lc.grad[0].item(), 3), "| per rejected token", round(lr_.grad[0].item(), 3), "(rejected tokens get 1/4 the push)")

# ---------- KL direction / estimator ----------
print("== PPO bug 4: KL sign / direction ==")
g = torch.Generator().manual_seed(1)
pi = torch.softmax(torch.tensor([1.5, .5, 0., -1.]), 0); ref = torch.softmax(torch.tensor([.3, .2, .1, 0.]), 0)
kl_pi_ref = (pi * (pi / ref).log()).sum().item(); kl_ref_pi = (ref * (ref / pi).log()).sum().item()
x = torch.multinomial(pi, 200000, replacement=True, generator=g)           # samples come from the policy
est_ok = (pi.log()[x] - ref.log()[x]).mean().item(); est_bug = (ref.log()[x] - pi.log()[x]).mean().item()
print(f"  exact KL(pi||ref) {kl_pi_ref:.4f}; sample estimate mean(logp - logref) {est_ok:.4f}")
print(f"  buggy mean(logref - logp) {est_bug:+.4f} (negative: a 'KL' that rewards drifting). Exact KL(ref||pi) is a different number: {kl_ref_pi:.4f}")

# ---------- PPO clipped objective ----------
def ppo_fixed(logp, logp_old, adv, eps=0.2, normalise=True):
    if normalise: adv = (adv - adv.mean()) / (adv.std() + 1e-8)
    r = torch.exp(logp - logp_old.detach())
    return -torch.minimum(r * adv, torch.clamp(r, 1 - eps, 1 + eps) * adv).mean()
def ppo_noclip(logp, logp_old, adv, eps=0.2):
    adv = (adv - adv.mean()) / (adv.std() + 1e-8)
    return -(torch.exp(logp - logp_old.detach()) * adv).mean()               # BUG: no clipping

acts = torch.tensor([0, 0, 1, 1, 2, 3, 3, 3]); adv0 = torch.tensor([1., 1.5, -1., -.5, 0.2, -1., -1.2, -.3])
def run_ppo(loss_fn, epochs=40, lr=0.5):
    theta = torch.zeros(V, requires_grad=True); old = F.log_softmax(theta, -1)[acts].detach()
    opt = torch.optim.SGD([theta], lr=lr); rmax = 1.
    for _ in range(epochs):
        opt.zero_grad(); lp = F.log_softmax(theta, -1)[acts]
        loss_fn(lp, old, adv0).backward(); opt.step()
        rmax = max(rmax, torch.exp(F.log_softmax(theta, -1)[acts] - old).max().item())
    return rmax
print("== PPO bug 5: missing clipping (40 passes over one batch) ==")
print(f"  max probability ratio with clipping {run_ppo(ppo_fixed):.2f}; without clipping {run_ppo(ppo_noclip):.2f}")

print("== PPO bug 6: advantage not normalised (rewards sit near +100) ==")
rew = 100 + adv0
def grad_norm(adv, normalise):
    theta = torch.zeros(V, requires_grad=True); lp = F.log_softmax(theta, -1)[acts]
    ppo_fixed(lp, lp.detach(), adv, normalise=normalise).backward(); return theta.grad.norm().item()
print(f"  gradient norm raw advantage {grad_norm(rew, False):.2f} vs normalised {grad_norm(rew, True):.2f}")

print("== PPO bug 7: old log-prob not detached ==")
theta = torch.zeros(V, requires_grad=True); lp = F.log_softmax(theta, -1)[acts]
lp_old_bug = F.log_softmax(theta, -1)[acts]                 # same weights, still attached to the graph
adv_n = (adv0 - adv0.mean()) / adv0.std()
loss = -(torch.exp(lp - lp_old_bug) * adv_n).mean(); loss.backward()
print(f"  ratio {torch.exp(lp - lp_old_bug)[0].item():.1f} (looks right) but gradient norm {theta.grad.norm().item():.4f}: the two paths cancel, nothing is learned")
theta = torch.zeros(V, requires_grad=True); lp = F.log_softmax(theta, -1)[acts]
ppo_fixed(lp, lp.detach(), adv0).backward(); print(f"  detached old log-prob: gradient norm {theta.grad.norm().item():.4f}")

# ---------- fixed versions vs independent numpy reference (float64, plain loops) ----------
print("== Fixed code vs independent numpy reference ==")
rng = np.random.default_rng(0)
def ref_dpo(pc, pr, rc, rr, beta):
    z = beta * ((pc.sum() - rc.sum()) - (pr.sum() - rr.sum())); return math.log(1 + math.exp(-z))
def ref_ppo(lp, lo, adv, eps):
    a = (adv - adv.mean()) / (adv.std(ddof=1) + 1e-8); tot = 0.
    for i in range(len(lp)):
        r = math.exp(lp[i] - lo[i]); tot += min(r * a[i], min(max(r, 1 - eps), 1 + eps) * a[i])
    return -tot / len(lp)
for _ in range(3):
    pc, pr, rc, rr = (rng.normal(-1, .3, n) for n in (6, 3, 6, 3))
    t = dpo_fixed(*(torch.tensor(a, dtype=torch.float64).sum() for a in (pc, pr, rc, rr)), beta=0.3).item()
    print(f"  DPO torch {t:.10f} numpy {ref_dpo(pc, pr, rc, rr, .3):.10f}")
lp, lo, adv = rng.normal(-1, .3, 20), rng.normal(-1, .3, 20), rng.normal(0, 1, 20)
t = ppo_fixed(torch.tensor(lp), torch.tensor(lo), torch.tensor(adv)).item()
print(f"  PPO torch {t:.10f} numpy {ref_ppo(lp, lo, adv, .2):.10f}")
# DPO gradient vs central finite differences on the policy sequence log-prob
x = torch.tensor(-3., dtype=torch.float64, requires_grad=True); dpo_fixed(x, torch.tensor(-2., dtype=torch.float64), torch.tensor(-3.5, dtype=torch.float64), torch.tensor(-2.5, dtype=torch.float64), .3).backward()
fd = (ref_dpo(np.array([-3 + 1e-6]), np.array([-2.]), np.array([-3.5]), np.array([-2.5]), .3) - ref_dpo(np.array([-3 - 1e-6]), np.array([-2.]), np.array([-3.5]), np.array([-2.5]), .3)) / 2e-6
print(f"  DPO grad autograd {x.grad.item():.8f} finite-diff {fd:.8f}")
