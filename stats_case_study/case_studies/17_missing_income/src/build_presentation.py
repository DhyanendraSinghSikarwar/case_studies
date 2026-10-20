"""Build the stakeholder deck for Case Study 17 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/17_missing_income/src/build_presentation.py
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
    return f"{'−' if v < 0 else ''}{abs(v):.{d}f}"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    miss = pd.read_csv(tables / "missingness_by_variable.csv", index_col=0)
    grade = pd.read_csv(tables / "strategy_grading.csv", index_col=0)
    sens = pd.read_csv(tables / "delta_sensitivity.csv", index_col=0)
    pred = pd.read_csv(tables / "scoring_comparison.csv", index_col=0)
    cmp_ = pd.read_csv(tables / "missing_vs_present.csv", index_col=0)
    sim = pd.read_csv(tables / "repeated_sampling_simulation.csv", index_col=0)

    inc_share = miss.loc["monthly_income", "share missing"]
    d_miss, d_pres = cmp_.loc["default rate", "income missing"], cmp_.loc["default rate", "income present"]
    truth = grade["coefficient of log income"].iloc[0] - grade["bias in coefficient"].iloc[0]
    cc = grade.loc["Complete cases (delete missing)"]
    mean_imp = grade.loc["Mean imputation"]
    mi_in = grade.loc["Multiple imputation, outcome INCLUDED"]
    mi_ex = grade.loc["Multiple imputation, outcome EXCLUDED from the imputation model"]
    best_auc = pred["AUC"].idxmax()

    deck = Deck("Case 17 · The missing income problem · synthetic data")
    deck.title_slide("What to Do When a Quarter of Applications Have No Income",
                     "Handling missing income in the personal-loan scorecard · Credit Risk analytics",
                     "8,000 personal-loan applications with a known 12-month outcome. Synthetic data created for training. "
                     "Not actual customer data.")
    deck.bullets(
        "Summary: neither 'delete them' nor 'fill with the average' is safe",
        [
            f"**{inc_share:.0%} of applications have no income**, and it is not random: gig and self-employed applicants, agent and online "
            f"channels and, crucially, **later defaulters** leave it out ({d_miss:.0%} default vs {d_pres:.0%} when income is given).",
            f"**Over 150 repeated datasets, deleting them** weakens the estimated protective effect of income by "
            f"{sim.loc['Complete cases', 'bias (% of benchmark)']:.0f}% and its CI contains the truth only "
            f"{sim.loc['Complete cases', 'CI coverage (nominal 95%)']:.0%} of the time; **mean-filling** weakens it by "
            f"{sim.loc['Mean imputation', 'bias (% of benchmark)']:.0f}% (coverage {sim.loc['Mean imputation', 'CI coverage (nominal 95%)']:.0%}).",
            f"**Multiple imputation that includes the outcome** has the smallest bias ({sim.loc['MI, outcome included', 'bias (% of benchmark)']:.0f}%) and "
            f"{sim.loc['MI, outcome included', 'CI coverage (nominal 95%)']:.0%} coverage; leaving the outcome out is as bad as a single fill "
            f"({sim.loc['MI, outcome excluded', 'bias (% of benchmark)']:.0f}% bias, {sim.loc['MI, outcome excluded', 'CI coverage (nominal 95%)']:.0%} coverage).",
            "**For scoring new applicants the best approach is different:** a simple fill plus a 'income missing' flag, because not "
            "providing income is itself a risk signal.",
        ],
        takeaway="Recommendation: multiple imputation (outcome included) for estimation; mean-fill plus flag for scoring; a sensitivity range for the unknowable part.",
        size=16,
    )
    deck.image("Income is missing for a quarter of applications; score and years for far fewer", figs / "fig01_missingness_overview.png",
               takeaway="Missing credit scores mean 'no credit history' (a thin file), not lost data, so they are modelled differently.")
    deck.image("Who leaves income out? Self-employed, gig workers, agent and online applicants, and later defaulters",
               figs / "fig02_missingness_drivers.png",
               takeaway="Because missingness is related to default itself, deleting these applications selects a healthier sample.")
    rows = pd.DataFrame({
        "Strategy": ["Complete cases (delete)", "Mean imputation", "Group-mean imputation", "Regression imputation (one value)",
                     "Multiple imputation, outcome left out", "Multiple imputation, outcome included"],
        "Income effect": [sgn(grade.iloc[i]["coefficient of log income"]) for i in [0, 1, 2, 4, 6, 7]],
        "Off by": [f"{abs(grade.iloc[i]['coefficient bias (%)']):.0f}%" for i in [0, 1, 2, 4, 6, 7]],
        "Spread of income": [f"{grade.iloc[i]['SD log income']:.2f}" for i in [0, 1, 2, 4, 6, 7]],
    })
    deck.table(f"Estimating the effect of income on default (truth {sgn(truth)}; closer to it is better)", rows,
               takeaway="In this one dataset, deleting and MI-with-outcome look similar and both CIs cover the truth. One dataset can mislead: see the repeated test next.",
               col_widths=[2.6, 1.1, 0.9, 1.1], font_size=15, highlight_rows=[5])
    deck.image("What the filled-in values look like", figs / "fig03_imputed_distributions.png",
               takeaway="Mean-filling puts every missing income at one value; good imputation puts the natural variation back.")
    deck.image("Grading the strategies against the complete data", figs / "fig05_strategy_grading.png",
               takeaway="Left: coefficient and 95% CI for each strategy in the actual dataset. Right: how much each shrinks the spread of income.")
    deck.image("Repeating the exercise on 150 simulated datasets: bias and honesty of each strategy", figs / "fig06_repeated_sampling.png",
               takeaway=f"Deleting: {sim.loc['Complete cases', 'bias (% of benchmark)']:.0f}% bias, {sim.loc['Complete cases', 'CI coverage (nominal 95%)']:.0%} coverage. "
                        f"MI with outcome: {sim.loc['MI, outcome included', 'bias (% of benchmark)']:.0f}% bias, {sim.loc['MI, outcome included', 'CI coverage (nominal 95%)']:.0%} coverage. "
                        "Single fills and MI without the outcome almost never contain the truth.")
    deck.image("What if low earners are the ones hiding income? Sensitivity range", figs / "fig04_delta_sensitivity.png",
               takeaway=f"Even if missing incomes are up to 39% lower than imputed, the income effect stays between {sgn(sens['coefficient of log income'].min())} and "
                        f"{sgn(sens['coefficient of log income'].max())}; the average income level moves by about 11%.")
    rows2 = pd.DataFrame({
        "Approach for scoring a new applicant": [k for k in pred.index],
        "Test AUC": [f"{v:.3f}" for v in pred["AUC"]],
        "Brier score (lower is better)": [f"{v:.4f}" for v in pred["Brier score"]],
    })
    deck.table("Scoring is a different job: keep a 'missing income' flag", rows2,
               takeaway="A fill plus the missing-income flag gives the best AUC (mean and stochastic fills tie). Not providing income is a risk signal in its own right.",
               col_widths=[3.3, 1.0, 1.6], font_size=14, highlight_rows=[list(pred.index).index(best_auc)])
    deck.bullets("Recommendations",
                 ["**Do not delete applications without income, and do not fill with the average.**",
                  "**For coefficients and reporting:** multiple imputation (at least 20 draws) with the default outcome in the imputation model.",
                  "**For production scoring:** fill plus a missing-income flag; review the flag's effect for hidden channel or agent bias.",
                  "**Always show a sensitivity range** for the part no one can test (are low incomes the ones missing?).",
                  "**Fix collection at the source:** agent and online channels drive the gaps. Track the missing rate by channel."],
                 takeaway="Decision needed: approve the imputation approach and the missing-rate KPI.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Simple simulated mechanism; real data are messier.", "One variable imputed; real projects impute several jointly.",
                      "Missing-not-at-random cannot be tested, only bounded."],
                     "Next steps",
                     ["Chase documents for a random sample to measure the true gap.", "Impute several variables jointly and check diagnostics.",
                      "Monitor the missing-income rate by channel."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
