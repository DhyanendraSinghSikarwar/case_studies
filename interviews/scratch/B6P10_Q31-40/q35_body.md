**Say this first (1 line):** 3 million listings x 1,000 tokens is 3 billion tokens, 150,000 seconds or 41.67 cluster-hours, so two clusters meet the 24-hour deadline at 87% utilisation with little room for reruns.

**Clarifying questions:**
- Does the 1,000 tokens include the prompt and the listing text, or only the generated output? Generation is the slow part, so I treat all 1,000 as generated (conservative).
- What does enrichment produce (attributes, translated titles, descriptions), and is a wrong attribute worse than a missing one? It sets the quality bar.
- Is 24 hours a one-off backfill or a recurring job? One-off can use spare capacity; recurring needs a steady-state design.
- Which languages and what review capacity do I have per language? Quality varies by language.
- Can enriched content appear without review, and who owns wrong claims? Ask compliance about any claim rules; I make none.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 4, baseline 5, model and pipeline 10, evaluation 7, launch 5, monitoring and cost 5):**
1. Clarify and frame: a bulk backfill with a deadline, not a chat product.
2. Metrics and guardrails: attribute accuracy per language on an audited sample, schema-valid rate, unsupported-claim rate, cost per listing.
3. Data and labels: a gold set of listings checked by people for each language.
4. Baseline first: rules and a small extraction model for easy attributes; the LLM covers the rest.
5. Model and pipeline: prompt with a strict schema, batch inference, validators (schema, allowed values, language check), a second cheaper check, and a human queue for failures. Sizing: 3,000,000,000 tokens / 20,000 = 150,000 s = 41.67 hours; / 24 = 1.74, so 2 clusters. With 10% redone, 45.8 hours still fits two (95.5% utilisation); at 15% it is 99.8%; at 20% it needs three.
6. Evaluation: audit about 385 listings per language (worst-case margin about 5 points), compare with the gold set before the full run.
7. Launch: pilot on 1% (30,000 listings), then run in batches with a kill switch; publish through an A/B on a category before all.
8. Monitoring and cost: validator failure rate per batch, drift by language, tokens spent per listing, rerun share; keep a checkpoint so a failed batch restarts without redoing the rest.

**Metrics:**
- Attribute accuracy = correct attributes / audited attributes, per language.
- Schema-valid rate = outputs passing the validator / outputs.
- Throughput = tokens per second achieved / 20,000; redo share = listings re-run / listings.

**Risks:**
- Throughput quoted for the cluster may fall with long prompts or small languages with more tokens per word.
- Hallucinated attributes enter the catalogue; a wrong size or material has a real cost.
- No spare capacity at 87%; a failure loses the deadline.
- Token counts differ by language, so 1,000 average hides a heavy tail.

**What the interviewer scores:**
- Strong: gets 3 billion tokens, 41.67 hours, 2 clusters, and talks about headroom and redo rate.
- Strong: validators, human queue and per-language audits, not one overall accuracy.
- Weak: ignores deadline arithmetic; sends everything to the LLM with no checks.

**Example:** Illustrative numbers. 3,000,000 x 1,000 = 3 x 10^9; / 20,000 = 150,000 s = 41.67 h; / 24 h = 1.74 clusters, so 2.
- Weak: "We will run the LLM on all listings and fix errors later."
- Strong: "Three billion tokens at 20,000 a second is 41.7 cluster-hours, so two clusters for 24 hours, 87% busy. If 15% of listings are redone I am at 99.8%, so I want either a third cluster for a few hours or a validator that keeps redo below 10%."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if the prompt tokens are separate from the 1,000?* Then input is processed faster than output; measure both rates (editor knowledge).
- *How do you cut cost?* Use a smaller model for easy attributes and cache repeated listing templates; compare quality first.

**Common mistakes:** Forgetting to round up clusters. No redo allowance. One accuracy figure for all languages. No staged rollout.
