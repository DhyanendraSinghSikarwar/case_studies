### Q1 ⭐⭐⭐ 🟢 What is RLHF? Walk through the pipeline (SFT, reward model, policy optimisation) and explain why a base LLM needs it.
**Asked at:** all types; post-training and GenAI-engineer loops
**Say this first (1 line):** RLHF (reinforcement learning from human feedback) is a three-step recipe: fine-tune on good demonstrations (SFT), train a reward model on human comparisons of outputs, then optimise the model with RL (usually PPO) to score high on that reward model while a KL penalty keeps it close to the SFT model.

**Then explain:**
- **Why a base model needs it:** a pretrained model predicts the next token on web text. It continues text, it does not follow intent. "Be helpful, honest, harmless" is not what the pretraining loss measures.
- **Step 1, SFT:** train on labeller-written demonstrations of good answers. This gives a sensible starting policy (SFT itself is Part 4 Q2).
- **Step 2, reward model:** show labellers several outputs for a prompt, collect rankings or comparisons, and train a model that outputs a scalar score so preferred answers score higher (Q5).
- **Step 3, RL:** sample responses from the policy, score them with the reward model, update with PPO. The reward is shaped with a KL penalty against the SFT reference so the policy cannot drift into reward-model exploits (Q2, Q3).
- **Sourced result (InstructGPT abstract):** SFT on labeller demonstrations, then RLHF on rankings. Human raters preferred outputs from the 1.3B InstructGPT over the 175B GPT-3 on the authors' prompt distribution, with improved truthfulness, less toxic output and minimal regressions on public NLP datasets. That is the authors' result on their prompts, not a universal law.
- **SFT and RLHF are sequential, not alternatives.** RLHF starts from the SFT model.
- **Where it fails:** noisy or inconsistent labels, reward hacking (Q3), expensive human data, a reward model that generalises poorly outside its training distribution, and a complex, unstable RL loop.

**Example:** Prompt: "Explain compound interest to a teenager." A base model might continue with a textbook definition or more quiz questions. After SFT it answers in a helpful tone. For RLHF we sample 4 answers, labellers rank them (short and clear beats long and jargon-heavy), the reward model learns that taste, and PPO nudges the policy toward answers the reward model scores higher, within a KL leash to the SFT model.

**Code:** not needed for this conceptual question; the pieces are runnable in Q2 (KL-shaped objective), Q5 (reward model) and Q6 (DPO loss).

**Follow-ups:**
- *Why not just do more SFT?* SFT copies demonstrations; comparisons are easier to give than perfect answers, and RL can optimise beyond the demonstrations. SFT quality still matters a lot.
- *Why the reference model?* To stop the policy exploiting the reward model and producing gibberish that scores high (Q2).
- *Is PPO required?* No; DPO and other methods skip the explicit RL loop (Q4).

**Common mistakes:** Presenting SFT and RLHF as alternatives; forgetting the KL term; saying the reward model is "the human" (it is a learned, imperfect proxy); quoting InstructGPT as proof that RLHF always makes a small model beat a large one.

### Q2 ⭐⭐⭐ 🟢 What is the KL penalty in RLHF, why is it needed, and what does the beta coefficient trade off?
**Asked at:** all types; post-training loops
**Say this first (1 line):** The KL penalty subtracts beta times the KL divergence between the current policy and the frozen reference (SFT) model from the reward, so the policy is rewarded for scoring high but charged for moving away from the reference.

**Then explain:**
- **Shaped reward:** r_total(x, y) = r(x, y) - beta * KL(pi || pi_ref). In practice it is estimated per token on sampled responses: sum over tokens of beta * (log pi(token) - log pi_ref(token)).
- **Why needed:** the reward model is a proxy that is only reliable near the data it was trained on. Without a leash the policy finds odd outputs the reward model overrates (reward hacking, Q3) and also loses fluency and diversity.
- **Beta is a dial:** too low means little protection, reward rises but quality can collapse; too high means the policy barely moves from SFT and you wasted the RL step.
- **Closed form for the toy:** maximising E[r] - beta*KL gives pi*(y) proportional to pi_ref(y) * exp(r(y)/beta). Small beta makes the exponent large and sharpens onto the highest-reward choice.
- **No universal beta:** it is tuned per setup by watching reward, KL and held-out quality together. Some write-ups quote values like 0.1, but treat that as an example.

**Example:** In the toy below with 4 tokens, at beta=10 the best policy is nearly the reference (KL 0.000, expected reward 0.27). At beta=0.3 it shifts mass to the high-reward token (KL 0.79, reward 0.71). At beta=0.05 it collapses to one token (KL 2.30, reward 1.00), which is exactly what the penalty is meant to prevent in a real model.

