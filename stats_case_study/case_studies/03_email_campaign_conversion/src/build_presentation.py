"""Build the stakeholder deck for Case Study 03 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/03_email_campaign_conversion/src/build_presentation.py
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
    grp = pd.read_csv(tables / "conversion_by_group.csv", index_col=0)
    res = pd.read_csv(tables / "key_results.csv", index_col=0)
    econ = pd.read_csv(tables / "campaign_economics.csv", index_col=0)["value"]
    pilot = pd.read_csv(tables / "pilot_results.csv", index_col=0)["value"]

    # Rates from integer counts (avoids rounding artefacts in the saved CSV).
    p_e = grp.loc["email", "conversions"] / grp.loc["email", "customers"]
    p_h = grp.loc["holdout", "conversions"] / grp.loc["holdout", "customers"]
    lift = res.loc["Email campaign: absolute lift (pp)"]
    rel = res.loc["Email campaign: relative lift"]
    loans = res.loc["Email campaign: incremental loans"]
    net = res.loc["Email campaign: net value (₹ lakh)"]
    cace = res.loc["Effect among openers, CACE (pp)", "estimate"]
    naive = res.loc["Naive openers vs non-openers gap (pp)", "estimate"]
    emails_per_loan = 100 / lift["estimate"]

    deck = Deck("Case 03 · Did the email campaign increase conversions? · synthetic data")

    deck.title_slide(
        "Personal-Loan Email Campaign: What Did It Really Deliver?",
        "Campaign read-out for Marketing leadership · Marketing Analytics",
        "80,000 eligible customers, 15% randomly held out; plus a 360-customer RM-call pilot. "
        "Synthetic data created for training. Not actual customer data.",
    )

    deck.bullets(
        "Summary: the email works and pays, but the effect is about +23%, not 3×",
        [
            f"**The email increased conversion:** {p_e:.2%} vs {p_h:.2%} for customers who got no email, a gain of "
            f"**{lift['estimate']:.2f} points (+{rel['estimate']:.0%})**.",
            f"That is about **1 extra loan per {emails_per_loan:.0f} emails**, roughly **{loans['estimate']:.0f} extra loans** in total.",
            f"**It pays:** about **₹{net['estimate']:.0f} lakh** net (likely ₹{net['ci_low']:.0f}–{net['ci_high']:.0f} lakh). "
            "Emails are cheap, so a small lift is enough.",
            "**The '3× for openers' figure is misleading.** People who open emails are engaged customers who borrow more anyway.",
            "**The RM-call pilot is too small to judge**: promising, but not proven.",
        ],
        takeaway="Recommendation: repeat the campaign with a holdout every time; do not double the budget on the '3×' figure.",
        size=18,
    )

    deck.two_columns(
        "Two questions from Marketing",
        "What Marketing asked",
        [
            "Did the email campaign increase personal-loan take-up?",
            "Openers converted ~3× more: should we double the email budget?",
            "Should we scale the relationship-manager (RM) call pilot?",
        ],
        "Why we could answer properly",
        [
            "15% of eligible customers were **randomly** held back from the email.",
            "Random selection makes the two groups alike in every way except the email.",
            "So the difference between them measures what the email **caused**.",
        ],
        takeaway="The holdout group is the most valuable part of the campaign design: without it, we could not measure the effect.",
    )

    deck.image(
        "Comparing openers with non-openers exaggerates the effect; the random holdout gives the true picture",
        figs / "fig01_wrong_vs_right_comparison.png",
        bullets=[
            "**Left:** openers vs non-openers, about 3×. But customers chose whether to open.",
            f"**Right:** email vs random holdout: **{p_e:.2%} vs {p_h:.2%}**.",
            "Only the right-hand comparison is fair.",
        ],
        image_share=0.64,
    )

    deck.image(
        "Why openers look so good: engaged customers borrow more even without any email",
        figs / "fig02_engagement_confounding.png",
        bullets=[
            "In the **holdout** (no email), digitally active customers converted ~1.5× more than inactive ones.",
            "Engaged customers both **open emails** and **take loans anyway**.",
            f"The email's real effect on openers: about **{cace:.1f} points**, not the {naive:.1f}-point gap the dashboard shows.",
        ],
        image_share=0.6,
    )

    deck.kpis(
        "The real effect: modest, clearly positive, and causal",
        [
            (f"+{lift['estimate']:.2f} pts", "conversion lift", f"Likely range +{lift['ci_low']:.2f} to +{lift['ci_high']:.2f} points."),
            (f"+{rel['estimate']:.0%}", "relative lift", f"Likely range +{rel['ci_low']:.0%} to +{rel['ci_high']:.0%}."),
            (f"~{loans['estimate']:.0f}", "extra loans", f"Likely {loans['ci_low']:.0f}–{loans['ci_high']:.0f}, caused by the email."),
            ("< 1 in 250", "chance of a fluke", "If the email did nothing, a gap this big would almost never appear."),
        ],
        takeaway="Report this as '+0.4 points (+23%)'. Relative lifts sound bigger than they are when the base rate is ~2%.",
    )

    deck.image(
        "Even the most pessimistic estimate clears break-even many times over",
        figs / "fig04_lift_vs_breakeven.png",
        takeaway=f"Break-even needs only +{econ['break-even lift (pp)']:.3f} points; the worst plausible lift is about "
                 f"{lift['ci_low'] / econ['break-even lift (pp)']:.0f}× that.",
    )

    econ_tbl = pd.DataFrame({
        "Item": ["Emails sent", "Campaign cost", "Extra loans caused by the email", "Value per extra loan", "Net value"],
        "Estimate": [f"{econ['emails sent']:,.0f}", f"₹{econ['campaign cost (₹ lakh)']:.1f} lakh", f"~{loans['estimate']:.0f}",
                     "₹9,000 (Finance)", f"₹{net['estimate']:.0f} lakh"],
        "Likely range": ["–", "–", f"{loans['ci_low']:.0f} – {loans['ci_high']:.0f}", "–",
                         f"₹{net['ci_low']:.0f} – ₹{net['ci_high']:.0f} lakh"],
    })
    deck.table(
        f"The campaign returned about {econ['ROI multiple (estimate)']:.0f}× its cost",
        econ_tbl,
        takeaway="Cheap channel, positive effect, robust profit. The case for repeating the email is strong.",
        col_widths=[2, 1.4, 1.4],
        font_size=16,
        highlight_rows=[4],
    )

    deck.image(
        "RM-call pilot: an encouraging signal, but far too small to be sure",
        figs / "fig05_rm_pilot.png",
        bullets=[
            f"Called: **{pilot['conv_rm_call']:.1%}** converted; not called: **{pilot['conv_no_call']:.1%}**.",
            "That is **6 vs 1 customers**: too few to separate a real effect from luck.",
            f"Plausible effect: anywhere from about **−{abs(pilot['diff_ci_low_pp']):.1f} to +{pilot['diff_ci_high_pp']:.1f} points**.",
            "'Not proven' ≠ 'doesn't work'. It means 'test properly'.",
        ],
        image_share=0.55,
        takeaway="Run a larger, properly sized pilot before committing RM time.",
    )

    deck.two_columns(
        "What we can and cannot say",
        "We can say",
        [
            "The email **caused** a modest rise in loan take-up.",
            "The campaign was profitable, even in the pessimistic case.",
            "The 'openers 3×' comparison overstates the effect.",
        ],
        "We cannot say yet",
        [
            "Whether RM calls work: the pilot is too small.",
            "Whether the lift holds for repeated campaigns (fatigue).",
            "How much is truly new business vs loans brought forward a few weeks.",
        ],
    )

    deck.bullets(
        "Recommendations",
        [
            "**Repeat the email campaign**, always with a random holdout, so every send is measured.",
            "**Do not double the budget** on the basis of the openers comparison. Test frequency and targeting first.",
            "**Fix the dashboard:** report email vs holdout with a likely range, not openers vs non-openers.",
            "**RM calls:** run a larger pilot (sized in advance) before scaling.",
            "**Measure at 60–90 days** to check how much of the lift is pulled forward.",
        ],
        takeaway="Decision for Marketing: approve the next send with a holdout; approve a properly sized RM pilot.",
    )

    deck.two_columns(
        "Limitations and next steps",
        "Limitations",
        [
            "One campaign, 30-day window.",
            "Loan value and costs are Finance estimates.",
            "Engagement finding not planned in advance.",
            "A repeat could land anywhere from ~+0.15 to ~+0.7 points.",
        ],
        "Next steps",
        [
            "Next send: same design, with holdout.",
            "Targeting test: engaged vs non-engaged customers.",
            "RM pilot sized for a conclusive answer.",
            "60/90-day follow-up on conversions.",
        ],
    )

    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
