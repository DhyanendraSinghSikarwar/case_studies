"""Build the stakeholder deck for Case Study 20 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/20_simpsons_paradox_approvals/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def pp(v: float, d: int = 1) -> str:
    return f"{'−' if v < 0 else '+'}{abs(v):.{d}f}"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    ov = pd.read_csv(tables / "overall_comparison.csv", index_col=0)
    bb = pd.read_csv(tables / "by_risk_band.csv", index_col=0)
    dec = pd.read_csv(tables / "decomposition.csv", index_col=0)
    mix = pd.read_csv(tables / "risk_mix.csv", index_col=0)
    chm = pd.read_csv(tables / "channel_mix.csv", index_col=0)
    std = pd.read_csv(tables / "standardised_rates.csv", index_col=0)
    mh = pd.read_csv(tables / "mantel_haenszel.csv", index_col=0)

    d_all = ov.loc["difference (percentage points)", "estimate"]
    rate_e, mix_e = dec.loc["TOTAL", "rate (within-band) effect (pp)"], dec.loc["TOTAL", "mix (composition) effect (pp)"]
    cd0, cd1 = mix.loc["Before", ["C", "D"]].sum(), mix.loc["After", ["C", "D"]].sum()
    std_pool = std.loc["Pooled mix (all applications)"]

    deck = Deck("Case 20 · Did the new approval policy hurt approval rates? · synthetic data")
    deck.title_slide("Did the New Approval Policy Reduce Approvals?",
                     "Why overall approval fell while every risk band improved · Credit Policy analytics",
                     "27,000 personal-loan applications, before and after the April policy change. Synthetic data created for training. "
                     "Not actual customer data.")
    deck.bullets(
        "Summary: overall approval fell, but only because riskier applicants arrived; the policy is more generous at every level",
        [
            f"**Overall approval fell {abs(d_all):.1f} points** ({ov.loc['approval rate before', 'estimate']:.1%} → {ov.loc['approval rate after', 'estimate']:.1%}).",
            f"**Within every risk band it rose by {bb['difference (pp)'].min():.0f}–{bb['difference (pp)'].max():.0f} points.** This is Simpson's paradox.",
            f"**Why:** the share of applicants in the two riskiest bands rose from {cd0:.0%} to {cd1:.0%}. The change splits exactly into "
            f"**{pp(rate_e)} points from the policy** and **{pp(mix_e)} points from who applied**.",
            f"**The cause is the new agent channel** ({chm.loc['Before', 'Agent']:.0%} → {chm.loc['After', 'Agent']:.0%} of applications). "
            "The risk mix within each channel did not change.",
        ],
        takeaway="Recommendation: do not roll back the policy; report approval by risk band and standardised, and monitor defaults.",
        size=16,
    )
    deck.image("The paradox: down overall, up in every risk band", figs / "fig01_the_paradox.png",
               takeaway="Left: approval before and after. Right: the change by band (green) and overall (red).")
    deck.image("Why: a riskier applicant mix hides the policy's effect", figs / "fig02_mix_and_decomposition.png",
               takeaway=f"Overall change {pp(d_all)} points = policy effect {pp(rate_e)} + mix effect {pp(mix_e)}.")
    deck.image("What changed the mix: the agent channel", figs / "fig03_channel_mix.png",
               takeaway="Agent applicants are mostly in the two riskiest bands. Within each channel, risk did not shift.")
    rows = pd.DataFrame({"Comparison": ["Raw overall comparison", "At the before-policy mix", "At the after-policy mix", "Mantel-Haenszel odds ratio"],
                         "Result": [f"{pp(d_all)} points", f"{pp(std.iloc[0]['difference (pp)'])} points", f"{pp(std.iloc[1]['difference (pp)'])} points",
                                    f"{mh.iloc[0]['estimate']:.2f} (95% CI {mh.iloc[0]['ci_low']:.2f}–{mh.iloc[0]['ci_high']:.2f})"],
                         "Answers": ["Policy + who applied", "The policy, same applicants", "The policy, same applicants", "The policy, band by band"]})
    deck.table("Fair comparisons all agree: the policy raised approvals", rows,
               takeaway=f"Standardised difference: {pp(std_pool['difference (pp)'])} points (95% CI {pp(std_pool['ci_low (pp)'])} to {pp(std_pool['ci_high (pp)'])}).",
               col_widths=[2.4, 2.2, 2.4], font_size=15, highlight_rows=[1, 2, 3])
    deck.image("Which comparison is right depends on the causal story", figs / "fig04_causal_stories.png",
               takeaway="Our data fit story A: the campaign, not the policy, changed who applies. Timing and process knowledge confirm this, not statistics alone.")
    deck.bullets("What this analysis does not show",
                 ["**Whether the extra approvals are good.** We have not looked at defaults yet.",
                  "**Whether anything else changed** between the two periods (seasonality, other campaigns). There is no control group.",
                  "**Whether finer risk groups would change the picture.** Four bands are coarse.",
                  "**Effects on the total portfolio.** The agent campaign made the book riskier regardless of the policy."],
                 takeaway="Adjusting for measured bands removes the mix effect, but not unmeasured time effects.")
    deck.bullets("Recommendations",
                 ["**Do not roll back the policy.** At every risk level it is more generous, as intended.",
                  "**Report approval by risk band and standardised to a fixed mix** every quarter, next to the overall rate.",
                  "**Brief the Chief Risk Officer with the decomposition:** about +5.6 points from policy, −9.5 from who applied.",
                  "**Monitor default rates by channel and band** to judge the extra approvals.",
                  "**Run the next policy change as a staged roll-out** with a comparison group."],
                 takeaway="Decision needed: approve the reporting change and the default monitor.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Before/after comparison without a control group.", "Four risk bands only.", "No default outcomes yet."],
                     "Next steps",
                     ["Link approvals to 12-month defaults.", "Monthly rate-and-mix dashboard.", "Staged or randomised roll-out for the next change."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
