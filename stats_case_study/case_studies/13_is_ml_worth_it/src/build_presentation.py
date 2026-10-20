"""Build the stakeholder deck for Case Study 13 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/13_is_ml_worth_it/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402

ML_COST = 45


def lakh(x: float) -> str:
    return f"{'−' if x < 0 else ''}₹{abs(x):,.0f} lakh"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    key = pd.read_csv(tables / "key_results.csv", index_col=0)
    value = pd.read_csv(tables / "value_comparison.csv", index_col=0)
    oot = pd.read_csv(tables / "oot_delong_bootstrap.csv", index_col=0)
    claim = pd.read_csv(tables / "ml_team_claim_reproduced.csv", index_col=0).iloc[:, 0]
    lab = pd.read_csv(tables / "scenario_lab.csv", index_col=0)
    split = pd.read_csv(tables / "dev_oot_split.csv", index_col=0)

    m0, m1, m2, m3 = "M0 current scorecard", "M1 full linear", "M2 spec. GLM", "M3 GBM"
    auc = key["OOT AUC"]
    v20 = value.loc[f"{m2} − {m0}"]
    v32 = value.loc[f"{m3} − {m2}"]
    d32 = oot.loc[f"{m3} − {m2}"]
    d20 = oot.loc[f"{m2} − {m0}"]
    n_apps = int(split["applications"].sum())
    leak_auc = claim.filter(like="WITH leakage").iloc[0]
    noleak_auc = claim.filter(like="without leakage").iloc[0]
    m0_rand = claim.filter(like="Current scorecard").iloc[0]

    deck = Deck("Case 13 · Is a machine-learning model worth it? · synthetic data")

    deck.title_slide(
        "Should We Replace Our Scorecard with Machine Learning?",
        "Independent model review for the Chief Risk Officer and Model Risk Committee · Credit Risk Analytics",
        f"{n_apps:,} card applications (Jan-2023 to Dec-2024) with 12-month outcomes. "
        "Synthetic data created for training. Not actual customer data.",
    )

    deck.bullets(
        "Summary: upgrade the scorecard; do not adopt the ML model yet",
        [
            f"**The ML team's 'AUC 0.93' is not real.** It relies on a field recorded **after** customers fall into arrears. "
            f"Without that field, the ML model is no better than today's scorecard ({noleak_auc:.2f} vs {m0_rand:.2f}).",
            f"**A better scorecard is available now.** Using statistical tests to model curves and one key interaction lifts "
            f"accuracy on new customers (AUC {auc[m0]:.3f} → {auc[m2]:.3f}), worth about **{lakh(v20['value_gain_lakh_per_year'])} a year**.",
            f"**The ML model does not beat the improved scorecard** on new customers (AUC {auc[m3]:.3f} vs {auc[m2]:.3f}). "
            f"Its extra value is uncertain and roughly equal to its ₹{ML_COST} lakh running cost.",
            "**ML is not ruled out forever.** It is catching up as data grows. We set a clear test it must pass.",
        ],
        takeaway="Recommendation: deploy the improved scorecard; run the ML model as a silent challenger; review in 12 months.",
        size=17,
    )

    deck.two_columns(
        "The question: is the ML model's gain real, big enough, and lasting?",
        "What the CRO asked",
        [
            "Is the ML team's improvement real?",
            "Is it big enough to matter in money?",
            "Will it hold on new customers?",
            "Could an improved scorecard do just as well?",
        ],
        "Why the bar for ML is high",
        [
            "Harder to explain decline reasons to customers and the regulator.",
            "Extended model-risk validation and bias testing.",
            "New monitoring and retraining infrastructure.",
            f"≈ ₹{ML_COST} lakh a year extra running cost.",
        ],
        takeaway="ML must beat the BEST simple model by more than its cost, on future customers. Beating the old scorecard is not enough.",
    )

    deck.kpis(
        "How we tested it",
        [
            (f"{n_apps:,}", "applications", "Numerical, ordered and unordered customer attributes."),
            ("18 + 6", "months: build + test", "Models built on older data and tested on the 6 most recent months."),
            ("4", "models compared", "Current scorecard, full scorecard, improved scorecard, ML."),
            ("5", "independent tests", "Cross-validation, out-of-time, DeLong, McNemar, value with uncertainty."),
        ],
        takeaway="Testing on later months mimics real use: the model always scores customers it has never seen.",
    )

    deck.kpis(
        "The ML team's headline came from a field we cannot use at application time",
        [
            (f"{leak_auc:.2f}", "ML with the leaky field", "Reproduces (and exceeds) the claimed 0.93."),
            (f"{noleak_auc:.2f}", "ML without it", "Same random-split test as the ML team."),
            (f"{m0_rand:.2f}", "current scorecard", "Same test: no meaningful difference."),
            ("After", "when the field is filled", "Collections contact happens once a customer is already in arrears."),
        ],
        takeaway="'Too good to be true' results usually are. Every model review must check when each field is recorded.",
    )

    deck.image(
        "Risk follows curves and thresholds, which a well-built scorecard can capture",
        figs / "fig01_binned_logodds.png",
        bullets=[
            "**Utilisation:** risk is high at 0% and rises steeply at high usage.",
            "**Enquiries:** risk jumps after 3 in six months.",
            "**Debt burden** hurts the self-employed far more.",
            "Each pattern was **confirmed by a statistical test** before entering the model.",
        ],
        image_share=0.62,
    )

    deck.image(
        "A weak correlation does not mean a weak predictor",
        figs / "fig02_correlation_vs_mi.png",
        bullets=[
            "Utilisation barely correlates with default, yet carries real information.",
            "Its U-shape cancels out in a simple correlation.",
            "A 'drop low-correlation variables' rule would have thrown it away.",
        ],
        image_share=0.62,
    )

    ladder = pd.DataFrame({
        "Model": ["Current scorecard", "Full scorecard (all variables)", "Improved scorecard (curves + interaction)", "ML model (gradient boosting)"],
        "Accuracy on new customers (AUC)": [f"{auc[m]:.3f}" for m in (m0, m1, m2, m3)],
        "Annual value": [lakh(key.loc[m, "value ₹ lakh/yr"]) for m in (m0, m1, m2, m3)],
        "Explainable?": ["Yes", "Yes", "Yes", "Needs extra tooling"],
    })
    deck.table(
        "The improved scorecard is the most accurate model on new customers",
        ladder,
        takeaway=f"Improved vs current scorecard: about {lakh(v20['value_gain_lakh_per_year'])} a year "
                 f"(likely {lakh(v20['ci_low'])} to {lakh(v20['ci_high'])}).",
        col_widths=[2.4, 1.6, 1.3, 1.5],
        highlight_rows=[2],
        font_size=15,
    )

    tests = pd.DataFrame({
        "Question": ["Improved vs current scorecard: better?", "ML vs improved scorecard: better?",
                     "ML vs improved scorecard: different decisions?", "ML vs improved scorecard: worth its cost?"],
        "Answer": [f"Yes: AUC +{d20['auc_diff']:.3f}, not chance", f"No: AUC −{abs(d32['auc_diff']):.3f} (ML slightly worse)",
                   "No meaningful difference at our approval cut-off",
                   f"Unclear: +{lakh(v32['value_gain_lakh_per_year'])}/yr vs ₹{ML_COST} lakh cost; "
                   f"{v32['P(gain > ML cost)']:.0%} chance it pays"],
    })
    deck.table(
        "Four tests, one consistent answer: the ML model has not earned its place",
        tests,
        takeaway="The ML model finds the same risk signals as the improved scorecard. It does not find new ones.",
        col_widths=[2.2, 3.0],
        font_size=15,
    )

    deck.image(
        "Each step's value, with its uncertainty",
        figs / "fig07_value_gain.png",
        takeaway="The scorecard upgrade very likely pays (about 97% probability). The ML step is as likely to fall short of its cost as to exceed it.",
    )

    deck.image(
        "When ML IS worth it: a simulation of four different worlds",
        figs / "fig08_scenario_lab.png",
        bullets=[
            "**Simple patterns:** ML is worse.",
            "**Complex, tangled patterns:** ML wins clearly.",
            "**No signal:** no model helps.",
            "**Little data:** simple models win.",
            "Our data looks like a mix of the first two, so an improved scorecard is enough today.",
        ],
        image_share=0.6,
    )

    deck.bullets(
        "A standing test for any future ML proposal",
        [
            "**No leakage:** every field must exist at decision time.",
            "**Tested on later months**, not a random sample of the same period.",
            "**Compared with the best scorecard**, not the old one.",
            "**Gain confirmed by valid statistical tests** (corrected for repeated testing).",
            "**Value gain clearly above running cost**, including its uncertainty.",
            "**Explainable enough** for decline reasons and Model Risk approval.",
        ],
        takeaway="Adopt this as model-governance policy, so future ML decisions are made on evidence, not on headlines.",
    )

    deck.bullets(
        "Recommendations",
        [
            "**Reject the ML proposal as submitted.** Its headline result depends on a post-event field.",
            "**Deploy the improved scorecard** (≈ ₹6 lakh one-off, within existing systems).",
            "**Run the ML model as a silent challenger**, scored in parallel and compared monthly.",
            "**Review in 12 months** with more data. The ML model's accuracy is still rising with data size.",
            "**Fix data lineage:** flag post-decision fields in the data warehouse so they cannot leak again.",
        ],
        takeaway="Decision for the Committee: approve the scorecard upgrade and the challenger set-up; decline the ML switch for now.",
    )

    deck.two_columns(
        "Limitations and next steps",
        "Limitations",
        [
            "Outcomes are known only for approved customers.",
            "Loss and profit per customer are averages.",
            "One 6-month test window (~10,000 applications).",
            "Real data may hold richer patterns than this study.",
        ],
        "Next steps",
        [
            "Validate the improved scorecard's decline reasons with Credit Policy.",
            "Fairness testing across customer groups.",
            "Champion–challenger reporting from next month.",
            "Test new data sources (e.g., bank statements), where ML often helps more.",
        ],
    )

    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
