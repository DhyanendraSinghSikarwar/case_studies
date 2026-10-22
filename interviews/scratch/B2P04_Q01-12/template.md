@@HEAD:1@@
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

@@HEAD:2@@
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

@@HEAD:3@@
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
@@CODE:q3@@
```
Output (my run):
```
@@OUT:q3@@
```
The loss falls to about 0 because the toy fits four examples; the point is that only A and B train, and the merged matrix reproduces the adapter output.

**Follow-ups:**
- *Why is B zero and not both zero?* If both were zero the gradients to both would be zero and nothing would train; with A random and B zero, B gets a gradient immediately.
- *Is LoRA always as good as full FT?* No, it can lag on large domain shifts or hard tasks; check on your eval.
- *Does LoRA reduce activation memory?* Not much; activations still flow through the full model (Q7).

**Common mistakes:** Saying LoRA trains a "smaller copy" of the model; forgetting the alpha/r scale; saying it lowers inference latency versus the base (it only avoids adding latency when merged); quoting the paper's 10,000x as if it applied to a small model.

@@HEAD:4@@
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
@@CODE:q4@@
```
Output (my run):
```
@@OUT:q4@@
```

**Follow-ups:**
- *Higher rank always better?* No; returns diminish, and more capacity means more forgetting and overfit on small data.
- *How do you tune it?* Sweep r in {8, 16, 64} with a fixed alpha rule, compare validation task metric and the general regression set (Q9).
- *Different rank per layer?* PEFT exposes `rank_pattern` and `alpha_pattern`; rarely needed.

**Common mistakes:** Changing r while holding alpha fixed and not noticing the scale changed; treating alpha = 2r as a theorem; tuning dropout before data quality; confusing r with the number of layers adapted.

@@HEAD:5@@
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
@@CODE:q5@@
```
Output (my run):
```
@@OUT:q5@@
```
So q,v only is 8.4M trainable parameters and all-linear is 40.0M, both small next to the roughly 6.5B base linear weights.

**Follow-ups:**
- *Which layers help most?* Evidence is mixed; I'd run an ablation (q,v / attention-only / all-linear) on the eval.
- *Embeddings and lm_head?* Usually left frozen; PEFT's `modules_to_save` can train them fully if you add new tokens.

**Common mistakes:** Only adapting q,v because a tutorial did; assuming parameter count is the memory bottleneck (activations and the base model dominate); using wrong module names for the architecture.

@@HEAD:6@@
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
@@CODE:q6@@
```
Output (my run):
```
@@OUT:q6@@
```
The quantile-style book has lower error on normal data (about 17% lower MSE here), which is the intuition behind NF4. Real NF4 differs in its exact levels, so do not quote these numbers as NF4 results.

**Follow-ups:**
- *Speed?* Dequantization adds overhead, so QLoRA is typically slower per step than bf16 LoRA (vendor docs say so; I have not measured it).
- *Can I merge the adapter?* Not directly into the 4-bit base without dequantizing (Q13).
- *Does 4-bit hurt quality?* The paper reports it recovers 16-bit fine-tuning quality in its experiments; verify on your task.

**Common mistakes:** Saying the whole model trains in 4-bit; forgetting scale constants cost memory; claiming NF4 is just int4; thinking paged optimizers reduce steady-state memory.

@@HEAD:7@@
**Say this first (1 line):** Full fine-tuning needs about 16 bytes per parameter before activations, LoRA needs the frozen bf16 base (2 bytes) plus a small adapter, and QLoRA needs about half a byte per parameter for the base, so a 13B model is hopeless for full FT on 40 GB, tight for bf16 LoRA, and comfortable for QLoRA.

**Then explain (all figures are estimates under assumed accounting):**
- **Full FT (Part 2 Q34):** bf16 weights 2 B, gradients 2 B, Adam fp32 master + m + v = 12 B, so 16 B/param.
- **LoRA:** frozen bf16 base 2 B/param, plus adapters (I assume about 1% of base parameters, each at 16 B for weights, grads and Adam).
- **QLoRA:** base at 0.5 B/param plus about 3% for quantization constants (assumed), plus the same adapter state.
- **Not included:** activations (grow with batch size x sequence length; gradient checkpointing trades compute for memory), CUDA context, fragmentation. Budget a few GB to tens of GB for these.

**Code:** (run, plain arithmetic)
```python
@@CODE:q7@@
```
Output (my run):
```
@@OUT:q7@@
```
**Example (can 13B fit on 40 GB?):** With bf16 LoRA the weights alone are 26 GB and my estimate is about 28 GB with adapter state, leaving roughly 12 GB for activations and overhead. That can work with short sequences, small batch and gradient checkpointing, but it is tight and depends on all of those. QLoRA is about 9 GB for state, leaving about 31 GB, so it fits comfortably and allows longer sequences. The prep article's rough figures (about 30 GB LoRA, 10 GB QLoRA for 13B) are secondary sources but land close to this estimate; I computed mine from stated assumptions instead of quoting them.

**Follow-ups:**
- *What else grows memory?* Sequence length and batch size through activations; the optimizer if you train more modules.
- *If it does not fit?* Gradient checkpointing, smaller micro-batch with accumulation, QLoRA, or sharding (Part 2 Q34).

