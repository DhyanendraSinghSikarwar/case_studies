# Book 3 Part 10 Sources & research notes (Pivot/unpivot, string ops, NULL traps)

Date: 2026-10-25. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported SQL questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found or relied on; every source is documentation, a public problem statement, a guide or a search snippet. Final count: 40 questions (3-star 15, 2-star 16, 1-star 9).

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| SQLite core functions | https://www.sqlite.org/lang_corefunc.html | official docs | lower/upper ASCII only, trim character-set semantics and space-only default, length (code points, stops at NUL) vs octet_length, substr, concat/concat_ws NULL rules, instr NULL/0, replace with empty pattern, nullif/coalesce/ifnull, hex/unhex/unicode/char, quote, format/printf, iif (summary says 2-argument iif needs 3.48 and more than 3 arguments 3.49: not relied on for 3.45.1) |
| SQLite expressions | https://www.sqlite.org/lang_expr.html | official docs | LIKE (ASCII case-insensitive, ESCAPE), GLOB, REGEXP not built in, IS [NOT] DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL matrix, CAST rules, boolean expressions and IS TRUE |
| pandas reshaping | https://pandas.pydata.org/docs/user_guide/reshaping.html | official docs | pivot duplicate error, pivot_table aggfunc/margins, melt, wide_to_long, stack/unstack, crosstab normalize, explode (the page does not cover dropna, observed, fill_value or future_stack; those were checked by running) |
| pandas text data | https://pandas.pydata.org/docs/user_guide/text.html | official docs | str vs string dtype, NA handling, na= argument, split/rsplit expand, replace regex, extract, cat, casefold, normalize; the summary did not state default regex values (checked by running) |
| doocs LeetCode 1484 | https://leetcode.doocs.org/en/lc/1484/ | LeetCode mirror | COUNT(DISTINCT), GROUP_CONCAT(DISTINCT) per sell_date |
| doocs LeetCode 1795 | https://leetcode.doocs.org/en/lc/1795/ | LeetCode mirror | unpivot store1..store3, NULL price dropped, UNION of three SELECTs |
| doocs LeetCode 1667 | https://leetcode.doocs.org/en/lc/1667/ | LeetCode mirror | UPPER(LEFT) + LOWER(SUBSTRING) |
| doocs LeetCode 1527 | https://leetcode.doocs.org/en/lc/1527/ | LeetCode mirror | 'DIAB1%' OR '% DIAB1%' |
| doocs LeetCode 1873 | https://leetcode.doocs.org/en/lc/1873/ | LeetCode mirror | odd id and name not starting with M |
| DataVidhya pivot/cross-tab | https://datavidhya.com/learn/sql/interview-patterns/pivot-cross-tab | prep lesson | opened but only the introduction returned (CASE inside SUM/COUNT, dynamic pivot, NULL categories) |
| prachub string manipulation topic | https://prachub.com/topic/sql-data-manipulation-interview/string-manipulation | question list | titles with company labels (Meta, Stripe etc.); the page does not say they are candidate reports, so no company claims used |

## Search results only (snippets, not opened)
- Pivot: datadriven.io/sql/pivot, Educative 'pivot flip', coddykit 'dynamic pivots with unknown columns', mimo.org, a Medium PIVOT/UNPIVOT post (conditional aggregation as the default answer; UNION ALL for unpivot; dynamic pivot = generate SQL from distinct values; a Snowflake PIVOT subquery/ANY claim was not verified).
- Strings: datadriven.io string-functions, DesignGurus, Codecademy, DataCamp split_part pages, sqltest.online, prachub topic (domain extraction, split, case and whitespace normalisation, off-by-one in SUBSTR, NULL concat differences).
- NULL: prachub null-handling and COALESCE pages, datadriven.io null-handling, dataford, Interview Query handling-null-values (= NULL mistake, AVG skips NULL, COALESCE inside aggregate vs around it).
- Indian IT-services banks: Scribd Cognizant GenC SQL cluster and other uploads, Telegram jobs_SQL, kitemetric TCS guide (generic topics: NULL, duplicates, CONCAT, SUBSTRING, REPLACE, pivot definition; quality unverified).
- LeetCode 1965 Employees With Missing Information (not used).
- Not found: candidate reports for any exact question here; many questions are expert extensions (tagged 'Expert extension').

