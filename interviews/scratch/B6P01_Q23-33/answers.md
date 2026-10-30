### Q23 ⭐⭐ 🟢 Define success metrics for a referral programme that gives Rs 100 to both sides. List the metrics, the guardrails, and the abuse patterns, and say which number you would present to finance to prove the programme is not just buying users who leave.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** I would show finance one number, the contribution earned per rupee of reward on genuine, incremental users still active at day 90, because that is the only number that shows the programme is not buying users who leave.

**Clarifying questions:**
- When is the Rs 100 paid: at signup, first order, or after a minimum spend? It decides how much abuse we pay for before we can catch it.
- Is there a clawback if the referred user is later flagged or refunds? It caps the loss from fraud.
- What does a user normally cost us through paid channels? We need a benchmark to say "cheap" or "dear".
- Can we hold out a small random slice of users from seeing the offer? Without a holdout we cannot say who would have joined anyway.
- What is a "retained" user for this business (order, session, payment)? The metric has to match how we earn money.

**Approach:**
1. Draw the funnel: invites sent, invites opened, signups, qualified (met the reward rule), rewarded.
2. Split every qualified user into genuine and suspicious using rules (same device, same payment instrument, same address, burst signups, referrer with an unusual number of referrals).
3. Compare genuine referred users with a matched or held-out group on day-30 and day-90 activity, orders and margin.
4. Estimate incrementality: the share of referred users who would not have joined without the offer (from a holdout of users not shown the programme).
5. Put cost, retention, incrementality and margin into one ratio, and compare cost per incremental retained user with the paid-channel cost.

**Metrics:**
| Metric | Definition | Role |
|---|---|---|
| Qualified referral rate | qualified referred users / invites sent | Funnel health |
| Abuse share | flagged qualified users / all qualified users | Guardrail |
| D90 active rate | genuine referred users active on day 90 / genuine referred users | Quality |
| Incrementality | referred users who would not have joined anyway / genuine referred users (holdout estimate) | Causal |
| Cost per incremental D90-active user | total reward cost / (D90-active genuine users x incrementality) | Efficiency |
| **Contribution per Rs of reward** | (incremental D90-active users x 90-day margin per retained user) / total reward cost | **Number for finance** |

Guardrails: abuse share, refund and chargeback rate of referred users, support tickets per referred user, the referred users' share of promo-only orders.

**Risks:**
- Paying on signup rewards fake accounts, not value.
- Referrers are already heavy users, so their friends look good (selection). Compare with a holdout, not with the all-user average.
- Counting rewards as marketing but not as the cost of a discount on the first order (double benefit).
- Day-90 data is late. Use day-30 as a leading read, but label it so.

**What the interviewer scores:**
- Strong: separates genuine from abusive users and uses an incrementality estimate. Weak: reports invites and signups only.
- Strong: picks one finance number with a defined numerator and denominator. Weak: lists ten metrics and no decision.
- Strong: names concrete abuse patterns and a rule for the payout (pay after first order, clawback). Weak: says "monitor fraud".
- Strong: compares with another channel's cost. Weak: gives cost per signup alone.

**Example:** (illustrative numbers) 1,250 users qualify and Rs 100 goes to both sides, so the reward cost is 1,250 x Rs 200 = Rs 2,50,000. Rules flag 250 as abusive (20%), leaving 1,000 genuine. 35% of them are active on day 90, that is 350. A holdout says 60% would not have joined without the offer, so 210 are incremental. Cost per incremental D90-active user is Rs 2,50,000 / 210 = about Rs 1,190. If a retained user is worth Rs 1,500 of margin in 90 days, contribution is Rs 3,15,000, which is Rs 1.26 per rupee of reward.
- Weak: "Cost per qualified user is Rs 200, great, scale it."
- Strong: "Rs 200 per qualified user is really Rs 1,190 per incremental retained user, and it returns Rs 1.26 per rupee, so it pays for itself but with thin headroom, and abuse is 20%."

**Code:**
```python
# Q23 referral programme unit economics (illustrative numbers)
reward_each_side = 100            # Rs per side, paid on qualification
qualified_pairs = 1250            # referred users who met the qualifying rule
abusive = 250                     # flagged as self-referral / fake / device-sharing
genuine = qualified_pairs - abusive
reward_cost = qualified_pairs * 2 * reward_each_side   # paid before detection
d90_active_rate = 0.35            # genuine referred users active on day 90
incrementality = 0.60             # share who would NOT have joined without the offer (holdout estimate)
margin_per_retained_90d = 1500    # Rs contribution per retained user over 90 days (assumed)

d90_active = genuine * d90_active_rate
incremental_active = d90_active * incrementality
cost_per_incr_active = reward_cost / incremental_active
net_contribution = incremental_active * margin_per_retained_90d
ratio = net_contribution / reward_cost

print("genuine referred users:", genuine)
print("reward cost (Rs):", reward_cost)
print("abuse share of qualified:", abusive / qualified_pairs)
print("D90-active genuine:", d90_active)
print("incremental D90-active:", incremental_active)
print("cost per incremental D90-active (Rs):", round(cost_per_incr_active, 1))
print("net contribution (Rs):", net_contribution)
print("contribution per Rs of reward:", round(ratio, 3))

assert genuine == 1000 and reward_cost == 250000
assert abusive / qualified_pairs == 0.2
assert round(d90_active) == 350 and round(incremental_active) == 210
assert round(cost_per_incr_active, 1) == 1190.5
assert net_contribution == 315000 and round(ratio, 2) == 1.26
# naive view that finance would reject: cost per qualified user ignores abuse, retention, incrementality
print("naive cost per qualified pair (Rs):", reward_cost / qualified_pairs)
assert reward_cost / qualified_pairs == 200
```

**Output (my run):**
```text
genuine referred users: 1000
reward cost (Rs): 250000
abuse share of qualified: 0.2
D90-active genuine: 350.0
incremental D90-active: 210.0
cost per incremental D90-active (Rs): 1190.5
net contribution (Rs): 315000.0
contribution per Rs of reward: 1.26
naive cost per qualified pair (Rs): 200.0
```

**Follow-ups:**
- How do you get incrementality without a holdout? Compare against users with similar tenure and activity who did not get the offer, and say that it is weaker. See Book 1 Part 10 Q24 (holdout / long-term holdout) for the idea.
- Which side of the reward matters more? Test the split: referrer-only, referee-only and both. Costs differ and so do the abuse patterns.
- What if D90 is positive but the margin number is a guess? Show the ratio at a low, base and high margin and say where it breaks even.

**Common mistakes:** Presenting signups as success. Using cost per signup. Ignoring abuse in the denominator. No holdout. Using the all-users retention as the comparison.

### Q24 ⭐⭐ 🟢 Email open rate jumped from 20% to 45% overnight with no change in content. Explain what you would suspect first, how you would check it using downstream metrics such as clicks and conversions, and what you would do to the metric definition.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** A jump from 20% to 45% overnight with no content change is almost always a measurement change, most likely mail clients pre-fetching the tracking pixel, so I would not celebrate, I would check clicks and rebuild the metric.

**Clarifying questions:**
- Did anything change on the sending side (new email platform, new tracking domain, new image-loading setup)? A vendor or template change can move opens by itself.
- Is the jump across all audiences or in some mail clients or domains? A localised jump points to the client, not to the people.
- Did clicks, conversions and unsubscribes move too? These do not depend on the pixel.
- Is it the open rate on delivered or on sent emails, and did the denominator change? A bounce-handling change also moves it.
- Is this campaign-level or one sender? It tells me whether it is a pipeline-wide issue.

**Approach:**
1. Suspect the measurement first. An "open" is only a request for a tiny image. Some mail clients and privacy features fetch images automatically (Apple Mail Privacy Protection since 2021 is the best-known example), so a machine can create an open with no human reading.
2. Check downstream metrics. Clicks, click-to-open rate, conversions and unsubscribes should rise if people truly engaged more. If they are flat, the extra opens are not people.
3. Segment opens by mail client, user agent, IP ranges, and time between send and open. Machine opens come within seconds of delivery and from a small set of proxy addresses.
4. Compare with a client that does not pre-fetch. If its open rate is unchanged, the jump lives in the pre-fetching segment.
5. Fix the definition: report click rate per delivered email as the headline, keep opens only as a directional signal, exclude known proxy opens where possible, and annotate the date.

