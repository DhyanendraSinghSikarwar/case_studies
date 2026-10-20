"""Build the stakeholder deck for Case Study 15 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/15_branch_processing_nonparametric/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def pfmt(p: float) -> str:
    return "p < 0.001" if p < 0.001 else f"p = {p:.2f}" if p >= 0.01 else f"p = {p:.3f}"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    desc = pd.read_csv(tables / "branch_summary.csv", index_col=0)
    bt = pd.read_csv(tables / "branch_tests.csv", index_col=0)
    dunn = pd.read_csv(tables / "dunn_posthoc.csv")
    pt = pd.read_csv(tables / "paired_tests.csv", index_col=0)
    pilot = pd.read_csv(CASE_DIR / "data" / "workflow_pilot.csv")
    change = pilot["days_after"] - pilot["days_before"]
    n_fast = int((change < 0).sum())
    hl = pt.iloc[1]

    deck = Deck("Case 15 · Branch loan processing times and a new workflow · synthetic data")
    deck.title_slide("Which Branches Are Slow, and Did the New Workflow Help?",
                     "Branch comparison and workflow pilot · Lending Operations analytics",
                     "190 personal loans from 5 branches; a 20-officer workflow pilot. "
                     "Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: two branches are slower, and the workflow saves about a day; the 'not significant' verdict came from the wrong test",
        [
            f"**Panvel and Thane are slower:** typical times {desc.loc['Panvel', 'median']:.0f} and {desc.loc['Thane', 'median']:.0f} days vs "
            f"about {desc.loc[['Andheri', 'Borivali', 'Vashi'], 'median'].mean():.0f} at Andheri, Borivali and Vashi.",
            f"**Averages hide it:** a few 'stuck' loans of 40–70 days blur the means. A test of averages found nothing "
            f"({pfmt(bt.iloc[0]['p_value'])}); a test of typical times found a clear difference ({pfmt(bt.iloc[3]['p_value'])}).",
            f"**The new workflow cut a typical officer's time by about a day** (≈ 12%): {n_fast} of {len(pilot)} officers got faster.",
            f"**One officer got {change.max():.0f} days slower** because of an unrelated system migration. It dragged the average change "
            f"to {change.mean():+.1f} days and made the usual test say '{pfmt(pt.iloc[0]['p_value'])}'.",
        ],
        takeaway="Recommendation: roll out the workflow after fixing the migration issue; review processes at Panvel and Thane.",
        size=16,
    )
    deck.image("Stuck loans dominate the raw numbers; on a log scale the branch differences show",
               figs / "fig01_branch_times.png",
               takeaway="Every branch has a few loans stuck for 40–70 days; typical loans at Panvel and Thane take longer.")
    rows = pd.DataFrame({
        "Test": ["Test of averages (ANOVA)", "Test of averages, unequal spread (Welch)", "Test of log times (ANOVA)",
                 "Test of typical times (Kruskal-Wallis)"],
        "Result": [pfmt(p) for p in bt["p_value"]],
        "Verdict": ["No difference found", "No difference found", "Branches differ", "Branches differ"],
    })
    deck.table("Same data, opposite answers: it depends on what the test compares", rows,
               takeaway="Stuck loans inflate the noise in average-based tests. Pick the test from the question and the data's shape, before looking at results.",
               col_widths=[3.0, 1.2, 1.6], font_size=15, highlight_rows=[3])
    deck.image("How often is a loan at one branch slower than at another?", figs / "fig02_pairwise_superiority.png",
               takeaway=f"{int(dunn['significant (Holm, 5%)'].sum())} of 10 pairs differ after correcting for multiple comparisons; "
                        "Andheri, Borivali and Vashi are indistinguishable.")
    deck.image("Workflow pilot: most officers got faster; one got much slower", figs / "fig03_pilot_changes.png",
               takeaway="The one slow officer (red) was affected by a system migration, not by the workflow.")
    rows2 = pd.DataFrame({
        "Test": ["Paired t-test (average change)", "Wilcoxon signed-rank (typical change)", "Sign test (how many improved)",
                 "Permutation test (average change)"],
        "Result": [pfmt(p) for p in pt["p_value"]],
        "Verdict": ["Not significant", "Significant", "Significant", "Not significant"],
    })
    deck.table("Workflow: the verdict depends on whether one extreme officer is allowed to dominate", rows2,
               takeaway=f"Typical change: {hl['estimate (days)']:.1f} days (95% range {hl['ci_low']:.1f} to {hl['ci_high']:.1f}). "
                        "Without the migration-affected officer, every test agrees.",
               col_widths=[3.0, 1.2, 1.6], font_size=15, highlight_rows=[1])
    deck.image("When does each test win? Simulation with 20 pairs", figs / "fig04_power_simulation.png",
               takeaway="With outliers or heavy tails, rank-based tests detect real effects far more often; with clean normal data, they lose very little.")
    deck.bullets("Recommendations",
                 ["**Roll out the new workflow**, after resolving the migration problem that delayed one officer.",
                  "**Review processes at Panvel and Thane**, separately from the stuck-loan problem, which affects every branch.",
                  "**Report median processing time** and the **share of loans over 20 days** as two separate measures.",
                  "**Use rank-based tests** for small samples of processing times; use averages only when ₹ totals matter.",
                  "**Roll out in stages** with comparison branches, so improvement can be separated from seasonality."],
                 takeaway="Decision needed: approve the roll-out and the process reviews.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Branch case mix (loan size, customer type) may differ.",
                      "The pilot had no control group.", "20 officers, one month before and after."],
                     "Next steps",
                     ["Stepped roll-out across branches.", "Model time-to-disbursement with loan characteristics.",
                      "Early-warning flag for stuck loans."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
