P = {}

P[23] = dict(
say="Join `users` twice, once as client and once as driver, keep only trips where both are unbanned, then per `request_date` divide cancelled trips (any status other than completed) by all qualifying trips, using `* 1.0` so SQLite does not do integer division; a day with no qualifying trip has no group, so it simply does not appear.",
schema_note="twelve trips, seven users, `banned` stored as 'Yes' or 'No' (the LeetCode 262 convention; I state that as an assumption). Trip 3 has a banned client, trip 4 a banned driver, trip 9 is the only trip on 2024-03-03 and it involves two banned users, trip 12 has a client id (99) that is not in `users`. The `city` column is carried but not used.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` in the Code block (two joins to `users`, the ban test inside each join so it is applied to the right side):",
sqls=["SQL_MAIN"],
sqlafter="The wrong version (`SQL_WRONG` in the Code block) joins `users` once, for the client only. It is printed in the output so you can see the number move.",
pdnote="the same logic, shown once here and identical to the Code block. Two merges against the unbanned users, one renamed to `client_id` and one to `driver_id`:",
example="""- Day 2024-03-01 has five trips. Trip 3 (banned client 3) and trip 4 (banned driver 6) drop out, leaving trips 1, 2 and 5: one completed, one cancelled by the driver, one completed. 3 requests, 1 cancellation, rate 1/3 = 0.33, all of it driver-side (0.33 by driver, 0.00 by client).
- Day 2024-03-02 has three qualifying trips (6, 7, 8): two are cancelled by the client, so 2/3 = 0.67 and the split is 0.00 driver, 0.67 client.
- Day 2024-03-03 has one trip and both of its users are banned, so zero qualifying trips and no output row. Trip 12 on 2024-03-04 has a client id that is not in `users`; an inner join drops it, so that day has 2 qualifying trips and rate 0.00.
- Wrong version (client filter only): on 2024-03-01 the banned-driver trip 4 stays in, giving 4 requests and 2 cancellations, 0.50 instead of 0.33. Days where only a driver is banned are the ones that move.""",
edge="""- A day with zero qualifying trips has no group, so no row and no division by zero. If the report must show every day with 0 or NULL, start from a date list and LEFT JOIN, and say which you want.
- A user id missing from `users` (trip 12): with inner joins the trip is dropped; with a LEFT JOIN plus `banned = 'No'` in the WHERE it is also dropped; with `banned <> 'Yes'` it would be kept. Pick and state the rule.
- `banned` NULL: `banned = 'No'` is not true for NULL, so the user is treated as not provably unbanned and the trip is dropped; the opposite rule is `COALESCE(banned,'No') = 'No'`.
- Rounding: values here are 1/3 and 2/3, no exact half; for a value like 0.125 SQLite ROUND and pandas round disagree (see Q31).""",
explain="""- Both parties must be unbanned: banning is a property of a user, a trip has two users, and the question's rule needs both. Filtering only the client leaves trips with a banned driver in the numerator and denominator.
- The denominator is all qualifying requests (completed plus both cancel types), not only completed trips.
- `SUM(status <> 'completed')` works in SQLite because a comparison is 0 or 1; in Postgres you would write `COUNT(*) FILTER (WHERE ...)` or `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`, in BigQuery `COUNTIF(...)` (not executed here). The CASE form is portable.
- Put the ban condition in the join (`ON ... AND c.banned = 'No'`) for an inner join; it is equivalent to a WHERE there. With a LEFT JOIN it must stay in the WHERE or the row survives with NULLs.
- Round the final ratio only; do not round counts first.""",
fu="""- Also show the days with zero qualifying trips? Generate a date spine (recursive CTE, see Q33) and LEFT JOIN the daily result, returning NULL or 0 as agreed.
- Cancellation rate by city as well? Add `t.city` to the GROUP BY; the double join is unchanged.
- Split by who cancelled but over cancellations only? Use `NULLIF(SUM(status <> 'completed'), 0)` as the denominator; Q24 does this for a marketplace.""",
mist="""- Filtering only the client side (shown in the output).
- Joining `users` once and checking `client_id` and `driver_id` against the same alias.
- Integer division: `SUM(...) / COUNT(*)` gives 0 in SQLite when the ratio is below 1; multiply by 1.0 first.
- Putting the ban filter in WHERE after a LEFT JOIN and then wondering why unmatched trips vanish (or the reverse).
- Counting only 'cancelled_by_client' as cancellations.""",
)

