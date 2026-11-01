### Q13 ⭐⭐⭐ 🟡 How do you merge a LoRA adapter into the base model? Why does a merged LoRA add no latency, why can't a QLoRA adapter be merged directly, and when would you keep adapters separate?
**Asked at:** product, GenAI startups, inference/platform teams
**Say this first (1 line):** To merge, I compute W' = W + (alpha/r)·B·A once and replace the base weight, so the layer is a plain matrix again and the adapter costs nothing at inference; for QLoRA the base is 4-bit, so I dequantize to 16-bit first, merge there, and keep adapters separate when I need many tasks on one base.

**Then explain:**
- **Why zero latency:** unmerged, the layer does `Wx + (alpha/r)·B(Ax)`, which is two extra small matmuls and an add. Merged, it is one matmul with W', the same shape and cost as the original. The LoRA paper's claim is exactly this: no extra inference latency, unlike bottleneck adapters (Q18).
- **How, in PEFT** (names from the PEFT LoRA guide opened 2026-10-22, check the current docs, these change): `merge_and_unload()` merges and returns a standalone base model with no adapter wrappers; `merge_adapter()` / `unmerge_adapter()` merge in place and undo it, so you can toggle; `add_weighted_adapter()` combines several adapters into a new one.
- **QLoRA:** the base is stored in 4-bit (NF4, Q6). The adapter was trained against the *dequantized* base. A prep article says you cannot merge into the 4-bit base without dequantizing. So: load the base in 16-bit, apply the adapter, merge, save. If you merge and then re-quantize, you add a second rounding error on top (demo below). Some library versions may allow merging into quantized layers with rounding error; I would check the docs and compare outputs before trusting it.
- **Keep adapters separate when:** many tenants or tasks share one base (swap a few MB of adapter per request instead of hosting many 14 GB copies), A/B testing adapters, you may want to roll back, or you want to blend adapters. Merge when you ship one fixed model and want the simplest, fastest serving path (deployment detail is Part 10).

**Example (toy, run):** the merged and unmerged outputs differ by about 1e-5, which is float32 rounding noise. With a toy 4-bit quantizer (uniform, per-row absmax; NOT NF4), dequantize-then-merge in 16-bit matches what training saw (error ~1e-5), while merge-then-requantize gives a max output error of 1.36 on this toy. The exact size depends on the quantizer; the direction is the point.

**Code:** (executed, torch CPU)
```python
import torch, torch.nn.functional as F
torch.manual_seed(0)
d_in, d_out, r, alpha = 64, 32, 8, 16
W = torch.randn(d_out, d_in)
A = torch.randn(r, d_in) * 0.1
B = torch.randn(d_out, r) * 0.1          # nonzero B, as after training
x = torch.randn(5, d_in)
scale = alpha / r

unmerged = F.linear(x, W) + scale * F.linear(F.linear(x, A), B)   # two extra matmuls
W_merged = W + scale * (B @ A)                                    # one-off merge
merged = F.linear(x, W_merged)                                    # same cost as the base layer
print("max |merged - unmerged| =", (merged - unmerged).abs().max().item())
print("allclose:", torch.allclose(merged, unmerged, atol=1e-5))
W_back = W_merged - scale * (B @ A)                               # unmerge
print("unmerge error:", (W_back - W).abs().max().item())

# TOY 4-bit quantizer (uniform, per-row absmax; NOT NF4, just to show the effect)
def toy_q4(w):
    s = w.abs().amax(dim=1, keepdim=True) / 7
    return torch.round(w / s).clamp(-8, 7) * s
Wq = toy_q4(W)                                  # the frozen 4-bit base (dequantized view)
y_ref = F.linear(x, W) + scale * F.linear(F.linear(x, A), B)       # what training saw (fp base, adapter)
y_train = F.linear(x, Wq) + scale * F.linear(F.linear(x, A), B)    # QLoRA training view: quantized base + adapter
W_deq_merged = Wq + scale * (B @ A)             # dequantize -> merge into 16-bit copy: exact w.r.t. training view
W_requant = toy_q4(W_deq_merged)                # merge then re-quantize: extra error
e_deq = (F.linear(x, W_deq_merged) - y_train).abs().max().item()
e_req = (F.linear(x, W_requant) - y_train).abs().max().item()
print(f"dequantize+merge (16-bit) error vs training view: {e_deq:.2e}")
print(f"merge then re-quantize error vs training view:   {e_req:.2e}")
```
Output from my run:
```
max |merged - unmerged| = 9.5367431640625e-06
allclose: True
unmerge error: 1.1920928955078125e-07
dequantize+merge (16-bit) error vs training view: 9.54e-06
merge then re-quantize error vs training view:   1.36e+00
```

**Follow-ups:**
- *Can you unmerge?* Yes, subtract the same term; tiny float error accumulates if you merge and unmerge many times, so keep the original weights if exactness matters.
- *Does merging change quality?* Mathematically no (same function), except in low precision: merging into bf16 weights rounds the small update.
- *Many adapters on one base?* Serve them unmerged and route per request (multi-adapter serving, Part 10).

**Common mistakes:** Saying merging "adds the adapter weights" (it adds the product B·A scaled by alpha/r); forgetting the scaling factor; merging into an already-quantized base and not measuring the error; merging when you needed per-tenant adapters; merging twice by accident.

### Q14 ⭐⭐⭐ 🟡 Code: implement a LoRA linear layer from scratch in PyTorch (frozen weight, A and B initialisation, alpha/r scaling, merge) and verify it against W + BA.
**Asked at:** product, big tech, live-coding rounds
**Say this first (1 line):** The layer keeps the pretrained weight W frozen, adds two small trainable matrices A (r x in) and B (out x r) with B starting at zero, computes `Wx + (alpha/r)·B(A(drop(x)))`, and can fold the update into W for inference.

**Then explain:**
- **Init:** A is Kaiming-uniform with `a=sqrt(5)` (what `nn.Linear` uses), B is zeros. So B·A = 0 and the layer equals the base at step 0; training starts from the pretrained behaviour (PEFT LoRA guide). If both were zero, no gradient would flow; with B zero and A random, B gets a gradient immediately.
- **Scaling:** `alpha / r`, so changing r does not by itself rescale the update (Q4). rsLoRA uses `alpha/sqrt(r)` (Q19).
- **Dropout** is applied to the input of the adapter branch only, not to the frozen path.
- **Merge/unmerge:** `W += scaling · B@A` and the reverse (Q13).
- Only A and B have `requires_grad=True`; the optimizer sees only those.

**Example (run):** a 256 to 128 layer with r=8 has 3,072 trainable parameters (A: 8x256, B: 128x8) out of 35,840 in total, 8.57% of this single layer (the base is 128x256 = 32,768; for a big layer the share is far smaller, see Q18). Output equals the base at init, loss falls from 0.996 to 0.094 on synthetic data, and the merged output equals the unmerged output to float tolerance.

