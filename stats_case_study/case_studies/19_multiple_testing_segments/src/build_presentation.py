"""Build the stakeholder deck for Case Study 19 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/19_multiple_testing_segments/src/build_presentation.py
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
    res = pd.read_csv(tables / "segment_results.csv", index_col=0)
    adj = pd.read_csv(tables / "multiplicity_adjusted.csv", index_col=0)
    null = pd.read_csv(tables / "all_null_simulation.csv", index_col=0)
    wc = pd.read_csv(tables / "winners_curse_two_waves.csv", index_col=0)
    grade = pd.read_csv(tables / "method_grading.csv", index_col=0)
    tiers = pd.read_csv(tables / "tiers.csv", index_col=0)

    n_sig = int((res["p_value"] < 0.05).sum())
    n_bonf, n_holm = int(adj["Bonferroni"].sum()), int(adj["Holm"].sum())
    n_bh = int(adj["BH (FDR 5%)"].sum())
    g_unc, g_holm, g_bh = grade.loc["uncorrected p < 0.05"], grade.loc["Holm"], grade.loc["BH (FDR 5%)"]

    deck = Deck("Case 19 · Testing a campaign across 40 segments · synthetic data")
    deck.title_slide("Which Segments Really Respond to the Campaign?",
                     "Multiple testing across 40 customer segments · Campaign Analytics for Cards Marketing",
                     "Randomised SMS test in 40 segments, two waves, about 258,000 customers. Synthetic data created for training. "
                     "Not actual customer data.")
    deck.bullets(
        "Summary: the campaign works overall, but the 'seven winning segments' are partly luck",
        [
            "**The SMS lifts conversion by about 0.2 percentage points overall** (95% CI 0.04 to 0.40, tested once): real but small.",
            f"**Seven of 40 segments are 'significant' at 5%.** But even a useless campaign would flag about **{null.loc['no correction', 'average number of false alarms']:.0f}** "
            f"segments, and at least one in **{null.loc['no correction', 'P(at least one false alarm)']:.0%}** of campaigns.",
            f"**After correcting for 40 looks:** {n_holm} segments are confirmed (strict, same as the 5% false-discovery screen); four more are promising at a 10% screen.",
            f"**Winners' uplifts are inflated:** wave-1 winners averaged {wc.iloc[0, 1]:+.1f} points in wave 1 and only {wc.iloc[1, 1]:+.1f} in fresh wave-2 data.",
        ],
        takeaway="Recommendation: keep the broad campaign, budget on shrunken uplifts, and confirm the promising segments in a third wave.",
        size=16,
    )
    deck.image("Forest plot: seven segments cross the line, but with 40 tests that is not surprising",
               figs / "fig01_forest_and_pvalues.png",
               takeaway="Red intervals (left) are the seven segments with p < 0.05. The spike of small p-values (right) says some segments truly respond; the flat part says many do not.")
    deck.image("If the campaign did nothing, we would still see 'winners'", figs / "fig02_all_null_simulation.png",
               takeaway="Left: the number of 'significant' segments in 5,000 simulated campaigns with no effect anywhere.")
    rows = pd.DataFrame({"Rule": ["p < 0.05, no correction", "Bonferroni (strict, any false alarm)", "Holm (strict, more power)",
                                  "Benjamini-Hochberg, 5% false discoveries"],
                         "Declared winners": [n_sig, n_bonf, n_holm, n_bh],
                         "What it controls": ["nothing", "chance of ANY false winner", "chance of ANY false winner",
                                              "share of false winners among winners"]})
    deck.table("Correcting for 40 looks changes the list", rows,
               takeaway="Strict corrections protect against any false winner but miss real responders. The strict rules found only 2 of the 8 real responders; a 10% false-discovery screen finds 4 but with 2 false entries, so it feeds a confirmation wave.",
               col_widths=[2.8, 1.2, 2.6], font_size=15, highlight_rows=[3])
    deck.image("Where each correction draws the line", figs / "fig03_correction_lines.png",
               takeaway="Points under the green line are discoveries at a 5% false-discovery rate; points under the red line survive the strictest rule.")
    deck.image("The winner's curse: wave-1 winners fall back in wave 2", figs / "fig04_winners_curse.png",
               takeaway=f"Selecting the best-looking segments selects partly for luck. Their average uplift fell from {wc.iloc[0, 1]:+.1f} to {wc.iloc[1, 1]:+.1f} points in fresh data.")
    deck.image("Checking against the truth: evidence strength and what each method declares", figs / "fig05_grading.png",
               takeaway=f"Uncorrected: {int(g_unc['truly positive (correct)'])} real and {int(g_unc['no real effect (false alarm)'] + g_unc['truly harmful (wrong sign)'])} false winners. "
                        f"Holm: {int(g_holm['truly positive (correct)'])} real, none false. BH 5%: {int(g_bh['truly positive (correct)'])} real, "
                        f"{int(g_bh['no real effect (false alarm)'] + g_bh['truly harmful (wrong sign)'])} false.")
    trows = pd.DataFrame({"Tier": [i.split(". ", 1)[1] for i in tiers.index], "Segments": tiers["segments"].astype(int),
                          "Average uplift": [f"{v:+.1f} pp" for v in tiers["mean_uplift_pp"]],
                          "Action": ["Target now", "Confirm in wave 3, then target", "Keep the default campaign", "Do not target; investigate"][: len(tiers)]})
    deck.table("A tiered segment list instead of seven circled winners", trows,
               takeaway="Budget with shrunken uplifts, not the raw wave-1 numbers.",
               col_widths=[3.2, 0.9, 1.1, 2.4], font_size=14)
    deck.bullets("Recommendations",
                 ["**Keep the campaign broad.** Its overall effect is positive; nothing justifies dropping 34 segments.",
                  "**Target the 2 confirmed segments now** and re-test the 4 promising ones in a confirmation wave.",
                  "**Budget with shrunken uplifts.** Raw winners' effects are overstated.",
                  "**Declare the analysis plan in advance:** primary test = overall effect; segment tests = a pre-defined family of 40.",
                  "**Show corrected values (BH q-values) next to p-values** in every experiment report."],
                 takeaway="Decision needed: approve the tiered list and the confirmation wave.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Segments overlap in practice, so error rates are approximate.", "Wave 2 has the same power limits as wave 1.",
                      "Segment tests are underpowered for modest effects."],
                     "Next steps",
                     ["Confirmation wave sized for the promising segments.", "Hierarchical model across type and region.",
                      "Individual-level uplift modelling."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
