R = {}
R["«EXEC»"] = """*(Synthetic data built on Zerodha's documented intervention and "more than 50%" headline. The true effect is set at −30% so that methods can be judged against it. Written after the analysis.)*

- **The question:** did the point-of-trade warning really halve penny-stock trading by first-time investors, or did a cooling market do part of the work?
- **The four methods give very different answers:**

| Method | Estimate | Verdict |
|---|---|---|
| Before vs after (as reported) | **−62.5%** | Wrong: other brokers, with no nudge, fell **−46.8%** over the same windows. Most of the "drop" is the market fading after the 2020 boom. |
| Interrupted time series, own trend only | −72% | Worse, because it extends the boom-era trend |
| Interrupted time series + market control | −20% (CI −30% to −8%) | Closer |
| **Difference-in-differences vs other brokers**, using the staggered web → Android → iOS rollout | **−28.3%** (CI −30.0% to −26.5%) | Close to the truth |
| **Randomised 5% holdout** of users never nudged | **−31.9%** (CI −35% to −29%) | Close to the truth (−30%) |

- **The checks that make the DiD credible:**
  - Placebo launch dates find ≈ 0 in 8 of 9 cases.
  - The event study is flat before each launch (wobbles ≤ 6%) and drops after.
  - Allowing each platform its own trend still gives −25% to −27%.
- **The nudge works,** cutting penny trading by about **30%**, which is very valuable. But the headline "more than 50%" overstates it roughly 2×.
- **₹ impact (a broker with 20 lakh active first-time investors):** the holdout implies ≈ **₹220 crore/year of investor losses avoided** (₹280 per user per quarter). Pre/post would have claimed ≈ ₹430 crore. "Tens of crores" is, if anything, conservative.
- **I recommend:**
  - Keep the nudge.
  - Report its impact with a control (staggered rollout + other-broker benchmark) or a small permanent holdout (2–5% detects a 7–10% change).
  - Never use a pre/post comparison through a market turn."""