P[24] = dict(
say="Per city: fill rate is completed over all requests (including no_driver_found), cancellation share is rider-cancelled and driver-cancelled over cancellations, rides per active driver is completed rides over distinct drivers with an assigned request, and take rate is summed commission over summed fare on completed rides only; every ratio gets `NULLIF` so an empty denominator is NULL, not an error.",
schema_note="thirteen requests in three cities. Mumbai has all four statuses and one rider cancellation after a driver was assigned (driver 12). Pune has two completed rides by the same driver. Delhi has only `no_driver_found`, so cancellations, active drivers and fare are all zero there. `fare` and `commission` are NULL on rows that did not complete. All fares and commissions are made-up toy values.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` in the Code block:",
sqls=["SQL_MAIN"],
sqlafter="",
pdnote="the same logic as one function (`nz` turns a zero denominator into NaN, the counterpart of `NULLIF`):",
example="""- Mumbai: 7 requests, 3 completed (requests 1, 2, 6) so fill rate 3/7 = 0.43. Cancellations are requests 3 (driver), 4 (rider) and 7 (rider): 3 in all, rider share 2/3 = 0.67, driver share 1/3 = 0.33. The request with `no_driver_found` is in the fill-rate denominator but not among the cancellations.
- Active drivers in Mumbai are the distinct non-NULL driver ids: 10, 11, 12, so 3. Rides per active driver is 3 completed / 3 = 1.0. `COUNT(DISTINCT driver_id)` ignores the two NULL rows by itself.
- Take rate: commissions 40 + 20 + 48 = 108 over fares 200 + 100 + 300 = 600, 0.18.
- Pune: fill 2/4 = 0.50, one cancellation (rider), so shares 1.00 and 0.00, one active driver (20), 2.0 rides per driver, take rate 80/400 = 0.20.
- Delhi: fill 0.00, no cancellations, no drivers, no fare: the four ratios are NULL (NaN in pandas), not 0 and not an error.""",
edge="""- Zero denominators give NULL here. In SQLite `x / 0` also returns NULL rather than raising (Q31 runs it), but PostgreSQL and others raise a division error (not executed here), so `NULLIF` is the portable habit.
- Driver NULL on a cancelled_by_rider row (rider left before assignment, request 4) versus a driver assigned (request 7): the first does not count toward active drivers, the second does. That is a business rule to confirm.
- A driver with one completed ride and one driver-cancelled request is one active driver; counting rows instead of distinct ids would double count.
- Drivers who were online but never got a request are not in this table at all, so they cannot be in the denominator; that needs a supply table.""",
explain="""- no_driver_found belongs in the fill-rate denominator because fill rate measures how much of the demand you served; a request nobody could serve is the clearest failure of supply. It is not a cancellation: nobody cancelled, the platform failed to match.
- Cancellation share by side is a share of cancellations here (rider plus driver = 1). If the interviewer means each side's cancellations over all requests, change the denominator to `COUNT(*)`; say which you used.
- Rides per active driver uses distinct drivers with at least one assigned request (3 in Mumbai). The alternatives are drivers with a completed ride (2 in Mumbai, which would give 1.5) or drivers logged in from a supply table. All are defensible; the choice changes the number, so name it.
- Take rate is a ratio of sums over completed rides, not an average of per-ride ratios; the average of ratios weights a 100 fare ride like a 1000 fare ride.
- Metric design (is fill rate the right goal?) belongs to Book 6; this answer stays on the SQL.""",
fu="""- Per day or per hour instead of per city? Add the truncated `request_ts` to the GROUP BY; with few rows per bucket the ratios get noisy.
- Why not average per-ride commission rates? Because that is a different, unweighted number (see above).
- How would you split cancellations before and after driver assignment? Use `driver_id IS NULL` on cancelled_by_rider rows as the proxy and say it is a proxy.""",
mist="""- Putting `no_driver_found` in the cancellation numerator.
- Dividing rides by all drivers in the company instead of drivers active in that city and period.
- Summing fares over all rows (including cancelled) for the take-rate denominator.
- Averaging per-ride take rates.
- Dividing by zero instead of `NULLIF` for a city with no completed rides.""",
)