**Common mistakes:** Forgetting activations; using 4 B/param for everything; claiming LoRA removes the cost of the base weights (it does not, they still sit in memory); presenting these estimates as measured numbers.

@@HEAD:8@@
**Say this first (1 line):** Catastrophic forgetting is when fine-tuning on a narrow task overwrites general abilities the base model had; I detect it by tracking a held-out general set next to the task metric, and I reduce it with lower learning rate, fewer epochs, lower rank, mixing in general data, and freezing more.

**Then explain:**
- **Why it happens:** the gradients only see the new data, so any weight direction useful for the old behaviour but irrelevant to the new data is free to drift. High LR, many epochs and large capacity make it worse.
- **Detection:** keep a small general suite (e.g. MMLU or HellaSwag style multiple-choice, plus a few prompts from your own product) and evaluate it at every checkpoint along with the task metric. A task metric that rises while the general score drops is the signature. Also read samples: refusals, format leakage into unrelated prompts.
- **Mitigations:** lower LR and fewer epochs; smaller rank or fewer target modules (less capacity to drift); LoRA instead of full FT; replay, i.e. mix general or earlier-task examples into the fine-tuning data (Q27); freeze more layers; early stop on the general metric; merge-weight scaling at the end (reduce the adapter strength).
- **Honest caveat:** LoRA forgets less than full FT in several reports but not zero; do not assume it is safe.

**Code:** a SYNTHETIC demo, not a language model. One small MLP is trained on a "general" toy task, then fine-tuned on a second toy task (labelled by a different random rule, flagged by a task bit). Takes about 1-2 minutes on CPU.
```python
@@CODE:q8@@
```
Output (my run):
```
@@OUT:q8@@
```
Fine-tuning on the new task alone drops general accuracy from 0.98 to 0.27. Replaying 600 general examples restores it to 0.91 with no loss on the new task. The tiny-LR run stays at 0.96 general accuracy but also does not learn the new task (0.27), so lowering LR alone is a trade, not a fix. Numbers from this toy say nothing about real LLM magnitudes.

**Follow-ups:**
- *Would you use a bigger replay ratio?* Tune it: more replay protects general ability but dilutes the task signal.
- *Is it only about knowledge?* No: format, safety behaviour and instruction following also regress.

**Common mistakes:** Only watching the task metric; calling any drop "forgetting" without a baseline; fixing it by lowering LR so far that the task is not learned; evaluating the general set once at the end.

@@HEAD:9@@
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

@@HEAD:10@@
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
@@CODE:q10@@
```
Output (my run):
```
@@OUT:q10@@
```

**Follow-ups:**
- *Synthetic data?* Useful for coverage but copies the teacher's mistakes and style; filter and sample-check.
- *How do you know you have enough?* The data-size curve and validation plateau, not a magic number.

**Common mistakes:** Chasing volume with noisy data; duplicates that leak across train and test; unbalanced task mix; no review of a random sample by a human; quoting "1,000 examples is enough" without the LIMA caveats.

@@HEAD:11@@
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
@@CODE:q11@@
```
Output (my run):
```
@@OUT:q11@@
```
Masked loss counts 6 response tokens, the unmasked-prompt loss counts 10; they differ (4.83 vs 4.54), and my manual NLL equals `F.cross_entropy` with `ignore_index`.

**Follow-ups:**
- *Does masking change the model's input?* No, the prompt still conditions the response; only the loss differs.
- *Loss normalisation with packing?* Decide whether to average per token or per example; token-average gives long responses more weight.

**Common mistakes:** Forgetting the shift (off-by-one labels); leaving padding unmasked; masking the EOS; assuming packing is free when attention crosses example boundaries; not checking the masked labels by printing one batch.

@@HEAD:12@@
**Say this first (1 line):** The chat template turns messages into the exact token string the model sees; if training and inference use different templates, or the EOS token is missing or mismatched, the model sees a format it was never trained on and may behave badly or never stop.

**Then explain:**
- **Template:** role markers, separators and special tokens. Different model families use different ones; the instruct checkpoint's own template is the safe choice (Q36).
- **Train-test skew:** if training strings look like `<|user|>...` and inference sends `User: ...`, the prompt falls outside the learned distribution and quality drops even though loss looked fine.
- **Generation prompt:** at inference the string ends with the assistant header so the model continues as the assistant; training must contain that same prefix before the response.
- **EOS:** the response must end with the end-of-turn token, and it must be in the labels. TRL docs say to align the EOS token with the chat template or the model may not stop. Without it you get run-on output or the model inventing the next user turn.
- **Checks:** print one rendered training example and the inference prompt, confirm the prompt is a prefix of the training string, and confirm the stop token configured in the server matches.

**Code:** (run, plain Python toy template; no transformers library)
```python
@@CODE:q12@@
```
Output (my run):
```
@@OUT:q12@@
```
The last toy "model" is a hand-written stand-in, not a real LLM, to show the effect of training without a stop signal.

**Follow-ups:**
- *Double BOS?* A common bug: template adds BOS and the tokenizer adds another; check the token ids.
- *Why does a LoRA model ramble after merging?* Often a stop-token or template mismatch, not the adapter itself.

**Common mistakes:** Hand-writing prompts at inference; training on text without EOS; using a base-model template on an instruct checkpoint; changing templates between training and serving; not looking at the actual rendered string.
