"""Build the stakeholder deck for Case Study 06 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/06_loan_amount_simple_regression/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths, fmt_money  # noqa: E402


def lakh(x: float) -> str:
    return f"₹{x / 1e5:.1f}L"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    res = pd.read_csv(tables / "key_results.csv", index_col=0)
    offer = pd.read_csv(tables / "pre_offer_table_log_model.csv")
    cov = pd.read_csv(tables / "holdout_pi_coverage.csv", index_col=0)

    per10k = res.loc["Raw model: ₹ loan per ₹10k income"]
    el = res.loc["Log model: elasticity"]
    r2 = res.loc["Raw model: R²", "estimate"]
    resid_sd = res.loc["Log model: residual SD (log)", "estimate"]
    import math
    factor = math.exp(resid_sd)

    deck = Deck("Case 06 · Predicting loan amount from income · synthetic data")
    deck.title_slide(
        "A Simple, Honest Loan Pre-Offer Rule for Branches",
        "Recommendation for the Head of Personal Loans · Lending Analytics",
        "Based on 3,000 personal loans disbursed in the last six months. Synthetic data created for training. Not actual customer data.",
    )
    deck.bullets(
        "Summary: customers borrow roughly a fixed number of months of income, give or take 50%",
        [
            f"**Each extra ₹10,000 of monthly income goes with about {fmt_money(round(per10k['estimate'], -3))} more borrowing** on average "
            f"(likely {fmt_money(round(per10k['ci_low / value 2'], -3))}–{fmt_money(round(per10k['ci_high'], -3))}).",
            f"Better rule of thumb: **10% more income → about {(1.1 ** el['estimate'] - 1) * 100:.0f}% more loan**. Loans scale with income.",
            f"**Income explains about {r2:.0%} of loan sizes.** A typical customer borrows within ×/÷ {factor:.1f} of the suggested amount.",
            f"**Show branches a realistic range, not just one number.** On new loans our 80% range held {cov['log_model_coverage'].iloc[:5].min():.0%}–"
            f"{cov['log_model_coverage'].iloc[:5].max():.0%} of the time in every income band.",
        ],
        takeaway="Recommendation: roll out the pre-offer table below for incomes up to ₹4 lakh/month; above that, offer the cap and refer to an RM.",
        size=18,
    )
    deck.kpis(
        "What the data shows",
        [
            ("3,000", "recent personal loans", "With verified monthly income and the amount taken."),
            (f"{r2:.0%}", "explained by income", "The rest depends on debts, purpose, job type, etc."),
            (f"{el['estimate']:.2f}", "elasticity", "1% more income → about 0.9% more loan."),
            (f"×/÷ {factor:.1f}", "typical spread", "How far a real customer is from the suggested amount."),
        ],
    )
    deck.image(
        "Loan amounts scale with income, and so does the spread between customers",
        figs / "fig01_scatter_raw_vs_log.png",
        takeaway="Customers vary by similar PERCENTAGES around the typical amount, so ranges must be in percentages too.",
    )
    deck.image(
        "A straight-line rule gives the wrong ranges: too wide for small loans, too narrow for large ones",
        figs / "fig02_ci_vs_pi_raw.png",
        bullets=[
            "The thin orange band is the average customer: precise, but not what branches need.",
            "The wide blue band is one customer, and it even goes below zero at low incomes.",
            "The spread in the data clearly widens with income. The straight-line rule ignores that.",
        ],
        image_share=0.62,
    )
    tbl = offer.copy()
    tbl = pd.DataFrame({
        "Monthly income": tbl["income"].map(fmt_money),
        "Suggested offer": tbl["typical (median) amount"].map(lambda v: fmt_money(round(v, -4))),
        "Most customers borrow between (80%)": [f"{fmt_money(round(a, -4))} – {fmt_money(round(b, -4))}" for a, b in zip(tbl["low"], tbl["high"])],
    })
    deck.table(
        "The pre-offer table for branch staff",
        tbl,
        takeaway="Suggest the middle number; expect most customers to land within the range. Round to the nearest ₹10,000.",
        col_widths=[1.2, 1.2, 2.2],
        font_size=16,
    )
    deck.image(
        "Tested on loans the rule never saw: the range is close to its 80% promise at every income level",
        figs / "fig06_holdout_coverage.png",
        takeaway=f"Straight-line rule: {cov.iloc[0]['raw_model_coverage']:.0%} for low earners vs {cov.iloc[4]['raw_model_coverage']:.0%} for top "
                 f"earners. New rule: {cov.iloc[0]['log_model_coverage']:.0%} and {cov.iloc[4]['log_model_coverage']:.0%}.",
    )
    deck.two_columns(
        "What the rule can and cannot do",
        "It can",
        ["Give a consistent starting offer across branches.", "Give a realistic range for incomes up to ₹4 lakh/month.",
         "Be explained in one sentence."],
        "It cannot",
        ["Say what very high earners would borrow without our ₹20 lakh cap.",
         "Account for existing debts, purpose or job type (yet).",
         "Tell us that higher income CAUSES bigger loans. It reflects current customers and policy."],
    )
    deck.bullets(
        "Recommendations and next steps",
        [
            "**Roll out the pre-offer table** (incomes up to ₹4 lakh/month) with its 80% range.",
            "**Above ₹4 lakh/month:** offer the cap; route to a relationship manager.",
            "**In planning materials:** 'about ₹26,000 more per ₹10,000 of income, on average', with the range.",
            "**Next quarter:** add job type and existing debts to narrow the ranges (multiple regression).",
            "**Monitor monthly:** check the range still holds ~80% of the time in each income band.",
        ],
        takeaway="Decision: approve the branch pre-offer rule; fund the next modelling step.",
    )
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