**Code:** (executed, torch CPU; the "pretrained" weight is random, the data is synthetic)
```python
import math, torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)

class LoRALinear(nn.Module):
    def __init__(self, in_f, out_f, r=8, alpha=16, dropout=0.0, bias=False):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_f, in_f) * 0.1, requires_grad=False)  # frozen base (stand-in for pretrained)
        self.bias = nn.Parameter(torch.zeros(out_f), requires_grad=False) if bias else None
        self.A = nn.Parameter(torch.empty(r, in_f))
        self.B = nn.Parameter(torch.zeros(out_f, r))
        nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))       # same init as nn.Linear's weight
        self.scaling = alpha / r
        self.drop = nn.Dropout(dropout)
        self.merged = False
    def forward(self, x):
        out = F.linear(x, self.weight, self.bias)
        if not self.merged:
            out = out + self.scaling * F.linear(F.linear(self.drop(x), self.A), self.B)
        return out
    @torch.no_grad()
    def merge(self):
        if not self.merged:
            self.weight += self.scaling * (self.B @ self.A); self.merged = True
    @torch.no_grad()
    def unmerge(self):
        if self.merged:
            self.weight -= self.scaling * (self.B @ self.A); self.merged = False

layer = LoRALinear(256, 128, r=8, alpha=16, dropout=0.1)
tot = sum(p.numel() for p in layer.parameters())
trn = sum(p.numel() for p in layer.parameters() if p.requires_grad)
print(f"trainable {trn} / total {tot} = {trn/tot:.2%}")

x = torch.randn(10, 256)
layer.eval()
print("init: output == base output:", torch.equal(layer(x), F.linear(x, layer.weight)))

# synthetic regression: a hidden low-rank update the adapter should learn
W_true = layer.weight.detach() + 0.5 * torch.randn(128, 4) @ torch.randn(4, 256) / 16
X = torch.randn(512, 256); Y = F.linear(X, W_true)
opt = torch.optim.Adam([p for p in layer.parameters() if p.requires_grad], lr=1e-2)
layer.train()
for step in range(201):
    loss = F.mse_loss(layer(X), Y)
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 100 == 0: print(f"step {step:3d} loss {loss.item():.4f}")
print("base weight unchanged by training: grads on base are None ->", layer.weight.grad is None)

layer.eval()
y_un = layer(x)
w_eff = layer.weight + layer.scaling * (layer.B @ layer.A)
print("unmerged == F.linear(x, W + sBA):", torch.allclose(y_un, F.linear(x, w_eff), atol=1e-5))
layer.merge(); y_m = layer(x)
print("merged   == unmerged:", torch.allclose(y_m, y_un, atol=1e-5), "max diff", (y_m - y_un).abs().max().item())
layer.unmerge(); print("unmerge restores:", torch.allclose(layer(x), y_un, atol=1e-5))
```
Output from my run:
```
trainable 3072 / total 35840 = 8.57%
init: output == base output: True
step   0 loss 0.9961
step 100 loss 0.1005
step 200 loss 0.0944
base weight unchanged by training: grads on base are None -> True
unmerged == F.linear(x, W + sBA): True
merged   == unmerged: True max diff 9.5367431640625e-07
unmerge restores: True
```
The loss stops near 0.09 after 200 steps (dropout is active while training); I did not tune this toy, so do not read anything into the exact value.

**Follow-ups:**
- *Why not init B randomly too?* The model would start off from a random perturbation of the pretrained weights, which can damage it.
- *How do you save only the adapter?* Save the state dict entries for A and B (PEFT does this for you).
- *What changes for a Conv or Embedding layer?* Same idea with a low-rank update on the weight; PEFT has separate classes (details: check the docs).

**Common mistakes:** Zero-initialising both A and B; forgetting to freeze W; applying dropout to the frozen path; wrong scaling (r/alpha); merging twice (check a `merged` flag); calling `.merge()` before training and then training the merged copy.

### Q15 ⭐⭐⭐ 🟡 Code: implement the SFT loss with prompt masking in PyTorch (shifted labels, ignore index) and check it against F.cross_entropy.
**Asked at:** product, big tech, live-coding rounds
**Say this first (1 line):** Build `labels` as a copy of `input_ids` with prompt and padding positions set to -100, shift so the logits at position t are scored against the label at t+1 (`logits[:, :-1]` vs `labels[:, 1:]`), and let `F.cross_entropy(..., ignore_index=-100)` average over the remaining response tokens.

**Then explain:**
- **Why the shift:** a causal LM at position t predicts token t+1. Without the shift you score the model on copying its own input.
- **Why -100:** it is PyTorch's default `ignore_index`, and the TRL SFT docs describe the same token-level NLL with one-token shift and ignore index -100. Masked positions contribute no loss and no gradient. The prompt is masked so the model is trained to produce responses, not to model user text (Q2, Q12). TRL has options such as `completion_only_loss` and `assistant_only_loss` (check the current docs, these change).
- **Mean vs sum:** the default is the mean over unmasked tokens, so the loss scale does not depend on batch length; `reduction="sum"` grows with the number of tokens and needs the learning rate or normalisation adjusted.
- **Token-level vs sequence-level averaging:** token-level mean (the default across the batch) gives every response token the same weight, so a long response contributes more total gradient than a short one. Sequence-level (mean per sequence, then mean of means) gives each example equal weight, so short answers get a larger per-token weight. Neither is "right"; it changes what the model learns, and it also matters when gradient accumulation splits a batch unevenly.

**Example (run):** two sequences, responses of 2 and 10 tokens (random logits stand in for a model). Token-mean 3.4477, sequence-mean 3.5711, sum 41.372. The long sequence gets 2.17x the gradient norm of the short one under token-level averaging, but 0.43x under sequence-level. (Not 5x, because gradient norms of independent token terms add roughly like a square root.)

**Code:** (executed, torch CPU)
```python
import torch, torch.nn.functional as F
torch.manual_seed(0)
V, IGN = 20, -100
# 2 sequences: prompt tokens then response tokens; seq 2 has a LONG response. Pad to length 14 with ignore.
def make(prompt_len, resp_len, total):
    ids = torch.randint(0, V, (total,))
    labels = ids.clone()
    labels[:prompt_len] = IGN                 # mask the prompt: no loss on it
    labels[prompt_len + resp_len:] = IGN      # mask padding
    return ids, labels
(i1, l1), (i2, l2) = make(4, 2, 14), make(4, 10, 14)
input_ids, labels = torch.stack([i1, i2]), torch.stack([l1, l2])
logits = torch.randn(2, 14, V, requires_grad=True)       # stand-in for model output

# shift: logits at position t predict token t+1
sl, st = logits[:, :-1, :], labels[:, 1:]
loss = F.cross_entropy(sl.reshape(-1, V), st.reshape(-1), ignore_index=IGN)   # mean over unmasked tokens

# manual NLL
logp = torch.log_softmax(sl, dim=-1)
mask = st != IGN
nll = -logp.gather(-1, st.clamp(min=0).unsqueeze(-1)).squeeze(-1)
manual = (nll * mask).sum() / mask.sum()
print("F.cross_entropy:", round(loss.item(), 6), " manual:", round(manual.item(), 6),
      " equal:", torch.allclose(loss, manual))
print("unmasked tokens per sequence:", mask.sum(1).tolist())

# sum vs mean, token-level vs sequence-level averaging
summed = F.cross_entropy(sl.reshape(-1, V), st.reshape(-1), ignore_index=IGN, reduction="sum")
per_seq = (nll * mask).sum(1) / mask.sum(1)
print("sum:", round(summed.item(), 3), " token-mean:", round(manual.item(), 4),
      " seq-mean:", round(per_seq.mean().item(), 4))
# gradient share: how much of the total gradient norm^2 does each sequence get?
for name, l in [("token-level", manual), ("sequence-level", per_seq.mean())]:
    g, = torch.autograd.grad(l, logits, retain_graph=True)
    n = g.pow(2).sum((1, 2)).sqrt()
    print(f"{name:15s} grad norm per seq: short {n[0]:.4f}  long {n[1]:.4f}  long/short {n[1]/n[0]:.2f}")

# what if you forget the shift or the mask?
bad = F.cross_entropy(logits.reshape(-1, V), labels.reshape(-1), ignore_index=IGN)
print("no shift (wrong) loss:", round(bad.item(), 4))
```
Output from my run:
```
F.cross_entropy: 3.447694  manual: 3.447694  equal: True
unmasked tokens per sequence: [2, 10]
sum: 41.372  token-mean: 3.4477  seq-mean: 3.5711
token-level     grad norm per seq: short 0.1228  long 0.2660  long/short 2.17
sequence-level  grad norm per seq: short 0.3685  long 0.1596  long/short 0.43
no shift (wrong) loss: 3.4893
```
The no-shift number is just a different, meaningless loss on random logits. On a real model, a missing shift usually shows up as an implausibly easy loss (the target is the token already in the input), but I did not run that here.