P[25] = dict(
say="Decide the grain first: CTR is searches that got at least one click over searches, so mark each search with `EXISTS` on `clicks` (one row per search, no fan-out) and average that flag per day; clicks per search is a different number and joining first inflates it.",
schema_note="eight searches over three days and six clicks. Search 1 gets two clicks (positions 1 and 3), search 2 has zero results so it cannot be clicked, search 7 has `result_count` NULL (a logging gap, not the same as zero), search 8 is the only search on 2024-03-03 and has no click at all.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` (daily metrics) and `SQL_POS` (click-position distribution) in the Code block. `SQL_MAIN`:",
sqls=["SQL_MAIN", "SQL_POS"],
sqlafter="`SQL_WRONG` in the Code block is the join-first version, printed in the output for comparison.",
pdnote="both results come from one function, identical to the Code block (`isin` is the `EXISTS`; `pd.cut` makes the position buckets):",
example="""- 2024-03-01: four searches (1 to 4). Search 1 has two clicks, search 4 has one, searches 2 and 3 none, so searches with a click = 2 and CTR = 2/4 = 0.50. One of the four has `result_count = 0`, zero-result rate 0.25.
- Joining first: search 1 becomes two rows, so the joined table has 5 rows for 4 searches. Counting clicks over true searches gives 3/4 = 0.75, counting click rows over joined rows gives 3/5 = 0.60. Neither is the CTR. On 2024-03-02 the clicks-over-searches version reaches 1.00 although one search in three got no click.
- Zero-result search 2 stays in the denominator (it is a search that could not succeed); the search with `result_count` NULL is in the denominator and not counted as zero-result, so 2024-03-02 shows zero-result rate 0.00.
- Positions on 2024-03-01: clicked positions 1, 3, 2 give 33.33 percent each for buckets 1, 2 and 3 and 0 for the others. On 2024-03-02 positions 1, 12, 5 land in buckets 1, 11+ and 4-10 at 33.33 each. On 2024-03-03 there are no clicks, so the percentages are NULL (NaN in pandas), not 0.""",
edge="""- Zero-result searches cannot get a click, so they pull CTR down. Many teams also report CTR over searches that returned results; that is `WHERE result_count > 0` on the denominator and numerator, stated explicitly.
- NULL `result_count` is unknown; `result_count = 0` is false for it, so it is not zero-result.
- A day with searches but no clicks: CTR 0.00 (the flag is 0), positions NaN.
- Click rows whose `search_id` is not in `searches` are ignored by the `EXISTS` form and by the inner merge in the position table.
- Buckets with no clicks need the `CROSS JOIN` against the bucket list, otherwise the row is absent rather than 0.""",
explain="""- Two different grains: CTR is per search, position distribution is per click. Do not put them in one join.
- `EXISTS` (or `COUNT(DISTINCT search_id)` after a join) keeps one row per search. `EXISTS` is cheaper because it can stop at the first click.
- Percent of clicks uses clicks as the denominator, so a search with three clicks weighs three times in that table; that is intended and worth saying.
- Click-position metrics such as mean click position or MRR need a decision on searches with no click; not computed here.
- Dialect: the same shape works in Postgres and MySQL; BigQuery would use `COUNTIF` and `DATE(search_ts)` (not executed here).""",
fu="""- CTR by query? Group by `query`; low volume per query makes it noisy, so show the search count next to it.
- First-click position only? Take `MIN(position)` per search first, then bucket.
- Abandonment (no click and no refinement)? Needs a session notion, see Part 7.""",
mist="""- Joining searches to clicks and counting rows (shown in the output).
- Using `COUNT(DISTINCT click_id) / COUNT(DISTINCT search_id)`, which is clicks per search, not CTR.
- Treating NULL `result_count` as zero results.
- Dropping the zero-result searches from the denominator without saying so.
- Leaving out zero-count buckets so the distribution does not show them.""",
)

