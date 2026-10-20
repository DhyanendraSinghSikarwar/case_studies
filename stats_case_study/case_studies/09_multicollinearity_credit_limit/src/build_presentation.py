"""Build the stakeholder deck for Case Study 09 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/09_multicollinearity_credit_limit/src/build_presentation.py
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
    q = pd.read_csv(tables / "quarterly_income_coefficients.csv", index_col=0)
    vif = pd.read_csv(tables / "vif_full_model.csv", index_col=0)
    pb = pd.read_csv(tables / "pilot_prediction_bias.csv", index_col=0)
    rem = pd.read_csv(tables / "remedies_comparison.csv", index_col=0)
    cv = pd.read_csv(tables / "cv_prediction_accuracy.csv", index_col=0)

    qq = q.iloc[:4]
    full_err = pb.loc["Full (both income signals)", "mean error (actual vs predicted, %)"]
    q_err = pb.filter(like="fitted on", axis=0)["mean error (actual vs predicted, %)"]
    limit_low = 100 * (1 - 1 / (1 + full_err / 100))

    deck = Deck("Case 09 · Overlapping signals in the credit-limit model · synthetic data")
    deck.title_slide("Why Our Spend Model's Coefficients Keep Jumping",
                     "Credit-limit model review · Credit Risk for the Head of Cards",
                     "4,000 salaried card customers (four quarterly cohorts) and 600 self-employed pilot customers. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: the model's limits are fine; its coefficients are not readable, and it is not ready for the pilot",
        [
            "**Declared income and salary credits are near-copies** for salaried customers (correlation 0.996). "
            "The model cannot tell them apart, so their separate coefficients swing every quarter.",
            f"**Their combined effect is stable:** 10% more income → about **{10 * qq['b SUM'].mean():.0f}%** more spend, every quarter.",
            "**Limits did not jump around.** Predictions for salaried customers are stable and accurate.",
            f"**Self-employed pilot: not ready.** Their salary credits understate income, so the model predicts spend too low: "
            f"limits would be about **{limit_low:.0f}% too low**.",
        ],
        takeaway="Recommendation: replace the two income columns with one income index; build a separate model for the pilot.",
        size=17,
    )
    deck.image("Two columns, one piece of information",
               figs / "fig02_two_income_signals.png",
               takeaway="For salaried customers, the salary is paid into their account: declared income and credits match. "
                        "For self-employed customers they do not.")
    deck.image("Each quarter splits the income effect differently; the total never changes",
               figs / "fig03_quarterly_coefficients.png",
               takeaway=f"Q4's negative salary-credits coefficient ({qq.loc['2025-Q4', 'b credits']:+.2f}) is noise: its range runs well into positive values.")
    deck.table("'Neither income variable is significant' (Q2) does not mean income doesn't matter",
               pd.DataFrame({"Test (Q2 customers)": ["Declared income, on its own", "Salary credits, on its own",
                                                     "Both together"],
                             "Result": [f"p = {qq.loc['2025-Q2', 'p declared']:.2f}: not significant",
                                        f"p = {qq.loc['2025-Q2', 'p credits']:.2f}: not significant",
                                        f"p < 0.001: strongest signal in the model"]}),
               takeaway="Each test asks 'does this add anything beyond the other one?'. With two near-copies, the answer is no for each, "
                        "but together they matter most. Always test overlapping variables together.",
               col_widths=[2.0, 2.4], font_size=16)
    deck.kpis("How severe is the overlap?",
              [(f"{vif.loc['log_declared_income', 'VIF']:.0f}", "variance inflation factor (VIF)", "Above 10 counts as severe."),
               ("99%", "of each signal is explained by the others", "Almost nothing is left to tell them apart."),
               (f"×{vif.loc['log_declared_income', 'SE inflation (√VIF)']:.0f}", "uncertainty of each coefficient",
                "Compared with signals that do not overlap.")],
              takeaway="The other variables in the model are fine (VIF below 5).")
    deck.image("Where overlap hurts: customers whose signals disagree",
               figs / "fig06_pilot_bias.png",
               takeaway=f"Actual pilot spend is {full_err:.0f}% above the model's prediction, and anywhere from {q_err.min():+.0f}% to "
                        f"{q_err.max():+.0f}% depending on which quarter the model was fitted on.")
    rem_tbl = pd.DataFrame({
        "Option": ["Keep both (today)", "Drop salary credits", "Combine into one income index", "Ridge regression"],
        "Coefficients stable across quarters?": ["No (SD {:.2f})".format(rem.loc["Keep both (as is)", "quarter-to-quarter SD"]),
                                                 "Yes (SD {:.2f})".format(rem.loc["Drop salary credits", "quarter-to-quarter SD"]),
                                                 "Yes (SD {:.2f})".format(rem.loc["Combine into an index", "quarter-to-quarter SD"]),
                                                 "Partly (SD {:.2f})".format(rem.loc["Ridge regression", "quarter-to-quarter SD"])],
        "Accuracy (salaried)": ["Same", "Same", "Same", "Same"],
        "Easy to explain?": ["No", "Yes", "Yes", "No"],
    })
    deck.table("Fixing it: an income index keeps accuracy and makes the model readable", rem_tbl,
               takeaway=f"All options predict salaried spend equally well (error {cv['CV RMSE (log)'].min():.3f}–"
                        f"{cv.drop('Neither income signal')['CV RMSE (log)'].max():.3f} on the log scale). The difference is stability and clarity.",
               col_widths=[1.8, 1.6, 1.0, 0.9], font_size=14, highlight_rows=[2])
    deck.bullets("Recommendations",
                 ["**Replace declared income and salary credits with one income index** in the salaried model.",
                  "**Stop reporting the two income coefficients separately** in dashboards and model documentation.",
                  "**Remove the duplicate 'total obligations' column** (it equals EMI + rent exactly).",
                  "**Do not use this model for the self-employed pilot.** Build a segment model with income evidence that "
                  "works for them (tax returns, all-account credits) and check its error before setting limits.",
                  "**Add overlap checks (VIF, duplicate columns) to every quarterly refit.**"],
                 takeaway="Decision needed: approve the index-based model and a separate pilot model.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Spend model only; default risk is assessed separately.", "600 pilot customers: estimates have a few points of uncertainty.",
                      "Self-declared income may be inflated in digital journeys."],
                     "Next steps",
                     ["Monitor how closely income signals agree, by segment and channel.", "Collect independent income evidence for the pilot.",
                      "Re-validate after the next quarterly refit."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
