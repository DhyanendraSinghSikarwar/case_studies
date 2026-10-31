**Say this first (1 line):** OCR load is 110,000 pages x 0.8 s = 88,000 core-seconds, which at 50% utilisation over 6 hours needs 9 cores, and if only 85% go straight through, the other 7,500 invoices need 187.5 review hours, so 27 reviewers; the real design question is which fields are trusted without a person.

**Clarifying questions:**
- Which fields matter (invoice number, date, amount, tax identifier, line items) and what does a wrong amount cost? Error cost sets the confidence thresholds.
- Is the 85% straight-through target a goal or a measured rate? It is a goal; the reviewer count depends directly on it.
- What are the layouts and image quality (phone photos, scans, handwriting, Hindi and English mixed)? Quality drives recognition errors.
- Is there a purchase order or vendor master to validate against? Cross-checks catch errors OCR cannot.
- What is the arrival pattern: all at once, or spread through the day? A 6-hour batch window needs all files to have arrived.

**Approach:**
1. Clarify and frame. Goal: turn scans into validated records with 85% going straight through and the rest reviewed quickly. Define "straight through": all required fields above confidence and passing validation, with no human touch.
2. Metrics and guardrails. Field-level accuracy, invoice-level exact match, straight-through rate, review time per invoice, cost per invoice. Guardrail: wrong amount posted automatically (the costly error), and turnaround time.
3. Data and labels. Sample invoices across vendors, languages and quality; have people key the fields once (a gold set), and keep reviewer corrections as ongoing labels. Plan the labelling budget per layout family so rare vendors are covered.
4. Baseline first. Existing OCR plus regular expressions and vendor templates for the top vendors; measure field accuracy on the gold set.
5. Model and trade-offs. OCR (0.8 s a page on one core), then a layout-aware extractor for fields, then validation (totals add up, tax maths, date format, vendor match, duplicate check). Capacity: 88,000 core-seconds, 9 cores at 50% utilisation (see the code), plus the reviewer load. Trade-off: a higher confidence threshold cuts errors but lowers the straight-through rate and raises reviewer count.
6. Evaluation. Offline field accuracy and invoice-level exact match by vendor and language; calibration of confidence scores. Online: shadow mode where people key as usual and the system is compared, then partial automation on low-value invoices.
7. Launch and experiment plan. Start with the top vendors and lower-value invoices, expand by layout family; ramp straight-through share as audits stay clean.
8. Monitoring, retraining and risks. Weekly audit of a random sample of auto-posted invoices (598 clean audits bound the error rate below 0.5% at 95%, see the code), drift alerts on confidence scores and new layouts, retrain on reviewer corrections.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 6, 4, 11, 6, 5, 5.

**Metrics:**
- Pages = invoices x pages per invoice = 50,000 x 2.2 = 110,000; core-seconds = pages x 0.8 = 88,000.
- Cores = ceil(core-seconds / (window seconds x utilisation)) = ceil(88,000 / 10,800) = ceil(8.15) = 9.
- Straight-through rate = invoices posted with no human touch / all invoices.
- Reviewers = ceil(invoices to review x seconds per review / 3,600 / productive hours per person) = ceil(7,500 x 90 / 3,600 / 7) = ceil(26.8) = 27.
- Field accuracy = fields correct / fields; guardrail: auto-posted wrong-amount rate.

**Risks:**
- Silent errors (a misread digit in an amount) in auto-posted invoices; validation rules and audits are the control.
- The 85% target may not hold on poor scans or new vendors; the reviewer count moves by about 1.8 people per point.
- Mixed Hindi and English text and stamps reduce recognition; test per language.
- Peaks: a 6-hour window with uneven arrivals needs more than the average capacity.
- Personal and financial data in documents; ask compliance and legal about retention and access.

**What the interviewer scores:**
- Strong: 110,000 pages, 88,000 core-seconds, 9 cores, 187.5 review hours, 27 people, with the OCR applied to every page.
- Strong: confidence thresholds, validation rules and audit sampling for auto-posted records.
- Strong: sees the trade-off between straight-through rate and reviewer cost.
- Weak: "use a good OCR model", with no validation, no human loop and no capacity maths.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "OCR plus a language model reads the invoices and we are done."
- Strong: "50,000 invoices at 2.2 pages is 110,000 pages, so 88,000 core-seconds. At 50% utilisation over 6 hours, a core gives 10,800 seconds, so 9 cores. If 15% need review, that is 7,500 invoices, 187.5 hours, 27 reviewers. Each point of straight-through rate moves the team by about two people, so I would set the confidence threshold by the cost of a wrong amount, validate totals and vendors, and audit a random sample of auto-posted invoices every week."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if straight-through is only 75%? Reviewers rise to 45; consider better templates for top vendors, a second-pass model for low-confidence fields only, or a longer SLA.
- Could you skip OCR for digital invoices? Yes, if some arrive as text PDFs or structured files; that is a cheap win and cuts the core count.
- How do you set the confidence threshold? From the cost of a wrong auto-posted amount versus the cost of a review, using calibrated scores on the gold set.

**Common mistakes:**
- Computing OCR cores only for the straight-through 85%.
- Ignoring utilisation (running cores at 100%).
- Counting reviewers in people without productive hours.
- Treating the 85% target as a measured rate.
