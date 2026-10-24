### Q32 ⭐⭐ 🟡 How do you evaluate a reward model itself (held-out preference accuracy, agreement with humans, best-of-n probes)?
**Asked at:** post-training loops, research-leaning teams
**Say this first (1 line):** A reward model is only useful if its ranking matches what humans want where the policy will actually go, so I check: pairwise accuracy on held-out human pairs, calibration, behaviour on out-of-distribution prompts, and whether best-of-n picks and the over-optimisation curve hold up against fresh human or gold judgments.

**Then explain:**
- **Held-out pairwise accuracy:** on pairs the RM never trained on, how often is `r(chosen) > r(rejected)`. Easy to compute, but it is capped by label noise: if humans themselves agree only about 70-75% of the time, an accuracy of 72% may already be near the ceiling. So I always report it next to inter-annotator agreement.
- **Calibration:** the Bradley-Terry loss treats `sigmoid(r_A - r_B)` as the probability that A wins. I bin pairs by that probability and compare it with how often humans actually picked A (ECE, expected calibration error: the average gap between stated confidence and actual hit rate). An overconfident RM can have the same accuracy but a much worse ECE, and that matters when the score is used as a numeric reward in PPO.
- **Fresh human agreement:** a new batch of pairs, labelled by new annotators with the current guidelines, on prompts and *policy outputs* from the model I am training now. Old preference data comes from older models; the RM may be great there and wrong on today's outputs.
- **Out-of-distribution sets:** slice by domain (code, maths, safety, long answers, other languages), by length and by style. Check length bias directly: does a longer answer win even when it is not better? A benchmark suite of such slices exists (RewardBench; from memory, not verified: check what it covers before quoting it).
- **Best-of-n probe:** sample n answers per prompt, take the RM's top pick, and have humans (or a trusted judge) compare it with a random pick. The win rate should rise with n. If it flattens or drops at high n, the RM is being exploited.
- **Over-optimisation curve:** track proxy reward against an independent gold signal as the policy moves away from the reference (KL). The proxy keeps rising while gold rises, peaks, then falls; Gao et al. reported this shape (seen only as snippets). The peak tells me how much KL budget this RM can take (Q34).

**Example:** (illustrative numbers, close to the synthetic run below) My RM gets 72% on a held-out set. I check human agreement on those labels: 73%. So 72% is near the ceiling, not weak. But ECE is 0.20, so its probabilities are overconfident. I would temperature-scale or use rank-normalised rewards, not retrain. A best-of-8 probe then shows humans prefer the RM pick 84% of the time, which tells me the ranking is useful at the top, where RL will push.

**Code:** (executed, standalone, numpy only; SYNTHETIC data, not a real reward model)
```python
# Standalone, numpy only. SYNTHETIC data: a made-up reward model (RM) scored against made-up human labels.
import numpy as np
rng = np.random.default_rng(0)
N = 20000
true_gap = rng.normal(0, 1.5, N)              # hidden true quality difference (chosen minus rejected) for each pair
p_human = 1 / (1 + np.exp(-true_gap))         # humans prefer A over B with this probability (label noise built in)
human_pick_A = rng.random(N) < p_human        # observed human label: True = A preferred
noise_ceiling = np.mean(np.maximum(p_human, 1 - p_human))   # best possible accuracy against these noisy labels

def rm_delta(scale, noise, g):                # RM score difference = scale * (true gap + RM error)
    return scale * (true_gap + rng.normal(0, noise, N) + g)

def ece(prob_A, y, bins=10):                  # expected calibration error on P(A preferred)
    conf = np.where(prob_A >= .5, prob_A, 1 - prob_A); pred = prob_A >= .5; correct = pred == y
    edges = np.linspace(.5, 1, bins + 1); out = 0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any(): out += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return out

print(f"noise ceiling (best possible accuracy on these labels): {noise_ceiling:.3f}")
for name, scale, noise, shift in [("good RM, calibrated scale", 1.0, 0.5, 0.0),
                                  ("overconfident RM (x4 score scale)", 4.0, 0.5, 0.0),
                                  ("worse RM (more error)", 1.0, 2.0, 0.0)]:
    d = rm_delta(scale, noise, shift); p = 1 / (1 + np.exp(-d))
    acc = np.mean((d > 0) == human_pick_A)
    print(f"{name:42s} accuracy {acc:.3f}  ECE {ece(p, human_pick_A):.3f}")

# Best-of-n probe: RM picks the top of n candidates; how often does a (noisy) human judge prefer it to a random candidate?
def bon_win(n, noise, trials=4000):
    wins = 0
    for _ in range(trials):
        q = rng.normal(0, 1.5, n); rm = q + rng.normal(0, noise, n)
        pick, other = np.argmax(rm), rng.integers(n)
        if other == pick: other = (pick + 1) % n
        wins += rng.random() < 1 / (1 + np.exp(-(q[pick] - q[other])))
    return wins / trials
print("best-of-n win rate vs a random candidate (human-style noisy judge):")
for n in (2, 8, 32): print(f"  n={n:2d}  good RM {bon_win(n, 0.5):.3f}   weak RM {bon_win(n, 2.0):.3f}")
```
Output from my run: the noise ceiling is 0.735; the good RM gets 0.723 accuracy with ECE 0.021; an RM with the same kind of error but 4x score scale has accuracy 0.716 but ECE 0.201 (confident and wrong too often); a worse RM gets 0.631. In the best-of-n probe the good RM's pick beats a random candidate 77%, 84%, 90% of the time at n=2, 8, 32, while the weak RM gets 66%, 70%, 77%. Each RM was scored on freshly drawn noise, so accuracies differ slightly. All of it is synthetic; the point is the method.