**Metrics:**
- Open rate = unique opens / delivered emails (inflated by machine opens).
- Click rate = unique clicks / delivered emails (not pixel-based).
- Click-to-open rate = unique clicks / unique opens (falls when opens are inflated).
- Conversion rate per delivered email = conversions attributed to the email / delivered emails.
- Guardrails: unsubscribe rate, spam-complaint rate, bounce rate.

**Risks:**
- A real change can coincide (a better subject line). Segment before you decide.
- Excluding proxy opens removes some real opens too. Say that the new series is a different, smaller measure.
- Old open-rate-based rules (send-time optimisation, "engaged user" lists) can now be wrong. List them.

**What the interviewer scores:**
- Strong: says "suspect measurement before behaviour" and gives one concrete mechanism. Weak: explains the jump as better content.
- Strong: uses downstream metrics that do not rely on the pixel. Weak: checks only the same metric on more cuts.
- Strong: changes the definition and annotates the break. Weak: leaves it as is and reports a win.

**Example:** (illustrative numbers) 100,000 emails, half go to a client that pre-fetches. After the change that client shows a 70% open rate and the other stays at 20%, so the blend is 0.5 x 70% + 0.5 x 20% = 45%. Clicks are 2,000 both before and after (2% of delivered). Opens went from 20,000 to 45,000, so click-to-open fell from 10.0% to 4.4%.
- Weak: "Opens more than doubled, the new subject lines work."
- Strong: "Opens rose 125%, clicks are flat, click-to-open fell from 10% to 4.4% and the clients that do not pre-fetch are unchanged, so this is machine opens, and I will switch the headline to clicks per delivered."

**Code:**
```python
# Q24 open rate 20% -> 45% from machine opens (illustrative numbers)
sends = 100_000
apple_share = 0.5                  # share of sends delivered to a client that pre-fetches the pixel
open_before = {"proxy": 0.20, "other": 0.20}
open_after = {"proxy": 0.70, "other": 0.20}   # proxy opens now include machine opens
click_rate_per_send = 0.02         # unchanged in both groups, both periods

def blended(d):
    return apple_share * d["proxy"] + (1 - apple_share) * d["other"]

ob, oa = blended(open_before), blended(open_after)
opens_b, opens_a = round(ob * sends), round(oa * sends)
ob, oa = round(ob, 4), round(oa, 4)
clicks = round(click_rate_per_send * sends)
ctor_b, ctor_a = clicks / opens_b, clicks / opens_a
print("open rate before/after:", ob, oa)
print("opens before/after:", opens_b, opens_a)
print("clicks (both periods):", clicks)
print("click-to-open before/after:", round(ctor_b, 3), round(ctor_a, 3))
print("open rate non-proxy only, before/after:", open_before["other"], open_after["other"])
assert round(ob, 2) == 0.20 and round(oa, 2) == 0.45
assert opens_b == 20000 and opens_a == 45000
assert clicks == 2000
assert round(ctor_b, 3) == 0.100 and round(ctor_a, 3) == 0.044
assert open_after["other"] == open_before["other"]
# proxy-adjusted metric: count opens only from non-proxy clients, or use clicks per delivered
print("clicks per delivered:", clicks / sends)
assert clicks / sends == 0.02
```

**Output (my run):**
```text
open rate before/after: 0.2 0.45
opens before/after: 20000 45000
clicks (both periods): 2000
click-to-open before/after: 0.1 0.044
open rate non-proxy only, before/after: 0.2 0.2
clicks per delivered: 0.02
```

**Follow-ups:**
- Can you still use opens? As a trend within a client that does not pre-fetch, or as a rough signal, never as a precise level.
- What if clicks also jumped? Then check for link scanners and bots that click links (security gateways), which the same segmentation by user agent and timing would show.

**Common mistakes:** Reporting the jump as a win. Looking only at open rate by segment and not at clicks. Changing the definition without annotating the date, which breaks the trend.

### Q25 ⭐⭐ 🟡 DAU fell 6% during the week of a major festival and a cricket tournament. Describe how you would test whether this is seasonal, which prior periods to line up (same festival last year, same weekday), and what you would say to a PM who wants an alert raised.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** I would not raise an alert yet: first I line this week up against the same festival in earlier years, the same weekday, and the cricket schedule, and only call it abnormal if it falls outside what those weeks did.

**Clarifying questions:**
- Which days fell and how much per day? A festival often cuts the festival day itself and lifts the evening after.
- Is the festival date fixed by a lunar calendar? If so, last year's festival sits in a different calendar week and a same-week-last-year comparison is wrong.
- Did cricket matches fall on the same days, and are they new this year (a tournament cycle)? It tells me whether to treat it as a second seasonal factor.
- Is the drop in all regions and platforms or in a few? A festival hits some regions harder.
- Do we have clean data for at least two or three past years? With one year the seasonal estimate is thin.

**Approach:**
1. Rule out data problems first (pipeline, tracking), then ask whether the drop is large against normal noise.
2. Build a baseline per day: the average of the same weekday in the 4 weeks before the event, so a weekday pattern does not leak in.
3. Compute the ratio "event week / baseline" for the same festival in past years, aligned by the festival date and not by the calendar week.
4. Compare this year's ratio to the past ratios. If it is inside the range, call it seasonal.
5. Layer the cricket effect: look at the hours of match time versus normal hours (traffic drops during play and rises at breaks).
6. Agree an alert rule with the PM: alert only when the ratio is below the seasonal range for two consecutive days, or when the drop is in segments that festivals do not explain.

**Metrics:**
- Event-week ratio = DAU in the event week / mean DAU of the same weekdays in the 4 prior weeks.
- Excess drop = this year's ratio - mean of past ratios (in points).
- z-score = excess drop / standard deviation of past ratios (with 3 years it is rough, so I also check the range).
- Guardrail: next-week recovery. A seasonal dip rebounds. A real loss does not.

**Risks:**
- Using last year's calendar week for a lunar festival.
- Growth: compare ratios, not raw counts.
- Very few past years, so the standard deviation is fragile.
- Declaring "seasonal" and never checking that DAU recovers.

**What the interviewer scores:**
- Strong: aligns on the festival, the same weekday and uses ratios. Weak: compares to last week or the same calendar week last year.
- Strong: gives a rule for the alert (range, two days, recovery). Weak: "I will wait and see".
- Strong: separates festival and cricket effects. Weak: lumps all causes into one.

**Example:** (illustrative numbers) Baseline DAU this year is 10.0 million and the festival week shows 9.4 million, a 6% fall, ratio 0.94. In the three earlier years the same festival gave ratios 0.950, 0.940 and 0.955 (mean 0.9483, standard deviation 0.0076). This year is 0.83 points below the mean, z about -1.1, and inside the past range.
- Weak: "DAU fell 6%, raise the alert."
- Strong: "Past festivals fell between 4.5% and 6%, we fell 6%, which is inside that range. No alert now. I will alert if DAU has not recovered to within 1% of baseline by the next Monday."

**Code:**
```python
# Q25 festival-week DAU: compare with the same festival in past years (illustrative numbers)
import statistics as st
# ratio = DAU in festival week / DAU baseline (average of the same weekday over the 4 prior weeks)
past = {"year-1": 0.950, "year-2": 0.940, "year-3": 0.955}
this_year = round(9.4 / 10.0, 4)
vals = list(past.values())
mean, sd = st.mean(vals), st.stdev(vals)
print("past ratios:", vals)
print("mean:", round(mean, 4), "sd:", round(sd, 4))
print("this year ratio:", this_year, " drop:", round(1 - this_year, 3))
excess = this_year - mean
z = excess / sd
print("excess vs seasonal mean (pts):", round(excess * 100, 2), " z:", round(z, 2))
inside_range = min(vals) <= this_year <= max(vals)
print("inside past range:", inside_range)
# calendar-week comparison (wrong): same ISO week last year, festival fell in another week
print("a plain week-over-week view calls it a drop of", round((1 - this_year) * 100, 1), "pts")
assert round(mean, 4) == 0.9483 and round(sd, 4) == 0.0076
assert round(excess * 100, 2) == -0.83 and round(z, 2) == -1.09
assert inside_range
```

