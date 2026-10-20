"""Build the stakeholder deck for Case Study 21 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/21_cashback_churn_causality/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def sg(v: float, d: int = 1) -> str:
    return f"{'−' if v < 0 else '+'}{abs(v):.{d}f}"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    naive = pd.read_csv(tables / "naive_difference.csv", index_col=0).iloc[0]
    ladder = pd.read_csv(tables / "adjustment_ladder.csv", index_col=0)
    ipw = pd.read_csv(tables / "propensity_weighting.csv", index_col=0).iloc[0]
    pil = pd.read_csv(tables / "pilot_results.csv", index_col=0)
    grade = pd.read_csv(tables / "grading.csv", index_col=0)
    econ = pd.read_csv(tables / "decision_economics.csv", index_col=0)
    ev = pd.read_csv(tables / "e_values.csv", index_col=0)
    churn = pd.read_csv(tables / "churn_by_enrolment.csv", index_col=0)

    itt, comp = pil.iloc[0], pil.iloc[1]
    truth = grade["truth it targets (pp)"].iloc[0]
    n_ok = int(grade["CI covers the truth?"].iloc[:7].sum())

    deck = Deck("Case 21 · Does cashback reduce churn? · synthetic data")
    deck.title_slide("Does Cashback Cut Churn by Two Thirds?",
                     "Association, selection and what a randomised pilot says · Cards retention analytics",
                     "20,000 self-selected customers and a randomised pilot of 16,000. Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: the 19-point gap is mostly who signs up, not what cashback does",
        [
            f"**Enrolled customers churn {churn.loc[1, 'churn rate']:.0%} against {churn.loc[0, 'churn rate']:.0%}**, a {naive['difference (pp)']:.1f}-point gap. "
            "That is an association, not an effect.",
            "**Enrolled customers were already different:** more engaged, spending more, with a rising spend trend. Adjusting for what we can see "
            f"cuts the gap to {ladder['effect among enrolled (pp)'].iloc[3]:.1f} points and weighting to {ipw['estimate (pp)']:.1f}.",
            f"**The randomised pilot says:** offering cashback cuts churn by {abs(itt['estimate (pp)']):.1f} points, and enrolling by about {abs(comp['estimate (pp)']):.0f} points "
            f"(CI {abs(comp['ci_high']):.0f} to {abs(comp['ci_low']):.0f}).",
            f"**At current costs, break-even needs {7.5:.1f} points,** so cashback loses money on the real effect and only looks profitable on the naive number.",
        ],
        takeaway="Recommendation: do not push cashback to the whole base; keep it voluntary and test cheaper variants with a randomised offer.",
        size=16,
    )
    deck.image("Who signs up? Engaged customers, before they ever enrol", figs / "fig01_balance.png",
               takeaway="Enrolled customers differ strongly on logins, spend and spend trend. In the randomised pilot those differences disappear.")
    rows = pd.DataFrame({
        "What we compared": ["Enrolled vs not (no controls)", "+ tenure, income, complaints", "+ spend and logins", "+ spend trend before decision", "Propensity weighting"],
        "Churn effect (pp)": [sg(ladder["effect among enrolled (pp)"].iloc[i]) for i in [0, 1, 2, 3]] + [sg(ipw["estimate (pp)"])],
    })
    deck.table("Adjusting for what we can see: the estimate shrinks, then stalls", rows,
               takeaway="Every row has a narrow confidence interval, and none of them contains the true effect. Adjustment cannot remove what we cannot measure.",
               col_widths=[4.2, 1.6], font_size=15)
    deck.image("Overlap: the customers most likely to enrol have few look-alikes among non-enrolled customers", figs / "fig02_propensity_overlap.png",
               takeaway="Weighting balances measured variables only.")
    deck.kpis("What the randomised pilot says",
              [(sg(itt["estimate (pp)"]), "Effect of the OFFER", f"95% CI {sg(itt['ci_low'])} to {sg(itt['ci_high'])}; whole offered group"),
               ("55.8%", "Take-up", "share of offered customers who enrolled"),
               (sg(comp["estimate (pp)"]), "Effect of ENROLLING", f"95% CI {sg(comp['ci_low'])} to {sg(comp['ci_high'])}; offer effect ÷ take-up"),
               (sg(pil.iloc[2]["estimate (pp)"]), "Invalid in-pilot comparison", "enrolled vs not: selection again")],
              takeaway="Only the first, second and third numbers are protected by the lottery.")
    deck.image(f"Which estimates bracket the truth? Only {int(grade['CI covers the truth?'].iloc[1:].sum())} of {len(grade) - 1} adjusted or pilot intervals do", figs / "fig03_estimates_vs_truth.png",
               takeaway=f"True effect among enrolled customers: {sg(truth)} points. The pilot's complier estimate contains it; the adjusted estimates miss it.")
    deck.bullets(
        "How strong would a hidden factor have to be?",
        [f"The naive result would need a hidden factor with a risk ratio of about **{ev.loc['Naive', 'E-value']:.0f}** with both enrolment and churn.",
         f"The adjusted result would need only about **{ev.loc['Adjusted (model 4)', 'E-value']:.1f}**.",
         "Engagement and intention to leave plausibly clear that bar: spend trend alone differs by more than a full standard deviation between enrolled and not."],
        takeaway="The E-value measures how much hidden bias a claim must survive. It does not remove the bias.",
        size=18,
    )
    erow = pd.DataFrame({"Basis": list(econ.index),
                         "Churn reduction (pp)": [f"{v:.1f}" for v in econ["churn reduction (pp)"]],
                         "Net per enrolled customer (₹)": [f"{v:+,.0f}".replace("-", "−") for v in econ["net per enrolled customer (₹)"]] if "net per enrolled customer (₹)" in econ.columns
                         else [f"{v:+,.0f}".replace("-", "−") for v in econ.iloc[:, -1]]})
    deck.table("The wrong estimate flips the decision (assumes ₹450 cost, ₹6,000 per churner, break-even 7.5 points)", erow,
               takeaway="Costs and margins are assumptions for Finance. On the real effect cashback does not pay at today's cost.",
               col_widths=[3.0, 1.6, 2.2], font_size=15, highlight_rows=[1])
    deck.bullets("Recommendations",
                 ["**Do not move retention budget into cashback** on the observational numbers.",
                  "**Keep it voluntary** and cut the cost per customer or find a cheaper design.",
                  "**Randomise the offer** in any further test or rollout, with a holdout.",
                  "**Describe results precisely:** 'associated with' for the observational gap, 'reduces' only for the pilot.",
                  "**Look for who benefits** with a larger, segmented test."],
                 takeaway="Decision needed: approve a randomised follow-up test of cheaper cashback levels.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Costs and margins are assumptions.", "The complier effect covers customers who enrol when offered.",
                      "12-month follow-up only.", "Synthetic data with a known hidden confounder."],
                     "Next steps",
                     ["Multi-level cashback test.", "Heterogeneous effects from the pilot.", "Permanent holdout group.",
                      "Quasi-experimental designs where randomising is impossible."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides); adjusted/pilot intervals covering truth: {n_ok}")


if __name__ == "__main__":
    main()