**Follow-ups:**
- *Why not just use accuracy?* It ignores calibration and the top of the distribution. Two RMs with equal accuracy can behave very differently under optimisation pressure.
- *How do you know the human labels are good?* Measure inter-annotator agreement and gold-item accuracy (Q7, Q38); use them as the ceiling.
- *Does a good offline score mean the RL run will be fine?* No. I still watch proxy vs gold during training and sample outputs by hand.

**Common mistakes:**
- Reporting accuracy without the noise ceiling.
- Evaluating only on the RM's own training distribution, not on current policy samples.
- Ignoring length and style bias.
- Treating calibration as irrelevant when the score is used as a raw reward.

### Q33 ⭐ 🟡 AI code review: this LLM-written DPO/PPO training snippet has bugs (loss sign, reference model gradients, summed vs averaged log-probabilities, KL direction, missing clipping). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
**Say this first (1 line):** I review preference-training code against a checklist: loss sign, frozen reference, the same log-prob reduction for both responses, KL sign, ratio clipped, advantages normalised, old log-probs detached. Then I prove each bug on tiny tensors by its symptom and check the fixed code against an independent reference.

**Then explain:**

| # | Bug | Symptom (from my run, tiny torch demo) |
|---|---|---|
| 1 | DPO loss sign flipped (`+logsigmoid` instead of `-logsigmoid`) | Margin (implicit reward chosen minus rejected) after 60 steps: +8.14 fixed, -117.29 buggy. The model is trained to prefer the rejected answer, and nothing stops it |
| 2 | Reference model not frozen (computed with gradients, or put in the optimiser) | Reference logits drift by 3.59 (sum of absolute change) vs 0.00 frozen. The anchor moves with the policy, so the KL constraint is gone. At real scale it also stores a graph for a second large model |
| 3 | Chosen log-probs summed, rejected averaged | Gradient weight per rejected token: 0.102 vs 0.386 fixed (about 1/4, since the rejected answer has 4 tokens). Long chosen answers dominate: a hidden length bias |
| 4 | KL sign or direction wrong | For sampled tokens `logp - logref` gives 0.2479 (exact KL(pi\|\|ref) 0.2487). The flipped `logref - logp` gives -0.2479: a negative "KL" that pays the policy for drifting. The reverse KL(ref\|\|pi) is a different number, 0.2849 |
| 5 | No ratio clipping, several passes on one batch | Max probability ratio after 40 passes: 1.44 clipped vs 4.88 unclipped |
| 6 | Advantages not normalised (rewards near +100) | Gradient norm 28.33 raw vs 0.46 normalised, and an all-positive advantage pushes up every sampled action |
| 7 | Old log-prob not detached | Ratio prints 1.0 (looks right) but gradient norm is 0.0000: new and old paths cancel exactly, nothing is learned. Detached: 0.4647 |

