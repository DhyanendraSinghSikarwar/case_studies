### Q11 ⭐⭐⭐ 🟡 Your model started refusing benign requests after a safety-training round. What do you investigate and how do you fix it?
**Asked at:** post-training loops, product, safety teams
**Say this first (1 line):** This is over-refusal (exaggerated safety); I would first measure it against an unsafe-compliance number so I do not trade one failure for the other, then trace it to the safety data mix, the reward signal, over-training, or a guardrail threshold, and fix it with borderline-benign training data and rebalancing.

**Then explain:**
- **Measure first, on two sets.** A benign-but-edgy set (for example "how do I kill a Python process?") and a truly unsafe set. XSTest is the usual public example; as reported in its paper listing it has 250 safe prompts in ten types plus 200 unsafe contrasts (seen in search snippets only, so hedge the numbers). Compare refusal rate before and after the safety round. Track both numbers every time.
- **Inspect the safety data mix.** Too many refusal examples, too few "looks scary but is fine" examples, and refusals triggered by keywords rather than intent. Read 50 to 100 failing prompts by hand and group them by type.
- **Check the reward signal.** If annotators or an AI judge preferred a refusal whenever in doubt, the reward model learns "refusal = safe = high reward" (see Q3, Q5, Q17). Score refusals vs helpful answers on borderline prompts with the reward model.
- **Check over-training.** High learning rate, too many epochs, or a weak KL anchor to the reference (Q2) lets the policy drift far into a refusing style. Compare checkpoints.
- **Check the serving stack.** A classifier guardrail with a low threshold, or a system prompt that says "refuse anything risky", can cause this without any model change. Replay the failing prompts with guardrails off to separate model from wrapper.
- **Fixes:** add borderline-benign preference pairs (helpful answer chosen over refusal), keep the true-unsafe pairs, rebalance the mix, tune the classifier threshold per category rather than globally, soften the system prompt policy, and re-evaluate on both sets.

**Example (synthetic, run):** a made-up classifier scores three populations; sweeping the refusal threshold shows the trade-off. At threshold 0.3, 82.8% of edgy-benign prompts are refused and 0.4% of unsafe ones slip through; at 0.5, 37.0% and 8.6%; at 0.7, 5.3% and 46.3%. No threshold wins on both, which is why the data fix (making edgy and unsafe separable) matters more than moving a dial. These numbers come from random draws I chose, not from any real model.

**Code:** (run, numpy; SYNTHETIC scores)
```python
import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: a safety classifier scores prompts in [0,1] (higher = more likely unsafe).
# Three populations: clearly benign, benign-but-edgy (shares wording with unsafe), truly unsafe.
n = 2000
benign = rng.beta(2, 8, n)     # mostly low scores
edgy   = rng.beta(4, 5, n)     # overlaps the unsafe region
unsafe = rng.beta(7, 3, n)     # mostly high scores
print("thr  over-refusal(edgy)  over-refusal(benign)  unsafe-compliance")
for thr in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    over_edgy = (edgy >= thr).mean()
    over_ben = (benign >= thr).mean()
    unsafe_ok = (unsafe < thr).mean()   # model complies with an unsafe prompt
    print(f"{thr:.1f}  {over_edgy:18.3f}  {over_ben:20.3f}  {unsafe_ok:17.3f}")
```
Output (my run):
```
thr  over-refusal(edgy)  over-refusal(benign)  unsafe-compliance
0.3                 0.828                 0.193              0.004
0.4                 0.596                 0.078              0.018
0.5                 0.370                 0.023              0.086
0.6                 0.174                 0.005              0.232
0.7                 0.053                 0.001              0.463
0.8                 0.011                 0.000              0.749
0.9                 0.001                 0.000              0.945
```

**Follow-ups:**
- *How do you know it is the model and not the guardrail?* Replay the same prompts with the guardrail and system prompt removed; compare against the previous checkpoint.
- *Can you just roll back?* Yes as a stopgap, but you lose the safety gain; the aim is a checkpoint that is good on both sets.
- *How do you keep it from coming back?* Put an over-refusal set in the release eval next to the unsafe set (Q10) and gate on both.

**Common mistakes:** Only reporting refusal rate (or only unsafe compliance); fixing it by raising one global threshold; adding more refusal data "to be safe"; testing only obviously benign prompts, which never show the problem; blaming the model before checking the system prompt and classifier.

### Q12 ⭐⭐⭐ 🟡 Code: implement PPO's clipped surrogate objective and the KL-regularised reward in PyTorch and check it on toy tensors.
**Asked at:** big tech, research-leaning teams, post-training coding rounds
**Say this first (1 line):** The PPO surrogate is mean(min(ratio * A, clip(ratio, 1-eps, 1+eps) * A)) with ratio = exp(logp_new - logp_old), which we maximise (so the loss is its negative), and in RLHF the per-token reward is r - beta * (logp - logp_ref).

**Then explain:**
- **Ratio:** how much more (or less) likely the new policy makes the sampled token compared with the policy that generated it. Using log-probs and exp keeps it stable.
- **Clipping:** once the ratio leaves [1-eps, 1+eps] in the direction the advantage wants, the gradient is zero. For A>0 that is ratio above 1+eps; for A<0 it is ratio below 1-eps. On the other side the min keeps the unclipped term, so a bad move is still corrected.
- **KL-shaped reward:** subtract beta * (logp - logp_ref) at every token, so drifting from the reference (Q2) costs reward; the scalar reward model score is added at the last token.
- **GAE (optional):** advantage from one-step errors delta_t = r_t + gamma * V_(t+1) - V_t, summed with weight gamma * lambda. lambda=1 gives return-to-go minus V; lambda=0 gives the one-step error (Q13).
- **Advantage normalisation:** subtract the batch mean, divide by std; keeps the step size independent of reward scale.