**Output (my run):**
```text
past ratios: [0.95, 0.94, 0.955]
mean: 0.9483 sd: 0.0076
this year ratio: 0.94  drop: 0.06
excess vs seasonal mean (pts): -0.83  z: -1.09
inside past range: True
a plain week-over-week view calls it a drop of 6.0 pts
```

**Follow-ups:**
- What if there are only two prior years? Say the estimate is rough, use the range, and lean on segment checks.
- How do you automate it? A baseline model with weekday and holiday terms and an alert on the residual. Q44 of this part covers building an alert baseline.

**Common mistakes:** Comparing to the previous week. Using calendar weeks for moving festivals. Using raw counts instead of ratios. Raising an alert with no recovery check.

### Q26 ⭐⭐ 🟡 New-user retention looks worse this month, but marketing shifted spend from organic and referral to paid social. Explain how channel mix can lower blended retention without any product change, and how you would report retention fairly across the mix shift.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
**Say this first (1 line):** Blended retention is a weighted average of channel retentions, so when marketing buys more low-retention paid users the blend falls even if every channel improved, and I would report retention by channel plus a mix-standardised number.

**Clarifying questions:**
- How are channels defined, and has attribution changed? A new attribution rule can move users between channels without any real change.
- What did spend shift look like (share of new users by channel)? I need the mix before and after.
- Which retention day or window is being used (day 7, day 30)? The effect size depends on it.
- Has the product or onboarding changed in the same month? I need to rule out a true product effect.
- What is the cost per signup per channel? Lower retention may still be fine if the user is cheap.

**Approach:**
1. Split new-user retention by channel for both months.
2. Compute the mix: share of signups by channel each month.
3. Decompose the change in blended retention into a mix effect (the shares moved) and a rate effect (the channel retentions moved).
4. Standardise: take this month's channel retentions and weight them with last month's mix. That is the fair like-for-like number.
5. Go below channel when needed: campaign, creative, geography and device, because paid social is itself a mix.
6. Report retained users per rupee spent, so marketing and product read the same number.

**Metrics:**
- Channel D7 retention = users in the channel active on day 7 / signups in the channel.
- Blended D7 = sum over channels of (share of signups x channel D7).
- Mix effect = blended this month - blended at last month's mix.
- Rate effect = blended at last month's mix - blended last month.
- Cost per D7-retained user = spend / retained users.
- Guardrail: signup volume, so we do not trade volume for a nicer-looking rate.

**Risks:**
- Simpson's paradox: every channel improves but the total falls (the same pattern as Q11 of this part).
- The mix standardisation hides that paid users are weaker. Say that it is a like-for-like view, not a statement that the new mix is fine.
- Small channels give noisy rates.
- A channel's quality can drift as spend scales (the marginal paid user is worse than the average).

**What the interviewer scores:**
- Strong: decomposes into mix and rate with numbers. Weak: says "check segments".
- Strong: proposes the standardised metric and a cost-per-retained user. Weak: asks marketing to stop paid.
- Strong: notes marginal versus average quality. Weak: treats a channel as a single fixed quality.

**Example:** (illustrative numbers) Last month: 60% organic and referral at 30.0% D7, 40% paid social at 12.0%, blended 22.8%. This month: 40% organic at 30.5% and 60% paid at 12.5%, blended 19.7%. Blended fell 3.1 points. Mix effect is -3.6 points, rate effect is +0.5 points. At last month's mix, this month would be 23.3%.
- Weak: "Retention fell 3 points, onboarding is broken."
- Strong: "Both channels got slightly better. The fall is a mix effect of 3.6 points. Like-for-like retention is up 0.5 points. The real question for marketing is cost per retained user: at Rs 250 a signup and 12.5% retention, paid costs Rs 2,000 per D7-retained user."

**Code:**
```python
# Q26 channel mix and blended D7 retention (illustrative numbers)
last = {"organic+referral": (0.60, 0.300), "paid social": (0.40, 0.120)}   # (share of signups, D7 retention)
this = {"organic+referral": (0.40, 0.305), "paid social": (0.60, 0.125)}

def blend(d):
    return sum(s * r for s, r in d.values())

b_last, b_this = blend(last), blend(this)
print("blended last:", round(b_last, 4), " blended this:", round(b_this, 4), " change pts:", round((b_this - b_last) * 100, 2))
# standardise: this month's channel rates at last month's mix
std = sum(last[k][0] * this[k][1] for k in last)
print("this month at last month's mix:", round(std, 4), " change pts:", round((std - b_last) * 100, 2))
mix_effect = b_this - std
rate_effect = std - b_last
print("mix effect pts:", round(mix_effect * 100, 2), " rate effect pts:", round(rate_effect * 100, 2))
assert round(b_last, 3) == 0.228 and round(b_this, 3) == 0.197
assert round(std, 3) == 0.233
assert abs(mix_effect + rate_effect - (b_this - b_last)) < 1e-12
assert round(mix_effect * 100, 2) == -3.6 and round(rate_effect * 100, 2) == 0.5
assert all(this[k][1] > last[k][1] for k in last)   # every channel improved
# cost lens: retained users per Rs 100k spend (paid CAC Rs 250 per signup, organic costs 0) -> only paid is bought
paid_cac = 250
paid_signups = 100_000 / paid_cac
retained_per_100k = paid_signups * this["paid social"][1]
print("paid signups per Rs 100k:", paid_signups, " D7-retained:", retained_per_100k, " Rs per D7-retained:", 100_000 / retained_per_100k)
assert paid_signups == 400 and retained_per_100k == 50 and 100_000 / retained_per_100k == 2000
```

**Output (my run):**
```text
blended last: 0.228  blended this: 0.197  change pts: -3.1
this month at last month's mix: 0.233  change pts: 0.5
mix effect pts: -3.6  rate effect pts: 0.5
paid signups per Rs 100k: 400.0  D7-retained: 50.0  Rs per D7-retained: 2000.0
```

**Follow-ups:**
- How does this differ from Q11? Same arithmetic (weights shift), different setting: there it is traffic by device, here it is signups by channel.
- What if paid retention is lower but the CAC is low? Use contribution per spend, not retention alone.

**Common mistakes:** Reading the blended number as a product failure. Reporting only the average. Showing the standardised number without saying what it hides.

### Q27 ⭐⭐ 🟡 After a new OS release, DAU is down 5% only on iOS and only for users on the latest OS version. Describe the breakdowns, the logs and the checks you would use to decide between a real engagement loss and a tracking break, and who you would loop in.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** A drop confined to one OS version right after the release smells like a tracking break, so I would first size the segment, then check a second source that does not use the client event, and only then talk about real engagement loss.

**Clarifying questions:**
- Is "5%" of total DAU, of iOS DAU, or of the segment? The three readings imply very different segment drops (see the example).
- How is DAU defined: an app-open event, a foreground session, or any authenticated call? It tells me what could stop firing.
- Did our own app release go out around the same time, or only the OS update? A bug in our SDK on the new OS is the usual suspect.
- Do we have a server-side active measure (API calls, push delivery, orders)? That is the independent source.
- Are crashes, app store ratings and support tickets moving? They tell me about real user pain.

**Approach:**
1. Size it: how many users are in the segment and how much of the total drop would the segment have to explain?
2. Break down by OS version (latest, previous), app version, device model, country and time of day. A break that follows the OS version and not the app version points to the OS.
3. Compare client events with a server-side measure for the same users. If client DAU falls but backend DAU does not, events are being lost.
4. Look at the raw logs: event counts per user, session start events, the SDK init event, the error rate of the analytics endpoint, new-OS user-agent strings that a parser might drop.
5. Check real-engagement signals: orders, push open rates, crashes and ratings for that segment.
6. Loop in the mobile engineers, the analytics-SDK owner, and QA. If it is real, product and the app-store team.
7. Fix: patch the SDK or parser, then backfill if the raw events exist, and annotate the dashboard.

