"""Build the stakeholder deck for Case Study 14 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/14_acquisition_channel_anova/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def rs(v: float) -> str:
    return f"{'−' if v < 0 else ''}₹{abs(v):,.0f}"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    desc = pd.read_csv(tables / "channel_summary.csv", index_col=0)
    econ = pd.read_csv(tables / "channel_economics.csv", index_col=0)
    anc = pd.read_csv(tables / "ancova_channel_effects.csv", index_col=0)
    anova = pd.read_csv(tables / "anova_table.csv", index_col=0)
    welch = pd.read_csv(tables / "classic_vs_welch.csv", index_col=0)

    eta2 = anova.loc["channel", "share of total SS (η² for channel)"]
    half = (econ["net ci_high"] - econ["net ci_low"]) / 2
    deck = Deck("Case 14 · Which acquisition channel brings the most valuable customers? · synthetic data")
    deck.title_slide("Where Should Next Year's Acquisition Budget Go?",
                     "Comparing five card-acquisition channels · Cards Marketing analytics",
                     "6,000 customers acquired last year, first-year net revenue and cost per acquisition by channel. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: the aggregator is not our best channel, and social media is not our worst investment",
        [
            f"**Channels do differ in first-year revenue per customer**, but only **social media** is reliably lower "
            f"({rs(desc.loc['Social media', 'mean'])} vs about ₹3,050–3,300 elsewhere).",
            f"**The aggregator's lead is not reliable** and comes from **richer customers**: at the same income, its customers are worth "
            f"about **₹{abs(anc.loc['Aggregator', 'at the same income (₹)']):,.0f} less** than branch customers.",
            f"**After acquisition cost, the partner co-brand is best** ({rs(econ.loc['Partner co-brand', 'net value per customer (₹)'])} net "
            f"per customer) and the **aggregator worst** ({rs(econ.loc['Aggregator', 'net value per customer (₹)'])}).",
            "**Social media is cheap:** it returns more value per rupee than branch, search or the aggregator.",
        ],
        takeaway="Recommendation: do not double the aggregator or cut social media; grow the partner channel and test before big shifts.",
        size=16,
    )
    deck.image("Customers vary far more within a channel than between channels", figs / "fig01_revenue_by_channel.png",
               takeaway=f"Channel explains only about {eta2:.0%} of the variation in customer revenue, but ₹ differences × volume still matter.")
    deck.image("Which channels really differ? Only social media stands out", figs / "fig03_posthoc.png",
               takeaway="All 10 pairs compared at once, with a correction so that chance differences are not mistaken for real ones.")
    deck.image("The aggregator's advantage is its customers' income, not the channel", figs / "fig04_ancova.png",
               takeaway="High-income customers from the aggregator are worth less than high-income customers from other channels.")
    rows = pd.DataFrame({
        "Channel": econ.index,
        "Revenue per customer": [rs(v) for v in econ["mean value (₹)"]],
        "Cost per acquisition": [rs(v) for v in econ["cost per acquisition (₹)"]],
        "Net per customer": [rs(v) for v in econ["net value per customer (₹)"]],
        "Value per ₹1 spent": [f"₹{v:.2f}" for v in econ["value per ₹ of CAC"]],
    })
    deck.table("Net of what each customer cost us, the ranking reverses", rows,
               takeaway="The aggregator has the highest revenue per customer and the lowest return on spend.",
               col_widths=[1.6, 1.2, 1.2, 1.2, 1.1], font_size=15,
               highlight_rows=[list(econ.index).index("Partner co-brand")])
    deck.image("What the next ₹1 lakh would buy, at today's costs", figs / "fig05_channel_economics.png",
               takeaway="Averages, not marginal returns: doubling a channel's budget may bring worse or costlier customers.")
    deck.kpis("How sure are we?",
              [(f"p < 0.001", "channels differ (Welch test)", f"F = {welch.iloc[1]['F']:.1f}; robust to unequal spreads."),
               (f"{eta2:.0%}", "of customer variation explained by channel", "Small per customer, material across thousands."),
               (f"±₹{half.min():,.0f}–{half.max():,.0f}", "95% range on net value per customer", "Partner clearly best; aggregator's range nearly reaches zero.")],
              takeaway="The ranking of partner (best) and aggregator (worst) is robust; the middle three are closer.")
    deck.bullets("Recommendations",
                 ["**Do not double the aggregator budget.** It is the most expensive channel and, at the same income, the weakest.",
                  "**Do not cut social media** on revenue alone: it is cheap and returns more per rupee than branch or aggregator.",
                  "**Grow the partner co-brand** as far as its capacity allows.",
                  "**Test whether high-income customers can be reached more cheaply** through search or partners.",
                  "**Run a controlled budget test** (some regions or weeks) before any large shift, to measure marginal returns."],
                 takeaway="Decision needed: approve a partner-led reallocation and a budget-shift test.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Observed, not randomised: channels were not assigned at random.",
                      "Average, not marginal, costs and values.",
                      "First-year value only; retention may differ."],
                     "Next steps",
                     ["Geo budget-shift experiment.", "Extend to lifetime value.", "Add card type as a second factor."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