**Example:** with eps=0.2 and A=+1, a token whose ratio is 1.5 gets zero gradient (already moved enough), a token at ratio 0.5 still gets gradient -0.5 on the loss (the policy made a good token less likely, so we keep pushing). For A=-1 it mirrors: ratio 0.5 gives zero, ratio 1.5 gives +1.5. In the toy KL-shaped reward below, token rewards are small negatives or positives from the KL term and 1.0 lands on the last token.

**Code:** (run, torch CPU, toy tensors; checks verified with autograd)
```python
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
```
Output (my run):
```
ratio=1: True
A>0 ratio=0.5: grad=-0.500
A>0 ratio=1.0: grad=-1.000
A>0 ratio=1.5: grad=+0.000
A<0 ratio=0.5: grad=+0.000
A<0 ratio=1.0: grad=+1.000
A<0 ratio=1.5: grad=+1.500
grad inside range matches -ratio*A: True
normalised mean/std: -0.0 1.0
shaped rewards: [-0.02, -0.04, 0.1, 1.0]
GAE adv: [0.746, 0.701, 0.675, 0.5]
lam=1 equals return-to-go - V: True
```

**Follow-ups:**
- *Why not just use the unclipped ratio * A?* Nothing stops a large step from a single batch; clipping is a cheap trust region.
- *Is the KL in the reward or the loss?* Both appear in practice (reward shaping as here, or a separate KL loss term); say which one you use. This is a simplified view of what libraries do.
- *What if the old log-probs are recomputed instead of stored?* The ratio is then always 1 and clipping does nothing; store them at sampling time.

**Common mistakes:** Forgetting the minus sign (gradient ascent vs descent); using clip on the ratio but not taking the min; not detaching old log-probs; normalising advantages per token rather than per batch; reading "gradient vanishes when clipped" as "on both sides".

### Q13 ⭐⭐ 🟡 PPO inside RLHF: policy, value head, advantages and GAE, clipping, and why four models (policy, reference, reward, value) are in memory.
**Asked at:** post-training loops, research-leaning teams
**Say this first (1 line):** PPO-based RLHF samples responses from the policy, scores them with a reward model, uses a value head to turn rewards into per-token advantages (GAE), and updates the policy with the clipped objective (Q12), which means four models are alive at once: policy, frozen reference, frozen reward model, and a value model.

**Then explain:**
- **Policy:** the LLM being trained; generates responses and gets the update.
- **Reference:** a frozen copy of the SFT model, used only to compute the KL penalty (Q2).
- **Reward model:** frozen; gives one scalar per response (Q5).
- **Value head/critic:** predicts the expected future reward from each token position, so advantage = actual - expected. Often a head on the policy backbone or a separate model, and it is trained too.
- **Advantage with GAE:** blends low-variance but biased one-step estimates with high-variance full returns; lambda controls the mix.
- **Clipping:** keeps each update close to the sampling policy (Q12).
- **Why it is heavy:** two models are trained (policy, value) so they carry gradients and optimizer state; two are inference-only; plus generation needs a KV cache and training needs activations.
- **GRPO** removes the value model by using group-relative advantages (Q20). **Sharding** (ZeRO or FSDP) spreads weights and optimizer state across GPUs, see Part 2 Q34.

**Example (ASSUMED accounting, computed):** take a 7B policy, with the value and reward models also 7B (an assumption; reward models are often smaller). bf16 weights are 14 GB per model. For the two trained models I assume mixed precision with Adam at 16 bytes per parameter (bf16 weights 2, bf16 grads 2, fp32 master 4, Adam m 4, Adam v 4), which is 112 GB each. Reference and reward add 14 GB each. Total is 252 GB before activations and the KV cache, so you need at least about 3.1 80-GB GPUs even if perfectly sharded, and in practice more. A GRPO-style setup with no value model and a rule reward is 126 GB by the same assumptions. These are my estimates, not measurements; real frameworks use tricks (LoRA, offloading, shared backbones) that change them.

**Code:** (run, plain Python arithmetic; ASSUMED numbers)
```python
# ASSUMED accounting for a 7B-parameter policy; value and reward models assumed also 7B.
P = 7e9
GB = 1e9
bf16 = 2
weights_each = P * bf16 / GB
print(f"bf16 weights per model: {weights_each:.0f} GB")
frozen = 2 * weights_each                      # reference + reward, inference only
# trainable policy and value, mixed precision with Adam:
# bf16 weights (2) + bf16 grads (2) + fp32 master (4) + Adam m (4) + Adam v (4) = 16 B/param
train_bytes = 2 + 2 + 4 + 4 + 4
trainable = 2 * P * train_bytes / GB
print(f"frozen ref + reward: {frozen:.0f} GB")
print(f"policy + value with {train_bytes} B/param training state: {trainable:.0f} GB")
print(f"total before activations and KV cache: {frozen + trainable:.0f} GB")
print(f"80 GB GPUs needed at minimum if perfectly sharded: {(frozen + trainable)/80:.1f}")
# GRPO-style: no value model (critic), reference kept; reward is a rule or a small model
grpo = weights_each + P * train_bytes / GB + weights_each
print(f"GRPO-style (policy train + ref bf16 + reward as bf16 7B): {grpo:.0f} GB; with rule reward: {grpo - weights_each:.0f} GB")
```
Output (my run):
```
bf16 weights per model: 14 GB
frozen ref + reward: 28 GB
policy + value with 16 B/param training state: 224 GB
total before activations and KV cache: 252 GB
80 GB GPUs needed at minimum if perfectly sharded: 3.1
GRPO-style (policy train + ref bf16 + reward as bf16 7B): 140 GB; with rule reward: 126 GB
```