**Follow-ups:**
- *Do you mask padding too?* Yes, set it to -100 (or use the attention mask); the demo does this.
- *Where does the EOS token go?* It is part of the response and must be unmasked, otherwise the model never learns to stop, and it must match the chat template.
- *Loss is NaN?* Usually a batch where every label is -100, so the mean divides by zero; drop or guard such batches.

**Common mistakes:** Forgetting the shift or shifting twice; masking the EOS; computing the mean by hand with the wrong denominator (batch size instead of unmasked tokens); comparing losses across runs that average differently; applying `ignore_index` to the logits instead of the labels.

### Q16 ⭐⭐ 🟡 Full fine-tuning vs parameter-efficient fine-tuning: when is full fine-tuning justified, and how do learning rates differ?
**Asked at:** product, GenAI startups, big tech
**Say this first (1 line):** I default to PEFT (LoRA) because it is cheaper, safer against forgetting and easy to store per task, and I move to full fine-tuning only when the behaviour or domain shift is large, I have lots of good data, and the hardware budget allows it; full FT uses a much smaller learning rate (about 1e-5 to 3e-5) than adapters (about 1e-4).

**Then explain:**
| | PEFT (LoRA/QLoRA) | Full fine-tuning |
|---|---|---|
| Trainable params | small adapters (Q18) | all weights |
| Memory | weights + small optimizer state (memory maths: Q7, Part 2 Q34) | about 16 bytes/param with mixed-precision Adam, before activations |
| Storage per task | MBs per adapter, one shared base | a full model copy per task |
| Forgetting | usually less drift, not zero (Q8) | higher risk, base weights move |
| LR | about 1e-4 (TRL docs) | 1e-5 to 3e-5 (prep article); TRL `SFTConfig` default 2e-5 |
| Capacity | limited by rank (Q20) | highest |

- **When full FT is justified:** a large behaviour or domain shift, a big, clean dataset, a quality gap that LoRA at higher rank and all-linear targets did not close (Q20), and enough GPUs (sharding, Q34 in Part 2). Also when you will continue pretraining, or serve a single model where per-task adapters bring no benefit.
- **Why the LR differs:** LoRA's B starts at zero and the update is scaled by alpha/r, so the adapter needs bigger steps to move; in full FT every weight moves at once, so a large LR wrecks pretrained knowledge. Both numbers are starting points, not laws; sweep them.
- **Forgetting:** mitigations are the same either way (lower LR, fewer epochs, mix in general data, evaluate on a held-out general set, Q8). Research I recall (hedge, from memory) reports that LoRA learns less and also forgets less than full FT; do not quote it as settled.
- **Practical rule (judgement):** start LoRA/QLoRA; measure on your task and a general regression set; escalate only if the gap is real. A 2026 prep article also says full FT is "rarely" the right call for most applied roles.

**Example:** one 7B base plus 20 customer-specific tasks. Full FT: 20 copies of about 14 GB in bf16 = about 280 GB to store and deploy. LoRA r=16 on all linear layers: 20 adapters of tens of MB each (rough, depends on targets) on top of one 14 GB base. These are my own back-of-envelope numbers, not measured.

**Follow-ups:**
- *Same LR for LoRA and full FT?* No: ~1e-4 vs ~2e-5 are the commonly cited starting points; the TRL docs say adapters use higher LR (check the current docs).
- *Can LoRA match full FT?* On many tasks, yes (LoRA paper reports on-par or better on several benchmarks); on large shifts or new capabilities it can lag.
- *What about the middle path?* Train only some layers, or use a higher rank first.

**Common mistakes:** Using LoRA's 1e-4 on full FT (instability, forgetting); calling full FT "better" without measuring; ignoring storage and serving cost per task; not evaluating general capability after either method.

### Q17 ⭐⭐ 🟡 What hyperparameters matter in SFT (learning rate, epochs, batch size, warmup, scheduler, max length), and how do you recognise overfitting?
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** The ones that matter most are learning rate, number of epochs (how much you repeat the data), effective batch size, and data quality; I watch training and validation loss together, and if training loss keeps falling while validation loss turns up, I am overfitting and I roll back to the best checkpoint.

**Then explain:**
- **Learning rate:** the most sensitive knob. About 1e-5 to 3e-5 for full FT, about 1e-4 for adapters as starting points (Q16). Add warmup and a decay schedule (cosine or linear); warmup stops early noisy steps from damaging the model.
- **Epochs:** SFT datasets are small, so 1 to 3 passes is typical; more passes memorise the data. Fewer epochs on more data beats many epochs on little data.
- **Batch size:** use gradient accumulation to get an effective batch of tens of sequences; too small is noisy, very large needs a higher LR.
- **Max length:** truncation silently cuts responses (and the EOS); set it to cover your data and check how many examples are cut. Packing and padding-free options exist in TRL (check the docs).
- **Gradient clipping** (norm 1.0 is a common default) and weight decay are minor knobs.
- **Library defaults are not recommendations.** TRL `SFTConfig` defaults as I read them in the docs on 2026-10-22: `learning_rate` 2e-5, `num_train_epochs` 3.0, `max_length` 1024, `weight_decay` 0.0, `max_grad_norm` 1.0. They differ across versions; check the current docs, these change.
- **Overfitting signs:** the validation-loss minimum is passed while train loss keeps dropping; the train/val gap widens; outputs repeat training phrases; general benchmarks drop (Q8); task metric on a held-out set stops improving even if loss moves. Validation loss is only a proxy: the final call is the task metric plus a general regression check.

**Example (SYNTHETIC curves, made up from formulas, not a real run):** train loss falls every epoch; validation loss bottoms at epoch 3 (1.154) and then rises. A patience-2 rule stops after epoch 5, and I keep the epoch-3 checkpoint.

