# Cross-part duplicate resolution (Book 7, Wave A)

Method: token-overlap scan (Jaccard >= 0.6 on question headings) of all 633 Book 7 questions across and within the 9 parts, then manual judgement. One hit: B7P2Q2 (cars in Hyderabad) vs B7P2Q26 (ATMs in Hyderabad), which are different estimation targets with different drivers; kept. No questions removed. Guesstimate prompts share a template ("Estimate the number of X in Y") but differ in the thing estimated and the drivers; case prompts differ in data and context.

Result: 633 questions (target 600 met). Part counts: P1 32, P2 94, P3 72, P4 87, P5 91, P6 76, P7 71, P8 57, P9 53.
Note for answer agents: the question texts were written without computing figures. Every inline-data question must be computed by code before the answer is written; every guesstimate base number is an assumption, labelled approximate and unverified (no source could be fetched); overlap between Part 5 (root-cause cases) and Part 7 (product analytics cases), and between Part 4 metric formulas and Part 8 HR metrics, was noted by writers and is by design.
