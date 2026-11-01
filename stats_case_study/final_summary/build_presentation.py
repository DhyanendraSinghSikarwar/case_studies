"""Build the closing deck for the book: the statistics playbook.

    python final_summary/build_presentation.py
Writes final_summary/presentation/statistics_playbook.pptx
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "00_shared_resources"))
from presentation import Deck  # noqa: E402


def main() -> None:
    deck = Deck("Statistics for Data Science · the playbook · synthetic case studies")
    deck.title_slide("The Statistics Playbook",
                     "What 27 business cases teach about asking, analysing and deciding",
                     "Summary of the case-study book. All data in the cases are synthetic, created for training.")
    deck.bullets("The workflow every case follows",
                 ["**Business question** → statistical question → outcome and population.",
                  "**Data quality** → look at the data → pick the method (with alternatives).",
                  "**Assumptions** → analysis → validation.",
                  "**Interpretation** → what can and cannot be said → recommendation → limitations.",
                  "**Start from the question,** never from 'which test can I run?'."],
                 takeaway="A result is only as good as the question, the data and the validation behind it.", size=20)
    rows = pd.DataFrame({
        "You want to…": ["Compare two means", "Compare two proportions", "Compare 3+ groups", "Many segments at once", "Predict yes / no", "Time to an event", "Forecast a series", "Update a belief"],
        "Use": ["Welch t; Mann-Whitney for heavy tails", "Two-proportion z; Fisher if small", "ANOVA / Kruskal-Wallis, then post-hoc", "Holm or Benjamini-Hochberg",
                "Logistic regression; calibration and cost", "Kaplan-Meier, Cox", "Seasonal naive baseline; rolling origin", "Bayes, Beta-Binomial"],
        "Cases": ["02, 15", "03, 04", "14, 15", "19", "11, 12, 13, 27", "26", "25", "24"],
    })
    deck.table("Which method for which question", rows, takeaway="The method follows the estimand, the data and the decision.",
               col_widths=[2.4, 4.2, 1.5], font_size=13)
    deck.two_columns("Reading results correctly", "Always",
                     ["Report the estimate, the interval and the effect size.", "Compare the interval with a decision threshold.", "Say how many things were examined.",
                      "Validate on data the method did not see."],
                     "Never",
                     ["Treat p < 0.05 as 'it matters' or p > 0.05 as 'no effect'.", "Read an interval as covering bias.", "Peek at a running test.",
                      "Compare the model with itself, not with a baseline."],
                     takeaway="Statistical significance is not practical significance (cases 04, 22).")
    deck.bullets("Association is not causation",
                 ["**Selection:** engaged customers enrol and also churn less (case 21).",
                  "**Adjusting for what you can measure** gives confident, wrong intervals when something unmeasured matters (case 21).",
                  "**Randomise the offer;** read the intention-to-treat and complier effects (cases 04, 21).",
                  "**Segments can reverse the total** (case 20); **selected winners are overstated** (cases 19, 22).",
                  "**Proxies mimic drivers:** the agent channel and the interest rate in case 27."],
                 takeaway="Use 'associated with' unless the design supports 'causes'.", size=18)
    deck.bullets("Messy data and special data",
                 ["**Outliers:** decide what they are before touching them (16).", "**Missing values:** ask why; multiple imputation with the outcome (17).",
                  "**Biased samples:** weights fix only what you measure; follow up non-respondents (18).", "**Skewed statistics:** bootstrap, with its limits (23).",
                  "**Time series:** rolling-origin tests against seasonal naive (25).", "**Censored durations:** Kaplan-Meier, never the mean of finished cases (26)."],
                 takeaway="The quality of the data sets the ceiling for every method.", size=17)
    lessons = pd.DataFrame({
        "Case": ["18", "19", "21", "22", "24", "25", "26", "27"],
        "The lesson": ["A precise number from the wrong people is still wrong", "Corrected p-values, winner's curse, tiered list", "Adjustment gave narrow, wrong intervals; the pilot gave the answer",
                       "Compare the interval with the break-even; inconclusive is honest", "The base rate does as much work as the screen", "Autocorrelation breaks ordinary methods; beat seasonal naive",
                       "Censoring makes naive shares wrong (61% vs 42%)", "Proxies, confounding, out-of-time validation and a costed decision"],
    })
    deck.table("Highlights from the later cases", lessons, takeaway="Every case ends with 'what we can say, what we cannot, and what to do'.",
               col_widths=[0.8, 6.4], font_size=13)
    deck.bullets("Before you present: ten checks",
                 ["Question and population stated? Data quality checked and logged?", "Interval, effect size and a practical threshold for every number?",
                  "Assumptions checked? Number of tests counted and corrected?", "Validated out of sample or out of time?",
                  "Causal language only where the design supports it?", "What the analysis cannot tell us stated?",
                  "What would change the recommendation if the main assumption failed?"],
                 takeaway="Full checklists: final_summary/decision_framework.md and statistics_cheat_sheet.md.", size=17)
    out = deck.save(ROOT / "final_summary" / "presentation" / "statistics_playbook.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
