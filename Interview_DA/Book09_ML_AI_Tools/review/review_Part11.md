# Review Part 11 (Book 9, Cloud basics for analysts)

## Counts
- Answers checked: 21 of 21
- Code blocks run: 4 Python/SQL runnable blocks (Q5 Python, Q15 Python, Q14 SQLite stand-in, Q20 SQLite stand-in) plus the 2 Snowflake/BigQuery SQL blocks (Q14 fix, Q20), which cannot run here and are labelled as such
- Outputs matching pasted Output and prose: 4 of 4 (Q5 2/10, 0.4/2.0, 0.8; Q15 120 and 80; Q14 both queries [(1, 50.0), (2, 100.0)]; Q20 two rows)
- Answers changed: 9 (Q4, Q5, Q11, Q14, Q15, Q17, Q20, Q21, Q6). No numeric or code error found.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q4 | Azure "moving to Fabric" stated without label inside table | Added "from memory, unverified" |
| Q5 | No "Explain simply" section; TB unexplained | Added plain-words section |
| Q6 | Jargon "normalised tables" | Replaced with plain wording |
| Q11 | T-SQL and Spark unexplained | Added short glosses |
| Q14 | SQLite check used hidden data; "pruning" unexplained | Stated the invented 4-row table and strftime substitution; defined partition pruning |
| Q15 | No "Explain simply" section; credit unexplained | Added |
| Q17 | No vendor-facts label (mentions Snowflake/BigQuery) | Added label |
| Q20 | Hidden sample rows; VARIANT/cast unexplained; no "Explain simply" | Stated the two JSON rows, added explanation |
| Q21 | "Entra" unexplained | Glossed |

## Recomputed figures
Q5: 2 TB x 2/10 = 0.4 TB; cost 10 vs 2 (illustrative rate 5); saving 80%. Q15: 2 x 3 x 20 = 120; at 2 h/day = 80; each hour removed saves 2 x 20 = 40. Correct.

## Unresolved / report only
- Ordering/numbering: unchanged; star spread (no 3 stars) matches sources file. Q11 is referenced as "lakehouse" in Q2 correctly.
- Overlap: Q1/Q8/Q10 touch privacy topics also likely in other Book 9 parts (GenAI privacy); not checked against other part files.
- "Asked at" lines all say commonly asked (no company-specific report found); Q7's Microsoft Hyderabad review matches the sources file.
- Q3, Q16, Q10 etc. have no wrong claims but all vendor facts remain unverified (no web access).

## Claims left unverified (from memory, labelled in the file)
Snowflake auto-suspend, credits, Time Travel/UNDROP/Fail-safe, VARIANT path syntax, FLATTEN, query-history views; BigQuery bytes-scanned billing, LIMIT not cutting cost, partition pruning with functions, dry run; Fabric OneLake, SQL analytics endpoint read-only, Direct Lake; Synapse-to-Fabric direction; DPDP Act/GDPR applicability; Power BI mode behaviour. No cloud service was run.