P[26] = dict(
say="Collapse opens and clicks to one flag per send with `EXISTS`, then count sends: open rate is opened sends over sent, click-to-open is clicked sends over opened sends, and click-through is clicked sends over sent; raw event counts overstate every rate when a send is opened or clicked several times.",
schema_note="eight sends over two channels (`push` and `email`) to three users. Send 1 has two open rows, send 5 has three open rows and two click rows, so event counts exceed send counts. Sends 3, 6 and 8 have a click and no open row. Send 4 has no open and no click. All data is made up.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` in the Code block (`SQL_RAW` for the wrong raw-count rates and `SQL_USER` for the user-level open rate are in the Code block too):",
sqls=["SQL_MAIN", "SQL_USER"],
sqlafter="",
pdnote="the send-level function, identical to the Code block:",
example="""- Push has sends 1 to 4. Opened: sends 1 (two open rows) and 2, so unique opens 2. Clicked: sends 1 and 3, unique clicks 2. Open rate 2/4 = 0.50, CTOR 2/2 = 1.00, CTR over sent 2/4 = 0.50. Send 3 is a click with no open row.
- Email has sends 5 to 8. Opened: sends 5 (three open rows) and 7, so 2. Clicked: sends 5, 6 and 8, so 3. Open rate 2/4 = 0.50, CTR 3/4 = 0.75, CTOR 3/2 = 1.50, which is above 100 percent because two of the three clicked sends (6 and 8) have no open row.
- Restricting CTOR to clicks on sends that were also opened gives 1/2 = 0.50 for email and 1/2 = 0.50 for push; that is the alternative "clean" definition.
- Raw event counts: email has 4 open events and 4 click events for 4 sends, so a raw open rate of 1.00 and a raw click-over-open of 1.00 instead of 0.50 and 1.50; the unit is wrong.
- User level: push went to users 1, 2 and 3; only user 1 opened (both of their sends), so 1/3 = 0.33 users opened against a send-level 0.50. Email is 2/3 = 0.67 at user level against 0.50 at send level.""",
edge="""- A click with no open row: possible when images are blocked (the open pixel never loads), when the open tracking fails, or in push when the app records the tap without an open event. The result is CTOR above 1.
- Apple Mail Privacy Protection: general knowledge, not sourced here and not tested, is that it can preload email content on behalf of the user, which is widely reported to inflate email open counts; treat email open rate as an upper bound and lean on clicks.
- Opens and clicks that arrive before `sent_ts` or for unknown send ids point to a data problem; here they would be ignored by the `EXISTS` form.
- Zero opened sends gives CTOR NULL through `NULLIF`.
- Repeated rows per send (re-opens) are why distinct sends, not rows, are counted.""",
explain="""- Unit: one send is one chance to open. Open rate, CTOR and CTR all count sends, so each send is counted once no matter how many open or click rows it has.
- `EXISTS` per send avoids joining opens and clicks to sends together, which would multiply rows (opens times clicks per send).
- CTOR above 100 percent is a symptom, not a bug in the SQL: the click numerator and the open denominator are measured by different tracking.
- Send-level versus user-level: a user who got two pushes and opened both is two sends opened but one user opened. User-level rates answer 'how many people engaged'; send-level rates answer 'how well does a message perform'.
- Dialect: `EXISTS` and `COUNT(DISTINCT ...)` are portable; BigQuery or Postgres users might prefer `COUNTIF` or `FILTER` (not executed here).""",
fu="""- Which rate do you trust for email? Clicks over sent, because opens may be prefetched; say it is a judgement.
- Per campaign? Group by campaign id; keep the per-send flag CTE.
- Unsubscribes or bounces in the denominator? Define delivered sends and use that as the denominator; bounces are not in this table.""",
mist="""- Dividing event counts (open rows, click rows) by sends.
- Joining sends to opens and to clicks in one query without pre-aggregating.
- Computing CTOR as clicks over sends or opens over clicks.
- Treating CTOR above 1 as a bug and clipping it without explaining.
- Mixing user-level numerators with send-level denominators.""",
)