**Metrics:**
- Segment DAU change = DAU(segment, after) / DAU(segment, before) - 1.
- Client/backend ratio = users with the client event / users with any backend call, same segment and day.
- Event-loss indicator: events per active user and the share of backend-active users with zero client events.
- Guardrails: crash-free sessions, orders in the segment, push delivery rate.

**Risks:**
- Real causes can overlap, for example a crash on the new OS that is a true loss.
- Backend activity can include background syncs, so check that it is user-driven.
- Fixing the tracking and forgetting to restate the past dashboard.

**What the interviewer scores:**
- Strong: does the sizing sum first, then names an independent source. Weak: begins with "run a survey".
- Strong: separates a client-event break from a real loss with a concrete ratio. Weak: argues from intuition.
- Strong: names the people and the fix with backfill. Weak: stops at "find the cause".

**Example:** (illustrative numbers) Total DAU is 10 million, iOS 4 million, latest-OS users 1.2 million. If total DAU is down 5% (500,000 users) and everything sits in the segment, the segment would have fallen 42%, which real engagement almost never does. If the 5% is of iOS DAU, the segment fell 17%. If the segment itself is down 5%, that is 60,000 users and only 0.6% of total DAU. Second source: client DAU in the segment went from 1,200,000 to 1,140,000 (-5%) while backend DAU went from 1,260,000 to 1,257,000 (-0.2%), so the client/backend ratio fell from 0.952 to 0.907.
- Weak: "iOS users on the new OS are losing interest."
- Strong: "Backend activity is flat and the client ratio fell, so events are being lost for that OS. I would ask mobile engineering about the SDK on the new OS."

**Code:**
```python
# Q27 sanity check: how big would the segment loss have to be? (illustrative numbers)
total_dau = 10_000_000
ios_dau = 4_000_000
latest_os_dau = 1_200_000        # iOS users on the newest OS, before the drop

# reading A: total DAU is down 5% and all of it sits in the latest-OS segment
lost_A = 0.05 * total_dau
seg_drop_A = lost_A / latest_os_dau
# reading B: iOS DAU down 5%, all of it in the segment
lost_B = 0.05 * ios_dau
seg_drop_B = lost_B / latest_os_dau
# reading C: the segment itself is down 5%
lost_C = 0.05 * latest_os_dau
print("A lost users:", lost_A, " implied segment drop:", round(seg_drop_A, 3))
print("B lost users:", lost_B, " implied segment drop:", round(seg_drop_B, 3))
print("C lost users:", lost_C, " share of total DAU:", lost_C / total_dau)
assert lost_A == 500_000 and round(seg_drop_A, 3) == 0.417
assert lost_B == 200_000 and round(seg_drop_B, 3) == 0.167
assert lost_C == 60_000 and lost_C / total_dau == 0.006

# cross-check with a second source: backend active users (any authenticated API call) in the same segment
client_event_dau_before, client_event_dau_after = 1_200_000, 1_140_000   # app-open event
backend_dau_before, backend_dau_after = 1_260_000, 1_257_000             # server logs
ratio_before = client_event_dau_before / backend_dau_before
ratio_after = client_event_dau_after / backend_dau_after
print("client/backend ratio before:", round(ratio_before, 3), " after:", round(ratio_after, 3))
print("client DAU change:", round(client_event_dau_after / client_event_dau_before - 1, 3),
      " backend DAU change:", round(backend_dau_after / backend_dau_before - 1, 4))
assert round(ratio_before, 3) == 0.952 and round(ratio_after, 3) == 0.907
assert round(client_event_dau_after / client_event_dau_before - 1, 3) == -0.05
assert round(backend_dau_after / backend_dau_before - 1, 4) == -0.0024
# a falling client/backend ratio with flat backend points to lost events, not lost users
```

**Output (my run):**
```text
A lost users: 500000.0  implied segment drop: 0.417
B lost users: 200000.0  implied segment drop: 0.167
C lost users: 60000.0  share of total DAU: 0.006
client/backend ratio before: 0.952  after: 0.907
client DAU change: -0.05  backend DAU change: -0.0024
```

**Follow-ups:**
- What if backend DAU also falls? Then treat it as real: look at crashes, a launch failure, push token loss or an incompatible API call.
- How would you prevent it next time? Test the analytics SDK on beta OS versions and alert on the client/backend ratio per segment.

**Common mistakes:** Not sizing the segment. Trusting one data source. Assuming it is real because the dashboard says so. Forgetting to annotate and backfill.

### Q28 ⭐⭐ 🟡 A delivery fee change raised the fee from Rs 20 to Rs 30 on small orders. Orders fell 6%, but revenue rose 4%. Say how you would judge whether the change was good, what guardrails and time horizon you would use, and which customers you would look at separately.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
**Say this first (1 line):** I would judge the fee change by the contribution it adds after the orders it loses, over several weeks and including the customers who then stop ordering larger baskets, not by the revenue line alone.

**Clarifying questions:**
- What does "revenue" mean here: fee revenue only, or total platform revenue (commission plus fees)? The prompt does not say, and it changes the sums.
- Which orders are "small" (a threshold) and what share are they? The effect lives there.
- What does a small order cost us to deliver? Revenue up on a loss-making order is not the same as profit.
- Was the change tested with a control or rolled out everywhere? Without control, season and promotions are confounded.
- Which customers are price-sensitive: new users, low-frequency users, users who always order small?

**Approach:**
1. Write the economics per order: commission + fee - delivery cost - discounts = contribution.
2. Compare treated and control, or against a pre-trend, for orders, revenue and contribution.
3. Look for substitution: do customers merge small orders into bigger ones (good), order less (bad), or move to a competitor (worse)?
4. Check the halo: do the same customers reduce large orders or visits too?
5. Cut by customer type: new versus repeat, high versus low frequency, city.
6. Extend the horizon: 4 to 8 weeks, so the first reaction does not hide the lasting one.
7. Decide with a break-even: how many large orders can we lose before the gain is gone?

**Metrics:**
- Orders per active user per week = orders / users active that week.
- Contribution per order = commission + fee - delivery cost - discount.
- Total contribution = sum over orders of contribution (the decision metric).
- Small-order share and average basket = share of orders below the threshold; AOV.
- Guardrails: weekly active users, repeat rate, complaints about fees, app rating.

**Risks:**
- Revenue up on fewer orders can still mean fewer customers a month later.
- Fee revenue vs total revenue confusion in the quote.
- Mix: if the lost orders are low-margin ones, the picture improves, which is fine, but say so.
- Short horizon: the harm to repeat behaviour appears later.

**What the interviewer scores:**
- Strong: converts the prompt to contribution per order and a break-even. Weak: says "revenue went up, ship".
- Strong: names a halo check and segment cuts. Weak: looks at one average.
- Strong: asks what revenue means. Weak: assumes.

**Example:** (illustrative numbers) 100,000 weekly orders: 60,000 small (basket Rs 150, commission 20% = Rs 30, fee Rs 20) and 40,000 large (basket Rs 375, commission Rs 75, no fee). Revenue is Rs 60,00,000. After the change small orders drop 10% to 54,000, so total orders fall 6% to 94,000 and revenue becomes Rs 62,40,000, up 4%. With a rider cost of Rs 60 per small order, small-order contribution moves from -Rs 6,00,000 to Rs 0. The Rs 2,40,000 gain would be wiped out if large orders fell by 3,200, that is 8% of them.
- Weak: "Orders fell 6%, so it is bad."
- Strong: "Revenue is up 4% and small-order contribution went from negative to zero. I would ship if the large-order loss stays below 8% and repeat rate holds, and I would watch new users separately."