**Code:** (run; TOY, a 4-token vocabulary, not an LLM)
```python
import math
# TOY: 4-token vocabulary, one prompt. Not an LLM.
ref   = [0.40, 0.30, 0.20, 0.10]           # reference policy
reward = [0.0, 0.2, 0.5, 1.0]              # proxy reward per token (toy)
def kl(p, q): return sum(a*math.log(a/b) for a, b in zip(p, q) if a > 0)
def softmax(z):
    m = max(z); e = [math.exp(v-m) for v in z]; s = sum(e); return [v/s for v in e]
# Penalised objective J(pi) = E_pi[r] - beta*KL(pi||ref). Closed-form optimum: pi* ∝ ref * exp(r/beta)
for beta in [10.0, 1.0, 0.3, 0.05]:
    pi = softmax([math.log(p)+r/beta for p, r in zip(ref, reward)])
    er = sum(p*r for p, r in zip(pi, reward)); k = kl(pi, ref)
    print(f"beta={beta:5.2f}  pi*={[round(p,3) for p in pi]}  E[r]={er:.3f}  KL={k:.3f}  J={er-beta*k:.3f}")
# per-token sample estimate of KL: mean over samples of log pi(y) - log ref(y)
import random; random.seed(0)
pi = softmax([math.log(p)+r/0.3 for p, r in zip(ref, reward)])
ys = random.choices(range(4), weights=pi, k=20000)
print("exact KL", round(kl(pi, ref),3), " sampled estimate", round(sum(math.log(pi[y]/ref[y]) for y in ys)/len(ys),3))
```
Output (my run):
```
beta=10.00  pi*=[0.39, 0.298, 0.205, 0.108]  E[r]=0.270  KL=0.000  J=0.265
beta= 1.00  pi*=[0.292, 0.268, 0.241, 0.199]  E[r]=0.373  KL=0.059  J=0.313
beta= 0.30  pi*=[0.083, 0.121, 0.218, 0.578]  E[r]=0.712  KL=0.794  J=0.473
beta= 0.05  pi*=[0.0, 0.0, 0.0, 1.0]  E[r]=1.000  KL=2.302  J=0.885
exact KL 0.794  sampled estimate 0.792
```

**Follow-ups:**
- *Is it the same KL as in DPO?* DPO's beta plays the same role: it scales the implicit reward beta*log(pi/pi_ref) (Q6).
- *Why KL(pi || ref) and not the reverse?* It can be estimated from samples drawn from the current policy, which is what RL has.
- *Can you adapt beta?* Some implementations adapt it toward a target KL; details vary, check the framework you use.

**Common mistakes:** Saying a higher beta gives more reward (it does the opposite); forgetting the reference is frozen; treating the KL as a loss on logits rather than a term in the reward; confusing the penalty with a hard constraint.

### Q3 ⭐⭐⭐ 🟢 What is reward hacking? Give examples (length bias, sycophancy) and the standard mitigations.
**Asked at:** all types; post-training loops
**Say this first (1 line):** Reward hacking is the policy exploiting flaws in the reward model, getting a higher proxy score without actually getting better; it is Goodhart's law: when a measure becomes the target, it stops being a good measure.

**Then explain:**
- **Shape of the problem:** as the policy moves further from the reference (higher KL), the proxy reward keeps rising, but true quality rises, peaks and then falls. Gao et al. are reported to show this with a gold reward model; I have only seen summaries of that paper, so treat the details as reported.
- **Length bias:** longer answers often look more thorough, and reward models can learn that. The policy then pads. Singhal et al. are reported to find strong length correlations in RLHF reward gains; I would not quote a specific percentage.
- **Sycophancy:** if raters like agreement, the policy learns to agree with the user's wrong claim. Sharma et al. are reported to find this in several production assistants.
- **Other forms:** formatting tricks (bullets, confident tone), refusing too much because refusals are rarely penalised (Q11), and exploiting a code reward by special-casing tests.
- **Mitigations:** KL penalty and early stopping (Q2); refresh or ensemble reward models; length control (normalise or penalise length, compare at matched length); constitutional or rule-based rewards (Q14); held-out human checks on fresh prompts, not just the reward curve; red-team the reward model.

**Example:** In my synthetic demo, true utility is quality minus a penalty for padding beyond about 10 units; the proxy adds a bonus for length. Best-of-n on the proxy (more n means more optimisation, larger KL) raises the proxy from 2.5 to 7.6, but true utility peaks near n=4 (-0.23) and then falls to -3.48 as answers grow from 10 to 20 length units.

