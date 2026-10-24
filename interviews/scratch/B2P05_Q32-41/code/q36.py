# Standalone, numpy + torch. One prompt, 6 possible responses, so everything can be computed exactly.
import numpy as np, torch
torch.set_num_threads(1)
rng = np.random.default_rng(0)
K, beta = 6, 0.5
ref = rng.dirichlet(np.ones(K)); r = rng.normal(0, 1, K)           # reference policy pi_ref(y|x) and a reward r(y)

def J(pi):                                                         # regularised objective: E_pi[r] - beta * KL(pi || ref)
    return float((pi * r).sum() - beta * (pi * np.log(pi / ref)).sum())

# 1) closed form: pi*(y) = ref(y) * exp(r(y)/beta) / Z
w = ref * np.exp(r / beta); Z = w.sum(); pistar = w / Z
best_rand = max(J(rng.dirichlet(np.ones(K) * a)) for a in (0.3, 1, 5, 50) for _ in range(5000))
def perturb():
    q = np.clip(pistar + rng.normal(0, 0.02, K), 1e-6, None); return q / q.sum()
best_pert = max(J(perturb()) for _ in range(5000))
print(f"J(pi*) = {J(pistar):.6f}   beta*log Z = {beta * np.log(Z):.6f}   (equal: the max value is beta log Z)")
print(f"best J over 20000 random distributions {best_rand:.6f}; over 5000 small perturbations of pi* {best_pert:.6f}; J(ref) = {J(ref):.6f}")
assert J(pistar) > best_rand and J(pistar) > best_pert

# 2) invert: r(y) = beta*log(pi*/ref) + beta*log Z.   The Z term is the same for every y of the prompt, so it cancels in a difference
rhat = beta * np.log(pistar / ref)
print("max |r - (rhat + beta log Z)| =", float(np.abs(r - (rhat + beta * np.log(Z))).max()))
w_i, l_i = int(r.argmax()), int(r.argmin())      # winner = higher-reward response
print(f"pairwise: r_w - r_l = {r[w_i] - r[l_i]:.6f}   rhat_w - rhat_l = {rhat[w_i] - rhat[l_i]:.6f}   (Z cancelled)")
for Zfake in (0.1, 1.0, 37.0):                                     # any constant offset gives the same Bradley-Terry probability
    d = (rhat[w_i] + beta * np.log(Zfake)) - (rhat[l_i] + beta * np.log(Zfake))
    print(f"  with an arbitrary offset log Z={np.log(Zfake):+.2f}: P(w beats l) = {1/(1+np.exp(-d)):.6f}")
print(f"  true Bradley-Terry P(w beats l) from r = {1/(1+np.exp(-(r[w_i]-r[l_i]))):.6f}")

# 3) DPO loss: -log sigmoid(beta*(log pi/ref(y_w) - log pi/ref(y_l))). Train a policy on the EXACT expected loss over all pairs
#    (each ordered pair weighted by its Bradley-Terry probability) and check it recovers pi*.
P = 1 / (1 + np.exp(-(r[:, None] - r[None, :])))                   # P[i, j] = prob i is preferred over j under the true reward
Pt, reft = torch.tensor(P), torch.tensor(ref)
logits = torch.zeros(K, dtype=torch.float64, requires_grad=True)
opt = torch.optim.Adam([logits], lr=0.05)
for step in range(3000):
    if step in (0, 100, 500): print("  step", step, "max abs diff to pi* so far", float(np.abs(torch.softmax(logits, 0).detach().numpy() - pistar).max()))
    opt.zero_grad()
    lr_ = torch.log_softmax(logits, 0) - reft.log()               # log pi/ref per response
    margin = beta * (lr_[:, None] - lr_[None, :])
    loss = -(Pt * torch.nn.functional.logsigmoid(margin)).sum() / K**2
    loss.backward(); opt.step()
pi = torch.softmax(logits, 0).detach().numpy()
print("learned vs closed-form pi*:", np.round(pi, 4), np.round(pistar, 4), "max abs diff", float(np.abs(pi - pistar).max()))
