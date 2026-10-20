"""Build the stakeholder deck for Case Study 05 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/05_correlation_card_spend/src/build_presentation.py
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
    lc = pd.read_csv(tables / "limit_spend_correlations.csv", index_col=0)
    upl = pd.read_csv(tables / "limit_increase_uplift.csv", index_col=0).iloc[:, 0]
    logins = pd.read_csv(tables / "logins_spend_by_segment.csv", index_col=0)
    rev = pd.read_csv(tables / "limit_increase_profile.csv", index_col=0)
    naive, bound, true = upl.iloc[0], upl.iloc[1], upl.iloc[2]
    pooled = logins.loc["ALL (pooled)", "Spearman ρ"]
    within = logins["Spearman ρ"].iloc[1:]
    spend_ratio = rev.iloc[1]["median_spend"] / rev.iloc[0]["median_spend"]

    deck = Deck("Case 05 · What correlation can and cannot tell you · synthetic data")
    deck.title_slide(
        "Three Growth Proposals, Three Misleading Correlations",
        "Review of the card-spend growth plan for the Head of Cards · Cards Analytics",
        "6,000 cardholders and 36 months of portfolio data. Synthetic data created for training. Not actual customer data.",
    )
    deck.bullets(
        "Summary: none of the three correlations supports the decision built on it",
        [
            f"**Raise all limits by 30%?** Limits and spend move together mainly because **income drives both**, and because "
            f"we raise limits for big spenders. Expected gain: about **+{true:.1%}** of spend, not +{naive:.0%}.",
            f"**App users spend less?** Only because Mass customers log in more. **Within every customer group, app users "
            f"spend more.**",
            "**Age doesn't matter?** It does: spending peaks in the early 40s. A simple correlation cannot see a curve.",
            "**Marketing drives spend (r = 0.91)?** Both just grew over time. Month to month, they are unrelated.",
        ],
        takeaway="Recommendation: no blanket limit increase; keep app investment and age targeting; test changes before rolling them out.",
        size=17,
    )
    deck.two_columns(
        "A correlation describes the past; a decision needs to know what changes if we act",
        "What a correlation can tell us",
        ["Two things tend to move together.", "How strongly, in the data we have."],
        "What it cannot tell us",
        ["**Why** they move together.", "Which one drives the other.", "What happens if **we** change one of them."],
        takeaway="Before acting on any correlation, ask: could a third factor, or the reverse direction, explain it?",
    )
    deck.kpis(
        "Even the strength of the correlation depended on data problems",
        [
            (f"{lc['Pearson r'].iloc[0]:.2f}", "with data errors", "15 spends keyed in paise made the link look weak."),
            (f"{lc['Pearson r'].iloc[1]:.2f}", "with corporate cards", "12 special cards made it look stronger."),
            (f"{lc['Spearman ρ'].iloc[2]:.2f}", "robust measure", "Rank-based correlation: unaffected either way."),
        ],
        takeaway="27 unusual rows out of 6,000 swung the dashboard number. Robust measures and a look at the data come first.",
    )
    deck.image(
        f"Raising limits for everyone would add about {true:.1%} to spend, not {naive:.0%}",
        figs / "fig03_naive_vs_true_effect.png",
        bullets=[
            "**Income** drives both the limit we set and what customers spend.",
            f"We already raise limits for heavy users: they spend **{spend_ratio:.1f}×** more.",
            "Most customers use only 15–35% of their limit, so a higher limit changes nothing for them.",
        ],
        image_share=0.6,
        takeaway="A blanket increase adds credit risk on the whole book to gain spend from about 1 customer in 20.",
    )
    deck.image(
        "Most customers are nowhere near their limit",
        figs / "fig02_utilisation_headroom.png",
        takeaway="Only the small group at the right could spend more with a higher limit. Target and test them instead.",
    )
    deck.image(
        "App users spend MORE within every customer group; the opposite pooled pattern is a mix-up of segments",
        figs / "fig04_logins_reversal.png",
        takeaway=(f"Pooled: {pooled:+.2f}. Within segments: {within.min():+.2f} to {within.max():+.2f}. ".replace("-", "−")
                  + "Mass customers log in most but spend least."),
    )
    deck.image(
        "Age matters: spending (relative to income) peaks in the early 40s",
        figs / "fig05_age_inverted_u.png",
        takeaway="Correlation measures straight lines only. A rise-then-fall pattern shows up as 'zero correlation'.",
    )
    deck.image(
        "Marketing and card spend both grew, but month-to-month they don't move together",
        figs / "fig06_spurious_time_series.png",
        takeaway="Any two growing numbers correlate. Measuring marketing's effect needs a proper marketing-mix analysis.",
    )
    deck.bullets(
        "Recommendations",
        [
            "**No blanket limit increase.** Run a **randomised test** of limit increases for near-limit, low-risk customers, "
            "measuring spend and losses.",
            "**Keep the app budget.** Test app campaigns with a holdout group to measure their real effect.",
            "**Keep life-stage (age) targeting**: mid-career customers spend the most.",
            "**Fix the dashboard:** correct the paise error, report corporate cards separately, show scatter plots and robust correlations.",
            "**Commission a marketing-mix analysis** before claiming marketing drives spend.",
        ],
        takeaway="Decision: reject proposals 1–3 as stated; approve two small experiments that measure real effects.",
    )
    deck.two_columns(
        "Limitations and next steps",
        "Limitations",
        ["Snapshot data (6-month averages).", "Engagement measured only by logins.", "Only 36 months for the marketing question."],
        "Next steps",
        ["Design the limit-increase test (sample size, risk guardrails).", "App campaign test with holdout.",
         "Spend model with income, age and segment."],
    )
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