**Code:** (run; SYNTHETIC, quality and length are random numbers, no LLM)
```python
import numpy as np
# SYNTHETIC demo of reward hacking (no real LLM). Each candidate response has quality q and length l (independent).
# True utility   = q - 0.05*max(0, l-10)^2   (padding past ~10 hurts the reader)
# Proxy reward   = q + 0.25*l                (a reward model with a length bias)
# "Optimising" = best-of-n on the proxy; more n = more optimisation = larger KL from the reference sampler
# (analytic KL of best-of-n vs the base distribution: log n - (n-1)/n).
rng = np.random.default_rng(0)
N = 400000
q = rng.normal(0, 1, N); l = np.clip(rng.normal(10, 4, N), 1, None)
true = q - 0.05*np.maximum(0, l-10)**2
proxy = q + 0.25*l
print(f"{'n':>6} {'KL':>6} {'proxy':>7} {'true':>7} {'avg len':>8}")
for n in [1, 2, 4, 16, 64, 256, 1024, 4096]:
    k = N//n
    idx = np.arange(k*n).reshape(k, n)
    pick = idx[np.arange(k), proxy[idx].argmax(1)]
    print(f"{n:6d} {np.log(n)-(n-1)/n:6.2f} {proxy[pick].mean():7.2f} {true[pick].mean():7.2f} {l[pick].mean():8.1f}")
```
Output (my run):
```
     n     KL   proxy    true  avg len
     1   0.00    2.51   -0.40     10.0
     2   0.19    3.30   -0.24     11.6
     4   0.64    3.95   -0.23     12.9
    16   1.84    4.99   -0.50     15.0
    64   3.17    5.81   -1.04     16.6
   256   4.55    6.48   -1.73     18.0
  1024   5.93    7.07   -2.73     19.4
  4096   7.32    7.62   -3.48     20.4
```

**Follow-ups:**
- *How do you detect it?* Watch proxy vs held-out human or independent-judge scores, response length drift and KL; a rising reward with flat human scores is the signal.
- *Does DPO avoid it?* No; it can still over-fit preference quirks, and papers are reported to show over-optimisation there too.
- *Is length always bad?* No, sometimes longer is better; the problem is length rewarded independently of quality.

**Common mistakes:** Believing a rising reward curve means a better model; fixing it only with a bigger beta; calling any bad output reward hacking without showing the proxy-vs-true gap; quoting percentages from papers you have not read.

### Q4 ⭐⭐⭐ 🟡 DPO vs PPO-based RLHF: how does DPO work, what does it remove, and when would you pick each?
**Asked at:** all types; post-training loops
**Say this first (1 line):** DPO (Direct Preference Optimization) trains the policy directly on preference pairs with a simple classification-style loss, so it removes the separate reward model, the RL loop and sampling during training, while PPO-based RLHF keeps all three.

**Then explain:**
- **What DPO does (per the abstract):** it reparameterises the reward so the optimal policy of the KL-regularised objective has a closed form, which lets you optimise the policy with a classification loss on (chosen, rejected) pairs. The reward is implicit: beta * log(pi/pi_ref) (loss in Q6).
- **Claim:** the authors report that it matches or beats PPO-based RLHF on sentiment control, summarisation and single-turn dialogue. Those are the authors' claims on those tasks, not a guarantee for your model.
- **DPO strengths:** simpler, cheaper, more stable, easy to run with ordinary fine-tuning infrastructure.
- **DPO limits:** it learns from a fixed offline dataset, so there is no online exploration of new outputs; it depends on good preference pairs, ideally close to the policy's own distribution; it can be sensitive to beta and data quality.
- **PPO strengths:** it can use fresh on-policy samples and an explicit reward model, which can also be reused for filtering or best-of-n and can take non-preference rewards. Cost: more moving parts (policy, reference, reward model, usually a value head), more memory, more instability.
- **Who uses what:** a prep article claims open-source fine-tunes commonly use DPO while frontier labs use PPO. That is a claim I could not verify, so I would not state it as fact.

**Example:** A startup with 30k preference pairs from its product logs and one GPU node would start with DPO on its SFT model. A team with a verifiable reward (code tests) or a strong reward model and a need to keep improving on fresh samples would consider online RL.

**Code:** not needed here; the loss is implemented and tested in Q6.

**Follow-ups:**
- *Is DPO really "RL-free"?* It avoids an RL loop, but it still has an implicit reward and a KL-style reference anchor.
- *Can you do DPO online?* Yes, variants sample new pairs from the current policy and label them; I would describe that as a hybrid.
- *What if pairs are off-distribution?* The gradient is less informative; sample pairs from the SFT model (Q7).

**Common mistakes:** Saying DPO has no reference model (it needs the reference log-probs); claiming DPO always beats PPO; stating the open-source-vs-frontier split as fact; ignoring data quality.

### Q5 ⭐⭐⭐ 🟡 How is a reward model trained? Explain preference pairs, the Bradley-Terry loss and the architecture.
**Asked at:** post-training loops, research-leaning teams
**Say this first (1 line):** A reward model is the language model with a scalar head, trained on (prompt, chosen, rejected) pairs so that the chosen response scores higher, using the Bradley-Terry loss -log sigmoid(r_chosen - r_rejected).