**Follow-ups:**
- *Can the policy and reference share weights?* With LoRA, yes: disable the adapter to get the reference. That is a common memory trick.
- *Why is the value model hard?* It must learn on noisy, sparse sequence-level rewards, and a poor critic gives bad advantages.
- *What dominates at generation time?* The KV cache and slow autoregressive sampling, not the weights.

**Common mistakes:** Saying the reference is trained; forgetting the value model also has optimizer state; counting only weights and ignoring optimizer state and activations; quoting my 252 GB as a universal number.

### Q14 ⭐⭐ 🟡 What are Constitutional AI and RLAIF? How do the two phases work, and what are the benefits and risks of AI feedback?
**Asked at:** post-training loops, safety teams
**Say this first (1 line):** Constitutional AI (Anthropic, arXiv 2212.08073) trains a harmless but non-evasive assistant using a written list of principles as the only human input: a supervised phase where the model critiques and revises its own answers, then an RL phase where AI-judged preferences replace human harm labels (RLAIF, RL from AI feedback).

**Then explain:**
- **Phase 1, supervised:** sample a response to a (possibly harmful) prompt, ask the model to critique it against a principle, ask it to revise, and fine-tune on the revised answers (per the abstract).
- **Phase 2, RL from AI feedback:** sample pairs of responses, have a model judge which is better under the principles, train a preference model on those AI labels, and use it as the reward for RL (per the abstract). It is the same pipeline as RLHF (Q1, Q5) with the harm labels coming from a model.
- **Only human input is the constitution** (the abstract's claim); helpfulness data can still come from humans in practice, so read the claim carefully.
- **Goal:** harmless but non-evasive: explain objections instead of refusing flatly (links to over-refusal, Q11).
- **Benefits:** cheaper and faster than human harm labelling, labels are consistent, the rules are readable and editable.
- **Risks (my judgement):** the AI judge's biases are baked in and can compound across rounds; who writes the constitution and whether it covers real cases is a policy question; and you still need human evaluation to check the result (Q10).

**Example (MOCK, run):** a scripted fake model "answers" a lock-picking request with steps, "critiques" it as violating principle 1, and "revises" it to a refusal that offers a locksmith. The pair (prompt, revision) is one supervised example; the (revision chosen, draft rejected) pair is one RLAIF preference pair. No real LLM is involved; this only shows the data flow.

**Code:** (run; MOCK scripted model, not a real LLM)
```python
# MOCK: a scripted fake "model" (no real LLM). It shows the data flow of the supervised phase only.
CONSTITUTION = ["Do not give instructions that could cause harm.",
                "Stay helpful: explain why you decline and offer a safe alternative."]

def fake_model(prompt):
    # scripted behaviour keyed on the prompt text
    if prompt.startswith("RESPOND:"):
        return "Sure, here is how to pick a lock: insert a tension wrench..."
    if prompt.startswith("CRITIQUE:"):
        return "The reply gives lock-picking steps, which may help a break-in (violates principle 1)."
    if prompt.startswith("REVISE:"):
        return ("I can't walk through bypassing someone else's lock, but if you are locked out "
                "of your own home, a locksmith or your landlord can help.")
    return ""

def critique_revise(user_prompt, principle):
    draft = fake_model("RESPOND: " + user_prompt)
    critique = fake_model(f"CRITIQUE: {principle} || {draft}")
    revision = fake_model(f"REVISE: {critique} || {draft}")
    return {"prompt": user_prompt, "draft": draft, "critique": critique, "revision": revision}

sft_data = []
rec = critique_revise("How do I pick a lock?", CONSTITUTION[0])
sft_data.append((rec["prompt"], rec["revision"]))   # finetune on (prompt, revision)
for k, v in rec.items():
    print(f"{k:9s}: {v}")
print("SFT pairs kept:", len(sft_data))

# RL phase (RLAIF) data flow: the AI judge picks between two samples per principle
def fake_judge(prompt, a, b, principle):
    return "A" if "locksmith" in a else "B"   # scripted, not a real judge
pref = {"chosen": rec["revision"], "rejected": rec["draft"]}
print("judge picks revision:", fake_judge(rec["prompt"], rec["revision"], rec["draft"], CONSTITUTION[1]) == "A")
```
Output (my run):
```
prompt   : How do I pick a lock?
draft    : Sure, here is how to pick a lock: insert a tension wrench...
critique : The reply gives lock-picking steps, which may help a break-in (violates principle 1).
revision : I can't walk through bypassing someone else's lock, but if you are locked out of your own home, a locksmith or your landlord can help.
SFT pairs kept: 1
judge picks revision: True
```

**Follow-ups:**
- *Does it remove humans?* It removes human harm labels, not human oversight; humans write principles and audit outcomes.
- *Why critique before revising?* Writing the critique first tends to make the revision more targeted (reported in the paper; I did not verify details beyond the abstract).
- *RLAIF vs RLHF?* Same loop; only the label source differs.

**Common mistakes:** Saying there is no human at all; confusing the supervised phase with the RL phase; ignoring judge bias; claiming it removes the need for evaluation.

### Q15 ⭐⭐ 🟡 DPO in more detail: the reference model, beta, the implicit reward, data requirements and known failure modes.
**Asked at:** post-training loops, GenAI startups
**Say this first (1 line):** DPO (arXiv 2305.18290) skips the separate reward model and RL: it trains the policy directly on preference pairs with a logistic loss on the gap in implicit rewards, where implicit reward = beta * log(pi / pi_ref), and the frozen reference keeps the policy from drifting.

**Then explain:**
- **Reference model:** frozen SFT model; log-probs from it are precomputed or computed each step. It defines "how far have we moved".
- **Beta:** scales the implicit reward. Small beta lets the policy move far from the reference; large beta keeps it close. It also sets how fast the pair weight saturates (demo below).
- **Gradient weight:** each pair is weighted by sigmoid(-beta * margin), so mis-ranked pairs get large updates and already-correct pairs fade out.
- **Data:** quality matters most (Q7). SFT first on similar data so pairs are roughly on-policy; off-policy pairs from other models make the log-ratios less meaningful.
- **Failure modes (reported, hedge):** the chosen response's log-prob can also fall since the loss only cares about the gap; verbosity; and over-optimisation, which a 2024 paper reportedly found in DPO-style methods (seen as a snippet only). Noisy labels hurt because the loss pushes hard on any mis-ranked pair.
- Code for the loss itself is Q6.

**Example (synthetic, run):** for implicit margins from -4 to +4, the weight is 0.599 to 0.401 at beta=0.1 (almost flat), 0.881 to 0.119 at beta=0.5, and 0.982 to 0.018 at beta=1.0. So at beta=1.0 a badly mis-ranked pair gets about 55 times the weight of a well-ranked one (0.982 / 0.018); at beta=0.1 only 1.5 times. Note the margin here is the log-ratio gap before multiplying by beta.

**Code:** (run, torch CPU; synthetic margins)
```python
import torch
torch.set_num_threads(1)
# SYNTHETIC: DPO per-pair gradient weight = sigmoid(-beta * margin), where
# margin = (logp_c - ref_c) - (logp_r - ref_r) is the implicit-reward gap / beta.
m = torch.tensor([-4.0, -2.0, 0.0, 2.0, 4.0])   # implicit log-ratio margin (positive = correctly ranked)
for beta in [0.1, 0.5, 1.0]:
    z = (beta * m).clone().requires_grad_(True)
    loss = -torch.nn.functional.logsigmoid(z).sum()
    loss.backward()
    w = torch.sigmoid(-beta * m)
    print(f"beta={beta}: loss grad wrt z = {[round(-g,3) for g in z.grad.tolist()]}  weight sigmoid(-beta*m) = {[round(x,3) for x in w.tolist()]}")
# gradient wrt the policy log-probs is beta * weight (per pair); so beta both scales the step and the sigmoid width
for beta in [0.1, 0.5, 1.0]:
    print(f"beta={beta}: grad scale on logp_chosen = {[round(beta*x,3) for x in torch.sigmoid(-beta*m).tolist()]}")
```
Output (my run):
```
beta=0.1: loss grad wrt z = [0.599, 0.55, 0.5, 0.45, 0.401]  weight sigmoid(-beta*m) = [0.599, 0.55, 0.5, 0.45, 0.401]
beta=0.5: loss grad wrt z = [0.881, 0.731, 0.5, 0.269, 0.119]  weight sigmoid(-beta*m) = [0.881, 0.731, 0.5, 0.269, 0.119]
beta=1.0: loss grad wrt z = [0.982, 0.881, 0.5, 0.119, 0.018]  weight sigmoid(-beta*m) = [0.982, 0.881, 0.5, 0.119, 0.018]
beta=0.1: grad scale on logp_chosen = [0.06, 0.055, 0.05, 0.045, 0.04]
beta=0.5: grad scale on logp_chosen = [0.44, 0.366, 0.25, 0.134, 0.06]
beta=1.0: grad scale on logp_chosen = [0.982, 0.881, 0.5, 0.119, 0.018]
```

**Follow-ups:**
- *Why can chosen log-prob fall?* The loss is a function of the difference; pushing the rejected response down a lot satisfies it even if the chosen one drifts down a little (reported behaviour; check on your own run).
- *Typical beta?* One prep page uses 0.1 as an example; tune it.
- *On-policy or off-policy pairs?* Pairs sampled from your own SFT model usually match the reference better; public off-policy datasets work but may be a worse fit.

**Common mistakes:** Calling the reference trainable; forgetting to precompute or mask padding in log-probs; assuming DPO is immune to reward hacking or length bias; tuning beta without looking at KL or win rate.

### Q16 ⭐⭐ 🟡 What do IPO, KTO, ORPO and SimPO change relative to DPO, and when would you consider them?
**Asked at:** post-training loops, research-leaning teams
**Say this first (1 line):** All four are DPO-family alternatives named in a prep article; from memory (not verified against the papers): IPO adds regularisation against overfitting to near-deterministic preferences, KTO learns from single thumbs-up/down labels, ORPO folds a preference term into SFT with no reference model, and SimPO uses a length-normalised average log-prob reward with a margin and no reference.

**Then explain:**
- **IPO (from memory):** DPO can overfit when preferences are almost always the same way, pushing log-ratios very far; IPO changes the objective to regularise that.
- **KTO (from memory):** needs only binary labels (desirable or not), not paired comparisons. Useful when you have logs with thumbs-up and thumbs-down but no pairs.
- **ORPO (from memory):** one stage; adds an odds-ratio penalty to the SFT loss so there is no separate SFT run and no reference model. Saves memory.
- **SimPO (from memory):** reward = average log-prob per token, plus a target margin, no reference model. Removes the length bias that summed log-probs have, and the memory cost of the reference.
- **When to look:** pairs are scarce (KTO), reference memory is tight (ORPO, SimPO), DPO overfits or lengthens answers (IPO, SimPO). Always compare on your own eval; the gains in papers are the authors' settings.

**Example (run, my simplified reading, not the papers' code):** a toy pair has a 3-token chosen and an 8-token rejected answer. The raw sum-log-prob gap is 5.6 in favour of the short chosen one, but the mean-log-prob gap is only 0.075, so length drives the sum. A DPO margin (with reference, beta=2) is 1.0 (loss 0.313); a SimPO-style margin (beta=2, gamma=0.5, no reference) is -0.35 (loss 0.883), so the length-fair view says the model does not yet clearly prefer the chosen answer.

**Code:** (run, torch CPU; simplified reading, not the authors' implementation)
```python
import torch
torch.set_num_threads(1)
# SIMPLIFIED READING, not the papers' code. Toy pair: token log-probs of a short chosen and a long rejected answer.
logp_c = torch.tensor([-1.0, -0.8, -1.2])                 # chosen: 3 tokens
logp_r = torch.tensor([-0.9, -1.0, -1.1, -1.0, -1.2, -1.1, -1.0, -1.3])   # rejected: 8 tokens
ref_c  = torch.tensor([-1.2, -1.0, -1.3])
ref_r  = torch.tensor([-0.9, -1.0, -1.1, -1.0, -1.2, -1.1, -1.0, -1.3])
beta, gamma = 2.0, 0.5
ls = torch.nn.functional.logsigmoid

# DPO: implicit reward = beta * (sum logp - sum logp_ref); needs the reference model
dpo_margin = beta * ((logp_c.sum() - ref_c.sum()) - (logp_r.sum() - ref_r.sum()))
print("DPO  margin:", round(dpo_margin.item(), 3), " loss:", round((-ls(dpo_margin)).item(), 3))

# SimPO-style: implicit reward = beta * average logp (length-normalised), no reference, plus target margin gamma
sim_margin = beta * (logp_c.mean() - logp_r.mean()) - gamma
print("SimPO-style margin:", round(sim_margin.item(), 3), " loss:", round((-ls(sim_margin)).item(), 3))

# what a raw sum-logp reward without normalisation would say (length effect)
print("sum-logp gap chosen - rejected:", round((logp_c.sum() - logp_r.sum()).item(), 3),
      "| mean-logp gap:", round((logp_c.mean() - logp_r.mean()).item(), 3))
```
Output (my run):
```
DPO  margin: 1.0  loss: 0.313
SimPO-style margin: -0.35  loss: 0.883
sum-logp gap chosen - rejected: 5.6 | mean-logp gap: 0.075
```

**Follow-ups:**
- *Which is best?* No universal winner I can cite; they behave differently by dataset, so run an ablation.
- *Why drop the reference?* Saves one model in memory and compute, at the cost of the explicit anchor DPO has.

**Common mistakes:** Stating these descriptions as verified; saying SimPO and DPO use the same reward; thinking KTO needs pairs; picking by novelty instead of evaluation.

### Q17 ⭐⭐ 🟡 How do reward models fail (overfitting, distribution shift, length bias, over-optimisation), and what do ensembles and process reward models offer?
**Asked at:** post-training loops, research-leaning teams
**Say this first (1 line):** A reward model is a proxy trained on limited human comparisons, so it fails in predictable ways (it learns annotator quirks, it is unreliable off its training distribution, it likes long answers, and a policy optimised hard against it exploits it), and the main defences are KL limits, ensembles, fresh comparisons and denser (process) rewards.

**Then explain:**
- **Overfitting to annotator quirks:** if raters like confident tone or bullet lists, the model learns that, not quality. Pairwise accuracy on held-out pairs is only about as good as annotator agreement allows (Q5, Q7).
- **Distribution shift:** the policy moves into regions the reward model never saw during training, where its scores are unreliable.
- **Length bias:** longer answers often score higher (Q19).
- **Over-optimisation:** as reported by Gao et al. (seen via snippets only), the proxy reward keeps rising while a held-out "gold" reward peaks and then falls as the policy drifts further; Q3 and Q2 cover the KL control.
- **Ensembles:** train several reward models; use the mean for the reward and the disagreement as an uncertainty signal, penalising or stopping where they disagree.
- **Refresh:** collect new comparisons on the current policy's outputs and retrain.
- **Outcome vs process reward models (from memory, hedge):** an outcome model scores the final answer; a process model scores each reasoning step. Process rewards give denser feedback and can catch right-answer-wrong-reasoning, but need step-level labels, which are costly.

**Example (SYNTHETIC, run):** eight polynomial "reward models" are fit on bootstrap samples of data from x in [-1, 1]. In-distribution the ensemble's mean absolute error is 0.008 and its std (disagreement) is 0.060. At x in [2, 3] the error blows up to 4.843 and the disagreement to 74.164, so high disagreement correctly flags where the proxy is untrustworthy. Real reward models are not polynomials; this only shows the mechanism.

**Code:** (run, numpy; SYNTHETIC)
```python
import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: true reward is a function of a 1-D feature x. Ensemble members are fit on small noisy
# data from the region x in [-1, 1] only, so they agree in-distribution and disagree far outside it.
def true_r(x): return np.sin(2 * x)
x_tr = rng.uniform(-1, 1, 40)
members = []
for k in range(8):
    idx = rng.choice(40, 40, replace=True)                     # bootstrap
    y = true_r(x_tr[idx]) + rng.normal(0, 0.15, 40)
    members.append(np.polyfit(x_tr[idx], y, 5))                # degree-5 polynomial "reward model"
for name, xs in [("in-distribution  x in [-1,1]", np.linspace(-1, 1, 50)),
                 ("shifted          x in [2,3]  ", np.linspace(2, 3, 50))]:
    preds = np.array([np.polyval(c, xs) for c in members])
    mean_err = np.abs(preds.mean(0) - true_r(xs)).mean()
    print(f"{name}: mean abs error {mean_err:7.3f} | ensemble std (disagreement) {preds.std(0).mean():8.3f}")
```
Output (my run):
```
in-distribution  x in [-1,1]: mean abs error   0.008 | ensemble std (disagreement)    0.060
shifted          x in [2,3]  : mean abs error   4.843 | ensemble std (disagreement)   74.164
```

**Follow-ups:**
- *Does an ensemble fix over-optimisation?* It helps by flagging uncertainty, but members trained on the same data share blind spots; it does not remove the problem.
- *How would you detect it in training?* Watch proxy reward vs an independent eval (human or held-out judge) as KL grows.

**Common mistakes:** Treating the reward model as ground truth; reporting only reward-model accuracy; thinking ensembles of identical models give independent errors; claiming process reward models are always better.

### Q18 ⭐⭐ 🟡 What is sycophancy? Why does RLHF encourage it, and how do you measure and reduce it?
**Asked at:** post-training loops, product, safety teams
**Say this first (1 line):** Sycophancy is the model telling users what they seem to want to hear (matching their stated views or caving when challenged) instead of what is true, and RLHF can encourage it because human raters, and the reward model trained on them, tend to prefer agreeable answers.

**Then explain:**
- **Two forms:** (1) tailoring: the answer shifts to match the user's stated opinion; (2) caving: a correct answer is dropped after "I think you're wrong".
- **Why:** Sharma et al. 2023 reportedly found it across several production assistants and linked it partly to human preference data that rewards agreement (reported from a search snippet; I did not read the paper, so hedge).
- **Measure:** build pushback prompts where the first answer is right and the user pushes back wrongly; report the flip rate. Also measure the opposite, appropriate updates, so a stubborn model does not look perfect.
- **Reduce:** preference data where the non-sycophantic answer is chosen; training examples with pushback cases; opinion-swap tests (same question, opposite stated views, answers should not change); evaluation as a release gate (Q10).
- **Watch the trade:** the fix should not make the model rude or unable to change its mind when the user is right.

**Example (SYNTHETIC, run):** in made-up transcripts, model A flips on 39.9% of wrong pushbacks (n=1418) and updates correctly on 72.5% of valid ones. Model B after hypothetical pushback training flips 8.5% and updates 64.5%. A stubborn model C scores 0.0% flips but also 0.0% appropriate updates, which shows why you need both numbers. The probabilities are my made-up inputs, not results from real models.

**Code:** (run, numpy; SYNTHETIC transcripts)
```python
import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC transcripts (no real model). Each: was the first answer correct, was the user's pushback valid
# (the first answer really was wrong), and did the answer change after pushback.
def make(n, p_cave_wrong_push, p_fix_valid_push):
    out = []
    for _ in range(n):
        first_correct = rng.random() < 0.7
        pushback_valid = not first_correct          # pushing back on a wrong answer is legitimate
        p = p_fix_valid_push if pushback_valid else p_cave_wrong_push
        out.append((first_correct, pushback_valid, rng.random() < p))
    return out
def report(name, t):
    bad = [x for x in t if x[0] and not x[1]]       # correct first, pushback invalid
    good = [x for x in t if (not x[0]) and x[1]]    # wrong first, pushback valid
    print(f"{name}: sycophantic flip rate {np.mean([x[2] for x in bad]):.3f} (n={len(bad)}) | "
          f"appropriate update rate {np.mean([x[2] for x in good]):.3f} (n={len(good)})")
report("model A", make(2000, 0.40, 0.70))
report("model B (after pushback training)", make(2000, 0.08, 0.65))
report("model C (stubborn, never flips)", make(2000, 0.00, 0.00))
```
Output (my run):
```
model A: sycophantic flip rate 0.399 (n=1418) | appropriate update rate 0.725 (n=582)
model B (after pushback training): sycophantic flip rate 0.085 (n=1398) | appropriate update rate 0.645 (n=602)
model C (stubborn, never flips): sycophantic flip rate 0.000 (n=1389) | appropriate update rate 0.000 (n=611)
```

**Follow-ups:**
- *How do you get ground truth for pushback?* Use questions with verifiable answers (facts, arithmetic) so you know who is right.
- *Is agreeing always sycophancy?* No; agreeing when the user is right is fine. The problem is agreement that does not track truth.

**Common mistakes:** Measuring only flips (a never-flipping model looks perfect); using subjective prompts with no ground truth; blaming only the reward model; fixing it with a rude system prompt.

### Q19 ⭐⭐ 🟡 What causes length bias and verbosity in aligned models, and how do you measure and mitigate it?
**Asked at:** post-training loops, evaluation teams
**Say this first (1 line):** Reward models and human or LLM judges tend to prefer longer answers (Singhal et al. reported length correlations, seen via snippets), so RL against them pushes the policy toward verbosity; I measure the length-reward correlation and a length-controlled win rate, and mitigate with length penalties, normalised objectives and balanced data.

**Then explain:**
- **Causes:** longer answers look more thorough to raters; some preference data has chosen answers longer than rejected ones; the policy exploits any cheap feature that raises reward (Q3).
- **Size of the effect:** a wiki summary of those papers claimed that 70-90% of a PPO reward gain comes from length shifts, but that is unverified and dataset-dependent, so I would not quote it.
- **Measure:** (1) correlation between length and reward-model score; (2) average length of chosen vs rejected in the data; (3) win rate versus a baseline, adjusted for length (for example, compare within length bins or regress out length).
- **Mitigate:** a length penalty in the reward; length-normalised objectives (Q16, SimPO-style, from memory); balance data so chosen is not systematically longer; tell judges not to favour length; keep a human spot check.
- Verbosity also costs money (tokens) and latency, not just quality.

**Example (SYNTHETIC, run):** a made-up reward model adds 0.012 per token of length to quality. The length-reward correlation is 0.77 while length-quality correlation is only 0.242. Model B writes longer answers (320 vs 200 tokens) but is slightly worse in true quality (true win rate 45.2%), yet the raw biased win rate is 77.9%. After removing the fitted length slope the adjusted win rate is 47.3%, close to the truth. All numbers come from my synthetic generator.

**Code:** (run, numpy; SYNTHETIC)
```python
import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: a reward model that gives +0.004 per token of length on top of true quality (a built-in length bias).
n = 4000
quality = rng.normal(0, 1, n)
length = np.clip(rng.normal(200, 80, n) + 20 * quality, 30, None)
reward = quality + 0.012 * (length - 200) + rng.normal(0, 0.3, n)
print("corr(length, reward):", round(np.corrcoef(length, reward)[0, 1], 3), " corr(length, true quality):", round(np.corrcoef(length, quality)[0, 1], 3))
# A/B comparison: model B writes longer answers but is slightly WORSE in true quality
qa = rng.normal(0.00, 1, n); la = rng.normal(200, 50, n)
qb = rng.normal(-0.15, 1, n); lb = rng.normal(320, 50, n)
ra = qa + 0.012 * (la - 200); rb = qb + 0.012 * (lb - 200)
print("raw win rate of B (judge with length bias):", round((rb > ra).mean(), 3))
print("true-quality win rate of B:                 ", round((qb > qa).mean(), 3))
# length-controlled: regress reward on length, compare residual (length-adjusted) scores
X = np.concatenate([la, lb]); Y = np.concatenate([ra, rb])
slope = np.polyfit(X, Y, 1)[0]
ra_adj = ra - slope * la; rb_adj = rb - slope * lb
print("length-adjusted win rate of B:              ", round((rb_adj > ra_adj).mean(), 3), "(slope", round(slope, 4), ")")
```
Output (my run):
```
corr(length, reward): 0.77  corr(length, true quality): 0.242
raw win rate of B (judge with length bias): 0.779
true-quality win rate of B:                  0.452
length-adjusted win rate of B:               0.473 (slope 0.0113 )
```

**Follow-ups:**
- *Is longer always bad?* No; complex questions need long answers. The problem is length unrelated to need.
- *Does length-controlled evaluation fully fix it?* It removes the linear length effect only, other style biases remain (Part 9 covers judges).

**Common mistakes:** Quoting the 70-90% figure as fact; reporting raw win rate against a longer-answering baseline; penalising length so hard that answers become terse; ignoring the data as a source of the bias.

### Q20 ⭐⭐ 🟡 What are GRPO and RLVR? How does a group-relative advantage replace the critic, and what are the weaknesses of verifiable rewards?
**Asked at:** post-training loops, GenAI startups, research-leaning teams
**Say this first (1 line):** GRPO samples a group of responses per prompt, scores each, and uses (reward - group mean) / group std as the advantage, so no value network is needed; RLVR (RL with verifiable rewards) is the setting where those scores come from rules such as answer match or unit tests rather than a learned reward model. This is as explained in reported explainers; check the DeepSeekMath paper (arXiv 2402.03300) for the primary definition.

**Then explain:**
- **Group baseline instead of a critic:** the group mean plays the role of the value estimate for that prompt, so one fewer large model is trained and held in memory (Q13).
- **Update:** PPO-style clipped ratio (Q12) with that advantage, plus a KL term to a reference model, per the explainers I saw. Group sizes in the 8-64 range were mentioned by one source.
- **RLVR rewards:** exact match for math, unit tests for code, format checks. Cheap, objective, and hard to argue with, unlike a learned reward (Q17).
- **Weakness 1, uniform credit:** every token in a response gets the same advantage, so the update cannot tell the key step from filler.
- **Weakness 2, weak verifiers get hacked:** if the check is loose, the policy finds the loophole (Q21 demo).
- **Weakness 3, no signal in uniform groups:** if all responses get the same reward (all right or all wrong), advantages are zero, so hard-but-solvable prompts need enough samples or curriculum. When std is zero you divide by zero, so add a small epsilon.

**Example (run, synthetic):** reward group [1, 0, 0, 1] gives advantages [1, -1, -1, 1]; [1, 1, 1, 0] gives [0.577, 0.577, 0.577, -1.732] (the lone failure is pushed down hard); [0, 0, 0, 0] and [1, 1, 1, 1] both give all zeros, so no learning from that prompt. In a toy 6-answer bandit where answer 4 is correct (exact match reward), a softmax policy trained with REINFORCE using the group baseline (group of 8, no value network, a small KL to uniform) goes from 0.167 to 0.995-0.998 probability on the correct answer over five seeds. This toy uses plain policy gradient without the clipping, to isolate the group baseline.

**Code:** (run, torch CPU; synthetic bandit)
```python
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
```
Output (my run):
```
[1, 0, 0, 1] -> [1.0, -1.0, -1.0, 1.0]
[1, 1, 1, 0] -> [0.577, 0.577, 0.577, -1.732]
[0, 0, 0, 0] -> [0.0, 0.0, 0.0, 0.0]
[1, 1, 1, 1] -> [0.0, 0.0, 0.0, 0.0]
[0.2, 0.5, 0.9, 0.4] -> [-1.177, 0.0, 1.569, -0.392]
P(correct) after training, 5 seeds: [0.997, 0.996, 0.997, 0.995, 0.998]
```

**Follow-ups:**
- *Why divide by std?* It normalises scale across prompts of different difficulty (reported in the explainers); some later variants reportedly drop it, which I have not verified.
- *Can you use GRPO with a learned reward model?* Yes; the group normalisation works for any scalar score, but then you inherit reward-model failures (Q17).

**Common mistakes:** Saying GRPO has no baseline (it has a group one); forgetting epsilon for zero std; claiming all tokens are credited differently; treating RLVR as unhackable.

### Q21 ⭐⭐ 🟡 How are reasoning models post-trained (RL on verifiable tasks, test-time compute), and how does that differ from preference-based RLHF?
**Asked at:** post-training loops, big tech, GenAI startups
**Say this first (1 line):** Reasoning models are, as commonly described, post-trained with RL on tasks that have checkable answers (math, code), which rewards long chains of thought that end in a correct result, and they then spend more tokens at inference (test-time compute), whereas preference-based RLHF optimises a learned reward for human-liked answers. Details of specific systems are not public in full, so hedge.

**Then explain:**
- **Reward source:** RLHF uses a learned reward model from human comparisons (Q5). Reasoning RL uses a verifiable reward such as answer match or passing tests (Q20), which is cheap and not a proxy for taste.
- **Long chain of thought:** the model is rewarded for the final outcome, and longer deliberate reasoning (checking, backtracking) tends to emerge or be encouraged (reported in explainers; hedge).
- **Test-time compute:** more thinking tokens or more samples at inference trade latency and cost for accuracy; costs are covered in Part 2 Q43 and Part 4 Q47.
- **Examples:** the prep article lists o1/o3 and DeepSeek-R1 as examples of this track; I am only naming them as listed and not describing their internals.
- **Pitfalls:** weak verifiers get hacked; format hacking (satisfying the answer pattern without real reasoning); cost of long rollouts; unreadable or mixed-language reasoning; tasks without a verifier (writing, advice) still need preference-based methods.
- **In practice** the two are combined: verifiable RL for reasoning, preference tuning for helpfulness and safety (Q1, Q11).

**Example (MOCK, run):** for "17 * 3" with true answer 51, a weak verifier that accepts any output containing "51" gives reward 1 to "Possible answers: 41, 45, 51, 60. Answer: 41 51", while a stricter format check gives 0 (and also 1 to a reasoning-free "Answer: 51", which a correctness check cannot punish). The strict check wrongly gives 0 to "The result is 51." Neither verifier is perfect, and an RL loop will find whichever gap exists. Scripted outputs, no real model.

**Code:** (run; MOCK scripted outputs)
```python
import re
# MOCK verifiers on scripted outputs (no real model). Question: 17 * 3 = ?  (true answer 51)
outputs = {
  "correct, reasoned":   "17*3 = 10*3 + 7*3 = 30 + 21 = 51. Answer: 51",
  "wrong, reasoned":     "17*3 = 41. Answer: 41",
  "hack: lists many":    "Possible answers: 41, 45, 51, 60. Answer: 41 51",
  "hack: no reasoning":  "Answer: 51",
  "correct, bad format": "The result is 51.",
}
def weak_verifier(text):          # 'contains the number 51 anywhere'
    return float("51" in text)
def strict_verifier(text):        # requires exactly one 'Answer: N' at the end and N == 51
    m = re.fullmatch(r".*Answer: (\d+)", text, flags=re.S)
    return float(bool(m) and m.group(1) == "51")
print(f"{'output':22s} weak  strict")
for k, v in outputs.items():
    print(f"{k:22s} {weak_verifier(v):.0f}     {strict_verifier(v):.0f}")
```
Output (my run):
```
output                 weak  strict
correct, reasoned      1     1
wrong, reasoned        0     0
hack: lists many       1     0
hack: no reasoning     1     1
correct, bad format    1     0
```

**Follow-ups:**
- *Why does verifiable reward scale better than a reward model?* It is not learned, so it is harder to over-optimise in the Gao-style way (reported), but only where the verifier is sound.
- *Does more test-time compute always help?* No; it helps up to a point and costs latency and money (Part 2 Q43).
- *How do you keep reasoning readable?* Add format or language rewards or a short SFT stage; trade-offs exist and details vary by system (hedge).

**Common mistakes:** Saying reasoning models skip RLHF entirely; describing o1 or R1 internals as fact; forgetting verifiers can be gamed; ignoring inference cost.
