# Book 2 — Part 04: Fine-tuning (SFT, LoRA/QLoRA, PEFT, Distillation)

**Topic:** when to fine-tune, SFT and instruction tuning (data, loss masking, chat templates), LoRA and QLoRA (rank, alpha, target modules, memory maths, merging), other PEFT methods and LoRA variants, catastrophic forgetting and evaluation, knowledge distillation (classic, white-box and black-box LLM distillation, forward vs reverse KL), and fine-tuning design and debugging.
**Target:** 45  |  **Actual:** 47 (⭐⭐⭐ 15, ⭐⭐ 21, ⭐ 11)  |  **Date:** 2026-10-22  |  **Status:** Wave A done; Wave B answers written (Q1-Q47); Wave C review done (see review_notes/Book2_Part04_review.md)

Scope note: Book 1 only frames fine-tuning basics (B1P09-Q39 full vs adapters vs feature extraction and forgetting; B1P09-Q14 prompting vs RAG vs fine-tuning, depth deferred to Book 2; B1P08-Q39 transfer learning; B1P08-Q55 and B1P09-Q47 distillation basics for serving), so answers here must go deeper and cross-reference rather than copy. Part 2 already covers pretraining vs continued pretraining vs fine-tuning (Q8), extending a tokenizer and model to a new domain (Q36), bf16/fp16 (Q27) and the 16 bytes-per-parameter training memory accounting (Q34); Part 3 covers prompt and tool-calling design. RLHF, DPO and safety belong to Part 5; quantization, serving and merging for deployment to Part 10; evaluation depth (LLM-as-judge, benchmarks) to Part 9; RAG to Parts 6-7. Library details (Hugging Face PEFT and TRL parameter names, defaults) change quickly: answers must use the names from the docs opened on 2026-10-22 and tell the reader to check current docs.

---

### Q1 ⭐⭐⭐ 🟢 Prompting vs RAG vs fine-tuning: what is your decision framework, and in what order do you try the adaptation methods?
**Asked at:** all types; service-company, GCC and product GenAI loops
**Say this first (1 line):** Start with the cheapest method and move up only when a measured gap remains: prompt, then few-shot examples, then RAG for knowledge, then LoRA/QLoRA for form and behaviour, and full fine-tuning or continued pretraining last.

**Then explain:**
- **The ladder:** (1) better prompt, (2) few-shot examples in the prompt, (3) RAG (retrieve documents at query time), (4) LoRA/QLoRA fine-tune, (5) full fine-tune, (6) continued pretraining (Part 2 Q8). Each step costs more and is slower to change.
- **The core split:** facts that change or must be quoted go in retrieval. Form, tone, format, and a stable skill go in weights. Fine-tuning is poor at adding reliable new facts (Q2, and Q44 later in this part).
- **Criteria I check:** is the task stable; is the gap about knowledge or behaviour; how much clean labelled data exists; latency and cost per call (a tuned small model can replace a long prompt); privacy (can data leave, must the model run in-house); how often the content changes.
- **Production pattern:** retrieval supplies the facts, a small adapter fixes the output format and house tone, and an eval set decides whether either step was worth it.
- **Always:** write the eval first. If you cannot measure the gap, you cannot say a tuned model closed it.

**Example (trap cases):**
| Situation | Answer |
|---|---|
| "We have 50 labelled examples, should we fine-tune?" | No. Put them in the prompt as few-shot, or use them as an eval set. 50 is too little to train and too valuable to waste. |
| "The bot must quote our internal policy word for word" | Retrieval. Weights give paraphrase and sometimes wrong numbers; a retrieved passage can be cited and updated the same day. |
| "Every reply must be a strict 6-field JSON in our brand voice, 200k calls a day, long prompt today" | Fine-tune a small model (LoRA). Stable task, behaviour not facts, and a shorter prompt cuts cost and latency. |

**Follow-ups:**
- *Why not fine-tune first?* Slow loop, needs data, risks forgetting (Q8), and a prompt change takes minutes.
- *Does fine-tuning replace RAG?* No. They solve different problems and are often combined.
- *Depth on the basics?* Book 1 B1P09-Q14 frames prompt vs RAG vs fine-tune and B1P09-Q39 covers full vs adapter tuning; this part goes into how.

**Common mistakes:** Fine-tuning to "teach the model our documents"; skipping prompt and few-shot baselines; no eval set; ignoring that the knowledge changes weekly; picking by what is fashionable instead of by the failure you measured. Evidence level: prep-guide advice, not a law.

### Q2 ⭐⭐⭐ 🟢 What is supervised fine-tuning (instruction tuning)? What does it teach a model, what does it not teach, and what is the training loss?
**Asked at:** all types
**Say this first (1 line):** SFT continues training a pretrained model on (prompt, response) pairs so it answers in the format and behaviour we want; the loss is the usual next-token negative log-likelihood, computed only on the response tokens given the prompt.

**Then explain:**
- **Loss:** `L = - (1/N) * sum over response tokens t of log p(y_t | prompt, y_<t)`. Same cross-entropy as pretraining, with a one-token shift and prompt tokens ignored (Q11). The TRL docs describe it as token-level NLL with ignore index -100.
- **What it teaches well:** following instructions, answer style, output format (JSON, tone), refusing or deferring in a certain way, domain phrasing. The knowledge was mostly there from pretraining; SFT shows the model how to surface it.
- **What it does not teach reliably:** new facts. Training on a few thousand statements can make the model say them in-distribution but it will also hallucinate confidently around them. Facts belong in retrieval (deeper in Q44).
- **LIMA idea:** a small set of carefully chosen examples can give strong instruction following, which suggests SFT mostly teaches style (critique and evidence in Q40; data advice in Q10).
- **After SFT:** preference tuning (RLHF, DPO) is a separate stage in Part 5.

**Example:** A base model asked "Summarise this ticket" may continue the text or ramble. After SFT on 2,000 ticket-summary pairs it returns a three-bullet summary in the house format every time. It still does not know yesterday's refund policy unless you put it in the prompt.

**Follow-ups:**
- *Why not train on the prompt as well?* You can, but you then spend gradient on reproducing the user's text; usually masked (Q11).
- *SFT vs pretraining?* Same loss, very different data size, purpose and learning rate (Part 2 Q8).
- *Instruction tuning vs SFT?* Instruction tuning is SFT on instruction-style data.

**Common mistakes:** Saying SFT "adds knowledge"; forgetting that loss is on response tokens only; mixing up SFT with RLHF; training without the EOS token so the model never stops (Q12).

### Q3 ⭐⭐⭐ 🟢 What is LoRA and how does it work? Why is it parameter-efficient, and what stays frozen?
**Asked at:** all types; product, GenAI startups, GCC
**Say this first (1 line):** LoRA freezes the pretrained weight W and learns a low-rank update B A beside it, so the layer computes W' = W + (alpha/r) B A with only A and B trained, which is a tiny fraction of the parameters.

**Then explain:**
- **Shapes:** W is (d_out x d_in). A is (r x d_in), B is (d_out x r), r is much smaller than d. Trainable parameters per matrix: r * (d_in + d_out) instead of d_in * d_out.
- **Init:** per the PEFT guide, A is Kaiming-uniform and B is zeros, so B A = 0 and the model starts exactly as the base. Training moves it away smoothly.
- **Frozen:** every original weight (and with default settings embeddings and norms). Only A and B receive gradients and optimizer state, which is where the memory saving comes from (Q7).
- **Why low rank works:** the bet is that the weight change needed for adaptation has low intrinsic rank. It holds well for format/behaviour shifts and less well for big new-domain shifts.
- **No extra inference latency:** after training you can compute W + (alpha/r) B A once and serve a normal model (merging is Q13). Adapter layers in series (older approach) add depth and latency.
- **Paper claims (abstract, for GPT-3 175B with Adam):** up to 10,000x fewer trainable parameters and about 3x less GPU memory than full fine-tuning, quality on par with or better than full FT on the models tested. These are the authors' claims for that setting, not a guarantee for your 7B model.

**Code:** (run, torch; written from scratch, no peft library)
```python
import math, torch
torch.manual_seed(0)
class LoRALinear(torch.nn.Module):
    def __init__(self, d_in, d_out, r=8, alpha=16):
        super().__init__()
        self.W = torch.nn.Parameter(torch.randn(d_out, d_in) / d_in**0.5, requires_grad=False)  # frozen
        self.A = torch.nn.Parameter(torch.empty(r, d_in))
        torch.nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))   # A: Kaiming-uniform
        self.B = torch.nn.Parameter(torch.zeros(d_out, r))       # B: zeros
        self.scale = alpha / r
    def forward(self, x):
        return x @ self.W.T + self.scale * (x @ self.A.T) @ self.B.T
m = LoRALinear(64, 64, r=8, alpha=16)
x = torch.randn(4, 64)
print("same as base at init:", torch.allclose(m(x), x @ m.W.T))
opt = torch.optim.SGD([p for p in m.parameters() if p.requires_grad], lr=0.1)
target = torch.randn(4, 64)
for _ in range(50):
    loss = ((m(x) - target) ** 2).mean(); opt.zero_grad(); loss.backward(); opt.step()
print("loss after 50 steps:", round(loss.item(), 4), "| W unchanged grad:", m.W.grad is None)
trainable = sum(p.numel() for p in m.parameters() if p.requires_grad)
print("trainable", trainable, "of", trainable + m.W.numel())
with torch.no_grad():
    Wm = m.W + m.scale * m.B @ m.A      # merge
print("merged matches:", torch.allclose(m(x), x @ Wm.T, atol=1e-5))
```
Output (my run):
```
same as base at init: True
loss after 50 steps: 0.0 | W unchanged grad: True
trainable 1024 of 5120
merged matches: True
```
The loss falls to about 0 because the toy fits four examples; the point is that only A and B train, and the merged matrix reproduces the adapter output.

**Example:** In my toy run only 1,024 of 5,120 parameters were trainable, the layer matched the base at initialisation, and after training the merged matrix reproduced the adapter output. For a real 4096x4096 weight at r=16 the adapter holds 131,072 parameters, about 0.78% of 16,777,216 (see Q4).

**Follow-ups:**
- *Why is B zero and not both zero?* If both were zero the gradients to both would be zero and nothing would train; with A random and B zero, B gets a gradient immediately.
- *Is LoRA always as good as full FT?* No, it can lag on large domain shifts or hard tasks; check on your eval.
- *Does LoRA reduce activation memory?* Not much; activations still flow through the full model (Q7).

**Common mistakes:** Saying LoRA trains a "smaller copy" of the model; forgetting the alpha/r scale; saying it lowers inference latency versus the base (it only avoids adding latency when merged); quoting the paper's 10,000x as if it applied to a small model.

### Q4 ⭐⭐⭐ 🟡 How do you choose LoRA's rank, alpha and dropout? What does the alpha/r scaling do?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Rank r sets the adapter's capacity, alpha scales its contribution by alpha/r, and dropout regularises the adapter; I start around r = 8-16 with alpha = 2r and dropout about 0.05 and tune on a validation set.

