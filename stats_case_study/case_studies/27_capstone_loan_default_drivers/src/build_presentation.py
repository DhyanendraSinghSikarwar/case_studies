"""Build the stakeholder deck for Case Study 27 (capstone) from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/27_capstone_loan_default_drivers/src/build_presentation.py
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
    claims = pd.read_csv(tables / "claims_raw_vs_adjusted.csv", index_col=0)
    met = pd.read_csv(tables / "validation_metrics.csv", index_col=0)
    pol = pd.read_csv(tables / "policy_comparison.csv", index_col=0)
    me = pd.read_csv(tables / "marginal_effects.csv", index_col=0)
    dq = pd.read_csv(tables / "data_cleaning_log.csv")
    rec = pd.read_csv(tables / "coefficient_recovery.csv", index_col=0)

    oot = met.loc["final: out-of-time (2023)"]
    score_only = met.loc["score only (credit score alone), out-of-time", "AUC"]
    p_all, p_agent, p_score, p_model = pol.iloc[0], pol.iloc[1], pol.iloc[2], pol.iloc[3]

    deck = Deck("Case 27 · Capstone: loan default drivers · synthetic data")
    deck.title_slide("What Really Drives Loan Default, and What Should Risk Do?",
                     "A full analysis: data quality to policy · Credit Risk analytics",
                     "24,000 synthetic personal-loan applications, 2022 for development and 2023 for out-of-time testing. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: the three proposed actions treat symptoms; the drivers are affordability and track record",
        [
            f"**The dashboard's claims fall apart once borrowers are compared like with like:** agent channel odds ratio {claims.iloc[0, 0]:.2f} to {claims.iloc[0, 3]:.2f}, "
            f"interest rate {claims.iloc[1, 0]:.2f} to {claims.iloc[1, 3]:.2f}, income {claims.iloc[2, 0]:.2f} to {claims.iloc[2, 3]:.2f}.",
            "**The real drivers:** debt-to-income, loan size relative to income, utilisation, prior delinquency, credit score and employment type.",
            f"**The model ranks well and holds up in a later year:** AUC {oot['AUC']:.3f} out of time (the credit score alone: {score_only:.3f}), nearly calibrated.",
            f"**A model-based approval rule earns ₹{p_model['total profit (₹ lakh)']:.0f} lakh** on 2023 loans, against ₹{p_all['total profit (₹ lakh)']:.0f} lakh approving all and ₹{p_agent['total profit (₹ lakh)']:.0f} lakh under an agent ban.",
        ],
        takeaway="Recommendation: decline the three actions, adopt a probability-based approval rule, recalibrate, and monitor quarterly.",
        size=16,
    )
    drows = pd.DataFrame({"Problem": [r.replace("incomes more than 20 times the median (two extra zeros)", "incomes with two extra zeros") for r in dq["problem"]],
                          "Rows": [f"{int(v):,}" for v in dq["rows affected"]], "Action": list(dq["action"])})
    deck.table("Step 1: the data needed cleaning", drows,
               takeaway="Income is missing more often for the agent channel and self-employed borrowers; a missing credit score signals risk (10.1% default vs 7.3%).",
               col_widths=[3.6, 1.0, 3.2], font_size=13)
    deck.image("Step 2: default rises with debt-to-income, utilisation, loan size and falls with credit score", figs / "fig01_default_by_decile.png",
               takeaway="Default rate by decile of each variable, 95% intervals. City tier and loan amount carry no signal.")
    deck.image("Step 3: the dashboard's claims, raw and adjusted", figs / "fig02_claims_raw_vs_adjusted.png",
               takeaway="Agent borrowers have lower credit scores (627 vs 660); the interest rate is correlated −0.84 with the score. Adjusting leaves little behind.")
    meff = pd.DataFrame({"Change": list(me.index), "Change in default probability (pp)": [f"{v:+.1f}" for v in me.iloc[:, 0]]})
    deck.table("Step 4: what moves the probability of default (baseline 7.7%)", meff,
               takeaway="Percentage-point effects from the logistic model. The agent channel adds about half a point once credit quality is in the model.",
               col_widths=[3.6, 2.4], font_size=14)
    deck.image("Step 5: validation out of time (2023)", figs / "fig04_validation.png",
               takeaway=f"AUC {oot['AUC']:.3f} (CI {oot['AUC low']:.3f} to {oot['AUC high']:.3f}), KS {oot['KS']:.2f}, calibration slope {oot['calibration slope']:.2f}. The agent share rose from 22% to 29% with little drift in scores.")
    prow = pd.DataFrame({"Policy": list(pol.index), "Approved": [f"{v:.0%}" for v in pol["approval rate"]],
                         "Default rate": [f"{v:.1%}" for v in pol["default rate among approved"]],
                         "Profit (₹ lakh)": [f"{v:.0f}" for v in pol["total profit (₹ lakh)"]]})
    deck.table("Step 6: approval policies on 2023 loans (₹6,000 margin, ₹60,000 loss)", prow,
               takeaway="The model-based cut-off beats the agent ban and the score rule of thumb; profit is flat between about 9% and 13%.",
               col_widths=[4.4, 1.2, 1.4, 1.5], font_size=13, highlight_rows=[3])
    deck.image("Profit against the model's cut-off", figs / "fig05_profit_vs_cutoff.png",
               takeaway="The theoretical cut-off (9.1%) is close to the best on the sample. The result rests on the stated margin and loss.")
    deck.bullets(
        "Checking against the truth (training answer key)",
        [f"**{int(rec['CI covers truth'].sum())} of {len(rec)} coefficient intervals contain the true value;** the thin-file coefficient is the one miss.",
         "**The three variables with no real effect** (interest rate, age, income) have intervals containing zero in the kitchen-sink model.",
         "**The ceiling AUC using the true probabilities is 0.798;** the final model is at 0.793.",
         "**The model captures about 95% of the attainable profit.**"],
        takeaway="The drivers are real, the proxies were seen through, and the model is close to the best possible.", size=18)
    deck.bullets("Recommendations",
                 ["**Do not stop agent lending:** underwrite agent loans with the same model; monitor the agent share.",
                  "**Do not raise the minimum income:** use DTI and loan-to-income limits.",
                  "**Do not price harder on rate segments:** price on the model's probability of default.",
                  "**Adopt the probability-based approval rule** (cut-off about 9% to 13%) and recalibrate before pricing.",
                  "**Monitor quarterly:** calibration, PSI, agent share, default by channel."],
                 takeaway="Decision needed: approve the model-based rule for a controlled rollout.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Observational: 'drivers' means associated after adjustment.", "Costs and margins are assumptions.", "One out-of-time year.",
                      "Synthetic data; no answer key in real life."],
                     "Next steps",
                     ["Randomised cut-off test on borderline applications.", "Bureau and behavioural data.", "Challenger model compared out of time.", "Fairness and compliance review."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
