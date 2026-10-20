---

# Case Study 27 — Rating-fraud detection with Bayesian anomaly scoring (Flipkart, BIRDNEST) · `cs27_fake_review_rating_fraud.ipynb`

## D-27-01: Data source — synthetic ratings with hidden fraud labels and honest look-alikes

- Date: 2026-10-20
- Case: 27
- Context / question: We need ratings, timestamps and a known fraud label to test an unsupervised score.
- Options considered: public review sets (non-Indian, heuristic labels); synthetic data.
- Decision: 80,000 users, 30,000 products, 1,500 sellers, 269,310 clean ratings; 1.34% fraud in five behaviours, plus genuine enthusiasts and batch raters.
- Why: Flipkart's data and expert labels are not public; the documented ratio is about 3 ratings per user.
- Assumption checks / evidence: 27.8% of users have one rating; fraud accounts have 53.3% of gaps under 10 minutes vs 10.6% for honest.
- Impact if wrong / mitigation: Prevalence, star mix and fraud behaviours are assumed; re-measure on expert-labelled data.

## D-27-02: Score — our own expected-KL form of the documented NEST idea, global K = 1

- Date: 2026-10-20
- Case: 27
- Context / question: How do we turn the documented "expected surprise of the posterior" into a score?
- Options considered: K = 1, 2, 3 mixtures; per-view expected KL of the Dirichlet posterior from the global mean, standardised and summed.
- Decision: Global Dirichlet (K = 1) with expected KL per view, each divided by its standard deviation.
- Why: Matches the documented description; BIC prefers K = 2 for stars and K = 3 for time, but the global form is the documented one.
- Assumption checks / evidence: Dirichlet beats multinomial (LR 13,907); star alpha0 = 5.63.
- Impact if wrong / mitigation: The paper's exact formula may differ; this is an implementation of the idea, not the authors' code.

## D-27-03: Do not rely on the plain sum of the two signals

- Date: 2026-10-20
- Case: 27
- Context / question: Does combining star and time signals beat either alone?
- Options considered: stars only, time only, sum, max, raw baselines.
- Decision: Use time score or max(stars, time) for ranking; keep the star signal for defamers.
- Why: AP time only 0.713 and max 0.719 vs sum 0.577 and stars only 0.211; every gap significant (paired bootstrap, Holm p = 0.03).
- Assumption checks / evidence: Boosters are 4/5-star spam, which is normal when 53% of honest ratings are 5 stars; star recall for boosters 0%.
- Impact if wrong / mitigation: Depends on the assumed star mix; test on real data.

## D-27-04: Bayesian shrinkage rather than raw skew

- Date: 2026-10-20
- Case: 27
- Context / question: Is shrinkage for thin-evidence accounts worth the machinery?
- Options considered: raw skew KL; posterior (shrunk) KL.
- Decision: Use the posterior score.
- Why: Raw skew puts 769 of 800 flags on accounts with 1 to 2 ratings, none of them fraud (AP 0.011); the posterior flags none of them.
- Assumption checks / evidence: Fisher p < 1e-300; BIRDNEST precision 0.93 at 10+ ratings.
- Impact if wrong / mitigation: Shrinkage also hides real thin-evidence fraud (stealth recall 4.7%); add seller or device signals.

## D-27-05: Flag by queue depth, not by an FDR-controlled cut-off

- Date: 2026-10-20
- Case: 27
- Context / question: Where do we cut the ranked list?
- Options considered: BH on parametric-bootstrap p-values (5%, 1%), Bonferroni, fixed rank depth.
- Decision: Use a rank-depth queue; use BH list only for automatic action with a second signal.
- Why: BH at 5% flagged 116 accounts, all fraud, recall 10.8%; at 1% none. The null is contaminated and conservative.
- Assumption checks / evidence: Top-1,600 flags give precision 0.41, recall 0.60, 952 honest flagged; batch raters flagged 3.1% vs 1.1%.
- Impact if wrong / mitigation: Re-check the cut-off each cycle with random labels.

## D-27-06: Evidence needed and blind spots are accepted, with other signals

- Date: 2026-10-20
- Case: 27
- Context / question: How many ratings must an account leave to be caught?
- Options considered: power curves for boost, skew-only, burst-only at 0.1% false-positive rate.
- Decision: Accept that 2 to 4 rating and skew-only drip accounts are not caught by this model.
- Why: Power for boosters is 3.6% at 4 ratings, 19.8% at 10, 48.9% at 15, 99.2% at 30; skew-only 0% at every size.
- Assumption checks / evidence: Recall by type in top 1,600: defame 100%, burst-only 85%, boost 63%, skew-only 1.4%, stealth 4.7%.
- Impact if wrong / mitigation: Add seller concentration, device and text features.

## D-27-07: Seller concentration and labels — move to supervised early

- Date: 2026-10-20
- Case: 27
- Context / question: When do labels beat the unsupervised score?
- Options considered: BIRDNEST; gradient boosting on stars and time; plus seller concentration; 500 to 40,000 random labels.
- Decision: Collect random labels every cycle and train a supervised model including seller concentration.
- Why: With 500 labels (10 fraud) AP is 0.649 vs 0.576 for BIRDNEST; with seller concentration 0.732 at 500 and 0.967 at 40,000.
- Assumption checks / evidence: About 113 labels for precision of the top 250 within ±5 points; about 5,664 for prevalence within ±0.3 points.
- Impact if wrong / mitigation: Our labels are perfect and random; real labels are noisy and top-weighted.

## D-27-08: Business case — a short, high-precision review queue

- Date: 2026-10-20
- Case: 27
- Context / question: What is it worth and how deep should review go?
- Options considered: review depth 0.25% to 4% of users, worst/base/best assumptions, scaled to 1 crore rating accounts.
- Decision: Review the top 250 to 400 accounts per 80,000 users (0.3% to 0.5%).
- Why: Base net ₹2.6 crore at the top 0.25% and ₹4.0 crore at 0.5% a year; negative from 1% (₹-4.1 crore); worst case negative, best ₹20.6 to 35.9 crore.
- Assumption checks / evidence: Measured: mean rating shift -0.18 (defamed) and +0.05 (boosted), 59.8% of distortion removed at 400; assumed: GMV, conversion sensitivity, harm share, review cost. Break-even precision 0.86.
- Impact if wrong / mitigation: The rupee level is assumption-driven; the paper gives no impact figure. Validate with a seller-conversion holdback.
