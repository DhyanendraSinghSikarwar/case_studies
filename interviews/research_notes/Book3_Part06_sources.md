# Book 3 Part 6 Sources & research notes (Date/time: retention, cohorts, MoM/YoY)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; every source is documentation, a practice-site page, a prep guide or a search snippet. Final count: 45 questions (3-star 18, 2-star 16, 1-star 11).

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| SQLite date and time functions | https://www.sqlite.org/lang_datefunc.html | official docs (lists codes "as of 3.46.0"; mentions 3.54.0 additions) | functions date/time/datetime/julianday/unixepoch/strftime/timediff; strftime codes incl. %W, %U, %V, %G, %g, %u, %w, %j, %J, %s, %f; modifiers (N days/months/years, start of, weekday N, unixepoch, julianday, auto, localtime, utc, subsec, ceiling/floor); +1 month overflow rule; 'auto' caveat for first 63 days of 1970; localtime uses the host zone; no leap seconds |
| pandas time series user guide | https://pandas.pydata.org/docs/user_guide/timeseries.html | official docs (first 100000 of 167306 characters read; resample, Grouper, tz_localize and DateOffset(months) sections were truncated) | to_datetime errors/format/dayfirst, pandas 3 'us' default unit, Timestamp vs Period, date_range/bdate_range (weekmask, holidays with freq 'C'), anchored offsets W-SUN/W-MON/QE-DEC/YE-JUN, DateOffset vs Timedelta across DST, tz_localize/tz_convert example, ME alias (M gone for offsets, still used for Period) |
| pandas DataFrame.resample | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html | official docs (page showed pandas 3.1.0 dev) | closed/label default left except ME, YE, QE, BME, BA, BQE, W (right); origin/offset affect only Tick and naive-day frequencies; group_keys default False since 2.0; W-MON and MS behaviour only inferred, to be run |
| PracHub compute cohort retention rate | https://prachub.com/coding-questions/compute-cohort-retention-rate | practice-site listing | schema users(user_id, signup_ts), user_activity(user_id, activity_ts, event_name); retained in month k if any activity in the calendar month k after cohort month; k = 0..6; output cohort_month, months_since_signup, cohort_size, retained_users, retention_rate; tagged Intuit, Data Scientist, technical screen, no primary source cited (unverified, site-reported) |
| DataDriven monthly cohort retention ("The Slow Fade") | https://datadriven.io/interview/monthly_cohort_retention | practice-site mock interview | signup-month cohorts, share with at least one session from signup through December, output cohort, months since signup, active share; no schema given, no company label, medium, L4 |

## Fetch failed
- Dataford 'structure retention cohort analysis': HTTP 429. Level Up Gitconnected 'Master SQL retention analysis': HTTP 403. Their content is from search snippets only.

## Search results only (snippets, not opened)
- Cohort retention prep: Dataford 'joins for retention rates' (Zomato-style, retention by first-order month and restaurant city, delivered orders only, months 0 to 2), PracHub 'Monthly Cohort Retention' (Amazon Data Scientist technical screen tag, unverified), letsdatascience cohort guide (states it does not claim proprietary company questions; stresses precise definition and preserving the cohort denominator), basedash and Level Up guides (cohort by first event month; day-7 retention asked as 'for users who signed up in January'; first-purchase cohorts drop never-purchasers; partial current periods).
- Retention definitions: GoPractice, Linkrunner glossary and docs, Metricgate: classic day N (exactly day N), cumulative (within days 1..N), rolling (on or after N, unbounded, keeps rising, cannot be reported for immature cohorts). Linkrunner/Metricgate are the main sources for the 'unbounded' framing; no independent standard found.
- LeetCode 550 Game Play Analysis IV (fraction of players who log in the day after first login, rounded to 2 decimals; sample 0.33), 1193 Monthly Transactions I (month, country, counts and amounts, DATE_FORMAT, conditional aggregation), 197 Rising Temperature (higher than previous day), 262 Trips and Users (cancellation rate of unbanned users, 2013-10-01 to 2013-10-03; official rounding and output not seen). Statements from snippets and third-party write-ups; LeetCode pages not opened.
- Date spine: Galaxy glossary on cohort churn (spine of periods then join activity); LinkedIn '25 scenario-based time series SQL questions' (topic list only, no queries). No source found for MoM/YoY with missing months or generate_series; those questions are expert gap-checks.
- Zomato-style MoM with LAG on an orders table (practice sets seen in snippets); Flipkart/Swiggy-specific questions: none found. A site's claim of 'real Amazon, Flipkart and Google interviews' has no primary source and was not used.