**Then explain:**
- **Data:** for each prompt, labellers compare or rank outputs; a ranking of k outputs gives pairs.
- **Model:** usually initialised from the SFT model, with the vocabulary head replaced by a linear layer that maps the final hidden state (often at the last token) to one number.
- **Bradley-Terry:** assume P(chosen beats rejected) = sigmoid(r_chosen - r_rejected). Maximising the likelihood of labels gives the loss above. Only the score difference matters, so adding any constant to all rewards changes nothing; reward values have no absolute meaning.
- **Metric:** pairwise accuracy on held-out pairs. Labels are noisy, so even the best scorer cannot reach 100% (see the ceiling in the toy).
- **Pitfalls:** it is a proxy and can be hacked (Q3), can be biased to length, and generalises poorly off its training distribution.

**Example:** In my synthetic run the linear reward started at 0.646 test pairwise accuracy (random weights) and reached 0.89 after training, against a ceiling of 0.896 for the true utility because labels were sampled with noise. Adding +5 to every reward left the loss at 0.256.

**Code:** (run; SYNTHETIC features, a linear model stands in for "LM + scalar head")
```python
import torch
torch.set_num_threads(1); torch.manual_seed(0)
# SYNTHETIC: each response = 8 features. Hidden true utility w_true. Labeller prefers higher utility with Bradley-Terry noise.
d, n = 8, 4000
w_true = torch.randn(d)
def pairs(n):
    a, b = torch.randn(n, d), torch.randn(n, d)
    p_a = torch.sigmoid((a - b) @ w_true)               # P(a preferred) under BT
    a_wins = torch.rand(n) < p_a
    chosen = torch.where(a_wins[:, None], a, b); rejected = torch.where(a_wins[:, None], b, a)
    return chosen, rejected
Ctr, Rtr = pairs(n); Cte, Rte = pairs(2000)
rm = torch.nn.Linear(d, 1, bias=False)                  # stands in for "LM + scalar head"
opt = torch.optim.Adam(rm.parameters(), lr=0.05)
def acc(C, R): return (rm(C) > rm(R)).float().mean().item()
print("before: test pairwise acc", round(acc(Cte, Rte), 3))
for step in range(200):
    loss = -torch.nn.functional.logsigmoid(rm(Ctr) - rm(Rtr)).mean()
    opt.zero_grad(); loss.backward(); opt.step()
print("after : train loss", round(loss.item(), 3), "test pairwise acc", round(acc(Cte, Rte), 3))
# ceiling: the true utility itself, noisy labels cap accuracy
print("ceiling (true w) test acc", round(((Cte @ w_true) > (Rte @ w_true)).float().mean().item(), 3))
# shift invariance: adding a constant to every reward leaves the loss unchanged
s = rm(Ctr) - rm(Rtr); print("loss with +5 shift:", round(-torch.nn.functional.logsigmoid((rm(Ctr)+5) - (rm(Rtr)+5)).mean().item(), 3))
```
Output (my run):
```
before: test pairwise acc 0.646
after : train loss 0.256 test pairwise acc 0.89
ceiling (true w) test acc 0.896
loss with +5 shift: 0.256
```

**Follow-ups:**
- *Why pairwise and not absolute scores?* People are more consistent comparing than rating on a scale.
- *How do you handle ties?* Drop them, or use a soft label; implementations differ.
- *How do you evaluate a reward model beyond accuracy?* Check agreement with held-out humans on new prompts, length correlation, and whether policy gains survive human review.

**Common mistakes:** Treating reward values as calibrated probabilities; forgetting only differences matter; training and evaluating on pairs from the same prompts; ignoring that label noise caps accuracy.

### Q6 ⭐⭐⭐ 🟡 Code: implement the DPO loss in PyTorch (log-probability ratios against a reference model, beta, implicit rewards) and test it on toy tensors.
**Asked at:** product, big tech, post-training coding rounds
**Say this first (1 line):** DPO loss = -log sigmoid(beta * ((logp_policy(y_w) - logp_ref(y_w)) - (logp_policy(y_l) - logp_ref(y_l)))), where each logp is the sum of token log-probs over the response only, and the reference is frozen.

**Then explain:**
- **Sequence log-prob:** sum per-token log-probs over response tokens; mask out prompt and padding.
- **Reference:** compute under torch.no_grad() (or precompute it); only the policy gets gradients.
- **Implicit reward:** beta * (logp_policy - logp_ref) per response; the loss is the logistic loss on the reward margin.
- **Sanity tests:** policy equal to reference gives log 2 = 0.6931; raising chosen and lowering rejected log-probs lowers the loss; changing masked tokens changes nothing; a reversed preference gives a higher loss.
- **Practical:** use logsigmoid for stability; length matters because log-probs are sums (this is why length-normalised variants exist).

