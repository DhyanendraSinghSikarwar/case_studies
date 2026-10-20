"""Build the stakeholder deck for Case Study 04 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/04_checkout_ab_test/src/build_presentation.py
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
    res = pd.read_csv(tables / "key_results.csv", index_col=0)
    plan = pd.read_csv(tables / "test_duration_plan.csv")
    prim = pd.read_csv(tables / "primary_metric_v5.csv", index_col=0)
    srm = pd.read_csv(tables / "srm_diagnosis.csv", index_col=0)

    n_arm = res.loc["Planned users per arm (80% power, 1 pp MDE)", "estimate"]
    peek = res.loc["False-positive rate with daily peeking", "estimate"]
    lift = res.loc["Primary lift, v5+ (pp)"]
    rel = res.loc["Relative lift, v5+"]
    guard = res.loc["Guardrail: payment-error difference, v5+ (pp)"]
    d3 = res.loc["Day-3 cumulative lift (pp)"]
    rev = res.loc["Annual net revenue from v5+ rollout (₹ lakh)"]
    missing = int(round(res.loc["Missing pre-v5 treatment users", "estimate"], -1))
    pw7 = plan.loc[plan["days"] == 7, "power_for_1pp_lift"].iloc[0]
    rate_t = prim.loc["treatment", "events"] / prim.loc["treatment", "users"]
    rate_c = prim.loc["control", "events"] / prim.loc["control", "users"]
    pre = srm.loc["pre-v5"]

    deck = Deck("Case 04 · Checkout A/B test: design and read-out · synthetic data")

    deck.title_slide(
        "One-Tap Checkout: Test Design and Results",
        "Ship / no-ship read-out for Product leadership · Payments Data Science",
        "14-day randomised test on 10% of app traffic (~66,000 users). Synthetic data created for training. "
        "Not actual customer data.",
    )

    deck.bullets(
        "Summary: one-tap works for most users, crashes old Android apps, and may fall short of the 1-point bar",
        [
            f"**For v5+ app users** (91% of users): checkout completion rose from **{rate_c:.1%} to {rate_t:.1%}**, "
            f"a gain of **+{lift['estimate']:.1f} point** (likely +{lift['ci_low']:.1f} to +{lift['ci_high']:.1f}).",
            "**It is real** (not a fluke), and payment errors did not increase.",
            "**But we cannot confirm it reaches leadership's 1-point bar**: the likely range straddles it.",
            f"**Old Android app (pre-v5): one-tap crashes** for about a third of users. About {missing:,} users silently dropped out of the test.",
            f"**Stopping on day 3 would have overstated the gain** (+{d3['estimate']:.1f} vs +{lift['estimate']:.1f} points).",
        ],
        takeaway="Recommendation: ship to v5+ with a 5% holdout; block pre-v5 until the crash is fixed.",
        size=18,
    )

    deck.two_columns(
        "What we were asked, and when",
        "Before the test",
        [
            "How long must we run to detect a 1-point gain?",
            "Can we do it in a week?",
        ],
        "During and after",
        [
            "Day 3: '+1.8 points, p = 0.03. Can we stop and ship?'",
            "Day 14: the dashboard flags a 'sample ratio mismatch'. Can we trust the test?",
            "Did one-tap work? Is it at least 1 point? Is it safe for everyone?",
        ],
    )

    deck.image(
        "Two full weeks were needed; one week would have missed a real 1-point gain half the time",
        figs / "fig01_power_curves.png",
        bullets=[
            f"Needed: about **{round(n_arm, -3):,.0f} users per group**, i.e. 14 days at 10% of traffic.",
            f"After one week: only a **{pw7:.0%}** chance of detecting a real 1-point gain.",
            "Always run **whole weeks**: weekends behave differently.",
        ],
        image_share=0.62,
    )

    deck.image(
        f"Checking daily and stopping at the first 'significant' result gives false wins {peek:.0%} of the time",
        figs / "fig02_peeking_simulation.png",
        takeaway="Rule: decide the test length in advance and judge once at the end. Day-3 'significance' is not evidence.",
    )

    deck.image(
        "The test was partly broken: the new screen crashes on the old Android app",
        figs / "fig03_srm_diagnosis.png",
        bullets=[
            f"Expected a 50/50 split; **pre-v5 had only {pre['treatment_share']:.0%} in the new design**.",
            f"About **{missing:,} pre-v5 users** crashed before being counted.",
            "Those who got through saw **3× more payment errors**.",
            "Newer app versions and iOS were unaffected and split evenly.",
        ],
        image_share=0.6,
        takeaway="One-tap must not reach pre-v5 users until the crash is fixed. Add automatic split-ratio alerts.",
    )

    deck.kpis(
        "Result for v5+ users: a real gain of about one point, with no harm to payments",
        [
            (f"+{lift['estimate']:.2f} pts", "checkout completion", f"Likely range +{lift['ci_low']:.1f} to +{lift['ci_high']:.1f} points."),
            (f"+{rel['estimate']:.1%}", "relative gain", f"From {rate_c:.1%} to {rate_t:.1%}."),
            ("~1 in 200", "chance it's a fluke", "If one-tap did nothing, a gain this big would rarely appear."),
            (f"{'−' if guard['estimate'] < 0 else '+'}{abs(guard['estimate']):.2f} pts", "payment errors", "No increase; any rise larger than ~0.13 points is ruled out."),
        ],
    )

    deck.image(
        "Real, yes. At least one point? We can't tell yet",
        figs / "fig04_lift_vs_thresholds.png",
        takeaway="The likely range clears zero but straddles the 1-point bar, so the bar is neither met nor missed with confidence.",
    )

    deck.image(
        "Early results overstated the gain: the effect settled as the novelty wore off",
        figs / "fig05_lift_over_time.png",
        takeaway=f"Day 3 showed +{d3['estimate']:.1f} points; the full test shows +{lift['estimate']:.1f}. "
                 "Business cases should use full-test numbers.",
    )

    deck.kpis(
        "What a one-point gain is worth",
        [
            (f"₹{rev['estimate']:.0f} lakh", "per year (estimate)", "Net revenue from extra completed payments, v5+ users, full traffic."),
            (f"₹{rev['ci_low']:.0f}–{rev['ci_high']:.0f} lakh", "likely range", "Reflects the uncertainty in the lift."),
            ("No", "rise in payment errors", "No guardrail harm for v5+ users."),
        ],
        takeaway="A modest but positive return with little downside, provided pre-v5 users are excluded.",
    )

    deck.two_columns(
        "Decision options for leadership",
        "Option A (recommended): ship to v5+ now",
        [
            "Roll out to v5+ users, keeping **5% on the old flow** for 4–6 weeks.",
            "Confirms the settled gain with no further delay.",
            "Accepts that the gain may be somewhat under 1 point.",
        ],
        "Option B: extend the test 2 weeks",
        [
            "Roughly halves the uncertainty around the 1-point bar.",
            "Delays any benefit by 2+ weeks.",
            "Pre-v5 must be fixed and excluded either way.",
        ],
        takeaway="Either way: block pre-v5, fix the crash, re-test it, and add split-ratio alerts.",
    )

    deck.bullets(
        "Process changes we recommend for every future test",
        [
            "**Pre-register** the metric, the minimum gain that matters, and the test length.",
            "**Run whole weeks**, sized by a power calculation, not by impatience.",
            "**No ship decisions on interim p-values.** Use sequential rules if early stopping is needed.",
            "**Check the split ratio first**: a mismatch means something is broken.",
            "**Keep a holdout after launch** to measure the long-run effect.",
        ],
    )

    deck.two_columns(
        "Limitations and next steps",
        "Limitations",
        [
            "Two weeks may not show the long-run effect.",
            "Result applies to v5+ users only.",
            "First checkout only; repeat use not measured.",
            "Revenue uses Finance's ₹10 per payment.",
        ],
        "Next steps",
        [
            "Fix pre-v5 crash; re-test that segment.",
            "Holdout read-outs at 4 and 8 weeks.",
            "Measure repeat bill payments.",
            "Use pre-test history (CUPED) to shorten future tests.",
        ],
    )

    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
