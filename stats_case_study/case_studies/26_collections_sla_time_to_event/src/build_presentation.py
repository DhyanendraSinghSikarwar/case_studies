"""Build the stakeholder deck for Case Study 26 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/26_collections_sla_time_to_event/src/build_presentation.py
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
    arr = pd.read_csv(tables / "arrivals_by_hour.csv", index_col=0)
    staff = pd.read_csv(tables / "staffing_erlang_c.csv", index_col=0)
    naive = pd.read_csv(tables / "naive_summaries.csv", index_col=0)["value"]
    km = pd.read_csv(tables / "km_overall.csv", index_col=0)
    grp = pd.read_csv(tables / "km_by_group.csv")
    cox = pd.read_csv(tables / "cox_hazard_ratios.csv", index_col=0)
    seg = pd.read_csv(tables / "sla_by_segment.csv")
    gr = pd.read_csv(tables / "grading_segments.csv")

    sla = km.loc["resolved by day 30", "estimate"]
    lo, hi = km.loc["resolved by day 30", "ci_low"], km.loc["resolved by day 30", "ci_high"]
    report = naive.iloc[1]
    g = grp.set_index("group")
    n_cover = int(gr["KM CI covers"].sum())

    deck = Deck("Case 26 · Collections and SLA · synthetic data")
    deck.title_slide("Are We Meeting the 30-Day Collections SLA?",
                     "Censored durations, survival curves and staffing the call desk · Collections analytics",
                     "6,000 synthetic overdue accounts and 20 days of call arrivals. Synthetic data created for training. Not actual customer data.")
    deck.bullets(
        "Summary: the report says 61%; the right answer is 42%, and no segment meets the 70% SLA",
        [
            f"**The report divided by resolved accounts** and got {report:.0%} paid within 30 days. A third of accounts are still open or transferred, mostly slow cases.",
            f"**Kaplan-Meier, which uses every account for as long as it was observed, gives {sla:.0%}** (95% CI {lo:.0%} to {hi:.0%}); median {km.loc['median days to resolve', 'estimate']:.0f} days.",
            f"**Call-first speeds resolution** (hazard ratio {cox.loc['call_first', 'hazard ratio']:.2f}, CI {cox.loc['call_first', 'ci_low']:.2f} to {cox.loc['call_first', 'ci_high']:.2f}); late-bucket and high-balance accounts are slower. "
            "Even so, all 12 segments miss 70%.",
            f"**Call arrivals peak at 11:00 and 15:00 (about 14 per 15 minutes):** {staff['agents needed (80/20)'].min()} to {staff['agents needed (80/20)'].max()} agents needed by hour.",
        ],
        takeaway="Recommendation: re-base the SLA report on survival curves, expand call-first, and revisit the target.",
        size=16,
    )
    deck.image("Call arrivals: Poisson within the hour, but the rate changes through the day", figs / "fig01_arrivals.png",
               takeaway="Within each hour the variance equals the mean (no hour rejects Poisson). Across the day the variance is twice the mean because the rate moves.")
    rows = pd.DataFrame({"Hour": [f"{h:02d}:00" for h in staff.index], "Calls per 15 min": [f"{v:.1f}" for v in staff["calls per 15 min"]],
                         "Agents needed": [int(v) for v in staff["agents needed (80/20)"]],
                         "Service level": [f"{v:.0%}" for v in staff["service level at that staffing"]]})
    deck.table("Staffing by hour for 80% of calls answered in 20 seconds", rows,
               takeaway="Assumes 6-minute handling time and Poisson arrivals. A flat roster would be overloaded at the peaks and idle at lunch.",
               col_widths=[1.3, 1.8, 1.6, 1.6], font_size=14)
    deck.bullets(
        "Why the report's number is wrong",
        [f"**{naive.iloc[0]:.1f} days average and {naive.iloc[1]:.0%} within 30 days** use only accounts that were paid up.",
         "That leaves out every account still open or transferred, and slow cases are over-represented among them.",
         f"If open accounts are counted as events at their last day the average becomes {naive.iloc[2]:.0f} days; if counted as unresolved the 30-day share is {naive.iloc[3]:.0%}.",
         "None of these answers the SLA question: what share of accounts entering collections are paid within 30 days?"],
        takeaway="A censored account tells us it had not paid by its last day, not when it will.", size=17)
    deck.image("Survival curve: 42% resolved by day 30", figs / "fig02_km_overall.png",
               takeaway=f"Kaplan-Meier with 95% interval. At 60 days {km.loc['resolved by day 60', 'estimate']:.0%}; at 90 days {km.loc['resolved by day 90', 'estimate']:.0%}.")
    deck.image("Resolution by strategy, bucket and balance", figs / "fig03_km_groups.png",
               takeaway=f"Resolved by day 30: call-first {g.loc['call_first', 'resolved by 30 days']:.0%} vs SMS-first {g.loc['sms_first', 'resolved by 30 days']:.0%}; "
                        f"early {g.loc['early', 'resolved by 30 days']:.0%} vs late {g.loc['late', 'resolved by 30 days']:.0%}.")
    crow = pd.DataFrame({"Factor": ["Call-first (vs SMS-first)", "Late bucket (vs early)", "Balance mid (vs low)", "Balance high (vs low)"],
                         "Hazard ratio": [f"{v:.2f}" for v in cox["hazard ratio"]],
                         "95% interval": [f"{a:.2f} to {b:.2f}" for a, b in zip(cox["ci_low"], cox["ci_high"])]})
    deck.table("Effect on the speed of resolution (Cox model)", crow,
               takeaway="Above 1 means faster. A ratio of 1.41 is a 41% higher rate of resolution at any time, not 41% more accounts resolved.",
               col_widths=[3.0, 1.4, 2.0], font_size=15)
    deck.image("Estimated resolution by day 30, every segment versus the truth", figs / "fig06_segments_vs_truth.png",
               takeaway=f"All 12 segments are below the 70% line. The Kaplan-Meier interval covers the truth in {n_cover} of 12 segments.")
    deck.bullets("Recommendations",
                 ["**Re-base SLA reporting** on Kaplan-Meier probabilities (30, 60, 90 days) with intervals, by segment.",
                  "**Expand call-first,** especially for late-bucket and high-balance accounts; alone it lifts the 30-day share from about 42% to 48%.",
                  "**Revisit the 70%-in-30-days target** or set segment targets; 60 days is about 61%.",
                  "**Roster by hour** with Erlang C: 4 agents at 13:00, 9 at the peaks.",
                  "**Randomise strategy** in the next cycle to measure the causal effect."],
                 takeaway="Decision needed: change the SLA metric and approve a randomised strategy test.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Censoring assumed unrelated to the chance of paying.", "Strategy was not randomised.",
                      "Handling time assumed exponential and fixed.", "The Weibull model is right here by construction."],
                     "Next steps",
                     ["Randomised call-first test.", "Time-varying covariates in the Cox model.", "Competing risks: paid, written off, transferred.",
                      "Sensitivity analysis for informative censoring."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