**Example:** With made-up log-probs for 2 sequences, policy equals reference gives 0.6931. Raising chosen response log-probs by 0.3 per token and lowering rejected ones by 0.3 (3 response tokens each, so a margin of 1.8 in sequence log-prob) with beta=0.1 gives loss 0.6072 and implicit rewards of +0.09 and -0.09.

**Code:** (run; made-up tensors, no model)
```python
import math, torch
import torch.nn.functional as F
torch.set_num_threads(1)

def seq_logp(token_logps, mask):
    """Sum per-token log-probs over response tokens only (mask=1 on response, 0 on prompt/padding)."""
    return (token_logps * mask).sum(-1)

def dpo_loss(pol_w, pol_l, ref_w, ref_l, beta=0.1):
    """All inputs: sequence log-probs, shape (B,). ref_* must be computed under no_grad (frozen reference)."""
    chosen_reward = beta * (pol_w - ref_w)        # implicit reward of chosen
    rejected_reward = beta * (pol_l - ref_l)
    loss = -F.logsigmoid(chosen_reward - rejected_reward).mean()
    return loss, chosen_reward.detach(), rejected_reward.detach()

# made-up per-token log-probs, batch 2, 5 positions; first 2 positions are the prompt
mask = torch.tensor([[0, 0, 1, 1, 1]] * 2, dtype=torch.float)
ref_w_tok = torch.tensor([[-1., -1., -2., -1.5, -2.], [-1., -1., -1., -2., -2.]])
ref_l_tok = torch.tensor([[-1., -1., -2., -2.5, -2.], [-1., -1., -3., -2., -1.]])

# test 1: policy == reference -> loss = log 2
with torch.no_grad():
    rw, rl = seq_logp(ref_w_tok, mask), seq_logp(ref_l_tok, mask)
l0, _, _ = dpo_loss(rw.clone(), rl.clone(), rw, rl)
print("policy==ref loss:", round(l0.item(), 4), "log2:", round(math.log(2), 4))

# test 2: raise chosen log-prob (and lower rejected) -> loss falls, gradient pushes the right way
pw = (ref_w_tok + 0.3 * mask).clone().requires_grad_(True)
pl = (ref_l_tok - 0.3 * mask).clone().requires_grad_(True)
l1, cr, rr = dpo_loss(seq_logp(pw, mask), seq_logp(pl, mask), rw, rl)
l1.backward()
print("after widening the gap:", round(l1.item(), 4), "| implicit rewards chosen/rejected:", cr.tolist(), rr.tolist())
print("grad on chosen tokens negative (loss falls if logp rises):", bool((pw.grad[:, 2:] < 0).all()),
      "| grad on rejected positive:", bool((pl.grad[:, 2:] > 0).all()))

# test 3: masked tokens do not matter
pw2 = ref_w_tok.clone(); pw2[:, :2] += 5.0       # change prompt-position log-probs only
l2, _, _ = dpo_loss(seq_logp(pw2, mask), rl.clone(), rw, rl)
print("changing masked (prompt) tokens changes nothing:", torch.allclose(l2, l0))

# test 4: loss falls the wrong way when the gap is reversed
l3, _, _ = dpo_loss(rw - 1.0, rl + 1.0, rw, rl)
print("reversed preference loss:", round(l3.item(), 4), "> log2:", l3.item() > math.log(2))
```
Output (my run):
```
policy==ref loss: 0.6931 log2: 0.6931
after widening the gap: 0.6072 | implicit rewards chosen/rejected: [0.0899999663233757, 0.0899999663233757] [-0.0899999663233757, -0.0899999663233757]
grad on chosen tokens negative (loss falls if logp rises): True | grad on rejected positive: True
changing masked (prompt) tokens changes nothing: True
reversed preference loss: 0.7981 > log2: True
```

**Follow-ups:**
- *Where does the reference log-prob come from in real code?* A frozen copy of the SFT model, run under no_grad, or precomputed once.
- *What does beta do?* Scales the implicit reward; lower beta lets the policy move further from the reference (Q2).
- *Why can chosen log-prob fall even as loss falls?* The loss only cares about the margin; both can drop. That is a known behaviour worth monitoring.

**Common mistakes:** Averaging instead of summing token log-probs without saying so; forgetting the mask; letting gradients flow through the reference; using log(sigmoid(x)) directly (unstable); flipping the sign.