**Code:**
```python
# Q28 delivery fee Rs 20 -> Rs 30 on small orders (illustrative numbers)
small0, large0 = 60_000, 40_000        # weekly orders before
small_aov, large_aov = 150, 375
commission = 0.20
fee0, fee1 = 20, 30
small1 = 54_000                        # small orders fall 10%; large unchanged -> total falls 6%
large1 = 40_000

def rev(small, large, fee):
    return small * (small_aov * commission + fee) + large * (large_aov * commission)

r0, r1 = rev(small0, large0, fee0), rev(small1, large1, fee1)
print("orders before/after:", small0 + large0, small1 + large1, " change:", round((small1 + large1) / (small0 + large0) - 1, 3))
print("revenue before/after:", r0, r1, " change:", round(r1 / r0 - 1, 3))
assert small0 + large0 == 100_000 and small1 + large1 == 94_000
assert r0 == 6_000_000 and r1 == 6_240_000 and round(r1 / r0 - 1, 3) == 0.04

# contribution after a rider cost of Rs 60 per small order
rider = 60
c0 = small0 * (small_aov * commission + fee0 - rider)
c1 = small1 * (small_aov * commission + fee1 - rider)
print("small-order contribution before/after (Rs):", c0, c1)
assert c0 == -600_000 and c1 == 0

# halo: how many large orders can be lost before the revenue gain is gone?
gain = r1 - r0
large_order_rev = large_aov * commission
breakeven_orders = gain / large_order_rev
print("revenue gain:", gain, " breakeven lost large orders:", breakeven_orders, " as share of large:", breakeven_orders / large0)
assert gain == 240_000 and breakeven_orders == 3200 and breakeven_orders / large0 == 0.08
```

**Output (my run):**
```text
orders before/after: 100000 94000  change: -0.06
revenue before/after: 6000000.0 6240000.0  change: 0.04
small-order contribution before/after (Rs): -600000.0 0.0
revenue gain: 240000.0  breakeven lost large orders: 3200.0  as share of large: 0.08
```

**Follow-ups:**
- What if new users react much more? Exempt them for the first orders and measure again.
- How would you test? A holdout of cities or users at the old fee, so seasonality cancels.

**Common mistakes:** Treating revenue as profit. Ignoring the delivery cost. One-week horizon. Averaging all customers together.

### Q29 ⭐⭐ 🟡 Subscription churn rose from 3% to 4.5% a month after a price increase. Describe how you would find which segments churned, tell price effects from the usual seasonality or a product issue, and estimate the revenue impact over the next year.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** I would isolate the price effect with a comparison group that did not get the new price, find who churned by segment, and then model the year ahead two ways, because higher price with higher churn can raise 12-month revenue and still lower lifetime value.

**Clarifying questions:**
- Did everyone get the price increase on the same date, or was there a control group or grandfathered plan? A control is the only clean way to separate price from season.
- Is the 3% to 4.5% churn voluntary cancellation, failed payments or both? Payment failures have a different fix.
- What did the competitor and the product do that month? A rival promotion or an outage can look like a price effect.
- How is churn measured (share of subscribers at month start who left in the month)? The base matters.
- Was the increase announced in advance? Notice period changes when the churn shows up.

**Approach:**
1. Check the data first: same churn definition, no billing glitch, no change in how cancellations are logged.
2. Find who churned: by plan, tenure, price paid, region, payment method, usage level and cancellation reason. Price-driven churn usually concentrates in low-usage and short-tenure users.
3. Separate price from season: use difference-in-differences against a control (for example a region or plan still on the old price) and the same month in previous years.
4. Check for a product issue: usage, support tickets and ratings among churned users before they left.
5. Estimate the revenue impact: run the 12-month revenue under old price, new price with persistent churn, and new price with churn that fades.
6. Also compute the lifetime view and the break-even churn.

**Metrics:**
- Monthly churn = subscribers who cancelled in the month / subscribers at the start of the month.
- Price effect on churn = (treated after - treated before) - (control after - control before).
- 12-month revenue = sum over months of active subscribers x price (closed cohort, no new adds).
- Simple lifetime value = price / monthly churn.
- Guardrails: new subscriber volume, downgrades to a cheaper plan, support contacts.

**Risks:**
- The control group may differ from the treated group (for example by region), which biases the difference-in-differences.
- A closed cohort leaves out new subscribers, who also respond to the higher price.
- Short-run churn spikes can be pull-forward of cancellations that would have come later.
- Revenue over 12 months looks good while the lifetime value falls.

**What the interviewer scores:**
- Strong: separates price from season with a control and a number. Weak: says "churn went up because of price".
- Strong: gives a revenue model with scenarios and a break-even. Weak: a single guess.
- Strong: raises lifetime value versus 12-month revenue. Weak: stops at the short term.

**Example:** (illustrative numbers) 100,000 subscribers, price Rs 199 to Rs 249, churn 3.0% to 4.5%. A control region stayed on Rs 199 and moved 3.0% to 3.4%, so the price effect is 1.5 - 0.4 = 1.1 points. Over 12 months the old plan earns Rs 20.31 crore (a closed cohort). The new price with 4.5% persistent churn earns Rs 23.49 crore (+15.7%), with churn fading back to 3% after 3 months Rs 24.47 crore (+20.5%). The break-even constant churn at the new price is about 7.4% a month. The lifetime value per subscriber is Rs 199 / 0.03 = Rs 6,633 before and Rs 249 / 0.045 = Rs 5,533 after, 16.6% lower.
- Weak: "Churn rose 50%, the price increase failed."
- Strong: "About 1.1 of the 1.5 points are price. Revenue over a year is up even if the churn persists, but lifetime value is down about 17%, so I would check if segments with high usage tolerate the price and the low-usage segment does not."

**Code:**
```python
# Q29 price increase and churn: DiD and 12-month revenue (illustrative numbers)
subs0 = 100_000
old_price, new_price = 199, 249
# difference-in-differences: treated users saw the new price, a control region still on old price
treated_before, treated_after = 0.030, 0.045
control_before, control_after = 0.030, 0.034
did = (treated_after - treated_before) - (control_after - control_before)
print("raw churn change pts:", round((treated_after - treated_before) * 100, 2), " DiD price effect pts:", round(did * 100, 2))
assert round(did * 100, 2) == 1.10

def year_revenue(price, churn_by_month, subs=subs0):
    total = 0.0
    for c in churn_by_month:
        total += subs * price          # revenue from subscribers active this month
        subs *= (1 - c)                # churn at month end (closed cohort, no new adds)
    return total

old = year_revenue(old_price, [0.03] * 12)
persist = year_revenue(new_price, [0.045] * 12)
# price effect only: churn at 4.5% for 3 months then back to 3%
revert = year_revenue(new_price, [0.045] * 3 + [0.03] * 9)
# DiD view: only 3.0% + 1.1 pts = 4.1% is due to price; the rest is seasonality that hits old price too
did_view = year_revenue(new_price, [0.041] * 12)
old_season = year_revenue(old_price, [0.034] * 12)
for name, v in [("old price, 3.0% churn", old), ("new price, 4.5% persists", persist),
                ("new price, 4.5% for 3 months then 3.0%", revert),
                ("new price, 4.1% (DiD price effect)", did_view), ("old price, 3.4% (seasonal baseline)", old_season)]:
    print(f"{name:42} Rs {v/1e6:8.2f} m   vs old {v/old - 1:+.1%}")
assert persist > old and revert > persist and did_view > persist
assert round(persist / old - 1, 3) == 0.157 and round(revert / old - 1, 3) == 0.205
assert round(did_view / old - 1, 3) == 0.181 and round(old_season / old - 1, 3) == -0.021
# breakeven constant monthly churn at which 12-month revenue equals the old plan
lo, hi = 0.03, 0.30
for _ in range(60):
    mid = (lo + hi) / 2
    if year_revenue(new_price, [mid] * 12) > old:
        lo = mid
    else:
        hi = mid
print("breakeven monthly churn at new price:", round(lo, 4))
assert 0.07 < lo < 0.10

# lifetime view (simple geometric lifetime = price / churn, per subscriber, undiscounted)
ltv_old, ltv_new = old_price / 0.03, new_price / 0.045
print("LTV old:", round(ltv_old), " LTV new:", round(ltv_new), " change:", round(ltv_new / ltv_old - 1, 3))
assert round(ltv_old) == 6633 and round(ltv_new) == 5533 and round(ltv_new / ltv_old - 1, 3) == -0.166
```

**Output (my run):**
```text
raw churn change pts: 1.5  DiD price effect pts: 1.1
old price, 3.0% churn                      Rs   203.08 m   vs old +0.0%
new price, 4.5% persists                   Rs   234.89 m   vs old +15.7%
new price, 4.5% for 3 months then 3.0%     Rs   244.72 m   vs old +20.5%
new price, 4.1% (DiD price effect)         Rs   239.83 m   vs old +18.1%
old price, 3.4% (seasonal baseline)        Rs   198.84 m   vs old -2.1%
breakeven monthly churn at new price: 0.0737
LTV old: 6633  LTV new: 5533  change: -0.166
```

