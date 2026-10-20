"""Build the stakeholder deck for Case Study 22 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/22_statistical_vs_practical_significance/src/build_presentation.py
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
    ra = pd.read_csv(tables / "experiment_a_results.csv", index_col=0)
    eco = pd.read_csv(tables / "experiment_a_economics.csv", index_col=0)
    rb = pd.read_csv(tables / "experiment_b_results.csv", index_col=0)
    pw = pd.read_csv(tables / "experiment_b_power.csv", index_col=0)
    post = pd.read_csv(tables / "experiment_b_posterior.csv", index_col=0)
    voi = pd.read_csv(tables / "value_of_information.csv", index_col=0)
    tm = pd.read_csv(tables / "type_s_type_m.csv", index_col=0)["value"]
    grade = pd.read_csv(tables / "grading.csv", index_col=0)

    lift_a, lo_a, hi_a = ra.iloc[2]["estimate"], ra.iloc[2]["ci_low"], ra.iloc[2]["ci_high"]
    be_a = eco.loc["BREAK-EVEN", "lift (pp)"]
    net_a = eco.loc["estimate", "net of cost, per year (₹ lakh)"]
    lift_b, lo_b, hi_b, p_b = rb.iloc[2]["estimate"], rb.iloc[2]["ci_low"], rb.iloc[2]["ci_high"], rb.iloc[6]["estimate"]
    power_b = pw.iloc[:, 0].loc[2.0] if 2.0 in pw.index else float("nan")
    p_flat, p_weak = post.iloc[0]["P(lift > break-even)"], post.iloc[1]["P(lift > break-even)"]
    sig_avg = tm.iloc[2]

    deck = Deck("Case 22 · Significant but irrelevant, non-significant but promising · synthetic data")
    deck.title_slide("p = 0.0001 and p = 0.25: Which Experiment Should We Back?",
                     "Statistical vs practical significance · Digital Product analytics",
                     "Two synthetic A/B tests (a checkout redesign and a fee-waiver offer). Synthetic data created for training. "
                     "Not actual customer data.")
    deck.bullets(
        "Summary: the p-values point to exactly the wrong decision on both tests",
        [
            f"**A (redesign): p = 0.0001, but the lift is {lift_a:.2f} points** (95% CI {lo_a:.2f} to {hi_a:.2f}). Break-even is {be_a:.2f} points, so the "
            f"entire interval is below it: **net value about ₹{abs(net_a):.0f} lakh a year lost**.",
            f"**B (fee waiver): p = {p_b:.2f}, but the lift is +{lift_b:.1f} points** (95% CI {lo_b:.1f} to +{hi_b:.1f}) against a break-even of 1.3 points. "
            f"The pilot had only {power_b:.0%} power: a miss was likely even if the offer works.",
            f"**Probability the offer beats break-even: {p_flat:.0%}** (flat prior), {p_weak:.0%} (cautious prior). "
            f"Buying more data is worth about ₹{voi.iloc[2, 0] - voi.iloc[0, 0]:.0f} lakh a year more than launching now.",
            f"**Significant results from small tests exaggerate**: significant pilots average {sig_avg:.1f} points, about twice the true +2.0.",
        ],
        takeaway="Decide on the confidence interval against break-even, not on the p-value.",
        size=16,
    )
    deck.image("A: a large, clean test finds a tiny lift", figs / "fig01_experiment_a.png",
               takeaway=f"3 million visitors make a {lift_a:.2f}-point lift statistically clear (p = 0.0001); that is a 2% relative change.")
    deck.image("A vs break-even: the whole interval sits below what the redesign must earn", figs / "fig02_a_vs_breakeven.png",
               takeaway=f"Break-even {be_a:.2f} points; the upper CI limit is {hi_a:.2f}. Even in the best case the redesign loses money.")
    deck.image("Why p-values mislead: the same tiny effect becomes 'significant' with enough visitors", figs / "fig03_pvalue_vs_n.png",
               takeaway="Significance tracks sample size; business value tracks effect size relative to cost.")
    deck.image("B: the pilot was too small to find even a valuable effect", figs / "fig04_b_power.png",
               takeaway=f"A non-significant result from a study with {power_b:.0%} power says little. Look at the interval ({lo_b:.1f} to +{hi_b:.1f} points).")
    deck.image("B: what the pilot implies for the decision", figs / "fig05_b_posterior.png",
               takeaway=f"P(lift above break-even) is {p_flat:.0%} to {p_weak:.0%}: more likely than not worthwhile, far from certain.")
    rows = pd.DataFrame({"Option": ["Launch now", "Drop now (the p-value advice)", "Bigger test, then decide", "Perfect information (upper bound)"],
                         "Expected value (₹ lakh / year)": [f"{v:.0f}" for v in voi.iloc[:, 0]]})
    deck.table("Value of information: a follow-up test beats both launching and dropping", rows,
               takeaway="When the plausible range spans worthless to valuable and the test is cheap, buy the evidence.",
               col_widths=[4.2, 2.4], font_size=16, highlight_rows=[2])
    deck.image("Significant results in small studies are exaggerated (Type M) and sometimes wrong-signed (Type S)", figs / "fig06_type_m.png",
               takeaway=f"Only {tm.iloc[0]:.0%} of pilots reach p < 0.05; those that do average {sig_avg:.1f} points against a true 2.0.")
    g = grade
    rows2 = pd.DataFrame({"Test": list(g.index), "True lift (pp)": [f"{v:.2f}" for v in g["true lift (pp)"]],
                          "Estimated (pp)": [f"{v:.2f}" for v in g["estimated lift (pp)"]],
                          "True net value (₹ lakh / yr)": [f"{v:+.0f}" for v in g["true net value per year (₹ lakh)"]],
                          "Right call": ["Do not build", "Test further / launch"]})
    deck.table("Grading against the truth: the p-values were wrong twice", rows2,
               takeaway="CIs compared with break-even pointed the right way both times.", col_widths=[2.6, 1.3, 1.4, 2.0, 1.8], font_size=14)
    deck.bullets("Recommendations",
                 ["**Do not build the checkout redesign:** the whole CI is below break-even.",
                  "**Run a follow-up test of the fee waiver** rather than dropping it: about 7,000 per arm to detect the break-even lift (4,000 per arm detects only 1.8 points).",
                  "**Define the break-even lift before the test** and report CIs against it.",
                  "**Report power** with every non-significant result.",
                  "**Replicate** before acting on a significant result from a small test."],
                 takeaway="Decision needed: stop A; fund the B follow-up.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Margins, costs and horizon are assumptions from Finance.", "Visitor split in A is slightly unbalanced (p = 0.004): investigate.",
                      "Lift in A fades after week 1: possible novelty effect."],
                     "Next steps",
                     ["Repeat A's economics with a range of margins.", "Run the B follow-up test.", "Add a holdout to measure long-run effects."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
