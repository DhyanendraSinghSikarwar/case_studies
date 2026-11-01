import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B6P02_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 50
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
assert n == N and sum(c) == N, (n, c)
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
    rows += f"| B6P02-Q{i} | 2 | {t} |\n"
hdr = f"""# Book 6 — Part 2: Model Performance Degraded in Production

**Topic:** Scenario-based "what do you do when..." questions for Data Scientist and ML Engineer loops on a model that gets worse after launch: accuracy, precision, recall or AUC falling, silent data, concept, label and prior drift, label delay and monitoring without labels, training-serving skew, feature-pipeline bugs and null or unit changes, upstream schema changes, feedback loops, seasonality, a model good offline but bad online, threshold and calibration decay, segment-level degradation, retrain versus rollback versus patch, shadow, canary and A/B validation of a fix, adversarial and fraud adaptation, recommender and ranking degradation, forecasting drift, and AI-era twists (LLM and RAG quality degradation, LLM-as-judge drift, agent tool changes).

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part owns the judgement angle (what do you do, in what order, with what evidence). It does not repeat the concept coverage in Book 1 (for example Part 1 on a model good offline but poor in production, Part 11 on training-serving skew, monitoring and retraining, Part 5 on drift and feedback loops in fraud, Part 6 on forecast monitoring) or the tooling in Book 4 Part 8 (drift tests, monitoring layers, late labels); Wave B answers should cross-reference those only by checked headings. Book 6 Part 1 owns product-metric drops (a business dashboard number fell); here the object is the model. Book 2 owns LLM internals, and here only the production-quality angle appears. All numbers in the prompts are invented illustrative numbers, not data from any company. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part02_sources.md). Searches returned production-degradation question banks (Dataford, Prepfully, TryExponent), MLOps and system-design guides on drift, skew and monitoring without labels, practitioner posts on fraud, calibration, schema changes, RAG degradation and shadow or canary rollout, and recommender feedback-loop papers. Forecasting-drift and adversarial-fraud searches found practitioner pages, not interview pages. No result tied a scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

"""
os.makedirs('Book6_Scenarios', exist_ok=True)
open('Book6_Scenarios/Book6_Scenarios_Part02.md', 'w', encoding='utf-8').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B6P02_wavea/index_rows.txt', 'w', encoding='utf-8').write(rows)
idx = open('question_index.md', encoding='utf-8').read()
if 'B6P02-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8').write(idx + rows)
print(n, c)
