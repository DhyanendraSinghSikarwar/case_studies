### Q37 ⭐ 🟡 AI code review: this LLM-written LoRA/SFT training script has bugs (unshifted or unmasked labels, wrong learning rate, merging in 4-bit, dropout left on at eval, wrong target modules). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
**Say this first (1 line):** I read a training script against a fixed checklist: labels shifted and masked, only adapter weights trainable, `model.eval()` for evaluation, a sane learning rate, `zero_grad` every step, and one merge only after training. I prove each bug on a tiny model by its symptom, then fix them and lock the fixes with a small test.

**Then explain:**

| # | Bug | Symptom (from my run, tiny torch model) |
|---|---|---|
| 1 | Labels not shifted (predict token t from token t) | Loss falls to 0.001, real next-token accuracy 0.00: the model learned to copy its input. Shifted: accuracy 1.00 |
| 2 | Padding (and prompt) tokens not set to `-100` | Batch was 67% PAD: reported loss 0.213 vs real 0.322. On the untuned base 9.66 vs 15.55, so the loss is diluted and misleading |
| 3 | Base weights not frozen | Trainable params 2,608 instead of 512; the head weights changed. At real scale this means full fine-tuning memory and forgetting |
| 4 | Dropout left on at eval (no `model.eval()`) | Same batch, two evals: 15.636 vs 15.826. With `eval()`: 15.595 and 15.595 |
| 5 | Learning rate far too high | lr 1.0: loss spiked to 95.8; lr 100: spiked to 1.5 million. This toy task is so easy that it recovered; do not count on that |
| 6 | `optimizer.zero_grad()` forgotten | Gradient norm on 5 identical steps: 1.578, 3.156, 4.734, 6.312, 7.890 (adds up). Correct: constant |
| 7 | Adapter merged twice | Max logit difference vs unmerged model 26.6; with a merged flag it is 0.0000 |

- **Isolation:** each demo changes exactly one thing against the same base model, so the symptom is attributable. The base was "pretrained" on +1 (next token = current + 1) and fine-tuned to +2; the model is a bigram-style toy, not a transformer.
- **Learning rate:** a LoRA adapter usually takes a higher LR than full fine-tuning (the TRL docs mention about 1e-4 for adapters vs 2e-5 default for full FT). "Far too high" is relative. If a loss spikes or goes NaN, I lower the LR before anything else. In my toy, Adam's step size is set by LR, not gradient size, so LR matters directly.
- **Bugs I did not run (no 4-bit or PEFT library here):** merging into a 4-bit quantised base (the weights are rounded; merging needs a dequantised copy and loses a bit of accuracy; check the PEFT docs on merging quantised models), and wrong `target_modules` (module names differ by model; a name that matches nothing should fail loudly, or you silently train nothing; check your PEFT version). I would still list both in the review and verify by printing `trainable parameters` and the module names.
- **Other things I check:** EOS token appended and matching the chat template, loss only on the assistant tokens (TRL has `assistant_only_loss` / `completion_only_loss` options, check current docs), train/eval split with no leakage, seed, gradient clipping, bf16 vs fp32 for the adapter.
- **How to review LLM-written code:** do not trust that it runs. Print the trainable parameter count, print one decoded batch with its labels, overfit 8 examples (loss must go near 0), compare eval twice.

**Example:** an LLM-written script reports a beautiful loss of 0.001 after 100 steps. In an interview I would say: "that is suspicious, not good". With unshifted labels this is exactly what happens (bug 1), and the model is useless at generation.

