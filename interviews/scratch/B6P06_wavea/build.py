import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B6P06_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 45
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
assert n == N and sum(c) == N, (n, c)
assert c == [15, 20, 10], c
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
    rows += f"| B6P06-Q{i} | 6 | {t} |\n"
hdr = f"""# Book 6 — Part 6: Stakeholder Conflicts and Trade-off Decisions

**Topic:** Scenario-based "you and a stakeholder disagree, or two good options conflict; what do you do" questions for Data Scientist, Product Analyst and ML Engineer loops: a launch date the model cannot meet, business distrust of findings, accuracy versus latency versus cost versus interpretability, speed versus rigour under a deadline, ethics, fairness and privacy pushback, pressure to inflate or cherry-pick metrics, vague or shifting requirements, disagreeing with a senior person or an executive, saying no with data, backlog prioritisation, build versus buy politics, explaining a model to executives or regulators, owning a failed model or a wrong analysis, cross-team dependencies, resourcing disagreements, engineering versus data-science tension on productionising, ML versus rules baselines, dashboard versus model requests, black-box explanation demands, and AI-era twists (an LLM for everything, hallucination-risk acceptance, vendor API versus self-hosting, reviewing AI-written analysis).

**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part keeps to trade-off decisions and stakeholder conflicts inside data-science and ML work, with numbers where a cost of delay, a threshold or an expected value can be computed. Generic behavioural scripts (conflict with a coworker, a time you failed, leadership stories) belong to Book 9 and are not repeated here; experiment theory belongs to Book 1 Part 10 and Book 6 Part 4, business case maths to Book 6 Part 5, and model degradation to Book 6 Part 2. Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers in one unnamed currency unit, not data from any company; every percentage names its base in the prompt, and every arithmetic claim in a prompt is checked in scratch/B6P06_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part06_sources.md). Searches returned Dataford, PracHub, codemia and Yardstick stakeholder-conflict and pushback prompt pages, trade-off guides, prioritisation and saying-no pages, ethics and explainability material, productionising pages and 2026 vendor and CTO posts on LLM build versus buy. Most results were user-contributed prompt pages or general guidance with few model answers; none tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

"""
open('Book6_Scenarios/Book6_Scenarios_Part06.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B6P06_wavea/index_rows.txt', 'w').write(rows)
print(n, c)
