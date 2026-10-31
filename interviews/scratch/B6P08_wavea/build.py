import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B6P08_wavea')
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
    rows += f"| B6P08-Q{i} | 8 | {t} |\n"
hdr = f"""# Book 6 — Part 8: MLOps Incidents (Pipeline Failures, Rollback, Drift)

**Topic:** Scenario-based "something broke in the ML platform; what do you do" questions for ML Engineer, MLOps and Data Scientist loops: a training pipeline silently producing a worse model, bad deploys and rollback criteria, training-serving skew and feature-store incidents, late or failing data pipelines and backfills, upstream schema and unit changes, model-registry mix-ups, canary, shadow and blue/green problems, drift alerts that fire constantly or never, alert fatigue, GPU cost and autoscaling incidents, retraining loops gone wrong, on-call response, blameless postmortems, CI/CD and reproducibility failures, secrets leaks, serving outages and fallbacks, double-running batch jobs and idempotency, monitoring gaps, error budgets, blast radius and LLM-serving incidents.

**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-31  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part is the incident, on-call and judgement angle, with numbers where an error budget, a detection delay, a rollback threshold, a backlog or a cost can be computed. MLOps tooling (CI/CD, containers, versioning, serving, monitoring tools) belongs to Book 4, model degradation in general to Book 6 Part 2, data quality gates to Book 6 Part 3 and GenAI quality and cost to Book 6 Part 7; Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers, not data from any company, and costs are in one unnamed currency unit. Every percentage names its base and says relative or absolute where it matters, rates are labelled as measured samples where it matters, and every arithmetic claim is checked in scratch/B6P08_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part08_sources.md). Searches returned MLOps interview-prep pages, feature-store and skew pages, data-pipeline blogs, alerting and drift-monitor pages, LLM-resilience pages, registry and rollback runbooks and leakage papers. None tied a scenario to a verified employer round, and none located a public ML incident postmortem, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page for the exact framing. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

"""
open('Book6_Scenarios/Book6_Scenarios_Part08.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B6P08_wavea/index_rows.txt', 'w').write(rows)
print(n, c)
