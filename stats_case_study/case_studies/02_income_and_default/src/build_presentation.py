"""Build the stakeholder deck for Case Study 02 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/02_income_and_default/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def crore(x: float, d: int = 1) -> str:
    """Signed ₹ crore with a proper minus sign: -0.29 -> '−₹0.3 crore'."""
    return f"{'−' if x < 0 else '+' if x > 0 else ''}₹{abs(x):.{d}f} crore"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    bands = pd.read_csv(tables / "default_rate_by_band.csv", index_col=0)
    eff = pd.read_csv(tables / "threshold_effects.csv", index_col=0)
    impact = pd.read_csv(tables / "floor_impact.csv", index_col=0)
    sens = pd.read_csv(tables / "floor_sensitivity.csv", index_col=0)
    res = pd.read_csv(tables / "key_results.csv", index_col=0)

    n_loans = int(bands["loans"].sum())
    overall = bands["defaults"].sum() / n_loans
    low_rate = eff.loc["default rate, income < ₹30k", "estimate"]
    high_rate = eff.loc["default rate, income ≥ ₹30k", "estimate"]
    rr = eff.loc["risk ratio"]
    f30 = impact.loc[30_000]
    net = res.loc["Net value of ₹30k floor (₹ crore)"]
    ratio = res.loc["Typical income ratio, defaulted / repaid"]
    breakeven = float(res.loc["Net value of ₹30k floor (₹ crore)", "effect size"].split()[-1].rstrip("%")) / 100
    # Share of defaulters below ₹30k = defaulters excluded by a ₹30k floor / all defaulters
    p_low_given_def = f30["defaults_avoided"] / bands["defaults"].sum()

    deck = Deck("Case 02 · Do higher earners default less? · synthetic data")

    deck.title_slide(
        "Should We Raise the Minimum Income to ₹30,000?",
        "Evidence review for the Credit Committee · Risk Policy",
        f"Based on {n_loans:,} personal loans disbursed in 2024 with 12 months of performance. "
        "Synthetic data created for training. Not actual customer data.",
    )

    deck.bullets(
        "Summary: low earners do default more, but a ₹30k floor would cost more than it saves",
        [
            f"**The belief is right:** default falls steadily with income, from **{bands['default_rate'].iloc[0]:.1%}** "
            f"(₹20–25k) to **{bands['default_rate'].iloc[-1]:.1%}** (≥ ₹100k). This is not chance.",
            f"Customers under ₹30k are **{rr['estimate']:.1f}× as likely** to default ({low_rate:.0%} vs {high_rate:.0%}).",
            f"**But {1 - low_rate:.0%} of them repay.** A ₹30k floor turns away **~{f30['good_lost_per_default_avoided']:.0f} good "
            "customers for every default it prevents**.",
            f"Net effect on the 2024 book: about **{crore(net['estimate'])}** (likely {crore(net['ci_low'])} to "
            f"{crore(net['ci_high'])}), i.e. value lost.",
            "Part of the income signal is really credit score and debt burden, which we already use.",
        ],
        takeaway="Recommendation: keep the ₹20k floor; use income in pricing and loan sizing instead of a hard cut-off.",
        size=18,
    )

    deck.two_columns(
        "The proposal rests on a belief, a number and a decision; each needs checking",
        "What we were asked",
        [
            "Do higher earners really default less?",
            "By how much?",
            "Is raising the floor from ₹20k to ₹30k worth it?",
        ],
        "How we checked",
        [
            f"{n_loans:,} loans approved in 2024, each followed for 12 months.",
            "Compared default rates across five income bands.",
            "Tested whether the pattern could be chance.",
            "Re-ran 2024 as if the ₹30k floor had applied: defaults avoided vs good business lost.",
        ],
        takeaway="A real risk difference does not automatically make a good policy. The third question needs economics, not just statistics.",
    )

    deck.kpis(
        "The data: one year of approved personal loans",
        [
            (f"{n_loans:,}", "loans analysed", "Disbursed in 2024; 59 with missing income excluded."),
            (f"{overall:.1%}", "default rate", "90+ days past due within 12 months."),
            (f"{f30['share_excluded']:.0%}", "earn under ₹30k", "The customers a ₹30k floor would exclude."),
            ("Approved only", "no declined applicants", "We cannot see how applicants below ₹20k would perform."),
        ],
    )

    deck.image(
        "Lower earners do default more, with a steady decline across income bands",
        figs / "fig02_default_rate_by_band.png",
        bullets=[
            f"From **{bands['default_rate'].iloc[0]:.1%}** in the lowest band to **{bands['default_rate'].iloc[-1]:.1%}** in the highest.",
            "Every step down in income brings a step up in risk.",
            "Far too consistent to be the luck of the sample (less than 1-in-a-billion chance).",
            "Error bars show the likely range for each band.",
        ],
        takeaway="Income genuinely carries risk information. The question is how best to use it.",
    )

    deck.kpis(
        "How big is the difference? It depends on which way you look at it",
        [
            (f"{rr['estimate']:.1f}×", "relative risk under ₹30k", f"Likely range {rr['ci_low']:.1f}–{rr['ci_high']:.1f}×."),
            (f"{low_rate:.0%} vs {high_rate:.0%}", "default rate below vs above ₹30k", f"A gap of {100 * (low_rate - high_rate):.0f} percentage points."),
            (f"{1 - low_rate:.0%}", "of under-₹30k customers repay", "Most low-income customers are good customers."),
            (f"{p_low_given_def:.0%}", "of defaulters earn < ₹30k", f"This is NOT the chance a low earner defaults (that is {low_rate:.0%})."),
        ],
        takeaway="'Most defaulters are low-income' is true, but it does not mean most low-income customers default.",
    )

    deck.image(
        "Incomes of defaulters and repayers overlap heavily, so any income cut-off is blunt",
        figs / "fig01_income_by_outcome.png",
        bullets=[
            f"Defaulters' typical income is **{1 - ratio['estimate']:.0%} lower** than repayers'.",
            "But the two groups overlap: many defaulters earn well, and most low earners repay.",
            "A random defaulter still out-earns a random repayer about 1 time in 3.",
        ],
        image_share=0.66,
    )

    tbl = impact.loc[[25_000, 30_000, 35_000, 40_000]]
    floor_tbl = pd.DataFrame({
        "Income floor": [f"₹{int(f / 1000)}k" for f in tbl.index],
        "Loans excluded": [f"{s:.0%}" for s in tbl["share_excluded"]],
        "Defaults avoided": tbl["defaults_avoided"].astype(int).astype(str),
        "Good customers lost": tbl["good_customers_lost"].astype(int).map("{:,}".format),
        "Good lost per default avoided": tbl["good_lost_per_default_avoided"].map("{:.1f}".format),
        "Net value (₹ crore)": tbl["net_value_cr"].map(lambda v: f"{'−' if v < 0 else '+'}{abs(v):.2f}"),
    })
    deck.table(
        "Every floor we tested would have lost money on the 2024 book",
        floor_tbl,
        takeaway="The higher the floor, the more good business is lost for each default avoided.",
        col_widths=[1.1, 1.1, 1.1, 1.3, 1.5, 1.3],
        highlight_rows=[1],
        font_size=15,
    )

    deck.image(
        f"A ₹30k floor saves less in losses than it gives up in profit",
        figs / "fig04_floor_tradeoff.png",
        takeaway=f"₹30k floor: ~{int(f30['defaults_avoided'])} defaults avoided vs ~{int(f30['good_customers_lost']):,} good customers "
                 f"lost. Net ≈ {crore(net['estimate'])}.",
    )

    sens_tbl = sens.copy()
    sens_tbl = sens_tbl.map(lambda v: f"{'−' if v < 0 else '+'}{abs(v):.2f}")
    sens_tbl.insert(0, "Loss on default", sens_tbl.index.str.replace("LGD ", ""))
    sens_tbl.columns = ["Loss on default (LGD)"] + [c.replace("margin", "Margin") for c in sens.columns]
    deck.table(
        f"The answer hinges on the margin: below ~{breakeven:.1%}, the floor starts to pay",
        sens_tbl,
        takeaway="Net value of the ₹30k floor (₹ crore). Base case: LGD 65%, margin 12%. Ask Finance to confirm the margin before deciding.",
        col_widths=[1.4, 1, 1, 1, 1],
        highlight_rows=[2],
        font_size=15,
    )

    deck.image(
        "Part of the 'income effect' is really credit score: low earners tend to have weaker scores",
        figs / "fig05_income_within_score_band.png",
        bullets=[
            "Among customers with similar credit scores, income matters less.",
            "We already use credit score and debt burden in approvals.",
            "An income floor would partly **double-count** risk we already price.",
        ],
        image_share=0.62,
    )

    deck.two_columns(
        "What we can and cannot say",
        "We can say",
        [
            "Lower-income customers default more, and this is not chance.",
            f"Below ₹30k: {low_rate:.0%} default vs {high_rate:.0%} above.",
            f"{1 - low_rate:.0%} of below-₹30k customers repay.",
            "A ₹30k floor would very likely reduce value under Finance's assumptions.",
        ],
        "We cannot say",
        [
            "That low income **causes** default.",
            "How applicants **below ₹20k** would perform. We never approved them.",
            "How much income adds beyond credit score and debt burden.",
            f"That the result holds if the true margin is below ~{breakeven:.1%}.",
        ],
    )

    deck.bullets(
        "Recommendations",
        [
            "**Keep the ₹20,000 floor.** Do not raise it to ₹30,000 on current evidence.",
            f"**Confirm the margin with Finance:** if good loans earn under ~{breakeven:.1%} over their life, revisit this.",
            "**Use income more precisely:** risk-based pricing, smaller loan sizes or shorter tenures for the ₹20–30k segment.",
            "**Build a combined risk model** (income + credit score + debt burden) to measure what income adds.",
            "**Fix the framing:** 'most defaulters are low-income' ≠ 'most low-income customers default'.",
            "**If a policy change is still wanted, pilot it** in selected regions with a comparison group.",
        ],
        takeaway="Decision for the Committee: reject the ₹30k floor; approve the combined risk model and a pricing review.",
        size=18,
    )

    deck.two_columns(
        "Limitations and next steps",
        "Limitations",
        [
            "Approved loans only: no data below ₹20k.",
            "Income overlaps with score and debt burden.",
            "Loss and margin are book-wide Finance assumptions.",
            "One cohort (2024), one economic environment.",
        ],
        "Next steps",
        [
            "Weeks 1–4: combined risk model (income, score, debt burden, employment).",
            "Weeks 2–4: Finance to provide loss and margin by income band.",
            "Weeks 4–6: pricing proposal for the ₹20–30k segment.",
            "Optional: regional pilot of any policy change.",
        ],
    )

    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