## Environment checks (run, SQLite 3.45.1, Python sqlite3; pandas 3.0.5)
SQLite results:
- Missing: regexp (error 'no such function: regexp'), split_part, reverse, lpad, char_length. ICU not compiled (ENABLE_ICU 0), FTS5 compiled.
- Present: format and printf (printf('%05.1f|%,d',3.14159,1234567) gave '003.1|1,234,567', so the %,d comma flag works here: portability not claimed), concat('a',NULL,'b')='ab', concat_ws(',','a',NULL,'b')='a,b', string_agg exists and accepts ORDER BY inside (string_agg(v,'|' ORDER BY v)='a|b'), group_concat(v ORDER BY v DESC) works, octet_length('é')=2, length('é')=1, length('a'||char(0)||'b')=1, unicode('é')=233, hex('é')='C3A9', unhex('4142') is a blob, quote(NULL)='NULL', iif works, IS DISTINCT FROM works, NULLS LAST works.
- Case: lower('ÄB')='Äb', upper('ß')='ß', 'Ä' LIKE 'ä' = 0, 'a' LIKE 'A' = 1, 'é'='É' COLLATE NOCASE = 0, 'B' < 'a' = 1 (binary).
- Trim: trim('  x  ')='x'; trim('xxaxx','x')='a'; ltrim('xxa','xa')=''; trim does not strip char(160) or tab or newline by default.
- CAST: 'abc'->0, '12abc'->12, '1e3' as INTEGER ->1 and as REAL ->1000.0, ' 12 '->12, '1,234'->1, '007'->7, ''->0, '0x10'->0, '  3.7' as REAL->3.7. '3x'+1 = 4 and 'a'+1 = 1 (arithmetic coerces the same way).
- Comparison: '10'<'9' = 1; 10<9 = 0; '10'<9 = 0; 10<'9' = 1 (literals, no affinity); '12'=12 literal = 0 but a TEXT column holding '12' compared with 12 matched (column affinity converts); typeof for INTEGER/NUMERIC affinity columns converts '12' to integer, 'x' stays text, ' 12' became integer 12 in the run (verify before stating in an answer).
- LIKE: 'a_c' LIKE 'a\_c' = 0 without ESCAPE, = 1 with ESCAPE '\'; 'abc' LIKE 'A_C' = 1; GLOB is case-sensitive; 'x' GLOB '[^a-c]' = 1.
- NULL: 1 IN (2,NULL) NULL; 1 NOT IN (2,NULL) NULL; NULL NOT IN () = 1; CASE NULL WHEN NULL ... gives ELSE; CASE without ELSE gives NULL; NULL UNION NULL one row; NULL INTERSECT NULL one row; NULL EXCEPT NULL none; count(distinct) of NULLs 0; sum(NULL) NULL, total(NULL) 0.0, avg(NULL) NULL; 'a'||NULL NULL; NULL IS TRUE 0, NULL IS NOT TRUE 1.
- Constraints: UNIQUE(a) accepted two NULL rows; CHECK(x>0) accepted NULL; a non-INTEGER 'a primary key' column accepted two NULLs (legacy quirk); INTEGER PRIMARY KEY with NULL gets an auto id.
- Window: lag(x,1,-1) with NULL x gives -1 only for the first row (the default applies to missing rows, not NULL values); SUM over a frame skips NULL.
- Dates: date('2024-1-1') NULL, date('2024-13-01') NULL; round(2.5)=3.0, round(0.125,2)=0.13, round(703.125,2)=703.13; printf('%.0f',2.5)='2' (half to even via the C library), printf('%.0f',3.5)='3'... check again for Wave B.
- sqlite3 'You can only execute one statement at a time' for executescript-style strings in execute(): use executescript for DDL batches.
- regexp registered with create_function('regexp',2,fn) works: 'abc123' REGEXP '\d+' = 1.
pandas 3.0.5 results:
- pd.Series(['a',None,np.nan,'B ','']) dtype is str; missing values are NaN (not None); isna True for both; .str.len gives float64 with NaN; .str.contains gives False for missing in the default call and with na=False; dtype 'string' uses pd.NA and gives <NA> in comparisons; object dtype stays object and .str.upper keeps None; bool(pd.NA) raises TypeError ('boolean value of NA is ambiguous'); mixed list ['a',1] stays object; Series([None,'x']).astype(str) kept NaN in the str dtype run (check what astype(str) does to missing: it gave [nan,'x']).
- str.replace default regex is False: ' +' did not collapse spaces; str.contains default regex True ('.' matched 'a.b' with 'A'? check: contains('.') returned True); str.strip removes NBSP (U+00A0); str.normalize('NFC') merged 'é' forms; str.casefold, zfill, pad fine; str.split(expand=True) gives NaN row for missing; str.cat with sep and NaN skips missing; Series.str on ints raises AttributeError ('Can only use .str accessor with string values').
- groupby dropna: default drops NaN keys, dropna=False keeps them; nunique default skips NaN; value_counts(dropna=False) keeps NaN; sum of all-NaN is 0.0, with min_count=1 is NaN, mean is NaN.
- pivot_table default for a categorical key: observed=True by default in 3.0.5 (shape (1,2) vs (2,2) with observed=False); pivot with duplicates raises ValueError 'Index contains duplicate entries, cannot reshape'; margins adds 'All'; NaN row label (product None) is dropped from columns; crosstab on a column named product/prod: do not use df.product (it is the DataFrame.product method; use df['product']); stack(): shape stayed 4 with and without future_stack on a frame with one NaN (NaN row kept in the 3.0 default), unstack sorts; wide_to_long worked with sep='_'; explode of 'a,b,,c' split keeps the empty string; split of None gives NaN.
- to_numeric(errors='coerce') on ['1','x','1e3',' 4 ','1,234'] gave [1,NaN,1000,4,NaN]; astype(int) on 'x' raises ValueError; astype of '007' to int gives 7; to_datetime(errors='coerce') on '05/01/2024' after an ISO first value gave NaT (format inferred from the first element); format='mixed', dayfirst=True parsed '05/01/2024' as 1 May; category: assigning a value outside categories raises TypeError in the run; .str.upper works on a category of strings; groupby with a categorical key: no unobserved row appeared in the run (observed default True in 3.0.5).
- Python str.title: not checked here (Wave B should run 'o''neil').

