# Review: Book 3 Part 6 (data cleaning), Wave C

Reviewer: Wave C agent, pandas 3.0.5 / numpy 2.5.3 / Python 3.13. Scratch: `.../scratchpad/C03_Part06`.

## Counts
- Answers checked: 63 of 63 (Q1 to Q63).
- Snippets run: 63 of 63 ran without error. 60 matched the pasted Output exactly; Q34, Q40, Q55 differed only in column spacing (fixed, now exact); Q54's Output is hand-labelled (stdout matches, a ChainedAssignmentError warning goes to stderr, as stated).
- Answers edited: 12 (Q26, Q27, Q34, Q36, Q40, Q55, Q56, Q62, plus the sample-data line cleanup in Q17 to Q32).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q34 | Pasted Output had misaligned columns (header width); not what pandas prints | Replaced with real output |
| Q40 | Output column misaligned for the True rows | Replaced with real output |
| Q55 | Output row 3 misaligned; timings (0.12 s / 0.16 s) did not reproduce | Real output; re-timed to 0.15 s / 0.19 s and added "timings vary by machine" |
| Q34 | "see grade-wise logic" was a vague cross-reference | Now "(see Q56)" |
| Q56 | Prose said a global rule "would have kept 90,000" only; checked: a global IQR flags neither 90,000 nor 150,000 | Prose corrected |
| Q26 | `thresh=` was given a float (2.0) | `int(len(employees) * 0.5)`; output unchanged |
| Q27 | "`errors='ignore'` removed" was marked from memory | Verified on 3.0.5: `to_numeric(errors="ignore")` raises ValueError; text updated |
| Q36 | Follow-up about missing ages was vague | Explains NaN compares as False so it slips past the filter |
| Q62 | Last "common mistake" was confusing | Reworded (NaN > 0 is False, so that check fails too) |
| Q17 to Q32 (16 answers) | Filler "(the data is created inside the code block below)" after Sample data | Removed |

## Claims verified by running (pandas 3.0.5)
Q14/Q37/Q54 chained assignment: silent for subset assignment, ChainedAssignmentError warning for `df[mask]["col"] = x`, original unchanged. Q18 `fillna(method=)` removed (TypeError). Q30 `how` with `thresh` raises TypeError. Q38 memory 10.6 MB to 0.2 MB. Q39 `df["col"].fillna(inplace=True)` warns and leaves the frame unchanged; `inplace=True` returns None; `df.drop(columns=..., inplace=True)` no warning. Q32 regex shortcut gives 0.45; "45,000.50" gives 45000.5; "1,25,000" gives 125000. Q51 difflib result. Q52 `include="object"` still selects str columns with a warning. Q55 apply raises AttributeError on NaN. Q58 `format="mixed", dayfirst=True` turns 2025/11/05 into 2025-05-11. Q59 29.5 cannot become Int64 (TypeError); lowercase `int64` fails (IntCastingNaNError). Q62 AssertionError message and ValueError for an un-`.all()`ed assert. Q50 leading NaN stays NaN.

## Claims and "Asked at"
- All "Asked at" lines are either "commonly asked (no company-specific report found)" or match `research/Book03_Part06_sources.md` (Tiger Analytics mean imputation snippet in Q8; Glassdoor IQR function in Q11/Q63; Flexiple lists in Q24/Q29; training-blog snippets in Q12). No invented companies or statistics found.
- Template: all 63 answers contain every required field (Asked at, interviewer checking, Say this, Explain simply, What it means, Likely follow-ups, Common mistakes, Sample data, Code, Output).
- Style: no em dashes in answer text (one in the file title line, left as is); code fences balanced; no tables in the part.

## Unresolved / report only
- Format drift: Q17 to Q32 use numbered follow-ups and "```text" fences; the rest use bullets and plain fences. Harmless; left unchanged.
- Q60 includes a `change_log` list in the code; it is the point of the question (documenting changes), so kept.
- Q14/Q54 show deliberately "risky" lines; they run silently or warn on pandas 3, as described.
- Overlap (report only): Q14, Q37 and Q54 all cover chained assignment/SettingWithCopy (intentional graded variants); Q11, Q33, Q34, Q56, Q63 outlier methods overlap with Book 5 Part 2 (sources note says concepts live there); Q7/Q8/Q15/Q40 overlap on fill-and-flag. Ordering and numbering are consistent (stars descend 3, 2, 1).

## Left unverified (labelled in the text)
- Q54: pandas 2.x had an opt-in Copy-on-Write switch (from memory).
- Q60: 5 lakh rows fit comfortably in laptop memory (from memory).
- Q62: asserts are skipped under `python -O` (from memory).
- Q14: `SettingWithCopyWarning` on pandas 2.x and older (cannot run; stated as such).
- Q51: rapidfuzz, Q62: pandera/Great Expectations (not run, labelled).
