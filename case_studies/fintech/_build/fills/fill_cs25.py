R = {}
R["«EXEC»"] = """*(Synthetic evaluation records for a copilot like ICICI Lombard's; the vendors disclosed only "2×" and ">50%". Written after the analysis.)*

- **The question:** does the AI claims copilot deliver the reported "2× productivity" without making claim decisions worse?
- **Speed: yes, close to the claim.** In a randomised test of 6,000 claims, AI-assisted adjudication took a median **41.8 minutes vs 75.1** (time ratio **0.56**, CI 0.55–0.57; **44% less time**, **1.8× more claims per adjudicator-day**). The saving is the same on simple and complex claims. This is slightly short of the documented "over 50%" and "2×", but the same order.
- **Quality: no sign of harm, but the proof is thin.** Decision accuracy vs the true outcome was **84.7% (AI) vs 84.5% (manual)**, non-inferior within 2 pp (CI −1.7 to +2.0). Disputes are unchanged (7.1% vs 7.4%). However, on the realistic **10% gold-audited sample** (546 claims) the interval is ±6 pp, so *non-inferiority cannot be shown* with an audit that small. Proving a 2 pp margin needs ≈ 4,000 audited claims per arm.
- **The main risk is automation bias:** the summary is wrong in **8.7%** of AI-assisted claims (46% of them complex), and when it is wrong adjudicators are right only **74%** of the time vs **86%** when it is right (−11.7 pp, p ≈ 3e-6). That costs ≈ 30 extra wrong decisions in this study, offset by gains elsewhere.
- **Extraction accuracy is good but not enough to skip checking:**
  - Fields are extracted correctly **92%** of the time; only **57% of claims** have all 8 fields right.
  - Handwritten documents have **2.7×** and scans **7.7×** the error odds of clean print.
  - The risk-flag ("pre-existing") field and procedure code are weakest (84% and 89%).
- **The model knows when it is unsure** (confidence AUC 0.92): flagging the 21% least-confident fields for "verify" catches **84% of errors** and leaves 1.6% of unflagged fields wrong.
- **The guideline check** finds 74% of treatment deviations (specificity 93%); **28% of its flags are false alarms**.
- **₹ impact (2 lakh claims/month):** ≈ **125,000 adjudicator-hours a month** freed (≈ 840 FTE) and a net saving of ≈ **₹10.6 crore/month** after copilot costs. Decision-error cost is unchanged.
- **I recommend:**
  - Roll out with human decision-making, with a "verify" flag on low-confidence fields.
  - Force source-page links for every summary fact.
  - Add a 2-click "I checked the source" step for the guideline flag and for handwritten files.
  - Audit ≥ 1,000 gold-labelled claims a quarter to keep the quality claim honest."""
