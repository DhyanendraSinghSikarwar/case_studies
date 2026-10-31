# Book 7 Part 3 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five research agents). Scope: 10 company profiles (Walmart, Target, JPMorgan Chase, Goldman Sachs, American Express, Visa, Mastercard, Intuit, Atlassian, Optum). No pay figures; no visa or legal claims.

## Process
Five agents researched two companies each (7 to 9 WebSearch searches per company, snippet-only) and wrote profiles, source logs and per-company progress files; merged in company order with `scratch/B7_merge.py 3`; the lead wrote the header (with entity notes) and the comparison table from the profiles. No spend-limit stops.

## Checks (`scratch/B7_check.py`, including tag-to-source integrity)
| Check | Result |
|---|---|
| Profile numbering C1-C10 and all 13 template labels present and in order | pass for all 10 |
| At least 8 evidence tags per profile; at least 2 source URLs; every `[S#]` used exists in that profile's Sources list | pass |
| 5 to 8 sample questions per profile, each tagged `[illustrative]` or `[S#]` | pass |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and codes with digits) | 0 hits |
| Cross-references to Books 1-6: every "Book N Part M (topic)" pair resolves to a real part and the parenthetical shares words with the plan.md title (the agents also checked this; the lead re-ran the scan) | pass, 0 mismatches |

## Findings and honest limits
- Visa is the only profile with an official page that states round structure and AI-tool rules (careers page: 2 to 4 rounds, AI use during interviews prohibited, Copilot transcription for interviewer notes only), so its general shape is rated Medium; its India data science and ML evidence is Thin. Mastercard's and Atlassian's official pages give partial shape (behavioural component and problem-solving assessment; recruiter, hiring manager, skills, values interview, committee).
- Entity attribution: Walmart Global Tech India versus the global company, Target in India, Optum Global Solutions India versus other Optum business units (Dataford "Optum Tech" and "Optum Financial" guides and a Dublin report are flagged as other units), and American Express reports tagged only by city are all labelled; the American Express profile states that no report names a specific team.
- Many India reports are software-engineer, analyst or data-engineer roles; the profiles use them only as labelled proxies. No Hyderabad content for Walmart; no Chennai interview reports for American Express; no Mumbai interview information for JPMorgan; no applied scientist loops for Walmart, Target, Atlassian or American Express.
- Goldman Sachs and Atlassian: two source lines for Goldman point at the same posting URL for different claims (kept as listed); several Glassdoor sources across the part are pooled snippets whose page-to-detail match is flagged as approximate.
- AI-tool policy: official statements exist for Visa (prohibited) and Mastercard (encouraged in preparation, some roles invited to use AI with rules); the rest are third-party, news or anecdotal, and are labelled.
- Pay aggregates and ranges seen in results were discarded (Walmart, Goldman Sachs, JPMorgan, Optum, Intuit, Atlassian).
- Agents ran 7 to 9 searches per company, close to the brief's target; the healthcare data science search for Optum returned other companies and was used only as a [G] pattern with no source attributed to Optum.

## Not done
No page was opened (WebFetch fails in this environment). Nothing here replaces the company's careers page or the recruiter's description of the current process.