**Follow-ups:**
- How would you test a future price change? A randomised price test on a share of new users, with 90-day churn as a guardrail. Book 1 Part 10 Q19 (cannot randomize) covers the options when you cannot randomise.
- What would you add to the model? New subscribers, plan downgrades, discounting for win-backs and discounting future revenue.

**Common mistakes:** Reading raw churn change as the price effect. Ignoring season. Using only 12-month revenue. Forgetting the tenure mix of the churners.

### Q30 ⭐⭐ 🟡 In a two-sided marketplace, new seller listings grew 25% this quarter but buyer conversion fell from 5% to 4.2%. Explain the possible reasons, how you would tell a supply-quality dilution from a search or ranking problem, and which metrics you would add to monitor both sides.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** More supply and lower conversion can come from weaker new listings diluting the results or from search and ranking not handling the larger catalogue, and I would tell them apart by comparing conversion for sessions that mostly show old listings with sessions that mostly show new ones.

**Clarifying questions:**
- Where did the 25% more listings come from (new sellers, existing sellers listing more, a bulk upload)? Quality differs a lot by source.
- Did search, ranking or the filters change this quarter? A ranking change is the other main suspect.
- Is the conversion drop everywhere or in some categories and cities? Dilution and ranking problems show different footprints.
- Did buyer traffic mix change (more new buyers, more paid traffic)? Buyer mix can lower conversion on its own.
- How is conversion defined (sessions with a search that end in an order)? The denominator matters.

**Approach:**
1. Check data and the buyer mix first, so I am not chasing the supply when the cause is traffic.
2. Segment sessions by how much of the top results are new listings.
3. Compare conversion in those segments. Dilution says: old-heavy sessions convert as before and new-heavy sessions convert badly. A search or ranking problem says: conversion fell in all segments, including old-heavy ones.
4. Look at listing quality: photo count, price versus category median, response time, cancellation rate, duplicate listings.
5. Look at search itself: zero-result rate, click-through on the first page, depth of scroll, query reformulation rate.
6. Look at the seller side: orders per listing and the share of listings with no order in 30 days.
7. Decide the action: quality gates for new listings, a ranking penalty for low-quality supply, or search fixes.

**Metrics:**
- Buyer conversion = sessions with an order / sessions with a search.
- Conversion by exposure = the same, within sessions grouped by share of new listings in the top 10.
- Orders per listing = orders / active listings (supply health).
- Search success = sessions with a click on a result / sessions with a search; zero-result rate.
- Guardrails: seller churn, cancellation rate, buyer repeat rate.

**Risks:**
- Selection: sessions with many new listings may be different sessions (broader queries).
- Both causes can be present, so the segment table can show both.
- New listings may need a few weeks to attract orders, so "low conversion" might be a cold-start effect.

**What the interviewer scores:**
- Strong: gives a test that separates the two stories. Weak: lists reasons.
- Strong: names metrics for both sides of the marketplace. Weak: only buyer conversion.
- Strong: proposes an action tied to each cause. Weak: "improve quality".

**Example:** (illustrative numbers) 1,000,000 sessions. Before, conversion 5% (50,000 orders). After, 42,000 orders (4.2%). Suppose 75% of sessions are old-heavy and 25% new-heavy. World A (dilution): old-heavy 5.0%, new-heavy 1.8%, blended 0.75 x 5.0 + 0.25 x 1.8 = 4.2%. World B (ranking or search problem): both segments 4.2%. The blended number is 4.2% in both worlds, and the segment table tells them apart. Supply side: orders per listing fell from 0.50 to 0.336 (-33%).
- Weak: "More listings is good, conversion fell, it is noise."
- Strong: "The blended 4.2% is the same in both stories, so I split by new-listing exposure. Old-heavy sessions at 5.0% mean dilution, so I would gate quality. If they are at 4.2% too, I would look at ranking and search."

**Code:**
```python
# Q30 marketplace: listings +25%, buyer conversion 5.0% -> 4.2% (illustrative numbers)
sessions = 1_000_000
share_old_heavy, share_new_heavy = 0.75, 0.25   # sessions whose top results are mostly old / mostly new listings

worlds = {
    "A: quality dilution":  {"old-heavy": 0.050, "new-heavy": 0.018},
    "B: ranking/search bug": {"old-heavy": 0.042, "new-heavy": 0.042},
}
for name, w in worlds.items():
    blended = share_old_heavy * w["old-heavy"] + share_new_heavy * w["new-heavy"]
    print(f"{name:24} old-heavy {w['old-heavy']:.1%}  new-heavy {w['new-heavy']:.1%}  blended {blended:.2%}  orders {blended*sessions:,.0f}")
    assert round(blended, 4) == 0.042
    assert round(blended * sessions) == 42_000
print("orders before:", 0.05 * sessions)
assert 0.05 * sessions == 50_000
# supply side: listings +25% -> avg listings per query result slot competing; sellers' orders per listing
orders_before, orders_after = 50_000, 42_000
listings_before, listings_after = 100_000, 125_000
opl_b, opl_a = orders_before / listings_before, orders_after / listings_after
print("orders per listing before/after:", opl_b, round(opl_a, 3), " change:", round(opl_a / opl_b - 1, 3))
assert opl_b == 0.5 and round(opl_a, 3) == 0.336 and round(opl_a / opl_b - 1, 3) == -0.328
```

**Output (my run):**
```text
A: quality dilution      old-heavy 5.0%  new-heavy 1.8%  blended 4.20%  orders 42,000
B: ranking/search bug    old-heavy 4.2%  new-heavy 4.2%  blended 4.20%  orders 42,000
orders before: 50000.0
orders per listing before/after: 0.5 0.336  change: -0.328
```

**Follow-ups:**
- How would you confirm causation? A small experiment that ranks new listings lower or applies a quality score for a share of traffic. Book 1 Part 10 Q13 (primary metric up, guardrail down) covers weighing the two sides.
- What would you monitor going forward? Conversion by listing age and quality tier, plus orders per listing.

**Common mistakes:** Blaming noise. One blended conversion number. Monitoring only the buyer side. Not asking where the new supply came from.

### Q31 ⭐⭐ 🟡 A new ETA model improved ETA accuracy by 15%, but orders in the treatment group are 2% lower. Explain how a better prediction can reduce orders, what you would look at by segment, and how you would pick the metric that decides the launch.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** A more accurate ETA can reduce orders because the old one was optimistic: honest, longer estimates lose some orders at checkout but remove late deliveries, cancellations and bad experiences, so I would decide on delivered orders, repeat rate and satisfaction over several weeks, not on checkout orders alone.

**Clarifying questions:**
- What does "accuracy improved by 15%" mean (mean absolute error down 15%, share within 5 minutes, bias)? The prompt does not say, and a lower error can hide a bias shift.
- Did the displayed ETA go up on average? That is the likely mechanism.
- Is the 2% drop in orders placed or in delivered orders? Cancellations change the picture.
- Which segments are affected (short versus long distance, peak versus off-peak, new versus repeat users)?
- How long did the test run? Repeat behaviour needs weeks.

**Approach:**
1. Check the experiment is clean (sample ratio, same exposure period).
2. Split the accuracy gain into error and bias: did the shown ETA get longer on average?
3. Look at the funnel: from ETA view to checkout, by ETA bucket shown. Orders fall where the shown ETA moved up.
4. Follow what happens after checkout: late-delivery rate, cancellations, refunds, complaints, rating.
5. Look at repeat orders over the next 4 to 8 weeks per user.
6. Cut by segment: orders may fall mostly where the old ETA was most optimistic.
7. Pick the deciding metric: delivered orders per exposed user over several weeks (and contribution), with satisfaction and late rate as guardrails.

**Metrics:**
- ETA bias = mean (shown ETA - actual time).
- ETA MAE = mean of |shown ETA - actual time|.
- Late rate = orders delivered later than shown ETA + 5 minutes / delivered orders.
- Delivered orders per exposed user over 4 weeks.
- Guardrails: cancellation rate, refund rate, support contacts, repeat rate.

