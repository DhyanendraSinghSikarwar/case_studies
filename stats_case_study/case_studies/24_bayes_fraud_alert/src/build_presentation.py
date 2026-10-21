"""Build the stakeholder deck for Case Study 24 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/24_bayes_fraud_alert/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    perf = pd.read_csv(tables / "screen_performance.csv", index_col=0)
    chan = pd.read_csv(tables / "ppv_by_channel.csv", index_col=0)
    pat = pd.read_csv(tables / "alert_patterns.csv", index_col=0)
    pol = pd.read_csv(tables / "policy_costs.csv", index_col=0)
    mg = pd.read_csv(tables / "merchant_group_estimates.csv", index_col=0)
    shr = pd.read_csv(tables / "shrinkage_grading.csv", index_col=0)
    prior = pd.read_csv(tables / "prior_sensitivity.csv", index_col=0)
    summ = pd.read_csv(tables / "results_summary.csv", index_col=0)["Value"]

    r = perf.loc["Rule engine"]
    sens, ppv = r["sensitivity P(alert|fraud)"], r["PPV P(fraud|alert)"]
    ppv_lo, ppv_hi = r["PPV CI low"], r["PPV CI high"]
    both, one_r, one_m = pat.loc["both alert"], pat.loc["rule only"], pat.loc["ML only"]
    block_all = pol.iloc[1]
    best = pol.iloc[3]
    top_p = mg["P(rate > 1%)"].sort_values(ascending=False)

    deck = Deck("Case 24 · A fraud alert fired · synthetic data")
    deck.title_slide("The Rule Catches 85% of Fraud. So Why Are 88% of Its Alerts Wrong?",
                     "Base rates, Bayes' theorem and small-group estimates · Fraud Operations analytics",
                     "150,000 synthetic card and UPI transactions with two screens and a confirmed outcome. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: an alert is a probability, not a verdict",
        [
            f"**The rule catches {sens:.0%} of fraud, but when it fires only {ppv:.0%} of alerts are fraud** (95% CI {ppv_lo:.0%} to {ppv_hi:.0%}). "
            "Fraud is 0.42% of transactions, so false alarms from the 99.6% genuine outnumber true alerts about 7 to 1.",
            f"**Where the alert fires matters:** the same rule has a PPV of {chan.loc['Card present', 'PPV']:.0%} for card-present, "
            f"{chan.loc['UPI', 'PPV']:.0%} for UPI and {chan.loc['Card not present', 'PPV']:.0%} for card-not-present, because the base rate differs about 6-fold.",
            f"**When both screens fire, fraud is {both['observed P(fraud)']:.0%} likely**; one alone gives about {one_r['observed P(fraud)']:.1%}. "
            "The two screens are independent here, so their evidence multiplies.",
            f"**Blocking every rule alert costs ₹{block_all['total cost (₹ lakh)']:.0f} lakh** and blocks {int(block_all['genuine customers blocked']):,} genuine customers. "
            f"A probability-based policy costs ₹{best['total cost (₹ lakh)']:.0f} lakh and blocks {int(best['genuine customers blocked'])}.",
        ],
        takeaway="Recommendation: investigate single alerts where the probability clears 2.5%, block only on combined evidence.",
        size=16,
    )
    deck.image("Out of every 100,000 transactions, who is in the alert queue?", figs / "fig01_natural_frequencies_and_ppv.png",
               takeaway=f"About 360 true alerts and 2,630 false ones. The PPV rises with the base rate: {ppv:.0%} today, 50% only if fraud were about 3% of transactions.")
    deck.image("The same rule means different things in different channels", figs / "fig02_ppv_by_channel.png",
               takeaway="Card-present transactions generate 39% of all alerts at the lowest PPV.")
    rows = pd.DataFrame({
        "Alert pattern": ["Neither", "Rule only", "ML score only", "Both"],
        "Transactions": [f"{int(pat.loc[k, 'transactions']):,}" for k in ["neither", "rule only", "ML only", "both alert"]],
        "Fraud rate": [f"{pat.loc[k, 'observed P(fraud)']:.2%}" for k in ["neither", "rule only", "ML only", "both alert"]],
        "Predicted by Bayes": [f"{pat.loc[k, 'Bayes prediction (independence)']:.2%}" for k in ["neither", "rule only", "ML only", "both alert"]],
    })
    deck.table("A second alert multiplies the evidence", rows,
               takeaway="The prediction from multiplying the screens' likelihood ratios matches what was observed. This holds only because the screens are independent.",
               col_widths=[2.2, 1.6, 1.4, 1.8], font_size=15, highlight_rows=[3])
    deck.image("What if the screens overlap? The combined evidence shrinks fast", figs / "fig03_two_alerts.png",
               takeaway="If only 70% of the evidence is independent, P(fraud | both alert) falls from 85% to 39%. Test independence before chaining screens.")
    prow = pd.DataFrame({
        "Policy": list(pol.index),
        "Cost (₹ lakh)": [f"{v:.1f}" for v in pol["total cost (₹ lakh)"]],
        "Frauds stopped": [f"{int(v)}" for v in pol["frauds stopped"]],
        "Genuine blocked": [f"{int(v):,}" for v in pol["genuine customers blocked"]],
    })
    deck.table("Decisions from probabilities: investigate above 2.5%, block above 11%", prow,
               takeaway="Costs are assumptions (₹300 per investigation, ₹12,000 per fraud, ₹1,500 per wrongly blocked customer). Policy thresholds were set on the same data, so its edge is somewhat optimistic.",
               col_widths=[4.6, 1.2, 1.2, 1.4], font_size=13, highlight_rows=[3])
    deck.image("Small merchant groups: raw rates are mostly noise", figs / "fig04_beta_binomial_shrinkage.png",
               takeaway=f"Group G (3 frauds in 189 transactions) has the highest raw rate, 1.6%, but its estimate falls to 0.8% once it borrows strength from the other groups.")
    deck.bullets(
        "Which groups are really worse than average?",
        [f"**Probability each group exceeds a 1% fraud rate:** N {top_p.iloc[0]:.0%}, J {top_p.iloc[1]:.0%}, G {top_p.iloc[2]:.0%}. No group is beyond reasonable doubt.",
         f"**The prior matters for tiny groups:** for G a flat prior gives {prior.iloc[0, 3]:.0%} probability of exceeding 1%, the data-based prior {prior.iloc[1, 3]:.0%}.",
         f"**Shrinkage is better on average, not always:** on this one set of 14 groups it did not beat the raw rates "
         f"(squared error {shr.iloc[1, 0]:.1f} for shrinkage vs {shr.iloc[0, 0]:.1f} for raw rates, ×10⁻⁶). Over 3,000 simulated sets it won 71% of the time."],
        takeaway="Report probabilities and intervals for small groups, not a raw league table.",
        size=17,
    )
    deck.bullets("Recommendations",
                 ["**Report the PPV and alert volume** to operations, not just the catch rate.",
                  "**Do not block on a single alert.** Investigate in card-not-present, and block when both screens agree.",
                  "**Use channel-specific thresholds:** the base rate differs about 6-fold.",
                  "**Check independence** before chaining screens; track PPV and base rate monthly.",
                  "**Monitor merchant groups with posterior probabilities,** not raw rates."],
                 takeaway="Decision needed: approve the investigate-then-block policy for a pilot.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Costs are assumptions; blocking costs include hard-to-measure attrition.", "Fraudsters adapt, so rates drift.",
                      "Labels arrive after about 60 days.", "Real screens usually share signals."],
                     "Next steps",
                     ["Build a calibrated model that outputs P(fraud) directly.", "Monitor base rate and PPV monthly.",
                      "Model both alerts jointly with channel.", "Hierarchical model for merchant groups."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