**Code:** (executed, standalone, torch only, CPU, seconds)
```python
# Standalone, torch only, tiny bigram-style LM so it runs in seconds on CPU.
# Task: next token = (current + 1) % V for the base, (current + 2) % V for the fine-tune.
import copy, torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(1)

V, D, T, PAD = 16, 32, 12, 0

class LoRALinear(nn.Module):
    def __init__(self, base, r=8, alpha=16, p=0.0):
        super().__init__()
        self.base, self.scale, self.merged = base, alpha / r, False
        self.A = nn.Parameter(torch.randn(r, base.in_features) * 0.1)
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        self.drop = nn.Dropout(p)
    def forward(self, x):
        out = self.base(x)
        return out if self.merged else out + self.drop(x) @ self.A.T @ self.B.T * self.scale
    @torch.no_grad()
    def merge(self, guard=True):
        if guard and self.merged: return                     # fixed: never merge twice
        self.base.weight += self.scale * self.B @ self.A
        self.merged = True

class TinyLM(nn.Module):
    def __init__(self, p=0.0):
        super().__init__()
        self.emb, self.proj, self.head = nn.Embedding(V, D), nn.Linear(D, D), nn.Linear(D, V)
        self.drop = nn.Dropout(p)
    def forward(self, ids):
        return self.head(self.drop(torch.relu(self.proj(self.emb(ids)))))

def make_batch(n, shift, g, ragged=False):
    start = torch.randint(1, V, (n, 1), generator=g)
    ids = torch.cat([(start + shift * t - 1) % (V - 1) + 1 for t in range(T)], 1)   # tokens 1..15, 0 = PAD
    if ragged:
        lens = torch.randint(3, 6, (n,), generator=g)
        for i, L in enumerate(lens): ids[i, L:] = PAD
    return ids

def lm_loss(model, ids, shifted=True, mask_pad=True):
    logits = model(ids)
    if shifted: logits, labels = logits[:, :-1], ids[:, 1:].clone()
    else:       labels = ids.clone()                           # BUG shown when shifted=False
    if mask_pad: labels[labels == PAD] = -100
    return F.cross_entropy(logits.reshape(-1, V), labels.reshape(-1), ignore_index=-100)

def train(model, params, steps, lr, shift, shifted=True, mask_pad=True, ragged=False, seed=0, zero_grad=True):
    g, opt, losses = torch.Generator().manual_seed(seed), torch.optim.Adam(params, lr=lr), []
    model.train()
    for _ in range(steps):
        if zero_grad: opt.zero_grad()
        loss = lm_loss(model, make_batch(64, shift, g, ragged), shifted, mask_pad)
        loss.backward(); opt.step(); losses.append(loss.item())
    return losses

def acc(model, shift):                                         # next-token accuracy on the true shifted task
    model.eval(); ids = make_batch(256, shift, torch.Generator().manual_seed(99))
    with torch.no_grad(): return (model(ids)[:, :-1].argmax(-1) == ids[:, 1:]).float().mean().item()

def add_lora(base, p=0.0):
    m = copy.deepcopy(base); m.proj = LoRALinear(m.proj, p=p); return m
def freeze_base(m):
    for n, q in m.named_parameters(): q.requires_grad = n.endswith(".A") or n.endswith(".B")
def n_trainable(m): return sum(q.numel() for q in m.parameters() if q.requires_grad)

torch.manual_seed(0)
base = TinyLM(); train(base, base.parameters(), 400, 1e-2, shift=1)      # "pretrained" on +1
print(f"base accuracy on +1 task {acc(base,1):.2f}, on +2 task {acc(base,2):.2f}")

print("\n== Bug 1: labels not shifted ==")
m = copy.deepcopy(base); l = train(m, m.parameters(), 300, 1e-2, shift=2, shifted=False)
print(f"loss {l[0]:.2f} -> {l[-1]:.3f} (looks great); real +2 next-token accuracy {acc(m,2):.2f} (model learned to copy its input)")
m = copy.deepcopy(base); l = train(m, m.parameters(), 300, 1e-2, shift=2, shifted=True)
print(f"shifted: loss {l[0]:.2f} -> {l[-1]:.3f}; real accuracy {acc(m,2):.2f}")

print("\n== Bug 2: padding not masked ==")
m = copy.deepcopy(base); train(m, m.parameters(), 300, 1e-2, shift=2, mask_pad=False, ragged=True)
ids = make_batch(256, 2, torch.Generator().manual_seed(5), ragged=True); m.eval()
with torch.no_grad():
    print(f"same trained model, batch is {(ids==PAD).float().mean():.0%} PAD: reported loss {lm_loss(m,ids,mask_pad=False):.3f}, "
          f"real loss {lm_loss(m,ids,mask_pad=True):.3f}")
with torch.no_grad():
    b = make_batch(256, 2, torch.Generator().manual_seed(5), ragged=True)
    print(f"untrained-on-task base: unmasked {lm_loss(base,b,mask_pad=False):.3f} vs masked {lm_loss(base,b,mask_pad=True):.3f}  (pad tokens dilute the signal)")

print("\n== Bug 3: base not frozen ==")
m = add_lora(base); print("buggy trainable params:", sum(q.numel() for q in m.parameters() if q.requires_grad))
before = m.head.weight.clone(); train(m, m.parameters(), 50, 1e-2, shift=2)
print("head weights changed:", not torch.equal(before, m.head.weight))
m = add_lora(base); freeze_base(m); print("fixed trainable params:", n_trainable(m))

print("\n== Bug 4: dropout left on at eval ==")
m = add_lora(base, p=0.0); m.drop.p = 0.3; ids = make_batch(64, 2, torch.Generator().manual_seed(3))
m.train()
with torch.no_grad(): a1, a2 = lm_loss(m, ids).item(), lm_loss(m, ids).item()
m.eval()
with torch.no_grad(): b1, b2 = lm_loss(m, ids).item(), lm_loss(m, ids).item()
print(f"no eval(): {a1:.4f} vs {a2:.4f} on the same batch; with eval(): {b1:.4f} vs {b2:.4f}")

print("\n== Bug 5: learning rate far too high for the adapter ==")
for lr in (1e-2, 1.0, 100.0):
    m = add_lora(base); freeze_base(m); l = train(m, [q for q in m.parameters() if q.requires_grad], 200, lr, shift=2)
    print(f"lr={lr}: loss {l[0]:.2f} -> {l[-1]:.3f}, max {max(l):.1f}, accuracy {acc(m,2):.2f}")

print("\n== Bug 6: optimizer.zero_grad() forgotten ==")
for z in (True, False):
    m = add_lora(base); freeze_base(m); g = torch.Generator().manual_seed(0)
    ps = [q for q in m.parameters() if q.requires_grad]; opt = torch.optim.SGD(ps, lr=0.0); ids = make_batch(64, 2, g)
    norms = []
    for _ in range(5):
        if z: opt.zero_grad()
        lm_loss(m, ids).backward(); norms.append(round(m.proj.B.grad.norm().item(), 3))
    print(f"zero_grad={z}: grad norm of B over 5 identical steps {norms}")

print("\n== Bug 7: merging the adapter twice ==")
m = add_lora(base); freeze_base(m); train(m, [q for q in m.parameters() if q.requires_grad], 200, 1e-2, shift=2)
ids = make_batch(64, 2, torch.Generator().manual_seed(3)); m.eval()
with torch.no_grad(): ref = m(ids)
for guard in (False, True):
    mm = copy.deepcopy(m); mm.proj.merge(guard=guard); mm.proj.merge(guard=guard)
    with torch.no_grad(): print(f"guard={guard}: max logit diff vs unmerged {(mm(ids)-ref).abs().max():.4f}, accuracy {acc(mm,2):.2f}")
# note: with guard=False the 2nd merge adds the delta again but the flag already skips the adapter path, so output = base + 2*delta

print("\n== FIXED recipe + test ==")
def finetune_fixed(seed=0):
    torch.manual_seed(seed); m = add_lora(base, p=0.05); freeze_base(m)
    ps = [q for q in m.parameters() if q.requires_grad]
    l = train(m, ps, 300, 1e-2, shift=2, ragged=True, seed=seed); return m, l
m, l = finetune_fixed()
base_head, base_proj = base.head.weight.clone(), base.proj.weight.clone()
# tests
assert n_trainable(m) == 8 * D * 2, n_trainable(m)
assert torch.equal(m.head.weight, base_head) and torch.equal(m.proj.base.weight, base_proj), "base moved"
assert l[-1] < 0.2 * l[0], "loss did not drop"
assert acc(m, 2) > 0.9, acc(m, 2)
m.eval(); ids = make_batch(64, 2, torch.Generator().manual_seed(3))
with torch.no_grad(): ref = m(ids); assert torch.equal(ref, m(ids)), "eval nondeterministic"
mm = copy.deepcopy(m); mm.proj.merge(); mm.proj.merge()
with torch.no_grad(): assert (mm(ids) - ref).abs().max() < 1e-4, "merge changed outputs"
print(f"all tests passed: trainable {n_trainable(m)} of {sum(q.numel() for q in m.parameters())}, loss {l[0]:.2f} -> {l[-1]:.3f}, accuracy {acc(m,2):.2f}")

```

