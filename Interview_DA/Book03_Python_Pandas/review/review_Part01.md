# Review: Book 3 Part 01 (Python basics), Wave C

## Counts
- Answers checked: 73 of 73 (Q1 to Q73).
- Python blocks run: 75 (every block in the part, each in a fresh process on Python 3.13, pandas 3.0.5, numpy 2.5.3). Result: 75/75 run as shown; 66 outputs match the pasted Output exactly, 9 differ only for expected reasons:
  - Q1, Q4, Q13, Q14: the code ends on a deliberate error; the pasted Output shows only the final error line (not the full traceback). Acceptable.
  - Q50 (alternative snippet) and Q66, Q71 (alternative snippets): fragments that need the main snippet's data or print a comment; they run correctly once the main data is in place.
  - Q52: prints nothing (stated in the answer); timings re-measured, see fixes.
  - Q58: needs typed input; re-run with `Ravi` and `45000` piped in, output matches.
- Answers fixed: 12 (Q4, Q9, Q20, Q35, Q48, Q49, Q52, Q55, Q60, Q68, Q72, plus the bare-fence change on Q39 to Q55 and Q57 listed below).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q4 | Follow-up said mutable default is "not covered here" | Points to Q46 |
| Q9 | Vague "loop-control questions in this part" | Points to Q33 |
| Q20 | Claimed `list(set(...))` "gave ['IT','Sales','HR'] in my run"; string set order changes between runs (hash randomisation; I got two different orders) | Reworded: order is not fixed and varies from run to run |
| Q35 | `bool(float("nan"))` marked "from memory, not run here" | Ran it (True); label changed to "checked" |
| Q48 | Prose said the list "takes about 8 MB"; `getsizeof` counts only the list's pointer array, not the million int objects; generator size stated as exact | Prose corrected (about 8.4 MB for the list's own storage, excluding the number objects; generator "a few hundred bytes") |
| Q49 | `if employee["left"] == True:` (non-idiomatic); a weak, confusing "integer thinking" mistake line | Now `if employee["left"]:`; mistake line replaced with relevant ones; output re-run (40.0, 0) |
| Q52 | Timing figures not reproducible (0.109 s, 0.0066 s, "15 times") | Re-timed: loop about 0.12 s, vectorised about 0.005 s, about 20 times (still labelled single run, machine dependent) |
| Q55 | List timing 0.99 s | Re-timed: about 0.74 s for 100 searches; set about 0.00001 s |
| Q60 | Cryptic variable `s` in the comprehension (style rule 10/11) | Renamed to `salary`; output re-run |
| Q68 | Mistake line "writing `is not None` as `not x is None`" was backwards | Now "writing `not x is None` instead of `x is not None`" |
| Q72 | Awkward bullet "no guaranteed funnel order of meaning" | Rewritten in plain words |
| Q39 to Q55, Q57 | 34 Output blocks used bare code fences (no language) while the rest use `text` | Changed to ```text for consistency; fences remain balanced (146 plain + 71 text/python openers match) |

## Concept and claim checks (all run on pandas 3.0.5 / Python 3.13 unless noted)
- Verified by running: `{"a":1} | {"a":2}`; `divmod(23,5)`; `-7 // 2` = -4; `round(2.5)` = 2, `round(3.5)` = 4; error messages for `list.remove`, `list.index`, `50000 + None`, `int("abc")`, `int("45.5")`; `int(" 45000 ")` works; zip stops at shorter list; recursion limit 1000; Decimal from float keeps the error; `help()` shows the docstring; pandas `groupby(...)["name"].apply(list)` and `value_counts().head(3)` equivalents; NumPy `array == None` returns an elementwise array.
- Asked-at lines: all company mentions (TCS, Capgemini, Indium, Tiger Analytics, LatentView, Deloitte-style, Deliveroo mutable default) match `research/Book03_Part01_sources.md` or `research/interview_processes.md`; others say "commonly asked (no company-specific report found)". No invented sources found. Note: the sources file states these are single anecdotes seen only as search snippets.

## Unresolved / report only
- Ordering: stars descend 3 -> 2 -> 1, difficulty ascends inside each star except Q22 (green) sits before Q23 to Q25 (yellow) in the three-star block, which is correct; numbering Q1 to Q73 is continuous. No issues.
- Overlap: Q5, Q51, Q62, Q70 all teach frequency counting (cross-referenced with each other, deliberate). Q11/Q47 both teach lambda; Q24 also uses lambda for sorting. Q60/Q68 both cover None. Possible overlap with Book 3 Part 2 (strings), Part 10 (OOP basics/closures) and Book 2 pandas-equivalent rows; not checked against those files.
- Part title line (line 1) contains an em dash; it is a heading, left unchanged per the no-heading-change rule. Answer text has none.
- Q1, Q4, Q13, Q14 Output blocks show a one-line error instead of the full traceback (intentional, readable).
- Target says 70, actual 73; noted in the file header already.

## Left unverified
- Q17: claim that Python reuses small numbers or short strings, already labelled "from memory, unverified".
- All "Asked at" mentions rest on snippet-level, single-anecdote sources (see the sources file); not independently confirmable here.
- Q67: mention of `@st.cache_data` (Streamlit) is from memory, not run (Streamlit not installed).