**Code:** (executed, numpy; the curves are synthetic)
```python
# SYNTHETIC curves (made up from formulas, not a real training run)
import numpy as np
rng = np.random.default_rng(0)
epochs = np.arange(1, 9)
train = 2.0 * np.exp(-0.45 * epochs) + 0.15 + rng.normal(0, 0.01, 8)          # keeps falling
val = 1.1 + 0.9 * np.exp(-0.9 * epochs) + 0.035 * np.maximum(epochs - 3, 0) ** 1.3 + rng.normal(0, 0.01, 8)
def pick_epoch(val, patience=2, min_delta=0.005):
    best, best_ep, bad = np.inf, 0, 0
    for e, v in enumerate(val, 1):
        if v < best - min_delta: best, best_ep, bad = v, e, 0
        else:
            bad += 1
            if bad >= patience: break
    return best_ep, best, e
print("epoch  train   val   gap")
for e, t, v in zip(epochs, train, val): print(f"{e:5d} {t:6.3f} {v:6.3f} {v-t:6.3f}")
be, bv, stop = pick_epoch(val)
print(f"best epoch {be} (val {bv:.3f}); early-stopping with patience 2 would stop after epoch {stop}")
```
Output from my run:
```
epoch  train   val   gap
    1  1.427  1.459  0.032
    2  0.962  1.236  0.274
    3  0.675  1.154  0.479
    4  0.482  1.160  0.678
    5  0.355  1.173  0.817
    6  0.288  1.248  0.960
    7  0.249  1.301  1.053
    8  0.214  1.377  1.163
best epoch 3 (val 1.154); early-stopping with patience 2 would stop after epoch 5
```

**Follow-ups:**
- *Validation loss up but task metric fine?* Possible (loss and generation quality are different); trust the task metric, but keep an eye on calibration and diversity.
- *How big should the validation set be?* Large enough that its noise is smaller than the differences you care about; hold out by source or time to avoid leakage (Q21).
- *Loss spikes?* Lower the LR, check the data for bad examples, use clipping.

**Common mistakes:** Copying library defaults as if they were tuned; tracking only train loss; no validation split; validation set leaking from train (duplicates); not saving the best checkpoint; truncating away the EOS.

### Q18 ⭐⭐ 🟡 Compare PEFT methods: adapters, prefix tuning, prompt tuning, IA3 and LoRA. When would you use each?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** PEFT methods freeze the base model and train a tiny set of extra parameters; they differ in where those parameters live (inserted modules, input vectors, rescaling vectors, low-rank weight updates), and LoRA became the default because it is simple, strong and can be merged for zero inference overhead.

**Then explain:**
| Method | What is trained | Inference cost | Notes |
|---|---|---|---|
| Adapters | small bottleneck modules inserted in each block | extra layers, so extra latency | LoRA paper contrasts itself with this |
| Prefix tuning | learned vectors prepended to the keys/values of each layer | longer sequence | uses context length |
| Prompt tuning | learned "soft prompt" embeddings at the input only | longer sequence | lightest; may lag on smaller models or hard tasks (from memory, hedge) |
| IA3 | learned scaling vectors on keys, values and FFN activations | merge-able in principle (multiplicative; from memory) | very few parameters |
| LoRA | low-rank A, B added to weight matrices | zero when merged (Q13) | default choice, all-linear targets (Q5) |
| DoRA | magnitude and direction, LoRA on direction (Q19) | merge-able | reported gains, treat as reported |
| QLoRA | LoRA on a 4-bit base (Q6) | needs dequantize to merge | memory saving, slower training than plain LoRA |
- NVIDIA's NeMo PEFT docs list LoRA, DoRA, QLoRA, IA3, adapters and prefix/prompt tuning as supported methods (I saw this in a search snippet, did not open the page). I am not quoting the parameter-percentage tables from third-party comparison pages because I could not verify them; use the formula counts below.
- **When to use what (judgement):** LoRA/QLoRA by default; IA3 or prompt tuning when you need an extremely small per-task footprint and accept lower ceiling; prefix/prompt tuning when you cannot touch weights but can change inputs; classic adapters mostly for legacy or multi-task research setups.

**Example (computed from formulas, one 4096x4096 layer, assumed config):** full layer 16,777,216 parameters. LoRA r=16: 131,072 (0.78%). DoRA r=16: 135,168 (0.81%). IA3: 4,096 (0.02%). Bottleneck adapter of width 64: 528,448 (3.1%). Prompt tuning with 20 virtual tokens: 81,920 once for the whole model (not per layer). Prefix tuning with 20 tokens: 163,840 per layer (before any reparameterisation trick). The assumptions (d=4096, r=16, 20 tokens, width 64) are mine.

**Code:** (executed)
```python
# Trainable parameters for ONE d x d linear layer (d=4096), formulas only; config assumed
d, r = 4096, 16
n_virtual = 20          # prompt / prefix tokens (assumed)
bottleneck = 64         # adapter bottleneck width (assumed)
layer = d * d
rows = {
 "full fine-tune of this layer": layer,
 "LoRA (r=16): A (r x d) + B (d x r)": r * d + d * r,
 "DoRA (r=16): LoRA + magnitude vector (d)": r * d + d * r + d,
 "IA3: one learned scale vector (d)": d,
 "Bottleneck adapter (64): down d*64 + up 64*d (+biases)": d * bottleneck + bottleneck + bottleneck * d + d,
 "Prompt tuning: 20 soft tokens x d (once per MODEL, not per layer)": n_virtual * d,
 "Prefix tuning: 20 x d for K and V (per layer, before any reparam.)": 2 * n_virtual * d,
}
for k, v in rows.items(): print(f"{k:68s} {v:>11,d}  {v/layer:8.4%} of the layer")
```
Output from my run:
```
full fine-tune of this layer                                          16,777,216  100.0000% of the layer
LoRA (r=16): A (r x d) + B (d x r)                                       131,072    0.7812% of the layer
DoRA (r=16): LoRA + magnitude vector (d)                                 135,168    0.8057% of the layer
IA3: one learned scale vector (d)                                          4,096    0.0244% of the layer
Bottleneck adapter (64): down d*64 + up 64*d (+biases)                   528,448    3.1498% of the layer
Prompt tuning: 20 soft tokens x d (once per MODEL, not per layer)         81,920    0.4883% of the layer
Prefix tuning: 20 x d for K and V (per layer, before any reparam.)       163,840    0.9766% of the layer
```
Parameter count is not memory: with Adam, activations and the frozen base dominate (Q7).

**Follow-ups:**
- *Why not adapters for latency-sensitive serving?* They add sequential layers that cannot be folded into the weights.
- *Why is prompt tuning light but sometimes weak?* Only the input embeddings change, so there is little capacity to change deep behaviour.
- *Can these be combined?* Yes in research (and some libraries), but LoRA alone is usually enough.

**Common mistakes:** Quoting "0.1% of parameters" without a formula or config; saying all PEFT methods are mergeable; confusing prompt engineering with prompt tuning; comparing methods at different parameter budgets without saying so.

### Q19 ⭐⭐ 🟡 What do LoRA variants change (rsLoRA, DoRA, LoRA+, LoftQ initialisation)? When are they worth trying?
**Asked at:** GenAI startups, research-leaning teams, fine-tuning teams
**Say this first (1 line):** The variants tweak one part of LoRA: rsLoRA changes the scaling so higher ranks stay stable, DoRA splits the weight into magnitude and direction, LoRA+ uses different learning rates for A and B, and LoftQ gives a better starting point when the base is quantized; I treat all of them as "try if plain LoRA plateaus", not as defaults.