- **Isolation:** every demo changes one thing against the same setup (a 5-token vocabulary, one table of logits as the "policy"), so each symptom is attributable. This is a toy, not a transformer; the symptom sizes are not what a real run would show, only the direction.
- **Which direction is correct:** PPO samples from the policy, so the per-token KL term is `logp - logref` on the sampled tokens, an estimate of KL(pi || ref). Many implementations fold this into the reward as `-beta * (logp - logref)` (the common RLHF setup; Q2). DPO needs the *sequence* log-prob, normally the sum over response tokens, for policy and reference in the same way.
- **Checks I would add to any such code:** print the trainable parameter count and `ref.requires_grad`; assert the first-epoch ratio is 1 *and* the gradient is not zero; log the mean KL (it should be non-negative on average); log the clip fraction; unit-test on tiny tensors against a plain-loop reference, as below.
- **Not run (no real model or library here):** masking of prompt/padding tokens in the log-prob sum, and EOS handling. They belong on the same checklist, the same as in Part 4 Q37.
- **Fixed versions vs reference:** the fixed DPO loss matched a plain numpy float64 loop to 10 decimals on three random cases (0.5648279127, 0.4667483073, 1.1031749310), the fixed PPO loss matched (0.0664234596), and the DPO gradient matched central finite differences (-0.15000000).

**Example:** an LLM-written training loop reports DPO loss falling smoothly and the implicit margin growing, but generations get worse. I check the sign first. In my toy the flipped version drives the margin to -117 while the loss number (a negative log-sigmoid with the wrong sign) just keeps going down toward minus infinity. A loss that heads below zero when it should be bounded below by zero is itself the red flag.

**Code:** (executed, standalone, torch + numpy, CPU, seconds; toy tensors, no real model)
```python
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
```

**Follow-ups:**
- *Why sum and not mean in DPO?* The sequence log-prob is the log of the probability of the whole response, which is what the derivation uses (Q36). Length-normalised variants exist as deliberate choices (for example SimPO, from memory, not verified); the bug is mixing the two.
- *Why is the old log-prob detached?* It is a constant from the sampling policy. If it is attached, it cancels the new log-prob's gradient. If you recompute it with gradient on, you get exactly the zero-gradient case above.
- *Does clipping alone keep the policy near the reference?* No. Clipping limits the step per batch against the old policy; the KL term anchors to the reference (Q2).

**Common mistakes:**
- Reading code for style and never running it on tiny tensors.
- Trusting a falling loss without checking the sign and the margin.
- Letting the reference model share an optimiser or a graph with the policy.
- Averaging log-probs for one response and summing for the other.
- Saying "ratio is 1 so it is fine" without looking at the gradient.

### Q34 ⭐ 🟡 Best-of-n with a reward model vs RL fine-tuning: what are the cost, quality and over-optimisation trade-offs?
**Asked at:** post-training loops, product, GenAI startups
**Say this first (1 line):** Best-of-n draws n answers and returns the one with the highest reward-model score: no training, but n times the generation cost at every request. RL pays that cost once during training and bakes the preference into the policy. Both over-optimise the same proxy: the more you push (bigger n or more KL), the more you exploit reward-model errors.

**Then explain:**

| | Best-of-n (BoN) | RL (PPO or similar) |
|---|---|---|
| Training | none, only a reward model | a full RL run (Q41), several models in memory |
| Inference cost | n generations plus n reward-model scores per request. Can run in parallel, so latency grows less than cost, but throughput drops | one generation, like the base model |
| Flexibility | change n or the reward model any time, per request | a new policy per change |
| Risk control | simple knob: n | KL penalty, early stopping (Q2) |
| Typical use | quick win, data generation (rejection sampling, Part 4 Q47), test-time compute (Part 2 Q43) | amortise the gain into the model for cheap serving |

- **Over-optimisation:** Gao et al. reported (seen only as snippets, not opened) that for both BoN and RL, the proxy reward keeps rising while the gold reward peaks and then falls as you optimise harder, measured in KL from the base. My demo shows the same mechanism in a synthetic setting.
- **How much does BoN move the distribution?** A known result (from memory, not verified as a citation): the KL divergence of the best-of-n distribution from the base is at most `log n - (n-1)/n`. I checked it numerically on three discrete toys and it held in every case (table below). So n=16 uses at most about 1.8 nats, n=64 at most about 3.2 nats of KL. Useful as a cheap way to put BoN and RL on the same KL axis.
- **Why it saturates or reverses:** with light noise between proxy and truth, the selected sample's true reward grows roughly like the top of a Gaussian: slowly, with diminishing returns. With heavy noise it grows even more slowly. If a few samples are exploits (proxy very high, true quality bad), then as n grows you are more likely to see one, and the true reward of the pick *falls*.
- **Choosing:** BoN for low traffic, quick experiments, offline data generation, or when the reward model changes often. RL (or distil the BoN outputs into the model, Part 4 Q47) when serving volume makes n-times cost too expensive.
- **My demo numbers (SYNTHETIC; true reward is standard normal; proxy is true reward plus noise):**