R["«O5»"] = """we removed **60 duplicate rows** and dropped **41 records with handling time 0** (the timer was never stopped, which would make the copilot look impossibly fast). Clean: **5,960 claims**, of which **546 are gold-audited**. Randomisation looks sound but not perfect: the arms are 51.3% / 48.7% (SRM p = 0.036, borderline at 6,000 claims) and complex claims are 25.9% (manual) vs 28.4% (AI). We therefore **adjust for pages, ICU and claim value** in the models, as a careful analyst would."""
R["«O61»"] = """**left:** the AI-assisted distribution of handling time sits clearly to the left of the manual one, with the same shape: a uniform shift, not a few lucky claims. **Right:** extraction accuracy depends heavily on document quality: clean print is mostly 90%+ correct, scans lose 10–20 points on the hardest fields, and handwriting drops some fields (pre-existing flag, procedure code, room rent) into the 60–80% range. The "pre-existing" flag is hardest everywhere. It is also the field that most affects claim outcomes."""
R["«O71»"] = """
- **Overall field accuracy is 92.1%**, from **84.1% for the pre-existing flag** (CI 82.9–85.2%) and **88.7% for procedure code**, to **95.7–96.0% for dates**.
- **Document quality is the driver:** odds of an error are **7.7×** higher on scans and **2.7×** higher on handwriting than on clean print (LR χ² = 1,345, p ≈ 0), and +15% for every 10 extra pages. (The scan odds exceed the handwriting odds, because our simulation's baseline error rates differ by field; the *rates* in the heat-map are the cleaner picture.)
- **Only 56.9% of claims (CI 55.3–58.4%) have all eight fields right.**
- **(f) Business meaning:** the copilot cannot be treated as a data-entry system; it is a first draft that an adjudicator must be able to verify fast."""
R["«O72»"] = """the copilot's confidence separates right from wrong extractions well (**AUC 0.92**). Choosing **"verify" if confidence < 0.7** flags **21%** of fields and catches **84%** of all errors, leaving **1.6%** of unflagged fields wrong (vs 7.9% with no flag). A stricter 0.8 cut flags 40% and catches 94%. **Business meaning:** a confidence-based "please verify" highlight makes the human check efficient. It points effort where the errors are, instead of asking adjudicators to re-read everything."""
R["«O73»"] = """
- **AI-assisted claims take a median 41.8 minutes vs 75.1:** a ratio of **0.56** (bootstrap CI 0.54–0.57; Mann–Whitney p ≈ 0).
- **The mixed model agrees:** time ratio **0.560** (CI 0.550–0.571), **44% saved**, with adjudicator-to-adjudicator variation of ≈ 23% (log SD).
- **Simple vs complex:** ratio 0.564 vs 0.551 (interaction p = 0.32): the same proportional saving, so complex (longer) claims save more *minutes*.
- **Productivity:** 5.3 → 9.6 claims per adjudicator-day = **1.8×**, slightly under the documented "2×" and 44% saving vs the documented "over 50%".
- **(f) Business meaning:** the productivity claim is credible, and is measured in a proper randomised test, not before/after."""
R["«O74»"] = """
- **Against the senior-panel sample** (546 claims), accuracy is 84.3% (AI) vs 83.4% (manual): +0.9 pp with a CI of **−5.2 to +7.2 pp**. That does **not** show non-inferiority at 2 pp: *not enough audited claims*, not evidence of harm.
- **Against the hidden truth on all 5,960 claims** (possible only in simulation): 84.7% vs 84.5%, **+0.17 pp (CI −1.67 to +2.00)**, which does meet the 2 pp margin.
- **By complexity:** simple claims 87.0% → 87.6%; complex claims 77.4% → 77.4%. Disputes 7.4% → 7.1%. No difference is significant (all Holm p = 1).
- **(f) Business meaning:** nothing suggests the copilot degrades decisions, but with a 10% audit a regulator could not be shown *proof*. The audit sample must grow for that claim."""
R["«O75»"] = """in the AI arm, the summary contained an error in **8.7%** of claims (265), and **46% of those were complex**. When it was wrong, adjudicators decided correctly only **74.0%** of the time, vs **85.7%** when it was right: **−11.7 pp (CI −17.5 to −6.6; Fisher p ≈ 3e-6)**. Manual adjudicators averaged 84.5%. So a wrong summary pulls adjudicators well below their unaided accuracy: the classic automation-bias pattern. This costs about **31 extra wrong decisions** in the study, roughly offset by the AI arm's gains elsewhere. **Business meaning:** the copilot's net accuracy is flat only because its benefits happen to cancel its bias costs. Reducing summary errors on complex claims would convert that into a real gain."""
R["«O76»"] = """at the default flag the guideline check has **sensitivity 74.3%** (CI 69–79%), **specificity 93.2%**, precision 72.1% and negative predictive value 93.9% (deviation prevalence 19.2%). So **28% of flags are false alarms**, a workload for adjudicators. Raising the confidence cut-off to 0.5 gives 53% precision and 73% sensitivity, and 0.7 gives 70% precision but only 43% sensitivity. Confidence AUC is 0.83. **Business meaning:** this check is an assistant, not a decider: it should *prompt* a closer look, never auto-reject or auto-approve."""
R["«O77»"] = """
- **Speed claims need little data:** detecting a 20% time saving needs only **≈ 70 claims per arm**; a 10% saving, ≈ 315.
- **Quality claims need a lot:** proving non-inferiority within 2 pp needs **≈ 4,000 claims per arm** (3 pp ≈ 1,800; 5 pp ≈ 640) if true accuracy is ~85%.
- **Business meaning:** speed can be certified in weeks. Quality, which regulators care about most, needs either a much bigger gold-labelled audit or a looser margin agreed in advance."""
R["«O9»"] = """per **2 lakh claims a month** (adjudicators ₹900/hour; a wrong decision costs ₹6,000; copilot ₹45 per claim):
- **Hours:** 281,600 → 156,100 a month: **≈ 125,500 hours freed** (≈ 840 full-time adjudicators).
- **Cost:** manual ≈ **₹43.9 crore/month** (adjudicators ₹25.4 crore + wrong decisions ₹18.6 crore); AI-assisted ≈ **₹33.3 crore/month** (adjudicators ₹14.1 crore + wrong decisions ₹18.4 crore + copilot ₹0.9 crore). **Net saving ≈ ₹10.6 crore/month.**
- **Reading:** almost all the value is **adjudicator time**. The cost of wrong decisions is unchanged, and it is the largest single line, so improving *decision quality* (fewer wrong summaries, better guideline checks) is the next lever."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** extraction errors depend strongly on document quality.
- **H2 ✅:** time ratio 0.56 (44% saved).
- **H3:** non-inferiority holds on the full simulated truth (+0.17 pp) but **cannot be shown on a 10% audit** (CI ±6 pp).
- **H4 ✅ (a real risk):** a wrong summary lowers adjudicator accuracy by 11.7 pp.

**I recommend:**
1. **Roll out as decision support** with adjudicators remaining the decision-makers: ≈ 44% faster, ≈ ₹10 crore/month saving.
2. **Show a "verify" highlight for low-confidence fields** (< 0.7: 21% of fields, 84% of errors) and **link every summary fact to its source page**.
3. **Fight automation bias:** require an explicit "source checked" tick for handwritten/scanned files, complex claims and guideline flags. Measure adjudicator accuracy when summaries are wrong in a regular audit.
4. **Treat the guideline check as a prompt,** not a decision (28% false alarms).
5. **Audit properly:** ≥ 1,000 gold-labelled claims a quarter (more to prove a 2 pp non-inferiority margin), and re-run the extraction audit after every OCR/model/prompt change.

**KPIs:** median handling time and claims per adjudicator-day; decision accuracy vs gold; dispute rate; field accuracy by document quality; share of errors caught by the verify flag; accuracy when the summary is wrong; guideline-flag precision."""
