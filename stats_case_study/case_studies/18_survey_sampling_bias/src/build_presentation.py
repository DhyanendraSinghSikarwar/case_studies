"""Build the stakeholder deck for Case Study 18 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/18_survey_sampling_bias/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def sgn(v: float, d: int = 2) -> str:
    return f"{'−' if v < 0 else '+'}{abs(v):.{d}f}"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    grade = pd.read_csv(tables / "estimator_grading.csv", index_col=0)
    naive = pd.read_csv(tables / "naive_estimates.csv", index_col=0)
    rep = pd.read_csv(tables / "representativeness.csv")
    wd = pd.read_csv(tables / "weight_diagnostics.csv", index_col=0)
    fu = pd.read_csv(tables / "followup_estimate.csv", index_col=0)
    tip = pd.read_csv(tables / "tipping_point.csv", index_col=0)
    sim = pd.read_csv(tables / "design_simulation.csv", index_col=0)
    key = pd.read_csv(CASE_DIR / "data" / "answer_key_teaching_only.csv")  # teaching key, used only for the truth line
    act, left = key[key.status == "active"]["true_score"], key[key.status == "left"]["true_score"]

    n_resp, n_frame = int(fu.loc[fu.index[0], "n"]), 40_000
    rate_lo, rate_hi = rep["response rate"].min(), rep["response rate"].max()
    nv, rk = grade.loc["Unweighted (naive)"], grade.loc["Raked"]
    fc = grade.loc["Phone follow-up combined"]
    truth, truth_all = act.mean(), key["true_score"].mean()
    tp, td = (act >= 9).mean(), (act <= 6).mean()
    truth_nps = 100 * (tp - td)
    ess = wd.loc["Raking", "effective sample size"]

    deck = Deck("Case 18 · Customer satisfaction survey · synthetic data")
    deck.title_slide("Who Did We Actually Hear From?",
                     "Why the 7.9 / 10 satisfaction score should not go in the annual report · Retail Banking customer analytics",
                     "40,000 active customers invited; 2,058 answered. Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: a precise number that is wrong",
        [
            f"**The survey says {nv['mean score']:.1f} out of 10 and NPS {sgn(nv['NPS'], 0)}**, with a margin of error of only ±0.07, "
            f"but only **{n_resp / n_frame:.0%}** of customers replied.",
            f"**Respondents are not our customers:** older, more digital and less likely to have complained. Response ranged from "
            f"{rate_lo:.1%} to {rate_hi:.1%} across groups.",
            f"**Weighting to the customer base** lowers the score to {rk['mean score']:.2f} (NPS {sgn(rk['NPS'], 0)}) but still leaves "
            f"most of the error, because happier customers answer more even within a group.",
            f"**A random phone follow-up of non-respondents** gives {fu.loc[fu.index[1], 'mean score']:.2f}, and a combined "
            f"estimate of {fc['mean score']:.2f}. The true value was {truth:.2f} (NPS {sgn(truth_nps, 0)}).",
        ],
        takeaway="Recommendation: do not publish 7.9. Report a range with the response rate, and use a random sample with follow-up next time.",
        size=18,
    )
    deck.kpis("The headline versus what we later learned",
              [(f"{nv['mean score']:.2f}", "Naive survey mean", f"NPS {sgn(nv['NPS'], 0)}; interval {nv['ci_low']:.2f}–{nv['ci_high']:.2f}"),
               (f"{rk['mean score']:.2f}", "After weighting", f"NPS {sgn(rk['NPS'], 0)}; still too high"),
               (f"{fc['mean score']:.2f}", "With phone follow-up", "random sample of non-respondents"),
               (f"{truth:.2f}", "Truth (answer key)", f"NPS {sgn(truth_nps, 0)}; leavers pull all-customer view to {truth_all:.2f}")],
              takeaway="A confidence interval measures sampling error. It said nothing about the +0.80 bias.")
    deck.image("Who answers? Older, app-using, non-complaining customers", figs / "fig01_response_rates.png",
               takeaway="Response rate rises from under 2% for the youngest to about 12% for the over-60s. A representative survey needs similar rates in every group.")
    deck.image("Respondents do not look like our customers", figs / "fig02_respondent_profile.png",
               takeaway="Dots on the right of the grey line are over-represented among respondents; customers with complaints are under-represented.")
    deck.image("Weighting makes respondents look like the customer base, at a price", figs / "fig03_weights.png",
               takeaway=f"Weights run from about 5 to 245. Effective sample size falls from {n_resp:,} to about {ess:,.0f}.")
    rows = pd.DataFrame({
        "Estimate": ["Naive (unweighted)", "Post-stratified", "Raked", "Inverse propensity", "Phone follow-up combined"],
        "Mean score": [f"{grade.loc[k, 'mean score']:.2f}" for k in ["Unweighted (naive)", "Post-stratified", "Raked", "Inverse propensity", "Phone follow-up combined"]],
        "Error vs truth": [sgn(grade.loc[k, "bias"]) for k in ["Unweighted (naive)", "Post-stratified", "Raked", "Inverse propensity", "Phone follow-up combined"]],
        "Interval contains truth?": ["No" if not grade.loc[k, "CI covers the truth?"] else "Yes" for k in
                                     ["Unweighted (naive)", "Post-stratified", "Raked", "Inverse propensity", "Phone follow-up combined"]],
    })
    deck.table(f"Grading the estimates (truth: {truth:.2f})", rows,
               takeaway="Weighting removes about 30% of the error. The follow-up gets closest. No interval contains the truth: bias, not noise, is the problem.",
               col_widths=[2.8, 1.2, 1.4, 1.8], font_size=15, highlight_rows=[4])
    deck.image("Measured error versus the truth", figs / "fig04_estimator_grading.png",
               takeaway=f"Customers who left scored {left.mean():.1f}. Including them, the experience of everyone served this year was {truth_all:.2f}.")
    t_row = tip.loc[0.2]
    deck.bullets(
        "How much hidden bias can a conclusion survive?",
        [f"If non-respondents score just **0.14 points lower** than weighted respondents, the average drops below 7.5.",
         f"At **0.67 points lower** it drops below 7.0. The phone follow-up showed a gap of about 0.36.",
         f"With a 95% non-response rate the non-respondents are almost everyone, so even small differences matter.",
         f"At a gap of 0.2 the implied average is {t_row.iloc[0]:.2f}."],
        takeaway="Very low response rates need a follow-up study before any number is published.",
        size=18,
    )
    deck.image("What a better survey design would have done", figs / "fig05_design_simulation.png",
               takeaway=f"A random 800 has bias 0.00 and {sim.iloc[0, -1]:.0%} coverage. 800 volunteers have bias +0.80 and {sim.iloc[3, -1]:.0%} coverage.")
    deck.bullets("Recommendations",
                 ["**Do not publish 7.9 or NPS +19.** If a number is needed, give a range (about 7.3 to 7.6) with the response rate and who it covers.",
                  "**Compare years only with the same method.** A change in who answers looks like a change in satisfaction.",
                  "**Next survey:** a stratified random sample, reminder waves and a follow-up of a random sample of non-respondents.",
                  "**Add an exit survey** so customers who left are not invisible.",
                  "**Monitor response rate by group** for every survey."],
                 takeaway="Decision needed: approve a random-sample design for the next survey.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Weights use only variables on the customer list; hidden drivers remain.",
                      "Only 60% of the follow-up sample was reached.",
                      "Synthetic population with a chosen response mechanism."],
                     "Next steps",
                     ["Run a stratified random-sample survey in parallel.", "Run an exit survey for leavers.",
                      "Track response rates by age, app use and complaints."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
