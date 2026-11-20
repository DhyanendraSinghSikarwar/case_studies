# Review: Book 4 Part 02 (Power Query transformations), Wave C

Reviewer scratch: /tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C04_Part02 (pandas 3.0.5; no Power BI, DAX engine or Power Query available; Microsoft Learn not fetched).

## Counts
- Answers checked: 61 of 61 (Q1-Q61).
- Pandas check snippets: 48 (13 concept answers have none: Q1, Q2, Q8, Q13, Q23, Q27, Q29, Q32, Q35, Q36, Q38, Q51, Q60 - acceptable, no measure or table).
- Snippets run OK, output equals the printed output: 48 of 48 (Q3-Q21 passed unchanged; Q22-Q61 had to be rebuilt first, see below).
- Answers fixed: 35 (31 snippet rewrites plus text fixes; some overlap).
- DAX measures: none needing a result re-derivation (only calculated-column IF/TRIM/DATEDIFF/CALENDAR snippets, read by hand, syntax OK, all labelled "not run here").

## Main finding
Q22-Q61 (31 answers with a pandas check) used fragments that could not run (undefined `emp`, `d`, `pd`, `n`, ...) and had no real printed output, only "Printed: ...". Each was replaced with a self-contained snippet plus the real pandas 3.0.5 output. Q28 had a snippet but no output block. Results lines already matched the new outputs, except where listed below.

## Fix table
| Q | What was wrong | Fix |
|---|---|---|
| Q22, Q24-26, Q28, Q30, Q31, Q33, Q34, Q37, Q39-Q50, Q52-Q59, Q61 | Pandas check not runnable, no real output | Self-contained snippets, real output pasted (Q42 builds temp CSV folders; Q58 runs SQLite; Q61 counts reads) |
| Q28 | Said fixed decimal "truncates" but example rounds | Reworded to "keeps four decimals"; rounding rule labelled unverified |
| Q30 | Follow-up DAX had `...` placeholder | Full `COUNTROWS(FILTER(Attendance_Long, ...))`, labelled not run |
| Q37 | "Blanks never match" contradicts Q9 (nulls match nulls) | Corrected to "a blank matches only another blank" |
| Q38 | "Filters flow both ways" wrong for default relationships | Now: flow from lookup table to data table |
| Q39 | Unsupported claim on how Service treats cell errors | Softened and labelled unverified |
| Q41 | Regional Settings path abbreviated | Full path given, labelled unverified |
| Q42 | Claim that firewall "trims" parameters stated as sourced | Labelled from memory, unverified |
| Q46 | DAX referenced `Employee[Dept]`, table is `Employees_Raw` | Fixed table name |
| Q47 | Main M used Table.Max on date only, yet Result claimed RecordID tie-break; "Microsoft says buffer" overstated | Table.Max now takes {EffectiveDate, RecordID} (list rule labelled unverified); buffering described as community workaround; Result says neither M version was run |
| Q48 | TransformColumnTypes culture-record claim unlabelled | Labelled from memory, unverified |
| Q51 | Said Windows-only verified by Microsoft; Q1 says unverified | Made consistent: from memory, unverified (sources file only has vendor blogs); "free" kept (Microsoft page) |
| Q53 | Jaccard unexplained; Pune row misleading | Plain explanation; scores re-derived by script (1.00, 0.67, 0.23, 0.67, 0.00 match) |
| Q57 | Compatibility table omitted Private/Public; "partition" unexplained; parameter claim unlabelled | Row added, term explained, claim labelled |
| Q58 | "DDL" unexplained | Explained in brackets |
| Q59 | Sample table lacked Name and Dept needed by the code | Table now has Name, Dept; Dim_Dept keys stated |
| Q27 | Vague edge case about "Include in report refresh" | Reworded, labelled unverified |
| Q60 | "Semantic model" unexplained | Explained as the Power BI data model |

## Checks with no change needed
- Template fields present everywhere; measure/transformation answers have Sample data, Steps, Alternative, Result, Pandas check. Every M/DAX block and click-path is labelled "not run here" (or "M code, not run here"); results say "reproduced with pandas".
- Ordering: stars descending, then green-yellow-red within star: correct. Numbering Q1-Q61 continuous. Headings untouched.
- Markdown: 61 headings, code fences balanced, no table missing a blank line, no ANSWER_PENDING.
- Duplicates/overlap (report only): Q9/Q37 (left anti), Q13/Q35/Q36 (folding, deliberate pair), Q25/Q30/Q31 (unpivot), Q47/Q61 (latest record vs Table.Buffer), Q41/Q52 (locale dates), Q44/Q45 (performance). Incremental refresh policy (Q56) and gateways overlap Part 7; relationships (Q38) overlap Part 3; folding performance scenarios overlap Part 9.

## Unresolved / unverified
- Many version, menu and behaviour claims cite Microsoft Learn pages that are not in research/Book04_Part02_sources.md (which lists 8 fetched pages). They could not be re-checked here: e.g. Working with duplicate values, Fill values, Replace values, Parameters, Fuzzy merge, Add column from examples, Diagram view, Dataflow Gen1/Gen2 pages, native-query folding connector list (Q58), Table.Buffer/Table.Sort/Table.Distinct buffering advice (Q61), Download Power BI Desktop. Left as written; treat as Wave B citations, not confirmed.
- M functions were checked by reading only: Table.Max with a list rule (Q47), SplitTextByEachDelimiter arguments (Q17), culture record with MissingField (Q48), Number.From(null) returning null (Q43, assumption already stated).
- Windows-only Desktop, Enable load / Using Locale menu names, Close/Apply variants: unverified (labelled).
- Q53 scores are an own bigram approximation, not Power Query's algorithm (already stated).
- "Asked at" lines match the sources file (no company-specific Power Query report found); none changed.
