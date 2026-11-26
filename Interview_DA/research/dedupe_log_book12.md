# Book 12 dedupe log

- Frozen FAQ list: 108 questions (A12a 48 for Sections 1-2, A12b 36 for Sections 3-4, A12c 24 for Sections 5-6; target 100). Global numbering Q1-Q108 in `Book12_Portfolio_JobSearch/Book12_FAQs.md`, grouped by section, stars then difficulty inside each section.
- Method: Jaccard similarity on question wording across the three agent files (threshold 0.45) and against all 123 Book 0 FAQ headings (threshold 0.45).
- Result: no question matched a Book 0 FAQ. One internal pair above threshold (A12b Q21 "follow up if nobody replies to my message" vs A12c Q17 "follow up on an application"): kept both, different channel and timing advice (Section 4 outreach vs Section 6 applications).
- Agents were told to point to Book 0 Q14, Q19, Q58, Q64, Q74, Q75, Q84, Q101 rather than repeat them.
- Section 7 of the plan ("100 FAQs") is satisfied by the 108 FAQs.
