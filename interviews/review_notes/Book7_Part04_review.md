# Book 7 Part 4 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five research agents). Scope: 10 company profiles (Spotify, Zalando, Booking.com, Klarna, SAP, Delivery Hero, Revolut, Wise, Grab, Shopee). No pay figures; no visa, relocation or legal claims.

## Process
Five agents researched two companies each (7 to 11 WebSearch searches per company, snippet-only) and wrote profiles, source logs and per-company progress files; merged in company order with `scratch/B7_merge.py 4`; the lead wrote the header and the comparison table from the profiles. No spend-limit stops.

## Checks (`scratch/B7_check.py`, including tag-to-source integrity)
| Check | Result |
|---|---|
| Profile numbering C1-C10 and all 13 template labels present and in order | pass for all 10 |
| At least 8 evidence tags per profile; at least 2 source URLs; every `[S#]` used exists in that profile's Sources list | pass |
| 5 to 8 sample questions per profile, each tagged `[illustrative]` or `[S#]` | pass |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and codes with digits) | 0 hits |
| Cross-references to Books 1-6: every "Book N Part M (topic)" pair resolves to a real part and the parenthetical shares words with the plan.md title (agents checked; the lead re-ran the scan) | pass, 0 mismatches |

## Findings and honest limits
- Delivery Hero is the only Medium profile: the careers page and an official tech-blog interview post describe the loop (recruiter call, technical interview, system design for senior roles, hiring manager, bar raiser), and several 2025 Glassdoor reports describe a similar five-step shape; the official posts are dated (2019-2023) and engineering-oriented.
- Official sources that exist and are labelled official in the profiles: Booking.com (how we hire, AI-use guide), Wise (analytics case-study page, AI-in-recruitment page), Zalando (applied scientist blog, fragments), Grab (about a month, stages of 30 minutes to 1 hour), Spotify (principles and AI notice, no stage list), Revolut (AI interview tool announcement). None gives a full data science or ML round list.
- Candidate-facing AI-tool rules: official statements for Booking.com and Wise; the rest are absent or third-party. Revolut's April 2025 AI interview tool is a product announcement; its scope in data-role hiring is not stated.
- Offices: reports mix London, Stockholm, Berlin, Amsterdam, Tallinn, Singapore, Kuala Lumpur and Jakarta; where a source does not name an office the profile says so. No Walldorf or Berlin report for SAP; no London, Berlin-ML or India report for Klarna; no India-office process evidence for any company in the part.
- Many Glassdoor reports are old (Klarna 2011-2026, Revolut take-homes 2018-2020, Spotify mostly 2016-2023) and mix roles; the profiles label them anecdotal and keep conflicting round counts side by side.
- Discarded: pay mentions (Revolut, Wise, Spotify, Shopee), Deliveroo (a different company) in the Delivery Hero search, Spotify's consultancy posts, SEO aggregator pages.

## Not done
No page was opened (WebFetch fails in this environment). Nothing here replaces the company's careers page or the recruiter's description of the current process.

# Book 7 overall note
All 40 profiles (Parts 1-4) share the same evidence method and checker. Evidence levels across the book: no profile rated High; Medium for Google, Microsoft, Amazon, Meta, Apple, Uber, LinkedIn and Delivery Hero (and Visa for general shape only); the rest Thin or Thin to Medium. Use the books as a map of what to prepare and what to verify, not as a description of any company's current loop.
