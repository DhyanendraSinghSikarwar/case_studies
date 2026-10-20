"""Build the stakeholder deck for Case Study 16 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/16_payment_outliers/src/build_presentation.py
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
    grade = pd.read_csv(tables / "detector_grading.csv", index_col=0)
    treat = pd.read_csv(tables / "treatment_comparison.csv", index_col=0)
    tri = pd.read_csv(tables / "triage_metrics.csv", index_col=0)
    cors = pd.read_csv(tables / "correlation_with_without_outliers.csv", index_col=0)

    dash = grade.loc["Dashboard: z > 3 (raw ₹)"]
    new = grade.loc["New screen (segment OR customer OR context)"]
    harmless = int(dash["vip"] + dash["festival"] + dash["normal"])
    nothing, delete_dash, corrected = treat.iloc[0], treat.iloc[1], treat.iloc[3]
    pearson_col = [c for c in cors.columns if c.startswith("Pearson r (amount")][0]
    r_all, r_clean = cors.iloc[0][pearson_col], cors.iloc[1][pearson_col]

    deck = Deck("Case 16 · Payment outliers: error, fraud, VIP or rare event? · synthetic data")
    deck.title_slide("Which Unusual Payments Are Problems, and Which Are Our Best Customers?",
                     "An outlier policy for payment monitoring · Risk Analytics for Payments Operations",
                     "20,230 payments over a quarter. Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: the '3 standard deviations' rule flags the wrong payments and misses the right ones",
        [
            f"**The dashboard flags {int(dash['total flagged'])} payments; {harmless} ({harmless / dash['total flagged']:.0%}) are harmless** "
            "(VIPs, festival purchases, ordinary large payments).",
            f"**It catches only {dash['errors caught (of 40)']:.0%} of the keying errors and {dash['fraud caught (of 60)']:.0%} of the fraud.**",
            f"**A three-lens screen** (unusual for the segment, for the customer, and several risk flags) **catches all "
            f"{int(new['entry_error'])} errors and all {int(new['fraud'])} frauds** with {int(new['total flagged'])} flags, and none of the VIP or festival payments.",
            f"**Doing nothing about errors overstates the average ticket by {nothing['bias vs truth (%)']:.0f}%**; "
            f"deleting the dashboard's flags understates it by {abs(delete_dash['bias vs truth (%)']):.1f}%.",
        ],
        takeaway="Recommendation: retire the 3-SD rule; correct errors, investigate fraud, keep and whitelist VIP and festival payments.",
        size=16,
    )
    deck.image("Payments are far from 'normally' distributed: each segment has its own normal", figs / "fig01_amount_distribution.png",
               takeaway="A ₹40,000 payment is routine at a jeweller and extraordinary at a grocer. One mean and one spread cannot describe both.")
    deck.image("Four ways to define 'unusual' give 10, 16, 58 or 2,537 payments", figs / "fig02_detectors.png",
               takeaway="The dashboard's flags are simply the largest payments in the two most expensive segments.")
    deck.bullets("There are four kinds of unusual payment, and each needs a different action",
                 ["**Data error:** typed 100× too large by an operator → **correct** it and fix the process.",
                  "**Fraud:** new device, location mismatch, night time, burst → **investigate**; never delete.",
                  "**VIP:** long-standing top-tier customer, amount in line with their own history → **keep**; do not alert.",
                  "**Rare real event:** festival-week buying of jewellery or electronics by regular customers → **keep**; add an event calendar."],
                 takeaway="The amount alone cannot tell them apart. Context can.")
    deck.image("What each method catches: only the combined screen finds both errors and fraud", figs / "fig04_detector_grading.png",
               takeaway="Left: what is flagged, by true type. Right: the share of real errors and frauds each method catches.")
    rows = pd.DataFrame({
        "Method": ["Dashboard: 3 SD on raw ₹", "IQR fence on raw ₹", "Robust z on log ₹ (MAD)", "Unusual for the customer", "Several risk flags",
                   "Combined screen"],
        "Flags": [f"{int(grade.loc[k, 'total flagged']):,}" for k in ["Dashboard: z > 3 (raw ₹)", "IQR fence (raw ₹)", "MAD robust z (log ₹)",
                                                                      "Customer-relative robust z", "3+ risk flags",
                                                                      "New screen (segment OR customer OR context)"]],
        "Errors caught": [f"{grade.loc[k, 'errors caught (of 40)']:.0%}" for k in ["Dashboard: z > 3 (raw ₹)", "IQR fence (raw ₹)", "MAD robust z (log ₹)",
                                                                                 "Customer-relative robust z", "3+ risk flags",
                                                                                 "New screen (segment OR customer OR context)"]],
        "Fraud caught": [f"{grade.loc[k, 'fraud caught (of 60)']:.0%}" for k in ["Dashboard: z > 3 (raw ₹)", "IQR fence (raw ₹)", "MAD robust z (log ₹)",
                                                                               "Customer-relative robust z", "3+ risk flags",
                                                                               "New screen (segment OR customer OR context)"]],
    })
    deck.table("Scorecard of the methods", rows,
               takeaway="Each lens finds something the others miss. Together they find everything with 130 flags instead of 2,537.",
               col_widths=[2.3, 0.8, 1.1, 1.1], font_size=14, highlight_rows=[5])
    deck.image("Triage by what the payment is: the rules separate errors, fraud, VIP and festival buying", figs / "fig05_triage_confusion.png",
               takeaway=f"Errors: {tri.loc['entry_error', 'precision']:.0%} precise. Fraud: {tri.loc['fraud', 'precision']:.0%} precise, "
                        f"{tri.loc['fraud', 'recall among all true cases']:.0%} caught. The remainder is ordinary variation.")
    deck.image("What each treatment does to the average ticket size Finance uses", figs / "fig06_treatment_bias.png",
               takeaway=f"Ignoring errors: {nothing['bias vs truth (%)']:+.0f}%. Deleting all large payments or capping them also distorts. "
                        "Correcting identified errors gets within 0.1%.")
    deck.bullets("Outliers and the numbers Finance and Risk use",
                 [f"**Average ticket:** correct identified errors and keep genuine extremes ({corrected['bias vs truth (%)']:+.2f}% off the truth).",
                  "**Typical ticket:** the median or a trimmed mean needs no cleaning.",
                  f"**Correlations:** 40 keying errors cut the correlation between a payment and the customer's usual payment from "
                  f"{r_clean:.2f} to {r_all:.2f}; rank and log-scale versions barely move.",
                  "**Never delete a payment because it is big.** VIP and festival payments are data, and the model needs them."],
                 takeaway="Delete only what is wrong, and only when you know it is wrong.")
    deck.bullets("Recommendations",
                 ["**Retire the '3 standard deviations' dashboard rule.**",
                  "**Screen on the log scale, with three lenses:** unusual for the segment, unusual for the customer, several risk flags.",
                  "**Route by type:** errors to correction, fraud to investigators, VIP and festival payments off the queue.",
                  "**Add keying controls:** a 'did you mean ₹X?' check when an amount is 10× or more above the customer's usual.",
                  "**Audit a random sample of flagged and unflagged payments each quarter** to keep the rules honest."],
                 takeaway="Decision needed: approve the new screen and routing rules.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Rules are tuned to this simulated mix; real outliers overlap more.",
                      "Fraud confirmation lags by weeks in reality.", "Thresholds are choices and should be tested on audits."],
                     "Next steps",
                     ["Stratified audit sample to measure precision and recall.", "Supervised fraud model with confirmed labels (Case 12).",
                      "Festival calendar feature."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
