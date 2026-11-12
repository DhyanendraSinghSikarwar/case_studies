# Review: Book 3 Part 12 (How to Develop Python Skills)

Reviewed on Python 3.13, pandas 3.0.5. Scratch: C03_Part12 (run.py extracts and runs every snippet, compares to pasted Output).

## Counts
- Answers checked: 29 (Q1 to Q29).
- Python snippets run: 11 (Q4, Q6, Q10, Q12, Q13, Q16, Q17, Q19, Q20, Q26, Q29); 11 OK, output identical to the pasted Output and to the numbers in the prose. Q11 holds shell commands, not Python (not run).
- Answers fixed: 6 (Q4, Q11, Q12, Q14, Q18, Q20).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q14 | "Python in about 32% of sampled JDs" does not match research/market_skills_2026.md (Python 14 of 40 = 35%, 0-2 year band) | Changed to "14 of 40 (35%)", common but not universal |
| Q18 | "Asked at" named Accenture and Amazon BA for Python; interview_processes.md supports Python mentions only for Infosys, Tiger Analytics, HSBC, JPMorgan (Hyderabad) | Rewrote to those four, stated as basic level and anecdote-based |
| Q20 | `validate="one_to_many"` hint was vague ("from memory") and suggested the wrong setting for the check | Ran it on pandas 3.0.5: `validate="one_to_one"` raises MergeError on repeated keys; text now says so |
| Q11 | First-person scaffolding sentence ("I confirmed ... on a machine here") in answer text | Replaced with "from memory, unverified; check python.org and jupyter.org" |
| Q12 | "Excel slows down near about a million rows" imprecise | Now: Excel limit is 1,048,576 rows per sheet and slows earlier |
| Q4 | "attrition" used without explanation at first use in the spoken answer | Added "the share of staff who leave" |

## Concept claims verified by execution (pandas 3.0.5)
- `df.append` gives AttributeError; `fillna(method="ffill")` gives TypeError; `fillna(0, inplace=True)` on a column leaves the DataFrame unchanged and raises ChainedAssignmentError (Q29 text says "warns"; in 3.0.5 it is a warning class named ChainedAssignmentError, wording acceptable).
- `info()` shows `pandas.DataFrame` and `str` dtype (Q10); `rank` ties default to average (Q16).

## Unresolved / report-only
- Template: non-code answers have no "What it means" line (Explain simply covers it); code answers all have Sample data, Code, Output, What it means. Q11 shows shell commands with no Output block, acceptable.
- Q1 (projects weeks 9-16) and Q8 (projects weeks 12-14, practice 15-16) timelines differ slightly; both are labelled templates.
- Several answers use compact "1) ... 2) ..." follow-ups on one line (Q16 to Q29) while Q1 to Q15 use bullets; style inconsistency only.
- Overlap: Q14 and Q27 both define a "job-ready" checklist; Q15 touches Part 11 (AI use) as already noted in sources; Q12/Q13 overlap Excel-to-pandas mapping with other Book 3 parts (not checked in depth).
- Count: header says Target 20, Actual 29; unchanged.

## Claims left unverified
- All resource, dataset and platform facts (Kaggle Learn, CS50P, StrataScratch free tier, PCEP, IBM HR dataset size about 1,470 rows, seaborn `load_dataset` needing internet) remain labelled "from memory, unverified" in the text; no internet to check.
- "Asked at" lines: all "commonly asked (no company-specific report found)" except Q4 (Tiger Analytics snippet, flagged unverified), Q15 (DataCamp webinar snippet, flagged), Q14 and Q18 (internal research, corrected above).
- The sources file says no page was fetched in full; nothing here upgrades that.
