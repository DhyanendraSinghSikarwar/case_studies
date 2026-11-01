import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B6P01_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 55
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
assert n == N and sum(c) == N, (n, c)
assert [q[0] for q in S] == sorted([q[0] for q in S], reverse=True)
for s in (3, 2, 1):
    d = [order[q[1]] for q in S if q[0] == s]; assert d == sorted(d)
title = lambda t: t.split('. ')[0].rstrip('.')
assert len({title(q[2]) for q in S}) == N and len({q[2] for q in S}) == N
for q in S:
    assert q[2].strip() and q[3] in AS and q[1] in order and 2 <= q[2].count('. ') + 1 <= 6, q[2][:40]
    assert '<!--' not in q[2] and '|' not in q[2] and '\n' not in q[2]
def stars(s): return '⭐' * s
body = ''; rows = ''
for i, (s, d, t, a) in enumerate(S, 1):
    body += f"### Q{i} {stars(s)} {d} {t}\n**Asked at:** {AS[a]}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B6P01-Q{i} | 1 | {t} |\n"
hdr = f"""# Book 6 — Part 1: Product Metrics and Metric Drops

**Topic:** Scenario-based product-metrics questions for Data Scientist, Product Analyst and ML Engineer loops at Indian product companies, GCCs and global tech: DAU, WAU and MAU drops, conversion, retention and revenue drops, one metric up while another is down, Simpson's paradox and mix shift, metric definition and instrumentation changes, seasonality and holidays, new versus existing users, platform, version and geography breakdowns, notification, ranking and pricing changes, success metrics for a new feature, north-star and guardrail metrics, funnel and cohort diagnosis, decomposition trees, SQL-flavoured follow-ups at concept level, and AI-era twists (metrics for a GenAI feature).

**Target:** 55  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part owns diagnosing and defining metrics in product settings. It does not repeat the experiment theory in Book 1 Part 10 (choosing primary and guardrail metrics for a test, the Simpson's paradox definition inside an A/B test, reading a test where the primary metric and a guardrail disagree); the questions here are the same ideas met as live business situations (a dashboard drop, a rollup, a launch review), so Wave B answers should cross-reference those Book 1 questions only by checked headings. Book 6 Part 4 owns ambiguous experiment situations; Book 3 owns the full SQL; Book 2 owns GenAI internals (here only the metrics of a GenAI feature). All numbers in the prompts are invented illustrative numbers, not data from any company. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part01_sources.md). Searches returned metric-drop and root-cause question banks (Interview Query, Prachub, Codemia), product-sense and north-star pages (Dataford, datainterview.com), Simpson's-paradox prompts, metric trade-off guides, a checkout-conversion case page, Indian analyst interview guides (Interview Query, AmbitionBox, Dataford) and GenAI-chatbot metric posts. No result tied a single scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked as editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

"""
os.makedirs('Book6_Scenarios', exist_ok=True)
open('Book6_Scenarios/Book6_Scenarios_Part01.md', 'w', encoding='utf-8').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B6P01_wavea/index_rows.txt', 'w', encoding='utf-8').write(rows)
idx = open('question_index.md', encoding='utf-8').read()
if 'B6P01-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8').write(idx + rows)
print(n, c)