P[27] = dict(
say="Collapse events to one row per session with flags (`MAX(event_name = ...)`), take the day from the session's first event, then abandonment is cart sessions without a purchase over cart sessions and bounce is sessions with exactly one event over all sessions; the definitions of 'no purchase' and of 'one event' are the two things to state out loud.",
schema_note="fifteen events in nine sessions. Session D has the purchase before the add_to_cart. User 6 adds to cart in session F and buys in a different session G. Session E is a single add_to_cart. Session H has two page views. Session I (2024-03-03) is a single page view and there is no cart session that day.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` in the Code block (literal definition: a cart session is abandoned when it has no purchase anywhere in the session), and `SQL_ORDERED` for the variant where the purchase must come at or after the first add_to_cart:",
sqls=["SQL_MAIN", "SQL_ORDERED"],
sqlafter="",
pdnote="the same logic for the main definition, identical to the Code block:",
example="""- 2024-03-01 has sessions A to E. Cart sessions: A, B, D, E (4). With the literal definition A (bought) and D (bought, earlier) are not abandoned; B and E are, so 2/4 = 0.50.
- With the ordered variant D counts as abandoned (its purchase came before the cart), so 3/4 = 0.75. One session moves the rate by 25 points.
- 2024-03-02: F has a cart and no purchase in F; the purchase is in session G (a different id), so F is abandoned: 1/1 = 1.00. If you stitched sessions per user within a day the answer would differ, but the question says sessions stay separate.
- Bounce on 2024-03-01: session C (one page_view) and session E (one add_to_cart) have exactly one event, so 2/5 = 0.40 under 'one event of any kind'; only C is a single page view, so 1/5 = 0.20 under 'one page_view only'.
- 2024-03-02: G (one purchase) is the only single-event session, 1/3 = 0.33 under the any-event rule and 0 under the page_view rule. H has two page views so it is not a bounce here.
- 2024-03-03: no cart session, so abandonment is NULL (not 0); the one session is a bounce, 1.00.""",
edge="""- No cart sessions on a day: `NULLIF(SUM(has_cart), 0)` returns NULL; reporting 0 would suggest nobody abandoned.
- Sessions that cross midnight belong to the day of their first event (`date(MIN(event_ts))`), not split by day.
- Session id reuse across users or days would merge unrelated rows; assume the id is unique and, if it is not, group by (user_id, session_id).
- Ties on `event_ts` do not matter for these flags except in the ordered variant, where a purchase and a cart at the same timestamp counts as completed (`<` test).
- Bounce is also sometimes defined with time on page; not available here.""",
explain="""- Grain: the rate is a ratio of sessions, so build one row per session first and aggregate that. Counting events gives different, wrong, numbers.
- 'Abandoned' must be defined: literal (no purchase in the session) versus ordered (no purchase after the cart). They differ when purchases can precede carts (for example a re-order flow).
- A purchase in a later session does not rescue the earlier session in this metric; a user-level or time-windowed cart abandonment would, and is a different metric.
- Bounce depends on the event definition: with 'one page_view only' a single `add_to_cart` or `purchase` session is not a bounce; with 'one event of any kind' it is. Many analytics tools define bounce differently again (engagement based); state which one you use.
- Dialect: `MAX(boolean)` as a flag works in SQLite and MySQL; in Postgres use `BOOL_OR(...)` or `MAX(CASE WHEN ... THEN 1 ELSE 0 END)` (not executed here).""",
fu="""- Cart abandonment at user-day level? Group by user and day first, then apply the flags.
- Add checkout steps? That is a funnel; keep the per-session flags and add one flag per step.
- Abandonment value (cart value lost)? Needs cart contents; not in this table.""",
mist="""- Computing abandonment over all sessions instead of cart sessions.
- Counting events, not sessions, in numerator or denominator.
- Not saying whether a purchase before the cart counts.
- Defining bounce by `COUNT(*) = 1` and then reporting it as 'single page_view'.
- Reporting 0 when the denominator is empty.""",
)
