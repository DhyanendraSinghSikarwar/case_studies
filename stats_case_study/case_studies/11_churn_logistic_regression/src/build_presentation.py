"""Build the stakeholder deck for Case Study 11 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/11_churn_logistic_regression/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402

CLV, OFFER_COST, OFFER_SUCCESS, CAPACITY = 12_000, 600, 0.35, 1_000


def money_lakh(v: float) -> str:
    return f"{'+' if v >= 0 else '−'}₹{abs(v) / 1e5:.1f} lakh"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    ame = pd.read_csv(tables / "average_marginal_effects.csv", index_col=0)
    q = pd.read_csv(tables / "model_quality_test.csv", index_col=0)["value"]
    strat = pd.read_csv(tables / "call_strategies.csv", index_col=0)
    raw = pd.read_csv(tables / "raw_vs_adjusted_complaints.csv", index_col=0)
    cat = pd.read_csv(tables / "churn_by_category.csv", index_col=[0, 1])

    base = cat.xs("complaints_6m")["churners"].sum() / cat.xs("complaints_6m")["customers"].sum()
    c_rates = cat.xs("complaints_6m")["churn rate"]
    top, be, dflt, rnd = strat.iloc[2], strat.iloc[1], strat.iloc[0], strat.iloc[3]
    p_star = OFFER_COST / (OFFER_SUCCESS * CLV)
    a = ame["AME (pp)"]

    deck = Deck("Case 11 · Which customers are about to churn? · synthetic data")
    deck.title_slide("Who Is About to Leave, and Whom Should We Call?",
                     "Savings-account churn model and retention call list · Retail Liabilities Analytics",
                     "12,000 savings customers; churn measured over the following 6 months. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        f"Summary: {top['recall (share of all churners)']:.0%} of next half-year's churners are in the top 8% of customers",
        [
            f"**{base:.1%} of savings customers leave within 6 months.**",
            f"**Complaints matter most:** two or more complaints add about **{a['2+ complaints (vs none)']:.0f} percentage points** "
            f"of churn risk; one adds about {a['1 complaint (vs none)']:.0f}.",
            f"**Salary accounts, more products and a credit card protect:** about {a['salary account (yes vs no)']:.0f}, "
            f"{a['one more product']:.0f} and {a['credit card (yes vs no)']:.0f} points.",
            "**New customers and customers whose balances are falling** are the early-warning groups. Region does not matter.",
            f"**Calling the top {CAPACITY:,}** reaches {top['churners reached']:.0f} churners ({top['recall (share of all churners)']:.0%} of all) "
            f"and is worth about **₹{top['realised net value (₹)'] / 1e5:.1f} lakh**, if the offer works as assumed.",
        ],
        takeaway="Recommendation: score monthly, call the top 1,000, and test the offer properly before scaling.",
        size=16,
    )
    deck.image("Churn by customer characteristic, one at a time", figs / "fig01_churn_by_variable.png",
               takeaway="These raw views mix effects together; the model separates them.")
    deck.table("Is 'complaints make customers three times more likely to leave' right?",
               pd.DataFrame({"Complaints in last 6 months": ["None", "One", "Two or more"],
                             "Churn rate": [f"{c_rates['0']:.1%}", f"{c_rates['1']:.1%}", f"{c_rates['2+']:.1%}"],
                             "Compared with none": ["–", f"{c_rates['1'] / c_rates['0']:.1f}× as likely",
                                                    f"{c_rates['2+'] / c_rates['0']:.1f}× as likely"],
                             "Extra risk": ["–", f"+{100 * (c_rates['1'] - c_rates['0']):.0f} points",
                                            f"+{100 * (c_rates['2+'] - c_rates['0']):.0f} points"]}),
               takeaway="True for repeat complainants, not for one complaint. Beware: model 'odds ratios' are not 'times as likely' "
                        f"(for two or more complaints the odds ratio is {raw.loc['2+ complaints', 'adjusted odds ratio']:.1f}).",
               col_widths=[1.8, 1.0, 1.4, 1.2], font_size=16)
    deck.image("What each factor does to the churn probability", figs / "fig04_marginal_effects.png",
               takeaway="The same complaint adds a few points for a loyal customer and far more for a new customer with a falling balance.")
    deck.image("Can we trust the probabilities? Yes: tested on 3,000 customers the model never saw",
               figs / "fig05_roc_calibration.png",
               takeaway=f"Ranking quality (AUC) {q['AUC (test)']:.2f}; predicted and actual churn agree closely across risk deciles "
                        f"({q['mean predicted churn']:.1%} predicted vs {q['actual churn rate']:.1%} actual).")
    deck.kpis("When is a retention call worth making?",
              [(f"{p_star:.1%}", "break-even churn probability", f"₹{OFFER_COST} offer ÷ (35% success × ₹{CLV:,} value)"),
               (f"{be['customers called']:,.0f}", "customers above break-even", "More than the call centre can handle."),
               (f"{CAPACITY:,}", "calls available", "So call the highest-risk customers first.")],
              takeaway="The usual 'above 50%' rule would call only "
                       f"{dflt['customers called']:.0f} customers and miss most of the value.")
    rows = pd.DataFrame({
        "Call strategy": ["Top 1,000 by predicted risk", "Everyone above 50%", "1,000 random customers"],
        "Churners reached": [f"{top['churners reached']:.0f} ({top['recall (share of all churners)']:.0%})",
                             f"{dflt['churners reached']:.0f} ({dflt['recall (share of all churners)']:.0%})",
                             f"{rnd['churners reached']:.0f} ({rnd['recall (share of all churners)']:.0%})"],
        "Hit rate": [f"{top['precision (churners / called)']:.0%}", f"{dflt['precision (churners / called)']:.0%}",
                     f"{rnd['precision (churners / called)']:.0%}"],
        "Net value": [money_lakh(s["realised net value (₹)"]) for s in (top, dflt, rnd)],
    })
    deck.table("Who to call: the model's top 1,000", rows,
               takeaway="Based on the assumed 35% offer success rate and ₹12,000 customer value; both should be tested.",
               col_widths=[2.0, 1.4, 0.9, 1.2], font_size=16, highlight_rows=[0])
    deck.image("Calling more customers adds value up to the break-even point", figs / "fig06_gains_and_value.png",
               takeaway=f"The top 1,000 hold {top['recall (share of all churners)']:.0%} of all churners. "
                        f"Extra capacity would pay off up to about {be['customers called']:,.0f} calls.")
    deck.bullets("Recommendations",
                 [f"**Score customers monthly and call the top {CAPACITY:,}** (all above the {p_star:.1%} break-even).",
                  "**Run the offer as a randomised test for two months:** call half of the top group, not the other half, and "
                  "measure the real success rate.",
                  "**Escalate repeat complaints:** two or more complaints is the strongest single warning sign.",
                  "**Watch new customers and falling balances** as early-warning triggers.",
                  "**Report effects in percentage points**, not odds ratios."],
                 takeaway="Decision needed: approve the call list and the two-month offer test.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Shows who is at risk, not whom a call will keep.",
                      "Offer success (35%) and customer value (₹12,000) are assumptions.",
                      "One cohort; must be re-validated on new data."],
                     "Next steps",
                     ["Randomised offer test, then an uplift model.",
                      "Check whether salary-account customers react less to complaints (suggestive, unproven).",
                      "Monitor calibration monthly."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
