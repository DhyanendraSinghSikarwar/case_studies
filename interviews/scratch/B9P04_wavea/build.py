import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B9P04_wavea')
sys.dont_write_bytecode = True
from qs import S as RAW
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(RAW, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 60
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
cats = ["Stakeholder conflict", "Ambiguity", "Failure and ownership", "Influence without authority", "Team dynamics", "Ethics and judgement", "Communication", "Interview room", "Remote and global"]
want = dict(zip(cats, (6, 6, 6, 6, 6, 6, 6, 12, 6)))
g = {k: sum(1 for q in S if q[2] == k) for k in cats}
assert n == N and sum(c) == N, (n, c)
assert c == [20, 26, 14], c
assert [q[0] for q in S] == sorted([q[0] for q in S], reverse=True)
for s in (3, 2, 1):
    d = [order[q[1]] for q in S if q[0] == s]; assert d == sorted(d)
assert g == want, g
assert len({q[3] for q in S}) == N and len({q[4] for q in S}) == N and len({q[5] for q in S}) == N
for q in S:
    assert all(str(x).strip() for x in q) and q[1] in order, q[3]
    for x in q[3:]:
        assert '<!--' not in x and '|' not in x and '\n' not in x
    ns = q[4].count('. ') + 1
    assert 2 <= ns <= 4, (q[3], ns)
def stars(s): return '⭐' * s
body = ''; rows = ''
for i, (s, d, cat, summ, sit, asked) in enumerate(S, 1):
    t = f"{cat}: {summ}"
    body += f"### S{i} {stars(s)} {d} {t}\n**Asked at:** {asked}\n**Situation:** {sit}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B9P04-S{i} | 4 | {t} |\n"
hdr = f"""# Book 9 — Part 4: Soft-Skill Scenarios (Weak versus Strong Responses)

**Topic:** Sixty short 'what do you do right now' situations from data, ML and GenAI workplaces and interview rooms, each answered later with a weak response, a strong response, why it works and what the interviewer scores. Workplace categories: stakeholder conflict, ambiguity and shifting requirements, failure and ownership, influence without authority, team dynamics, ethics and judgement (privacy, bias, metric pressure, a data leak, an unsafe launch, an AI tool used against policy), communication, and remote and global teams; plus twelve interview-room situations (blanking, a question you cannot answer, disagreeing with the interviewer, a bad connection, a late or distracted interviewer, an inappropriate question, a live-coding stumble, a long take-home, pushback on your solution, 'any questions for us?', a surprise panel, an earlier mistake).

**Target:** 60  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Categories:** stakeholder conflict {g[cats[0]]}, ambiguity {g[cats[1]]}, failure and ownership {g[cats[2]]}, influence without authority {g[cats[3]]}, team dynamics {g[cats[4]]}, ethics and judgement {g[cats[5]]}, communication {g[cats[6]]}, interview room {g[cats[7]]}, remote and global {g[cats[8]]}  |  **Date:** 2026-10-31  |  **Status:** Scenarios frozen (Wave A); answers pending (Wave B)

**Scope note:** this part is editor guidance. The strong responses written in Wave B are templates to adapt, not scripts to memorise, and the sample lines are illustrative. It gives NO pay figures, NO legal advice and no advice to deceive anyone. Where a scenario is legal-adjacent (a privacy concern, a data leak, an inappropriate interview question, an AI tool used against policy) the response is to stay calm, escalate through the proper internal channel or the recruiter, ask compliance or HR how it is handled and check official sources; this book gives no legal advice. Cultural points are process-level only (written-first versus live, meeting conventions, handover habits), with no claims about what people of any nationality or background are like. Company claims come only through Book 7 profiles with their caveats; this part names no company. Numeric data-science trade-off scenarios belong to Book 6 Part 6, and story-style behavioural questions to Book 9 Parts 1 to 3, so these scenarios are short, present-tense decisions. Each block carries a frozen **Situation:** line; Wave B keeps it and adds the remaining labels. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; stars and difficulty tags are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch result snippet or summary only (see research_notes/Book9_Part04_sources.md). Public material is mostly question banks, coaching blogs and crowd-sourced pages (codemia.io, Yardstick, Dataford, Towards Data Science, KDnuggets), not employer rubrics. They support the themes (stakeholder conflict, ambiguity, ownership, blanking, live-coding recovery, async and time-zone friction) but almost never the concrete situations, which are editor-designed. Thin or empty in the search: rude or late interviewers, over-long take-homes, interview pushback on a solution, questions to ask the interviewer (searched, nothing returned), credit taken, data leaks and AI-tool policy at work, metric inflation. Those 'Asked at' lines say 'no public page found, editor-designed'.

---

## How to use a scenario answer

Read the situation and say aloud what you would do in the first minute before you read the answer. Then compare it with the weak and strong responses and the scoring list. Adapt the 'Say it like this' lines into your own words: they are illustrations, not scripts. Add a real example of your own where the answer invites one; never invent an achievement. Practise the 'If they push back' lines, because interviewers often test the first answer.

---

"""
open('Book9_SoftSkills/Book9_SoftSkills_Part04.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B9P04_wavea/index_rows.txt', 'w').write(rows)
print(n, c, g)
