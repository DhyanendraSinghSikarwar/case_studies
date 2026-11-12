# Review: Book 3 Part 02 (strings, file handling, error handling)

Environment: Python 3.13, pandas 3.0.5. Scratch: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C03_Part02` (run.py, claims.py, patch.py).

## Counts
- Answers checked: 50 (Q1 to Q50)
- Python snippets run: 52 blocks across 50 answers, all ran as shown (Q17, Q24, Q25, Q49 end in the intended error; Q25 has 2 blocks, Q50 has 2)
- Output match: 44 of 50 identical; the other 6 (Q17, Q24, Q25, Q27, Q49, Q50) differ only by file path, warning text or the extra "Alternative" block output; real wrong parts fixed below
- Side claims run on pandas 3.0.5 / plain Python: title() on "o'neil", zfill sign, :05 on a string, json with np.int64/None/tuple, bare except catching Ctrl+C, assert removed by -O, finally-before-return, casefold, find/index, pandas .str equivalents (Q5, Q16, Q31, Q39, Q43), read_csv chunksize, to_numeric coerce, read_csv sep="|"
- Answers fixed: 34 (31 got a Sample data field; 3 more fixed for other reasons: Q12, Q39, Q47; several of the 31 also had other fixes)

## Fixes
| Q | Wrong | Fix |
|---|---|---|
| 17 | Pasted traceback lacked the caret line Python 3.13 prints | Added `~~~~~~~~~~^^^^^` line |
| 22 | Claimed `:05` on a string pads spaces on the right; actual result is `'45000'` (zeros on the right) | Corrected the Common mistakes line |
| 25 | Line numbers 2 in both pasted errors; the code blocks start with a comment, so the error is on line 3 | Changed to line 3 in output and in "What it means" |
| 49 | Traceback trimmed with `...` and a note | Replaced by the real traceback lines (path shortened) |
| 12 | Common mistakes sentence about `" 45000"` was confusing and misleading | Rewrote it plainly |
| 14, 49, 39, 47 | "from memory, not run here" for claims that can be run | Ran them (bare except catches Ctrl+C; `-O` drops assert; pandas split/strip; chunksize) and replaced the label with "checked" |
| 3, 5 | First-person "(I ran it)" notes in answer text | Reworded to neutral "checked by running it" or removed |
| 50 | "checked by running" wording | Changed to "verified by running" |
| 3, 5, 6, 7, 8, 10, 11, 14, 15, 17, 20, 21, 22, 23, 25, 27, 28, 31, 33, 35, 37, 38, 39, 42, 43, 44, 45, 46, 48, 49, 50 | Template field Sample data missing for code questions | Added a one-line Sample data field before each Code block (31 answers) |

## Claims check (Asked at)
All "Asked at" lines say "commonly asked (no company-specific report found)" or cite only sources listed in `research/Book03_Part02_sources.md` (ClimbTheLadder, Packt, AshokIT, Dataford, Glassdoor Securin, Analytics Vidhya, Naukri Code360, dev.to, Fiveable, Tiger Analytics snippets flagged "details not read"). Q40 matches `research/interview_processes.md` ("Mostly basic (lists, strings, duplicates, pandas)"). No invented companies or statistics found.

## Unresolved / report only
- Q38: the Windows blank-line symptom cannot be reproduced on Linux; kept labelled "from memory, unverified".
- Q1: "a file left open can lock the file on Windows" is not run (Windows only), stated in general terms.
- Pasted tracebacks (Q17, Q24, Q25, Q49) use shortened file names by design; Q27 omits the SyntaxWarning (the prose already mentions it).
- Q35 to Q50 use a shorter "Asked at" line and list-style follow-ups; format differs from Q1 to Q34 but fields are complete.
- Title line 1 contains an em dash (heading, not answer text), left unchanged.
- Overlap (report only): Q4/Q18/Q47 (reading files line by line), Q9/Q26 (missing file), Q3/Q37 (try/else/finally), Q28/Q48/Q49 (raise vs custom exception vs assert), Q12/Q36 (bad value handling), Q5/Q39 (strip/split cleaning), Q15/Q43 (case handling), Q31/Q20 (phone digits). Intentional cross-references exist; the spread across stars is consistent with the Wave A order. Q5/Q23 names and Q11 codes may overlap with Part 10 string tasks (boundary stated in the sources file).
- Ordering: stars descend 3, 2, 1 as required; no numbering issues.

## Not verified
Windows-only behaviour (Q1, Q27 path behaviour on Windows, Q38); pandas 2.x behaviour (none claimed).