**Risks:**
- Accuracy is a model metric. The product metric is orders and satisfaction.
- Short test hides the repeat benefit.
- Segment mix: the loss may be in new users, who have no experience to correct for the optimistic ETA.

**What the interviewer scores:**
- Strong: gives the mechanism (honest ETA shown longer) and a test of it. Weak: "the model must be wrong".
- Strong: chooses a decision metric over a longer horizon. Weak: picks checkout orders.
- Strong: asks what accuracy means. Weak: takes it at face value.

**Example:** (illustrative numbers) 100,000 sessions, 30% convert. Average actual time is 30 minutes. Old ETA shown averaged 24 (bias -6), new 28 (bias -2). Assume each extra displayed minute lowers conversion by 0.5% relative: 4 minutes x 0.5% = 2%, so orders go from 30,000 to 29,400. Late rate falls from 30% to 12%. If late orders cancel 10% of the time and on-time orders 2%, the cancellation rate falls from 4.4% to 2.96%, so delivered orders are 28,680 before and 28,530 after, only 0.5% lower. A 0.5% repeat-purchase gain would close it. Mean absolute error 6.0 to 5.1 minutes is the 15%.
- Weak: "Orders are down 2%, roll back the model."
- Strong: "Orders placed are down 2% because the promise got honest. Delivered orders are down 0.5% and cancellations fell by a third. I would hold the decision for a 4-week repeat and satisfaction read, and consider showing a range."

**Code:**
```python
# Q31 better ETA, fewer orders (illustrative numbers)
sessions = 100_000
conv0 = 0.30
shown_old, shown_new = 24, 28      # average ETA shown, minutes
actual = 30                        # average actual delivery time, minutes
elasticity = -0.005                # relative drop in conversion per extra displayed minute (assumed)
conv1 = conv0 * (1 + elasticity * (shown_new - shown_old))
orders0, orders1 = sessions * conv0, sessions * conv1
print("bias old/new (min, shown - actual):", shown_old - actual, shown_new - actual)
print("orders before/after:", round(orders0), round(orders1), " change:", round(orders1 / orders0 - 1, 3))
assert round(orders0) == 30_000 and round(orders1) == 29_400 and round(orders1 / orders0 - 1, 3) == -0.02

late0, late1 = 0.30, 0.12          # share of orders delivered later than shown + 5 min
cancel_late, cancel_ontime = 0.10, 0.02
cr0 = late0 * cancel_late + (1 - late0) * cancel_ontime
cr1 = late1 * cancel_late + (1 - late1) * cancel_ontime
d0, d1 = orders0 * (1 - cr0), orders1 * (1 - cr1)
print("cancel rate before/after:", round(cr0, 4), round(cr1, 4))
print("delivered orders before/after:", round(d0), round(d1), " change:", round(d1 / d0 - 1, 4))
assert round(cr0, 3) == 0.044 and round(cr1, 4) == 0.0296
assert round(d0) == 28_680 and round(d1) == 28_530 and round(d1 / d0 - 1, 4) == -0.0052
# what repeat-rate gain from fewer late orders would turn delivered orders positive over 8 weeks?
repeat_uplift_needed = d0 / d1 - 1
print("delivered-order gain needed from repeat purchases:", round(repeat_uplift_needed, 4))
assert round(repeat_uplift_needed, 4) == 0.0053
# the "15% better accuracy" in the prompt, read as mean absolute error falling 15%
mae_old, mae_new = 6.0, 5.1
print("MAE change:", round(mae_new / mae_old - 1, 3))
assert round(mae_new / mae_old - 1, 3) == -0.15
```

**Output (my run):**
```text
bias old/new (min, shown - actual): -6 -2
orders before/after: 30000 29400  change: -0.02
cancel rate before/after: 0.044 0.0296
delivered orders before/after: 28680 28530  change: -0.0052
delivered-order gain needed from repeat purchases: 0.0053
MAE change: -0.15
```

**Follow-ups:**
- Could you keep accuracy and recover orders? Yes: speed up delivery, show a range, offer a cheaper slower option.
- Which metric decides the launch? The one tied to the goal over a long window, here delivered orders per user plus a satisfaction guardrail. See Q16 of this part for the same pattern with a ranking change.

**Common mistakes:** Treating model accuracy as the business goal. Reading placed orders only. Short test window. Not checking the shown-ETA shift.

### Q32 ⭐⭐ 🟡 Sessions per DAU jumped 20% overnight while DAU stayed flat. Explain which causes you would test (bots, a logging change, a new auto-refresh, a real engagement spike), and which two checks would settle it fastest.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Flat DAU with 20% more sessions per user overnight is more likely a definition or logging change than real behaviour, and two checks settle it: does the jump line up with an app or SDK version, and are actions or active time per DAU flat.

**Clarifying questions:**
- How is a session defined (timeout, foreground event) and did that change? A changed timeout splits one visit into more sessions.
- Did a release or SDK update go out that night? It would explain a step change.
- Is the jump uniform across platforms, versions and countries? Instrumentation changes are usually localised to a version.
- Did any feature with background refresh or auto-play ship? These create sessions with no user action.
- Is time spent or orders per user also up? Real engagement lifts them.

**Approach:**
1. Treat it as a measurement question first, since the change is overnight and DAU did not move.
2. Check the timeline against releases, SDK changes, config flags and the session-timeout setting.
3. Break sessions per DAU by platform, app version, country and new versus old users. A step change in one version is a logging cause.
4. Compare sessions with other measures per DAU: events per DAU, actions (orders, messages, plays) per DAU, total active time per DAU. If they are flat, sessions were split or inflated.
5. Look at session length and events per session: a fall in both with a rise in session count means splitting.
6. Look for bots and automation: very high session counts per user, identical timings, data-centre IPs, no touch events.
7. If real, find which feature drove it and check quality (is it good engagement or notification-driven opening).

**Metrics:**
- Sessions per DAU = sessions / daily active users.
- Events per DAU, actions per DAU and active time per DAU (independent of how sessions are cut).
- Events per session = events / sessions (falls when sessions split).
- Share of users above a high session-count threshold (bot indicator).
- Guardrails: DAU, retention, crash rate.

**Risks:**
- Several causes at once (a new refresh and a timeout change).
- Fixing only the dashboard and not warning the teams whose goals use sessions.
- Bot filtering removing real heavy users.

**What the interviewer scores:**
- Strong: names four causes and the two fastest checks. Weak: starts a long analysis plan.
- Strong: uses an independent measure (actions or time per DAU). Weak: relies on the same inflated metric.
- Strong: says what to do next either way. Weak: stops at diagnosis.

**Example:** (illustrative numbers) 5,000 simulated users, same events, seeded. Changing the timeout from 30 to 15 minutes raised sessions per user from 1.54 to 1.96 (+26.8%), the same order as the 20% in the prompt, while events per user stayed 18.91 and events per session dropped from 12.26 to 9.66.
- Weak: "Users are 20% more engaged, great."
- Strong: "DAU and actions per DAU are flat while events per session fell, which is what session splitting does. I will check the version and the timeout config before anyone celebrates."

