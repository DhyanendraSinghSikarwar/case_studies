import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B9P05_wavea')
sys.dont_write_bytecode = True
from qs import P
n = len(P); c = [sum(1 for q in P if q[0] == s) for s in (3, 2, 1)]
assert n == 12 and c == [6, 4, 2], (n, c)
assert [q[0] for q in P] == sorted([q[0] for q in P], reverse=True)
assert len({q[2] for q in P}) == 12 and len({q[3] for q in P}) == 12
for q in P:
    assert all(str(x).strip() for x in q) and q[1] in '🟢🟡🔴'
    for x in q[2:]:
        assert '<!--' not in x and '|' not in x and '\n' not in x
body = ''; rows = ''
for i, (s, d, sk, sc, asked) in enumerate(P, 1):
    body += f"### P{i} {'⭐'*s} {d} {sk}\n**Asked at:** {asked}\n**Scope:** {sc}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B9P05-P{i} | 5 | {sk}: {sc} |\n"
hdr = f"""# Book 9 — Part 5: Skill-Improvement Playbooks

**Topic:** Twelve step-by-step playbooks for improving the soft skills that data, ML and GenAI interview loops test: structured communication, data storytelling, stakeholder management, business acumen, influencing and negotiation (process only), presentation and public speaking, written communication, ownership and prioritisation, handling feedback, cross-cultural communication (process level), mentoring and leadership, and composure under pressure. Each playbook is written later with what good looks like, a self-assessment, daily and weekly practice, a 30-day plan, resources, how to show the skill in interviews, common traps and measures of progress.

**Target:** 12  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-31  |  **Status:** Playbooks frozen (Wave A); content pending (Wave B)

**Scope note:** this part is editor guidance. The plans are templates to adapt to your own role, schedule and starting level, not fixed prescriptions, and nothing here replaces a coach, a mentor or your manager. It gives NO pay figures, NO negotiation numbers, NO legal advice and no advice to deceive anyone; pay and offer scripts elsewhere in Book 9 use placeholders, and legal-adjacent points are routed to the recruiter or HR and official sources. Cultural guidance is process-level only, with no claims about what people of any nationality or background are like. Stars: 3 means the skill is tested in most loops, 2 regular, 1 senior or niche; the tags 🟢 🟡 🔴 show how long the skill usually takes to build (🟢 weeks, 🟡 a few months, 🔴 many months of repeated practice). Stars and tags are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch result snippet or summary only (see research_notes/Book9_Part05_sources.md). Public material is mostly coaching blogs, consulting case-interview pages, question banks and general workplace-skills pages, not employer rubrics and not studies of how skills improve. They support the themes but rarely the concrete practice plans, which are editor-designed. Thin in the search: PR-description and executive-email guidance, data-science-specific stakeholder mapping, how to measure mentoring impact, and anything specific to interview rubrics. Those 'Asked at' lines say so.

---

## How to use these playbooks

1. Self-assess: score yourself 1 to 5 on each skill using the self-assessment in its playbook, and ask one colleague or friend to score you too.
2. Pick two skills only: one that your target roles test most (look at the stars) and one you score lowest on.
3. Run the 30-day plan for each, week by week, with the daily and weekly practice. Fifteen minutes a day beats a long weekend session.
4. Measure: use the 'Measures of progress' list, keep a short log, and record yourself or collect feedback at the end of each week.
5. Repeat: after 30 days re-score, keep what works, and switch one skill. Link practice to the Book 9 question and scenario items named in each playbook.

---

"""
open('Book9_SoftSkills/Book9_SoftSkills_Part05.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B9P05_wavea/index_rows.txt', 'w').write(rows)
print(n, c)