**Follow-ups:**
- *Why does the unshifted loss go to zero?* The model sees token t and is asked for token t. An identity map is easy, so it learns it. Training should predict token t+1 from the prefix up to t.
- *Why `-100`?* It is the default `ignore_index` of PyTorch cross-entropy (and TRL uses it), so those positions add no loss and no gradient.
- *After merging, can I keep training the adapter?* Not safely. Keep the unmerged adapter file; merge only a copy for serving (Part 10).

**Common mistakes:**
- Judging a training run by loss alone, not by held-out task accuracy and generations.
- Calling `merge` repeatedly in a notebook cell that is re-run.
- Evaluating without `model.eval()` and then chasing noise between runs.
- Not printing the trainable parameter count. One line catches bug 3 and a wrong `target_modules`.

### Q38 ⭐ 🔴 Why does low-rank adaptation work? Derive the parameter count, the identity initialisation, and the effective scaling of the update.
**Asked at:** big tech, research-leaning teams, GenAI startups
**Say this first (1 line):** LoRA freezes W and learns a rank-r update, W' = W + (alpha/r)·B·A, with B (d_out x r) starting at zero so the model starts exactly as the base. It works because fine-tuning updates are believed to be close to low-rank, so r(d_out + d_in) numbers capture most of what d_out·d_in would learn.