**Then explain:**
- **rsLoRA:** replaces `alpha/r` with `alpha/sqrt(r)` (PEFT: `use_rslora=True` in `LoraConfig`). With `alpha/r`, the update shrinks as rank grows, so large ranks may learn too slowly; `alpha/sqrt(r)` is intended to keep the update size stable at higher ranks. Worth trying at r of 64 or more.
- **DoRA:** decomposes a weight into a magnitude vector and a direction, and applies LoRA to the direction while training the magnitude separately. NVIDIA's docs describe DoRA this way and claim it can outperform LoRA; I treat that as a reported result, not something I verified. It adds some compute and a small number of parameters (Q18).
- **LoRA+** (from memory, hedge): uses a larger learning rate for B than for A, because the two matrices play different roles; reported to speed up training. Check the paper and your library's support before relying on it.
- **LoftQ:** a LoRA initialisation for quantized bases: it picks the adapter init to compensate for quantization error. The PEFT guide says to use it without quantizing the base first (the library does the quantization as part of initialisation). Check the current docs, these change.
- **How I decide:** get a plain LoRA baseline (all-linear, r=16, Q4/Q5); if it underfits at higher rank, try rsLoRA; if quality is short of full FT, try DoRA; if you train on a 4-bit base and see a quality drop, try LoftQ. Change one thing at a time and compare on the same eval.

**Example (toy, run):** with alpha=16 the standard factor is 1.0 at r=16 and 0.0625 at r=256, a 16x shrink; the rsLoRA factor goes from 4.0 to 1.0, a 4x shrink. In a toy with random B and A whose entries scale like 1/sqrt(d), the size of the scaled update B@A stays near 16 for every r under rsLoRA, while the standard factor lets it fall from 8.0 to 1.0. At real initialisation B=0, so this only illustrates the scaling argument; it is not a training run.

**Code:** (executed, numpy; synthetic)
```python
import math
alpha = 16
print(" r | alpha/r | alpha/sqrt(r)")
for r in [4, 8, 16, 64, 256]:
    print(f"{r:3d} | {alpha/r:7.3f} | {alpha/math.sqrt(r):7.3f}")
# Why: with B,A both random-ish after init, the update B@A sums r terms -> its size grows with r,
# classic scaling alpha/r divides by r (shrinks as r grows), rs scaling divides by sqrt(r).
import numpy as np
rng = np.random.default_rng(0)
d = 512
print("\nsize (Frobenius) of scale * B@A for random unit-variance B/d**.5, A/d**.5 entries (toy):")
for r in [4, 16, 64, 256]:
    B = rng.normal(size=(d, r)) / np.sqrt(d); A = rng.normal(size=(r, d)) / np.sqrt(d)
    base = np.linalg.norm(B @ A)
    print(f"r={r:3d}  raw {base:6.3f}   x alpha/r {alpha/r*base:6.3f}   x alpha/sqrt(r) {alpha/np.sqrt(r)*base:6.3f}")
```
Output from my run:
```
 r | alpha/r | alpha/sqrt(r)
  4 |   4.000 |   8.000
  8 |   2.000 |   5.657
 16 |   1.000 |   4.000
 64 |   0.250 |   2.000
256 |   0.062 |   1.000

size (Frobenius) of scale * B@A for random unit-variance B/d**.5, A/d**.5 entries (toy):
r=  4  raw  1.989   x alpha/r  7.957   x alpha/sqrt(r) 15.915
r= 16  raw  3.959   x alpha/r  3.959   x alpha/sqrt(r) 15.836
r= 64  raw  8.021   x alpha/r  2.005   x alpha/sqrt(r) 16.043
r=256  raw 16.040   x alpha/r  1.002   x alpha/sqrt(r) 16.040
```

**Follow-ups:**
- *Do I need rsLoRA at r=8 or 16?* Probably not; the difference between the two scalings is small at low rank.
- *Is DoRA mergeable?* Yes, it can be merged into the weights for inference (from memory; check the docs).
- *Which variant first?* None until a plain LoRA baseline and data quality are sorted out; data usually matters more.

**Common mistakes:** Treating variants as free wins and skipping a proper baseline; changing several things at once; quoting benchmark gains from a vendor page as if they were general; quantizing the base before using LoftQ init; forgetting that alpha must be retuned when you switch the scaling rule.

### Q20 ⭐⭐ 🟡 Does a higher LoRA rank always help? What limits capacity, and how do you decide when LoRA is not enough?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** No: a higher rank gives the adapter more capacity, but returns diminish quickly because most useful updates are low-rank and the rest is noise or something LoRA's structure cannot express; when higher rank, all-linear targets and better data still fall short, the task needs more than LoRA (full fine-tuning or a different approach).

**Then explain:**
- **What rank limits:** the update is B·A, so its rank is at most r. If the true change you need has most of its energy in a few directions, ranks beyond that add parameters but little signal; extra capacity can also fit noise.
- **Diminishing returns:** like truncated SVD, the first few components capture most of a structured matrix and later ones capture little (demo below). The LoRA paper reports that small ranks already work well on its tasks (from memory; check the paper).
- **Practical rank guidance:** prep article suggests r = 8-16 for small shifts and 64+ for large domain shifts (Q4). Cost grows linearly with r, and high r may need rsLoRA (Q19).
- **Research claims (hedge, from memory):** some papers argue LoRA learns less than full FT on hard, data-rich targets such as code and maths, but also forgets less. Do not state these as settled.
- **When LoRA is not enough:** big domain shift or a new language/modality, new capabilities rather than new style, lots of high-quality data and a clear quality gap versus full FT. The ladder: raise r and target all linear layers, then raise LR/epochs carefully, then continued pretraining or full FT (Q16, Part 2 Q8).
- **Do not blame rank first:** weak data, wrong LR, truncation or bad masking explain most "LoRA is not learning" cases (Q15, Q17).

**Example (SYNTHETIC, run):** a 256x256 matrix with true rank 8 (singular values 10 down to 3) plus noise. Error against the noisy matrix keeps falling slowly with rank because noise is full rank, but error against the clean signal is lowest at rank 8 (0.167) and gets worse beyond it (0.273 at 16, 0.620 at 128), because the extra components fit noise. Parameters grow linearly (4,096 at r=8 vs 65,536 at r=128).

**Code:** (executed, numpy; synthetic)
```python
# SYNTHETIC: a "weight update" with true rank 8 plus small noise
import numpy as np
rng = np.random.default_rng(0)
d, true_r = 256, 8
sv = np.array([10, 9, 8, 7, 6, 5, 4, 3.0])
U = np.linalg.qr(rng.normal(size=(d, true_r)))[0]; V = np.linalg.qr(rng.normal(size=(d, true_r)))[0]
signal = U @ np.diag(sv) @ V.T
noise = 0.05 * rng.normal(size=(d, d))
M = signal + noise
u, s, vt = np.linalg.svd(M)
print(" rank | rel. error vs M | rel. error vs clean signal | params 2*d*r")
for r in [1, 2, 4, 8, 16, 32, 64, 128]:
    Mr = (u[:, :r] * s[:r]) @ vt[:r]
    print(f"{r:5d} | {np.linalg.norm(M-Mr)/np.linalg.norm(M):15.4f} | {np.linalg.norm(signal-Mr)/np.linalg.norm(signal):25.4f} | {2*d*r:6d}")
print("top-12 singular values:", np.round(s[:12], 2))
```
Output from my run:
```
 rank | rel. error vs M | rel. error vs clean signal | params 2*d*r
    1 |          0.9019 |                    0.8603 |    512
    2 |          0.8146 |                    0.7282 |   1024
    4 |          0.6716 |                    0.4902 |   2048
    8 |          0.5305 |                    0.1670 |   4096
   16 |          0.4988 |                    0.2731 |   8192
   32 |          0.4417 |                    0.3893 |  16384
   64 |          0.3419 |                    0.5134 |  32768
  128 |          0.1807 |                    0.6199 |  65536
top-12 singular values: [10.08  9.04  8.09  7.1   6.1   5.18  4.25  3.2   1.57  1.52  1.52  1.5]
```
This is an SVD (best rank-r approximation) of a given matrix, not LoRA training; LoRA's training dynamics differ, so it shows the capacity argument only.

