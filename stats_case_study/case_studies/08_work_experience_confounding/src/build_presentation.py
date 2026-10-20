"""Build the stakeholder deck for Case Study 08 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/08_work_experience_confounding/src/build_presentation.py
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
    path = pd.read_csv(tables / "coefficient_path.csv", index_col=0)
    med = pd.read_csv(tables / "mediation_experience_grade.csv", index_col=0)
    metro = pd.read_csv(tables / "metro_effect.csv", index_col=0)
    ten = pd.read_csv(tables / "tenure_effect.csv", index_col=0)
    edu = pd.read_csv(tables / "education_effect.csv", index_col=[0, 1])
    cv = pd.read_csv(tables / "cv_model_comparison.csv", index_col=0)
    rob = pd.read_csv(tables / "robustness_values.csv", index_col=0)

    exp_v1 = path.loc["M4: + tenure  (= model v1)", "experience (%/yr)"]
    exp_v2 = path.loc["M5: + job grade  (= model v2)", "experience (%/yr)"]
    share = med.loc["share of total that runs through grade", "share (%)"]
    m_raw, m_adj = metro.loc["metro alone", "% effect"], metro.loc["full model v2", "% effect"]
    t_raw, t_adj = ten.loc["tenure alone", "% effect"], ten.loc["full model v2", "% effect"]
    pg_raw = edu.loc[("Postgraduate", "alone"), "% effect"]
    pg_exp = edu.loc[("Postgraduate", "same experience"), "% effect"]
    err = cv["median abs. % error"]

    deck = Deck("Case 08 · Why did work experience stop mattering? · synthetic data")
    deck.title_slide("Why Did \"Work Experience\" Stop Mattering?",
                     "Income-estimation model v2 sign-off · Risk Analytics for Credit Policy",
                     "6,000 salaried customers with verified salaries. Synthetic data created for training. "
                     "Not actual customer data.")
    deck.bullets(
        "Summary: all four proposals rest on one-variable views, and three of them are wrong",
        [
            f"**Experience still matters.** Its effect now shows up through **job grade**: about **{share:.0f}%** of it runs "
            f"through promotions ({exp_v1:+.1f}%/yr → {exp_v2:+.1f}%/yr at the same grade).",
            f"**Metro uplift: reject.** The {m_raw:+.0f}% gap is an employer-type effect; at the same employer it is {m_adj:+.1f}% (not significant).",
            f"**Tenure: keep.** No correlation on its own, but **{t_adj:+.1f}% per year** at the same experience (people who never switched jobs).",
            f"**Education: keep.** Postgraduates look no better paid ({pg_raw:+.1f}%) only because they are younger; "
            f"at the same experience they earn **{pg_exp:.0f}%** more.",
        ],
        takeaway="Recommendation: approve v2 for customers with verified grade, keep v1 for the rest, keep experience on the form.",
        size=17,
    )
    deck.image("The dashboard view: four claims, each from one variable at a time",
               figs / "fig02_four_puzzles.png",
               takeaway="Each chart is correct as a description. None of them shows what happens 'with everything else equal'.")
    deck.image("Experience's effect depends on what else is in the model",
               figs / "fig04_experience_coefficient_path.png",
               takeaway=f"v1 → v2: adding job grade takes over about {share:.0f}% of experience's effect. That part did not disappear; it moved.")
    deck.image("Experience pays off mainly by getting people promoted",
               figs / "fig05_experience_through_grade.png",
               takeaway="Within a grade, extra years add little. But years of experience are what get people to the higher grades.")
    deck.image("Metro customers earn more only because better-paying employers are in metros",
               figs / "fig06_metro_confounding.png",
               takeaway="A metro uplift would pay the employer premium twice. Reject.")
    deck.image("Tenure: zero correlation, yet one of our most useful variables",
               figs / "fig07_tenure_suppression.png",
               takeaway=f"On its own {t_raw:+.1f}%/yr; at the same experience {t_adj:+.1f}%/yr. "
                        "Never drop a variable just because its correlation is near zero.")
    deck.image("Education: the premium was hidden by who our postgraduate customers are",
               figs / "fig08_education_masking.png",
               takeaway="A campus partnership brought in many young postgraduates. Compared at equal experience, the premium is clear.")
    rows = pd.DataFrame({
        "Model": ["v1 (no grade)", "v1 without tenure", "v1 without education", "v2 (with grade)",
                  "v2 without experience", "v2 without tenure", "v2 without metro"],
        "Typical error (median)": [f"{err[k]:.1f}%" for k in ["A2 v1 (no grade)", "A3 v1 − tenure", "A4 v1 − education",
                                                              "B2 v2 (with grade)", "B3 v2 − experience", "B4 v2 − tenure",
                                                              "B5 v2 − metro"]],
        "Verdict": ["Use for the 40% without verified grade", "Worse", "Worse", "Use when grade is verified",
                    "No real difference", "Worse", "No difference"],
    })
    deck.table("Tested on customers the models did not see: what each variable is worth", rows,
               takeaway="With grade known, experience adds little to accuracy; without grade, it is the most important variable we have.",
               col_widths=[1.6, 1.2, 2.2], font_size=15, highlight_rows=[0, 3])
    deck.bullets("How confident are we?",
                 [f"**Experience (total), tenure and education:** a hidden factor (e.g. ability) would have to explain "
                  f"**{rob['RV: confounder strength to remove effect'].loc[['experience, total (v1)', 'tenure (v2)', 'Postgraduate vs Graduate (v1)']].min():.0%}–"
                  f"{rob['RV: confounder strength to remove effect'].loc[['experience, total (v1)', 'tenure (v2)', 'Postgraduate vs Graduate (v1)']].max():.0%}** "
                  "of the remaining variation to overturn them. **Robust.**",
                  f"**Experience at the same grade ({exp_v2:+.1f}%/yr):** a modest hidden factor "
                  f"(≈ {rob.loc['experience, direct (v2)', 'RV: confounder strength to remove effect']:.0%}) could explain it away. **Do not build policy on it.**",
                  "**These are associations**, not proof of cause: we did not run an experiment.",
                  "**Training data must not be filtered on salary** (e.g. 'premium customers only'): that flattens every effect."],
                 takeaway="The recommendations rely only on the robust findings.")
    deck.bullets("Recommendations",
                 ["**Approve model v2** for customers with a payroll-verified grade.",
                  "**Keep model v1** for customers without a verified grade (about 40%).",
                  "**Keep experience** on the application form: v1 depends on it.",
                  "**Keep tenure and education** in both models.",
                  "**Reject the metro uplift.** It double-counts employer type.",
                  "**Follow up** on government/PSU metro customers (about 6% lower pay; may be chance)."],
                 takeaway="Decision needed: sign off v2 with these variable choices.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Observational data: associations, not causes.", "Ability and performance are not measured.",
                      "Education masking is specific to our customer mix."],
                     "Next steps",
                     ["Validate v1 and v2 on next quarter's customers.", "Track the share of customers with verified grade.",
                      "Add this 'why did the coefficient change?' check to every model review."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
