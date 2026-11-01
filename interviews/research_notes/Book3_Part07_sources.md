# Book 3 Part 7 Sources & research notes (Gaps and islands, streaks, sessionization)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; every source is a practice-site page, vendor tutorial, prep guide, documentation page or search snippet. Final count: 40 questions (3-star 17, 2-star 14, 1-star 9).

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| techinterview.org SQL interview patterns | https://www.techinterview.org/post/3233476262/sql-interview-question-patterns/?format=md | prep guide | pattern list: longest login streak, ranges of missing invoice numbers, consecutive available seats, current streak (the group containing today), 30 minute sessions, time between consecutive purchases; mentions Meta and an unnamed payments company only as examples of demanding SQL rounds, not as reports |
| DataVidhya gaps and islands | https://datavidhya.com/learn/sql/interview-patterns/gaps-and-islands | prep lesson (intro only; rest paywalled) | ROW_NUMBER subtraction trick; sidebar problem titles only |
| Dataiku sessionization tutorial | https://developer.dataiku.com/latest/tutorials/data-engineering/sessionization/index.html | vendor tutorial | LAG gap, CASE flag, running SUM; 30 minute timeout; uses >= (exactly 30 minutes starts a new session); first event not flagged; no tie handling |
| oneuptime merge overlapping intervals | https://oneuptime.com/blog/post/2026-03-31-clickhouse-merge-overlapping-intervals/markdown | engineering blog (ClickHouse-flavoured) | running MAX(end) over ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING, new-group flag when start > running max, cumulative SUM key, min/max per group; strict > means touching intervals merge |
| DataDriven 'The Overlap' | https://datadriven.io/problems/the_overlap.md | practice-site problem (Python, hard, L5, no company) | merge overlapping or touching windows; contained window must not shrink the end |
| pandas Series.shift | https://pandas.pydata.org/docs/reference/api/pandas.Series.shift.html | official docs (page showed 3.1.0 dev) | periods, fill_value, integer columns upcast to float64 with default fill, NaT for datetimes |

## Fetch failed
- leetcode.com problem pages for 601 and 1285: HTTP 403. SQLite windowfunctions.html: HTTP 503 (second time; Part 5 note said the same). Nothing relied on from these pages.

## Search results only (snippets, not opened)
- Gaps and islands guides: CoddyKit 'detecting consecutive calendar days' and 'longest streak per user', DataVidhya practice, DevPath sql-interview-patterns, a Medium 'Google advanced SQL interview question walkthrough' (title only; no verification of any company claim): date minus ROW_NUMBER, group by user and key, MIN/MAX/COUNT; several assume one login per day and say to dedupe first.
- Sessionization: Cube event analytics, DevGenius 'Pattern 014', a LinkedIn interview post, datasciencecentral, Scribd guides: LAG, flag at gap >= or > 30 minutes, running SUM; sources differ on the operator, and one suggests an event id tie-breaker.
- Intervals: oneuptime ClickHouse maxIntersections (aggregate, ClickHouse-specific), a Medium 'merge overlapping date ranges' guide (LAG-and-group-counter), a 2009 PostgreSQL mailing-list thread on simultaneous users (no settled answer), Itzik Ben-Gan Packing Date Intervals and single-scan packing articles (itprotoday, red-gate, SQL Server MVP Deep Dives ch. 5). The +1/-1 sweep with ends before starts at ties is general knowledge, not from these results.
- LeetCode mirrors (doocs, walkccc, talentd): 180 Consecutive Numbers (at least three times in a row, logs(id, num), any order), 601 Human Traffic of Stadium (three or more consecutive ids with people >= 100, ordered by visit_date; ids consecutive, dates may skip), 603 Consecutive Available Seats (premium; free seats adjacent to another free seat, ordered by seat_id), 1454 Active Users (premium; five or more consecutive days; Logins may contain duplicates; follow-up general N), 1285 Find the Start and End Number of Continuous Ranges (recalled; statement not seen in results), 2173 Longest Winning Streak (matches with Win/Draw/Lose; sample longest streaks 3, 0, 1; players without wins get 0). A Hello Interview result labelled 2173 is a different problem and was ignored.
- Oracle SQL blog 'longest and current consecutive streaks' (snippet only).
- pandas run-grouping: Stack Overflow / Towards Data Science / gurubase snippets for (s != s.shift()).cumsum() and diff().ne(0).cumsum(), groupby agg first and size.
- StrataScratch and DataLemur pages: searched indirectly, no gaps-and-islands page opened; not relied on.

## Quick checks I ran on this machine
- SQLite 3.45.1: `IS NOT` and `IS DISTINCT FROM` both work (1 returned for the three probes). Nothing else executed in Wave A; DuckDB not checked.

## Provenance of the questions
- Source-supported: islands by date/id minus ROW_NUMBER, longest streak, current streak, at-least-N (1454), 180, 601, 603, 1285, 2173, session flag plus running SUM, 30 minute timeout, running-MAX interval merge, pandas shift/cumsum run key.
- Expert gap-check (no source found): duplicate-date debugging, stock up-streaks, reset-by-condition, bounce sessions and midnight crossing, back-to-back dedup, state-change NULL handling, booking conflicts, working-day attendance streaks, SCD collapse, subscription snapshots, coverage gaps, zero/increase runs, hot streaks, rolling checks, SQL-vs-pandas table, time-zone streaks, room availability.
- Candidate-reported: none.
- Boundaries: Part 4 ranking, Part 5 running totals and LAG/LEAD basics, Part 6 retention and cohorts, Part 8 funnels, Part 9 recursive CTEs (reset by threshold is a pointer).
- Question index: B3P07 rows use Part column 7.

## Unverified; Wave B must hedge or run
- All SQL on SQLite 3.45.1 only; other engines (PostgreSQL date minus integer, DATEDIFF, generate_series, IS DISTINCT FROM, interval syntax, MySQL 5.7 lacking window functions as noted on LeetCode 180) are general knowledge, not executed.
- Exact LeetCode statements, output order and sample outputs (snippets only; 603 and 1454 are premium; 1285 not seen).
- Whether exactly 30 minutes starts a new session: sources disagree (Dataiku uses >=); present both and state the assumption.
- pandas 3.0.5: sort_values stability and default sort kind, diff on datetime then .dt.days, groupby dropping NaN keys, NaN != NaN, shift upcasting integers to float, rolling(3).min() with min_periods, cummax inside groupby, concat sort ties, itertools.groupby: run, do not assume.
- DST behaviour for streaks (hedged; SQLite has no zones), julianday precision for timestamps (floating point) versus unixepoch integer seconds: run.
- Whether SQLite 3.45.1 accepts ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING with MAX (expected yes; run).
- Recursive CTE date spine syntax runs on SQLite (Part 6 used it); depth in Part 9.