R["«O5»"] = """we removed **20 duplicated platform-days** and found **6 trading days with zero trades** on one series while the others were normal: the exchange file had not arrived. They are set to **missing, not zero**. Treating them as zero would create fake "drops" on those days, and on a log scale they cannot be analysed at all. Clean: **386 trading days × 4 series** (web, Android, iOS, other brokers), plus 120,000 users in the holdout study."""
R["«O61»"] = """indexed to their pre-launch average, **all four series rise into the 2020 boom and then fall**, including **other brokers, who never had a nudge** (grey). The nudged platforms fall *further*, and each one bends down at its own launch date (dotted lines): web first, then Android, then iOS. This picture is the whole argument: part of the decline is the market (shared by everyone), and part is the nudge (the extra drop at each platform's own launch). A before/after on one platform cannot separate the two."""
R["«O71»"] = """the documented-style comparison shows daily penny trades falling from **16,856 to 6,316: −62.5%** (95% CI −64.1% to −60.9%, even allowing for heavy over-dispersion, φ ≈ 129). It looks precise and decisive. But **other brokers with no nudge fell −46.8% over exactly the same windows**: most of the drop is the market cooling after the speculative peak. The tight CI is no comfort. It measures noise, not bias. **(f) Business meaning:** this is how press-release impact numbers get inflated. The "more than 50%" may be true as a description, but it is not the nudge's effect."""
R["«O72»"] = """
- **ITS on the broker's own series** estimates a level drop of −0.55 log points plus a steeper downward slope, an effect of **−72%** 60 days after launch. That is even worse than pre/post: the pre-launch trend was the *boom* (rising), so projecting it forward makes the counterfactual far too high.
- **Adding other brokers' trades as a market control** shrinks the estimate to **−20%** (CI −30% to −8%; level p = 0.002, slope p = 0.046), which is plausible but imprecise, and it still relies on one series.
- **(f) Business meaning:** ITS is only as good as its counterfactual trend. Through a market turn, a single-series ITS is unreliable; with a control series it becomes a reasonable cross-check."""
R["«O73»"] = """
- **Each platform vs other brokers** (date fixed effects absorb the market cycle completely):
  - **Web −31.4%** (CI −34.1% to −28.5%).
  - **Android −25.8%**.
  - **iOS −27.5%**.
  - Pooled **−28.3%** (CI −30.0% to −26.5%). That is close to the true −30%, recovered three separate times at three different launch dates, which is hard to explain by anything other than the nudge. The platforms differ somewhat (Q = 7.6, p = 0.02).
- **Event study (chart):** the weekly coefficients are near zero before each launch, then fall to about −25% to −33% within two weeks.
- **The formal pre-trend tests reject for Android and iOS** (p < 0.001; web p = 0.09). The pre-launch wobbles are small (at most 4.6–6.4%), but with ~1,500–9,000 trades a day the test can detect even tiny drifts.
- **Robustness:** allowing each platform its own linear trend gives **−25% to −27%**, the same conclusion.
- **(f) Business meaning:** the staggered rollout plus a never-nudged comparison group turns an anecdote into evidence. Parallel trends are never perfect, so always show the size of pre-launch deviations next to the p-value."""
R["«O74»"] = """with fake launch dates (days 140/170/200, before any real nudge), the DiD finds **≈ 0 in 8 of 9 tests** (−2% to +4%, p ≥ 0.33). One placebo, iOS at day 140, shows **+9.8%** (p < 0.001). It has only four pre-weeks of data and sits in the noisiest, smallest series. One false alarm in nine at 5% is not alarming, but it is a reminder that short pre-periods make DiD fragile. By contrast, **naive pre/post on the never-nudged control "finds" −46.8%**: the method itself generates a large fake effect. **Business meaning:** the DiD passes its placebo checks; pre/post fails them badly."""
R["«O75»"] = """
- **The holdout is balanced** (6,011 users, 5.0%; age SMD 0.003).
- **Users who never saw nudges** traded penny stocks **23.5%** of the time in 90 days, vs **16.0%** for nudged users: **−7.5 pp** (CI −8.6 to −6.4; z = −15.3, p ≈ 1e-53), a relative effect of **−31.9%** (CI −35.1% to −28.6%). This matches the true −30% and the DiD.
- **Realised penny-stock losses** are **₹280 lower per user per quarter** (₹576 vs ₹856; CI ₹211–350).
- **(f) Business meaning:** this is the cleanest evidence, with no market assumptions at all. It also directly measures the investor-protection value in ₹."""
R["«O76»"] = """with 1.2 lakh users and a 23% base rate, a **2% holdout** (2,400 users) detects a ~10% relative reduction, and a **5% holdout** (6,000 users) detects ~7%. **Business meaning:** a very small holdout is enough to prove an effect of this size (~30%). Keeping it at 2% for a quarter minimises the number of investors who go without the warning, which addresses the ethical concern."""
R["«O9»"] = """for a broker with **20 lakh active first-time investors** (≈ ₹3,645 average 90-day loss per penny trader, from the holdout):

| Estimate | Investors protected a year | Losses avoided |
|---|---|---|
| **Holdout (best estimate)** | ≈ **6.0 lakh** | ≈ **₹219 crore/year** |
| DiD | ≈ 5.3 lakh | ≈ ₹194 crore/year |
| ITS + control | — | ≈ ₹135 crore/year |
| Naive pre/post | — | ≈ ₹428 crore/year, about **2× overstated** |

- **Reading:** the nudge is valuable on any credible estimate (the documented "tens of crores" is, if anything, an *under*statement at this scale). The point of better methods is not to shrink the good news but to report a number that survives scrutiny by a regulator or a sceptical board.
- Losses avoided are investors' money, not broker revenue. Brokers may even lose some brokerage, which makes the decision an investor-protection choice."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1** rejected: pre/post shows a drop, but it is biased (control −47%).
- **H2:** ITS shows a break only with a market control (−20%).
- **H3 ✅:** DiD −28% (CI −30% to −27%), consistent across three staggered launches and robust to platform trends.
- **H4 ✅:** holdout −32% (p ≈ 1e-53).
- **Conclusion:** the nudge causes a **≈ 30% reduction** in penny-stock trading by first-time investors, not "more than 50%".

**I recommend:**
1. **Keep and extend the nudge** (to F&O for first-time investors, illiquid SME stocks, etc.). It is a cheap, rule-based, highly effective protection.
2. **Measure every such launch credibly:**
   - Roll out in **stages** (by platform, city or user cohort).
   - Benchmark against a **never-treated** group (other brokers' public data, or untreated segments).
   - Keep a **2% randomised holdout** for one quarter.
3. **Report impact as "−30% (holdout), −28% (DiD)",** not a pre/post figure, especially through market turns.
4. **Check displacement:** track total risky activity per user (penny + F&O + other brokers where visible), not just the nudged product.
5. **Automate data hygiene:** treat missing exchange files as missing, never as zero.

**KPIs:** holdout-controlled % reduction in penny trades per first-time investor; DiD estimate per rollout wave; realised losses per user (nudged vs holdout); share of first-time investors who proceed after seeing a nudge; displacement to other risky products."""
