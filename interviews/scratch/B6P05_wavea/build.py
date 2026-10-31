import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B6P05_wavea')
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
    rows += f"| B6P05-Q{i} | 5 | {t} |\n"
hdr = f"""# Book 6 — Part 5: Business Case Studies (Pricing, Churn, Fraud, Supply Chain)

**Topic:** Scenario-based "a business has this problem; use data and models to decide" questions for Data Scientist, Product Analyst and ML Engineer loops: pricing and price changes, elasticity and demand curves, discount, coupon and promotion ROI and cannibalisation, dynamic pricing and surge, subscription pricing tiers, churn prediction and retention economics (propensity versus uplift), customer lifetime value and CAC payback, fraud-detection economics (false-positive cost, review capacity, chargebacks), credit and lending approval thresholds, demand forecasting and inventory or stock-outs, delivery ETA and routing, marketplace supply-demand balance and take rate, marketing mix and attribution, recommender, search and personalisation impact, build versus buy for a model, market sizing with data, unit economics and break-even, and AI-era twists (LLM support-agent ROI, GenAI feature cost-benefit).

**Target:** 55  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part owns the business-case and decision-maths angle: unit economics, expected value, break-even, ROI and what to do given the numbers. It does not repeat Book 6 Part 1 (product metrics), Part 2 (models degrading after launch), Part 3 (imbalanced and noisy data) or Part 4 (experiment design and ambiguous A/B results); Wave B answers should cross-reference those parts and the relevant Book 1 parts only by checked headings. All numbers in the prompts are invented illustrative numbers in one unnamed currency unit, not data from any company; every percentage names its base in the prompt and says whether it is a relative or absolute change where that could be ambiguous, and every arithmetic claim in a prompt is checked in scratch/B6P05_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part05_sources.md). Searches returned pricing case-study guides (Interview Query, Dataford), churn and uplift articles, fraud-threshold and review-capacity pages, CLV and CAC guides, retail forecasting and stock-out pages, marketplace and take-rate guides, credit cut-off pages, promotion-incrementality and marketing-measurement pages, ETA and surge-pricing pages and 2026 vendor and practitioner posts on LLM support ROI and GenAI unit economics. Many results were general guidance or vendor marketing rather than interview pages, and none tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

"""
open('Book6_Scenarios/Book6_Scenarios_Part05.md', 'w', encoding='utf-8').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B6P05_wavea/index_rows.txt', 'w', encoding='utf-8').write(rows)
idx = open('question_index.md', encoding='utf-8').read()
if 'B6P05-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8').write(idx + rows)
print(n, c)
