import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B9P01_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 50
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
assert n == N and sum(c) == N, (n, c)
assert c == [17, 22, 11], c
assert [q[0] for q in S] == sorted([q[0] for q in S], reverse=True)
for s in (3, 2, 1):
    d = [order[q[1]] for q in S if q[0] == s]; assert d == sorted(d)
assert len({q[2] for q in S}) == N
for q in S:
    assert q[2].strip() and q[3] in AS and q[1] in order, q[2][:40]
    assert '<!--' not in q[2] and '|' not in q[2] and '\n' not in q[2]
    assert q[2].strip().endswith(('?', '.'))
def stars(s): return '⭐' * s
body = ''; rows = ''
for i, (s, d, t, a) in enumerate(S, 1):
    body += f"### Q{i} {stars(s)} {d} {t}\n**Asked at:** {AS[a]}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B9P01-Q{i} | 1 | {t} |\n"
hdr = f"""# Book 9 — Part 1: Behavioural Interviews, Levels and the STAR/CARL Framework

**Topic:** The general behavioural round for data science, ML engineer and GenAI candidates. How to structure a story (STAR and CARL), what interviewers tend to expect at junior, mid, senior and staff level, and 50 behavioural questions: tell me about yourself and why this role, a proud project, failure and mistakes, conflict, disagreement, ambiguity, prioritisation, deadlines, feedback given and received, leading without authority, mentoring, learning fast, working with engineers, product managers and non-technical partners, ethics and judgement, remote and cross-time-zone work, motivation and career goals, why leave, strengths and weaknesses, changing your mind, data that contradicts intuition, using AI tools responsibly, questions to ask the interviewer, and level-specific questions for junior, mid, senior and staff.

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-31  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part is editor guidance for the behavioural round. It is not a script to memorise: the answers in Wave B are templates with placeholders and clearly illustrative details, and every one ends with a prompt to use your own real example. It gives no pay or negotiation figures and no legal advice; where a point touches legal or pay matters, ask the recruiter or HR and check official sources. Data-science trade-off and stakeholder scenarios that carry numbers belong to Book 6 Part 6 and are not repeated here; communication craft goes to Book 9 Part 2, leadership principles, negotiation process and HR scripts to Part 3. Company evidence is cited only from the Book 7 profiles, with their tags and caveats. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch result snippet or summary only (see research_notes/Book9_Part01_sources.md). The searches returned prep-site and vendor question lists, a few Towards Data Science and KDNuggets pieces and some commercial coaching pages. They agree on themes but not on exact wording, and none is a company rubric. 'Asked at' lines therefore name guide families, and 'commonly reported in public guides' is used only where a snippet supports the theme. Search coverage was thin for cross-time-zone work, mentoring, questions to ask the interviewer, and any rubric that maps behavioural criteria to level; those items say 'no public page found, editor-designed'. Star counts and difficulty tags are editorial.

---

## STAR and CARL: how to structure a behavioural answer

This is editor guidance [G], not a company requirement. Both frameworks are ways to keep a spoken story short, concrete and about you. Public guides describe STAR as the long-standing default and CARL as a variant that adds a reflection step; no study compares them, so pick the one you can use without sounding scripted.

**What each letter means**

| Letter | STAR | CARL |
|---|---|---|
| S / C | Situation: the setting in one or two sentences (team, goal, what was at stake) | Context: the same, kept even shorter |
| T | Task: your specific responsibility, what you were asked or decided to do | (folded into Context) |
| A | Action: what you did, step by step, using "I" for your own choices and "we" only for real team work | Action: the same, and the longest part |
| R | Result: the outcome, with a number or a concrete change where honest, plus what did not work | Result: the same |
| L | (not in STAR; many candidates add a closing lesson anyway) | Learning: what you changed afterwards, or would do differently |

**A six-line template** (fill in with your own real example)

```
1. Situation: [team, goal, why it mattered], in one sentence.
2. Task: [what I was responsible for or decided to own].
3. Action 1: [the first thing I did and why I chose it over the alternative].
4. Action 2: [the hard part: the disagreement, the dead end, the judgement call].
5. Result: [what happened, with a measured number or a plain description, and what did not work].
6. Learning: [one thing I do differently now, ideally one I can show].
```

**Time for a two-minute answer**

| Part | STAR | CARL |
|---|---|---|
| Situation and Task (or Context) | about 20 to 25 seconds | about 20 seconds |
| Action | about 60 to 70 seconds | about 60 seconds |
| Result | about 25 to 30 seconds | about 25 seconds |
| Learning | optional, 10 seconds | about 15 seconds |

The rule of thumb: spend about half the time on Action. Candidates tend to over-explain background and rush the part the interviewer is scoring.

**How CARL differs.** It trims the set-up so you reach your actions sooner, and it makes the reflection explicit. It suits questions about failure, feedback and changing your mind, where the learning is what is being asked. STAR suits a story that needs more set-up to be understood, such as a long project with several stakeholders. Both need a real result, including partial or negative ones.

**Adapting for follow-ups.** Interviewers usually interrupt to dig into one part of the story, so keep a layer of detail ready behind each letter.
- Probe on Situation: add one fact about scale or constraints, then return to your action.
- Probe on Action ("what exactly did you do?" or "why that way?"): name the alternative you rejected and the reason; separate your decisions from the team's.
- Probe on Result ("how do you know?"): say how it was measured, what you would not claim, and what is still unknown.
- Probe on Learning ("what would you do differently?"): give one specific change, not a general lesson.
- If you do not know or the story is thin: say so, then offer a closely related real example. Do not invent details; follow-up depth is how invented or AI-written stories get found out.
- For technical roles, keep the technical reasoning visible inside the story (one public guide makes this point), but keep numbers and names to what you can defend.

---

## What companies expect by level

**[G] Editor synthesis, not a company rubric.** Titles, years of experience and ladders differ by company and even by team, and no public rubric mapping behavioural criteria to level was found in the search snippets (sources: research_notes/Book9_Part01_sources.md; level framing in the public guides is opinion). Use the table to check whether your stories are pitched at the right level, then check the job posting and ask the recruiter what the level means at that company. No pay information is given here.

| Dimension | Entry / junior [G] | Mid [G] | Senior [G] | Staff / principal [G] |
|---|---|---|---|---|
| Scope | A well-defined task or part of a project | A project or workstream, from question to delivery | A product area or a set of projects, including problem selection | A multi-team or organisation-wide problem, often one that nobody has defined yet |
| Ownership | Delivers assigned work reliably and asks for help at the right moment | Owns outcomes of a project with light supervision | Owns outcomes and the risks around them; decides what is worth doing | Owns direction and its consequences; decides what not to do |
| Impact | Correct, reproducible work that helps the team | Measurable impact on a metric or decision for one team | Impact on a business area, shown with evidence | Impact across teams, the way people work, or the company's direction |
| Communication | Clear updates; asks good questions | Explains work and trade-offs to partners without handholding | Shapes decisions with stakeholders, written and spoken | Aligns executives and several teams, writes the documents others build on |
| Leadership | Learns from feedback; helps peers informally | Mentors juniors informally; pushes back with evidence | Mentors openly, sets technical direction, handles conflict | Grows other leaders, influences without authority, sets standards |
| Typical story pitch | "I did X, with help from Y" | "I owned X and made these decisions" | "I decided X, aligned people and handled the fall-out" | "I changed how several teams do X and stopped Y" |

How to use it:
- If you interview for senior or staff but your stories end at "I built it", they are likely to sound one level too junior; add the decision, the people you aligned and the trade-off you accepted. This pitch warning comes from a commercial coaching page and is an opinion.
- Ownership and scope matter more than headcount: you can show senior-level behaviour without a manager title.
- Do not overstate: a story pitched above the work you really did will fall apart under follow-ups.

**Level evidence in the Book 7 profiles (cited by company and Part; each keeps its caveat there)**

| Company | What the profile holds | Caveat to keep | Where |
|---|---|---|---|
| Microsoft | Applied Scientist levels L60 to L63 appear in sources. One guide says L60 and L61 lean on data structures and algorithms and L63 and above add extra rounds such as ML system design. A Blind thread reports a posting edited from Data and Applied Scientist II to Senior during a process. A Hyderabad posting lists an advanced degree and several years of experience | Third-party guide and anecdote; level can shift during the process; verify with the recruiter | Book 7 Part 1, Microsoft profile |
| Meta | Data Scientist levels appear as IC4 and IC5 and above. One Blind anecdote reports a candidate at IC5 on design but IC4 on behavioural, and another that the final level is decided after the rounds | Anecdotal; guides disagree on years of experience | Book 7 Part 1, Meta profile |
| Amazon | One prep guide describes Applied Scientist at L5 and Senior Applied Scientist at L6, with L6 leading projects and setting direction | The same guide's L5 title mapping looks questionable; verify against job postings | Book 7 Part 1, Amazon profile |
| Google | Levels L3 and L4 are reported with a Googleyness-and-leadership round on the software engineer track. No level-specific behavioural expectations were found for senior data scientist | Software engineer track; DS and ML mix may differ | Book 7 Part 1, Google profile |

These entries show that behavioural performance can be tied to level at some companies, which is why a level-matched story matters. They are not a rubric, and nothing here says how a company scores a given story.

---

"""
open('Book9_SoftSkills/Book9_SoftSkills_Part01.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B9P01_wavea/index_rows.txt', 'w').write(rows)
print(n, c)
