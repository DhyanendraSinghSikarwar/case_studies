R = {}
R["«EXEC»"] = """*(Synthetic data built on Paytm Labs' documented formula; Paytm disclosed no A/B results. Written after the analysis.)*

- **The question:** does the one-line Bayesian rule ("the user's own preference × how much a category is trending today vs usual") pick better homepage tiles than simpler or more complex alternatives?
- **Yes, and its edge over a "proper" learned model is large:**

| Rule | Share of next-day clicks landing in the user's top-3 tiles |
|---|---|
| **Bayesian filter** | **60.4%** |
| User habits alone | 60.1% |
| Matrix-factorisation recommender | 51.2% |
| "Show everyone what's trending" | 47.4% |

  All differences are significant (Wilcoxon p < 0.0001, Holm). On a simulated A/B with known true click probabilities, the filter achieves **93% of the best possible** top-3 click-through.
- **But its edge over "user habits alone" is small:** +0.4 pp (≈ +0.26 pp of expected click-through). It comes mostly on **festival and trend days**: +1.25 pp on Dhanteras vs +0.15 pp on normal days (borderline, p = 0.054). Trend weighting is a seasonal booster, not a transformation.
- **Its two dials can be set from data:**
  - The smoothing strength chosen on validation (α = 10 pseudo-clicks) matches the textbook empirical-Bayes estimate (10.9).
  - The best trend window is the **last 1 day**. A 14-day window reacts too late to spikes (−1.2 pp on Dhanteras).
- **Who benefits:** gains are significant for users with 6–60 past clicks. Brand-new users cannot be personalised and get the trending list, which the filter does automatically.
- **₹ (1 crore homepage visits/day; 35% of tile clicks transact; ₹3 take per transaction):**
  - **vs a non-personalised trending homepage:** ≈ **+13 lakh tile clicks/day ≈ ₹50 crore/year**.
  - **vs the learned matrix-factorisation model:** ≈ ₹36 crore/year.
  - **vs habits alone:** ≈ ₹1 crore/year.
  - **Remaining headroom** to a perfect ranking: ≈ ₹18 crore/year.
- **I recommend:**
  - Ship the Bayesian filter (α ≈ 10, 1-day trend window) as the homepage baseline. It is explainable, real-time and robust for sparse users.
  - Keep a random-exploration slot.
  - Require any complex recommender to beat it in a live A/B before replacing it."""
