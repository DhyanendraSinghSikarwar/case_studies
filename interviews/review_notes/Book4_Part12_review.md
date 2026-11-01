# Book 4 Part 12 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45 (cost, scaling, security, reliability, organisation and six timed MLOps system-design sets: F fraud, R recommender, D demand forecasting, C regulated credit risk, L LLM-serving boundary, E edge and on-device). Band per plan.md: Rs 30-80 LPA; no salary figures; no prices.

## Process
Four agents answered Q1-11, Q12-22, Q23-33, Q34-45; all four were stopped once by a spend limit and resumed with SendMessage after the reset; the agents found no saved work from before the stop, so they rebuilt their questions from scratch. Merged by heading: 45 of 45 merged, 0 skipped, 0 pending.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45; star order and counts 13 / 19 / 13 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 45 |
| Every "Part N Qn" reference (Parts 1-11) resolves to an existing `### Qn` heading | pass, 0 unresolved |

The Q23-33 agent re-ran its 11 scripts from a fresh copy and every output matched; the other agents ran each script with `python3 -I` and pasted the real output (code in each agent's `code/`, outputs in `out/`). The lead did not re-run them. Several agents re-read the cross-referenced headings and reworded text that had mischaracterised Part 6 Q38/Q39, Part 9 Q32, Part 3 Q36, Part 7 Q32, Part 4 Q25 and Part 11 Q31.

## What really ran
Python in abstract units with invented inputs (no prices): capacity and cost arithmetic, queue, autoscaling, spot Monte Carlo (26.12 h closed form vs 26.04 simulated), failover and outage simulations, forecasting policies, staged rollout, tiering break-even, extraction demo on a 20-feature logistic model; YAML policies with pydantic validators (data flows, deployment policy, RACI, ownership); the simplified IAM evaluator sketch (copied, unmodified); secret and pickle-opcode scanners (nothing is unpickled), pinned-hash and mutable-action checks; hash-chained decision logs with tamper tests; Ed25519 signing of a model file with an in-memory demo key; small ONNX export with int8 dynamic quantisation, accuracy gate and HMAC manifest; popularity feedback-loop simulation with an unpersonalised holdout.

## Findings and prompt inconsistencies kept in the answers
- Set F: 20M transactions a day at a 6x peak is about 1,389 TPS, not the 700 TPS assumed in the later set question (Q5); both are kept and the answer says to state which input changed. The prompt's "split across zones" needs 3 replicas per zone (6 total) to survive a zone loss (2 per zone would run at 105 percent); the exponential-service p99 estimate is about 64 ms against the 60 ms budget, so a real load test is advised.
- Q8: apparent recall at day 7 can be understated or overstated depending on how it is computed; both directions are shown. Q9: the prompt's 31 percent matches utilisation of held GPU-hours, not total capacity (21 percent). Q22: the invented table has a 10 percent override rate, not the 12 percent in the prompt.
- Retries alone send 3.0 attempts per request in an outage; a breaker plus fallback cuts provider attempts to about 80. A flapping no-cooldown autoscaler looks cheap but boots 101 times and has the most slow requests. A crashy edge model is halted after 374 devices while a silent accuracy drop reaches all devices without a confidence-proxy gate.
- A linear model is the easy case for extraction: full probabilities leak the weights even at 25 queries.
- Timings are sandbox-only and noisy (fp32 5.8 ms in one run, 20.7 ms in another).

## Not executed
Any cloud, credentials, prices, real regulation text, real incident tooling, real device fleets, signing infrastructure beyond the demo key. The failover model and packet-loss model are hand-made simplifications with invented timings.

## Hedged
RBI and DPDP points (no primary text read; adviser-summary level, not legal advice), the Sculley et al. technical-debt paper (not opened), FinOps and unit-economics framing, regulated-domain explainability and audit expectations.

## Evidence limits
No candidate-reported questions found; every WebFetch failed, so sources are snippets (8 searches). Gaps: GPU-specific FinOps, classic model-extraction sources, RBI/DPDP primary text. The six sets are expert designs, not company-reported. See research_notes/Book4_Part12_sources.md.
