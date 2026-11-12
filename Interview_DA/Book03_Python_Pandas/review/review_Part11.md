# Review: Book 3 Part 11 (Jupyter, APIs, Excel automation, AI assistants)

Environment: Python 3.13, pandas 3.0.5, openpyxl 3.1.5, requests; local mock HTTP server for API snippets.

## Counts
- Answers checked: 48 of 48 (Q1 to Q48).
- Python snippets run OK: 29 (Q6, Q7, Q8, Q13, Q14, Q15, Q17, Q18, Q19, Q20, Q21, Q23, Q24, Q25, Q26, Q28, Q29, Q30, Q31, Q32, Q34, Q38, Q39, Q40, Q41, Q42 (both), Q44, Q46). Every pasted output and every number in the prose matched the real run.
- Shell/cron/venv/nbconvert blocks (Q35, Q36, Q43) not run; already labelled "from memory, unverified" in the answers. Q4, Q9 to Q12, Q16, Q22, Q27, Q33, Q37, Q45, Q47, Q48 have no runnable code.
- Answers fixed: 8 (Q8, Q13, Q15, Q16, Q21, Q31, Q44, Q46); 9 fix rows because Q44 had two issues.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q8 | Sample data had no table (only a sentence); "denominator" unexplained; Asked at called AI verification "a recurring interview theme" citing a research paper | Added the 6-row table; explained denominator in plain words; Asked at now says the source is a 2024 Microsoft Research paper, not an interview report |
| Q13 | Sample data described test setup ("I served...") instead of the data | Reworded to what the data is and that only the URL changes with a real API |
| Q15 | "six employees" given only in words | Added 6-row sample table (output verified against it) |
| Q16 | Example prompt said "Use pandas 2.x" while the book runs pandas 3 | Changed to "Use pandas 3" |
| Q21 | Output showed lines (ok / missing / slow) that the shown code never printed; sample text mentioned test scaffolding | Added the three-call loop to the code so output matches exactly; reworded sample data |
| Q31 | Asked at said "2026 prep articles" (sources have one DataCamp article) | Named the single DataCamp 2026 article, snippet only |
| Q44 | Code used `employees` with no data and no output | Added the 5 sample rows and the real output (verified) |
| Q44 | Same "2026 prep material" over-claim | Same fix as Q31 |
| Q46 | Sample data said "Files created locally for the test"; department of each employee not stated | Replaced with the department of each person (matches output) |

## Concept checks (run on pandas 3.0.5)
- `DataFrame.append` raises AttributeError (Q31): confirmed.
- `read_excel(header=2, skipfooter=3)` on a title/blank/notes layout, merged title read as NaN, numeric dtypes kept (Q28): confirmed.
- openpyxl formula stored as text, `data_only=True` returns None before Excel recalculates (Q39); bold, width, number_format persist (Q38): confirmed.
- `sheet_name=None` returns dict (Q23); `json_normalize` column names and the `str.replace` rename (Q20); `pd.cut` bin edges are right-inclusive (Q17): confirmed.
- Timeout and 404 handling with `requests` (Q21), missing env var gives KeyError (Q40): confirmed.

## Unresolved / report only
- Ordering: stars descend 3, 2, 1 correctly; Q47 and Q48 are one-star hard questions, fine.
- Overlap: Q5/Q9/Q26 (restart and run all, kernel, out-of-order) overlap by design and cross-reference each other; Q17/Q16/Q48 overlap on privacy and prompts; Q22/Q42 overlap on 429. Q47 touches Excel vs Power Query vs VBA, possibly overlapping Book 1 Part 11 (VBA) and Book 4 Power Query parts.
- Many answers reuse file names such as `employees.xlsx` with different contents; each has its own table now, but a reader could mix them up.
- Part header says Target 40 / Actual 48; left unchanged.
- Q23, Q24, Q30, Q32 describe their sample data in a sentence or refer to Q18 instead of a table (outputs verified).

## Claims left unverified
- Jupyter shortcuts in JupyterLab and VS Code (Q10), `%matplotlib inline` default (Q34), nbconvert `--no-input` and PDF needing LaTeX (Q35), venv activation commands (Q36), cron line and Task Scheduler steps (Q43): from memory, unverified. Q34 chart was run with the Agg backend (no error) but not looked at.
- All "Asked at" lines are "commonly asked (no company-specific report found)" or snippet-only source mentions per research/Book03_Part11_sources.md; no company-specific claim exists.