R["«O5»"] = """we removed **2,971 duplicated log rows**, **one bot account** (400 clicks per category per day; it would have dominated "trending" counts) and flagged **day 21 (0-based day 20) as a logging gap**: total clicks were half the 7-day median, so half the events were lost. That day is kept in history but excluded from any evaluation, and this check only works *after* the bot is removed, whose 4,800 daily clicks masked the gap. Clean data: **1.31 million clicks from 49,273 users**. The median user clicked only **15 times in 8 weeks**: thin histories are the norm."""
R["«O61»"] = """
- **Left:** platform trends are sharp and short. Digital gold quadruples its share for 3 days at Dhanteras, movie tickets jump on blockbuster weekends, flights climb for two weeks before Diwali, and FASTag grows steadily. **The test period (shaded) contains most of these festival spikes.**
- **Right:** activity is heavy-tailed. A few users click daily; most click a handful of times. A recommender must work for both, which is why smoothing toward platform shares matters."""
R["«O71»"] = """the validation grid is fairly flat (hit@3 59.5–60.4%), but two choices stand out:
- **Smoothing strength α = 10 is best for every window.** Too little smoothing (α = 0.5) trusts one or two clicks too much; too much (α = 25) washes out personal taste. The **empirical-Bayes estimate from the Dirichlet–multinomial likelihood is α = 10.9**: the data choose the same value without any test-set tuning. That is a principled way to set the dial in production.
- **Trend window w = 1 day** is best, slightly ahead of 3 days. Trends here move fast, so "now" should mean yesterday.

**(f) Business meaning:** the formula has only two settings, both set from data, which makes it easy to explain, monitor and re-tune."""
R["«O72»"] = """over 14 test days and 44,258 active users:
- **Bayesian filter:** hit@3 **60.4%**, NDCG@3 0.505, MRR 0.493 and the best log loss (2.046). Its scores are also the best *probabilities*.
- **vs affinity only (60.1%):** **+0.40 pp per user** (CI +0.27 to +0.53). Wilcoxon p < 0.0001, but the effect size is tiny (rank-biserial 0.08); 12% of users are better off and 11% worse.
- **vs global trending (47.4%):** **+11.1 pp** (rank-biserial 0.52, a large effect).
- **vs matrix factorisation (51.2%):** **+9.2 pp** (rank-biserial 0.49). The rank-4 SVD model blurs individual habits into broad patterns and has no sense of time.
- **(f) Business meaning:** personal history is the main signal, and trend weighting adds a modest, real lift on top. A generic learned recommender is clearly worse here: "start simple" is vindicated."""
R["«O73»"] = """for **brand-new users** (0 clicks), nobody can personalise: the Bayesian filter falls back to the trending list (46.7%, vs 45.3% for affinity, which falls back to *usual* popularity). The +1.4 pp difference is not significant (482 users). For users with **6–20, 21–60 and 60+** clicks the filter's edge over affinity is small but significant (+0.25 to +0.47 pp; q ≤ 0.08). The **gap to "trending only" widens with history**, from +0.5 pp (new users) to +16.1 pp (60+ clicks): the more we know, the more personalisation pays. Matrix factorisation is worst for light users (42% for 1–5 clicks), because it needs data to learn factors."""
R["«O74»"] = """the filter's advantage over affinity peaks exactly on trend days:
- **Dhanteras (days 45–47):** **+0.85, +1.25 and +0.94 pp**.
- **Blockbuster weekend (days 49–51):** smaller gains.
- **Normal days:** around +0.15 pp. The spike-day vs normal-day difference is borderline (Mann–Whitney p = 0.054, only 14 days).
- **On day 52**, just after the spikes end, the filter is *worse* (−0.48 pp): yesterday's trend fades faster than a 1-day window assumes.
- **The 14-day window** reacts too slowly. It loses up to 1.2 pp on Dhanteras vs the 1-day window, while it is close on normal days.

**Business meaning:** the trend term earns its keep during the festival calendar (Diwali, Dhanteras, IPL, big releases), which is also when homepage real estate is most valuable."""
R["«O75»"] = """using the true click probabilities, the expected share of clicks falling in the 3 highlighted tiles is:
- **Bayesian filter:** **60.4%**, which is **93% of the oracle's** 65.3%.
- **Affinity only:** 60.2% (−0.26 pp, CI 0.24–0.27).
- **Matrix factorisation:** 51.2% (−9.3 pp).
- **Global trending:** 47.5% (−13.0 pp).

The twin confirms the offline ranking without day-to-day noise. **The remaining 7% headroom** is mostly users' individual responsiveness to trends, which a single global trend weight cannot capture: the natural next refinement."""
R["«O9»"] = """at **1 crore homepage visits a day** (assumptions: 35% of tile clicks lead to a transaction; ₹3 average take):
- **vs a non-personalised "trending" homepage:** ≈ **+13 lakh tile clicks/day ≈ ₹50 crore/year**.
- **vs the matrix-factorisation recommender:** ≈ +9.3 lakh clicks/day ≈ **₹36 crore/year**.
- **vs habits alone:** ≈ +0.26 lakh clicks/day ≈ **₹1 crore/year**, concentrated in festival weeks.
- **Headroom:** a perfect ranking would add ≈ ₹18.5 crore/year more. That is the most a fancier model could ever win here.
- **Reading:** personalisation itself is worth tens of crores. The trend term is a cheap seasonal top-up. Complexity is not automatically value."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** Bayes beats affinity (+0.40 pp, p < 0.0001), but the effect is small.
- **H2 ✅:** Bayes beats global trending (+11.1 pp).
- **H3 ✅:** Bayes beats matrix factorisation (+9.2 pp).
- **Twin:** 93% of the oracle.

**I recommend:**
1. **Ship the Bayesian trend filter as the homepage baseline** (α ≈ 10 pseudo-clicks, re-estimated monthly by empirical Bayes; 1-day trend window from **organic** clicks, excluding promoted tiles and bots).
2. **Keep a 5% random-exploration slot,** so trend estimates are not driven by what the homepage itself promotes.
3. **Next refinement:** a per-user trend exponent (some users ignore trends), and decay faster after spikes (the day-52 dip).
4. **Gate complex models:** any recommender must beat this baseline in a live A/B on transactions, not just clicks, before replacing it. Use Case 20's propensity × LTV logic for the money metric.
5. **Monitoring:** daily bot and logging-gap checks *before* computing trends (as §5 showed, a bot can hide a data outage).

**KPIs:** top-3 tile CTR and transactions per visit (vs holdout); hit@3 by user-history segment; festival-day lift; share of homepage impressions from exploration; data-quality alerts (bots, gaps)."""
