# Review G3 - Guide Sections 5, 6, 7 intro, Limitations
Scope file: guide_parts/Guide_S5_S6_S7intro_Limits.md. Items checked: about 75 numeric/process claims, 123 FAQ-group placements, 30 pointers. Edits: 13 targeted.

## Number audit
| Claim | Source | Result |
|---|---|---|
| Communication 73%, dashboards 75%, Excel 60%, SQL 54%, stakeholder 44%, Python 32%, Power BI 40% (n=186, +/-7) | MS Addendum table | OK |
| Stakeholder "about 60% Bengaluru and GCC" | Addendum per-sample: Hyd 64, Blr 60, GCC 60, orig 15, MIS 19 | corrected (added Hyd, n per sample, low samples) |
| MIS sample Excel 72, SQL 44, Python 16; Python 30-40% Hyd/Blr/GCC | Addendum per-sample | OK |
| ML 10%, DAX 5% | Addendum | OK |
| Deutsche Bank Entry; Syneos 3+; Unisys 4-6; Unisys OCM 0-2; People Data Analyst Rs 6-10 LPA snippet | MS Sections 4, 6 | OK |
| "SQL in nearly all of about 20 profiles" | IP Section 4: about 19 of 20 | corrected to "about 19 of 20", single-report caveat |
| Daily split 40/25/20/15, 2-3 h, soft skills 15 min | plan.md Section 7 | OK |
| 150 min -> 60/38/30/22 | arithmetic (37.5, 22.5 rounded; sum 150) | OK |
| 24 wk x 5 d x 2-3 h = 240-360; x7 = 336-504 | arithmetic | OK |
| Month table book/part ranges | plan.md Section 7 week table; Section 6 part tables | OK (overlaps stated in text) |
| Book 4 P1-4 wk 8-10, P5-12 wk 11-13, stats P3-6 wk 11-13, P7-12 wk 14-16 | plan.md Section 7 | OK |
| No certification required in any JD | MS Section 5, Addendum "Other findings" | OK |
| Rs 50,000-1.5 lakh bootcamp cost | B0S table (fueler blog, unverified) | OK, label made "vendor/blog claim" |
| "2-3 projects ... B0S anecdotal" | B0S has no project-count finding | corrected: "no reliable data", number is plan choice |
| Collected 2026-10-20/21 | MS, B0S dates | OK |
| First sample n=40 | not used in scope | n/a |

## Fixes
| Location | Problem | Fix |
|---|---|---|
| 5.4 item 1 | Overstated "no people-analytics role at 0-2"; omitted conflict and near-misses (Goldman HCM Analyst-HRIS Hyd 1-3 yrs, H22; McDonald's HR Analytics, exp not stated, MIS#19) | Narrowed to "naming Workday/SuccessFactors/Visier"; stated MS S6 vs Addendum conflict; listed near-misses |
| 5.1 table | Stakeholder figure partial | per-sample range with n |
| 5.1 SQL row | unlabelled claim | "general knowledge, not checked" |
| 5.4 item 2 | "nearly all" vague | "about 19 of 20", caveat |
| 6.1 | cited MS Section 8a (n=40 section) for n=186 figures | cite MS Addendum |
| 6.5 projects | cited B0S for something it does not contain | "no reliable data found"; plan choice; Book 12 S2 plans five |
| 6.5 bootcamp | "research offers" structure/network claim unsupported | now "general knowledge, not checked"; "no comparison" |
| 6 limitations | month vs week mismatch not noted there | sentence added |
| Limitations: sources | Glassdoor content actually reached research as search summaries; LinkedIn public pages were used | clarified |
| 7.1 groups | misplaced items: Q30 (technical question), Q64/Q65/Q73/Q74/Q99 (job search), Q72 (rejection), Q103 (people-analytics law) | moved Q30->G8; Q64,Q65,Q73,Q74,Q99->G7 (renamed "Company types, cities and job search"); Q72->G1; Q103->G2. G8 renamed. |

## Checks passed
- FAQ map: script check, each of Q1-Q123 in exactly one group, none missing or duplicated (after edits too).
- 7.2 "Say this in the interview" list (Q8, Q18, Q22, Q28-Q30, Q54, Q58-Q61, Q84, Q117): all 13 present in Book00_FAQs.md.
- Roadmap matches plan.md Section 7 (hours, split, week ranges); 6.0 states hours/milestones/apply timing are study-plan targets, not research.
- Pointers (Book 1 P11/P12, Book 2 P5,6,9,10,12, Book 3-5 P12, Book 4 P1-12, Book 6 mocks P10, Book 7 P4-7,8,9, Book 8 P8,9, Book 9 P12, Book 10 P1,2+,7,8, Book 11 P1-2,10, Book 12 S1,2,5): all exist in plan.md Section 6. Unwritten books only referenced by number.

## Still unverified / could not check
- Goldman H22 and McDonald's #19 are in the pooled samples; whether they count as "people analytics" is a judgement. Q34 and Q75 (outside my scope) may repeat the older "no role at 0-2" wording; recommend the FAQ reviewer align them.
- Table 5.3 translation wording and 6.4 apply timing are guidance, no data. "Many HR professionals use pivots" is general knowledge.
- Section 7.2 point 3 claims every FAQ has an evidence line: not audited here.
- plan.md Section 6 Book 0 table still says "100 FAQs" (guide says 123); plan not in my scope.