### Q7 ⭐⭐⭐ 🟡 How do you collect high-quality preference data (guidelines, annotator agreement, pair sampling, AI feedback)?
**Asked at:** post-training loops, data-platform teams
**Say this first (1 line):** Cover the prompt distribution you care about, sample diverse candidate responses from your own model, give annotators written guidelines with gold examples, measure agreement, and version everything; add AI feedback to scale but audit it with humans.

**Then explain:**
- **Prompts:** sample real-use categories (and edge cases, safety, multi-turn) rather than only easy prompts; track coverage by category.
- **Pair sampling:** draw several responses per prompt from the SFT model at different temperatures (or from different models), drop duplicates, and pick pairs with meaningful differences. Near-identical pairs give noisy labels; pairs from a very different model are off-policy. Randomise slot order to avoid position bias.
- **Guidelines:** write what helpful, honest and harmless mean with examples and tie-break rules; revise after disagreements, and keep a version number on each label.
- **Quality control:** gold items with known answers, calibration rounds, redundancy (2 to 3 annotators on a subset) and agreement statistics (Q31); review outliers.
- **AI feedback (RLAIF):** a model labels pairs against a written constitution or rubric (Q14); cheaper and more consistent, but inherits judge biases, so spot-check against humans.
- **Governance:** privacy (strip personal data, consent for user logs), annotator wellbeing for harmful content, and data versioning so you can reproduce a model.

**Example:** For 3 prompts, 2 temperatures and 4 samples each, I draw 2 pairs per prompt from the unique responses, shuffle which one appears as A, and attach the guideline version and the number of annotators. The sketch below produced 6 pairs.

**Code:** (run; the generator is a MOCK, not a language model)
```python
import random, itertools
# MOCK generator: stands in for sampling an SFT model. No real LLM.
def mock_generate(prompt, temperature, seed):
    rng = random.Random(f"{prompt}|{temperature}|{seed}")
    n_words = rng.randint(5, 12)
    return f"[{prompt[:12]}..] " + " ".join(rng.choice(["alpha","beta","gamma","delta","eps"]) for _ in range(n_words))

def sample_pairs(prompts, temps=(0.7, 1.0), k=4, pairs_per_prompt=2, seed=0):
    rng = random.Random(seed); out = []
    for p in prompts:
        cands = [dict(text=mock_generate(p, t, s), temp=t) for t in temps for s in range(k)]
        uniq = {c["text"]: c for c in cands}.values()               # drop exact duplicates
        uniq = list(uniq)
        combos = [(a, b) for a, b in itertools.combinations(uniq, 2)]
        for a, b in rng.sample(combos, min(pairs_per_prompt, len(combos))):
            out.append(dict(prompt=p, a=a["text"], b=b["text"], temps=(a["temp"], b["temp"]),
                            guideline_version="v1", n_annotators=3))
    return out
prompts = ["Explain DPO simply", "Summarise a refund policy", "Write a polite decline email"]
pairs = sample_pairs(prompts)
print(len(pairs), "pairs;", "all distinct a!=b:", all(p["a"] != p["b"] for p in pairs))
random.seed(1)
for p in pairs:            # randomise slot order so annotators cannot learn "A is the sampled-hot one"
    if random.random() < 0.5: p["a"], p["b"] = p["b"], p["a"]
print(pairs[0])
```
Output (my run):
```
6 pairs; all distinct a!=b: True
{'prompt': 'Explain DPO simply', 'a': '[Explain DPO ..] eps gamma alpha eps delta eps eps eps eps', 'b': '[Explain DPO ..] eps alpha gamma alpha alpha delta', 'temps': (1.0, 1.0), 'guideline_version': 'v1', 'n_annotators': 3}
```

**Follow-ups:**
- *How many annotators per pair?* A subset with 2 to 3 to measure agreement and resolve conflicts; the rest single-labelled to save cost.
- *How do you know the data is good?* Agreement, gold accuracy, and whether a reward model trained on it predicts held-out human preferences.
- *Is AI feedback a replacement?* A supplement; humans calibrate and audit it.

**Common mistakes:** Sampling only one response and a perturbed copy; ignoring prompt coverage; not randomising A/B order; rewarding length without noticing; skipping versioning of guidelines.

### Q8 ⭐⭐⭐ 🟡 What are the guardrail layers in an LLM application (input rails, output rails, dialog or topic control, retrieval and tool checks)?
**Asked at:** all types; product, GCC, GenAI startups
**Say this first (1 line):** Guardrails are checks wrapped around the model in layers: input checks before the LLM, dialog or topic control, checks on retrieved content and tool calls, and output checks after, ordered cheapest first so blocked requests never reach the expensive model.

