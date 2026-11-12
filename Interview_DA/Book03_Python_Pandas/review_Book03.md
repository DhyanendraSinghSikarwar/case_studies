# review_Book03.md — Book 3 (Python & pandas) review summary (Wave C, plan.md Section 8.6)

Date: 2026-11-12. One reviewer per part re-ran every Python snippet (Python 3.13, pandas 3.0.5, numpy 2.5.3, matplotlib 3.11.2, seaborn 0.13.2 with Agg; mock server for API snippets), fixed errors in place and wrote `review/review_PartNN.md` (per-fix detail there). Reviewer counts are the reviewers' own and some are approximate.

## Pass criteria (plan.md 8.6)
| Check | Result |
|---|---|
| Completeness | 672 of 672 answered; 0 `ANSWER_PENDING` (script check) |
| Count | 672 vs target 600 (met) |
| Ordering / numbering | Continuous Q1..Qn in all 12 parts (script check) |
| Template fields | Asked at, interviewer check, Say this, Explain simply, follow-ups, common mistakes present in all 672 (script check) |
| Markdown | Code fences balanced in all parts |
| Accuracy | All snippets re-run; pasted outputs now match except intended errors, machine-dependent timings and file-path/memory-address lines |

## Per part
| Part | Answers | Answers edited | Main fix types |
|---|---|---|---|
| 1 | 73 | 11 (+34 fence labels) | order-dependent set claim, misleading memory size, retimed claims |
| 2 | 50 | 34 | 31 missing Sample data lines, wrong `:05` padding claim, traceback lines |
| 3 | 30 | 18 | wrong timing claim (Q9), keepdims, argmax with NaN, "every pandas column is NumPy" limited |
| 4 | 75 | 59 | missing imports, scratch path in output, unsupported "Asked at" claims, Q53 dtype deprecation |
| 5 | 83 | 33 | Q1 sample missing columns, Q11 applymap removed, Q35/Q58 false pandas 3 claims, wrong output order |
| 6 | 63 | 12 | outputs re-pasted, Q56 IQR claim, filler lines removed |
| 7 | 46 | 5 | Q7 errors="ignore" now raises on pandas 3, Q45 output |
| 8 | 50 | 11 | Q33 weekend sample wrong weekday, Q49 inconsistent series, Q30 silent-drop claim |
| 9 | 54 | 18 | Q15 wrong biggest drop, Q4 ties claim, Q42 MCAR/MNAR, Q26 pivot_table defaults |
| 10 | 71 | 24 | Q68 wrong prose vs output, Q21 overflow claim, 19 missing Sample data lines |
| 11 | 48 | 8 | missing sample tables, Q21 output, over-claimed "Asked at" |
| 12 | 29 | 6 | Q14 JD share (35% not 32%), Q18 unsupported companies, Q20 validate advice |

## Known limits (not fixed; honest status)
- **pandas 2.x and older-version behaviour** was not run (only 3.0.5 installed); such claims are labelled "from memory, unverified".
- **Not run:** live API/web calls (mock server only), shell/cron/venv/nbconvert blocks (Parts 11), Jupyter magics, Streamlit, rapidfuzz, pandera, Great Expectations; plots checked for data and calls, images mostly not viewed.
- **Timings** are machine-dependent and labelled so; random outputs hold for numpy 2.5.3 only.
- **"Asked at"** limited to what research files support; research was search-snippet only and no page was opened in full (e.g. Tiger Analytics, Pivigo, PracHub, GoLinuxCloud mentions).
- seaborn 0.13.2 with matplotlib 3.11 emits deprecation warnings on boxplots/heatmaps (Part 8 Q12, Q34, Q42, Q43); charts still draw; answers unchanged.
- Part headers: Part 11 says Target 40 / Actual 48; Part 9 title says 🟡🔴 though some answers are 🟢. Left as is.
- Topic overlaps inside and across parts (frequency counting, lambda, chained assignment, outliers with Book 5 Part 2, charts with Book 4 Part 8) were reported, kept and cross-referenced.
- Follow-up formatting differs between early and late answers in several parts (bullets vs numbered); left as is.
- A human read-through by a non-technical reader is still advisable.
