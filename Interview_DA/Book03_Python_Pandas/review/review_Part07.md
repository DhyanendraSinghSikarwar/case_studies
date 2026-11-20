# Review: Book 3 Part 7 (Dates & Time Series in pandas)

Reviewed 2026-11-12 on Python 3.13, pandas 3.0.5, numpy 2.5.3. Part file: `Book03_Python_Pandas/Book03_Part07.md`.

## Counts
- Answers checked: 46 of 46
- Python snippets run: 47 blocks (46 main answers plus the Q19 alternative); 47 OK. Q2 needs its `emp.csv`, rebuilt from its Sample data row list, and then ran OK. The Q19 alternative is a one-line add-on that uses the `employees` frame from the main block, and it ran OK there.
- Printed output vs pasted Output: 45 of 46 identical line for line; 1 differed (Q45, below).
- Answers fixed: 5 (4 content fixes plus 1 template fix)
- Extra claim checks run: about 40 (see "Claims verified by running")

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q1 | The explanation used "object/str" with no explanation, so a non-technical reader had no way to follow it | Added one plain sentence: `object` or `str` is the label pandas shows for text, and a column's type is its dtype |
| Q7 | Follow-up said `errors="ignore"` "was removed in pandas 3 (from memory, unverified)" | Ran it: on 3.0.5 it raises an error. Rewrote as "no longer works in pandas 3 (raised an error when I ran it)" |
| Q14 | Template: no Sample data line | Added "Sample data: none needed; the code creates the dates itself." |
| Q45 | Pasted Output for `value_counts` omitted the `Freq: M,` part of the footer. Real output is `Freq: M, Name: count, dtype: int64` | Corrected the Output block |
| Q46 | Default `closed`/`label` claim covered `QE` and `YE`, which I could not tell apart by running | Kept the claim, labelled `ME` and weekly as checked and `QE`/`YE` as "from the pandas docs, not run here" |

## Claims verified by running (pandas 3.0.5)
- `resample("M")` raises "no longer supported, use ME" (Q6, Q9, Q14)
- `dayfirst=True` on ISO text "2026-04-03" reads it as 4 March (Q21 mistake)
- Month-first `format` makes 25/12/2025 NaT with coerce and an error without it (Q21)
- `astype(str)` before an integer `%Y%m%d` parse works (Q22)
- `pct_change` gives inf on a zero base; `pct_change(12)` works (Q10, Q24, Q39)
- `Q-MAR` labels 2026-01-15 as 2026Q4; `Y-MAR` labels by end year (Q27)
- `asfreq("D", fill_value=0)` and `asfreq(method="ffill")` work; `reindex` fails on duplicate dates (Q28, Q33)
- `.dt` on text raises the quoted AttributeError (Q31)
- `interpolate()` leaves leading NaN (Q34); `DateOffset(months=1)` on 31 Jan gives 28 Feb; `Timedelta(months=1)` raises (Q35)
- `BMonthEnd(0)` on Sunday 31 May 2026 rolls to 30 June; `MonthEnd(1)` also moves to the next month-end (Q36)
- `np.busday_count` on a plain datetime column raises TypeError (Q37)
- `tz_convert` on naive times raises; `tz_localize(None)` removes the zone (Q40)
- Missing `unit` gives 1970 dates; ms read as seconds gives year 57971; the epoch inverse formula works (Q41)
- `Grouper` with another key drops months that have no rows at all (Q42)
- `end_time` exists on Period (Q45); `date_range` with start, end, periods and freq together raises (Q14)
- `ME` and `W` default to closed right; `MS`, `D`, `h` to closed left (Q46)

## Other checks
- "Asked at": every line is either "commonly asked (no company-specific report found)" or cites a source listed in `research/Book03_Part07_sources.md` as snippet only (Educative, AskPython, Udemy, Coursera, Naukri Code360, Telegram). No invented companies or statistics.
- Template: every answer has all required sections after the Q14 fix.
- Code is already interview-style (descriptive names, comments, no debug scaffolding). Q29 hard-codes "today" as 9 Nov 2026 for a repeatable output, with a comment on the real call; left as is.
- Style: no em dashes in answer text (the only one is in the file title line, left untouched); 186 code fences, balanced; no tables in the file.
- Q5 and Q29 outputs depend on the run date; they reproduce when run on 12 Nov 2026 (Q5) or with the fixed date (Q29).

## Unresolved / report only
- Numbering and ordering: stars and order look consistent (3-star, then 2-star, then 1-star). No change made.
- Format inconsistency: Q33 to Q46 write "Likely follow-ups" as a numbered list with plain text; Q1 to Q32 use bullets with italic questions. Left unchanged (cosmetic).
- Overlap: Q8 and Q42 (resample vs groupby/Grouper), Q9 and Q19 (monthly counts via resample), Q10 and Q24 (pct_change) and Q23 vs Q38 (shift) overlap within the part by design. The sources file already lists B2P6Q38 and B5P11Q15 as adjacent in other parts; not re-checked against other books.
- Header says target 40, actual 46; matches the 46 headings.

## Claims left unverified
- Defaults for `QE` and `YE` resample (closed/label right): from the pandas docs from memory, not distinguishable by my test data (Q46).
- Source-file claims that these topics appear in the named lists rest on search snippets only (no pages were opened by the source gatherer).
- `train_test_split(..., shuffle=False)` (Q44) was not run (scikit-learn not used).
- Old-pandas behaviour mentioned in passing (`object` dtype, `datetime64[ns]`, "M" frequency) is from memory, not run on pandas 2.x.
