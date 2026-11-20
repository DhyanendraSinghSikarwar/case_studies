# Review: Book 3 Part 04 (pandas: read, select, filter, sort), Wave C

Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, openpyxl 3.1.5. Scratch: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C03_Part04`.

## Counts
- Answers checked: 75 of 75 (headings, numbers, stars, order untouched; verified by diff).
- Python code per answer rebuilt from its Sample data (fixtures for CSV/Excel files) and run: 75 of 75 run. 71 match the pasted Output exactly; the other 4 are expected differences (Q14 deliberately raises the error shown; Q28 prints nothing and creates two files, checked; Q47 prints the machine's folder; Q69 prints nothing).
- About 55 concept claims (error types, defaults, NaN handling, deprecations) checked by running on pandas 3.0.5.
- Answers edited: 59 (many with several small edits).

## Fixes
| Q | Wrong | Fix |
|---|---|---|
| 47 | Output pasted another session's scratch path (`/tmp/claude-0/.../f1f97a91.../B03P04_Q39-57`), unusable for a reader | Re-ran in a real folder; output now `/home/hr/reports` and `False`; added Sample data line |
| 71 | Pasted Output had one extra space per row vs real output | Replaced with real output; added Sample data line |
| 57 | Output block mixed the stderr warning text with printed output | Output now only the two prints; warning described in a note after the block |
| 53 | Said `include="object"` selects text; on 3.0.5 it still works but raises a deprecation warning | Now says use `include="str"` on pandas 3, object is deprecated (ran it) |
| 63 | Default `kind` marked "from memory"; actually checkable | Verified from the installed docs: default quicksort, only mergesort/stable are stable, `kind` only for single-column sorts |
| 27 | "Column order: from memory, verify" | Ran it: file order, not list order; label updated |
| 69 | "About 20 columns and 60 rows" is notebook-only (terminal default is auto width, 0) | Reworded; added the missing Sample data and Output ("nothing printed") |
| 49 | Common mistake about `sort_values` with an index name was vague and unverified | Replaced with the real beginner mistake (mixing up `sort_values` and `sort_index`) |
| 50 | "inplace does not save memory" stated as fact | Labelled "from memory, unverified" |
| 5-9, 11-16, 19 | Code uses `employees` but Sample data did not say how it was loaded | Sample data line now gives the `pd.read_csv("employees.csv")` load, Q7 notes the set_index |
| 10 | `payroll` DataFrame appeared from nowhere | Sample data says the table is a DataFrame called `payroll` |
| 17, 18 | Code used `pd` without `import pandas as pd` | Import added |
| 20-38 | Sample data blocks used `pd` without import (code would not run as shown) | `import pandas as pd` added to each |
| 52 | No Sample data field | Added |
| 70 | Jargon "pointers" | Plain-words replacement |
| 64, 73 | In-memory CSV scaffolding unexplained | One-line comments added saying why |
| 58-60, 62, 63, 67, 72, 74 | Tables without blank line after (and before) | Blank lines added |
| many | Output fences without language | `text` added |
| Asked at: 2, 5, 6, 8, 10, 14, 16, 20, 21, 23-26, 29-31, 33, 34, 36-38 | Claimed "DataCamp, AskPython" or "every guide"/"classic"/"staple" for topics the sources file does not support | Reworded to what Book03_Part04_sources.md supports; otherwise "no specific source found". Q36, Q37 keep DataCamp (loc vs iloc is in the source) |

## Verified true by running (no change needed)
`&` without brackets gives `TypeError ... 'int' and 'StringArray'` (Q13); `and` gives the ambiguous-truth ValueError (Q14); `drop("department")` KeyError and axis+columns ValueError (Q19); `nlargest` on text TypeError, `keep="all"` (Q23, Q35); `between(inclusive="left")`, chained comparison ValueError (Q26); usecols misspelt ValueError (Q27); `sum()` on text joins words (Q31); filtering on a duplicate name raises (Q32); `reset_index()` adds `index` column (Q34); `UndefinedVariableError`, `in @list` (Q41, Q42); `UnicodeDecodeError ... 0xe9 in position 13` (Q46); int column plus 1.10 raises TypeError on 3.0.5 (Q58); `iloc[105]` IndexError (Q59); `FileNotFoundError` for a text string passed to `read_csv` (Q71); MultiIndex `loc["L1"]` KeyError and unsorted-slice error (Q72); no SettingWithCopyWarning and original untouched (Q16, Q22, Q75); `ChainedAssignmentError` (Q57, Q75).

## Unresolved / report only
- Ordering: stars and difficulty are in order (3-star, 2-star, 1-star; within star, green then yellow then red) except Q57 (2-star red) correctly last of its group. No ordering problems found.
- Overlap: Q20 (unique/nunique) and Q31 (count by condition) touch Book 5 Part 11 (value_counts, describe); Q23, Q35 (top-N) overlap each other; Q21 and Q6 (single vs double brackets) overlap; Q57, Q16, Q75 (chained assignment, Copy-on-Write) overlap three ways; Q30 and Q51 (max vs idxmax) overlap; Q43, Q27, Q73 (large file reading) overlap. Left as is; dedupe decision belongs to the book owner.
- Q8, Q10 "Asked at" no longer cites specific sources for the plain examples; nothing company-specific exists for any answer in this part.
- Line 1 title contains an em dash ("Book 3 — Python"); it is the file title, not answer text, left unchanged.
- Q22, Q50, Q75 mention pandas 2.x behaviour: marked "from memory, unverified" (pandas 2.x not installed).

## Claims left unverified
- All pandas 2.x and earlier behaviour (warning text, `object` dtype display, Copy-on-Write opt-in).
- Q45 `ImportError` when openpyxl is missing (openpyxl is installed here).
- Q35 "nlargest is usually faster" (docs/blog claim, not timed). 
- Q71 live URL read (no internet).
- Tiger Analytics / Adaface mentions in Q1 and Q48 rest on search-summary snippets per the sources file.
