import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B6P09_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 50
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
assert n == N and sum(c) == N, (n, c)
assert c == [16, 23, 11], c
assert [q[0] for q in S] == sorted([q[0] for q in S], reverse=True)
for s in (3, 2, 1):
    d = [order[q[1]] for q in S if q[0] == s]; assert d == sorted(d)
title = lambda t: t.split('. ')[0].rstrip('.')
assert len({title(q[2]) for q in S}) == N and len({q[2] for q in S}) == N
PFX = {'Fintech:': 'Fintech', 'E-commerce:': 'E-commerce', 'Healthcare:': 'Healthcare', 'Ads:': 'Ads'}
dom = {k: 0 for k in PFX.values()}
for q in S:
    assert q[2].strip() and q[3] in AS and q[1] in order, q[2][:40]
    ns = len(re.split(r'(?<=[.?])\s+', q[2].strip())); assert 2 <= ns <= 5, (ns, q[2][:40])
    assert '<!--' not in q[2] and '|' not in q[2] and '\n' not in q[2]
    p = [k for k in PFX if q[2].startswith(k)]; assert len(p) == 1, q[2][:30]
    dom[PFX[p[0]]] += 1
assert dom == {'Fintech': 13, 'E-commerce': 13, 'Healthcare': 12, 'Ads': 12}, dom
def stars(s): return '⭐' * s
body = ''; rows = ''
for i, (s, d, t, a) in enumerate(S, 1):
    body += f"### Q{i} {stars(s)} {d} {t}\n**Asked at:** {AS[a]}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B6P09-Q{i} | 9 | {t} |\n"
hdr = f"""# Book 6 — Part 9: Domain Sets (Fintech, E-commerce, Healthcare, Ads)

**Topic:** Domain-specific scenarios that only make sense inside one industry, for Data Scientist and ML Engineer loops. Fintech: credit scoring and thin-file applicants, reject inference, cutoff and profit trade-offs, payments fraud and step-up friction, KYC and AML alert triage, collections prioritisation, chargeback label noise, explainability for lenders, PD calibration and model-risk governance in general terms. E-commerce: search position bias, zero-result queries, cold-start sellers, censored demand and pricing cannibalisation, delivery promise, cart abandonment, fake reviews, size recommendation and returns, catalogue quality, seller trust and recommendation diversity. Healthcare: prevalence shift and positive predictive value, alarm fatigue and thresholds, clinician override and trust, label agreement, scanner and site bias, multi-hospital validation, consent and re-identification, LLM documentation audits, treatment-contaminated labels and change control. Ads: CTR calibration and bids, budget pacing, invalid traffic, signal loss and noisy reporting, frequency capping, cold-start campaigns, lookalike incrementality, delayed conversions, first-price bidding, geo lift versus last-click and creative selection.

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]}; Fintech {dom['Fintech']}, E-commerce {dom['E-commerce']}, Healthcare {dom['Healthcare']}, Ads {dom['Ads']})  |  **Date:** 2026-10-31  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part is the domain angle: each scenario combines metrics, modelling, risk and (where relevant) compliance in the setting of one industry, with numbers that can be reproduced in code (base rates, positive predictive value, cost matrices, calibration, incrementality). General metric drops, degradation, imbalance, experiments, business cases, stakeholder trade-offs, GenAI and MLOps incidents belong to Book 6 Parts 1 to 8; Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers, not data from any company, and money is in one unnamed currency unit. Every percentage names its base and says relative or absolute where it matters, rates are labelled as measured samples or projections, and every arithmetic claim is checked in scratch/B6P09_wavea/qs.py. Anything touching law, regulation or clinical rules is framed as a question for compliance, the privacy officer or the regulatory team, and no legal or regulatory claim is made as fact. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part09_sources.md). Searches returned fintech and credit-scoring prep guides and reject-inference pages, UPI-fraud papers, e-commerce company question lists, fake-review items, clinical-AI validation coverage and ad-tech question pages. None tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page for the exact framing. Search coverage was thin for KYC and AML, collections, delivery promise, demand forecasting, size recommendation, device bias, invalid traffic and signal loss. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

"""
open('Book6_Scenarios/Book6_Scenarios_Part09.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B6P09_wavea/index_rows.txt', 'w').write(rows)
print(n, c, dom)
