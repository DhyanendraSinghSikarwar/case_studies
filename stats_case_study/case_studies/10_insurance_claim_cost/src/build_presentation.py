"""Build the stakeholder deck for Case Study 10 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/10_insurance_claim_cost/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    hold = pd.read_csv(tables / "holdout_comparison.csv", index_col=0)
    res = pd.read_csv(tables / "reserve_range.csv", index_col=0)
    gam = pd.read_csv(tables / "log_ols_vs_gamma.csv", index_col=0)
    top = pd.read_csv(tables / "top_cooks_distance.csv", index_col=0)

    eff = gam["gamma % effect"]
    best = res.iloc[0]["₹ crore"]
    lo, hi, p995 = res.iloc[2]["₹ crore"], res.iloc[3]["₹ crore"], res.iloc[4]["₹ crore"]
    naive = hold.loc["B: log-OLS, naive exp()", "total vs actual (%)"]
    uncapped = hold.loc["C: gamma GLM", "total vs actual (%)"]
    capped = hold.loc["C: gamma GLM + cap", "total vs actual (%)"]
    n_err = int(top["claim > sum insured?"].sum())

    deck = Deck("Case 10 · Modelling health claim cost · synthetic data")
    deck.title_slide("A Claim-Cost Model We Can Defend",
                     "Pricing relativities and reserves for open claims · Analytics for the Appointed Actuary",
                     "6,000 settled hospitalisation claims; 1,500 held back to test reserving. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: the current model is the wrong shape; a gamma model with the policy cap gets the reserve right",
        [
            f"**{n_err} claims were keyed in paise instead of rupees** (×100). They dominated the old model.",
            "**Claim costs are multiplicative and their spread grows with their size.** A straight-line model on ₹ cannot "
            "capture that: it even predicts negative costs.",
            f"**The log model under-reserved by {abs(naive):.0f}%** because exp() of a log prediction gives a typical claim, "
            "not the average.",
            f"**Recommended: a gamma model that respects the sum insured.** On 1,500 test claims its total was within "
            f"{abs(capped):.1f}% of what was actually paid.",
            f"**Reserve for open claims: ≈ ₹{best:.1f} crore**, 90% range ₹{lo:.1f}–{hi:.1f} crore.",
        ],
        takeaway="Decision needed: adopt the gamma model for pricing and reserving, and add a sum-insured validation rule.",
        size=16,
    )
    deck.image("Claim costs: a long tail of expensive claims, very different by procedure",
               figs / "fig01_claim_distribution.png",
               takeaway="On a log scale the distribution is roughly symmetric, a sign that effects multiply rather than add.")
    deck.table("Six impossible claims: above the policy's maximum payout",
               top.loc[top["claim > sum insured?"], ["procedure_category", "sum_insured", "claim_amount"]]
               .assign(sum_insured=lambda d: d["sum_insured"].map(lambda v: f"₹{v / 1e5:,.0f} lakh"),
                       claim_amount=lambda d: d["claim_amount"].map(lambda v: f"₹{v / 1e5:,.1f} lakh"))
               .rename(columns={"procedure_category": "Procedure", "sum_insured": "Sum insured", "claim_amount": "Recorded claim"})
               .reset_index().rename(columns={"claim_id": "Claim"}),
               takeaway="Divided by 100 they become normal amounts: keyed in paise. Removed and sent to the claims-data team.",
               col_widths=[1.4, 1.6, 1.0, 1.2], font_size=14)
    deck.image("The old model's checks fail: spread grows with claim size, and big claims are far off",
               figs / "fig03_diagnostics_raw_clean.png",
               takeaway="Top-left: a funnel. Top-right: far more very large claims than the model expects. Its error bars cannot be trusted.")
    deck.image("Why a gamma model: the variance of claims grows with the square of their average",
               figs / "fig05_mean_variance.png",
               takeaway="Bigger claims are not 'more random' in % terms; they are just bigger. That is exactly what a gamma model assumes.")
    deck.bullets("Why the log model under-reserved",
                 ["A log model predicts the **typical** (median) claim. For skewed costs, the **average** is higher.",
                  f"Reserves need the average. Taking the prediction at face value under-reserved by **{abs(naive):.0f}%** on the test claims.",
                  "A correction factor (≈ 1.23) fixes the average, but the result still ignores the policy limit.",
                  f"Models that ignore the sum-insured cap **over-reserve by about {uncapped:.0f}%**: we never pay above the limit."],
                 takeaway="The gamma model predicts the average directly, and we apply the cap to every claim.")
    deck.image("On 1,500 test claims: only the gamma model with the cap gets the total right",
               figs / "fig09_holdout_calibration.png",
               takeaway=f"Total error: naive log {naive:+.0f}%, gamma without cap {uncapped:+.0f}%, gamma with cap {capped:+.1f}%. "
                        "Within procedures, errors of up to ~10% remain (small groups).")
    rel = pd.DataFrame({
        "Factor": ["Cardiac (vs medical management)", "Oncology", "Orthopaedic", "Suite (vs general ward)", "Private room",
                   "Non-network hospital (vs network-metro)", "Diabetic", "Smoker", "Double the length of stay"],
        "Cost difference": [f"{eff['procedure_category[T.Cardiac]']:+.0f}%", f"{eff['procedure_category[T.Oncology]']:+.0f}%",
                            f"{eff['procedure_category[T.Orthopaedic]']:+.0f}%", f"{eff['room_type[T.Suite]']:+.0f}%",
                            f"{eff['room_type[T.Private]']:+.0f}%", f"{eff['hospital_type[T.Non-network]']:+.0f}%",
                            f"{eff['diabetic']:+.0f}%", f"{eff['smoker']:+.0f}%",
                            f"{100 * (2 ** gam.loc['log_los', 'gamma GLM coef'] - 1):+.0f}%"],
    })
    deck.table("Pricing relativities from the gamma model (for similar patients and hospitals)", rel,
               takeaway="Associations, not causes: e.g. non-network patients may also differ in ways we don't observe.",
               col_widths=[3.0, 1.2], font_size=14)
    deck.image(f"Reserve for the 1,500 open claims: about ₹{best:.1f} crore",
               figs / "fig10_reserve_range.png",
               takeaway=f"90% range ₹{lo:.1f}–{hi:.1f} crore; 99.5th percentile ₹{p995:.1f} crore. The total is far more "
                        "predictable than any single claim.")
    deck.bullets("Recommendations",
                 ["**Adopt the gamma model** (with the sum-insured cap) for pricing relativities and open-claim reserves.",
                  f"**Reserve ≈ ₹{best:.1f} crore** for the open claims; base the risk margin on the simulated range.",
                  "**Retire the straight-line ₹ model**; do not use the log model without correction.",
                  "**Add a load-time rule:** reject claim amounts above the sum insured.",
                  "**Review calibration by procedure every quarter.**"],
                 takeaway="Decision needed: approve the gamma model and the reserve.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Real portfolios have rarer, larger claims than a gamma model expects.",
                      "No claim inflation or late-reported claims included.",
                      "Relativities are associations, not causes."],
                     "Next steps",
                     ["Test a separate large-claim model above a threshold.",
                      "Add inflation and late-reporting adjustments with the reserving team.",
                      "Track calibration by procedure each quarter."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