## Quick checks I ran on this machine (SQLite 3.45.1, pandas 3.0.5), for Wave B to reproduce
- strftime('%W') works (2024-12-30 gave 53); %U, %V, %G, %g return NULL; %w, %u, %j, %J, %s, %e, %k, %l, %p, %P, %I, %f, %F, %R, %T work.
- date('2023-01-31','+1 month') = 2023-03-03; the 'floor' modifier returns NULL (not supported in 3.45.1); 'end of month' returns NULL; date(x,'weekday -1') returns NULL; date(x,'weekday 1') and positive N work; date(x,'start of month','+1 month','-1 day') works; unixepoch() and timediff() exist; datetime(x,'localtime') ran (host zone dependent); datetime('2024-03-10T12:00:00+05:30') returns 06:30:00 UTC.
- DuckDB is not installed; nothing executed outside SQLite and pandas.
- The Python sqlite3 library version is the one that matters; the docs page describes 3.46 and later features that this build lacks.

## Provenance of the questions
- Documentation-supported: storing dates, truncation, extraction, week conventions, month arithmetic, time zones, unix/subsec, pandas resample/Grouper/DateOffset/tz, business-day calendars.
- Guide- or practice-page-supported: cohort assignment, retention counts and percentages, day-N definitions, LeetCode 550, 1193, 197, 262, date spine for missing periods, MoM with LAG.
- Expert gap-check only: new versus returning, MAU/WAU counting, MoM retention (both months), churn and resurrection, YoY with missing months, fiscal year and fiscal YoY, MTD versus prior MTD, seasonality, subscriptions active per month, calendar table, late-arriving data, cohort by segment, cohort LTV, DST day, ISO week, tenure survival, range joins, performance, fault-finding drill, dialect map.
- Candidate-reported: none (the Intuit and Amazon tags are third-party-site claims).
- Boundaries: Part 5 owns LAG and running totals (cross-referenced in MoM, LTV), Part 7 owns streaks and islands, Part 8 owns DAU/MAU design and funnels, Part 11 owns execution plans.
- Question index: B3P06 rows use Part column 6.

## Unverified; Wave B must hedge or run
- All SQLite results above on 3.45.1 only; the docs' 3.46/3.54 features (floor/ceiling, end of month, negative weekday, ISO %V/%G/%U) are NOT available here: run, label as newer-version only, and use emulation (date(d,'-3 days','weekday 4') for the ISO year).
- 'localtime' modifier output depends on the host TZ; do not print it as a result without stating the host zone.
- pandas: resample W-MON/MS closed/label defaults (inferred from docs); dt.floor('MS') error type; dt.to_period('Q-MAR') and qyear; groupby dropping NaT keys; pct_change(12) after reindex; DateOffset month clipping; tz_localize error class names and messages; bdate_range freq='C' with holidays; np.busday_count; resample on tz-aware DST days (23/25 buckets); merge_asof use. Run on pandas 3.0.5.
- Partial-string indexing df.loc['2024-01-01':'2024-01-31'] inclusive of the last whole day (general knowledge, run).
- Other engines: PostgreSQL/MySQL/BigQuery/Snowflake/SQL Server date functions (DATE_TRUNC, DATEDIFF argument order, DATE_ADD/INTERVAL, generate_series, AGE, TIMESTAMP_TRUNC, DATEADD), fiscal-quarter options: general knowledge, PostgreSQL date/time docs not opened; hedge as 'not executed'.
- LeetCode 550/1193/197/262 exact statements, rounding and output order (snippets only); Intuit/Amazon/Zomato attributions unverified.
- India fiscal year April to March: general knowledge, not looked up.