| n | noise 0.3 | noise 2.0 | noise 0.5 with 1% reward-model exploits |
|---|---|---|---|
| 1 | 0.00 | -0.00 | -0.03 |
| 4 | 0.99 | 0.46 | 0.80 |
| 16 | 1.68 | 0.79 | 1.06 |
| 64 | 2.25 | 1.05 | 0.20 |
| 256 | 2.71 | 1.27 | -1.57 |
| 1024 | 3.11 | 1.46 | -2.00 |

  The exploit column peaks near n=16 and then falls, even though the proxy score of the pick keeps rising (2.43 at n=16, 6.70 at n=1024). KL check: uniform base over 1000 outcomes gave 1.835 at n=16 against the bound 1.835 (equality in the limit of many distinct outcomes), a random 50-outcome base gave 1.821, a skewed 20-outcome base 1.794.

**Example:** a support bot answers once a minute per user. With n=8 and a reward model you get a clear quality gain but 8x the generation bill and about 2x latency if you batch the samples. I would use n=4 to 8 as a launch fix, collect the winners, and fine-tune on them (rejection sampling) so that later I can drop n back to 1 or 2.

**Code:** (executed, standalone, numpy only; SYNTHETIC)
```python
# Standalone, numpy only. SYNTHETIC: no real model or reward model.
import numpy as np
rng = np.random.default_rng(0)

# ---- Part A: best-of-n on a proxy reward = true reward + noise ----
def bon_true(n, noise, hack_rate=0.0, trials=20000):
    t = rng.normal(0, 1, (trials, n))                              # true reward of each of n samples
    proxy = t + rng.normal(0, noise, (trials, n))
    if hack_rate:                                                  # a few samples "exploit" the RM: huge proxy, bad true reward
        h = rng.random((trials, n)) < hack_rate
        proxy = np.where(h, proxy + 5.0, proxy); t = np.where(h, -2.0, t)
    pick = proxy.argmax(1)
    return t[np.arange(trials), pick].mean(), proxy[np.arange(trials), pick].mean()
ns = [1, 2, 4, 8, 16, 64, 256, 1024]
print("true reward of the selected sample (mean over 20000 prompts); higher is better")
print(f"{'n':>5} | {'noise 0.3':>9} {'noise 2.0':>9} | {'noise 0.5 + 1% RM exploits':>27} (proxy of pick)")
for n in ns:
    a, b = bon_true(n, .3)[0], bon_true(n, 2.0)[0]; c, cp = bon_true(n, .5, 0.01)
    print(f"{n:5d} | {a:9.2f} {b:9.2f} | {c:14.2f} ({cp:5.2f})")

# ---- Part B: KL of the best-of-n distribution from the base, vs log n - (n-1)/n ----
def bon_kl(p, n):                      # p: base probabilities of outcomes already sorted by reward (low to high, no ties)
    F = np.cumsum(p); Fprev = np.concatenate([[0.], F[:-1]]); q = F**n - Fprev**n
    m = q > 0; return float((q[m] * np.log(q[m] / p[m])).sum()), q
print("\nKL(best-of-n || base) on a discrete toy (outcomes sorted by reward) vs the claimed bound log n - (n-1)/n")
for name, p in [("uniform over 1000", np.ones(1000) / 1000), ("random over 50", rng.dirichlet(np.ones(50))),
                ("skewed over 20", np.array([2.0 ** -i for i in range(20)]) / np.array([2.0 ** -i for i in range(20)]).sum())]:
    row = []
    for n in (2, 4, 16, 64):
        kl, q = bon_kl(p, n); assert abs(q.sum() - 1) < 1e-9
        row.append(f"n={n}: KL {kl:.3f} <= {np.log(n) - (n - 1) / n:.3f} {'ok' if kl <= np.log(n) - (n - 1) / n + 1e-12 else 'VIOLATED'}")
    print(f"  {name:18s}", " | ".join(row))
print("generation cost: n=1 -> 1x, n=16 -> 16x the samples per request (can run in parallel, so latency grows less than cost)")
```

**Follow-ups:**
- *Why not set n very large?* Cost grows linearly and the returns shrink: the best of 1024 is not 1024 times better. With an imperfect proxy the true reward can fall.
- *Can BoN prevent reward hacking?* It limits it (the KL is bounded by a function of n), but does not remove it. A better or ensembled reward model, a cap on n, and a gold check on samples help.
- *How do you compare BoN with RL fairly?* Plot gold reward against KL from the base for both, as in Gao et al. (reported).

**Common mistakes:**
- Saying BoN has no over-optimisation because it does no training.
- Forgetting that the n generations are a serving cost on every request.
- Measuring only the proxy score of the winner, which always rises.
- Quoting the KL bound as exact rather than an upper bound.
