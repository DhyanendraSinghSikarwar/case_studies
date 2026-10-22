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
