import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B9P03_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 50
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
g = {k: sum(1 for q in S if q[2] == k) for k in ('LP', 'NEG', 'HR')}
assert n == N and sum(c) == N, (n, c)
assert [q[0] for q in S] == sorted([q[0] for q in S], reverse=True)
for s in (3, 2, 1):
    d = [order[q[1]] for q in S if q[0] == s]; assert d == sorted(d)
assert len({q[3] for q in S}) == N
assert (g['LP'], g['NEG'], g['HR']) == (18, 16, 16), g
assert len({q[4] for q in S}) == N or True
keys = [q[4] for q in S]; assert len(set(keys)) == N, 'asked-at key reused'
for q in S:
    assert q[3].strip() and q[4] in AS and q[1] in order, q[3][:40]
    assert '<!--' not in q[3] and '|' not in q[3] and '\n' not in q[3]
    assert q[3].strip().endswith(('?', '.'))
def stars(s): return '⭐' * s
body = ''; rows = ''
for i, (s, d, gr, t, a) in enumerate(S, 1):
    body += f"### Q{i} {stars(s)} {d} {t}\n**Asked at:** {AS[a]}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B9P03-Q{i} | 3 | {t} |\n"
hdr = f"""# Book 9 — Part 3: Leadership Principles, Negotiation Process and the HR Round

**Topic:** How to handle the values, offer and HR conversations of a data science, ML engineer or GenAI interview loop. Leadership-principle and values questions written so they work for any company (ownership, customer focus, bias for action, disagree and commit, diving deep, earning trust, raising the bar, simplifying, delivering despite obstacles, candour, long-term thinking, values under pressure); negotiation and pay-conversation process without numbers (answering an expectations question, asking for the range, redirecting a question about current pay, comparing offers by components, countering, asking for time, declining, competing offers and deadlines, non-pay terms such as scope, start date, remote arrangements, learning support, title and level, pay talks after a layoff); and the HR round (why us, why now, notice period and joining timeline, relocation, references, background verification as a process, other offers, a counter-offer from the current employer, gaps, job changes, a layoff, a performance issue, remote and hybrid work, long-term plans, startup versus large company).

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Groups:** leadership and values {g['LP']}, negotiation and pay-conversation process {g['NEG']}, HR round {g['HR']}  |  **Date:** 2026-10-31  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part is editor guidance for the leadership, offer and HR conversations in data, ML and GenAI hiring. The answers in Wave B are templates, not scripts to memorise, and each ends with a prompt to use your own real example. It gives NO pay figures and NO negotiation numbers: scripts use placeholders such as [your target range] and [their number]. It gives NO legal advice: where a topic is legal-adjacent (notice-period terms, questions about current pay, background checks, work authorisation) the advice is to ask the recruiter or HR how it is handled and to check official sources. Company claims come only through Book 7 profiles (Part 1 for Amazon, Google, Meta, Microsoft and Netflix; Part 3 for Atlassian, Visa and Mastercard) with their caveats, or through tagged sources. Leadership-principle names used in this part (for example ownership, customer obsession, bias for action, disagree and commit) come from the editor's memory of Amazon-style lists and are editor knowledge: check the company's current list, because older guides cite 14 principles and Amazon's own guide mentions 16 (Book 7 Part 1, Amazon). Behavioural stories in general belong to Book 9 Part 1, communication to Part 2, and numeric data-science trade-off scenarios to Book 6 Part 6. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch result snippet or summary only (see research_notes/Book9_Part03_sources.md). The searches returned prep blogs, career sites, HR-guide pages, forum threads and Glassdoor reviews, not employer rubrics. They agree on themes more than on wording. 'Asked at' lines name guide families; 'commonly reported in public guides' is used only where a snippet supports the theme. Thin coverage: Meta and Microsoft values questions (no snippet), offer deadlines and extension requests, negotiating scope and level, learning budgets, pay talks after a layoff, performance-plan questions, why-not-a-startup; those lines say 'editor-designed' or 'no public page found'. India-specific HR material is mostly guide-site and forum content (anecdotal). Star counts and difficulty tags are editorial.

---

## How to talk about pay without numbers in this book

Every pay and negotiation script in this book is written with placeholders, never with amounts. Where you would say a figure, the script shows a bracket such as [your target range], [their number] or [your minimum]. Three reasons. First, any number printed here would be wrong for your role, city, level and year, and would date quickly. Second, the skill the interviewer or recruiter sees is the process: how you ask, listen, compare and respond. Third, this is coaching on process and wording, not advice on what you are owed or what an employer may or may not do.

How to use the convention: before any call, fill each bracket with your own researched figure from sources you trust, and keep it in your notes, not in the script. Say it aloud only when you have chosen to. Where a question touches rules (for example how current pay, notice periods or checks are handled), the scripts say "ask the recruiter or HR how this is handled" and you should check official sources yourself; this book gives no legal advice. Be honest at every step: do not invent offers, deadlines or experience.

---

"""
open('Book9_SoftSkills/Book9_SoftSkills_Part03.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B9P03_wavea/index_rows.txt', 'w').write(rows)
print(n, c, g)