**Then explain:**
- **Rank r:** the capacity of the update. The prep guide suggests 8-16 for small shifts (tone, format) and 64 or more for large domain shifts. Raise it only if validation shows underfitting; it costs parameters linearly.
- **Alpha and the scale alpha/r:** the update is multiplied by alpha/r. With alpha fixed, doubling r halves the scale, so changing r would change the effective learning rate. The PEFT guide notes `use_rslora` switches the scale to alpha/sqrt(r), which keeps learning more stable at high ranks.
- **Alpha = 2r** is a popular heuristic (r=16, alpha=32 appears in the prep guide's example). It is a convention, not a law; treat alpha and learning rate together.
- **Dropout:** an example value of 0.05 is typical in config examples. The PEFT conceptual guide does not describe it, so call it a common default, not a rule. For small data it helps a little; I would not tune it first.
- **Learning rate:** adapters use a higher LR than full FT (the TRL docs mention about 1e-4 vs 2e-5 default for full FT). Check the current docs, these change.

**Example:** A 4096 x 4096 matrix has 16,777,216 weights. At r = 16 the adapter has 16*4096 + 4096*16 = 131,072 parameters, which is 0.78%. (The prep article calls this "a bit over a hundredth", but 131,072 / 16,777,216 is about 0.0078, closer to eight thousandths; a small slip in the source.)

**Code:** (run)
```python
d, r = 4096, 16
full = d * d
lora = r * d + d * r
print(f"full matrix {full:,}  LoRA r={r} {lora:,}  ratio {100*lora/full:.2f}%")
for r in (4, 8, 16, 64):
    print(f"r={r:3d} params {2*r*d:>9,} ({100*2*r*d/full:.2f}%)  scale alpha=2r: {2*r/r}  rsLoRA alpha=16: {16/r**0.5:.2f} vs standard {16/r:.2f}")
```
Output (my run):
```
full matrix 16,777,216  LoRA r=16 131,072  ratio 0.78%
r=  4 params    32,768 (0.20%)  scale alpha=2r: 2.0  rsLoRA alpha=16: 8.00 vs standard 4.00
r=  8 params    65,536 (0.39%)  scale alpha=2r: 2.0  rsLoRA alpha=16: 5.66 vs standard 2.00
r= 16 params   131,072 (0.78%)  scale alpha=2r: 2.0  rsLoRA alpha=16: 4.00 vs standard 1.00
r= 64 params   524,288 (3.12%)  scale alpha=2r: 2.0  rsLoRA alpha=16: 2.00 vs standard 0.25
```

**Follow-ups:**
- *Higher rank always better?* No; returns diminish, and more capacity means more forgetting and overfit on small data.
- *How do you tune it?* Sweep r in {8, 16, 64} with a fixed alpha rule, compare validation task metric and the general regression set (Q9).
- *Different rank per layer?* PEFT exposes `rank_pattern` and `alpha_pattern`; rarely needed.

**Common mistakes:** Changing r while holding alpha fixed and not noticing the scale changed; treating alpha = 2r as a theorem; tuning dropout before data quality; confusing r with the number of layers adapted.

### Q5 ⭐⭐⭐ 🟡 Which modules should LoRA target (query/value only vs all linear layers including the MLP), and why?
**Asked at:** product, GenAI startups
**Say this first (1 line):** The LoRA paper adapted only the attention query and value projections, but current practice is to target all linear layers including the MLP, because the MLP holds about two thirds of the parameters and usually gives better quality for modest extra cost.

**Then explain:**
- **Paper vs now:** the original setup used q and v; the prep guide's config example still shows q_proj and v_proj, while most recent recipes use all linear modules. Quality gains from more modules are generally reported, but check on your own eval.
- **Where the weights live:** in a Llama-style layer the MLP (gate, up, down) is about two thirds of linear weights; attention is one third.
- **Cost:** all-linear at r=16 is several times more adapter parameters than q,v only, but still under 1% of the base.
- **Trade-off:** more modules means more capacity and more activation/optimizer memory; with a tight budget keep all-linear and lower the rank rather than dropping the MLP (my judgement, not a law).
- Module names (q_proj, gate_proj, ...) differ per model; check the model's layer names and the current PEFT docs.

**Example (assumed config):** d = 4096, 32 layers, 32 heads (no grouped-query attention), gated MLP hidden 11008 with three matrices, adapter r = 16.

**Code:** (run)
```python
d, heads, mlp, L, r = 4096, 32, 11008, 32, 16     # assumed Llama-7B-like, no GQA
attn = {n: (d, d) for n in ("q", "k", "v", "o")}
mlpm = {"gate": (d, mlp), "up": (d, mlp), "down": (mlp, d)}
n = lambda s: s[0] * s[1]
a = sum(map(n, attn.values())); m = sum(map(n, mlpm.values()))
print(f"per layer attention {a:,} ({100*a/(a+m):.1f}%)  MLP {m:,} ({100*m/(a+m):.1f}%)")
lo = lambda s: r * (s[0] + s[1])
qv = lo(attn["q"]) + lo(attn["v"])
allp = sum(map(lo, attn.values())) + sum(map(lo, mlpm.values()))
print(f"r={r} per layer: q,v only {qv:,}; all linear {allp:,}")
print(f"x{L} layers: q,v only {qv*L:,} ({qv*L/1e6:.1f}M); all linear {allp*L:,} ({allp*L/1e6:.1f}M)")
print(f"base linear params in layers {(a+m)*L/1e9:.2f}B; all-linear LoRA share {100*allp/(a+m):.2f}%")
```
Output (my run):
```
per layer attention 67,108,864 (33.2%)  MLP 135,266,304 (66.8%)
r=16 per layer: q,v only 262,144; all linear 1,249,280
x32 layers: q,v only 8,388,608 (8.4M); all linear 39,976,960 (40.0M)
base linear params in layers 6.48B; all-linear LoRA share 0.62%
```
So q,v only is 8.4M trainable parameters and all-linear is 40.0M, both small next to the roughly 6.5B base linear weights.

**Follow-ups:**
- *Which layers help most?* Evidence is mixed; I'd run an ablation (q,v / attention-only / all-linear) on the eval.
- *Embeddings and lm_head?* Usually left frozen; PEFT's `modules_to_save` can train them fully if you add new tokens.

**Common mistakes:** Only adapting q,v because a tutorial did; assuming parameter count is the memory bottleneck (activations and the base model dominate); using wrong module names for the architecture.

### Q6 ⭐⭐⭐ 🟡 What is QLoRA? Explain NF4, double quantization and paged optimizers, and where precision matters during training.
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** QLoRA keeps the base model frozen in 4-bit (NF4) to save memory, backpropagates through it into higher-precision LoRA adapters, and adds double quantization and paged optimizers so a 65B model fits on one 48 GB GPU (per the paper's abstract).

**Then explain:**
- **Frozen 4-bit base:** weights are stored in 4 bits and dequantized on the fly to bf16 for each matmul. Gradients flow through the dequantized weights into the adapters; the base never updates.
- **NF4 (NormalFloat 4):** a 4-bit codebook the authors describe as information-theoretically optimal for normally distributed weights. Levels sit where normal data is dense, not evenly spaced.
- **Block-wise scaling:** weights are quantized in small blocks, each with a scale constant (absmax). Those constants cost memory too.
- **Double quantization:** quantize the scale constants themselves to save more memory.
- **Paged optimizers:** optimizer state pages to CPU memory under pressure to avoid out-of-memory spikes.
- **Where precision matters:** adapters, their gradients and optimizer states stay in higher precision (bf16 or fp32); compute runs in bf16. Only the frozen base is 4-bit.
- The paper also reports Guanaco reaching 99.3% of ChatGPT on the Vicuna benchmark; that is the authors' claim, and they themselves caution about chatbot benchmarks.

**Code:** a TOY comparison. This is NOT the real NF4 table: I build a 16-level codebook from normal quantiles (simplified) and compare it with evenly spaced 4-bit levels on normally distributed weights, both with block-wise absmax scaling.
```python
import numpy as np
from statistics import NormalDist
rng = np.random.default_rng(0)
w = rng.normal(0, 0.02, size=(4096 * 64,))          # TOY: normal "weights"
blocks = w.reshape(-1, 64)                           # blockwise, block size 64
scale = np.abs(blocks).max(1, keepdims=True)
x = blocks / scale                                   # in [-1, 1]

# (a) uniform 4-bit: 16 evenly spaced levels in [-1, 1]
uni = np.linspace(-1, 1, 16)
# (b) quantile-style 4-bit codebook (NF4-STYLE TOY, NOT the real NF4 table):
#     levels at quantiles of a standard normal, rescaled to [-1, 1]
nd = NormalDist()
q = np.array([nd.inv_cdf(p) for p in (np.arange(16) + 0.5) / 16])
quant = q / np.abs(q).max()
def roundtrip(x, book):
    idx = np.abs(x[..., None] - book).argmin(-1)
    return book[idx]
for name, book in (("uniform 4-bit", uni), ("quantile-style 4-bit (toy)", quant)):
    deq = roundtrip(x, book) * scale
    print(f"{name:28s} MSE {np.mean((deq - blocks)**2):.3e}")
print("16 levels = 4 bits; scale per 64-block costs extra bits (what double quantization shrinks)")
print("fp32 scale overhead: %.3f bits/param" % (32 / 64))
```
Output (my run):
```
uniform 4-bit                MSE 4.070e-06
quantile-style 4-bit (toy)   MSE 3.362e-06
16 levels = 4 bits; scale per 64-block costs extra bits (what double quantization shrinks)
fp32 scale overhead: 0.500 bits/param
```
The quantile-style book has lower error on normal data (about 17% lower MSE here), which is the intuition behind NF4. Real NF4 differs in its exact levels, so do not quote these numbers as NF4 results.

**Example:** On normally distributed toy weights, the quantile-style 4-bit codebook gave MSE 3.36e-6 against 4.07e-6 for evenly spaced levels (about 17% lower), which is the intuition behind NF4. The fp32 scale per 64-weight block costs 0.5 bits per parameter, which is what double quantization shrinks. These toy numbers are not NF4 results.

**Follow-ups:**
- *Speed?* Dequantization adds overhead, so QLoRA is typically slower per step than bf16 LoRA (vendor docs say so; I have not measured it).
- *Can I merge the adapter?* Not directly into the 4-bit base without dequantizing (Q13).
- *Does 4-bit hurt quality?* The paper reports it recovers 16-bit fine-tuning quality in its experiments; verify on your task.

**Common mistakes:** Saying the whole model trains in 4-bit; forgetting scale constants cost memory; claiming NF4 is just int4; thinking paged optimizers reduce steady-state memory.

### Q7 ⭐⭐⭐ 🟡 Memory maths: how much GPU memory does full fine-tuning, LoRA and QLoRA need for a 7B or 13B model, and can you fine-tune a 13B model on one 40 GB GPU?
**Asked at:** product, GenAI startups, big tech
**Say this first (1 line):** Full fine-tuning needs about 16 bytes per parameter before activations, LoRA needs the frozen bf16 base (2 bytes) plus a small adapter, and QLoRA needs about half a byte per parameter for the base, so a 13B model is hopeless for full FT on 40 GB, tight for bf16 LoRA, and comfortable for QLoRA.

**Then explain (all figures are estimates under assumed accounting):**
- **Full FT (Part 2 Q34):** bf16 weights 2 B, gradients 2 B, Adam fp32 master + m + v = 12 B, so 16 B/param.
- **LoRA:** frozen bf16 base 2 B/param, plus adapters (I assume about 1% of base parameters, each at 16 B for weights, grads and Adam).
- **QLoRA:** base at 0.5 B/param plus about 3% for quantization constants (assumed), plus the same adapter state.
- **Not included:** activations (grow with batch size x sequence length; gradient checkpointing trades compute for memory), CUDA context, fragmentation. Budget a few GB to tens of GB for these.

**Code:** (run, plain arithmetic)
```python
GB = 1e9
def est(P, seq_note=""):
    full = P * (2 + 2 + 12)                    # bf16 w + bf16 g + fp32 master+m+v
    lora_adapter = 0.01 * P                    # ASSUMED ~1% trainable (all-linear, r~16-64)
    lora = P * 2 + lora_adapter * (2 + 2 + 12) # frozen bf16 base + adapter w/g/Adam
    qlora = P * 0.5 * 1.03 + lora_adapter * (2 + 2 + 12)   # 4-bit + ~3% quant-constant overhead (assumed, with double quantization)
    return full / GB, lora / GB, qlora / GB
print("ESTIMATES, GB, excluding activations / CUDA context / fragmentation")
print(f"{'model':6s}{'full FT':>9s}{'LoRA(bf16)':>12s}{'QLoRA':>8s}")
for name, P in (("7B", 7e9), ("13B", 13e9)):
    f, l, q = est(P); print(f"{name:6s}{f:9.0f}{l:12.1f}{q:8.1f}")
print("13B bf16 weights alone:", 13e9 * 2 / GB, "GB; 40 GB headroom for LoRA:", round(40 - est(13e9)[1], 1), "GB")
print("13B QLoRA headroom on 40 GB:", round(40 - est(13e9)[2], 1), "GB")
```
Output (my run):
```
ESTIMATES, GB, excluding activations / CUDA context / fragmentation
model   full FT  LoRA(bf16)   QLoRA
7B          112        15.1     4.7
13B         208        28.1     8.8
13B bf16 weights alone: 26.0 GB; 40 GB headroom for LoRA: 11.9 GB
13B QLoRA headroom on 40 GB: 31.2 GB
```
**Example (can 13B fit on 40 GB?):** With bf16 LoRA the weights alone are 26 GB and my estimate is about 28 GB with adapter state, leaving roughly 12 GB for activations and overhead. That can work with short sequences, small batch and gradient checkpointing, but it is tight and depends on all of those. QLoRA is about 9 GB for state, leaving about 31 GB, so it fits comfortably and allows longer sequences. The prep article's rough figures (about 30 GB LoRA, 10 GB QLoRA for 13B) are secondary sources but land close to this estimate; I computed mine from stated assumptions instead of quoting them.

**Follow-ups:**
- *What else grows memory?* Sequence length and batch size through activations; the optimizer if you train more modules.
- *If it does not fit?* Gradient checkpointing, smaller micro-batch with accumulation, QLoRA, or sharding (Part 2 Q34).

**Common mistakes:** Forgetting activations; using 4 B/param for everything; claiming LoRA removes the cost of the base weights (it does not, they still sit in memory); presenting these estimates as measured numbers.

### Q8 ⭐⭐⭐ 🟡 What is catastrophic forgetting in fine-tuning? How do you detect it, and how do you mitigate it?
**Asked at:** all types; product, GenAI startups
**Say this first (1 line):** Catastrophic forgetting is when fine-tuning on a narrow task overwrites general abilities the base model had; I detect it by tracking a held-out general set next to the task metric, and I reduce it with lower learning rate, fewer epochs, lower rank, mixing in general data, and freezing more.

**Then explain:**
- **Why it happens:** the gradients only see the new data, so any weight direction useful for the old behaviour but irrelevant to the new data is free to drift. High LR, many epochs and large capacity make it worse.
- **Detection:** keep a small general suite (e.g. MMLU or HellaSwag style multiple-choice, plus a few prompts from your own product) and evaluate it at every checkpoint along with the task metric. A task metric that rises while the general score drops is the signature. Also read samples: refusals, format leakage into unrelated prompts.
- **Mitigations:** lower LR and fewer epochs; smaller rank or fewer target modules (less capacity to drift); LoRA instead of full FT; replay, i.e. mix general or earlier-task examples into the fine-tuning data (Q27); freeze more layers; early stop on the general metric; merge-weight scaling at the end (reduce the adapter strength).
- **Honest caveat:** LoRA forgets less than full FT in several reports but not zero; do not assume it is safe.

**Code:** a SYNTHETIC demo, not a language model. One small MLP is trained on a "general" toy task, then fine-tuned on a second toy task (labelled by a different random rule, flagged by a task bit). Takes about 1-2 minutes on CPU.
```python
import torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(1); torch.manual_seed(0)
# SYNTHETIC demo: one small MLP, two toy tasks. Input = 10 features + 2-dim task flag; labels from different random teachers.
d, k = 10, 4
tG, tT = torch.randn(d, k), torch.randn(d, k)
def data(t, flag, n):
    X = torch.randn(n, d); f = torch.zeros(n, 2); f[:, flag] = 1
    return torch.cat([X, f], 1), (X @ t).argmax(1)
G_tr, G_te = data(tG, 0, 3000), data(tG, 0, 2000)
T_tr, T_te = data(tT, 1, 3000), data(tT, 1, 2000)
def acc(m, ds): return (m(ds[0]).argmax(1) == ds[1]).float().mean().item()
def fit(m, X, y, steps, lr):
    opt = torch.optim.Adam(m.parameters(), lr=lr)
    for _ in range(steps):
        loss = F.cross_entropy(m(X), y); opt.zero_grad(); loss.backward(); opt.step()
def fresh():
    return nn.Sequential(nn.Linear(d + 2, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, k))
base = fresh(); fit(base, *G_tr, 1500, 3e-3)
def show(name, m): print(f"{name:34s} general acc {acc(m, G_te):.2f}   new-task acc {acc(m, T_te):.2f}")
show("base (trained on general only)", base)
import copy
m1 = copy.deepcopy(base); fit(m1, *T_tr, 1500, 3e-3); show("fine-tune on new task only", m1)
Xr = torch.cat([T_tr[0], G_tr[0][:600]]); yr = torch.cat([T_tr[1], G_tr[1][:600]])
m2 = copy.deepcopy(base); fit(m2, Xr, yr, 1500, 3e-3); show("new task + 600 general replay", m2)
m3 = copy.deepcopy(base); fit(m3, *T_tr, 100, 1e-4); show("new task only, tiny LR, few steps", m3)
```
Output (my run):
```
base (trained on general only)     general acc 0.98   new-task acc 0.24
fine-tune on new task only         general acc 0.27   new-task acc 0.97
new task + 600 general replay      general acc 0.91   new-task acc 0.97
new task only, tiny LR, few steps  general acc 0.96   new-task acc 0.27
```
Fine-tuning on the new task alone drops general accuracy from 0.98 to 0.27. Replaying 600 general examples restores it to 0.91 with no loss on the new task. The tiny-LR run stays at 0.96 general accuracy but also does not learn the new task (0.27), so lowering LR alone is a trade, not a fix. Numbers from this toy say nothing about real LLM magnitudes.

**Example:** In my synthetic run, fine-tuning on the new task alone took general accuracy from 0.98 to 0.27 while new-task accuracy went from 0.24 to 0.97; adding 600 general replay examples brought general accuracy back to 0.91 with the new task still at 0.97. A tiny learning rate kept general accuracy at 0.96 but left the new task at 0.27.

**Follow-ups:**
- *Would you use a bigger replay ratio?* Tune it: more replay protects general ability but dilutes the task signal.
- *Is it only about knowledge?* No: format, safety behaviour and instruction following also regress.

**Common mistakes:** Only watching the task metric; calling any drop "forgetting" without a baseline; fixing it by lowering LR so far that the task is not learned; evaluating the general set once at the end.

### Q9 ⭐⭐⭐ 🟡 How do you evaluate a fine-tuned model before shipping (task metric, general-capability regression, human or LLM judging)?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** I compare the fine-tuned model with the base model and the best prompted baseline on a held-out task set, run a general-capability regression suite, add human or LLM judging for open-ended quality with its known caveats, and report variance across seeds, before shipping.

**Then explain:**
- **Task metric on held-out data:** exact match, F1, accuracy, schema-valid rate, whatever fits the task. The test set is never used for tuning and is deduplicated against the training data (Q34).
- **Baselines:** (a) base model with a good prompt and few-shot, (b) the base model itself, (c) the previous production model. A fine-tune that does not beat a strong prompt is not worth the maintenance.
- **General regression:** a small suite such as MMLU or HellaSwag (examples named in the prep article) plus your own safety and instruction-following prompts, to catch forgetting (Q8).
- **Open-ended quality:** human review on a sample, or LLM-as-judge with controls for position and length bias and a human-labelled calibration set (depth in Part 9).
- **Variance:** SFT results move with seed and data order, so run two or three seeds on small data and report the spread; do not ship on a 1-point gain.
- **Beyond accuracy:** latency, cost, format failures, refusal rate, and slice results (per customer, language, length).
- **After shipping:** shadow or canary release, monitor, and keep the eval in CI.

**Example:** A support-ticket classifier tuned with LoRA scores 91 F1 vs 84 for a 5-shot prompt (illustrative numbers, not a run), but MMLU drops 3 points and schema failures on long tickets are 4%. I would ship only if the product does not rely on general ability, or I would add replay and retrain.

**Follow-ups:**
- *Why compare to the base model?* To separate what fine-tuning added from what the model already did.
- *Can the LLM judge be the same model family?* Risky: self-preference bias; use a different judge and spot-check with humans.

**Common mistakes:** Evaluating on training-like data; no prompted baseline; single-seed claims; using only an aggregate score and missing slice regressions; trusting a judge model without calibration.

### Q10 ⭐⭐⭐ 🟡 How much data do you need for SFT, and what matters more, quality or quantity? How do you build and clean the dataset?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** For format and behaviour, a few hundred to a few thousand clean, diverse examples is usually the right order of magnitude, and quality and diversity matter more than raw count; I build the set from real inputs, review it, deduplicate and filter it, and hold out a test split.

**Then explain:**
- **LIMA:** the paper tuned a 65B base on 1,000 curated examples and reported strong results in a small human study, which is the usual evidence for "quality over quantity". It is a small study on one model family, so treat it as indicative (critique in Q40).
- **Practical sizes (rough rules, not laws):** a few hundred to a few thousand for a narrow format or behaviour; more for broad instruction following, hard reasoning or multiple tasks. Always learn it by a data-size curve: train on 25%, 50%, 100% and see where validation flattens.
- **Quality checks:** responses are correct and consistent in style; prompts cover the real distribution including hard and edge cases; no contradictory labels for the same input.
- **Cleaning:** normalised deduplication (exact and near), length filters, format validation (parse the JSON), boilerplate or refusal filters, PII removal and contamination checks against your eval (Q34).
- **Sources:** logged production traffic with human-corrected answers, expert-written examples, and carefully filtered synthetic data from a stronger model (check licence and terms).
- **Split first:** carve out the test set before any cleaning decisions are tuned on it.

**Code:** (run, toy dataset)
```python
import re, hashlib, json
raw = [
 {"prompt": "Summarise: refunds take 5 days.", "response": "Refunds take 5 days."},
 {"prompt": "summarise:  Refunds take 5 days. ", "response": "Refunds take 5 days."},   # near-dup (case/space)
 {"prompt": "Translate 'hello' to Hindi.", "response": "Namaste."},
 {"prompt": "Translate 'hello' to Hindi.", "response": ""},                              # empty response
 {"prompt": "Hi", "response": "As an AI language model, I cannot help."},                # boilerplate refusal
 {"prompt": "Write a haiku about rain.", "response": "x" * 5000},                        # too long
 {"prompt": "Extract the city as JSON: 'I live in Pune'.", "response": '{"city": "Pune"}'},
 {"prompt": "Extract the city as JSON: 'I live in Delhi'.", "response": "city is Delhi"},   # wrong format
 {"prompt": "Explain overfitting in one line.", "response": "The model memorises training noise and fails on new data."},
]
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
seen, kept, drop = set(), [], []
def why(ex):
    r = ex["response"]
    if not r.strip(): return "empty response"
    if len(r) > 2000: return "too long"
    if r.lower().startswith("as an ai language model"): return "boilerplate"
    if "JSON" in ex["prompt"]:
        try: json.loads(r)
        except ValueError: return "format check failed"
    return None
for ex in raw:
    key = hashlib.md5((norm(ex["prompt"]) + "|" + norm(ex["response"])).encode()).hexdigest()
    reason = "exact dup after normalising" if key in seen else why(ex)
    seen.add(key)
    (drop if reason else kept).append((ex, reason))
print("kept", len(kept), "of", len(raw))
for ex, r in drop: print("  dropped:", r, "|", ex["prompt"][:35])
```
Output (my run):
```
kept 4 of 9
  dropped: exact dup after normalising | summarise:  Refunds take 5 days. 
  dropped: empty response | Translate 'hello' to Hindi.
  dropped: boilerplate | Hi
  dropped: too long | Write a haiku about rain.
  dropped: format check failed | Extract the city as JSON: 'I live i
```

**Example:** In my toy run a 9-example set was filtered down to 4: one exact duplicate after normalisation, one empty response, one boilerplate item, one over-long item and one that failed the JSON format check were dropped. Real filters need tuning on a human-reviewed sample.

**Follow-ups:**
- *Synthetic data?* Useful for coverage but copies the teacher's mistakes and style; filter and sample-check.
- *How do you know you have enough?* The data-size curve and validation plateau, not a magic number.

**Common mistakes:** Chasing volume with noisy data; duplicates that leak across train and test; unbalanced task mix; no review of a random sample by a human; quoting "1,000 examples is enough" without the LIMA caveats.

### Q11 ⭐⭐⭐ 🟡 In SFT, why do we mask prompt tokens from the loss (train on completions or assistant turns only)? How do label shifting, the ignore index and packing interact?
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** We mask prompt tokens (label -100) so the loss only rewards producing the response; labels are the inputs shifted by one, padding is also -100, and packing multiple examples into a row needs per-example masks and correct attention and position handling.

**Then explain:**
- **Why mask the prompt:** the prompt is given at inference. Training on it spends capacity on copying user text and can distort behaviour, especially with long prompts and short answers where prompt tokens dominate the loss average. It is a common default, not a universal rule (some setups train on all tokens).
- **Shift:** position t predicts token t+1, so logits[:, :-1] are compared with labels[:, 1:].
- **ignore_index:** `F.cross_entropy(..., ignore_index=-100)` skips those positions and averages over the rest only. Padding uses the same value.
- **TRL options (docs opened 2026-10-22; check the current docs):** `completion_only_loss` for prompt-completion data and `assistant_only_loss` for chat data (needs a chat template that marks assistant spans).
- **Packing:** fits several short examples into one fixed-length sequence to cut padding waste. TRL lists strategies `bfd`, `bfd_split` and `wrapped`. Without care, tokens attend across example boundaries and positions run on; `padding_free` mode, which TRL says needs FlashAttention 2/3, avoids padding and keeps examples separate.
- **Pitfall:** masking is applied per example before packing; the EOS token of each response must stay in the labels (Q12).

**Code:** (run, torch; made-up token ids and random logits)
```python
import torch, torch.nn.functional as F
torch.manual_seed(0)
V, PAD, IGN = 50, 0, -100
# batch of (prompt, response) token ids (made-up ids); response ends with EOS=2
ex = [([5, 6, 7, 8], [11, 12, 13, 2]), ([9, 10], [14, 2])]
L = max(len(p) + len(r) for p, r in ex)
ids = torch.full((len(ex), L), PAD); lab = torch.full((len(ex), L), IGN); lab_nomask = lab.clone()
for i, (p, r) in enumerate(ex):
    s = p + r; ids[i, :len(s)] = torch.tensor(s)
    lab[i, len(p):len(s)] = torch.tensor(r)          # train on response only
    lab_nomask[i, :len(s)] = torch.tensor(s)         # prompt too, pad still ignored
print("input_ids\n", ids); print("labels (masked)\n", lab)
logits = torch.randn(len(ex), L, V)                  # stand-in for model output
def loss(lab):
    sl, sy = logits[:, :-1], lab[:, 1:]              # shift: position t predicts token t+1
    return F.cross_entropy(sl.reshape(-1, V), sy.reshape(-1), ignore_index=IGN)
def manual(lab):
    sl, sy = logits[:, :-1].reshape(-1, V), lab[:, 1:].reshape(-1); keep = sy != IGN
    return -F.log_softmax(sl, -1)[keep, sy[keep]].mean()
print("tokens counted: masked", int((lab[:, 1:] != IGN).sum()), "| unmasked-prompt", int((lab_nomask[:, 1:] != IGN).sum()))
print("loss response-only:", round(loss(lab).item(), 4), "manual:", round(manual(lab).item(), 4))
print("loss incl. prompt :", round(loss(lab_nomask).item(), 4))
# packing: two examples in one row, labels still masked per example; position ids restart
packed = ex[0][0] + ex[0][1] + ex[1][0] + ex[1][1]
pos = list(range(8)) + list(range(4))
print("packed ids", packed); print("position_ids restart per example:", pos)
```
Output (my run):
```
input_ids
 tensor([[ 5,  6,  7,  8, 11, 12, 13,  2],
        [ 9, 10, 14,  2,  0,  0,  0,  0]])
labels (masked)
 tensor([[-100, -100, -100, -100,   11,   12,   13,    2],
        [-100, -100,   14,    2, -100, -100, -100, -100]])
tokens counted: masked 6 | unmasked-prompt 10
loss response-only: 4.8274 manual: 4.8274
loss incl. prompt : 4.5411
packed ids [5, 6, 7, 8, 11, 12, 13, 2, 9, 10, 14, 2]
position_ids restart per example: [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3]
```
Masked loss counts 6 response tokens, the unmasked-prompt loss counts 10; they differ (4.83 vs 4.54), and my manual NLL equals `F.cross_entropy` with `ignore_index`.

**Example:** In my run the second sequence had 2 response tokens and 6 padding or prompt positions masked; the response-only loss was 4.8274 (matching my manual NLL and F.cross_entropy with ignore_index), while including prompt tokens changed it to 4.5411. Packed position ids restarted at 0 for each example.

**Follow-ups:**
- *Does masking change the model's input?* No, the prompt still conditions the response; only the loss differs.
- *Loss normalisation with packing?* Decide whether to average per token or per example; token-average gives long responses more weight.

**Common mistakes:** Forgetting the shift (off-by-one labels); leaving padding unmasked; masking the EOS; assuming packing is free when attention crosses example boundaries; not checking the masked labels by printing one batch.

### Q12 ⭐⭐⭐ 🟡 Why do chat templates and the EOS token matter in fine-tuning? What breaks when training and inference templates differ?
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** The chat template turns messages into the exact token string the model sees; if training and inference use different templates, or the EOS token is missing or mismatched, the model sees a format it was never trained on and may behave badly or never stop.

**Then explain:**
- **Template:** role markers, separators and special tokens. Different model families use different ones; the instruct checkpoint's own template is the safe choice (Q36).
- **Train-test skew:** if training strings look like `<|user|>...` and inference sends `User: ...`, the prompt falls outside the learned distribution and quality drops even though loss looked fine.
- **Generation prompt:** at inference the string ends with the assistant header so the model continues as the assistant; training must contain that same prefix before the response.
- **EOS:** the response must end with the end-of-turn token, and it must be in the labels. TRL docs say to align the EOS token with the chat template or the model may not stop. Without it you get run-on output or the model inventing the next user turn.
- **Checks:** print one rendered training example and the inference prompt, confirm the prompt is a prefix of the training string, and confirm the stop token configured in the server matches.

**Code:** (run, plain Python toy template; no transformers library)
```python
BOS, EOS = "<s>", "</s>"
def render(messages, add_generation_prompt=False):
    out = BOS
    for m in messages: out += f"<|{m['role']}|>\n{m['content']}{EOS}\n"
    if add_generation_prompt: out += "<|assistant|>\n"
    return out
msgs = [{"role": "user", "content": "2+2?"}, {"role": "assistant", "content": "4"}]
train = render(msgs)
infer_ok = render(msgs[:1], add_generation_prompt=True)
infer_bad = "User: 2+2?\nAssistant:"          # hand-written, different from training
print("TRAIN string :", repr(train)); print("INFER (match):", repr(infer_ok)); print("INFER (bad)  :", repr(infer_bad))
print("train prefix == inference prompt:", train.startswith(infer_ok), "| bad:", train.startswith(infer_bad))
# EOS check: which positions are supervised in the response?
print("response label text with EOS   :", repr("4" + EOS))
print("response label text WITHOUT EOS:", repr("4"), "-> model never sees a stop signal, rambles on")
# toy generation: model that learned a stop token only if it was trained with it
def generate(trained_with_eos, max_tokens=8):
    out = []
    for i in range(max_tokens):
        if trained_with_eos and i == 1: out.append(EOS); break
        out.append("4" if i == 0 else "...more text")
    return out
print("with EOS   :", generate(True)); print("without EOS:", generate(False))
```
Output (my run):
```
TRAIN string : '<s><|user|>\n2+2?</s>\n<|assistant|>\n4</s>\n'
INFER (match): '<s><|user|>\n2+2?</s>\n<|assistant|>\n'
INFER (bad)  : 'User: 2+2?\nAssistant:'
train prefix == inference prompt: True | bad: False
response label text with EOS   : '4</s>'
response label text WITHOUT EOS: '4' -> model never sees a stop signal, rambles on
with EOS   : ['4', '</s>']
without EOS: ['4', '...more text', '...more text', '...more text', '...more text', '...more text', '...more text', '...more text']
```
The last toy "model" is a hand-written stand-in, not a real LLM, to show the effect of training without a stop signal.

**Example:** My toy template rendered the training string '<s><|user|>\n2+2?</s>\n<|assistant|>\n4</s>\n'. Inference with the matching template reproduced its prefix, while the hand-written 'User: 2+2?\nAssistant:' prompt did not. Dropping the EOS from the label text made the toy stand-in model keep generating.

**Follow-ups:**
- *Double BOS?* A common bug: template adds BOS and the tokenizer adds another; check the token ids.
- *Why does a LoRA model ramble after merging?* Often a stop-token or template mismatch, not the adapter itself.

**Common mistakes:** Hand-writing prompts at inference; training on text without EOS; using a base-model template on an instruct checkpoint; changing templates between training and serving; not looking at the actual rendered string.

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

### Q25 ⭐⭐ 🟡 When do you fine-tune a small model instead of calling a large API model? Work through a cost, latency, privacy and quality break-even.
**Asked at:** product, GCC, API-heavy teams
**Say this first (1 line):** I fine-tune and self-host a small model when the task is narrow and stable, volume is high and steady, and my own evals show the small model meets the quality bar; otherwise I stay on the API, because the API has no fixed cost, no idle GPU and no maintenance.

**Then explain:**
- **Cost has a fixed part and a per-token part.** API: pay per token, nothing when idle. Self-host: a GPU bill that runs 24x7 whether busy or not, plus a one-off cost (data, training runs, evals) and ongoing ops. So the break-even is a *volume*, and **utilisation** decides whether you ever reach it.
- **Break-even volume** = fixed monthly self-host cost / API price per token (while one GPU is enough). Above it, each extra token is almost free on your GPU. Below it, the API wins.
- **Utilisation is the sensitivity that bites.** GPU cost per 1M tokens = GPU cost per month / (monthly capacity x average utilisation). Traffic is bursty, so a GPU provisioned for peak may average 10-30%.
- **Non-cost factors:** latency (a small model on a nearby GPU can be faster and more predictable); privacy and residency (data stays in your account; see Q33); control (frozen version, no silent provider updates, no deprecation surprise); quality ceiling (a small model rarely matches a frontier model on open-ended or reasoning-heavy tasks, so measure); maintenance and on-call; drift (you own retraining when the data shifts).
- A cheaper middle path: try a smaller API model or prompt caching first (Part 3 Q36); distillation from a big model's outputs (Q22-Q24) is how the small model often gets good enough.

**Example (all numbers ASSUMED, not real prices):** API 3 USD per 1M blended tokens; GPU 2 USD/hour = 1,460 USD/month; 1,500 tokens/s per GPU; one-off 3,000 USD; ops 1,500 USD/month. Fixed floor = 2,960 USD/month, so break-even is about 987M tokens/month (and one GPU can serve that if average utilisation is at least about 25%). At 10% utilisation the GPU alone costs 3.70 USD per 1M tokens, more than the API: never break-even. At 2,000M tokens/month the self-host saves about 1,580 USD/month and the one-off pays back in about 1.9 months.

**Code:** (executed, pure Python; every input is an assumption)
```python
# Break-even: API model vs self-hosted fine-tuned small model.
# ALL NUMBERS BELOW ARE ASSUMED for illustration. Replace them with your own quotes and benchmarks.
import math
API_PRICE_PER_1M = 3.00     # ASSUMED blended USD per 1M tokens (input+output mix) for the API model
GPU_COST_PER_HR  = 2.00     # ASSUMED USD per hour for one GPU kept on 24x7
THROUGHPUT_TPS   = 1500     # ASSUMED sustained tokens/s per GPU at 100% load (batched)
FT_ONE_OFF       = 3000.0   # ASSUMED one-off USD: data work, training runs, evals
OPS_MONTHLY      = 1500.0   # ASSUMED monthly USD for maintenance / on-call share
HOURS = 730

gpu_month = GPU_COST_PER_HR * HOURS
cap_m = THROUGHPUT_TPS * 3600 * HOURS / 1e6          # M tokens one GPU can serve per month at 100%
print(f"one GPU: {gpu_month:,.0f} USD/month, capacity {cap_m:,.0f}M tokens/month at 100% load")

def self_cost(vol_m, util):
    """util = average utilisation you actually achieve (traffic is bursty, so < 100%)."""
    gpus = max(1, math.ceil(vol_m / (cap_m * util)))
    return gpus * gpu_month + OPS_MONTHLY

def api_cost(vol_m):
    return API_PRICE_PER_1M * vol_m

print("\nGPU-only cost per 1M tokens vs API price", API_PRICE_PER_1M)
for util in (0.7, 0.5, 0.3, 0.1):
    print(f"  util {util:.0%}: {gpu_month/(cap_m*util):.2f} USD per 1M tokens")

print("\nMonthly break-even volume (self-host cheaper from here)")
for util in (0.7, 0.5, 0.3, 0.1):
    v = next((m for m in range(1, 50000) if self_cost(m, util) < api_cost(m)), None)
    print(f"  util {util:.0%}: {('%dM tokens/month' % v) if v else 'never (GPU per-token cost >= API price)'}")

vol, util = 2000, 0.5
sav = api_cost(vol) - self_cost(vol, util)
print(f"\nAt {vol}M tokens/month, util {util:.0%}: API {api_cost(vol):,.0f} vs self {self_cost(vol, util):,.0f} USD/month,"
      f" saving {sav:,.0f}; one-off {FT_ONE_OFF:,.0f} pays back in {FT_ONE_OFF/sav:.1f} months")
```
Output from my run:
```
one GPU: 1,460 USD/month, capacity 3,942M tokens/month at 100% load

GPU-only cost per 1M tokens vs API price 3.0
  util 70%: 0.53 USD per 1M tokens
  util 50%: 0.74 USD per 1M tokens
  util 30%: 1.23 USD per 1M tokens
  util 10%: 3.70 USD per 1M tokens

Monthly break-even volume (self-host cheaper from here)
  util 70%: 987M tokens/month
  util 50%: 987M tokens/month
  util 30%: 987M tokens/month
  util 10%: never (GPU per-token cost >= API price)

At 2000M tokens/month, util 50%: API 6,000 vs self 4,420 USD/month, saving 1,580; one-off 3,000 pays back in 1.9 months
```

**Follow-ups:**
- *What if volume is spiky?* Autoscale or queue batch work; otherwise the API's pay-per-use wins. Part 10 covers serving cost.
- *What would make you move back to the API?* A better API model at a lower price, or the maintenance burden exceeding the saving.
- *How do you check quality fairly?* Same held-out set, same metric, both candidates (Q9).

**Common mistakes:** Comparing only per-token prices and ignoring idle GPUs; leaving out engineering and on-call time; assuming 100% utilisation; forgetting the API price can drop; not checking that the small model meets the quality bar first.

### Q26 ⭐⭐ 🟡 For classification or extraction, would you fine-tune an LLM with SFT, add a classification head, or use a small encoder? How do you choose?
**Asked at:** product, GCC, applied ML teams
**Say this first (1 line):** For a fixed label set with enough labelled data I start with a small encoder (BERT-class) plus a classification head, because it is cheap, fast and gives calibrated-ish probabilities; I move to an LLM (prompting first, then SFT) when the task needs world knowledge, long context, many or changing labels, or structured extraction output.

**Then explain:**

| Option | Best when | Watch out |
|---|---|---|
| Prompting an LLM | few labels or changing labels, no data, quick baseline | cost and latency per call, format drift, weak calibration |
| Small encoder + classification head | fixed labels, 1k+ labelled examples, high throughput, low latency, need probabilities | short context, no generation, retrain for new labels |
| LLM + classification head (pooled hidden state to a linear layer) | fixed labels, task needs LLM-level understanding, you still want one forward pass and a probability vector | bigger and slower than an encoder; the head is new and untrained |
| SFT of a generative LLM | extraction into JSON, many labels or free-text labels, explanations, multi-task in one model | output must be parsed; confidence is not a clean probability; slower per item |

- **Label set size:** 2-50 fixed labels favours a head. Hundreds or open-ended labels favours generation (or retrieval over label descriptions).
- **Calibration:** a softmax head gives a score you can threshold and calibrate on a held-out set. A generative model gives text; you can read label-token log-probabilities, but treat them as uncalibrated until measured.
- **Output structure:** extraction (entities, fields) needs token tagging (encoder with a token-classification head) or generation with a schema (Part 3 Q22, Q28 here).
- **Data volume:** about hundreds of examples can already beat prompting for a narrow label set; thousands make the encoder solid. Do not trust a single number, run a learning curve.
- Book 1 covered the classical side (B1P09-Q6, B1P09-Q9); here the new part is the LLM options.

**Example:** support-ticket routing into 12 fixed queues, 20k labelled tickets, 100 requests/s, 50 ms budget: a fine-tuned small encoder with a head, one forward pass, thresholded probabilities. Extracting invoice fields into JSON from messy text: SFT a small LLM (or prompt a large one first) with schema checks.

**Follow-ups:**
- *Prompting baseline first?* Yes, always: it tells you the achievable accuracy and labels free pseudo-data.
- *Can you combine?* Use a big LLM to label data, train the small encoder on it (distillation, Q22).
- *Imbalanced classes?* Class weights or resampling plus per-class metrics, same as classical ML.

**Common mistakes:** Using a 7B generator for a 5-label problem an encoder solves at a hundredth of the cost; judging only accuracy on imbalanced classes; parsing free text labels without a fallback; claiming generative confidence is calibrated.

### Q27 ⭐⭐ 🟡 How do you mix tasks and general data in SFT (data mixtures, ordering, replay of general data), and what goes wrong with a narrow dataset?
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** I treat the data mixture as a hyperparameter: target ratios per task, plus a slice of general instruction data replayed to protect broad abilities, and I verify that the batches I actually feed match those ratios.

**Then explain:**
- **Task ratios:** sampling ratio is not the same as dataset size. A small, important task can be upsampled, but heavy repetition invites memorisation (Q30), so watch epochs per source.
- **General replay:** mix some general instruction or chat data (and safety or refusal examples if the base is aligned) into the SFT set. The fraction is something to tune (people often start with a modest share, say 5-20%, but that is a starting guess, not a rule). Measure the general-capability regression (Q8, Q9) for each setting.
- **Ordering and curriculum:** evidence is weak. Shuffling the mix is the safe default; some practitioners put cleaner or harder data last, and results are mixed, so I would test it rather than assume it helps.
- **Narrow dataset consequences:** the model drifts to that style (every answer sounds like the training set), loses general skills and format flexibility, over-refuses or under-refuses, and fails out of distribution. That is catastrophic forgetting (Q8) plus overfitting (Q30).
- **Implementation detail:** use a scheduler that tracks running shares per source, not just per-batch rounding. Small pools repeat more often, which the sampler can report.

**Example:** 60% extraction, 20% summarisation, 15% general replay, 5% safety refusals, batch of 32. Rounding per batch alone cannot split 19.2 examples (19 of 32 is 59.4%), so I use a deficit scheduler; over 500 batches it hits the targets exactly, and shows the 200-example safety pool is seen 4.0 times while the big pool is seen 1.9 times.

**Code:** (executed, synthetic ids, no real data)
```python
# Synthetic mixed-batch sampler with target ratios. Sources are fake lists of example ids; no real data.
import random
from collections import Counter
random.seed(0)
TARGET = {"task_extract": 0.60, "task_summarise": 0.20, "general_replay": 0.15, "safety_refusal": 0.05}
POOLS = {k: [f"{k}_{i}" for i in range(n)] for k, n in
         {"task_extract": 5000, "task_summarise": 1500, "general_replay": 800, "safety_refusal": 200}.items()}

def mixed_stream(target, pools, batch_size=32):
    """Deficit scheduler: for every slot pick the source furthest below its target share so far.
    Batch-level counts are rounded, but the running ratio converges to the target."""
    names = list(target)
    given = {n: 0 for n in names}
    iters = {n: iter(random.sample(pools[n], len(pools[n]))) for n in names}
    seen = 0
    while True:
        batch = []
        for _ in range(batch_size):
            seen += 1
            n = max(names, key=lambda k: target[k] * seen - given[k])
            given[n] += 1
            try:
                batch.append(next(iters[n]))
            except StopIteration:                    # small pools repeat: more epochs than the big pool
                iters[n] = iter(random.sample(pools[n], len(pools[n])))
                batch.append(next(iters[n]))
        random.shuffle(batch)
        yield batch

gen = mixed_stream(TARGET, POOLS)
counts, total = Counter(), 0
for _ in range(500):
    b = next(gen)
    counts.update(x.rsplit("_", 1)[0] for x in b); total += len(b)
print("batch size 32, 500 batches =", total, "examples")
for k, v in TARGET.items():
    print(f"{k:15s} target {v:.2%}  realised {counts[k]/total:.2%}")
# epochs per source: how many times each pool was passed
for k in TARGET:
    print(f"{k:15s} pool {len(POOLS[k]):5d}  seen {counts[k]:6d}  -> {counts[k]/len(POOLS[k]):.1f} epochs")
```
Output from my run:
```
batch size 32, 500 batches = 16000 examples
task_extract    target 60.00%  realised 60.00%
task_summarise  target 20.00%  realised 20.00%
general_replay  target 15.00%  realised 15.00%
safety_refusal  target 5.00%  realised 5.00%
task_extract    pool  5000  seen   9600  -> 1.9 epochs
task_summarise  pool  1500  seen   3200  -> 2.1 epochs
general_replay  pool   800  seen   2400  -> 3.0 epochs
safety_refusal  pool   200  seen    800  -> 4.0 epochs
```

**Follow-ups:**
- *How do you pick the replay share?* Sweep a few values, plot task metric against general benchmark regression, pick the knee.
- *Which general data?* Instruction data similar in format to what the base was trained on; ideally the base's own outputs on general prompts (self-generated replay) to avoid drifting its distribution.
- *Do you mix at the token or example level?* Example level is usual; remember long examples carry more tokens, so token share can differ from example share.

**Common mistakes:** Mixing by file size by accident; assuming a curriculum helps without an ablation; no general eval, so forgetting goes unnoticed; heavily repeating a tiny high-priority pool.

### Q28 ⭐⭐ 🟡 How do you fine-tune for structured output or tool calling (dataset format, loss on tool calls, evaluation)? How does it relate to prompting for the same?
**Asked at:** product, GenAI startups, agent-building teams
**Say this first (1 line):** I fine-tune on conversations that contain the exact tool calls I want, with the tool definitions in the prompt and loss only on the assistant tokens, and I evaluate tool selection and argument accuracy on held-out cases; prompting (with constrained decoding) is my first try, and fine-tuning wins when there are many tools, a strict format, or tight latency and cost.

**Then explain:**
- **Dataset format (TRL docs, opened 2026-10-22; check the current docs, these change):** each example is a conversation (`messages`) where an assistant message carries `tool_calls`, a following message with role `tool` carries the result, and a `tools` column holds the JSON schemas of available tools. The chat template renders all of that into tokens, so train and inference templates must match (Q12).
- **Loss:** train on assistant tokens, including the tool-call text and the final answer; mask the system, user and tool-result tokens (Q11; `assistant_only_loss` needs a chat template that supports it, per the docs). Tool outputs are not model decisions, so they should not be in the loss.
- **Data:** include no-tool cases (answer directly), wrong-tool-avoidance cases, missing-argument cases (ask a clarifying question, Part 3 Q17), and error-recovery turns. A model trained only on successful calls over-calls tools.
- **Constrained decoding alternative:** a grammar guarantees valid JSON shape at generation time (Part 3 Q22) but not the right tool or right values. Fine-tuning improves the *choice*; constrained decoding guarantees the *syntax*. They combine well.
- **Evaluate:** tool-selection accuracy, argument accuracy, schema validity, no-tool precision, and multi-turn success (Part 3 Q44), on held-out tools too if you will add tools later.
- **When fine-tuning beats prompting:** dozens of tools (definitions eat the prompt, Part 3 Q30), a strict custom format, a small model that must be cheap and fast, or a stable tool set with lots of logged traffic.

**Example (illustrative data structure; the snippet only checks that it serialises to JSON, no training is run):**
```python
import json
example = {
  "messages": [
    {"role": "user", "content": "Refund order 4471, it arrived broken."},
    {"role": "assistant", "tool_calls": [
        {"type": "function", "function": {"name": "issue_refund", "arguments": {"order_id": "4471", "reason": "damaged"}}}]},
    {"role": "tool", "name": "issue_refund", "content": "{\"status\": \"ok\"}"},
    {"role": "assistant", "content": "Done: your refund for order 4471 has been issued."},
  ],
  "tools": [{"type": "function", "function": {
      "name": "issue_refund", "description": "Refund a delivered order.",
      "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}, "reason": {"type": "string"}},
                     "required": ["order_id", "reason"]}}}],
}
assert json.loads(json.dumps(example))["messages"][1]["tool_calls"][0]["function"]["name"] == "issue_refund"
print("structure serialises to valid JSON")   # structure check only; field names follow my reading of the TRL docs
```
The order id and message text are made up.

**Follow-ups:**
- *New tool added later?* Models fine-tuned on a fixed tool set can generalise poorly to unseen tools; include tool-schema variety in training or fall back to prompting for new tools.
- *Why include the final answer in the loss?* Because the model must also learn when to stop calling and answer.
- *Do you still validate?* Yes, schema validation and retries (Part 3 Q12).

**Common mistakes:** Putting tool results in the loss; only positive examples; template mismatch at inference; evaluating JSON validity but not whether the right tool was chosen; fine-tuning when a clearer tool description would fix it.

### Q29 ⭐⭐ 🟡 Continued pretraining vs SFT for a new domain or language: when do you need continued pretraining before SFT?
**Asked at:** product, GenAI startups, India product companies
**Say this first (1 line):** Continued pretraining (CPT) teaches the model a new domain's or language's vocabulary and text statistics through next-token loss on large amounts of raw text; SFT teaches behaviour on a smaller set of instruction-response pairs. I need CPT before SFT only when the base model has seen too little of that domain or language and I have enough raw text.

**Then explain:**
- **What each changes:** CPT shifts what the model knows and how fluently it writes in the domain (jargon, scripts, style). SFT shifts how it responds (format, task, tone). SFT cannot reliably add large amounts of new knowledge or fluency from a few thousand examples (Q2).
- **When CPT is justified:** (1) rare language or script where the model is weak, often with **tokenizer fragmentation**, so text costs many tokens (Part 2 Q17) and a tokenizer extension may be needed (Part 2 Q36); (2) dense domain jargon (legal, clinical, internal code) the base barely saw; (3) you hold a large raw corpus, on the order of many millions to billions of tokens (rough, depends on the gap).
- **When it is not:** the base already handles the domain (just SFT or LoRA), the corpus is small (use RAG for facts, Q1), or the budget cannot cover the compute.
- **Risks:** forgetting of general ability; mitigate by **mixing replay** of general text into the CPT stream, a lower LR than pretraining, and general-capability evals before and after (Q8).
- **Pipeline:** CPT on raw text (base checkpoint), then SFT for behaviour (Q36 on base vs instruct), then evals. Cost, data and risk comparison against pretraining and fine-tuning is in Part 2 Q8.
- **Cheaper probes first:** measure perplexity of the base on your domain text, and tokens per word. High perplexity and heavy fragmentation point to CPT; low gaps point to SFT.

**Example:** an Indian-language support bot where the base splits each word into many bytes and writes broken sentences: collect clean raw text, extend the tokenizer if needed, run CPT with a general-text replay slice, then SFT on instructions. For a Python-heavy internal codebase the base already knows Python: SFT or retrieval is enough.

**Follow-ups:**
- *Full fine-tune or LoRA for CPT?* LoRA is cheaper but has limited capacity to absorb a lot of new knowledge; large gaps often need full or high-rank training (Q4).
- *How much replay?* A tunable fraction, like the SFT mix in Q27; no universal value.
- *Does CPT make facts reliable?* No, facts still hallucinate; retrieval for facts.

**Common mistakes:** Using SFT to teach a language; running CPT with tiny data; no replay so the model forgets how to follow instructions; forgetting that CPT on a base then needs SFT again.

### Q30 ⭐⭐ 🟡 What does SFT overfitting look like (train vs validation loss, memorisation, narrow style), and what are your defences (early stopping, fewer epochs, regularisation, data)?
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** SFT overfitting shows up as training loss falling towards zero while validation loss turns upward, plus verbatim memorisation and a narrow, repetitive style; I defend with a good validation set, early stopping or fewer epochs, lower LR or smaller rank, weight decay or dropout, and above all more diverse data.

**Then explain:**
- **Signs:** train loss keeps dropping while val loss bottoms out then rises; the model reproduces training answers word for word; outputs sound the same whatever the prompt; general benchmarks regress (Q8); quality on held-out prompts is worse than an earlier checkpoint even though train loss is better.
- **Why it happens in SFT:** small datasets (hundreds to a few thousand examples) and many epochs; high-capacity model; repeated examples (Q27, Q34 dedup).
- **Defences:** hold out a validation set and checkpoint on it; early stopping (stop when val loss has not improved for N evals); 1-3 epochs is a common starting point, not a rule; lower LR; smaller LoRA rank or fewer target modules (Q4, Q5); weight decay and LoRA dropout; dedupe; add data diversity and replay. Do not trust val loss alone: check task metrics too (Q9), as lower loss does not always mean a better answer.
- **Analogy demo below:** it is NOT an LLM. An over-sized MLP fits 40 noisy points; it shows the same *shape* of curves that you look for in SFT.

**Example (from my run, analogy only):** without regularisation, train loss falls to 0.008 by epoch 2000 while val loss climbs from a best of 0.107 (epoch 355) to 0.160; the noise floor is 0.09. Early stopping with patience 100 stops at epoch 455 and keeps the epoch-355 checkpoint (0.107). AdamW with weight_decay 1.0 stays near 0.107 for all 2000 epochs (train 0.059). Seeds and settings matter; this is one run.

**Code:** (executed, torch CPU, synthetic)
```python
# ANALOGY, not an LLM: an over-sized MLP memorises 40 noisy points (y = sin(x) + noise).
# Train loss goes towards 0 while validation loss rises. Compare: no regularisation, weight decay, early stopping.
import torch, torch.nn as nn
torch.set_num_threads(1)   # tiny model: threads only add overhead
torch.manual_seed(0)
def make(n):
    x = torch.rand(n, 1) * 6 - 3
    return x, torch.sin(x) + 0.3 * torch.randn(n, 1)
xtr, ytr = make(40); xva, yva = make(400)

def run(wd, epochs=2000, patience=None):
    torch.manual_seed(1)
    m = nn.Sequential(nn.Linear(1, 128), nn.Tanh(), nn.Linear(128, 128), nn.Tanh(), nn.Linear(128, 1))
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3, weight_decay=wd)
    best, best_ep, hist, last_t, last_v = 1e9, 0, {}, 0, 0
    for ep in range(1, epochs + 1):
        opt.zero_grad(); l = nn.functional.mse_loss(m(xtr), ytr); l.backward(); opt.step()
        with torch.no_grad():
            v = nn.functional.mse_loss(m(xva), yva).item()
        if ep in (50, 200, 500, 2000): hist[ep] = (l.item(), v)
        if v < best: best, best_ep = v, ep
        if patience and ep - best_ep >= patience:       # early stopping: stop when val has not improved for `patience` epochs
            hist["stopped"] = ep; break
    return hist, best, best_ep

h, best, bep = run(0.0)
print("no regularisation (epoch: train, val):")
for ep, (t, v) in h.items(): print(f"  {ep:5d}: train {t:.4f}  val {v:.4f}")
print(f"  best val {best:.4f} at epoch {bep}")
h3, b3, e3 = run(0.0, patience=100)
print(f"early stopping (patience 100): stopped at epoch {h3['stopped']}, best val {b3:.4f} at epoch {e3}")
h2, best2, bep2 = run(1.0)
print("AdamW weight_decay=1.0 (epoch: train, val):")
for ep, (t, v) in h2.items(): print(f"  {ep:5d}: train {t:.4f}  val {v:.4f}")
print(f"  best val {best2:.4f} at epoch {bep2}")
print("noise floor of the data (0.3^2) = 0.09")
```
Output from my run:
```
no regularisation (epoch: train, val):
     50: train 0.0738  val 0.1203
    200: train 0.0617  val 0.1085
    500: train 0.0529  val 0.1078
   2000: train 0.0080  val 0.1598
  best val 0.1069 at epoch 355
early stopping (patience 100): stopped at epoch 455, best val 0.1069 at epoch 355
AdamW weight_decay=1.0 (epoch: train, val):
     50: train 0.0818  val 0.1230
    200: train 0.0635  val 0.1113
    500: train 0.0600  val 0.1084
   2000: train 0.0586  val 0.1074
  best val 0.1074 at epoch 2000
noise floor of the data (0.3^2) = 0.09
```

**Follow-ups:**
- *Is a rising val loss always bad?* In SFT, small rises with better task metrics can happen; I decide on task and general evals, not loss alone.
- *Epochs for SFT?* Few, because each example is seen with exact answers; check val after each.
- *Memorisation risk beyond quality?* Training data leakage of PII (Q34).

**Common mistakes:** No validation split; picking the last checkpoint instead of the best; many epochs over tiny data; treating weight decay as the main fix instead of data; reading the analogy demo as proof about LLMs.

### Q31 ⭐⭐ 🟡 What training-efficiency settings matter in practice (sequence packing, padding-free batches, gradient checkpointing, gradient accumulation, bf16), and what do they cost?
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** Packing and padding-free batches remove wasted compute on pad tokens, gradient checkpointing trades extra compute for much lower activation memory, gradient accumulation gives a bigger effective batch without more memory, and bf16 halves memory against fp32 with a wide exponent range; each has a cost I can name.

**Then explain:**
- **Padding waste:** padding every sequence to the batch max or a fixed length makes the GPU process pad tokens that carry no loss. **Packing** concatenates several examples into one fixed-length row. TRL docs (opened 2026-10-22; check the current docs, these change) list strategies `bfd` (best-fit decreasing: keeps examples whole), `bfd_split`, and `wrapped` (concatenate and cut, so examples may be split across rows). `padding_free` batches without pads and, per the docs, needs FlashAttention 2 or 3.
- **Packing risks:** attention should not leak across packed examples (position ids / masks must handle boundaries); with `wrapped` an example may be cut mid-way. Prefer strategies that keep examples whole when examples are short and distinct.
- **Gradient checkpointing:** do not store all activations; recompute them in the backward pass. Roughly one extra forward pass of compute (from memory, hedge) for a large drop in activation memory (Part 2 Q34).
- **Gradient accumulation:** sum gradients over k micro-batches before one optimizer step. For a mean loss it matches a k-times bigger batch if the loss is normalised over the same number of tokens; otherwise unequal sequence lengths bias it (Part 2 Q28).
- **bf16:** same exponent range as fp32, fewer mantissa bits, keeps fp32 optimizer state and master weights (Part 2 Q27).
- Cost side: checkpointing slows steps; packing changes effective sequence boundaries; accumulation lengthens wall time per update; bf16 needs hardware support.

**Example (synthetic lengths, lognormal, clipped to 16-1024; mean 317 tokens, 4,000 examples):** padding to the longest in batches of 8 wastes 57.1% of token slots, padding to a fixed 1024 wastes 69.0%; wrapped packing wastes 0.08% and best-fit-decreasing 0.16% (whole examples kept, 1,241 rows against 1,240). Real data will differ.

**Code:** (executed, numpy)
```python
# Padding waste with and without packing, on a synthetic length distribution (lognormal, clipped). Pure numpy.
import numpy as np
rng = np.random.default_rng(0)
MAXLEN = 1024
lens = np.clip(rng.lognormal(mean=5.5, sigma=0.8, size=4000).astype(int), 16, MAXLEN)   # synthetic token counts
print(f"{len(lens)} examples, mean length {lens.mean():.0f}, max {lens.max()}, real tokens {lens.sum():,}")

# 1) naive padding: batches of 8 in arrival order, each padded to the longest in the batch
B = 8
padded = sum(B * lens[i:i+B].max() for i in range(0, len(lens), B))
print(f"padded to batch max (batch {B}): slots {padded:,}  padding fraction {1 - lens.sum()/padded:.1%}")

# 2) padding to a fixed max_length for every example
fixed = len(lens) * MAXLEN
print(f"padded to fixed {MAXLEN}: slots {fixed:,}  padding fraction {1 - lens.sum()/fixed:.1%}")

# 3) packing: concatenate examples into rows of MAXLEN
def pack_wrapped(lens):
    """'wrapped'-style: concatenate everything and cut into MAXLEN rows (examples may be split across rows)."""
    return -(-lens.sum() // MAXLEN)                      # ceil rows; only the last row has padding

def pack_bfd(lens):
    """best-fit-decreasing bin packing: examples are kept whole, each placed in the fullest row that still fits."""
    free = []                                            # remaining space per row
    for L in sorted(lens, reverse=True):
        best, bi = None, None
        for i, f in enumerate(free):
            if f >= L and (best is None or f < best):
                best, bi = f, i
        if bi is None: free.append(MAXLEN - L)
        else: free[bi] -= L
    return len(free)

for name, rows in [("wrapped (cut across rows)", pack_wrapped(lens)), ("best-fit-decreasing (whole examples)", pack_bfd(lens))]:
    slots = rows * MAXLEN
    print(f"{name:38s}: rows {rows:5d} slots {slots:,}  padding fraction {1 - lens.sum()/slots:.2%}")
```
Output from my run:
```
4000 examples, mean length 317, max 1024, real tokens 1,268,750
padded to batch max (batch 8): slots 2,955,344  padding fraction 57.1%
padded to fixed 1024: slots 4,096,000  padding fraction 69.0%
wrapped (cut across rows)             : rows  1240 slots 1,269,760  padding fraction 0.08%
best-fit-decreasing (whole examples)  : rows  1241 slots 1,270,784  padding fraction 0.16%
```

**Follow-ups:**
- *Does packing change the result?* It can, because the number of examples per row varies, so loss normalisation and per-example weighting shift; check how your trainer averages.
- *Why is padding_free tied to FlashAttention?* The kernels can take variable-length sequences without a pad mask; check the docs for your version.
- *Which setting first?* bf16, then packing, then checkpointing if you run out of memory.

**Common mistakes:** Assuming accumulation is identical to a big batch with variable lengths; ignoring cross-example attention in packing; enabling checkpointing when memory is not the bottleneck; quoting defaults from memory instead of the docs.

### Q32 ⭐⭐ 🟡 How do you serve fine-tuned models: merged weights vs multi-LoRA serving, adapter swapping and versioning?
**Asked at:** product, platform teams, inference teams
**Say this first (1 line):** Merging an adapter into the base gives the simplest and fastest serving with one model per task; multi-LoRA serving keeps one base in memory and picks a small adapter per request, which saves memory when you have many tasks or customers.

**Then explain:**
- **Merged weights:** `W + (alpha/r) * B A` is baked in (Q13). No extra latency, standard serving stack, but each task is a full copy of the model in memory, and a QLoRA adapter does not merge directly into a 4-bit base (Q13).
- **Multi-LoRA:** the base matmul is shared and batched across all requests; the low-rank delta is added per request based on its adapter id. Memory is one base plus small adapters; hot-swapping and A/B routing are easy. Cost: extra kernel work per adapter, scheduling complexity, and a throughput hit when a batch mixes many adapters. Some servers support this; check the current docs of your serving stack (Part 10).
- **Versioning and rollback:** treat an adapter like a release: immutable id (`support-v2`), recorded base model hash, tokenizer and chat template version, training data version and eval scores. Rollback is a pointer change to the previous adapter, with no base reload. Keep the previous version warm for canary comparison.
- **Compatibility pitfalls:** adapter trained on base X must run on exactly base X (same revision and, if quantized, the same quantization recipe).
- **Choose:** few tasks, high traffic each, latency-critical: merge. Many tenants or tasks, low traffic each: multi-LoRA.

**Example (toy, run):** one frozen base layer, two random adapters standing in for trained ones. The same input gives different outputs per adapter, the same adapter twice gives identical output, the merged weight matches the adapter path, and rollback is a dictionary pointer change. It shows the mechanism only; it has no batching kernels.

**Code:** (executed, torch CPU, toy)
```python
# TOY multi-adapter serving: ONE frozen base layer, two LoRA adapters, adapter chosen per request.
# Not a real serving stack: it shows the idea (shared base matmul + small per-request low-rank delta).
import torch
torch.manual_seed(0)
d, r, alpha = 16, 4, 8
W = torch.randn(d, d) / d**0.5                       # frozen base weight, shared by everyone
def make_adapter():
    return {"A": torch.randn(r, d) * 0.5, "B": torch.randn(d, r) * 0.5}   # random stand-ins for trained adapters
adapters = {"support-v1": make_adapter(), "legal-v1": make_adapter()}

def forward(x, names):
    """x: (batch, d); names[i] = adapter for request i. Base matmul is batched across ALL requests."""
    base = x @ W.T
    out = base.clone()
    for i, n in enumerate(names):
        if n is None: continue                       # None = plain base model
        a = adapters[n]
        out[i] += (alpha / r) * (x[i] @ a["A"].T) @ a["B"].T     # per-request low-rank delta
    return out

x = torch.randn(1, d)
batch = x.repeat(4, 1)                               # same input, 4 requests with different adapters
y = forward(batch, ["support-v1", "legal-v1", None, "support-v1"])
print("same input, different adapter -> different output?")
print(" support vs legal :", not torch.allclose(y[0], y[1]))
print(" support vs base  :", not torch.allclose(y[0], y[2]))
print(" same adapter twice gives identical output:", torch.allclose(y[0], y[3]))
# merged-weights equivalence for one adapter
a = adapters["support-v1"]
W_merged = W + (alpha / r) * a["B"] @ a["A"]
print(" merged W matches adapter path:", torch.allclose(x @ W_merged.T, y[0:1], atol=1e-5))
# versioning/rollback toy: adapter registry
adapters["support-v2"] = make_adapter()
active = {"support": "support-v2"}
active["support"] = "support-v1"                     # rollback is a pointer change, no base reload
print(" active support adapter after rollback:", active["support"])
```
Output from my run:
```
same input, different adapter -> different output?
 support vs legal : True
 support vs base  : True
 same adapter twice gives identical output: True
 merged W matches adapter path: True
 active support adapter after rollback: support-v1
```

**Follow-ups:**
- *Can you quantize the base and serve adapters?* Yes in principle, but check that the serving stack supports it and re-evaluate quality (Q13).
- *How do you deploy safely?* Canary a slice of traffic, compare eval and user metrics, keep a rollback id.
- *What breaks on a base upgrade?* All adapters must be retrained or re-validated.

**Common mistakes:** Merging for dozens of tenants and paying for dozens of full models; no record of base revision and template; forgetting the template belongs to the adapter version; assuming mixed-adapter batches are free.

### Q33 ⭐⭐ 🟡 Hosted fine-tuning APIs vs self-hosted fine-tuning: what are the trade-offs in control, data privacy, cost and lock-in?
**Asked at:** product, GCC, regulated-industry teams
**Say this first (1 line):** Hosted fine-tuning is quicker to start and has less ops work; self-hosted gives control over data, model, cost and evaluation, at the price of running the stack; in regulated settings the data-residency and audit requirements usually decide it.

**Then explain:**
- **Control:** hosted: a fixed menu of base models and settings the provider allows. Self-hosted: any open-weight base, any recipe (LoRA, full, QLoRA), your own inference stack and decoding control.
- **Data privacy and residency:** hosted means training data leaves your environment under the provider's terms; read what is retained, where, and whether it is used for training. Self-hosted keeps it in your account or on premises. For regulated data (health, finance, personal data) legal review may force self-hosting or a private deployment. I would not assume any provider's policy; check the provider's current docs and contract.
- **Cost model:** hosted charges per training token and often higher per-token inference for the tuned model; self-hosted charges GPU time plus engineering, and has the break-even logic of Q25. No prices from me, because they change.
- **Lock-in and deprecation risk:** a hosted tuned model usually cannot leave the platform, and base models get retired, forcing re-tuning. Open weights you control do not vanish, though you maintain them. Keep the dataset and eval set portable either way.
- **Evaluation ownership:** you own the eval set in both cases. Never let the vendor's dashboard be your only evidence; run your own held-out and regression tests (Q9).
- **Speed to value:** hosted is good for a pilot to learn whether fine-tuning helps at all; move to self-hosted when volume, privacy or control justify it.

**Example:** a bank pilots a classifier-style assistant on a hosted service with synthetic and scrubbed data (Q34) to test value in two weeks; once production traffic and compliance need on-premise processing, it re-trains a LoRA on an open-weight base using the same dataset and eval set.

**Follow-ups:**
- *What do you keep portable?* Cleaned dataset, eval harness, prompts/templates, and recorded hyperparameters.
- *What if the vendor deprecates the base?* Budget for re-tuning and re-evaluation; that is why a portable pipeline matters.
- *Mixed approach?* Hosted for experiments, self-hosted for production.

**Common mistakes:** Assuming hosted data is automatically private or automatically unsafe, without reading terms; ignoring deprecation; comparing only sticker prices; trusting vendor-reported quality instead of your own eval.

### Q34 ⭐⭐ 🟡 How do you keep PII and benchmark contamination out of fine-tuning data (deduplication, held-out sets, filtering)?
**Asked at:** product, GCC, regulated-industry teams
**Say this first (1 line):** I scrub PII with patterns plus NER and human review, deduplicate exact and near-duplicate examples, split train and eval by group so near-copies never straddle them, and decontaminate against public benchmarks and my own eval set.

**Then explain:**
- **PII:** regex catches structured patterns (emails, phone-like numbers, card-like numbers) but misses names, addresses, free-form ids and anything in odd formats. Add NER-based detection, sample and review the output, log what was removed, and keep raw data access-controlled. Replace with typed placeholders (`<EMAIL>`) so the text stays natural. Fine-tuned models can memorise rare strings (Q30), so scrub before training, not after.
- **Dedup:** exact (hash of normalised text) first, then near-duplicate (shingles with Jaccard, or MinHash at scale, or embedding similarity with a threshold). Duplicates inflate memorisation and make eval scores look better.
- **Leakage between train and eval:** dedup across the two sets, not only within each, and split by group (same customer, same template, same document), otherwise paraphrases leak and the eval is optimistic.
- **Benchmark contamination:** remove examples overlapping with public benchmarks you will report on (n-gram overlap; methods in Part 2 Q30) and keep a private held-out set that never enters any training or prompt-tuning.
- **Process:** version the data, record filters and counts, rerun the eval after each cleaning step.

**Example (made-up data, run):** the scrub turns an email and Indian mobile number into placeholders but leaves "Priya Sharma" and "12 MG Road, Pune 411001" intact, which is why regex alone is not enough. Normalised exact dedup removes 1 of 5 rows after scrubbing; the near-duplicate with an extra word has Jaccard 0.44 against its neighbour (below a typical high threshold, so a threshold choice matters). With 200 templated tickets, a random row split puts 40 of 40 eval items on templates also in train; a group split puts 0 of 40.

**Code:** (executed, standard library only; the regexes are illustrative and incomplete)
```python
# ILLUSTRATIVE and INCOMPLETE PII scrubbing + dedup + split-before-dedup. Regex misses names, addresses, IDs in other formats.
# Use NER-based tools plus human review for real data. Data below is made up.
import re, hashlib, random
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")   # Indian mobile-like only
def scrub(t):
    t = EMAIL.sub("<EMAIL>", t)
    return PHONE.sub("<PHONE>", t)

rows = [
 "Hi, I am Priya Sharma, mail me at priya.sharma@example.com or call +91 98765 43210.",
 "Refund for order 4471 please. Contact: rahul_k@mail.example.org, 9123456780",
 "Refund for order 4471 please. Contact: rahul_k@mail.example.org, 9123456780",       # exact dup
 "refund for order 4471 please, thanks!  contact: someone@else.example.net, 9000011111",   # near dup
 "I live at 12 MG Road, Pune 411001. Cancel my plan.",
]
for r in rows[:2] + rows[4:]:
    print("IN :", r); print("OUT:", scrub(r))
print("-> names ('Priya Sharma') and the street address survive: regex is not enough.\n")

def norm(t):                                    # normalise before comparing
    t = scrub(t).lower()
    return re.sub(r"[^a-z0-9 ]+", " ", re.sub(r"\s+", " ", t)).strip()
def shingles(t, n=3):
    w = norm(t).split(); return {" ".join(w[i:i+n]) for i in range(max(1, len(w)-n+1))}
def jaccard(a, b): return len(a & b) / len(a | b)

# 1) exact dedup on normalised hash; 2) near-dup via Jaccard of word 3-shingles
seen, uniq = {}, []
for r in rows:
    h = hashlib.md5(norm(r).encode()).hexdigest()
    if h in seen: continue
    seen[h] = r; uniq.append(r)
print("after exact dedup (normalised):", len(rows), "->", len(uniq))
print("Jaccard row1 vs row3:", round(jaccard(shingles(rows[1]), shingles(rows[3])), 2))

# Dedup ACROSS train and eval (not only inside each), and split by GROUP, so a near-duplicate never straddles the two sets.
random.seed(0)
pool = [f"ticket template {i%50} variant {i}" for i in range(200)]        # 50 templates x 4 variants
def leak(train, test):
    tk = {t.rsplit(" variant", 1)[0] for t in train}
    return sum(t.rsplit(" variant", 1)[0] in tk for t in test)
random.shuffle(pool); tr_rand, te_rand = pool[:160], pool[160:]
groups = sorted({p.rsplit(" variant", 1)[0] for p in pool})
te_g = set(groups[:10])
te_grp = [p for p in pool if p.rsplit(" variant", 1)[0] in te_g]
tr_grp = [p for p in pool if p.rsplit(" variant", 1)[0] not in te_g]
print("random row split: eval items whose template is also in train:", leak(tr_rand, te_rand), "of", len(te_rand))
print("group split     : eval items whose template is also in train:", leak(tr_grp, te_grp), "of", len(te_grp))
```
Output from my run:
```
IN : Hi, I am Priya Sharma, mail me at priya.sharma@example.com or call +91 98765 43210.
OUT: Hi, I am Priya Sharma, mail me at <EMAIL> or call <PHONE>.
IN : Refund for order 4471 please. Contact: rahul_k@mail.example.org, 9123456780
OUT: Refund for order 4471 please. Contact: <EMAIL>, <PHONE>
IN : I live at 12 MG Road, Pune 411001. Cancel my plan.
OUT: I live at 12 MG Road, Pune 411001. Cancel my plan.
-> names ('Priya Sharma') and the street address survive: regex is not enough.

after exact dedup (normalised): 5 -> 4
Jaccard row1 vs row3: 0.44
random row split: eval items whose template is also in train: 40 of 40
group split     : eval items whose template is also in train: 0 of 40
```

**Follow-ups:**
- *How strict a near-dup threshold?* Inspect samples around the threshold; too loose deletes useful variety, too tight leaves leaks.
- *Is deleting PII enough for compliance?* No; legal and privacy review decide, and processes need audit trails.
- *Contamination detection after training?* Compare performance on a fresh private set against the public benchmark (Part 2 Q30).

**Common mistakes:** Trusting regex as PII removal; deduping inside train only; random split of grouped data; scrubbing the eval set differently from train; no record of what was filtered.

### Q35 ⭐⭐ 🟡 A fine-tune did not learn or got worse. Walk through your debugging checklist (template, masking, learning rate, data, evaluation).
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** I check the cheap, common causes in order: look at actual decoded training examples, then the template and EOS, the masking ratio and label shift, whether the adapter is attached and trainable, the learning rate and loss curve, dropout and train/eval mode, and finally whether the evaluation measures the right thing and whether I started from the right checkpoint.

**Then explain (ordered checklist):**
1. **Inspect data:** decode a few batches, with special tokens visible. Are answers correct, deduped, in the right language and format (Q10)?
2. **Template and EOS:** the same chat template at train and inference, and an EOS the model learns to emit (Q12). Missing EOS gives never-ending outputs.
3. **Masking ratio:** what share of tokens are supervised (Q11)? 0% masked means prompts are in the loss; about 100% masked means nothing is learned.
4. **Label shift:** in the common setup labels equal input ids and the trainer shifts internally; shifting them yourself too trains the wrong target.
5. **Trainable parameters:** count them. Is the LoRA adapter attached to the modules you meant (Q5), with `requires_grad` true, and is the optimizer given them?
6. **Learning rate:** too high gives NaN or garbage, too low a flat loss. Adapter training usually uses a higher LR than full fine-tuning (about 1e-4 vs 2e-5 default per the TRL docs; check the current docs).
7. **Dropout and mode:** `model.train()` during training, `model.eval()` for evaluation.
8. **Eval mismatch:** different prompt format, decoding settings or metric than training; a validation set from another distribution; look at samples, not only a score (Q9).
9. **Base vs instruct:** wrong checkpoint for the data or template (Q36).
10. **Then** quantisation issues, bad batching, data volume, and forgetting (Q8).
- A tiny overfit test (can the model memorise 10 examples?) separates pipeline bugs from data or capacity problems.

**Example (toy run):** the diagnostic reports masked fraction, whether labels equal inputs or the next input, trainable and adapter parameter counts, and EOS presence. On a healthy toy batch it flags nothing. On a batch with no masking, a frozen adapter, no EOS and eval mode it flags no masking, no trainable adapter parameters, missing EOS and eval mode. On pre-shifted labels it flags "double shift". When all labels are ignored it says so. Thresholds are rules of thumb, not standards.

**Code:** (executed, torch CPU, toy model; no library)
```python
# Diagnostic over a toy SFT batch: masked fraction, label shift, trainable params, suspicious-value flags. Toy model, no library.
import torch, torch.nn as nn
IGNORE = -100
def diagnose(model, input_ids, labels, eos_id, adapter_prefix="lora_"):
    flags = []
    valid = labels != IGNORE
    masked_frac = 1 - valid.float().mean().item()
    # label shift: in a correct HF-style batch, labels == input_ids at unmasked positions (the model shifts internally).
    same = (labels[valid] == input_ids[valid]).float().mean().item() if valid.any() else float("nan")
    # if labels were already shifted by the user, label[t] == input[t+1] and the double shift trains the wrong target
    shifted_match = (labels[:, :-1][labels[:, :-1] != IGNORE] == input_ids[:, 1:][labels[:, :-1] != IGNORE]).float().mean().item() \
        if (labels[:, :-1] != IGNORE).any() else float("nan")
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    adapters = sum(p.numel() for n, p in model.named_parameters() if adapter_prefix in n and p.requires_grad)
    last_has_eos = (input_ids[:, -1] == eos_id).float().mean().item()
    if masked_frac == 0: flags.append("no masking: prompt tokens are in the loss")
    if masked_frac > 0.95: flags.append("almost everything masked: few or no supervised tokens")
    if (~valid).all(): flags.append("ALL labels ignored: loss will be NaN/0")
    if shifted_match > same and shifted_match > 0.9: flags.append("labels look pre-shifted: double shift")
    if trainable == 0: flags.append("no trainable parameters")
    if adapter_prefix and adapters == 0: flags.append("no trainable adapter parameters (adapter not attached or frozen)")
    if trainable / total > 0.5 and adapter_prefix: flags.append("most params trainable: expected adapter-only?")
    if last_has_eos < 0.5: flags.append("EOS missing at sequence end")
    if not model.training: flags.append("model in eval mode: dropout off")
    print(f"masked {masked_frac:.1%} | labels==inputs {same:.2f} | labels==next-input {shifted_match:.2f} | "
          f"trainable {trainable}/{total} (adapter {adapters}) | EOS-final {last_has_eos:.0%}")
    print("FLAGS:", flags or "none")

class Tiny(nn.Module):
    def __init__(self, lora=True):
        super().__init__()
        self.emb = nn.Embedding(50, 8); self.base = nn.Linear(8, 8)
        self.lora_A = nn.Parameter(torch.zeros(2, 8)); self.lora_B = nn.Parameter(torch.zeros(8, 2))
        for p in list(self.emb.parameters()) + list(self.base.parameters()): p.requires_grad = False
        if not lora: self.lora_A.requires_grad = self.lora_B.requires_grad = False

EOS = 2
ids = torch.tensor([[5, 6, 7, 8, 9, EOS], [5, 6, 10, 11, 12, EOS]])
good = ids.clone(); good[:, :3] = IGNORE                       # prompt masked, answer supervised
print("== healthy batch"); diagnose(Tiny(), ids, good, EOS)
print("== bad: no masking, adapter frozen, no EOS, eval mode")
noeos = ids.clone(); noeos[:, -1] = 0
m = Tiny(lora=False).eval()
diagnose(m, noeos, noeos.clone(), EOS)
print("== bad: labels pre-shifted by the user")
pre = torch.full_like(ids, IGNORE); pre[:, 2:-1] = ids[:, 3:]     # label[t] = input[t+1]
diagnose(Tiny(), ids, pre, EOS)
print("== bad: everything masked")
diagnose(Tiny(), ids, torch.full_like(ids, IGNORE), EOS)
```
Output from my run:
```
== healthy batch
masked 50.0% | labels==inputs 1.00 | labels==next-input 0.00 | trainable 32/504 (adapter 32) | EOS-final 100%
FLAGS: none
== bad: no masking, adapter frozen, no EOS, eval mode
masked 0.0% | labels==inputs 1.00 | labels==next-input 0.00 | trainable 0/504 (adapter 0) | EOS-final 0%
FLAGS: ['no masking: prompt tokens are in the loss', 'no trainable parameters', 'no trainable adapter parameters (adapter not attached or frozen)', 'EOS missing at sequence end', 'model in eval mode: dropout off']
== bad: labels pre-shifted by the user
masked 50.0% | labels==inputs 0.00 | labels==next-input 1.00 | trainable 32/504 (adapter 32) | EOS-final 100%
FLAGS: ['labels look pre-shifted: double shift']
== bad: everything masked
masked 100.0% | labels==inputs nan | labels==next-input nan | trainable 32/504 (adapter 32) | EOS-final 100%
FLAGS: ['almost everything masked: few or no supervised tokens', 'ALL labels ignored: loss will be NaN/0']
```

**Follow-ups:**
- *Loss falls but outputs are bad?* Suspect eval or template mismatch, masking, or data quality before blaming the model.
- *Loss is flat?* Adapter not trainable, LR too low, all labels masked, or wrong labels.
- *Got worse than base?* Forgetting (Q8), overfitting (Q30), or a narrow mixture (Q27).

**Common mistakes:** Tuning hyperparameters before reading the data; not counting trainable parameters; judging by loss alone; changing several things at once.

### Q36 ⭐⭐ 🟡 Should you fine-tune a base or an instruct/chat checkpoint? What are the trade-offs?
**Asked at:** product, GenAI startups, fine-tuning teams
**Say this first (1 line):** I usually fine-tune the instruct checkpoint for a modest behaviour change on small or medium data, because it keeps chat ability and safety tuning; I start from the base when I want a clean slate for a big behaviour shift, have a lot of data, or need my own template and alignment.

**Then explain:**

| | Instruct/chat checkpoint | Base checkpoint |
|---|---|---|
| Starting point | follows instructions, has safety behaviour, uses its own chat template | raw next-token model, no instruction habits |
| Data needed | less; you adjust style or task | more; you teach instruction following too |
| Prior | strong, can resist big changes or leak its old style | weak, easy to reshape |
| Risks | forgetting its tuning, template mismatch (Q12), stacking SFT on top of RLHF/DPO-tuned behaviour | needs your own safety and alignment work (Part 5), longer pipeline |
| Template | must use the model's exact template | you can choose one |

- **Template alignment:** with an instruct model, format data in its own template and special tokens. With a base model, pick a template and train its tokens (the embeddings of new special tokens start untrained, Q12).
- **Forgetting:** fine-tuning an instruct model on narrow data can undo parts of its chat and safety behaviour (Q8); evaluate refusals and general ability afterwards.
- **Licensing:** check the licence of each checkpoint and of the data used to produce outputs; base and instruct variants can carry different terms, so read them.
- **Rule of thumb:** small data (hundreds to a few thousand examples), narrow adaptation: instruct. Tens of thousands plus, new format or domain with CPT (Q29): base. It is a judgement; the best answer comes from comparing both on your eval (Q9), because there is no universal winner.

**Example:** adding a company tone and a JSON extraction format with 3,000 examples: instruct plus LoRA. Building a specialised assistant for a new language with a large instruction set after CPT: base, then SFT, then preference tuning.

**Follow-ups:**
- *Can you fine-tune an instruct model with the base model's template?* You can, but mismatched templates usually hurt; use the instruct template.
- *Which one is cheaper?* Instruct, since less data and training are needed.
- *Safety?* Re-check refusal behaviour after tuning either way.

**Common mistakes:** Using the base model's template on instruct (or the reverse); assuming instruct is always better; ignoring that an instruct model may resist a drastic style change; skipping licence review.

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

### Q43 ⭐ 🔴 Design question: build an end-to-end fine-tuning project for a support-ticket extraction task (data, training, evaluation gates, regression checks, rollout and rollback).
**Asked at:** senior roles at product companies, GCCs, GenAI startups
**Say this first (1 line):** I start with a prompted-model baseline and a golden set, fine-tune only if the baseline misses the quality, cost or latency target, and I ship through hard gates: per-field F1 against the baseline, a regression suite, latency and cost budgets, then shadow, canary, and a ready rollback.

**Then explain:**
- **1. Framing:** the task is ticket text to JSON with fixed fields (for example category, priority, product, order id). Define each field's rules, allowed values and what "absent" means (null, not a guess). Write the success bar with the business: per-field F1, invalid-JSON rate, cost per 1,000 tickets, p95 latency.
- **2. Baseline first:** a prompted model with schema-constrained output (Part 3). Measure it. If it already clears the bar, stop. Fine-tuning pays when the baseline is too expensive or slow at volume, a smaller fine-tuned model can match it, or a few fields keep failing on company-specific wording.
- **3. Data:** sample real tickets across channels, products, languages and months. Label with a guideline, two annotators on a sample, measure agreement, resolve disputes; LLM pre-labels are fine if humans review them. Dedup near-duplicates (the same ticket appears via email threads), remove or mask PII (names, phones, emails, card numbers) before any data leaves its store, and check the legal basis for using customer text.
- **4. Splits:** split by time and by customer or thread, not by random row, so the test mimics the future and no thread leaks between train and test. Keep a frozen golden set nobody trains on, plus a hard slice (rare fields, long tickets, mixed languages, adversarial text).
- **5. Training:** SFT with LoRA or QLoRA on a right-sized base (Q42), loss only on the JSON, chat template matching serving, constrained decoding at inference. Start from small data (a few hundred to a few thousand examples is a plausible range, but I would plot a data-size curve rather than assume). Track against the baseline each epoch.
- **6. Eval gates (all must pass):** per-field F1 not below the baseline by more than a margin and above an absolute floor; invalid-JSON rate; a regression suite of previously failed tickets and prompt-injection-like tickets; general-ability sanity if the model is also used elsewhere (Q8); p95 latency; cost per 1,000.
- **7. Rollout:** shadow mode (candidate runs on live traffic, outputs logged, not used) then canary (a small share of traffic, a human-review sample) then gradual ramp. Rollback = flip a config flag to the previous model or the prompted baseline; keep both deployable.
- **8. Monitoring and retraining:** log field null-rates, value distributions, schema failures, disagreement with a weekly human-labelled sample, latency and cost. Retrain triggers: F1 on the weekly sample drops below a threshold, new product or category names appear, input distribution shifts (Part 11).
- **Gate function:** the code compares candidate to baseline per field on a synthetic golden set. The data and the "models" are simulated (label: synthetic); only the gate logic is meant to be reused.

| Run (synthetic) | priority F1 base to cand | other fields | latency p95 | Gate |
|---|---|---|---|---|
| Candidate A | 0.877 to 0.938 | all up | 420 ms | pass |
| Candidate B | 0.877 to 0.858 | all up | 950 ms | fail: priority regressed, latency over 800 ms budget |

**Example:** candidate B improves three fields strongly, and still fails: one field regressed and latency broke the budget. A single average F1 would have hidden the priority regression, which is why the gate works per field.

**Code:** (executed, standalone, stdlib only; SYNTHETIC golden set and simulated outputs; thresholds are illustrative)
```python
# Standalone, python stdlib only. SYNTHETIC golden set and simulated model outputs; no model is called.
import random
random.seed(0)
FIELDS = {"category": ["billing", "bug", "access", "other"], "priority": ["low", "med", "high"],
          "product": ["app", "web", "api"], "order_id": None}

def make_gold(n=400):
    rows = []
    for i in range(n):
        r = {f: random.choice(v) for f, v in FIELDS.items() if v}
        r["order_id"] = f"ORD{random.randint(1000, 9999)}" if random.random() < 0.6 else None   # absent in 40%
        rows.append(r)
    return rows

def simulate(gold, acc, abstain=0.0, hallucinate_id=0.0):                                    # fake model outputs
    out = []
    for g in gold:
        p = {}
        for f, v in FIELDS.items():
            if v: p[f] = g[f] if random.random() < acc[f] else random.choice(v)
        if g["order_id"] is None: p["order_id"] = f"ORD{random.randint(1000, 9999)}" if random.random() < hallucinate_id else None
        else: p["order_id"] = g["order_id"] if random.random() < acc["order_id"] else (None if random.random() < abstain else "ORD0000")
        out.append(p)
    return out

def field_f1(gold, pred, f):
    tp = sum(1 for g, p in zip(gold, pred) if g[f] is not None and p[f] == g[f])
    n_pred = sum(1 for p in pred if p[f] is not None); n_gold = sum(1 for g in gold if g[f] is not None)
    prec, rec = tp / max(n_pred, 1), tp / max(n_gold, 1)
    return 2 * prec * rec / max(prec + rec, 1e-9)

def gate(gold, base_pred, cand_pred, cand_latency_p95_ms, base_cost_per_1k, cand_cost_per_1k,
         min_f1=0.80, max_regress=0.01, latency_budget_ms=800, cost_ratio_max=1.0):
    reasons, rows = [], {}
    for f in FIELDS:
        b, c = field_f1(gold, base_pred, f), field_f1(gold, cand_pred, f); rows[f] = (round(b, 3), round(c, 3))
        if c < min_f1: reasons.append(f"{f}: F1 {c:.3f} below absolute floor {min_f1}")
        if c < b - max_regress: reasons.append(f"{f}: regressed {b:.3f} -> {c:.3f}")
    if cand_latency_p95_ms > latency_budget_ms: reasons.append(f"latency p95 {cand_latency_p95_ms}ms > {latency_budget_ms}ms")
    if cand_cost_per_1k > base_cost_per_1k * cost_ratio_max: reasons.append(f"cost {cand_cost_per_1k} > baseline {base_cost_per_1k}")
    return {"pass": not reasons, "per_field_f1 (base, cand)": rows, "reasons": reasons}

gold = make_gold()
base = simulate(gold, {"category": .86, "priority": .83, "product": .90, "order_id": .85}, abstain=.2, hallucinate_id=.08)
good = simulate(gold, {"category": .93, "priority": .90, "product": .95, "order_id": .96}, abstain=.2, hallucinate_id=.02)
bad  = simulate(gold, {"category": .95, "priority": .78, "product": .95, "order_id": .97}, abstain=.2, hallucinate_id=.02)
print("candidate A:", gate(gold, base, good, 420, 5.0, 1.2))
print("candidate B:", gate(gold, base, bad, 950, 5.0, 1.2))

```

**Follow-ups:**
- *What if there are few labels?* Prompt with few-shot first; use a strong model to pre-label then review, and fine-tune later. With about 50 examples, few-shot is the better answer (Q1).
- *How do you handle PII?* Mask before labelling and training, restrict access, keep a retention policy, and check outputs for leakage. The legal side is for the company's policy and counsel.
- *When do you drop the fine-tune?* When the prompted frontier model gets cheaper or better and meets the gate at acceptable cost: re-run the gate against it every quarter.

**Common mistakes:**
- Random row split with the same thread in train and test.
- One overall score instead of per-field results.
- No null handling: the model learns to invent order ids.
- No rollback path, or no plan to re-measure the baseline.

### Q44 ⭐ 🔴 Can fine-tuning inject new facts? Why does it often fail compared with retrieval, and what does the evidence say?
**Asked at:** senior roles at product companies, GenAI startups, research-leaning teams
**Say this first (1 line):** Sometimes a little, but it is unreliable and it can make hallucination worse, so for facts I use retrieval and I use fine-tuning for form, behaviour and cost. The exception is heavy continued pretraining on a large domain corpus, which is a different job from a small SFT.

**Then explain:**
- **Why SFT on a few facts is weak:**
  - A few thousand Q&A pairs, seen a few epochs, teach the model to answer in that shape, but the fact is stored only as a brittle association. Rephrase the question and it may not recall (the "reversal curse" and paraphrase failures are commonly reported; named as from memory, not verified).
  - Pushing the model to give answers it cannot connect to what it already knows can encourage it to guess confidently. Gekhman et al., 2024, "Does fine-tuning LLMs on new knowledge encourage hallucinations?" reports roughly this (from memory, not verified: new-knowledge examples are learned slowly and, once learned, raise hallucination on other questions). Read the paper before quoting it.
  - Overfitting to the training set, and forgetting of other abilities (Q8).
- **Operational reasons against it:** facts go stale (every update is a new training run); no citation or source; no access control (the model may reveal training text to everyone); hard to delete one fact; evaluation is hard (you need paraphrase tests).
- **What I use instead:** RAG for facts, with citations and permissions (Parts 6 and 7); fine-tune to teach the model *how* to use retrieved context, output format, tone, refusal behaviour, and to say "not found".
- **Where fact-heavy training does work:** continued pretraining on a large in-domain corpus (billions of tokens, Part 2 Q8) can change what the model knows, at much higher cost and with the same staleness issue. Some teams combine: continued pretraining for domain language, RAG for current facts.
- **How I would test a claim "the model learned it":** ask the fact in 5 to 10 paraphrases, in reverse direction, inside multi-step questions, and for facts the model did not see (to catch invented answers); compare to RAG on the same set.

**Example:** a company's price list changes every month. Fine-tuning on the old list yields confident, outdated prices, with no citation. Retrieval from the current price table gives the right number and the source. If the bot also needs the company's reply style, fine-tune that part with a few hundred examples.

**Follow-ups:**
- *So never fine-tune on domain facts?* For stable, widely repeated domain knowledge at scale (continued pretraining), it can help. For a small, changing, or private document set, use retrieval.
- *Does RAG plus fine-tuning conflict?* No. Fine-tune with examples that include retrieved passages, so the model learns to rely on them and to abstain when they lack the answer.
- *What about "knowledge editing" methods?* Research area (locate-and-edit approaches); I would treat them as experimental, not production, and say I have not validated them.

**Common mistakes:**
- Fine-tuning on documents and expecting reliable Q&A.
- Testing only with the exact training questions.
- Claiming research results with exact numbers from memory.
- Forgetting that fine-tuned facts cannot be cited or access-controlled.

### Q45 ⭐ 🔴 What are the pitfalls of distillation (capacity gap, exposure bias, evaluation, teacher licensing terms), and when does it fail?
**Asked at:** senior roles at product companies, GenAI startups, big tech
**Say this first (1 line):** Distillation fails when the student cannot represent what the teacher knows, when the student only sees teacher-written text and never its own mistakes, when evaluation looks only at the average, and when the teacher's errors, biases or licence terms come along with the data.

**Then explain:**
- **Capacity gap:** if the student is far smaller than the teacher, it may not benefit and the soft targets can even be a worse teaching signal than hard labels. A common mitigation is an intermediate "teacher assistant" model (Mirzadeh et al., 2020, from memory, not verified). In my toy, a linear student trained with soft targets from an MLP teacher reached 0.942 overall accuracy, no better than the same student with hard labels (0.940); a small MLP student with the same soft targets reached 0.991 (teacher 0.992).
- **Exposure bias:** in sequence distillation the student trains on teacher-written prefixes, but at inference it conditions on its own, which drift. Mitigations: on-policy distillation where the student samples and the teacher scores (MiniLLM's abstract describes on-policy optimisation with reverse KL, Q24); also mix student samples into training.
- **Teacher errors and bias inherited:** the student copies hallucinations, refusals, political or demographic bias and the teacher's style. Filter by correctness or a checker (Q39), audit slices.
- **Evaluation:** an average can hide the tail. In the toy, a rare slice (3% of data) was answered correctly 0.77 of the time by the teacher and 0.53 by the linear student, while overall numbers were 0.992 and 0.942. Even the teacher's tail was far below its average. I evaluate by slice, by difficulty, on safety prompts, on long inputs and in production-like conditions, not only on a benchmark average (Part 9).
- **Licensing and terms:** model licences and API terms may forbid using outputs to train other models, or restrict who may use the student. Check the current terms, and have legal sign off. I do not assume a given provider's rule.
- **Tokenizer mismatch (logit KD):** probability-matching needs the same vocabulary and token ids. With sizes 32,000 vs 50,000 the KL fails in the toy; real pairs may have the same size but different ids, which silently misaligns. Options: same-family models, vocabulary alignment methods (research), or black-box text distillation.
- **Over-reliance on teacher style:** the student learns phrasing and length habits; if the teacher is verbose, so is the student, and costs go up. Style-match is not skill-match.
- **When not to distil:** no clear cost or latency problem; a prompted large model is good enough; the task is mostly new knowledge; the licence forbids it; the student is too small for the skill.

**Example:** distilling a 70B into a 1B for classification of tickets: average F1 matches, but the rare "legal complaint" class drops sharply. The team only noticed because the gate has a per-class check (Q43). They then trained a 3B student and kept a rule to route low-confidence tickets to the large model.

**Code:** (executed, standalone, torch only; SYNTHETIC 2-D data; teacher is a small MLP; this is a toy, not an LLM)
```python
# Standalone, torch only. SYNTHETIC 2-D data. Shows: a too-small student can match the teacher's average accuracy
# and still lose a rare slice, so the average metric hides it. Also a vocabulary-mismatch check for logit KD.
import torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(1); torch.manual_seed(0)

def make(n):
    x = torch.randn(n, 2) * 1.0
    y = (x[:, 0] > 0).long()                                     # majority rule: linear
    rare = torch.rand(n) < 0.03                                  # 3% rare slice in its own region
    x[rare] = torch.randn(int(rare.sum()), 2) * 0.3 + torch.tensor([3.0, 3.0])
    y[rare] = ((x[rare, 0] > 3.0) ^ (x[rare, 1] > 3.0)).long()      # inside the slice the rule is XOR (needs nonlinearity)
    return x, y, rare
xtr, ytr, _ = make(20000); xte, yte, rte = make(20000)

def fit(model, loss_fn, steps=1500, lr=0.05):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for _ in range(steps):
        opt.zero_grad(); loss_fn(model(xtr)).backward(); opt.step()
    return model
def report(name, m):
    with torch.no_grad(): p = m(xte).argmax(-1)
    print(f"{name:<28} overall acc {(p==yte).float().mean():.3f}   rare-slice acc {(p[rte]==yte[rte]).float().mean():.3f}")

teacher = fit(nn.Sequential(nn.Linear(2, 32), nn.Tanh(), nn.Linear(32, 32), nn.Tanh(), nn.Linear(32, 2)), lambda o: F.cross_entropy(o, ytr))
with torch.no_grad(): soft = F.softmax(teacher(xtr), -1)
student_kd = fit(nn.Linear(2, 2), lambda o: F.kl_div(F.log_softmax(o, -1), soft, reduction="batchmean"))      # linear student, KD only
student_hard = fit(nn.Linear(2, 2), lambda o: F.cross_entropy(o, ytr))
big_kd = fit(nn.Sequential(nn.Linear(2, 16), nn.Tanh(), nn.Linear(16, 2)), lambda o: F.kl_div(F.log_softmax(o, -1), soft, reduction="batchmean"))
print(f"rare slice share of test set: {rte.float().mean():.3f}")
report("teacher (MLP 32x32)", teacher); report("student linear + KD", student_kd)
report("student linear, hard labels", student_hard); report("student MLP 16 + KD", big_kd)

# logit KD needs the same vocabulary / token ids
teacher_vocab, student_vocab = 32000, 50000
try:
    t = torch.randn(1, teacher_vocab); s = torch.randn(1, student_vocab)
    F.kl_div(F.log_softmax(s, -1), F.softmax(t, -1), reduction="batchmean")
except RuntimeError as e: print("\nlogit KD with different vocab sizes fails:", str(e)[:70])

```

**Follow-ups:**
- *Forward or reverse KL?* Forward KL is mass-covering and can spread the student over modes it cannot fit; reverse KL is mode-seeking (the MiniLLM abstract uses reverse KL for generative models). It is a trade-off, not a rule (Q24).
- *Does temperature matter for LLMs?* Classic distillation uses softened targets; the tutorials I saw say LLM distillation often uses temperature 1 (unverified detail).
- *Can the student beat the teacher?* Sometimes on narrow tasks with good filtering and task-specific data; on general ability, rarely.

**Common mistakes:**
- Reporting one average and calling the student "as good".
- Ignoring the tokenizer when planning logit distillation.
- Forgetting the legal check on teacher outputs.
- Choosing a student too small and blaming the method.

### Q46 ⭐ 🔴 How do you handle sequential or continual fine-tuning without forgetting (replay, per-task adapters, EWC-style regularisation, merging)?
**Asked at:** research-leaning teams, big tech, GenAI startups
**Say this first (1 line):** I avoid sequential overwriting where I can: replay a slice of old data, or keep one adapter per task and route at inference; regularisers like EWC and weight merging are the next options, each with a cost I measure on the old tasks after every stage.
**Then explain:**
- **Replay:** mix a sample of earlier data (or generated or curated stand-ins) into the new training set. Simple and usually the strongest baseline. Cost: you must keep or regenerate old data, and the privacy and licence status of it matters.
- **Per-task adapters:** train a separate LoRA per task on the frozen base. No interference by construction. Cost: you need a router (task id, a classifier or user choice), more artefacts to serve and version.
- **EWC (Elastic Weight Consolidation, Kirkpatrick et al., 2017, from memory, not verified):** add a penalty lambda/2 * sum_i F_i (theta_i - theta*_i)^2 where theta* are the weights after the old task and F_i is the diagonal Fisher information (how much the old-task loss cares about weight i, estimated from squared gradients of the old data). Important weights are held in place. Costs: a Fisher estimate per task, lambda tuning, and it trades new-task accuracy for old-task retention.
- **Model merging:** combine adapters or fine-tuned weights after the fact (Q41); cheap, needs the same base, check interference.
- **Always:** evaluate all previous tasks plus a general set after each stage (Q8), keep a rollback checkpoint, and fine-tune with a small LR and few epochs.
- **What my toy shows (synthetic, small MLP, 3 seeds, test accuracy; two binary tasks on different input regions, chance 0.5):**

| Method | Task A before B | Task A after B | Task B |
|---|---|---|---|
| sequential, no replay | 0.974 | 0.571 | 0.983 |
| replay 500 of 2,000 A | 0.974 | 0.891 | 0.944 |
| EWC lambda=10 | 0.974 | 0.573 | 0.983 |
| EWC lambda=1,000 | 0.974 | 0.636 | 0.977 |
| EWC lambda=100,000 | 0.974 | 0.789 | 0.938 |

  Forgetting was nearly complete without protection. Replay recovered most of task A at a small cost on B. EWC helped only as lambda grew very large, and still trailed replay at similar B accuracy. This is one small synthetic setup. My first attempt, where both tasks used the same inputs with conflicting labels and a smaller network, showed that neither replay nor EWC could help (no task identity, so the tasks truly conflict); I replaced it with a version where tasks occupy different regions. Results on LLMs will differ.

**Example:** a support model is fine-tuned in January on billing tickets and in March on returns. A March-only run drops billing F1. The team replays 20% billing data in the March run, evaluates both slices, and keeps a billing adapter as a fallback.

**Code:** (executed, standalone, torch only, single thread; SYNTHETIC toy, about 25 seconds)
```python
# Standalone, torch only. SYNTHETIC sequential tasks on a small MLP (not an LLM). Averages over 3 seeds.
import torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(1)
D, H = 20, 32

def task_data(w, n, g, offset):                                # task = (input region, labelling rule); regions overlap only a little
    z = torch.randn(n, D, generator=g)
    y = (z @ w > 0).long()                                     # linear rule in task-centred coordinates
    return z + offset, y

def acc(m, x, y):
    with torch.no_grad(): return (m(x).argmax(-1) == y).float().mean().item()

def run(seed, mode, lam=0.0):
    g = torch.Generator().manual_seed(seed); torch.manual_seed(seed)
    wA, wB = torch.randn(D, generator=g), torch.randn(D, generator=g)
    oA, oB = torch.zeros(D), torch.cat([torch.full((6,), 2.0), torch.zeros(D - 6)])
    xa, ya = task_data(wA, 2000, g, oA); xb, yb = task_data(wB, 2000, g, oB)
    xat, yat = task_data(wA, 2000, g, oA); xbt, ybt = task_data(wB, 2000, g, oB)
    m = nn.Sequential(nn.Linear(D, H), nn.ReLU(), nn.Linear(H, 2))
    def fit(x, y, steps=800, penalty=None, replay=None):
        opt = torch.optim.Adam(m.parameters(), lr=1e-2)
        for _ in range(steps):
            opt.zero_grad(); loss = F.cross_entropy(m(x), y)
            if replay is not None: loss = loss + F.cross_entropy(m(replay[0]), replay[1])   # replay: mix in old data
            if penalty is not None: loss = loss + penalty()
            loss.backward(); opt.step()
    fit(xa, ya); a_after_A = acc(m, xat, yat)
    if mode == "ewc":                                          # diagonal Fisher from task A (empirical, per-sample grads on 300 samples)
        star = [p.detach().clone() for p in m.parameters()]; fisher = [torch.zeros_like(p) for p in m.parameters()]
        for i in range(300):
            m.zero_grad(); F.cross_entropy(m(xa[i:i+1]), ya[i:i+1]).backward()
            for f, p in zip(fisher, m.parameters()): f += p.grad.detach() ** 2 / 300
        pen = lambda: lam / 2 * sum((f * (p - s) ** 2).sum() for f, p, s in zip(fisher, m.parameters(), star))
        fit(xb, yb, penalty=pen)
    elif mode == "replay": fit(xb, yb, replay=(xa[:500], ya[:500]))   # replay 25% of old data
    else: fit(xb, yb)
    return a_after_A, acc(m, xat, yat), acc(m, xbt, ybt)

def avg(mode, lam=0.0, seeds=range(3)):
    r = torch.tensor([run(s, mode, lam) for s in seeds]); return r.mean(0).tolist()

print(f"{'method':<22}{'A before B':>11}{'A after B':>11}{'B':>8}   (test accuracy, mean of 3 seeds; chance = 0.50)")
for name, mode, lam in [("sequential, no replay", "plain", 0), ("replay 500 of 2000 A", "replay", 0)] + [(f"EWC lambda={l}", "ewc", l) for l in (10, 1000, 100000)]:
    a0, a1, b = avg(mode, lam); print(f"{name:<22}{a0:>11.3f}{a1:>11.3f}{b:>8.3f}")

```

**Follow-ups:**
- *Why is Fisher diagonal?* Full Fisher is parameters x parameters, far too big; the diagonal is a cheap approximation that ignores weight interactions.
- *Does LoRA reduce forgetting?* It is often reported to forget less than full fine-tuning, but not zero, so measure (Q8). I am not quoting numbers.
- *Replay data is private?* Use synthetic or de-identified stand-ins, or choose adapters.

**Common mistakes:**
- Evaluating only the newest task.
- Setting EWC lambda by feel, without sweeping it on old-task data.
- Using adapters with no router plan.
- Assuming results from a toy transfer to an LLM.

### Q47 ⭐ 🔴 What is rejection-sampling fine-tuning or self-improvement (RFT, STaR-style): how do you bootstrap SFT data from a model's own verified samples, and what can go wrong?
**Asked at:** research-leaning teams, GenAI startups, big tech
**Say this first (1 line):** For each prompt I sample k answers from the model, keep only those a verifier or checker marks correct, fine-tune on the kept ones, and repeat. It works when there is a reliable checker, and it goes wrong through weak verifiers, easy-problem bias, lost diversity and compounding errors.
**Then explain:**
- **Loop:** (1) sample k answers (with reasoning) per prompt at a temperature above zero; (2) verify: exact match, unit tests for code, a calculator, a proof checker, or a reward model; (3) keep correct samples, often capped per prompt and deduplicated; (4) SFT, usually from the base or the original SFT model rather than stacking on the last round; (5) evaluate on a held-out set; (6) repeat if it still improves.
- **Named work (from memory, not verified):** STaR (Zelikman et al., 2022) bootstraps reasoning from the model's own correct rationales, and adds "rationalisation" (re-trying failed problems with the answer as a hint); rejection-sampling fine-tuning is described in work on math reasoning (for example Yuan et al., 2023, "RFT"). Check the papers for details and numbers. This is closely related to expert iteration and to the sampling step in RL pipelines (Part 5).
- **Risks:**
  - *Weak verifier, reward hacking:* the model learns whatever passes the check, not what is right.
  - *Easy-problem bias:* hard prompts rarely produce a correct sample, so they vanish from the kept data and the training mix gets easier each round.
  - *Diversity collapse:* repeated training on its own best samples narrows styles and solution paths; pass@k can fall even as pass@1 rises.
  - *Compounding errors:* a wrong-but-accepted sample is learned, and the next round samples more of it.
  - Also: right answer with wrong reasoning (Q39), contamination if prompts overlap the eval, and cost of sampling k times.
- **Mitigations:** strict verifiers (and spot checks of the verifier itself with human review), per-prompt caps, upweight or add hard prompts, keep a mix of earlier data, track diversity and a held-out set that is never used to select data, stop when held-out accuracy plateaus.
- **What my mock shows (sampler is a scripted mock, prompts are synthetic multiplications of 1 to 4 digits, 250 each, k=8):** with a strict checker, kept data was 55.8% / 35.2% / 8.4% / 0.6% from 1, 2, 3, 4-digit problems (the prompt mix is 25% each); only 71% of 3-digit and 8% of 4-digit prompts had any kept sample. With a weak checker that only compares the last digit, 46.8% of the kept samples were wrong, and the kept mix looked deceptively balanced (30.6 / 26.9 / 22.2 / 20.3%). The last lines of the code are a crude assumed update rule, not training; they just show hard-problem skill rising slowly.

**Example:** code generation with unit tests as the verifier: 16 samples per problem, keep those that pass. Problems nobody solves are dropped, so I add a curriculum or hint-based retries for them, and I check that the tests are strong enough that wrong code cannot pass.

**Code:** (executed, standalone, stdlib only; MOCK sampler and SYNTHETIC prompts, no model)
```python
# Standalone, stdlib only. MOCK sampler and SYNTHETIC prompts: no model. Shows how rejection sampling skews data.
import random
from collections import Counter
random.seed(0)
# prompt = multiply two numbers with `digits` digits each; difficulty = digits (1..4)
prompts = [(d, random.randint(10**(d-1), 10**d - 1), random.randint(10**(d-1), 10**d - 1)) for d in (1, 2, 3, 4) for _ in range(250)]
SKILL = {1: 0.95, 2: 0.6, 3: 0.15, 4: 0.01}                  # mock per-sample success probability by difficulty

def mock_sample(d, a, b):                                    # the "model": right with prob SKILL, else a plausible wrong answer
    if random.random() < SKILL[d]: return a * b
    wrong = a * b + random.choice([-1, 1, -10, 10, 100])
    if random.random() < 0.15: wrong = (a * b // 10) * 10 + (a * b) % 10 + 10 * random.choice([-1, 1])   # keeps the last digit
    return wrong

def strict_check(a, b, ans): return ans == a * b
def weak_check(a, b, ans):   return ans % 10 == (a * b) % 10     # BAD verifier: only checks the last digit

K = 8
for name, check in [("strict checker", strict_check), ("weak checker (last digit)", weak_check)]:
    kept, solved_prompts, wrong_kept = Counter(), Counter(), 0
    for d, a, b in prompts:
        got = [s for s in (mock_sample(d, a, b) for _ in range(K)) if check(a, b, s)]
        kept[d] += len(got); solved_prompts[d] += bool(got); wrong_kept += sum(s != a * b for s in got)
    tot = sum(kept.values())
    print(f"\n{name}: kept {tot} samples from {len(prompts)} prompts x {K}")
    print("  share of kept data by difficulty (digits):", {d: f"{kept[d]/tot:.1%}" for d in sorted(kept)}, "(prompt mix is 25% each)")
    print("  prompts with at least one kept sample:", {d: f"{solved_prompts[d]/250:.0%}" for d in sorted(kept)})
    print(f"  wrong answers inside the kept set: {wrong_kept} ({wrong_kept/tot:.1%})")

# crude mock of iterating: SFT on the kept data nudges skill toward the kept mix (assumed update rule, NOT real training)
skill = dict(SKILL)
for rnd in range(1, 4):
    kept = Counter()
    for d, a, b in prompts:
        kept[d] += sum(strict_check(a, b, s) for s in (mock_sample(d, a, b) for _ in range(K)))
    tot = sum(kept.values())
    for d in skill: skill[d] = min(0.99, skill[d] + 0.3 * (kept[d] / tot) * (1 - skill[d]))
    SKILL.update(skill)
    print(f"round {rnd}: mock skill by difficulty {[round(skill[d], 2) for d in (1, 2, 3, 4)]}")

```

**Follow-ups:**
- *How is this different from RLHF or RL with verifiable rewards?* It is offline, filter-then-SFT, with no gradient from the reward on failed samples; RL also learns from failures (Part 5).
- *How do you pick k?* Enough to find a correct sample on mid-difficulty prompts; measure the fraction of prompts with at least one kept sample as k grows, against compute cost.
- *Can the model exceed its starting ability?* It can sharpen what it can already sometimes do; it cannot reliably learn what it never samples correctly.

**Common mistakes:**
- Trusting a checker nobody tested.
- Ignoring the difficulty distribution of kept data.
- Training on all rounds' data without a held-out check.
- Quoting paper results from memory.