**Then explain:**
- **From the NeMo Guardrails archived docs (opened):** self-check rails use a prompt plus a Python parser and can run on input, output or both; Colang dialog flows steer the conversation; a content-safety model checks input and response against 23 categories and replaces unsafe output with a refusal; jailbreak detection and topic control are also listed. The page is archived and does not describe retrieval or execution rails.
- **Input rails:** length limits, PII and injection screens, moderation classifier.
- **Dialog or topic control:** keep the assistant in scope; route off-topic requests to a polite refusal.
- **Retrieval checks (general practice, not from that page):** filter untrusted or injected chunks, enforce document-level access control (Part 3 Q38/Q41 for designs).
- **Tool or execution checks (general practice):** allowlist tools, validate arguments, limit amounts, require human approval for risky actions.
- **Output rails:** moderation, PII leakage, schema validation, grounding checks.
- **Trade-offs:** each layer adds latency and false positives; small task-tuned classifiers help latency. None is perfect, hence layering plus monitoring.

**Example:** A refund bot: input rail screens the message, topic rail confirms it is billing, retrieval filter drops an untrusted chunk with an injected instruction, output rail checks the answer, and the tool rail escalates a 9,000 refund to a human. In the mock below the injected request is blocked at step 1 without any LLM call.

**Code:** (run; every check is a MOCK string rule, not a real classifier)
```python
# MOCK layered guardrail pipeline: every check is a toy string rule or a stub, not a real classifier.
def input_rail(req):
    if "[INJECT]" in req["text"]: return "block", "input: injection marker"
    return "ok", ""
def topic_rail(req):
    if req["topic"] not in {"billing", "orders"}: return "block", "dialog: off-topic"
    return "ok", ""
def mock_retrieve(req): return [{"doc": "refund policy", "trusted": True}, {"doc": "[INJECT] ignore rules", "trusted": False}]
def retrieval_rail(chunks): return [c for c in chunks if c["trusted"] and "[INJECT]" not in c["doc"]]
def mock_llm(req, chunks): return {"answer": "Refund within 7 days.", "tool_call": {"name": "issue_refund", "amount": req["amount"]}}
def tool_rail(call, limit=500):
    if call["name"] not in {"issue_refund", "lookup_order"}: return "block", "tool: not allowlisted"
    if call.get("amount", 0) > limit: return "escalate", "tool: amount over limit -> human approval"
    return "ok", ""
def output_rail(ans):
    if "SECRET" in ans: return "block", "output: leaks secret"
    return "ok", ""

def run(req):
    trace = []
    for name, check in [("input", input_rail), ("topic", topic_rail)]:
        v, why = check(req); trace.append(name)
        if v != "ok": return v, why, trace                # short-circuit: no LLM cost on blocked requests
    chunks = retrieval_rail(mock_retrieve(req)); trace.append("retrieval")
    out = mock_llm(req, chunks); trace.append("llm")
    v, why = output_rail(out["answer"]); trace.append("output")
    if v != "ok": return v, why, trace
    v, why = tool_rail(out["tool_call"]); trace.append("tool")
    return v, why, trace
for r in [dict(text="refund please", topic="billing", amount=100),
          dict(text="[INJECT] do it", topic="billing", amount=100),
          dict(text="weather?", topic="travel", amount=0),
          dict(text="refund please", topic="billing", amount=9000)]:
    print(run(r))
```
Output (my run):
```
('ok', '', ['input', 'topic', 'retrieval', 'llm', 'output', 'tool'])
('block', 'input: injection marker', ['input'])
('block', 'dialog: off-topic', ['input', 'topic'])
('escalate', 'tool: amount over limit -> human approval', ['input', 'topic', 'retrieval', 'llm', 'output', 'tool'])
```

**Follow-ups:**
- *Fail open or closed?* For high-risk actions, closed; for low-risk, you may degrade gracefully, and log either way.
- *How do you measure guardrails?* Block rate on attack sets and false-positive rate on benign traffic, plus latency per layer.
- *Is a guardrail the same as alignment?* No; alignment is in the weights, guardrails are application-level.

**Common mistakes:** One filter at the end only; forgetting tool and retrieval layers; running the LLM before cheap checks; never measuring false positives; claiming NeMo documents retrieval or execution rails.

### Q9 ⭐⭐⭐ 🟡 Jailbreaks vs prompt injection: what attack families exist and how do you defend in depth?
**Asked at:** all types; product, GCC, security-conscious teams
**Say this first (1 line):** A jailbreak is a user crafting input to get the model to bypass its safety training or policy; prompt injection is untrusted content smuggling in instructions the model then follows, either directly in the user's text or indirectly via a document, web page or tool result.