**Follow-ups:**
- *How do you pick r empirically?* Sweep r (for example 8, 16, 64) with the same data and LR and plot the validation metric against r; stop when the curve flattens.
- *Does r change memory much?* Adapter parameters and optimizer state scale with r, but the frozen base still dominates (Q7).
- *Rank per layer?* PEFT supports per-module ranks (`rank_pattern`); useful but a second-order tune.

**Common mistakes:** Assuming more rank always means better; raising r instead of fixing data or LR; comparing ranks at different alpha/r scaling; quoting "LoRA forgets less" as a guarantee; ignoring that the target change may be genuinely high-rank.

### Q21 ⭐⭐ 🟡 How do you create instruction data: human-written, synthetic from a stronger model, self-instruct? What are the quality and licensing risks?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** I mix a small, high-quality human-written seed set with synthetic data generated by a stronger model, then filter hard for quality, dedupe, and check diversity; and I check the licence and terms of the model that produced the data before training on its outputs.

**Then explain:**
- **Human-written:** best quality and the right style, but expensive and slow. Use it for a seed set, an evaluation set, and the hard cases. The LIMA paper (seen via explainers, not opened) argues that about 1,000 curated examples can go far, which supports "quality and diversity over quantity" (Q10).
- **Synthetic from a stronger model:** cheap and scalable. Self-instruct style: start from seed tasks, ask a model to generate new instructions and responses, filter, and repeat. Risks: copies the teacher's mistakes and style, hallucinated facts in the responses, and low diversity (many near-identical prompts).
- **Filtering:** drop empty, too short or too long, truncated or broken-format items; language and PII checks; rule checks (valid JSON, code runs, tests pass); a judge model or reward score with a threshold (judge bias is Part 9); and check answers against ground truth where it exists.
- **Dedup and diversity:** exact and near-duplicate removal (hashing, n-gram or embedding similarity), balance across task types and lengths, and decontaminate against your eval set so you do not train on the test.
- **Licensing and terms:** model providers' terms of use may restrict training another model on their outputs, and datasets have their own licences. I would have legal check the specific provider's terms; I will not state what they say. Data with personal information raises privacy duties too.
- **Evaluate the data, not just the model:** sample and read 50 to 100 rows by hand; a small bad slice can teach the model bad habits.

**Example (run, toy):** 8 raw synthetic items. Rules drop two too-short or empty ones and one refusal boilerplate, and near-duplicate removal (3-gram Jaccard above 0.5, an arbitrary threshold) drops two more, so 3 remain. The numbers come from the demo and show the mechanism only; they are not a quality claim about any real dataset.

**Code:** (executed, pure Python; the items are made-up)
```python
import re
raw = [  # made-up synthetic (instruction, response) pairs
 ("Explain overfitting in two sentences.", "Overfitting is when a model memorises training data and fails on new data. Regularisation and more data help."),
 ("Explain overfitting in two sentences!", "Overfitting is when a model memorises training data and fails on new data. Regularisation and more data help."),
 ("Write a SQL query to count users per city.", "SELECT city, COUNT(*) FROM users GROUP BY city;"),
 ("What is a p-value?", ""),
 ("Summarise the causes of inflation.", "As an AI language model, I cannot help with that."),
 ("Hi", "Hello"),
 ("Give one use of the F1 score.", "F1 balances precision and recall, which matters for imbalanced classes."),
 ("Give one use of the F1-score.", "F1 balances precision and recall, which matters for imbalanced classes."),
]
def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
def shingles(s, n=3):
    t = norm(s).split(); return {tuple(t[i:i+n]) for i in range(max(1, len(t)-n+1))}
def jaccard(a, b): return len(a & b) / max(1, len(a | b))
def rule_ok(i, r):
    if len(r.split()) < 3: return "too short/empty"
    if len(i.split()) < 3: return "prompt too short"
    if r.lower().startswith("as an ai"): return "refusal boilerplate"
    return None
kept, dropped = [], []
for i, r in raw:
    why = rule_ok(i, r)
    if why: dropped.append((i, why)); continue
    sh = shingles(i + " " + r)
    if any(jaccard(sh, k_sh) > 0.5 for _, _, k_sh in kept):
        dropped.append((i, "near-duplicate")); continue
    kept.append((i, r, sh))
print(f"raw {len(raw)} -> kept {len(kept)}")
for i, why in dropped: print("  dropped:", why, "|", i)
```
Output from my run:
```
raw 8 -> kept 3
  dropped: near-duplicate | Explain overfitting in two sentences!
  dropped: too short/empty | What is a p-value?
  dropped: refusal boilerplate | Summarise the causes of inflation.
  dropped: too short/empty | Hi
  dropped: near-duplicate | Give one use of the F1-score.
```

**Follow-ups:**
- *Is synthetic data enough?* For style and format, often; for new facts or hard reasoning, it inherits the teacher's gaps, so verify or ground it.
- *How much data?* Depends on the shift; start small, grow while the validation metric moves (Q17).
- *Can I use an API model's outputs to train my own?* Check that provider's current terms; some restrict it.

**Common mistakes:** Generating a large volume and skipping inspection; no dedup (the model memorises repeated prompts); contaminating the eval set; ignoring terms of use; filtering only by length; letting the same model generate and judge without checks.

### Q22 ⭐⭐ 🟡 What is knowledge distillation? Explain teacher and student, soft targets, temperature and the combined KL plus cross-entropy loss.
**Asked at:** all types; product, GCC
**Say this first (1 line):** Knowledge distillation trains a small student to match a large teacher's output distribution; the teacher's softened probabilities (soft targets) carry more information than a hard label, and the loss mixes a KL term on temperature-softened outputs with the normal cross-entropy on labels.

**Then explain:**
- **Soft targets:** a hard label says "cat". The teacher's distribution says "cat 0.9, lynx 0.07, dog 0.02", which tells the student which wrong classes are similar. That is the extra signal ("dark knowledge", Hinton et al. 2015).
- **Temperature T:** `softmax(z / T)`. T>1 flattens the distribution so the small probabilities become visible; T=1 is normal.
- **Loss:** `L = alpha * T^2 * KL(p_teacher^T || p_student^T) + (1 - alpha) * CE(labels, student)`. Teacher is fixed; only the student is trained.
- **Why T^2:** the gradient of the soft term shrinks by about 1/T^2 as T grows, so multiplying by T^2 keeps its size comparable to the hard-label term (verified numerically below).
- **alpha:** tutorials often use about 0.5 to 0.9 (hedge: this is common tutorial practice, not a rule); tune it on validation. T is also tuned, often 2 to 4 in classic tutorials.
- **LLM note:** for LLM distillation the snippet-level sources I saw say tau = 1 is often used (the temperature trick is common in classification-era tutorials); hedge, details in Q23.
- Book 1 covers the serving motivation (B1P08-Q55, B1P09-Q47); this answer is the loss and mechanics.

**Example (run, synthetic):** with random logits, the soft-term gradient norm without T^2 is 0.0469, 0.0152, 0.0040, 0.0010 for T = 1, 2, 4, 8; with T^2 it is 0.0469, 0.0607, 0.0637, 0.0620, so it stays comparable. In a toy 4-class XOR-like problem with 2-D inputs, a teacher (2x32 hidden units, 98.9% test accuracy) labels 500 extra unlabelled points; a tiny student (12 hidden units) trained on 60 labelled points reaches mean 94.2% test accuracy over 3 seeds, and with distillation 98.6%. Note the distilled student also sees 500 extra inputs that the teacher labelled, so the gain mixes soft targets and extra unlabelled data; I did not separate the two.

