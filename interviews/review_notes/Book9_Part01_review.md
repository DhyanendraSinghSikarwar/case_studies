# Book 9 Part 1 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five answer agents). Scope: 50 behavioural questions (Q1-Q50) with the STAR/CARL section and the "What companies expect by level" section. No pay figures or negotiation numbers; no legal claims.

## Process
Five agents answered Q1-10, 11-20, 21-30, 31-40, 41-50; merged by heading with `scratch/B9_merge.py 01 Q`: 50 of 50 merged, 0 skipped, 0 pending. No spend-limit stops.

## Checks (`scratch/B9_check.py q`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering Q1-Q50; star order and counts 17 / 22 / 11 (checked on the part file) | pass |
| All 8 required labels present and in order; optional Script block positioned between Make it yours and Follow-ups; fences balanced | pass for all 50 |
| Strong sample answer length 50 to 260 words | pass, no outliers |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and codes with digits, digits near raise/hike/increase/bump/counter-offer) | 0 hits |
| Legal-word flags (illegal, unlawful, legally, by law, law requires, right to) | 0 flags |
| Checker defect found and fixed during Wave B: the checker expected the label "Say this first" while the plan uses "Say this first (1 line)"; the checker was corrected and all agents' files pass | fixed |

## Corrections and notes
- Q19 and Q20: the Asked-at lines (copied from a Q18-specific source line) were replaced with an honest line ("no public page found for this exact wording, editor-designed; HR-style career and motivation questions of this kind appear on aggregator lists"), applied identically to the part file and the agent's answers file before merge.
- Q18 to Q20 are not STAR stories (they ask for reasons, plans and preferences); the answers use a short three-beat structure and say so.
- Q16 and Q17 carry a red difficulty tag although they are not harder than neighbouring yellow stories; left unchanged because re-tagging would break the easy-to-hard order inside the three-star group (a tag-level cosmetic issue, not a content issue).
- Spot-checks (Q18, Q37 and the scripts): sample answers are marked illustrative with a "Make it yours" step that tells the candidate to use their own real example; pay and notice questions are routed to the recruiter or HR with a "no legal advice" note and placeholders instead of figures.
- Overlap guard with Book 6 Part 6: Q9, Q10, Q12, Q28 and Q43 are written as general story versions and point to Book 6 Part 6 (Stakeholder Conflicts and Trade-off Decisions) for the numeric scenarios.
- Company mentions come only from Book 7 Part 1 (cited with their caveats); the level table is labelled an editor synthesis [G], with Microsoft, Meta, Amazon and Google level evidence cited from Book 7 Part 1 with its caveats (the Amazon title mapping is marked questionable there).

## Honest limits
Evidence is snippet-only (7 searches; WebFetch unavailable); mentoring, cross-time-zone work, questions to ask the interviewer and level rubrics had little public coverage and are marked editor-designed; staff-level content came from one promotional page; CARL has blog sources only and no study compares STAR and CARL. These are coaching templates, not a promise of what any interviewer asks or scores.
