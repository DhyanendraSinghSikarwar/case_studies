# Review: Book 4 Part 7 (Power BI Service: publishing, refresh, gateways, incremental refresh, RLS, workspaces, licensing)

Reviewer: Wave C. Environment: pandas 3.0.5 only; no Power BI/DAX/M engine; Microsoft Learn not fetched. Scratch script: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C04_Part07/run.py`.

## Counts
- Answers checked: 65 of 65 (all headings, numbers, stars and order untouched).
- Pandas snippets run: 16 answers carry a Pandas check (Q1, 5, 7, 9, 19, 20, 22, 29, 30, 36, 38, 53, 54, 60, 61, 62). 15 reproduced the printed output and Result exactly; Q30 did not (see fixes). Several snippets are fragments relying on the sample-data table (`emp`, `s`, `log`, `p`, `e`, `dept`); I rebuilt the data from the tables and ran them all.
- Answers edited: 10 (Q19, Q23, Q26, Q30, Q35, Q38, Q39, Q51, Q61, Q63).
- DAX/M snippets (Q1, 5, 7, 19, 20, 29, 38, 61, 62, 64) read for syntax: balanced, correct functions and argument order (PATH, PATHCONTAINS, LOOKUPVALUE, Sql.Database, Table.SelectRows). All labelled "not run here". All results say "Reproduced with pandas".
- Template: all 65 have the nine common fields; non-calculation answers use "Result: Not a calculation". Markdown: 54 code fences (balanced), every table followed by a blank line.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q30 | Sample data pointed to the Q29 table (4 rows) but claimed monthly counts 2025-01:1 ... that need 8 rows; pandas on the real table gives only 2026-10:2, 2026-11:2. | Added an explicit 8-row Sales table (IDs 1-4 older rows plus Q29 rows); counts now reproduce. |
| Q23 | Said Build permission is "the other way RLS can be bypassed"; contradicts Q51 and the sources file (RLS applies only to Viewers; editors bypass). | Reworded: edit (write) access bypasses RLS, Build alone does not (from memory, unverified). Edge case rewritten. |
| Q39 | Suggested checking Build on the model as a cause of seeing all data. | Changed to "edit (write) access to the model through another route". |
| Q51 | "Granting Build to Contributors defeats RLS" muddled (Contributors already bypass). | Reworded: Contributor or higher defeats RLS; Build alone does not (unverified). |
| Q26 | Line "nobody is restricted properly: blocked or rely on edit rights" confusing and inaccurate. | Replaced with: a Viewer in no role sees no rows; editors still see all (unverified). |
| Q19 | Alternative text "FILTER-style ... IN" confusing. | Rewritten to plain `[Region] IN {"North","East"}` for several regions. |
| Q38, Q61 | "Asked at" claimed Wipro RLS report; interview_processes.md has Wipro for DAX/SUMX only, no RLS. | Removed Wipro from the RLS claim; kept Deloitte (Sept 2025) and Cognizant (2022) as single anecdotes. |
| Q63 | "Azure AD" is the old product name; Q5 uses Entra. | Now "Microsoft Entra ID (formerly Azure AD)" in both places. |
| Q35 | "Success emails? Not by default" stated as fact. | Marked "I believe not by default (unverified)". |

## Re-derived by hand (all match the Result lines)
Q1/Q5/Q22 region counts and salaries (North 3 / 113,000, neha 2 / 110,000, total 368,000); Q9 1,765 days, 31 reloaded, 1.8%; Q29 October window = IDs 5, 6, amount 280, `<=` gives 3; Q36 views and unused reports; Q38 150 / 195 / 345; Q53 1 of 6; Q54 off = 12-14 Nov, on = 11-13 Nov (UTC 20:30 on 14 Nov); Q60 249,999 vs 9,000,000 (36x); Q61 m1 sees A, C, D, departments Sales and IT; Q62 PATH strings and each manager's subtree.

## Unresolved / for the coordinator
- Pandas snippets in Q29, Q30, Q36, Q38, Q53, Q54, Q61, Q62 are fragments (no data construction); they run only after building the data from the sample table. Left as is to avoid padding; consider a "setup" line if full runnability is wanted.
- Q62: `LOOKUPVALUE` on the same table inside an RLS filter is a common pattern but its behaviour was not verified (labelled "from memory").
- Q61: the "Apply security filter in both directions" checkbox is believed to be available only when the relationship cross-filter direction is Both; not stated in the answer, unverified.
- Overlap (report only): Q23/Q39/Q51 repeat the Viewer-only RLS rule; Q16/Q34/Q47 repeat 8/48 and 2h/5h limits; Q12/Q59/Q65 overlap on licences and sharing; Q9/Q30 overlap on incremental refresh; Q27 vs Q6 on gateway set-up. Possible overlap with Part 9 (RLS/refresh scenarios) and Part 1 (licences) not checked file-by-file.
- Ordering: stars descending (3, 2, 1) and green-yellow-red within each star group: consistent. Numbering Q1-Q65 continuous.

## Claims left unverified (nothing could be fetched)
Refresh limits 8 vs 48 per day and 2 h vs 5 h duration; F64 free-viewer threshold; Pro 1 GB model size (Q50); Desktop Windows-only; workspace-role permission matrix; group types allowed in RLS roles (Q24); `USERNAME()` vs UPN behaviour in Desktop and Service (Q21); guest `#EXT#` UPN format (Q63); pause after four consecutive failures (Q47); deployment pipeline licence (Q45); gateway clustering details (Q46); Direct Lake requirements (Q52); OneDrive hourly check (Q32); all menu and click-path names. All are already labelled "from memory, unverified" or "not re-fetched" in the answers. No invented company claims, prices or statistics were found.