**Then explain:**
- **Parameter count:** full layer d_out·d_in. LoRA: B has d_out·r, A has r·d_in, so r(d_out + d_in). For 4096 x 4096: r=8 gives 65,536 (0.39%), r=16 gives 131,072 (0.78%), r=64 gives 524,288 (3.12%) of 16,777,216. (One of the prep articles I read says r=16 is "a bit over a hundredth"; the real figure is 0.78%, so check the arithmetic yourself.)
- **Identity at init:** A is random (PEFT's guide says Kaiming-uniform), B is zeros, so BA = 0 and the output equals the frozen model's. Training starts from a working model, not a perturbed one. If both were random the update would start as noise.
- **Why not both zero:** with both zero, both gradients are zero and nothing ever moves. With B = 0 and A random, the gradient to B is non-zero from step 1.
- **Gradient at step 1:** dL/dA = s·Bᵀ·(dL/dW), which is exactly zero when B = 0. So at the very first step only B moves; from step 2 on, B is non-zero and A gets gradient too. I checked this numerically: step 1 |grad A| = 0 exactly, |grad B| = 0.1825; step 2 |grad A| = 0.0059.
- **Scaling alpha/r:** the update is multiplied by alpha/r. The goal is that when you change r, you do not have to retune the learning rate, because the update's overall size stays roughly the same (approximately, not exactly). In my toy (fixed alpha=16, 50 Adam steps, one seed) the update norm was 1.34, 1.31, 1.00, 0.80 for r = 1, 4, 16, 64 with alpha/r, but 1.34, 2.60, 4.56, 6.93 with no scaling, and 1.34, 1.98, 2.70, 3.84 with alpha/sqrt(r). So alpha/r is roughly flat with a slow drop at large r. rsLoRA (the `use_rslora` flag in PEFT, per the guide) argues that alpha/sqrt(r) is better for large ranks, because alpha/r shrinks the update too much and higher ranks then learn little. My toy does not prove that claim; it only shows the scaling behaviour.
- **Why low rank is plausible:** the LoRA paper builds on the idea that over-parameterised models live on a low intrinsic dimension (Aghajanyan et al., 2020, "Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning", from memory, not verified). The LoRA paper reports being on par with or better than full fine-tuning on several models with far fewer trainable parameters (per its abstract). It is empirical, not a theorem: hard tasks or big domain shifts need higher rank, or full fine-tuning.
- **Free at inference:** W + sBA can be merged into W, so no extra latency (a point the LoRA abstract makes against adapter layers).

**Example:** in the toy below I made the "fine-tuning target" differ from W by a rank-3 change plus small noise and trained the full matrix. The update came out with singular values [8.36, 6.10, 4.20, 0.08, 0.07, 0.07]: 3 big directions, then noise. A rank-3 truncation has 1.8% relative error. This is built in by design (the target is low-rank), so it shows what the claim means, not that real LLM updates are low-rank.

**Code:** (executed, standalone, torch only; toy single linear layer, not an LLM)
```python
# Standalone, torch only. Toy numbers on a single linear layer (not an LLM).
import math, torch
torch.set_num_threads(1)
torch.manual_seed(0)

# 1) parameter count: d_out*r + r*d_in vs d_out*d_in
d_out = d_in = 4096
for r in (8, 16, 64):
    lora = d_out * r + r * d_in
    print(f"r={r:>2}: LoRA {lora:>9,} vs full {d_out*d_in:,} -> {100*lora/(d_out*d_in):.2f}%")

# 2) identity at init, and the first-step gradient pattern (W' = W + s * B A, B=0, A random)
din, dout, r, alpha = 32, 24, 4, 8
W = torch.randn(dout, din) / math.sqrt(din)
A = (torch.rand(r, din) * 2 - 1) / math.sqrt(din); A.requires_grad_()   # uniform init (PEFT uses Kaiming-uniform; detail may differ)
B = torch.zeros(dout, r, requires_grad=True)
x, y = torch.randn(64, din), torch.randn(64, dout)
s = alpha / r
out = x @ (W + s * B @ A).T
print("\nmax |output - frozen output| at init:", (out - x @ W.T).abs().max().item())
loss = ((out - y) ** 2).mean(); loss.backward()
print(f"step 1: |grad B| = {B.grad.norm():.4f}, |grad A| = {A.grad.norm():.1e}  (A gets exactly zero because dL/dA = s * B^T * dL/dW and B = 0)")
with torch.no_grad(): B -= 0.1 * B.grad                                # only B moves
A.grad = None; B.grad = None
loss = ((x @ (W + s * B @ A).T - y) ** 2).mean(); loss.backward()
print(f"step 2: |grad A| = {A.grad.norm():.4f}  (nonzero now, both factors train from here)")

# 3) scaling: does the size of the update depend on r? same recipe, fixed alpha, 50 Adam steps
def delta_norm(r, mode, alpha=16, steps=50, lr=1e-3):
    torch.manual_seed(1)
    A = ((torch.rand(r, din) * 2 - 1) / math.sqrt(din)).requires_grad_()
    B = torch.zeros(dout, r, requires_grad=True)
    s = alpha / r if mode == "alpha/r" else alpha / math.sqrt(r) if mode == "alpha/sqrt(r)" else alpha
    opt = torch.optim.Adam([A, B], lr=lr)
    for _ in range(steps):
        opt.zero_grad(); ((x @ (W + s * B @ A).T - y) ** 2).mean().backward(); opt.step()
    return (s * B @ A).norm().item()
print("\n|delta W|_F after 50 Adam steps, alpha=16 fixed (toy; one seed):")
print("r      ", *[f"{r:>7}" for r in (1, 4, 16, 64)])
for mode in ("none", "alpha/r", "alpha/sqrt(r)"):
    print(f"{mode:<14}", *[f"{delta_norm(r, mode):7.3f}" for r in (1, 4, 16, 64)])

# 4) low-rank update: fine-tune a layer toward a target that differs from W by a rank-3 change + noise
torch.manual_seed(2)
Wt = W + torch.randn(dout, 3) @ torch.randn(3, din) * 0.3 + 0.01 * torch.randn(dout, din)
X = torch.randn(512, din); Y = X @ Wt.T
Wf = W.clone().requires_grad_(); opt = torch.optim.SGD([Wf], lr=0.05)
for _ in range(500):
    opt.zero_grad(); ((X @ Wf.T - Y) ** 2).mean().backward(); opt.step()
sv = torch.linalg.svdvals((Wf - W).detach())
e = (sv ** 2).cumsum(0) / (sv ** 2).sum()
print("\nfull fine-tune delta: top singular values", [round(v, 2) for v in sv[:6].tolist()])
print(f"energy in top 3 singular directions: {e[2]:.3f}; top 1: {e[0]:.3f}")
U, S, Vh = torch.linalg.svd((Wf - W).detach())
for k in (1, 3, 8):
    approx = U[:, :k] @ torch.diag(S[:k]) @ Vh[:k]
    print(f"rank-{k} truncation of the update: relative error {((Wf-W).detach()-approx).norm()/(Wf-W).detach().norm():.3f}")

```

**Follow-ups:**
- *Does LoRA match full fine-tuning always?* No. It often matches on narrow tasks; for large shifts or new capabilities it can fall behind, which is why rank and target modules are tuned (Q4, Q5).
- *Why is B the zero one, not A?* Either works in principle. The standard choice is B = 0 so BA = 0 and A random so B gets a useful gradient immediately.
- *What does alpha do if I double r and keep alpha?* With alpha/r, the multiplier halves, so the update stays about the same size. Many people set alpha = 2r or fix alpha and vary r; either way, check current PEFT docs.

**Common mistakes:**
- Saying "LoRA trains 0.1% of weights" without computing it for the actual r and layers.
- Claiming alpha/r keeps training "identical" across ranks. It is roughly stable at best.
- Saying both A and B are initialised to zero.
- Presenting the low intrinsic rank result as proven for LLM fine-tuning.

### Q39 ⭐ 🔴 Chain-of-thought and rationale distillation: how do you distil reasoning from a stronger model, and what are the limits and risks?
**Asked at:** big tech, GenAI startups, research-leaning teams
**Say this first (1 line):** I ask a stronger teacher to solve prompts with step-by-step reasoning, keep only the traces whose final answer is correct, and fine-tune the student (SFT) on rationale plus answer. It transfers the habit of writing reasoning, but it is limited by what the student can represent and by how trustworthy the traces are.

**Then explain:**
- **Pipeline:** (1) pick prompts that match the target distribution; (2) sample one or several traces per prompt from the teacher with a "think step by step" style prompt; (3) filter: final answer matches the label or a checker, plus format checks, dedup, length limits; (4) SFT the student on `prompt -> rationale + answer` with loss on the completion only; (5) evaluate on a held-out set, with the student's answers, not the rationales.
- **Known work (from memory, not verified):** "Distilling step-by-step" (Hsieh et al., 2023) trains small models on teacher rationales, in a multi-task form that also predicts the label; "Large language models are reasoning teachers" (Ho et al., 2022) fine-tunes small models on teacher chain-of-thought. Check the papers before quoting results.
- **Limits:**
  - *Student capacity:* a tiny student can copy the style of reasoning without being able to execute it. It writes fluent steps that are wrong (Q45 covers the capacity gap).
  - *Distribution shift:* prompts outside the teacher-traced set get rationales in the same style, but not the same skill.
  - *Teacher errors:* a correct final answer can sit on top of a wrong trace. In my mock run, 20 of 1,575 kept traces (1.3%) had a flawed step even though the answer was right.
  - *Faithfulness:* a rationale may not be the real reason the model answered. Training on it teaches the student to produce plausible text, so I do not treat the rationale as an explanation.
  - *Contamination:* if the teacher or the prompts include benchmark items, scores inflate. Dedup against eval sets (Part 9).
  - *Terms of use:* many API providers restrict using outputs to train competing models. Read the teacher's current license/terms before collecting data. This is a legal check, not a technical one.
- **Cost trade:** long rationales raise student inference cost (more tokens). Only worth it if the accuracy gain pays for it; sometimes direct-answer SFT is enough for easy tasks.
- **Better filtering:** answer match is the cheapest. Step-level checks (a calculator, unit tests for code, a verifier model) catch lucky-right traces, at extra cost (see Q47 and Part 5 for verifier ideas).

**Example:** math word problems: 5,000 prompts, 4 teacher samples each, keep the correct ones, up to 2 distinct traces per prompt. Student gains on in-distribution problems; I would report it also on a held-out set of different problem types, and check that rationales do not get longer without accuracy gain.

**Code:** (executed, standalone; MOCK teacher, no model is called; only demonstrates the filter and what it misses)
```python
# Standalone, no libraries beyond random. MOCK teacher (a scripted noisy solver), not an LLM.
# Problem: "a + b * c". Trace: "b*c=P; a+P=R. Answer: R"
import random
random.seed(0)

def mock_teacher(a, b, c):
    p = b * c
    if random.random() < 0.15: p += random.choice([-10, -1, 1, 10])          # arithmetic slip in step 1
    r = a + p
    if random.random() < 0.10: r += random.choice([-1, 1])                   # slip in step 2
    if random.random() < 0.05: r = a + b * c                                 # sloppy trace, lucky right answer
    return f"{b}*{c}={p}; {a}+{p}={r}. Answer: {r}", r

def rationale_is_consistent(a, b, c, trace):                                  # step-by-step check (what a process check could do)
    s1, s2 = trace.split(". Answer")[0].split("; ")
    p = int(s1.split("=")[1]); r = int(s2.split("=")[1])
    return p == b * c and r == a + p

data, stats = [], dict(sampled=0, kept=0, kept_but_bad_rationale=0)
for _ in range(2000):
    a, b, c = random.randint(1, 50), random.randint(2, 12), random.randint(2, 12)
    trace, ans = mock_teacher(a, b, c)
    stats["sampled"] += 1
    if ans == a + b * c:                                                      # filter 1: final answer correct
        stats["kept"] += 1
        ok = rationale_is_consistent(a, b, c, trace)
        stats["kept_but_bad_rationale"] += (not ok)
        data.append({"prompt": f"{a}+{b}*{c}", "completion": trace, "rationale_ok": ok})
print(stats)
print(f"answer-correct rate {stats['kept']/stats['sampled']:.1%}; of kept, flawed rationale {stats['kept_but_bad_rationale']/stats['kept']:.1%}")
strict = [d for d in data if d["rationale_ok"]]
print("after adding a step check:", len(strict), "examples")
print("example SFT row:", strict[0])

```

**Follow-ups:**
- *Do I train on the rationale tokens only or the answer too?* Both; mask the prompt. Some setups also add the label-only task so the model keeps a short-answer mode.
- *Is this the same as logit distillation?* No. This is black-box sequence-level distillation: only text is needed, so tokenizers can differ. Logit KD needs the teacher's probabilities and a shared vocabulary (Q22 to Q24).
- *How many samples per prompt?* A few; more diversity helps, duplicates do not. I would measure on a dev set rather than guess.

**Common mistakes:**
- Assuming a correct final answer means a correct rationale.
- Treating rationales as faithful explanations.
- Ignoring the teacher's terms of service.
- Evaluating on prompts that overlap with the distillation prompts.

### Q40 ⭐ 🔴 What is the superficial alignment hypothesis (LIMA)? What evidence supports it, and what are its critiques and implications for data curation?
**Asked at:** research-leaning teams, big tech, GenAI startups
**Say this first (1 line):** The hypothesis says a model learns almost all its knowledge and ability in pretraining, and alignment only teaches it which style and format to use when talking to users. LIMA (Zhou et al., 2023) tested it by fine-tuning a 65B LLaMA base on only about 1,000 carefully curated examples, and got surprisingly good chat behaviour.

**Then explain:**
- **The claim:** pretraining = knowledge; SFT/alignment = format, tone, "which sub-distribution of the pretrained model to use". So quality and diversity of a small set can matter more than quantity.
- **The evidence (as I recall it from the paper and its explainers; I did not re-open the paper):** 1,000 curated prompt-response pairs, no RLHF, on a 65B base; a human study that compared LIMA with other models and reported win-or-tie rates that were competitive. I am not quoting the exact percentages because I would rather not misstate them.
- **Critiques:**
  - *Small human study*, a few hundred prompts, so wide uncertainty and judge/prompt-set effects.
  - *Strong base model:* it works because a 65B base already knows a lot. A small or weak base may not show the same effect.
  - *Narrow eval:* chat-style helpfulness, not long multi-step reasoning, code or safety under attack.
  - *Harder skills* such as reasoning, code and tool use often improve with more (and more targeted) data and with RL. I would hedge here: this is a common view in the literature, not a result I can cite precisely.
  - *Style vs substance:* human and LLM judges can be swayed by style, so "looks aligned" is not "is correct" (Part 9).
  - *"Superficial" is a hypothesis*, not a law. Even LIMA's authors framed it as a hypothesis.
- **Implications for data curation:**
  - Invest in a small, clean, diverse, consistently formatted set before scaling up. Remove contradictions and low-quality answers.
  - Use a quality filter and a dedup step; cover task types and tones you will actually serve.
  - Always compare "1k curated" vs "10k noisy" on your own eval, then decide.
  - Do not use SFT to add knowledge; use retrieval or continued pretraining (Q44).

**Example:** a support bot on a strong 8B base: 800 hand-reviewed conversations in the company's tone often change the style a lot. The same 800 will not teach new product facts that changed last week; those belong in retrieval.

**Follow-ups:**
- *If alignment is superficial, why do labs use huge RLHF/preference pipelines?* Because safety, calibrated refusals, and harder skills are not just style. That is my reading; the hypothesis is about the portion of alignment that is style and format.
- *Is it a reason to use only 1,000 examples?* No. It is a reason to test small, high-quality data first as a baseline.
- *How would you test the hypothesis yourself?* Train with 100, 300, 1,000, 3,000 examples at fixed quality and plot task accuracy vs format adherence separately. If format saturates early and accuracy keeps rising, the claim holds only for format.

**Common mistakes:**
- Saying LIMA proves that alignment needs no data or no RLHF.
- Quoting precise win rates from memory.
- Ignoring the base-model-strength caveat.
- Concluding from it that SFT can add facts.

### Q41 ⭐ 🔴 How do multi-adapter composition and model merging work (weighted adapters, task arithmetic, TIES-style merging), and what are the risks?
**Asked at:** research-leaning teams, GenAI startups, platform teams
**Say this first (1 line):** Merging combines several fine-tunes of the same base into one model by adding scaled "deltas" (fine-tuned weights minus base weights) instead of retraining. It is cheap, but where two tasks push the same weight in opposite directions they interfere, so every merge needs its own evaluation.

**Then explain:**
- **Weighted adapters (PEFT):** the LoRA guide lists `add_weighted_adapter`, which builds a new adapter from several existing ones with weights. Combination methods and arguments change between versions, so check the current docs. Same base model and compatible target modules are required.
- **Task arithmetic (from memory, not verified: Ilharco et al., 2022):** task vector = W_finetuned − W_base. Merged = W_base + Σ λ_i · τ_i. Adding vectors adds skills (roughly); subtracting one can reduce a behaviour. λ is tuned on a dev set.
- **TIES-style merging (from memory, not verified: Yadav et al., 2023):** (1) trim: keep only the largest-magnitude entries of each task vector; (2) elect sign: per parameter, choose the sign with the larger total mass; (3) merge only entries that agree with the elected sign (a disjoint mean). The idea is to cut noise from small changes and stop opposing signs cancelling.
- **Why plain averaging hurts:** if task A pushes a weight up and task B pushes it down, the average is about zero and neither task gets its change. Averaging also scales every delta by 1/N, so each task is weakened even where nobody conflicts.
- **What my toy shows (synthetic task vectors, 2 tasks, 1,500 shared coordinates with opposed signs, 1,000 private ones each):** fraction of each task's own delta retained:

| Method | task0 private | task1 private | task0 shared | task1 shared |
|---|---|---|---|---|
| naive average | 0.50 | 0.50 | 0.10 | -0.08 |
| sum (scale 1) | 1.00 | 1.00 | 0.20 | -0.16 |
| TIES-style | 0.81 | 0.90 | 0.61 | -0.51 |

  Averaging cancels the shared block for both tasks and halves the private part. Sign election keeps most of the private deltas and rescues the shared block for the stronger task, but it does it by picking a winner: task 1 on shared coordinates is pushed the wrong way (-0.51). So sign election resolves conflicts, it does not remove them. This is a toy: real weights are not like this, and it says nothing about accuracy.
- **Risks:** interference and sign conflicts; same base and architecture only; merging adapters trained from different initialisations is unreliable; tuned λ can overfit the dev set; safety behaviour of a base can be diluted by a merge; evaluation after merging is mandatory (each task, plus general regression); quantised bases need care (Q37, Part 10). Merging many adapters is not a substitute for multi-task training when you can afford it.
- **Alternative to merging:** serve separate adapters and pick one per request (routing), which avoids interference at the cost of more serving complexity.

**Example:** a platform team has a "SQL helper" adapter and a "support tone" adapter on one base. They try `add_weighted_adapter` at 0.5/0.5, then 0.7/0.3, and ship the best on a joint dev set only if neither task drops more than an agreed margin versus its single adapter.

**Code:** (executed, standalone, numpy only; synthetic toy, not a model)
```python
# Standalone, numpy only. TOY: random "task vectors" (fine-tuned minus base), not real models.
# Two tasks: each has its own important coordinates, plus a shared block where their signs are opposed.
import numpy as np
rng = np.random.default_rng(0)
n, T = 10000, 2
idx = rng.permutation(n)
shared, own = idx[:1500], [idx[1500:2500], idx[2500:3500]]          # disjoint own-coordinate sets
tv = np.zeros((T, n))
for t in range(T):
    tv[t] = rng.normal(0, 0.02, n)                                  # small noise everywhere
    tv[t, own[t]] += rng.choice([-1, 1], 1000) * rng.uniform(0.5, 1.0, 1000)
    tv[t, shared] += (1 if t == 0 else -1) * rng.uniform(0.5, 1.0, 1500) * (1.2 if t == 0 else 1.0)  # opposed signs, task 0 a bit stronger

def retention(merged, t, coords):                                   # fraction of task t's delta kept on these coords (1.0 = all)
    v = tv[t, coords]; return float(merged[coords] @ v / (v @ v))

def ties_merge(tv, keep=0.2):
    trimmed = np.zeros_like(tv)
    for i, v in enumerate(tv):                                      # 1) trim: keep top-20% magnitude entries
        thr = np.quantile(np.abs(v), 1 - keep); trimmed[i] = np.where(np.abs(v) >= thr, v, 0)
    elected = np.sign(trimmed.sum(0))                               # 2) elect sign by total mass
    agree = (np.sign(trimmed) == elected) & (trimmed != 0)          # 3) keep only entries that agree
    return (trimmed * agree).sum(0) / np.maximum(agree.sum(0), 1)   # disjoint mean over agreeing entries

methods = {"naive average (1/2 each)": tv.mean(0), "task-vector sum (scale 1)": tv.sum(0), "TIES-style": ties_merge(tv)}
print(f"{'method':<28}{'task0 own':>10}{'task1 own':>10}{'task0 shared':>14}{'task1 shared':>14}")
for name, m in methods.items():
    print(f"{name:<28}{retention(m,0,own[0]):>10.2f}{retention(m,1,own[1]):>10.2f}{retention(m,0,shared):>14.2f}{retention(m,1,shared):>14.2f}")

```

**Follow-ups:**
- *Why do LoRA deltas merge differently from full deltas?* Each LoRA delta is a low-rank B·A. Merging adapters by averaging A and B separately is not the same as averaging the products, so implementations differ; I would check how the library combines them.
- *Does merging need data?* Not for training. It does for choosing weights and checking quality.
- *Per-task adapter or merge?* Per-task adapters when tasks conflict or must be updated independently; merge when you need one artefact and the eval says the loss is small.

**Common mistakes:**
- Merging models with different bases and being surprised by garbage.
- Reporting only the average score and missing one collapsed task.
- Using a single λ without a dev-set sweep.
- Saying TIES "solves interference".

### Q42 ⭐ 🔴 Design question: plan a fine-tune of a 13B-70B model on limited GPUs (QLoRA, gradient checkpointing, sharding), including how you validate the plan before spending the compute.
**Asked at:** senior roles at big tech, product, GenAI startups
**Say this first (1 line):** I first do the memory arithmetic on paper, pick the cheapest method that meets the quality bar (QLoRA before LoRA before full fine-tuning), then buy certainty cheaply: a dry run to measure memory and throughput, a tiny overfit run to check the loss, and an eval gate before the full job.

**Then explain:**
- **Step 0, is fine-tuning needed:** prompting or RAG first (Q1). Pick a smaller model if it passes the quality bar.
- **Memory plan, in order of cost:**
  1. QLoRA: frozen 4-bit base, trainable bf16/fp32 adapters (Q6). A 70B base then fits on one 80 GB GPU by weights, with limited room left for activations.
  2. LoRA on a bf16 base: if quality drops with 4-bit, use more GPUs and shard the frozen weights.
  3. Full fine-tuning: about 16 bytes per parameter before activations (Part 2 Q34), so only with sharding (FSDP or ZeRO-3) across many GPUs.
- **Activations:** gradient checkpointing (recompute instead of store, at the cost of extra forward compute), shorter max sequence length, micro-batch size 1 to a few with gradient accumulation to reach the effective batch size, and packing or length bucketing to avoid padding waste (check TRL docs for packing options).
- **Sharding:** FSDP/ZeRO-3 shard weights, gradients and optimizer state across GPUs (Part 2 Q34); with adapters only the adapter state is small, so sharding mainly helps when the bf16 base does not fit on one GPU. Details differ across libraries and QLoRA+FSDP setups; check the current docs.
- **Validate before spending:**
  1. Smoke test on 50 to 200 examples for a few steps: checks the data pipeline, chat template, label masking (Q37), saving and loading.
  2. Dry run at the real sequence length and micro-batch: record peak GPU memory and tokens per second, then extrapolate time and cost = tokens / throughput x GPU price. Try the worst-case (longest) batch first, because OOM often hits on one long example.
  3. Overfit test: 8 to 32 examples, loss should go close to zero. If not, there is a bug.
  4. Eval gate: baseline numbers on the held-out set *before* training; a pass/fail threshold written down in advance (task metric plus a general regression set, Q8).
  5. Checkpoint every N steps, save optimizer state to resume, and test one resume.
- **Run controls:** log loss, grad norm, LR, memory, tokens/s; stop on NaN or spikes; fix seeds; keep the config in version control.
- **Estimator:** below. The accounting is *assumed*: 4-bit weights ~0.55 byte/param (0.5 plus an assumed quantisation overhead), adapter weights and Adam states 16 byte/param in fp32, 90% of an 80 GB GPU usable, Llama-style shapes written from memory. It ignores activations, the KV/activation memory of long sequences, CUDA context and fragmentation, so it is a floor.

| Model (assumed shapes) | bf16 weights | 4-bit weights | 80 GB GPUs for weights only (bf16 / 4-bit) | LoRA r=16 adapter + states | Full FT states |
|---|---|---|---|---|---|
| 13B-like | 26.0 GB | 7.2 GB | 1 / 1 | 63M params, 1.0 GB | 208 GB (3 GPUs) |
| 70B-like | 140.0 GB | 38.5 GB | 2 / 1 | 207M params, 3.3 GB | 1,120 GB (16 GPUs) |

**Example:** 70B QLoRA on one 80 GB card: weights about 38.5 GB + adapter states 3.3 GB leave roughly 30 GB (of the 72 GB I assume usable) for activations. With checkpointing and a micro-batch of 1 at 2,048 tokens it may fit; the dry run tells me, not my estimate. If it does not, I cut sequence length, move to two GPUs with sharding, or choose the 13B model.

**Code:** (executed, standalone, pure Python; ASSUMED accounting, estimate not measurement)
```python
# Standalone, pure Python. ASSUMED accounting, an estimate for planning, NOT a measurement.
# Model shapes are Llama-style numbers written from memory (13B-like and 70B-like); verify against your config.json.
import math
GB = 1e9
MODELS = {  # params, layers, hidden, ffn, kv_dim
    "13B-like": dict(n=13.0e9, L=40, d=5120, ffn=13824, kv=5120),
    "70B-like": dict(n=70.0e9, L=80, d=8192, ffn=28672, kv=1024),
}
ASSUME = dict(bf16=2.0, nf4=0.5 + 0.05,       # 4-bit weights ~0.5 B/param + ~0.05 B/param quant constants (assumed)
              adapter_state=16.0,             # fp32 adapter weights 4 + grads 4 + Adam m,v 8 (assumed)
              full_ft=16.0,                   # mixed-precision Adam accounting from Part 2 Q34
              gpu_gb=80, usable=0.90)         # assume 90% of 80 GB is usable for tensors

def lora_params(m, r):
    d, ffn, kv = m["d"], m["ffn"], m["kv"]
    per_layer = sum(r * (i + o) for i, o in [(d, d), (d, kv), (d, kv), (d, d), (d, ffn), (d, ffn), (ffn, d)])
    return per_layer * m["L"]

def plan(name, r=16):
    m = MODELS[name]; n = m["n"]
    w_bf16, w_nf4 = n * ASSUME["bf16"] / GB, n * ASSUME["nf4"] / GB
    lp = lora_params(m, r); adapter_gb = lp * ASSUME["adapter_state"] / GB
    full = n * ASSUME["full_ft"] / GB
    cap = ASSUME["gpu_gb"] * ASSUME["usable"]
    gpus = lambda gb: math.ceil(gb / cap)
    print(f"{name}: {n/1e9:.0f}B params")
    print(f"  weights bf16 {w_bf16:6.1f} GB -> {gpus(w_bf16)} x 80GB GPUs (weights only)")
    print(f"  weights 4-bit {w_nf4:5.1f} GB -> {gpus(w_nf4)} x 80GB GPU  (weights only)")
    print(f"  LoRA r={r}: {lp/1e6:.0f}M adapter params ({100*lp/n:.2f}% of base), adapter+optimizer state {adapter_gb:.1f} GB")
    print(f"  full FT states (16 B/param) {full:7.0f} GB -> {gpus(full)} x 80GB GPUs before activations")
    print(f"  QLoRA floor (4-bit weights + adapter state) {w_nf4 + adapter_gb:.1f} GB; activations, CUDA context, fragmentation are EXTRA")

for k in MODELS: plan(k)

```

**Follow-ups:**
- *What if the dry run OOMs?* In order: shorter max length, micro-batch down, gradient checkpointing on, smaller r or fewer target modules, 4-bit if not already, then more GPUs and sharding.
- *How do you pick the learning rate?* Start from the adapter norm in the TRL docs (about 1e-4 for adapters per the docs I read), run a short sweep on the overfit set or a small subset, and look at the loss and eval curves.
- *How do you know it is worth the money?* Compare against the prompted baseline and the smaller model on the same eval, with cost per 1,000 requests (Part 10 for serving).

**Common mistakes:**
- Estimating only weights and forgetting activations and the optimizer.
- Launching the full job without a dry run on the longest batch.
- No resume test, so a crash at hour 20 wastes the run.
- Quoting a memory number without saying what it assumes.