**Code:**
```python
# Q32 sessions per DAU +20% with flat DAU: a session-timeout change splits sessions (seeded simulation)
import random
random.seed(7)
users = 5000
def make_events():
    ev = []
    t = random.uniform(8, 10) * 60.0            # minutes since midnight
    for _ in range(random.randint(8, 30)):      # events in the day
        ev.append(t)
        # most gaps are short; 3% are real breaks (35-120 min); 1.7% are mid gaps of 16-29 minutes
        r = random.random()
        if r < 0.03:
            t += random.uniform(35, 120)
        elif r < 0.047:
            t += random.uniform(16, 29)
        else:
            t += random.expovariate(1 / 3.0)
    return ev

data = [make_events() for _ in range(users)]

def sessions(events, timeout):
    n = 1
    for a, b in zip(events, events[1:]):
        if b - a > timeout:
            n += 1
    return n

s30 = sum(sessions(e, 30) for e in data) / users
s15 = sum(sessions(e, 15) for e in data) / users
events_per_user = sum(len(e) for e in data) / users
active_span30 = sum(e[-1] - e[0] for e in data) / users
print("users (DAU, unchanged):", users)
print("sessions per DAU, 30-min timeout:", round(s30, 2))
print("sessions per DAU, 15-min timeout:", round(s15, 2), " change:", round(s15 / s30 - 1, 3))
print("events per DAU (unchanged by the timeout):", round(events_per_user, 2))
print("events per session 30 vs 15:", round(events_per_user / s30, 2), round(events_per_user / s15, 2))
assert 1.15 < s15 / s30 < 1.30    # a pure definition change moves the ratio by roughly 20%
assert abs(events_per_user - sum(len(e) for e in data) / users) < 1e-9
# fastest check 2: events or orders per DAU is identical under both definitions
orders_proxy_30 = sum(len(e) for e in data)
orders_proxy_15 = sum(len(e) for e in data)
assert orders_proxy_30 == orders_proxy_15
```

**Output (my run):**
```text
users (DAU, unchanged): 5000
sessions per DAU, 30-min timeout: 1.54
sessions per DAU, 15-min timeout: 1.96  change: 0.268
events per DAU (unchanged by the timeout): 18.91
events per session 30 vs 15: 12.26 9.66
```

**Follow-ups:**
- The two checks again? One, split by app version and platform to see whether the step lines up with a release. Two, compare actions or active time per DAU, which do not depend on how sessions are cut.
- What if it is real? Then break down by feature and check retention and satisfaction, because refresh-driven opens are not value.

**Common mistakes:** Calling it engagement. Checking only sessions. Missing that the definition changed. No annotation on the dashboard.

### Q33 ⭐⭐ 🟡 A new onboarding flow lifts day-1 retention by 4 points, but day-30 retention is unchanged. Explain the likely story, how you would check for a novelty effect, and what you would recommend to the team that wants to ship it everywhere.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Day-1 up and day-30 flat usually means the new flow gets people through the first day (a reward, a nudge, a shorter path) without building a habit, so I would look at the full retention curve for a fade, check the effect by cohort week, and recommend a staged rollout with a long holdout, not shipping it everywhere as a retention win.

**Clarifying questions:**
- How many users per arm and how long has it run? The day-30 data must cover enough users and full weeks.
- What changed in the flow (incentive, fewer steps, forced permission prompts)? It points to the mechanism.
- What is the activation event that predicts value (first order, first message)? Day-1 return is only a proxy.
- Are there guardrails: uninstall rate, permission opt-in, support tickets, time to first value?
- Is the flow costly (rewards, extra engineering, notifications)? It changes the bar to ship.

**Approach:**
1. Draw the retention curve for both arms on days 1, 3, 7, 14, 30 and compute the gap with a confidence interval at each point.
2. A gap that shrinks smoothly to zero is consistent with a transient or novelty effect. A gap that stays is a lasting one.
3. Check the novelty and primacy pattern: compare the earliest-enrolled cohort with later ones, and look at repeat exposure within a user. Book 1 Part 10 Q8 covers the novelty effect and the primacy effect.
4. Ask what the 4 points are: users who return on day 1 and then leave. Check activation (first key action) and depth: did the extra returners do anything useful?
5. Segment by acquisition channel, platform and intent. The flow may help one group.
6. Check whether the day-30 result is "no effect" or "not enough data": the confidence interval says how large an effect it could still hide.
7. Recommend: do not ship to everyone as a retention win. Ship if it improves activation or cost with no harm, keep a long-term holdout to day 60 or 90, and iterate on what carries users from day 1 to the habit.

**Metrics:**
- Day-N retention = users in the arm active on day N / users in the arm that started onboarding.
- Gap at day N = treatment - control retention, with a 95% confidence interval from a two-proportion standard error.
- Activation rate = users completing the first key action within a set window / users starting onboarding.
- Guardrails: uninstall rate, permission opt-in, support contacts.

**Risks:**
- Reading "unchanged" as "no effect": the interval at day 30 is wide.
- Multiple days tested, so one significant day is not a finding. Q14 of Book 1 Part 10 (insignificant results) covers reading a null properly.
- Novelty versus true effect needs time, which the team does not want to spend.

**What the interviewer scores:**
- Strong: uses the curve, the interval and a mechanism. Weak: says "the flow is bad" or "ship it".
- Strong: separates "no effect" from "not enough data" with a number. Weak: reads the point estimate.
- Strong: a staged rollout and holdout. Weak: ship everywhere or kill it.

**Example:** (illustrative numbers) 20,000 users per arm. Retention control versus treatment: day 1 40% vs 44%, day 3 28% vs 30%, day 7 20% vs 21%, day 14 15% vs 15.5%, day 30 12% vs 12%. The gap runs 4.0, 2.0, 1.0, 0.5, 0.0 points, and the day-30 confidence interval is -0.64 to +0.64 points, so a gain of more than about 0.6 points is unlikely. Detecting a 1-point gain at day 30 would need about 17,166 users per arm for 80% power.
- Weak: "Day-1 retention is up 4 points, ship it."
- Strong: "The gap decays to zero by day 30 and the interval excludes a gain over 0.64 points, so this is not a habit lever. I would ship it only for the activation benefit, hold out 5% to day 90 and try to carry users from day 1 into week 2."

**Code:**
```python
# Q33 onboarding flow: day-1 up 4 pts, day-30 unchanged (illustrative numbers)
import math
n = 20_000                                       # users per arm
days = [1, 3, 7, 14, 30]
control = [0.40, 0.28, 0.20, 0.15, 0.12]
treat = [0.44, 0.30, 0.21, 0.155, 0.12]

def ci_diff(p1, p0, n):
    d = p1 - p0
    se = math.sqrt(p1 * (1 - p1) / n + p0 * (1 - p0) / n)
    return d, d - 1.96 * se, d + 1.96 * se

print("day  control treat  diff(pts)  95% CI (pts)")
rows = {}
for dday, c, t in zip(days, control, treat):
    d, lo, hi = ci_diff(t, c, n)
    rows[dday] = (d, lo, hi)
    print(f"{dday:>3}  {c:.3f}   {t:.3f}  {d*100:6.2f}    [{lo*100:5.2f}, {hi*100:5.2f}]")
d1, lo1, hi1 = rows[1]
d30, lo30, hi30 = rows[30]
assert round(d1 * 100, 2) == 4.0 and lo1 > 0
assert d30 == 0 and lo30 < 0 < hi30
print("day-30 half-width (pts):", round((hi30 - d30) * 100, 2))
assert round((hi30 - d30) * 100, 2) == 0.64
# diffs shrink with time -> consistent with a transient effect
diffs = [rows[d][0] for d in days]
assert all(a >= b for a, b in zip(diffs, diffs[1:]))
# users per arm needed to detect a 1-point day-30 gain (80% power, alpha 0.05, p=0.12)
z_a, z_b = 1.96, 0.8416
p0, p1 = 0.12, 0.13
n_need = ((z_a + z_b) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1))) / (p1 - p0) ** 2
print("users per arm to detect +1 pt at day 30:", math.ceil(n_need))
assert math.ceil(n_need) == 17_166
```

**Output (my run):**
```text
day  control treat  diff(pts)  95% CI (pts)
  1  0.400   0.440    4.00    [ 3.03,  4.97]
  3  0.280   0.300    2.00    [ 1.11,  2.89]
  7  0.200   0.210    1.00    [ 0.21,  1.79]
 14  0.150   0.155    0.50    [-0.20,  1.20]
 30  0.120   0.120    0.00    [-0.64,  0.64]
day-30 half-width (pts): 0.64
users per arm to detect +1 pt at day 30: 17166
```

**Follow-ups:**
- Could day-1 retention still matter? Yes, if it lifts activation or revenue, or lowers acquisition waste, but then name that benefit and measure it.
- How long should the holdout be? Long enough to cover the horizon you care about (day 60 or 90), see Book 1 Part 10 Q24 (long-term holdout).

**Common mistakes:** Calling a flat point estimate "no effect". Judging on day 1 only. Ignoring the fade pattern. Shipping everywhere with no holdout.