**Code:** (executed, torch CPU; synthetic data, 3 seeds)
```python
import torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)

# loss = alpha * T^2 * KL(softmax(t/T) || softmax(s/T)) + (1 - alpha) * CE(s, y)

# 1) why T^2: gradient of the soft-target term w.r.t. student logits shrinks like 1/T^2
t = torch.randn(256, 10) * 3
for T in [1, 2, 4, 8]:
    s = torch.randn(256, 10, requires_grad=True)
    kl = F.kl_div(F.log_softmax(s / T, -1), F.softmax(t / T, -1), reduction="batchmean")
    g1, = torch.autograd.grad(kl, s)
    s2 = s.detach().clone().requires_grad_(True)
    kl2 = T**2 * F.kl_div(F.log_softmax(s2 / T, -1), F.softmax(t / T, -1), reduction="batchmean")
    g2, = torch.autograd.grad(kl2, s2)
    print(f"T={T}: grad norm without T^2 {g1.norm():.4f}   with T^2 {g2.norm():.4f}")

# 2) toy teacher/student on synthetic 2-D, 4-class data (3 seeds)
def data(n):
    x = torch.randn(n, 2) * 2
    y = ((x[:, 0] > 0).long() * 2 + (x[:, 0] * x[:, 1] > 0).long())     # XOR-like, 4 classes
    return x, y
xtr, ytr = data(60); xte, yte = data(2000)
xun, _ = data(500)                                     # unlabeled data the teacher can label
teacher = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 4))
big_x, big_y = data(1000)
opt = torch.optim.Adam(teacher.parameters(), 1e-2)
for _ in range(200):
    opt.zero_grad(); F.cross_entropy(teacher(big_x), big_y).backward(); opt.step()
with torch.no_grad(): print("teacher test acc", (teacher(xte).argmax(1) == yte).float().mean().item())

def train_student(mode, seed):
    torch.manual_seed(seed)
    st = nn.Sequential(nn.Linear(2, 12), nn.ReLU(), nn.Linear(12, 4))
    opt = torch.optim.Adam(st.parameters(), 1e-2)
    xs = torch.cat([xtr, xun]) if mode == "kd" else xtr
    for _ in range(200):
        opt.zero_grad()
        if mode == "kd":
            with torch.no_grad(): tl = teacher(xs)
            # labels only exist for the first 60; for unlabeled rows alpha=1 (pure soft target)
            loss = 1.0 * 4.0 * F.kl_div(F.log_softmax(st(xs) / 2, -1), F.softmax(tl / 2, -1), reduction="batchmean") \
                   + 0.0
            loss = 0.7 * 4.0 * F.kl_div(F.log_softmax(st(xs) / 2, -1), F.softmax(tl / 2, -1), reduction="batchmean") \
                   + 0.3 * F.cross_entropy(st(xtr), ytr)
        else:
            loss = F.cross_entropy(st(xtr), ytr)
        loss.backward(); opt.step()
    with torch.no_grad(): return (st(xte).argmax(1) == yte).float().mean().item()
for mode in ["hard", "kd"]:
    accs = [train_student(mode, s) for s in range(3)]
    print(f"student trained with {mode:4s} labels: test acc per seed {[round(a,3) for a in accs]} mean {sum(accs)/3:.3f}")
```
Output from my run:
```
T=1: grad norm without T^2 0.0469   with T^2 0.0469
T=2: grad norm without T^2 0.0152   with T^2 0.0607
T=4: grad norm without T^2 0.0040   with T^2 0.0637
T=8: grad norm without T^2 0.0010   with T^2 0.0620
teacher test acc 0.9894999861717224
student trained with hard labels: test acc per seed [0.945, 0.934, 0.948] mean 0.942
student trained with kd   labels: test acc per seed [0.984, 0.987, 0.986] mean 0.986
```

**Follow-ups:**
- *KL direction here?* KL(teacher || student), forward KL. Q24 discusses the reverse direction.
- *Why not only soft targets?* The teacher can be wrong; the hard-label term anchors the student to ground truth (alpha mixes them).
- *Does the student need the same architecture?* No, only the same output space (for logit matching).

**Common mistakes:** Forgetting T^2; applying temperature to the hard-label CE term; using `F.kl_div` with probabilities instead of log-probabilities as input (it expects log-probs for the first argument); training the teacher too; reporting a distillation gain without a hard-label baseline of the same size and data.

### Q23 ⭐⭐ 🟡 How does distillation work for LLMs: logit-level (white-box) vs sequence-level or response distillation (black-box)? Does the student need the teacher's tokenizer?
**Asked at:** product, GenAI startups, big tech
**Say this first (1 line):** White-box distillation trains the student to match the teacher's next-token probabilities (logits), which needs access to them and a shared vocabulary; black-box (sequence-level) distillation just uses the teacher's generated responses as ordinary SFT data, so it works with an API teacher but sees less information per token.

**Then explain:**
| | White-box (logit-level) | Black-box (sequence-level / response) |
|---|---|---|
| Needs | teacher weights or logits, aligned tokenizer/vocab | only sampled text from the teacher |
| Loss | KL between teacher and student token distributions | plain SFT cross-entropy on teacher text (Q2, Q15) |
| Signal per token | the whole distribution | one sampled token |
| Cost | storing or recomputing teacher logits | generation cost only |
| Works with API teachers | no (unless logprobs are exposed) | yes, subject to terms (Q21) |
- **Tokenizer:** logit matching compares probabilities token by token, so student and teacher need the same vocabulary, or an alignment scheme. The distillation sources I saw say this (snippet cut off, treat as likely). Sequence-level SFT does not care: the teacher's text is re-tokenised by the student's tokenizer.
- **Memory:** full logits are vocab-sized per token. For a 128k vocabulary and 1B tokens in fp16 that is about 256 TB (arithmetic below), so people store only the top-k probabilities or compute teacher logits on the fly (hedge: common practice, from memory).
- **Black-box nuance:** sampling gives noisy, one-hot targets; you need more samples to cover the teacher's distribution (demo below), and you inherit the teacher's errors. Filtering teacher outputs (Q21) matters.
- **Terms:** training on a provider's outputs may be restricted; check their terms.

**Example (toy, run):** a categorical teacher over 12 tokens and 6 contexts, 20 random seeds. Matching the full distribution gives KL about 0.0005 (limited only by optimisation steps) regardless of sample count. Fitting sampled tokens gives KL 5.95, 2.23, 0.53, 0.064, 0.0053 for 1, 5, 20, 100 and 1000 samples per context: it converges to the teacher but needs many samples. This is a tabular toy with no neural network, so it shows the information difference only.

