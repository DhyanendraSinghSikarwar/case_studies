"""Build the stakeholder deck for Case Study 01 from the notebook's saved outputs.

Run the notebook first (it writes outputs/figures and outputs/tables), then:
    python case_studies/01_loan_portfolio_health_check/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402

BOOK_SIZE = 60_000
PLAN = 300_000
APPETITE = 0.04


def lakh(x: float, d: int = 2) -> str:
    return f"₹{x / 1e5:.{d}f} lakh"


def _rarity(p: float) -> str:
    """Plain-language bound for a small p-value: 0.0005 -> '1,000' (i.e. 'less than 1 time in 1,000')."""
    for k in (10_000, 1_000, 100, 20):
        if p < 1 / k:
            return f"{k:,}"
    return "20"


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    res = pd.read_csv(tables / "key_results.csv", index_col=0)
    seg = pd.read_csv(tables / "segment_summary.csv", index_col=[0, 1])
    conc = pd.read_csv(tables / "exposure_concentration.csv", index_col=0)
    desc = pd.read_csv(tables / "descriptive_statistics.csv", index_col=0)
    log = pd.read_csv(tables / "data_cleaning_log.csv")

    mean_r, med_r = res.loc["Mean ticket size (₹)"], res.loc["Median ticket size (₹)"]
    dpd, exc = res.loc["12m 90+ DPD rate"], res.loc["DTI policy-exception rate"]
    excess = mean_r["estimate"] - PLAN
    extra_cr = BOOK_SIZE * excess / 1e7
    extra_cr_lo = BOOK_SIZE * (mean_r["ci_low"] - PLAN) / 1e7
    extra_cr_hi = BOOK_SIZE * (mean_r["ci_high"] - PLAN) / 1e7
    dsa = seg.loc[("channel", "DSA")]
    others = seg.loc[[("channel", "Branch"), ("channel", "Digital")]]
    # Sum the *rounded* band shares so headline numbers match the rounded table on the slide.
    big = ["₹5–10L", "₹10–15L"]
    big_share_loans = (conc.loc[big, "share_of_loans"] * 100).round().sum() / 100
    big_share_exp = (conc.loc[big, "share_of_exposure"] * 100).round().sum() / 100
    n_errors = int(log.loc[log["decision"].str.startswith(("Corrected", "Dropped", "Set to missing")), "rows"].sum())
    n_no_hit = int(log.loc[log["column"].eq("credit_score"), "rows"].sum())
    mix = pd.read_csv(tables / "sample_vs_book_mix.csv")
    max_mix_gap = mix["difference_pp"].abs().max()

    deck = Deck("Case 01 · Personal-loan portfolio health check · synthetic data")

    deck.title_slide(
        "Personal-Loan Book Health Check",
        "Board Risk Committee pre-read · Retail Risk Analytics",
        "Based on an audited random sample of 2,500 loans from a book of 60,000. "
        "Synthetic data created for training. Not actual customer data.",
    )

    deck.bullets(
        "Summary: the book is very likely above risk appetite, and loans are larger than planned",
        [
            f"**Delinquency is above appetite.** About **{dpd['estimate']:.1%}** of loans went 90+ days past due within "
            f"12 months, against a **4%** appetite (likely range {dpd['ci_low']:.1%}–{dpd['ci_high']:.1%}).",
            f"**Loans are ~{excess / PLAN:.0%} larger than the plan assumed.** Average ticket {lakh(mean_r['estimate'])} vs "
            f"₹3.00 lakh, about **₹{extra_cr:,.0f} crore** more exposure across the book.",
            f"**The 'average' loan is not the typical loan.** Half of loans are below {lakh(med_r['estimate'], 1)}. "
            f"Large loans (≥ ₹5 lakh) are {big_share_loans:.0%} of loans but {big_share_exp:.0%} of the money.",
            f"**DTI policy exceptions are under control** at {exc['estimate']:.1%}, well within the 1% limit.",
            "**Next:** a driver analysis before any corrective action. The DSA channel is the first place to look.",
        ],
        takeaway="Recommendation: report an appetite breach to the Board and commission a driver analysis within 6 weeks.",
        size=18,
    )

    deck.two_columns(
        "What the CRO needs to tell the Board",
        "What the Board wants to know",
        [
            "What does a typical personal loan look like?",
            "How concentrated is the money in large loans?",
            "Is the average ticket in line with the ₹3.0 lakh plan?",
            "Is 12-month serious delinquency (90+ DPD) within the 4% appetite?",
            "Are DTI policy exceptions within the 1% limit?",
        ],
        "Why this needed care",
        [
            "A system migration left key fields unreconciled.",
            "Internal Audit re-verified a **random sample** of 2,500 loan files.",
            "Every number is therefore an **estimate**, so we report how precise it is.",
        ],
        takeaway="We answer every question with a number AND a margin of error, so the Board knows how firm each number is.",
    )

    deck.kpis(
        "The audit sample is a fair, clean miniature of the book",
        [
            ("2,500", "loans audited", "Chosen at random from all 60,000 loans, so every loan had an equal chance."),
            ("18 mths", "of disbursals", "Jan-2024 to Jun-2025; every loan observed for at least 12 months."),
            (f"±{max_mix_gap:.1f} pp", "mix vs book", "Channel, region and employment mix of the sample match the book closely."),
            (f"{n_errors}", "data errors fixed", f"Duplicates, decimal-keyed rates, annual-as-monthly incomes, invalid ages. "
                                                f"Plus {n_no_hit} 'no credit history' codes handled correctly."),
        ],
        takeaway="Because the sample is random, results apply to the whole book, within the margins of error shown.",
    )

    deck.bullets(
        "Approach: clean, describe, estimate with margins of error, then test against targets",
        [
            "**1. Clean:** remove duplicates and fix provable errors. Large loans were verified as genuine and kept.",
            "**2. Describe:** typical values, spread and concentration, using the median where averages mislead.",
            "**3. Estimate:** for every key number, a range that is right 95% of the time (a '95% confidence interval').",
            "**4. Test:** could the gap between our number and the target be just the luck of the sample?",
            "**5. Check:** we confirmed by simulation that the method's ranges capture the truth ~95% of the time.",
        ],
        takeaway="Statistics here answers one question: how sure can we be when we only looked at 1 in 24 loans?",
    )

    rate = desc.loc["interest_rate"]
    tenure_mode = 36
    deck.kpis(
        "A typical personal loan: ₹2.5 lakh at about 16% over three years",
        [
            (lakh(med_r["estimate"], 1), "median loan", "Half of loans are smaller, half larger. This is the 'typical' customer."),
            (lakh(mean_r["estimate"], 2), "average loan", "Pulled up by a minority of large loans. Use it for exposure totals."),
            (f"{rate['mean']:.1f}%", "average interest rate", f"Tightly clustered: most loans are within ±{rate['std']:.1f} points."),
            (f"{tenure_mode} months", "most common tenure", "Larger loans tend to take 48–60 months."),
        ],
        takeaway="Design products around the median customer. Plan capital using the average.",
    )

    deck.image(
        "Most loans are small, but a long tail of large loans pulls the average above the typical loan",
        figs / "fig01_loan_amount_distribution.png",
        bullets=[
            f"Half of all loans are below **{lakh(med_r['estimate'], 1)}**.",
            f"The average (**{lakh(mean_r['estimate'])}**) sits above most loans because a few are up to ₹15 lakh.",
            "Spikes at round amounts: customers ask for ₹1, 2, 3 lakh.",
            "Large loans are **genuine**, not data errors, so they stay in.",
        ],
        image_share=0.64,
    )

    conc_tbl = pd.DataFrame({
        "Loan size": conc.index,
        "Share of loans": (conc["share_of_loans"] * 100).round(0).astype(int).astype(str) + "%",
        "Share of money lent": (conc["share_of_exposure"] * 100).round(0).astype(int).astype(str) + "%",
    })
    deck.table(
        f"Loans of ₹5 lakh and above are {big_share_loans:.0%} of loans but {big_share_exp:.0%} of exposure",
        conc_tbl,
        takeaway="Losses will be driven by large loans. Monitor the ≥ ₹5 lakh segment separately, not just book averages.",
        col_widths=[1.2, 1, 1],
        highlight_rows=[4, 5],
    )

    deck.kpis(
        f"Loans are about {excess / PLAN:.0%} larger than the business plan assumed",
        [
            (lakh(mean_r["estimate"]), "average ticket (actual)", f"Likely range {lakh(mean_r['ci_low'])} – {lakh(mean_r['ci_high'])}."),
            ("₹3.00 lakh", "plan assumption", "Used in the capital and provisioning plan."),
            (f"+₹{excess / 1e3:,.0f}k", "per loan", "Too large to be the luck of the sample (less than 1-in-1,000 chance)."),
            (f"≈ ₹{extra_cr:,.0f} cr", "extra exposure", f"Across 60,000 loans; likely ₹{extra_cr_lo:,.0f}–{extra_cr_hi:,.0f} crore."),
        ],
        takeaway="Small per loan, material for the book: re-base the plan's ticket size for capital and provisioning.",
    )

    deck.image(
        f"Serious delinquency is about {dpd['estimate']:.1%}, above the 4% risk appetite",
        figs / "fig05_default_rate_by_segment.png",
        bullets=[
            f"Book estimate **{dpd['estimate']:.1%}**; likely range **{dpd['ci_low']:.1%}–{dpd['ci_high']:.1%}**. "
            "The whole range is above 4%.",
            f"If the book were truly at 4%, an audit result this high would happen less than **1 time in {_rarity(dpd['p_value'])}**.",
            f"DSA-sourced loans: **~{dsa['dpd90_rate']:.0%}**, roughly double Branch and Digital "
            f"({others['dpd90_rate'].min():.1%}–{others['dpd90_rate'].max():.1%}).",
            "Bars show the range of plausible values; smaller segments have wider bars.",
        ],
        takeaway="Treat this as an appetite breach. The DSA gap is a lead to investigate, not yet a proven cause.",
        image_share=0.6,
    )

    verdict = pd.DataFrame({
        "Metric": ["Average ticket size", "Typical (median) ticket", "12-month 90+ DPD rate", "DTI policy exceptions"],
        "Our estimate": [lakh(mean_r["estimate"]), lakh(med_r["estimate"], 1), f"{dpd['estimate']:.1%}", f"{exc['estimate']:.2%}"],
        "Likely range (95%)": [f"{lakh(mean_r['ci_low'])} – {lakh(mean_r['ci_high'])}",
                               f"{lakh(med_r['ci_low'], 1)} – {lakh(med_r['ci_high'], 1)}",
                               f"{dpd['ci_low']:.1%} – {dpd['ci_high']:.1%}",
                               f"{exc['ci_low']:.2%} – {exc['ci_high']:.2%}"],
        "Target": ["₹3.00 lakh (plan)", "–", "≤ 4% (appetite)", "≤ 1% (limit)"],
        "Verdict": ["Above plan (firm)", "–", "Above appetite (firm)", "Within limit (firm)"],
    })
    deck.table(
        "How sure are we? Each conclusion holds across its whole likely range",
        verdict,
        takeaway="'Firm' means the conclusion holds anywhere in the likely range, not only at our single best estimate.",
        col_widths=[1.5, 1.1, 1.6, 1.2, 1.4],
        font_size=15,
    )

    deck.two_columns(
        "What we can and cannot say yet",
        "We can say",
        [
            "The book is very likely above the 4% appetite.",
            "Average ticket is above plan by ~8%.",
            "Exposure is concentrated in large loans.",
            "DTI exceptions are within limit.",
        ],
        "We cannot say yet",
        [
            "**Why** delinquency is high. DSA customers may simply have weaker profiles.",
            "Whether it is **getting worse**: we pooled 18 months of loans.",
            "Anything about loans under 12 months old.",
            "Whether self-employed borrowers are riskier: the gap is within the noise.",
        ],
        takeaway="We know where to look, not yet what to change. Acting on the DSA channel now risks fixing the wrong thing.",
    )

    deck.bullets(
        "Recommendations",
        [
            "**Escalate:** report the 90+ DPD appetite breach to the Board, with its likely range.",
            "**Diagnose before acting:** a 4–6 week driver analysis separating channel, credit score and DTI effects.",
            "**Re-base the plan:** use an average ticket of about ₹3.25 lakh for capital and provisioning.",
            "**Report better:** show median and percentiles alongside averages; attach a margin of error to every "
            "sample-based number.",
            "**Fix the data pipeline:** duplicates, unit errors and 'no-history' codes must be fixed before the next system report.",
        ],
        takeaway="The decision for the Board: acknowledge the breach now; approve the diagnostic work that precedes corrective action.",
    )

    deck.bullets(
        "Limitations: what could change these conclusions",
        [
            "**Sample-based:** book-level numbers are precise; segment numbers (e.g., DSA, ~470 loans) much less so.",
            "**One definition of default** (ever 90+ DPD in 12 months). Other definitions can differ.",
            "**Income** is missing for 4% of loans, mostly self-employed, so income figures are for verified loans only.",
            "**Pooled period:** recent months could be better or worse than the 18-month average.",
            "**Approved loans only:** results describe the book, not all applicants.",
            "**No cause-and-effect conclusions:** differences between segments are associations.",
        ],
    )

    deck.bullets(
        "Next steps",
        [
            "**Weeks 1–2:** formal comparison of channels and customer types (are the gaps real?).",
            "**Weeks 2–4:** vintage view: delinquency by disbursal quarter, to establish the trend.",
            "**Weeks 3–6:** driver model of delinquency (score, DTI, channel, employment, age).",
            "**Next quarter:** a targeted audit of DSA and ≥ ₹5 lakh loans to sharpen segment estimates.",
            "**Ongoing:** monthly delinquency tracking with statistical control limits (react to signal, not noise).",
        ],
        takeaway="Return to the Committee next quarter with drivers identified and options costed.",
    )

    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
