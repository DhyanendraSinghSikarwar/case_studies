# Book 3 Part 8 Sources & research notes (Funnels, conversion, DAU/MAU, product metrics in SQL)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported SQL questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found or relied on; every source is a guide, vendor post, practice-site page, documentation page or search snippet. Final count: 45 questions (3-star 18, 2-star 16, 1-star 11).

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| PracHub product-analyst SQL funnel case | https://prachub.com/resources/product-analyst-sql-case-interview-event-data-funnel-definitions-and-recommendations | practice guide (states it is original, not a candidate report) | three funnel definitions on 8 users: presence within 24h 5/8, ordered same UTC day 2/8, ordered within 24h 4/8; DISTINCT safe only for identical duplicates; calendar day vs rolling window; strict vs inclusive; immature cohorts; MIN(event_ts) is first in available data |
| DataVidhya funnel analysis | https://datavidhya.com/learn/sql/interview-patterns/funnel-analysis | prep lesson (intro only) | description only: view to cart to purchase, self-joins and CTEs, time-bounded; body not visible |
| doocs LeetCode 1174 | https://leetcode.doocs.org/en/lc/1174/ | LeetCode mirror | delivery table, immediate order definition, first-order percentage, MIN subquery and RANK approaches |
| pandas pivot_table | https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html | official docs | aggfunc default mean, dropna default True drops NaN keys and all-NaN columns, observed default True (3.0.0), fill_value, margins |
| pandas crosstab | https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html | official docs | normalize all/index/columns, margins, dropna and empty categories; no normalize example on the page |
| Basedash DAU/WAU/MAU pitfalls | https://www.basedash.com/blog/dau-wau-mau-how-to-measure-active-users-without-fooling-yourself | vendor guide | loose active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users, mismatched stickiness inputs |
| LearnSQL SQL metrics in real interviews | https://learnsql.com/blog/sql-metrics-real-interviews | blog (author's own 11 interviews, no questions published) | metric patterns: breakdown, ratio, KPI, rank, running total, moving average, growth; pitfalls: grain, inflating joins, division by zero |
| letsdatascience e-commerce marketplace SQL | https://letsdatascience.com/blog/sql-interview-questions-ecommerce-marketplace | prep list (says "patterns that candidates have reported", no company claims) | repeat purchase rate, checkout funnel, cart abandonment, session funnel with 30-minute limit, top products by category, fan-out and grain pitfalls; GMV, AOV, cancellation and take rate not in it |
| StrataScratch product analytics blog | https://www.stratascratch.com/blog/product-analytics-data-scientist-interview-questions | practice-site blog | five example titles (Meta session time, Airbnb review score, Amazon lowest priced orders, Meta Messenger, Salesforce user growth rate); none labelled candidate-reported |

## Search results only (snippets, not opened)
- Funnel and DAU/MAU: datadriven.io data analyst questions, querio, ai2sql, prachub concept page, Quadratic funnel post (7-day window anchored on earliest start event), ByteHouse finderFunnel docs, oneuptime ClickHouse DAU/WAU/MAU and stickiness posts (window over daily rows; assumes a gap-free spine), Swace rolling insights (snippet looked buggy; not used), pmtoolkit, Adobe community on rolling stickiness.
- LeetCode mirrors for 1633 (doocs, Medium, velog: distinct registered users over all users, rounded to 2, ordered by percentage desc then contest_id) and 262 (doocs, tencent, velog, grandyang: daily cancellation rate, both client and driver unbanned, join Users twice). leetcode.com pages for 1174 and 1633 appeared in results but were not opened.
- Attribution: Cometly multi-touch SQL, oneuptime ClickHouse attribution, RisingWave, Adobe and Amplitude docs, Parse.ly (linear = equal credit, first touch = first touch in lookback window).
- SRM: abtestly, PracHub SRM guide, Statsig, MetricGate, singhajit glossary (chi-square goodness of fit on distinct-user counts; thresholds such as p < 0.001, 0.0005, 0.0001 vary by team).
- Search metrics: Elastic ES|QL click tracking, oneuptime ClickHouse search analytics, Algolia, SearchStax, Coveo, Adobe (CTR as searches with a click, zero-result rate, average click position, MRR).
- Company guides: Interview Query Swiggy and Paytm guides, AmbitionBox, Naukri Code360 (searched for Indian product companies; results were general SQL-heavy loop descriptions, nothing specific to funnels or cancellation rates; no Flipkart or Zomato result). Not relied on.
- DataLemur, Interview Query product-metrics article, dataford: searched; the specific Facebook MAU and CTR problems were not found, so no claim is made about them.
- Scribd uploads (SQL, SQL Hard Interview Question, LeetCode SQL Questions With Solutions): unattributed; not used.

## Fetch status
- No fetch failed in this part. Nothing executed beyond web research; DuckDB not checked.

## Provenance of the questions
- Source-supported: step counts and conversion, strict vs any-order, time windows (PracHub, Quadratic), DAU/WAU/MAU pitfalls (Basedash), 1174, 1633, 262-style cancellation, repeat purchase rate, cart abandonment, top products per category, attribution models, SRM as counts, search metrics, pandas pivot_table/crosstab behaviours.
- Expert gap-check (no source found): denominator comparison, GMV/AOV/ARPU/ARPPU definitions, net revenue fan-out, refund and cancellation rate, activation within N days, experiment arm tables, share and growth contribution, dashboard reconciliation, new/returning/resurrected, LTV to date, notification funnel, engagement deciles, KPI table, skipped steps, incomplete periods, bots and NULL attribution, dedup, revenue per active user, funnel lag, contamination, SQL-vs-pandas table.
- Candidate-reported: none.
- Boundaries: Part 3 scalar subquery, Part 4 NTILE and ranking, Part 5 running totals and LAG, Part 6 retention and cohorts, Part 7 sessions, Book 1/6 statistics and metric design.
- Question index: B3P08 rows use Part column 8; appended once (45 rows).

## Unverified; Wave B must hedge or run
- Exact LeetCode 1174, 1633 and 262 statements, output order and sample outputs: snippets and one mirror only.
- Benchmarks such as DAU/MAU above 20 percent healthy or 37 percent average (vendor heuristics, cited in snippets): do not state as facts.
- SRM thresholds (0.001, 0.0005, 0.0001 differ by vendor): pointer only; no p-value in this part.
- SQLite 3.45.1 specifics to run: ROUND half away from zero vs Python round half-to-even, integer division, power/exp availability (math functions depend on how Python's SQLite was compiled; a fallback is needed for time decay), no MEDIAN, recursive-CTE date spine, ROW_NUMBER tie handling, datetime(x, '+7 days') versus unixepoch arithmetic.
- pandas 3.0.5: pivot_table dropna and observed defaults, crosstab normalize with NaN keys, value_counts dropna, nunique with NaN, groupby dropna, merge on NaN keys, cumulative-funnel idioms: run, do not assume. rolling().nunique absence: run to confirm.
- Other engines (Postgres DATE_TRUNC, generate_series, FILTER, percentile_cont, MySQL DATEDIFF, BigQuery COUNTIF, Snowflake QUALIFY): general knowledge, not executed.
- Apple Mail Privacy Protection prefetch inflating opens (used in the notification question): general knowledge, not sourced here; hedge.