**Code:** (executed, numpy)
```python
import numpy as np
rng = np.random.default_rng(0)
V, N_ctx = 12, 6                      # toy vocabulary, 6 contexts
teacher = rng.dirichlet(np.ones(V) * 0.4, size=N_ctx)       # teacher next-token distributions (skewed)
def student_fit(kind, n_samples, steps=3000, lr=0.5):
    logits = np.zeros((N_ctx, V))
    for _ in range(steps):
        p = np.exp(logits - logits.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
        if kind == "logit":                       # white-box: target is the full teacher distribution
            target = teacher
        else:                                     # black-box: target = empirical one-hot counts of sampled tokens
            target = counts / counts.sum(1, keepdims=True)
        logits -= lr * (p - target)               # gradient of CE(target, p) wrt logits
    return p
def kl(p, q): return (p * (np.log(p + 1e-12) - np.log(q + 1e-12))).sum(1).mean()
print("samples per context | KL(teacher||student)  white-box (full logits) | black-box (sampled tokens)")
for n in [1, 5, 20, 100, 1000]:
    res = []
    for seed in range(20):
        r = np.random.default_rng(seed)
        counts = np.stack([np.bincount(r.choice(V, size=n, p=teacher[i]), minlength=V) for i in range(N_ctx)]).astype(float) + 1e-9
        res.append((kl(teacher, student_fit("logit", n)), kl(teacher, student_fit("seq", n))))
    a = np.mean(res, 0)
    print(f"{n:19d} | {a[0]:.4f} | {a[1]:.4f}")
# memory of storing full logits (arithmetic only)
vocab, tokens = 128_000, 1_000_000_000
print(f"\nfull fp16 logits for 1B tokens, vocab 128k: {vocab*2*tokens/1e12:.0f} TB;  top-20 (id int32 + fp16 value): {20*6*tokens/1e9:.0f} GB")
```
Output from my run:
```
samples per context | KL(teacher||student)  white-box (full logits) | black-box (sampled tokens)
                  1 | 0.0005 | 5.9541
                  5 | 0.0005 | 2.2318
                 20 | 0.0005 | 0.5339
                100 | 0.0005 | 0.0641
               1000 | 0.0005 | 0.0053

full fp16 logits for 1B tokens, vocab 128k: 256 TB;  top-20 (id int32 + fp16 value): 120 GB
```

**Follow-ups:**
- *Which first?* If I only have an API teacher, black-box. If I own the teacher and a shared tokenizer, white-box usually gives more signal per example (hedge: depends on the task).
- *Top-k logits loss?* Renormalise over the teacher's top-k tokens and compute KL on that subset.
- *Why combine with the true labels?* The same alpha idea as Q22.

**Common mistakes:** Assuming logit distillation works across different tokenizers; storing full logits for a big corpus; calling black-box distillation "logit distillation"; forgetting the teacher's terms of use; not filtering teacher outputs.

### Q24 ⭐⭐ 🟡 Forward vs reverse KL in LLM distillation (MiniLLM): what is the difference, and what does on-policy distillation fix?
**Asked at:** research-leaning teams, big tech, GenAI startups
**Say this first (1 line):** Forward KL(p||q) makes the student cover every region where the teacher has mass (mean-seeking), reverse KL(q||p) makes it avoid regions where the teacher is unlikely (mode-seeking); MiniLLM argues reverse KL suits generative LMs because the student then stops assigning probability to bad text, and trains it on-policy (on the student's own samples).

**Then explain:**
- **Forward KL** = E_p[log p/q]: penalises q for being near zero where p has mass, so a small student that cannot represent everything spreads out and puts mass in between modes, which in text means fluent-looking nonsense.
- **Reverse KL** = E_q[log q/p]: penalises q for putting mass where p is low, so the student locks on to high-probability teacher behaviour and may drop some modes (less diverse). The MiniLLM abstract says it prevents the student from overestimating low-probability regions of the teacher's distribution.
- **On-policy:** MiniLLM optimises the reverse KL by sampling from the student itself (policy-gradient style, per the abstract: on-policy optimisation; details beyond the abstract from memory). Plain SFT or forward-KL distillation trains on teacher-written text only, but at inference the student conditions on its own tokens: this mismatch is exposure bias, and on-policy sampling lets the student see and be corrected on its own mistakes.
- **Trade-off:** reverse KL gives precision, forward KL gives coverage. Choose by what you value (quality of single answers vs diversity). Variants (generalised KL, mixing the two) exist; I would not claim a winner without testing.

**Example (SYNTHETIC, run):** a bimodal teacher (two Gaussians at -4 and +4, std 1) and a single-Gaussian student fitted on a grid. Forward KL picks mean 0.00, std 4.10: it sits between the modes, with 0.28 of its mass near x=0, where the teacher has 0.01. Reverse KL picks mean -4.00, std 1.00: it matches one mode exactly (KL = 0.693 = ln 2, the cost of ignoring the other half), with 0.01 of its mass near 0. (The mirror solution at +4 has the same KL; the search returns the first one found.)

**Code:** (executed, numpy; synthetic)
```python
# SYNTHETIC: fit ONE Gaussian student q to a BIMODAL teacher p on a grid, minimising forward vs reverse KL
import numpy as np
x = np.linspace(-12, 12, 1201); dx = x[1] - x[0]
def norm(m, s): return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))
p = 0.5 * norm(-4, 1.0) + 0.5 * norm(4, 1.0)           # teacher: two modes
def kl(a, b): 
    eps = 1e-300
    return np.sum(a * (np.log(a + eps) - np.log(b + eps))) * dx
best = {"forward": (np.inf,), "reverse": (np.inf,)}
for m in np.linspace(-6, 6, 121):
    for s in np.linspace(0.3, 6, 115):
        q = norm(m, s)
        f = kl(p, q)            # forward KL(p||q): E_p[log p/q]
        r = kl(q, p)            # reverse KL(q||p): E_q[log q/p]
        if f < best["forward"][0]: best["forward"] = (f, m, s)
        if r < best["reverse"][0]: best["reverse"] = (r, m, s)
for k, (v, m, s) in best.items():
    print(f"{k:8s} KL={v:6.3f}  student mean={m:5.2f} std={s:4.2f}")
for name, (v, m, s) in best.items():
    q = norm(m, s)
    mass_mid = q[np.abs(x) < 1.5].sum() * dx; mass_modes = q[np.abs(np.abs(x) - 4) < 1.5].sum() * dx
    print(f"{name:8s} student mass near x=0: {mass_mid:.2f}   within 1.5 of a teacher mode: {mass_modes:.2f}   (teacher: {p[np.abs(x)<1.5].sum()*dx:.2f} / {p[np.abs(np.abs(x)-4)<1.5].sum()*dx:.2f})")
```
Output from my run:
```
forward  KL= 0.724  student mean= 0.00 std=4.10
reverse  KL= 0.693  student mean=-4.00 std=1.00
forward  student mass near x=0: 0.28   within 1.5 of a teacher mode: 0.36   (teacher: 0.01 / 0.86)
reverse  student mass near x=0: 0.01   within 1.5 of a teacher mode: 0.86   (teacher: 0.01 / 0.86)
```
The "within 1.5 of a teacher mode" column counts both modes for the teacher but the reverse student sits on just one of them; it is wholly inside one mode.

**Follow-ups:**
- *Is reverse KL always better?* No: it can collapse diversity; a toy bimodal case is not an LLM, so test on your task.
- *Why is reverse KL harder to optimise?* The expectation is over the student's own samples, so you need sampling and a gradient estimator with variance control (MiniLLM uses policy-gradient tricks; hedge).
- *What is exposure bias?* Training sees only teacher/ground-truth prefixes; inference sees the student's prefixes, so errors compound.

**Common mistakes:** Swapping the two directions; saying forward KL is "wrong" for LLMs (it is the standard SFT/MLE objective); ignoring that the claim is for a small student with limited capacity; treating the Gaussian toy as evidence about LLM quality.
