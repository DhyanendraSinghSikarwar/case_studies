import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B6P07_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 55
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
assert n == N and sum(c) == N, (n, c)
assert c == [18, 25, 12], c
assert [q[0] for q in S] == sorted([q[0] for q in S], reverse=True)
for s in (3, 2, 1):
    d = [order[q[1]] for q in S if q[0] == s]; assert d == sorted(d)
title = lambda t: t.split('. ')[0].rstrip('.')
assert len({title(q[2]) for q in S}) == N and len({q[2] for q in S}) == N
for q in S:
    assert q[2].strip() and q[3] in AS and q[1] in order and 2 <= q[2].count('. ') + 1 <= 5, q[2][:40]
    assert '<!--' not in q[2] and '|' not in q[2] and '\n' not in q[2]
def stars(s): return '⭐' * s
body = ''; rows = ''
for i, (s, d, t, a) in enumerate(S, 1):
    body += f"### Q{i} {stars(s)} {d} {t}\n**Asked at:** {AS[a]}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B6P07-Q{i} | 7 | {t} |\n"
hdr = f"""# Book 6 — Part 7: GenAI Scenarios (Hallucinations, Cost, Latency, Evaluation)

**Topic:** Scenario-based "this GenAI system is misbehaving, too slow or too expensive; what do you do" questions for Data Scientist, ML Engineer and GenAI Engineer loops: a RAG assistant answering wrongly or citing stale or irrelevant sources, measuring and reducing hallucinations, prompt-injection and data-leakage incidents, cost blow-ups from tokens, retries, long contexts and agent loops, latency budgets (time to first token, tokens per second, streaming, caching, batching), model upgrades and regression evaluation, LLM-as-judge validity and bias, offline versus online metrics, guardrails and over-refusal, agents looping or acting wrongly, fine-tune versus prompt versus RAG, vendor API versus self-host break-even, long context versus retrieval, multilingual and Indic-language quality, PII and compliance, user-feedback loops, prompt versioning and rollout, eval-set contamination, non-determinism, semantic-cache risks and small-model routing and cascades.

**Target:** 55  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-31  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part is the scenario and judgement angle on GenAI systems in production, with numbers where a cost, a latency, a rate or an interval can be computed. GenAI internals (attention, KV cache, tokenizers, decoding, fine-tuning mechanics, guardrail frameworks) belong to Book 2, MLOps tooling to Book 4, experiment theory to Book 1 Part 10 and Book 6 Part 4, model degradation in general to Book 6 Part 2; Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers in one unnamed currency unit, not data from any company; prices per million tokens are round invented figures, not any vendor's prices. Every percentage names its base in the prompt, rates are labelled as measured samples or projections where it matters, and every arithmetic claim is checked in scratch/B6P07_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part07_sources.md). Searches returned GenAI and LLM-engineer interview guides (mostly practitioner and prep sites, some candidate-reported), RAG-debugging pages, LLM-evaluation and LLM-as-judge pages, cost, routing and semantic-cache posts, Indic tokenizer papers, PII and retention playbooks and eval-contamination material. None tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page for the exact framing. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

"""
open('Book6_Scenarios/Book6_Scenarios_Part07.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B6P07_wavea/index_rows.txt', 'w').write(rows)
print(n, c)
