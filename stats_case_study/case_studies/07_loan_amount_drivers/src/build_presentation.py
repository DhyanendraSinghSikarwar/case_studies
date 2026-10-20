"""Build the stakeholder deck for Case Study 07 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/07_loan_amount_drivers/src/build_presentation.py
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
    comp = pd.read_csv(tables / "individual_vs_conditional.csv", index_col=0)
    coef = pd.read_csv(tables / "final_model_coefficients.csv", index_col=0)
    el = pd.read_csv(tables / "income_elasticity_by_employment.csv", index_col=0)
    pq = pd.read_csv(tables / "holdout_prediction_quality.csv", index_col=0)
    prof = pd.read_csv(tables / "profile_predictions.csv", index_col=0)

    emi_ind = comp.loc["existing EMI (per ₹1k)", "individual % effect"]
    emi_cond = comp.loc["existing EMI (per ₹1k)", "conditional % effect"]
    r2_1, r2_f = pq.iloc[0]["holdout R² (log)"], pq.iloc[2]["holdout R² (log)"]
    w1, wf = pq.iloc[0]["80% PI width (high ÷ low)"], pq.iloc[2]["80% PI width (high ÷ low)"]
    purp = {k.split("T.")[1].rstrip("]"): v for k, v in coef["% effect"].items() if k.startswith("loan_purpose")}

    deck = Deck("Case 07 · What drives the loan amount customers request? · synthetic data")
    deck.title_slide("What Really Drives How Much Customers Ask For",
                     "Input to the offer-tier redesign and disbursement forecast · Lending Analytics",
                     "5,000 recent personal-loan applications (requested amounts, before credit decisions). "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: income, purpose and existing debt drive requests; city and age do not",
        [
            f"**Income is the main driver.** 10% more income → about **{(1.1 ** el.loc['Salaried', 'income elasticity'] - 1) * 100:.0f}%** "
            f"bigger request (salaried); more for self-employed (**{(1.1 ** el.loc['Self-employed', 'income elasticity'] - 1) * 100:.0f}%**).",
            f"**Loan purpose matters a lot:** weddings **+{purp['Wedding']:.0f}%**, travel **{purp['Travel']:.0f}%** vs debt consolidation, at the same income.",
            f"**Customers with more existing EMIs ask for LESS** ({emi_cond:+.1f}% per ₹1,000 of EMI), not more, once income is accounted for.",
            "**Metro and older customers only look different because they earn more.** At the same income, no difference.",
            f"**Forecasts get much sharper:** explained share of requests {r2_1:.0%} → **{r2_f:.0%}**; ranges about 20% narrower.",
        ],
        takeaway="Recommendation: tier offers on income, EMI headroom, purpose and job type; drop city tier and age.",
        size=17,
    )
    deck.image("Looked at one by one, everything seems to matter",
               figs / "fig01_individual_relationships.png",
               takeaway="But most of these variables travel together with income. The question is what matters at the SAME income.")
    deck.image("The 'credit-hungry' belief is backwards: at the same income, more debt means a smaller request",
               figs / "fig02_emi_sign_flip.png",
               takeaway=f"On its own, each ₹1,000 of existing EMI goes with {emi_ind:+.1f}% bigger requests, only because richer people carry "
                        f"bigger EMIs. Comparing like with like: {emi_cond:+.1f}%.")
    rows = pd.DataFrame({
        "Belief from the dashboard": ["Metro customers ask for more", "Older customers ask for more",
                                      "Customers with more EMIs ask for more", "Better scores, bigger requests"],
        "On its own": ["Yes (Tier-3 about 31% lower)", "Yes (+1.3% per year)", f"Yes ({emi_ind:+.1f}% per ₹1k)", "Yes"],
        "At the same income, EMIs, purpose…": ["No difference", "No difference", f"Opposite ({emi_cond:+.1f}% per ₹1k)",
                                               "Small effect (≈ +5% per 50 points)"],
    })
    deck.table("Three of four dashboard beliefs do not survive a like-for-like comparison", rows,
               takeaway="City tier and age were stand-ins for income. Using them in offer tiers adds nothing.",
               col_widths=[1.6, 1.4, 1.8], font_size=15)
    deck.image("Loan purpose: one of the strongest and cheapest signals we have",
               figs / "fig04_purpose_effects.png",
               takeaway="Comparisons are with debt consolidation, for customers with the same income, debts and job type.")
    deck.image("Self-employed customers' requests rise faster with income",
               figs / "fig03_interaction_income_employment.png",
               takeaway="One income rule for everyone under-offers high-earning self-employed customers and over-offers low-earning ones.")
    prof_tbl = prof.reset_index().rename(columns={"profile": "Customer (all earn ₹60k/month)", "typical request": "Typical request",
                                                  "80% range": "Most ask between (80%)"})
    deck.table("Same income, very different needs", prof_tbl,
               takeaway="An income-only rule would offer these three customers the same amount.",
               col_widths=[2.6, 1.0, 1.4], font_size=15)
    deck.kpis("Better forecasts for Finance",
              [(f"{r2_1:.0%} → {r2_f:.0%}", "of requests explained", "Tested on applications the model never saw."),
               (f"×{w1:.1f} → ×{wf:.1f}", "width of 80% range", "High end ÷ low end of the range."),
               ("~80%", "range reliability", "The range still contains ~80% of actual requests.")])
    deck.bullets("Recommendations",
                 ["**Redesign offer tiers** on income, existing-EMI headroom, loan purpose and job type.",
                  "**Drop city tier and age** as tiering variables.",
                  "**Retire 'credit-hungry' targeting.** At the same income, indebted customers want less.",
                  "**Use the multi-driver model** for Finance's disbursement forecast.",
                  "**Keep loan tenure out** of these models. It is chosen together with the amount and would mislead."],
                 takeaway="Decision: approve the tier redesign using these drivers.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Associations, not causes.", "Only variables we observe.", "Requested amounts, not approved ones."],
                     "Next steps",
                     ["Model approved amounts and the requested–approved gap.", "Check new bureau variables for overlap (multicollinearity).",
                      "Re-validate on next quarter's applications."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
