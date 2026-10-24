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
