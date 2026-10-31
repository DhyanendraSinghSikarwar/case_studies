# Book 9 Part 4 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the six answer agents). Scope: 60 soft-skill scenarios (S1-S60) in nine categories. No pay figures; no legal claims; no advice to deceive.

## Process
Six agents answered S1-10, 11-20, 21-30, 31-40, 41-50, 51-60; merged by heading with `scratch/B9_merge.py 04 S`: 60 of 60 merged, 0 skipped, 0 pending. No spend-limit stops.

## Checks (`scratch/B9_check.py s`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering S1-S60; star order and counts 20 / 26 / 14 | pass |
| All 8 required labels present and in order (Situation, Weak response, Strong response, Why it works, What the interviewer scores, Say it like this, If they push back, Common mistakes); fences balanced | pass for all 60 |
| "Say it like this" script length 25 to 260 words | pass, no outliers |
| Pay patterns (including digits near raise, hike, increase, bump, counter-offer) | 0 hits |
| Legal-word flags (illegal, unlawful, legally, by law, law requires, right to) | 0 flags |
| Cross-references to Book 9 Parts 1-3 and Book 6 Part 6 by question number | each agent verified its question numbers by grep (for example Part 1 Q5, Q6, Q7, Q10, Q13, Q17, Q26, Q27, Q33, Q35, Q38, Q39, Q48; Part 2 Q11, Q15, Q17, Q32, Q33, Q36, Q38, Q39, Q40, Q41, Q45; Book 6 Part 6 Q1, Q13, Q26, Q28, Q42, Q43) |

## Corrections made before merge
- Four internal "Editor note for Wave B" sentences that had leaked into Asked-at lines (S25, S35-area items, S39, S40) were removed from the part file and the agents' files, and the resulting punctuation was tidied (`;` and separator artefacts) by `scratch/B9P04_clean.py`.
- S19's unverified "Book 4 covers the monitoring mechanics" was replaced by "Book 4 Part 8 (monitoring) covers the mechanics" (Part 8 is titled Monitoring in plan.md); S27's vague "Book 6 covers the technical trade-offs" was replaced by "Book 6 Part 6 covers data-science trade-offs with numbers".
- S29's loose Book 6 Part 6 Q28 pointer (headline-metric choice) was kept as a loose pointer, as the agent suggested.

## Spot-checks of the highest-risk scenarios
- S25 (family-plans question in an interview): the strong response stays calm, offers three honest options (brief answer steering to the work, asking what they want to learn, a polite decline), leaves any later step to the candidate, and says whether a rule was broken is for the recruiter, HR and official sources, with no legal advice.
- Ethics and escalation scenarios (S18 data leak, S39 and S40 privacy and AI-tool policy, S46 unsafe launch): route through the proper internal channel, manager, privacy, security or compliance contact, say compliance decides whether something is a breach, and make no legal claim.
- Interview-room scenarios use scripts with placeholders only and no instruction to deceive.

## Honest limits
Evidence is snippet-only (7 searches; WebFetch unavailable); rude or late interviewers, over-long take-homes, interviewer pushback on a solution, "any questions for us?" with none left, credit taken, a data leak noticed, AI-tool policy at work and metric inflation have no supporting page and are editor-designed; the panel scenario rests on a single anecdote; the remote and global scenarios rest on general async and time-zone pages plus crowd-sourced or forum material, and the process-level EU/US manager point has a thin basis. These are coaching templates, not a promise of what any interviewer asks or scores.
