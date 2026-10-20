"""Build the stakeholder deck for Case Study 12 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/12_fraud_imbalanced_classification/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def lakh(v: float) -> str:
    return f"{'' if v >= 0 else '−'}₹{abs(v) / 1e5:.1f} lakh"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    base = pd.read_csv(tables / "baseline_classifiers.csv", index_col=0)
    perf = pd.read_csv(tables / "model_performance_test.csv", index_col=0)
    reb = pd.read_csv(tables / "rebalancing_comparison.csv", index_col=0)
    pol = pd.read_csv(tables / "policy_comparison_month4.csv", index_col=0)
    unc = pd.read_csv(tables / "uncertainty_recommended_policy.csv", index_col=0)
    drift = pd.read_csv(tables / "monthly_calibration.csv", index_col=0)

    rec = pol.loc["Model, amount-aware within capacity"]
    rules = pol.loc["Current rules"]
    lr = perf.loc["Logistic regression"]
    extra = unc.loc["extra saving vs current rules (₹, bootstrap)"]

    deck = Deck("Case 12 · Card transaction fraud detection · synthetic data")
    deck.title_slide("Catching More Fraud With Fewer Alerts",
                     "Fraud model and alert policy · Fraud Risk analytics for the Head of Fraud Risk",
                     "120,000 card transactions over 4 months (fraud ≈ 0.4%); tested on the most recent month. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: a calibrated model, ranked by expected loss, beats our rules within analyst capacity",
        [
            f"**'99.6% accuracy' means little:** flagging nothing at all is {base.iloc[0]['accuracy']:.1%} accurate.",
            f"**Measured properly, the model is much better than our rules:** on next month's data, half the fraud can be caught "
            f"with about 1 in 3 alerts genuine (rules: {rules['precision']:.0%} of alerts genuine).",
            f"**Recommended policy:** review the {int(rec['alerts'])} transactions (1%) with the highest expected loss. "
            f"It stops **{rec['fraud ₹ caught (%)']:.0f}% of fraud rupees** and saves about **{lakh(extra['estimate'])} more per month** "
            "than the rules (in this sample).",
            "**Do not 'rebalance' the data** as the vendor suggests: it does not improve ranking and it breaks the probabilities "
            "that our money decisions rely on.",
            f"**Fraud is shifting:** month 4 had about {drift.loc[4, 'actual ÷ predicted'] - 1:.0%} more fraud than the model expected, almost all in online gaming.",
        ],
        takeaway="Decision needed: replace the two rules with the model and an expected-loss review queue; retrain monthly.",
        size=15,
    )
    deck.image("Where fraud happens", figs / "fig01_fraud_patterns.png",
               takeaway="E-commerce, online gaming, night-time and unusually large transactions. "
                        "Even in the riskiest groups, only 1–2% of transactions are fraud.")
    deck.table("'99.6% accurate' can mean 'catches nothing'",
               pd.DataFrame({"Approach (month 4)": ["Flag nothing", "Current rules", "Model: top 1% by expected loss"],
                             "Accuracy": [f"{base.iloc[0]['accuracy']:.1%}", f"{rules['accuracy']:.1%}", f"{rec['accuracy']:.1%}"],
                             "Frauds caught": ["0%", f"{rules['recall']:.0%}", f"{rec['recall']:.0%}"],
                             "Alerts that are fraud": ["–", f"{rules['precision']:.0%}", f"{rec['precision']:.0%}"],
                             "Fraud ₹ stopped": ["0%", f"{rules['fraud ₹ caught (%)']:.0f}%", f"{rec['fraud ₹ caught (%)']:.0f}%"]}),
               takeaway="Accuracy hardly moves. What matters is the share of fraud stopped and how clean the alert queue is.",
               col_widths=[2.2, 0.9, 1.0, 1.1, 1.0], font_size=15, highlight_rows=[2])
    deck.image("The vendor's 'AUC 0.97' and the view that matters for the alert queue",
               figs / "fig02_roc_vs_pr.png",
               takeaway=f"Same model, two pictures. Left (ROC): looks near-perfect. Right (precision-recall, score {lr['PR-AUC (average precision)']:.2f}): "
                        "shows how many alerts are genuine fraud.")
    deck.kpis("Should we rebalance the data?",
              [(f"{reb.loc['Standard (no rebalancing)', 'ROC-AUC']:.3f} → {reb.loc['Class weights (balanced)', 'ROC-AUC']:.3f}",
                "ranking quality", "Balancing changes nothing that matters."),
               (f"{reb.loc['Standard (no rebalancing)', 'mean predicted fraud rate']:.1%} → {reb.loc['Class weights (balanced)', 'mean predicted fraud rate']:.0%}",
                "average predicted fraud rate", f"Actual: {reb.loc['Standard (no rebalancing)', 'actual fraud rate']:.1%}."),
               (lakh(pol.loc["Amount-aware rule on the class-weighted model", "saving vs no alerts (₹)"]),
                "result of using its probabilities", "13,000+ alerts: costs swamp the savings.")],
              takeaway="Rebalancing only moves the threshold. We can move the threshold directly and keep honest probabilities.")
    deck.image("Which alert policy saves the most money? (month 4, unseen)", figs / "fig05_policy_savings.png",
               takeaway="The best unconstrained policy needs 3× our analysts. Ranking by expected loss within capacity keeps "
                        "about 92% of its saving.")
    rows = pd.DataFrame({
        "": ["Frauds caught", "Alerts that are fraud", "Saving vs no alerts", "Extra saving vs current rules"],
        "Estimate": [f"{unc.iloc[1]['estimate']:.0%}", f"{unc.iloc[0]['estimate']:.0%}", lakh(unc.iloc[2]['estimate']), lakh(extra['estimate'])],
        "95% range": [f"{unc.iloc[1]['95% CI low']:.0%}–{unc.iloc[1]['95% CI high']:.0%}",
                      f"{unc.iloc[0]['95% CI low']:.0%}–{unc.iloc[0]['95% CI high']:.0%}",
                      f"{lakh(unc.iloc[2]['95% CI low'])} to {lakh(unc.iloc[2]['95% CI high'])}",
                      f"{lakh(extra['95% CI low'])} to {lakh(extra['95% CI high'])}"],
    })
    deck.table("How sure are we? Only 157 frauds in the test month", rows,
               takeaway="The model is better than the rules in every plausible scenario; how much better is uncertain.",
               col_widths=[2.2, 1.0, 2.0], font_size=16)
    deck.image("Fraud is shifting: online gaming fraud is rising faster than the model expects",
               figs / "fig06_drift.png",
               takeaway="The model must be retrained monthly and its accuracy tracked by merchant type.")
    deck.bullets("Recommendations",
                 ["**Replace the two rules with the model.** Score every transaction.",
                  "**Rank by expected loss** (probability × 80% × amount) and send the top 1% to analysts.",
                  "**Do not rebalance the training data.** If we ever sample for speed, correct the probabilities afterwards.",
                  "**Retrain monthly** and monitor predicted vs actual fraud by merchant type, starting with online gaming.",
                  "**Report precision, recall and rupees stopped with ranges**, not accuracy or AUC alone."],
                 takeaway="Decision needed: approve the switch from rules to the model-based review queue.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["One test month with 157 frauds: wide ranges.",
                      "Costs (80% loss, ₹150 per alert) are assumptions.",
                      "Fraud labels arrive late in reality; fraudsters adapt."],
                     "Next steps",
                     ["Two-stage policy: auto-decline the very highest risk.",
                      "Retest gradient boosting with 6–12 months of data.",
                      "Monthly drift dashboard by merchant type."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