## Cross-references verified by heading (question_index.md and part files)
Part 1 Q4, Q5, Q6, Q10, Q13, Q14, Q16, Q36, Q39, Q41, Q44; Part 2 Q6, Q35; Part 3 Q3, Q22, Q25; Part 4 Q10, Q29; Part 5 Q3, Q18; Part 6 Q1; Part 9 Q1 (recursive CTE mechanics).

## Hedge list for Wave B (not verified by running, or from snippets)
- PIVOT/UNPIVOT syntax (SQL Server, Oracle, Snowflake, BigQuery), UNPIVOT NULL handling and INCLUDE NULLS options, Snowflake PIVOT ANY and subquery in IN, PostgreSQL crosstab and tablefunc, MySQL no PIVOT: not executed.
- SPLIT_PART, SUBSTRING_INDEX, STRING_SPLIT, UNNEST(STRING_TO_ARRAY), REGEXP_REPLACE/REGEXP_LIKE/REGEXP_SUBSTR, INITCAP, LPAD/RPAD, REVERSE, TO_CHAR, FORMAT, TO_DATE/STR_TO_DATE/TRY_CONVERT/SAFE.PARSE_DATE, TRY_CAST/SAFE_CAST, STRING_AGG/LISTAGG/GROUP_CONCAT limits (group_concat_max_len) and WITHIN GROUP, ILIKE and collation-dependent LIKE in MySQL, concat() NULL rules per engine, UNIQUE NULLS NOT DISTINCT (PostgreSQL 15), SQL Server unique index with one NULL, ROLLUP/CUBE/GROUPING SETS/GROUPING(), QUOTENAME/sp_executesql, EXECUTE IMMEDIATE: not executed.
- The 3.44 ORDER BY inside group_concat/string_agg works on 3.45.1 (run) but docs pages for the exact release were not opened; older SQLite lacks it.
- iif argument-count rules and unistr availability by version (docs summary mentions 3.48, 3.49 and 3.50): not relevant for 3.45.1, do not use unistr.
- The printf %,d thousands flag worked on 3.45.1 but its documentation (printf.html) was not opened: label it a SQLite quirk.
- STRICT tables (3.37+), PRAGMA case_sensitive_like and the exact affinity conversion of ' 12' were not documented-checked: run and report.
- No candidate reports: do not claim any company asked these.