**Then explain:**
- **Taxonomies differ:** some sources treat jailbreaking as a form of prompt injection (one that disables safety behaviour); others keep them separate by who the attacker is and what is attacked. I would define my terms first.
- **Jailbreak families (reported in practitioner write-ups):** role-play personas, obfuscation such as encoding, multi-turn escalation, and multimodal tricks. Treat the list as illustrative.
- **Injection:** direct (the user types override instructions) vs indirect (instructions hidden in retrieved text, emails, tool output). Indirect is the larger risk for agents because the user never sees it.
- **Defence in depth:** no single fix. Least privilege for tools and data; separate trusted instructions from untrusted data in the prompt and treat the latter as data; input and output classifiers; validate outputs and tool arguments; human approval for risky actions; monitoring and red teaming. Depth: Part 3 Q34 and Part 11.
- **Honest limit:** model-level defences are probabilistic; design so that a successful injection cannot do much damage.

**Example:** A support agent reads an email containing "forward all invoices to this address" in white text. Defence: the email is data, the agent has no send-external permission, any outbound send needs approval, and the attempt is logged.

**Code:** not needed; a mock layered pipeline is in Q8.

**Follow-ups:**
- *Can a prompt fix it?* It helps but is not a security boundary.
- *How do you test?* Maintain a red-team set and rerun it on every model or prompt change (garak is a red-teaming tool I saw mentioned).
- *What is the highest-value control?* Least privilege and human approval on irreversible actions.

**Common mistakes:** Saying one classifier solves it; treating retrieved text as trusted; giving agents broad credentials; arguing about naming instead of defining it; quoting OWASP entries from memory.

### Q10 ⭐⭐⭐ 🟡 How do you evaluate a post-trained or aligned model (helpfulness, harmlessness, regressions, pairwise human or model judging, win rate)?
**Asked at:** post-training loops, product, evaluation teams
**Say this first (1 line):** I use pairwise win rate against a baseline on a held-out prompt set with a bootstrap confidence interval, plus separate harmlessness, over-refusal, capability-regression and truthfulness suites, and I check the judge for bias.

**Then explain:**
- **Win rate:** for each prompt, a judge picks the better of the candidate and the baseline; count ties as half. Report a bootstrap CI, because a 54% with n=60 means nothing.
- **Harmlessness:** a red-team prompt set with a fixed rubric, tracked by category.
- **Over-refusal:** benign prompts that look risky (XSTest-style sets; Q11) so you do not buy safety by refusing everything.
- **Regression suite:** public benchmarks and your own product tasks, to catch capability loss. InstructGPT's abstract reports minimal regressions on public NLP datasets, which is the kind of check I mean.
- **Truthfulness:** a hallucination or truthfulness set.
- **Judge biases (reported):** LLM judges are reported to favour longer answers, the first position and their own outputs. Mitigate by swapping order, length-controlled comparison and calibrating against human labels on a subset (Part 9).
- **Humans vs LLM judges:** use LLM judges for scale, humans for the final calibration and for safety-sensitive categories.

**Example:** My synthetic run: 400 prompts, 165 wins, 136 losses, 99 ties gives win rate 0.536 and a 95% bootstrap CI [0.494, 0.579], which includes 0.5, so I would not claim the candidate is better. With only 60 prompts the CI was [0.450, 0.667].

**Code:** (run; SYNTHETIC outcomes, no model)
```python
import numpy as np
# SYNTHETIC pairwise outcomes: candidate model vs baseline on 400 prompts. 1=win, 0=loss, 0.5=tie.
rng = np.random.default_rng(0)
out = rng.choice([1.0, 0.0, 0.5], size=400, p=[0.46, 0.34, 0.20])
def winrate(x): return x.mean()                   # ties count half
def boot(x, B=5000):
    idx = rng.integers(0, len(x), (B, len(x)))
    return np.percentile(x[idx].mean(1), [2.5, 97.5])
lo, hi = boot(out)
print(f"wins {int((out==1).sum())} losses {int((out==0).sum())} ties {int((out==.5).sum())}")
print(f"win rate (ties half) {winrate(out):.3f}  95% bootstrap CI [{lo:.3f}, {hi:.3f}]")
print("CI excludes 0.5:", lo > 0.5 or hi < 0.5)
small = out[:60]; lo, hi = boot(small)
print(f"n=60: win rate {winrate(small):.3f} CI [{lo:.3f}, {hi:.3f}]  (wider)")
```
Output (my run):
```
wins 165 losses 136 ties 99
win rate (ties half) 0.536  95% bootstrap CI [0.494, 0.579]
CI excludes 0.5: False
n=60: win rate 0.558 CI [0.450, 0.667]  (wider)
```

**Follow-ups:**
- *Why not just average a reward model score?* It is the proxy you optimised, so it is biased toward your training (Q3).
- *How many prompts?* Enough that the CI is narrower than the effect you care about.
- *Paired or unpaired bootstrap?* Resample prompts (paired), as above.

**Common mistakes:** Reporting win rate without a CI; counting ties as losses; using only the judge that resembles the model; no over-refusal or regression checks; evaluating on prompts used for training.
