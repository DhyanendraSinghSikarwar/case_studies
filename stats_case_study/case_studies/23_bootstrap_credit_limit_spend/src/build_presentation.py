"""Build the stakeholder deck for Case Study 23 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/23_bootstrap_credit_limit_spend/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def sgn(v: float, d: int = 0) -> str:
    return f"{'−' if v < 0 else '+'}{abs(v):,.{d}f}"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    t = pd.read_csv(tables / "main_test_intervals.csv", index_col=0)
    desc = pd.read_csv(tables / "descriptives.csv", index_col=0)
    cov = pd.read_csv(tables / "coverage_simulation.csv")
    fail = pd.read_csv(tables / "bootstrap_failures.csv", index_col=0).iloc[:, 0]
    grd = pd.read_csv(tables / "interval_grading.csv")
    rev = pd.read_csv(tables / "revenue_impact.csv", index_col=0)

    mean_d, med_d, med_r, util = (t.loc[k] for k in ["difference in means (₹)", "difference in medians (₹)", "ratio of medians",
                                                       "difference in spend per rupee of limit (pp)"])
    big_share = t.loc["difference in share over ₹50,000 (pp)"]
    pilot_cov = grd[grd["data"].str.startswith("pilot")]["BCa CI covers?"].sum()
    main_cov = grd[grd["data"] == "main test"]["BCa CI covers?"].sum()
    c30 = cov[cov["n"] == 30].set_index("interval")["coverage"]

    deck = Deck("Case 23 · Credit-limit increase and spend · synthetic data")
    deck.title_slide("What Did a 25% Credit-Limit Increase Do to Spend?",
                     "Bootstrap confidence intervals for skewed metrics · Credit Cards analytics",
                     "Randomised test of 2,500 vs 2,500 customers and a 60 vs 60 regional pilot. Synthetic data created for training. "
                     "Not actual customer data.")
    deck.bullets(
        "Summary: typical spend is up and utilisation is down; total spend is too noisy to call",
        [
            f"**Typical (median) spend rose about {med_r['estimate'] - 1:.0%}**, ₹{med_d['estimate']:,.0f} per month (95% interval ₹{med_d['BCa low']:,.0f} to ₹{med_d['BCa high']:,.0f}).",
            f"**Average spend rose ₹{mean_d['estimate']:,.0f}, but the interval runs from {sgn(mean_d['BCa low'])} to {sgn(mean_d['BCa high'])}** "
            f"and includes zero: a few very large spenders dominate the mean.",
            f"**Spend per rupee of limit fell {abs(util['estimate']):.1f} points** (interval {sgn(util['BCa low'], 1)} to {sgn(util['BCa high'], 1)}): the limit rose 25%, spend far less.",
            f"**The 60 vs 60 regional pilot should not guide decisions:** its estimates are several times too large and its intervals cover the truth for only {pilot_cov} of 7 metrics.",
        ],
        takeaway="Recommendation: quote medians and utilisation as firm results, the mean with its wide interval, and rerun the pilot at scale.",
        size=16,
    )
    deck.image("Spend is extremely skewed: a few customers hold a large share", figs / "fig01_spend_distribution.png",
               takeaway=f"Mean is {desc.loc['mean', 'control'] / desc.loc['median', 'control']:.1f} times the median; the top 1% of customers hold {desc.loc['top 1% share of total spend', 'control']:.0%} of spend.")
    rows = pd.DataFrame({
        "Metric": ["Average spend (₹)", "Typical (median) spend (₹)", "Ratio of medians", "Share spending over ₹50,000 (pp)", "Spend per rupee of limit (pp)"],
        "Effect": [f"{sgn(mean_d['estimate'])}", f"{sgn(med_d['estimate'])}", f"{med_r['estimate']:.2f}", f"{sgn(big_share['estimate'], 1)}", f"{sgn(util['estimate'], 1)}"],
        "95% interval": [f"{sgn(mean_d['BCa low'])} to {sgn(mean_d['BCa high'])}", f"{sgn(med_d['BCa low'])} to {sgn(med_d['BCa high'])}",
                         f"{med_r['BCa low']:.2f} to {med_r['BCa high']:.2f}", f"{sgn(big_share['BCa low'], 1)} to {sgn(big_share['BCa high'], 1)}",
                         f"{sgn(util['BCa low'], 1)} to {sgn(util['BCa high'], 1)}"],
        "Clear?": ["No", "Yes", "Yes", "No", "Yes"],
    })
    deck.table("One experiment, five metrics, very different certainty", rows,
               takeaway="The bootstrap gives an interval for any metric. The width reflects the metric, not the method.",
               col_widths=[3.0, 1.3, 2.6, 0.9], font_size=14)
    deck.image("The bootstrap: resample the customers, recompute, read off the interval", figs / "fig02_bootstrap_distributions.png",
               takeaway="With 2,500 per arm, the percentile and BCa intervals nearly coincide.")
    deck.image("The 60 vs 60 pilot overstates every effect and its intervals are very wide", figs / "fig03_main_vs_pilot.png",
               takeaway=f"BCa intervals cover the truth for {main_cov} of 7 metrics in the main test and {pilot_cov} of 7 in the pilot. The pilot's mean difference (+₹12,600) is about six times the main test's.")
    deck.image("Does the bootstrap deserve trust? A coverage check on skewed data", figs / "fig04_coverage.png",
               takeaway=f"For the mean at n = 30, a nominal 95% interval contains the truth {c30['mean: t']:.0%} (t), {c30['mean: percentile']:.0%} (percentile), "
                        f"{c30['mean: BCa']:.0%} (BCa) and {c30['mean: bootstrap-t']:.0%} (bootstrap-t) of the time.")
    deck.bullets(
        "Where the bootstrap fails",
        [f"**Extremes:** an interval for the maximum never contains the true maximum ({fail.iloc[0]:.0%}).",
         f"**Tiny samples:** with 8 skewed values, coverage is {fail.iloc[1]:.0%}.",
         f"**Dependent data:** for an autocorrelated series the standard bootstrap covers {fail.iloc[2]:.0%}; resampling blocks restores {fail.iloc[3]:.0%}.",
         "**Resample the unit of randomisation** (customer, branch, day), within each experiment arm."],
        takeaway="The bootstrap is a large-sample tool that is more flexible than normal theory, not a cure for small samples.",
        size=18,
    )
    deck.bullets(
        "Revenue: the number Finance wants is the noisiest one",
        [f"At 1.6% interchange, the mean difference is about ₹{rev.iloc[1, 1]:,.0f} extra annual interchange per customer.",
         f"The interval runs from {sgn(rev.iloc[0, 1])} to {sgn(rev.iloc[2, 1])} per customer, so a loss cannot be ruled out.",
         "This ignores the extra credit-risk cost of larger limits and the fall in utilisation."],
        takeaway="A bigger test, or adjusting for prior spend, is needed before quoting revenue.",
        size=18,
    )
    deck.bullets("Recommendations",
                 ["**Report the median effect** (about +9%) and the utilisation fall as firm evidence of behaviour change.",
                  "**Report the mean with its interval,** not as a point estimate.",
                  "**Do not use the 60 vs 60 pilot to decide;** rerun it at scale or pool regions.",
                  "**Add a credit-loss outcome** to the next test before rolling out.",
                  "**Bootstrap by customer within each arm,** and use BCa for medians and ratios."],
                 takeaway="Decision needed: approve a larger follow-up test with delinquency tracked.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Three months of outcome only.", "Revenue ignores credit-risk costs.", "Customers assumed independent."],
                     "Next steps",
                     ["Adjust for prior spend to shrink the interval.", "Estimate effects by risk segment.", "Bootstrap net revenue including losses."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
