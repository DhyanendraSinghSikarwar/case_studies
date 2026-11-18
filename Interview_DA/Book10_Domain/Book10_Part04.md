# Book 10 — Domain Knowledge | Part 4: Healthcare & Pharma 🟢🟡🔴

**Target:** 70 questions | **Actual:** 79 questions
**Scope:** hospital operations and KPIs, health insurance claims and revenue cycle, clinical trials, pharma sales analytics, coding standards, and patient-privacy awareness in plain words (no medical advice, no legal advice).

### Q1 ⭐⭐⭐ 🟢 In plain words, how does a multispecialty hospital work, and what is the difference between OPD, IPD, emergency and day-care patients?
**Asked at:** commonly asked (no company-specific report found); hospital vocabulary is named in hospital-MIS and healthcare-analyst prep material (prep sites, unverified).
**What the interviewer is checking:** Whether you can speak the hospital's language, because every table and KPI is split by these patient types.
**Say this in the interview:** "A multispecialty hospital treats many kinds of conditions under one roof. OPD patients visit and go home the same day, IPD patients are admitted to a bed, emergency patients arrive unplanned, and day-care patients are admitted for a procedure but leave within the day."
**Explain simply:**
- **OPD (outpatient department):** consultation, tests or minor procedures with no bed. Think of a walk-in clinic inside the hospital.
- **IPD (inpatient department):** the patient is admitted and given a bed, often overnight or longer. Most beds, nursing hours and revenue per patient sit here.
- **Emergency (ER/casualty):** unplanned, urgent arrivals. Some are treated and sent home, some are admitted into IPD, so emergency is a doorway rather than a separate ward.
- **Day-care:** a planned procedure (for example a minor surgery or dialysis session) with admission and discharge on the same day. It uses a bed or chair for hours, not nights, so it is usually counted separately from inpatient days.
- **How it runs:** departments (cardiology, orthopaedics...) bring in doctors; support services (nursing, lab, radiology, pharmacy, billing) serve all of them.
- **HR parallel:** like separating full-time, part-time, walk-in and shift-based workers; you would never mix them in one headcount.
**Likely follow-ups:** 1) *Why keep them separate in data?* Their cost, length of stay and revenue behave very differently. 2) *Is an emergency patient IPD?* Only if admitted; track the "emergency-to-admission" flag.
**Common mistakes:** Mixing day-care into inpatient days; treating all visits as "patients" (a visit is not a person); forgetting emergency can convert to IPD.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a payer, a provider and a patient in healthcare, and how do money and data move between them?
**Asked at:** commonly asked (no company-specific report found); payer/provider data appears in US-healthcare analyst job postings (unverified).
**What the interviewer is checking:** Whether you understand the three-party structure behind claims data.
**Say this in the interview:** "The patient receives care, the provider (hospital or doctor) delivers it, and the payer (insurer, government scheme or employer) pays for it. Money flows from payer to provider and data flows as bills and claims."
**Explain simply:**
- **Patient:** the person treated. They may pay a share directly (a *co-pay* is a fixed share, a *deductible* is the first amount they pay before insurance helps).
- **Provider:** hospital, clinic, lab or doctor who bills for services.
- **Payer:** the party that funds care: a private insurer, a government scheme, a company paying for staff cover, or the patient themselves.
- **Data trail:** registration and clinical record at the provider, then a bill with diagnosis and procedure codes, then a claim to the payer, then an approval, partial approval or denial, then payment.
- **Why analysts care:** the provider sees clinical detail; the payer sees many hospitals' claims but little clinical detail. Your questions depend on whose data you hold.
- **HR parallel:** employer-sponsored health cover is just HR acting as one kind of payer.
**Likely follow-ups:** 1) *Who is the customer?* Both the patient and the payer, with different needs. 2) *What is a TPA?* A middle administrator for insurers (see Q19).
**Common mistakes:** Assuming the patient always pays the hospital; ignoring that the same bill is seen differently by provider and payer.

### Q3 ⭐⭐⭐ 🟢 What is a health insurance claim, and what is the difference between a cashless claim and a reimbursement claim?
**Asked at:** commonly asked (no company-specific report found); cashless vs reimbursement is a standard Indian health-claims topic in prep and insurer blogs (unverified).
**What the interviewer is checking:** Basic claims vocabulary and who pays first.
**Say this in the interview:** "A claim is a formal request to the insurer to pay for treatment. In cashless, the insurer settles directly with the hospital; in reimbursement, the patient pays first and then claims the money back."
**Explain simply:**
- **Claim:** the bill plus supporting documents (discharge summary, reports) sent to the insurer or its administrator.
- **Cashless:** usually only at network hospitals (hospitals that have an agreement with the insurer). The hospital asks for approval first (see Q20) and the patient pays only non-covered items.
- **Reimbursement:** the patient pays the hospital, collects documents and submits them afterwards; the insurer reviews and pays the patient. Often used at non-network hospitals or when cashless was not approved.
- **Analyst angle:** the two flows have different data owners, different delays and different rejection reasons, so analyse them separately.
- Rules and timelines differ by insurer and regulator; confirm specifics with the insurance team.
**Likely follow-ups:** 1) *Which is faster to settle?* Cashless is usually quicker for the patient, but measure it from data. 2) *Can cashless be denied?* Yes, at approval or at final bill stage.
**Common mistakes:** Calling every claim "cashless"; mixing claim count with claim value; treating "rejected" and "partly paid" as the same.

### Q4 ⭐⭐⭐ 🟢 What are ICD-10 codes, and why does a healthcare data analyst care about them?
**Asked at:** commonly asked (no company-specific report found); ICD-10 appears in healthcare and revenue-cycle analyst postings (unverified).
**What the interviewer is checking:** Whether you know diagnoses are stored as standard codes, not free text.
**Say this in the interview:** "ICD-10 is the international list of codes for diseases and conditions. Analysts use it to group patients and claims consistently, so hospitals and insurers can compare like with like."
**Explain simply:**
- ICD stands for *International Classification of Diseases*, maintained by the World Health Organization; the 10th edition is widely used (from memory, unverified; some countries use extended versions and newer editions exist).
- Each code is letters and digits (for example, a pattern like "A00.0"); the first characters give the broad group and later ones add detail.
- **Why it matters:** counting "diabetes patients" from free-text notes would be chaos; codes let you filter, group, compare hospitals and check whether a procedure fits a diagnosis (a common claim-denial check).
- **Quality risk:** codes are entered by coders or doctors, so mistakes and "upcoding" (picking a higher-paying code) exist. Treat codes as a record of billing and documentation, not perfect clinical truth.
- **HR parallel:** like standard job-family codes: they make headcount comparable.
**Likely follow-ups:** 1) *ICD vs CPT?* ICD codes the diagnosis, CPT codes procedures (see Q30). 2) *What if a patient has several diagnoses?* Usually one primary and several secondary codes; decide which you count.
**Common mistakes:** Grouping by exact code when a broader group is intended; ignoring secondary diagnoses; assuming coding is always accurate.

### Q5 ⭐⭐⭐ 🟢 What is an EMR/EHR and a hospital information system (HIS), and what kinds of tables or data would an analyst get from them?
**Asked at:** commonly asked (no company-specific report found); EMR/HIS data is the core source in healthcare analyst roles (prep sites, unverified).
**What the interviewer is checking:** Whether you know where hospital data lives and what shape it comes in.
**Say this in the interview:** "An EMR or EHR is the digital patient record: visits, diagnoses, medicines, results. The HIS is the wider hospital system that also runs registration, billing, beds and inventory. As an analyst I would get tables for patients, admissions, orders, billing and lab results."
**Explain simply:**
- **EMR (electronic medical record):** one provider's digital chart. **EHR (electronic health record):** meant to be shared across providers. People often use the two words loosely.
- **HIS:** the management side: patient registration, appointments, bed management, billing, pharmacy, stores.
- **Typical tables:** patient master (ID, age, sex, city); visits and admissions (admit, discharge, ward, doctor); diagnoses (ICD codes); procedures; orders (lab, radiology, medicines); lab results; billing lines (service, amount, payer); staff and roster.
- **Reality check:** tables often come from different vendors, with free-text fields, missing values and duplicate patients, so expect cleaning before any KPI.
- **HR parallel:** an HRMS is the employee master plus payroll and attendance; an HIS is the same idea for patients.
**Likely follow-ups:** 1) *What is the join key?* A patient ID plus visit or admission ID. 2) *How would you check quality?* Duplicates, discharge before admission, missing diagnosis.
**Common mistakes:** Assuming one clean table exists; joining on name; ignoring that billing and clinical systems may disagree.

### Q6 ⭐⭐⭐ 🟢 Why is patient data treated as especially sensitive, and what basic rules would you follow when you handle it as an analyst?
**Asked at:** commonly asked (no company-specific report found); privacy and governance are stressed in healthcare analyst guides (unverified).
**What the interviewer is checking:** Whether you handle sensitive data with care and know when to ask permission.
**Say this in the interview:** "Health data can reveal very personal facts and cannot be changed once leaked, so misuse can cause real harm. I would use only what the analysis needs, remove identifiers, share only with authorised people, and follow the organisation's privacy policy."
**Explain simply:**
- **Why sensitive:** diagnoses can lead to discrimination, stigma or fraud; a name plus a diagnosis plus a phone number is a ready-made harm.
- **Basic habits:** minimum data (only needed columns); remove or mask names, phone numbers and IDs; work in approved systems, not personal laptops or email; no screenshots with identifiers; small groups can identify people, so hide tiny counts.
- **Consent and purpose:** data collected for treatment may not be free to use for other purposes; check with the data owner.
- **Employee parallel:** the same care applies to HR records such as medical leave.
- **Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team. The US has HIPAA, India has the Digital Personal Data Protection Act (DPDP) and other health-record guidelines; details and dates must be confirmed.
**Likely follow-ups:** 1) *What if a manager asks for names?* Ask for the purpose and route through the data owner. 2) *What is masking?* Hiding or replacing identifiers.
**Common mistakes:** Emailing raw extracts; thinking removing the name alone makes data anonymous; reporting counts of one or two people.

### Q7 ⭐⭐⭐ 🟢 What is a clinical trial, and what happens in Phase I, II, III and IV in simple terms?
**Asked at:** commonly asked (no company-specific report found); Novartis Hyderabad reports mention clinical-trial and drug-pipeline topics (anecdotal, unverified).
**What the interviewer is checking:** Whether you understand the drug development pipeline you will measure.
**Say this in the interview:** "A clinical trial tests a new treatment on people under strict rules. Phase I checks safety on a small group, II looks at whether it works and the right dose, III confirms it in a large group against standard treatment, and IV watches it after approval."
**Explain simply:**
- **Phase I:** small group (often healthy volunteers, sometimes patients), focus on safety and dose. 
- **Phase II:** a few hundred patients with the condition; early signs of benefit and side effects.
- **Phase III:** large groups, often several hundred to thousands, compared with a standard treatment or placebo (a dummy treatment); results support the application for approval.
- **Phase IV:** after launch, tracks rare side effects and long-term use in the real world.
- Sizes are rough and vary; treat them as typical, from memory, unverified.
- **Analyst angle:** enrolment speed, dropouts, site performance and safety events are all tracked.
**Likely follow-ups:** 1) *Why do many drugs fail?* Weak benefit or safety problems show up in later phases. 2) *What is randomisation?* Random assignment to groups so they are comparable.
**Common mistakes:** Saying Phase I tests effectiveness; thinking the trial ends at approval; treating phases as numbers of patients only.

### Q8 ⭐⭐⭐ 🟢 In pharma sales, what is the difference between primary sales and secondary sales, and which one tells you more about real demand?
**Asked at:** commonly asked (no company-specific report found); IQVIA analyst reports mention Excel cases on sales and market share (anonymous, unverified).
**What the interviewer is checking:** Whether you know sales into the channel is not the same as sales to patients.
**Say this in the interview:** "Primary sales are the company's sales to its distributors (stockists). Secondary sales are the stockists' sales to chemists and hospitals. Secondary sales show real demand better, because primary can be stuffed into stock."
**Explain simply:**
- **Primary:** company invoices to stockists; this is what appears in company revenue.
- **Secondary:** stockists sell on to retail chemists and hospitals; closer to what patients actually buy.
- **Gap:** if primary exceeds secondary for several months, stock is building up at stockists, and a later dip may follow. This is often called *channel stuffing* when pushed deliberately to hit targets.
- **Even closer:** tertiary or prescription data is closest to true demand, but harder to get in India (availability varies, unverified).
- **Data issue:** secondary data often comes through stockists and may be late or incomplete.
- **HR parallel:** like hiring numbers (offers made) versus joiners who actually show up.
**Likely follow-ups:** 1) *Which does revenue reporting use?* Primary. 2) *How do you spot stuffing?* Primary growing faster than secondary, rising stock-days.
**Common mistakes:** Using primary as demand; comparing the two without matching periods; ignoring returns and expiry.

### Q9 ⭐⭐⭐ 🟢 Which five KPIs would you put on a hospital operations dashboard, and what does each one tell the management?
**Asked at:** commonly asked (no company-specific report found); IQVIA reports mention KPI prioritisation tasks (anonymous, unverified).
**What the interviewer is checking:** Judgement: picking few KPIs that cover capacity, efficiency, money and quality.
**Say this in the interview:** "I would choose bed occupancy, average length of stay, ARPOB, claim denial rate and 30-day readmission rate. They cover capacity, flow, earning power, billing health and care quality."
**Explain simply:**
- **Bed occupancy:** how full the beds are (Q10); too low wastes capacity, too high strains staff.
- **ALOS:** average days a patient stays (Q11); long stays tie up beds.
- **ARPOB:** revenue per occupied bed per day (Q12); shows earning power.
- **Claim denial rate:** share of claims insurers refuse (Q13); lost or delayed cash.
- **30-day readmission rate:** patients returning soon after discharge (Q14); a quality signal.
- Others could be emergency wait time, OPD no-show, theatre utilisation. Keep five so management can act.
- Define each metric on the dashboard (counting rule, denominator) and show trend, not just a single number.
**Likely follow-ups:** 1) *Why not 20 KPIs?* Too many hide the signal. 2) *What would you add for patients' experience?* Wait times or feedback score.
**Common mistakes:** Picking only financial KPIs; no definitions; showing a number without trend or comparison.

### Q10 ⭐⭐⭐ 🟡 Calculate bed occupancy rate and explain what data feeds it.
A hospital has 120 available beds. In a 30-day month the census records 2,880 inpatient days (one inpatient day = one patient occupying a bed at midnight).
**Asked at:** commonly asked (no company-specific report found); bed occupancy appears across hospital KPI sources (vendor blogs, unverified).
**What the interviewer is checking:** Can you compute it and state the denominator.
**Say this in the interview:** "Occupancy is inpatient days divided by bed days available. Here 2,880 divided by 3,600 is 80 percent."
**Explain simply:**
- **Bed days available** = 120 beds x 30 days = 3,600.
- **Occupancy** = 2,880 / 3,600 = 0.80 = **80 percent**.
- **Data feeding it:** the midnight census (a headcount of occupied beds each night) from the admission, discharge and transfer records, plus the bed master (how many beds exist).
- Definition used here: available beds as denominator; some hospitals use staffed beds (Q31).
**Worked example:** 120 x 30 = 3,600 bed days; 2,880 / 3,600 = 80.0 percent, exactly. The average midnight census is 2,880 / 30 = 96 patients.
**Likely follow-ups:** 1) *Is 80 percent good?* Depends on the hospital; very high values mean little room for emergencies. 2) *Does it include day-care?* Usually not, state it.
**Common mistakes:** Using patients admitted instead of inpatient days; using 31 days for a 30-day month; forgetting beds under maintenance.

### Q11 ⭐⭐⭐ 🟡 Calculate average length of stay (ALOS) and say what you would do before comparing it with another hospital.
In a month, 450 patients were discharged and they stayed a total of 1,980 patient days.
**Asked at:** commonly asked (no company-specific report found); ALOS is named in hospital MIS prep material (blogs, unverified).
**What the interviewer is checking:** The calculation and awareness that raw ALOS is not like-for-like.
**Say this in the interview:** "ALOS is total patient days divided by discharges: 1,980 divided by 450 is 4.4 days. Before comparing hospitals I would adjust for case mix, meaning the type and severity of patients treated."
**Explain simply:**
- **ALOS** = 1,980 / 450 = **4.4 days** (patients discharged in the month).
- A tertiary hospital with complex surgeries will naturally have longer stays than one doing mostly short procedures.
- **Before comparing:** align the definition (do both count day-care and deaths?), compare the same specialty or diagnosis group, check outliers (a few very long stays pull the average up; look at the median too), and use the same period.
- **Why management watches it:** shorter stays free beds, but too short may mean early discharge and readmissions (Q14).
**Worked example:** 1,980 / 450 = 4.40 days exactly. A few 40-day stays could make the average 4.4 while most patients stay 2 to 3 days; the median shows this.
**Likely follow-ups:** 1) *Why median?* Less distorted by outliers. 2) *Which patients are in the denominator?* Discharged ones, including deaths, unless stated.
**Common mistakes:** Dividing by admissions instead of discharges without saying so; comparing different specialties; ignoring outliers.

### Q12 ⭐⭐⭐ 🟡 Calculate ARPOB (average revenue per occupied bed per day) and explain why hospital management watches it.
Monthly hospital revenue is Rs 18 crore. Occupied bed days in the month are 3,600.
**Asked at:** commonly asked (no company-specific report found); ARPOB is cited as a key hospital-sector metric in explainer blogs (unverified).
**What the interviewer is checking:** The calculation, unit handling (crore) and the meaning.
**Say this in the interview:** "ARPOB is revenue divided by occupied bed days. Rs 18 crore is Rs 18,00,00,000; divided by 3,600 gives Rs 50,000 per occupied bed per day."
**Explain simply:**
- 1 crore = 10 million, so Rs 18 crore = Rs 180,000,000.
- **ARPOB** = 180,000,000 / 3,600 = **Rs 50,000 per occupied bed per day**.
- **Why watched:** it shows how much each used bed earns; it rises with complex procedures, better payer mix and pricing, and falls with long low-value stays. Together with occupancy it tells whether growth comes from more patients or richer patients.
- **Definition caution:** some hospitals use only inpatient revenue; here total revenue is used as given, so state your definition. Total revenue includes OPD and pharmacy, which can inflate ARPOB.
**Worked example:** 18 crore = 18 x 10,000,000 = 180,000,000; 180,000,000 / 3,600 = Rs 50,000.00. Rounded to the nearest rupee, no rounding needed.
**Likely follow-ups:** 1) *What if occupancy falls but ARPOB rises?* Fewer but higher-value patients; check profitability. 2) *Why separate by specialty?* Mix differs widely.
**Common mistakes:** Dividing by available beds instead of occupied bed days; unit errors with crore; mixing OPD revenue with inpatient bed days.

### Q13 ⭐⭐⭐ 🟡 Calculate the initial and the final claim denial rate and explain the difference.
A hospital billing team submitted 2,000 insurance claims in a quarter. 260 were denied at first. After appeals, 40 of those were paid.
**Asked at:** commonly asked (no company-specific report found); denial metrics appear in revenue-cycle analyst postings (unverified).
**What the interviewer is checking:** Whether you separate first-pass denial from the denial that finally sticks.
**Say this in the interview:** "Initial denial rate is 260 out of 2,000, which is 13 percent. After 40 were recovered on appeal, 220 remain denied, so the final denial rate is 11 percent."
**Explain simply:**
- **Initial denial rate** = 260 / 2,000 = **13 percent**; shows how clean the first submission was.
- **Final denial rate** = (260 - 40) / 2,000 = 220 / 2,000 = **11 percent**; shows what was finally lost.
- **Difference:** 2 percentage points, which the appeal team recovered. A big gap means good appeal work; a small gap with high initial rate means problems are fixed late and expensively.
- Definition used here is by count; also report by value (rupees), since a few big claims can matter more.
**Worked example:** 260 / 2,000 = 13.0 percent; 220 / 2,000 = 11.0 percent; 13 - 11 = 2 percentage points (not "2 percent"); appeal success = 40 / 260 = 15.4 percent (rounded to one decimal).
**Likely follow-ups:** 1) *Is denial same as rejection?* Terms vary; some separate rejected (technical error before review) from denied. 2) *Are all denials appealed?* Not always; track appeals filed.
**Common mistakes:** Subtracting percentages as "percent" instead of percentage points; ignoring claims still pending; using claim count only.

### Q14 ⭐⭐⭐ 🟡 Calculate the 30-day readmission rate and name two cautions when you report it.
800 patients were discharged in a month. 64 of them were admitted again within 30 days, of whom 10 were planned follow-up procedures.
**Asked at:** commonly asked (no company-specific report found); readmission is a standard quality metric in hospital KPI sources (unverified).
**What the interviewer is checking:** The maths and the understanding that planned returns are not quality failures.
**Say this in the interview:** "All-cause readmission is 64 out of 800, which is 8 percent. Excluding 10 planned procedures gives 54 out of 800, or 6.75 percent. I would report which one I mean."
**Explain simply:**
- **Readmission:** a patient returns to hospital within a set window (30 days here) after discharge.
- **All-cause** = 64 / 800 = **8.0 percent**. **Unplanned only** = 54 / 800 = **6.75 percent**.
- **Caution 1:** planned vs unplanned. A staged procedure is intended, so including it makes quality look worse.
- **Caution 2:** only you can see your own hospital. A patient readmitted elsewhere is missed, so the rate may be understated; and sicker case mix raises rates unfairly, so compare like groups.
- Also decide whether deaths and transfers sit in the denominator, and count by patient or by discharge.
**Worked example:** 64 / 800 = 0.08; (64 - 10) / 800 = 54 / 800 = 0.0675. Rates as percentages; 8.0 - 6.75 = 1.25 percentage points.
**Likely follow-ups:** 1) *Why 30 days?* A common convention; 7 or 90 days also used. 2) *How to reduce it?* Not medical advice; analysts find which groups return and share findings with clinicians.
**Common mistakes:** Mixing planned with unplanned; counting the same patient twice without a rule; no case-mix context.

### Q15 ⭐⭐⭐ 🟡 Calculate a brand's market share and evolution index and explain what each number tells a pharma sales manager.
Therapy market: Rs 30 crore this year, up 8 percent from last year. Brand A sold Rs 4.2 crore this year, up 12 percent from last year.
**Asked at:** commonly asked (no company-specific report found); IQVIA analyst reports mention market-share Excel cases (anonymous, unverified).
**What the interviewer is checking:** Share calculation and whether you can tell winning from merely riding the market.
**Say this in the interview:** "Market share is 4.2 divided by 30, which is 14 percent. The evolution index is brand growth relative to market growth: 1.12 / 1.08 x 100 is about 103.7, so Brand A is growing slightly faster than its market."
**Explain simply:**
- **Market share** = 4.2 / 30 = **14.0 percent** (a therapy market is all competing brands for one type of condition).
- **Evolution index (EI)** = (brand growth factor / market growth factor) x 100 = **about 103.7**. Above 100 means gaining share; below 100 means losing.
- **Last year's share:** brand 4.2 / 1.12 = 3.75 crore; market 30 / 1.08 = 27.78 crore; share = 13.5 percent. So share rose by **0.5 percentage points**.
- **Manager's reading:** brand is growing, and gaining a little share, but not dramatically. Check by territory and by competing brands.
- Definition note: some companies compute EI from growth percentages differently; state yours.
**Worked example:** 3.75 / 27.7778 = 13.5 percent; 14.0 - 13.5 = 0.5 percentage points; EI = 1.12 / 1.08 x 100 = 103.70 (rounded to two decimals).
**Likely follow-ups:** 1) *If the market is growing fast, is 12 percent good?* It must be compared with 8 percent; here it beats it. 2) *Source of market data?* Third-party audit data, availability varies.
**Common mistakes:** Subtracting the growth rates (4 points) instead of using the ratio; saying share rose "0.5 percent"; using different periods for brand and market.

### Q16 ⭐⭐⭐ 🟡 A trial needs 200 enrolled patients and the expected screen failure rate is 40 percent. How many people must be screened, and why does this matter for planning?
**Asked at:** commonly asked (no company-specific report found); screen failure and enrolment metrics appear in trial-operations sources (trade press, unverified).
**What the interviewer is checking:** Whether you divide by the success rate rather than adding the failure rate.
**Say this in the interview:** "If 40 percent fail screening, only 60 percent are enrolled, so I need 200 divided by 0.6, about 333.3, so 334 people screened."
**Explain simply:**
- **Screening:** checking whether a person meets the trial's entry rules (age, condition, test values). Those who do not qualify are *screen failures*.
- Enrolled = screened x (1 - 0.40) = screened x 0.60, so screened = 200 / 0.60 = 333.33, rounded **up** to **334**.
- Check: 334 x 0.6 = 200.4 (at least 200); 333 x 0.6 = 199.8 (just short).
- **Why it matters:** recruitment is the main time and cost driver. Planning for 200 screenings would leave the trial about 80 short. Screening effort, number of sites, timelines and budget all scale up.
- Real trials also lose patients after enrolment (dropouts); a plan would allow for those separately.
**Worked example:** 200 / 0.6 = 333.33; ceiling = 334. Wrong shortcut: 200 x 1.4 = 280, which gives only 168 enrolled (280 x 0.6).
**Likely follow-ups:** 1) *What if 10 percent also drop out?* Enrol 200 / 0.9, then screen on top of that. 2) *Why track by site?* Screen failure differs by site.
**Common mistakes:** Multiplying by 1.4; rounding down; ignoring dropouts.

### Q17 ⭐⭐⭐ 🟡 You are asked to analyse why health insurance claims are being denied at a hospital. What tables and fields would you ask for, and what are your first cuts?
**Asked at:** commonly asked (no company-specific report found); claims and denial analysis appears in hospital revenue-cycle job postings and prep guides (unverified).
**What the interviewer is checking:** Whether you can turn a vague "why" into specific tables, a clear denial definition and a sensible order of cuts.
**Say this in the interview:** "I would first agree what counts as a denial, then ask for one row per claim with its payer, department, amounts, dates and the denial reason code. My first cuts are denial rate and denied rupees by payer, department, reason and month, to find where the money is lost."
**Explain simply:**
- A *claim* is the hospital's bill sent to the insurer (the *payer*) for payment. A *denial* means the payer refused to pay all or part of it.
- Define it first: count by number of claims and by rupee value, and say whether you mean the first-time (initial) denial or what stays denied after appeals (see Q13).
**Data and tables involved:**
- *Claims table:* claim ID, patient ID, admission and discharge dates, department, doctor, payer, TPA (the insurer's claims handler), billed amount, approved amount, status.
- *Denial table:* claim ID, denial date, reason code and text, appeal date, appeal outcome.
- *Pre-authorisation table* (approval requested before treatment): request time, approved amount, decision time.
- *Billing lines* (to see which item was cut) and *coding table* (diagnosis and procedure codes).
- First cuts, in order: denial rate by month (trend), then by payer, department, reason, and top reasons by denied value.

Illustrative run on 8 invented claims (claim_id, department, status, billed in Rs): 1 Cardio Paid 150000; 2 Cardio Denied 200000; 3 Cardio Paid 120000; 4 Ortho Denied 110000; 5 Ortho Paid 90000; 6 Ortho Denied 80000; 7 General Paid 30000; 8 General Denied 40000. The query below works in SQLite and MySQL (in other databases write the denied count with CASE WHEN).
```sql
SELECT department,
       COUNT(*) AS claims,
       SUM(status = 'Denied') AS denied,
       ROUND(100.0 * SUM(status = 'Denied') / COUNT(*), 1) AS denial_rate_pct,
       SUM(CASE WHEN status = 'Denied' THEN billed ELSE 0 END) AS denied_value
FROM claims
GROUP BY department
ORDER BY denied_value DESC;
```
Output:

| department | claims | denied | denial_rate_pct | denied_value |
|---|---|---|---|---|
| Cardio | 3 | 1 | 33.3 | 200000 |
| Ortho | 3 | 2 | 66.7 | 190000 |
| General | 2 | 1 | 50.0 | 40000 |

In plain words: Cardio loses the most rupees, Ortho has the highest rate, so both need a look. Eight rows prove nothing; this only shows the cut.
**Regulation / privacy note (awareness only):** The extract has patient identity; ask for IDs masked and only needed fields (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Reason codes are free text?* Group them into a few standard buckets with the billing team. 2) *Rate looks fine but money is lost?* Check denied value and partial cuts, not just full denials.
**Common mistakes:** Mixing initial and final denials; quoting rate without rupees; blaming payers before checking documentation and coding errors.

### Q18 ⭐⭐⭐ 🟡 You receive a patient-level extract with names, phone numbers and diagnoses for an analysis that needs only trends. What do you do before you start?
**Asked at:** commonly asked (no company-specific report found); data-privacy handling is a recurring theme in healthcare analyst guides (unverified).
**What the interviewer is checking:** That you apply data minimisation: use only what the question needs, and raise the issue instead of quietly proceeding.
**Say this in the interview:** "I would not start with names and phone numbers in my file. I would tell the data owner the analysis needs only trends, ask for a version with direct identifiers removed or replaced by a coded ID, and delete the original copy I received if policy says so."
**Explain simply:**
- *Direct identifiers* (name, phone) point straight to a person; *quasi-identifiers* (age, pin code, rare diagnosis, dates) can identify someone when combined.
- Trends need counts by month, age band or department, not individuals. So: drop names and phones, keep a pseudonymous ID if you must link records, convert exact dates to months, and use age bands.
- Check small groups: a count of 1 or 2 for a rare diagnosis can reveal a person, so suppress or merge small cells.
- Work in the approved location, share only aggregates, and record what you did.
- HR parallel: you would not need employee names to study attrition by grade.
**Regulation / privacy note (awareness only):** India's DPDP Act (2023) and the US HIPAA both stress using personal data only for a stated purpose; the exact rules on de-identification differ and I cannot give specifics from memory (unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Can you keep a mapping from code to name?* Only the data owner should hold it, separately. 2) *Is removing names enough?* No, combinations of other fields can still identify people.
**Common mistakes:** Saving the raw file on a laptop or emailing it; thinking a dropped name column means anonymous; sharing a chart with tiny groups.

### Q19 ⭐⭐ 🟢 What does a TPA (third-party administrator) do in Indian health insurance, and what data does it hold?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know who sits between hospital and insurer and what data that creates.
**Say this in the interview:** "A TPA is a company that handles health-claim paperwork for insurers: it checks policies, approves cashless requests and processes claims. It holds policyholder, hospital, pre-authorisation and claim data."
**Explain simply:**
- An insurer may outsource claims handling to a TPA, much like a company outsourcing payroll processing. Some insurers handle claims in-house instead.
- Typical tasks: verify the policy is active and the illness is covered, decide pre-authorisation (Q20), manage the hospital network, settle or reject claims, handle queries.
- Data held: policy and member details, hospital network list and agreed rates, pre-auth requests and decisions with times, claim amounts approved and rejected, rejection reasons, settlement dates.
- For an analyst, TPA data is the "other side" of the hospital's own claims table; reconciling the two explains many differences.
**Regulation / privacy note (awareness only):** TPAs are regulated by the insurance regulator, IRDAI; details from memory, unverified, confirm with the compliance/legal team. They hold sensitive health data, so access is restricted.
**Likely follow-ups:** 1) *Why compare TPA and hospital data?* Amounts and statuses often differ. 2) *Does every claim go through a TPA?* No, depends on the insurer.
**Common mistakes:** Saying the TPA is the insurer; assuming TPA and hospital denial counts match without checking definitions.

### Q20 ⭐⭐ 🟢 What is pre-authorisation in cashless treatment, and why do turnaround times for it matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand the cashless flow and can link delay to patient and money impact.
**Say this in the interview:** "Pre-authorisation is the insurer's or TPA's approval, requested by the hospital before planned treatment, that it will pay up to a stated amount. Turnaround time matters because delays hold up admission and discharge and add cost."
**Explain simply:**
- In a *cashless* claim the patient pays nothing (or only non-covered items) at the hospital; the insurer pays the hospital directly.
- Steps: the hospital sends a pre-auth request with diagnosis and estimated cost; the TPA approves, queries or rejects; the amount may be revised later (enhancement) if treatment grows.
- Turnaround time (TAT) is the gap from request to decision. A slow answer means the patient waits, beds stay blocked, or the family pays upfront and claims later.
- Analyst view: report median and 90th percentile TAT by payer, not just the average, and track the share approved at first attempt. Specific regulatory time limits exist; from memory, unverified, I would not quote them.
**Likely follow-ups:** 1) *Does approval guarantee payment?* No, the final bill can still be partly cut. 2) *Which cut shows delay?* TAT by payer and hour of day.
**Common mistakes:** Reporting only averages; counting weekends and hours differently by payer; ignoring queries sent back to the hospital.

### Q21 ⭐⭐ 🟢 What are the main stages of the revenue cycle in a hospital, from registration to payment collection?
**Asked at:** commonly asked (no company-specific report found); revenue cycle management (RCM) stages appear in healthcare analyst job postings (unverified).
**What the interviewer is checking:** Whether you can walk the money path and name where it leaks.
**Say this in the interview:** "Registration, pre-authorisation or eligibility check, treatment and charge capture, coding, billing, claim submission, payer response with denial handling, and finally payment collection and reconciliation."
**Explain simply:**
- *Registration:* patient details and insurance captured (errors here cause later denials).
- *Eligibility / pre-auth:* is the patient covered and approved (Q20).
- *Charge capture:* every service given (room, tests, drugs) is recorded as a billable item; missed items are lost revenue.
- *Coding:* the diagnosis and procedures are turned into standard codes (see Q30).
- *Billing and claim submission:* the final bill goes to the insurer or the patient.
- *Denials and follow-up:* rejected claims are corrected and appealed.
- *Collection:* money received is matched to bills; unpaid balances go to follow-up.
- Analyst metrics per stage: pre-auth TAT, clean claim rate, denial rate, days in accounts receivable.
**Likely follow-ups:** 1) *Where do most denials start?* Often early: registration, missing documents, coding. 2) *Cash patients?* They skip the payer steps.
**Common mistakes:** Treating billing as the whole cycle; not noticing that front-end errors show up as back-end denials.

### Q22 ⭐⭐ 🟢 Who is a medical representative (MR) in pharma, and how is a typical field-force hierarchy organised (MR, area manager, regional manager)?
**Asked at:** commonly asked (no company-specific report found); a pharma analytics job posting in the internal notes mentions field-force analysis (unverified).
**What the interviewer is checking:** Whether you understand who generates sales and how the sales team's data rolls up.
**Say this in the interview:** "An MR visits doctors and chemists in a defined territory to explain the company's medicines. MRs report to an area manager, who reports to a regional manager, and numbers roll up from territory to area to region to country."
**Explain simply:**
- The MR does *detailing*: a short visit to a doctor to present a brand, leave samples and literature. The MR does not sell to patients.
- Typical ladder (names vary by company): MR, then area manager (team of several MRs), then regional manager (several areas), then zonal or national head.
- Each MR owns a *territory*, a set of doctors and chemists. Targets, calls made and sales are tracked at that level.
- Analyst uses: call coverage (share of target doctors visited), sales versus target, performance by territory, then rolled up. Similar to HR rolling headcount from team to department.
**Likely follow-ups:** 1) *What if territories change?* Keep a history table, otherwise trends break. 2) *Why do MRs matter to data?* They are the main source of field activity data.
**Common mistakes:** Calling an MR a salesperson who sells to consumers; comparing territories with very different doctor counts without adjusting.

### Q23 ⭐⭐ 🟢 What do these pharma terms mean: molecule, brand, generic, formulation, therapy area?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic vocabulary, since every pharma dataset uses these words as columns.
**Say this in the interview:** "The molecule is the active ingredient, a brand is a company's named product, a generic is the same molecule sold under its chemical name or a cheaper label, the formulation is the form and strength, and the therapy area is the disease group."
**Explain simply:**
- *Molecule* (or salt): the active chemical, for example paracetamol.
- *Brand:* the trade name a company sells it under. Many brands can carry the same molecule.
- *Generic:* a product with the same molecule as an original, sold after the original's protection ends, usually at a lower price.
- *Formulation:* tablet, syrup, injection, and the strength (such as 500 mg); the same brand can have several, each tracked as a separate item (SKU).
- *Therapy area:* a disease group such as diabetes or cardiology, used to group brands and markets.
- Analyst use: market share is usually computed within a molecule or therapy area, so these columns define "the market".
**Likely follow-ups:** 1) *Why does the market definition matter?* Share changes with who you include. 2) *Is generic lower quality?* Not for me to judge; analysts just treat it as a product type.
**Common mistakes:** Mixing brand and molecule in one group; comparing different formulations as if equal.

### Q24 ⭐⭐ 🟢 Who are the sponsor, the CRO, the site and the investigator in a clinical trial, and what is a case report form (CRF)?
**Asked at:** commonly asked (no company-specific report found); one Novartis report mentions clinical trials, anecdotal and unverified.
**What the interviewer is checking:** Whether you know the players and where trial data originates.
**Say this in the interview:** "The sponsor owns and funds the trial, the CRO is a company hired to run parts of it, the site is the hospital or clinic where patients are treated, the investigator is the doctor in charge there, and the CRF is the form where each patient's trial data is recorded."
**Explain simply:**
- *Sponsor:* usually the pharma company that wants the drug approved.
- *CRO (contract research organisation):* an outside firm that manages monitoring, data and statistics for the sponsor.
- *Site and investigator:* the investigator leads the study at one site and is responsible for the patients there.
- *CRF:* a (now mostly electronic) form with one set of entries per patient per visit: measurements, medicines, adverse events (Q25).
- Data flows from site CRFs to a clinical database, gets checked and cleaned, then analysed. Analysts query it by site and patient.
**Regulation / privacy note (awareness only):** Trial participants are identified by a code, not a name; consent and ethics review rules apply (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Why look at data by site?* Sites differ in quality and speed. 2) *Who cleans data?* Usually clinical data management at the CRO or sponsor.
**Common mistakes:** Treating the CRO as the sponsor; assuming trial data is like clean business data when it is query-driven and corrected.

### Q25 ⭐⭐ 🟢 What is the difference between an adverse event (AE) and a serious adverse event (SAE), and who tracks them?
**Asked at:** commonly asked (no company-specific report found); AE and SAE appear in clinical data prep blogs (unverified).
**What the interviewer is checking:** That you know AE is any bad event and SAE is the severe subset with stricter reporting.
**Say this in the interview:** "An AE is any unwanted medical event in a trial participant, whether or not the drug caused it. An SAE is an AE that is serious, for example it leads to hospitalisation or death or is life-threatening, and it must be reported faster."
**Explain simply:**
- Examples: a headache is an AE; a hospital admission because of a reaction is an SAE.
- "Adverse" does not prove the drug caused it; causality (relatedness) is assessed separately by the investigator.
- Tracking: the investigator records it at the site, the sponsor or CRO safety team reviews it, and ethics committees and regulators are informed per rules. Drug safety teams (pharmacovigilance) keep tracking after the drug is launched.
- Analyst uses: AE counts per patient-year or per arm, SAE lists, and reconciling SAEs between the safety database and the clinical database.
**Regulation / privacy note (awareness only):** Reporting timelines are set by regulators; I do not recall exact days (unverified, confirm with the compliance/legal team). No medical judgement from analysts.
**Likely follow-ups:** 1) *Is every AE caused by the drug?* No. 2) *Why compare two databases?* A missing SAE is a safety issue.
**Common mistakes:** Using "serious" as "severe pain"; counting events instead of patients without saying which.

### Q26 ⭐⭐ 🟢 What is NABH accreditation in plain words, and why would quality indicators be tracked by an analyst?
**Asked at:** commonly asked (no company-specific report found); NABH, NABL and JCI appear as likely hospital-MIS topics on prep blogs (unverified).
**What the interviewer is checking:** Whether you know hospitals are measured against quality standards and that data backs it.
**Say this in the interview:** "NABH is an Indian body that accredits hospitals, meaning it certifies they meet set quality and safety standards. Analysts track indicators such as infections and waiting times so the hospital can show and improve its standards."
**Explain simply:**
- NABH is part of the Quality Council of India (from memory, unverified). Accreditation works like an audit with a pass certificate that must be renewed.
- Hospitals are expected to monitor indicators regularly. Examples: hospital-acquired infection rate, patient fall rate, medication errors, readmissions, waiting time, patient satisfaction.
- Analyst role: define each indicator, collect data consistently, report trends and flag outliers before an audit. The same indicator must use the same definition every month.
- NABL is a similar body for laboratories (from memory, unverified).
**Likely follow-ups:** 1) *Why does consistency matter?* Trends are meaningless if definitions change. 2) *Who uses the data?* Quality team and management.
**Common mistakes:** Reporting rates without a clear denominator; treating accreditation as a one-time event.

### Q27 ⭐⭐ 🟢 What is a patient unique ID (UHID or MRN), and what goes wrong in analysis when one patient has two IDs?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand patient identity and duplicate records.
**Say this in the interview:** "UHID (unique health ID) or MRN (medical record number) is the number a hospital gives each patient, so all their visits link together. If one patient has two IDs, counts and histories split."
**Explain simply:**
- It is like an employee ID: it should identify one person for life across OPD, IPD and billing.
- Duplicates happen from spelling differences, a second registration after losing a card, or emergency admission with no details.
- Effects: unique patients are overcounted; repeat visits and readmissions are missed (a readmission under a new ID looks like a new patient); history, such as allergies, is split; revenue per patient looks wrong.
- Fixes: match on name, date of birth, phone and similar fields; the registration desk should search before creating; keep a merge log for approved merges.
**Regulation / privacy note (awareness only):** Matching uses personal data, so do it inside the approved system with limited access (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Can two people share an ID?* Rare, but worse; it mixes records. 2) *How do you size the problem?* Share of IDs that match on date of birth and name.
**Common mistakes:** Counting rows as patients; merging records on name alone.

### Q28 ⭐⭐ 🟢 Besides doctors and nurses, which staff groups does a hospital have, and how do visiting consultants and contract staff complicate headcount reporting?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill question.
**What the interviewer is checking:** Whether you see that a hospital's workforce is wider than clinicians and that headcount definitions need care.
**Say this in the interview:** "Besides doctors and nurses there are paramedical and technical staff, pharmacy, housekeeping, security, front office, billing and administration. Visiting consultants and contract staff are not on payroll the same way, so I would state which groups a headcount includes."
**Explain simply:**
- Groups: allied health (lab technicians, radiographers, physiotherapists), pharmacy, front desk and billing, housekeeping and security (often through contractors), kitchen, engineering and IT, management.
- *Visiting consultants* are doctors who come on a fee or revenue-share basis, not salary. They may not be employees, yet they bring patients and income.
- *Contract staff* are on an agency's payroll, so they may not be in the HR system.
- Reporting fix: split headcount into employees, contractual, and visiting, and report each. Say whether the number is headcount or full-time equivalent (FTE).
- A ratio like patients per nurse changes if contract nurses are left out.
**Likely follow-ups:** 1) *Where does contract data live?* Vendor invoices or attendance logs. 2) *Why FTE?* Part-timers distort headcount.
**Common mistakes:** Quoting one "total staff" number; leaving out agency staff; counting visiting doctors as employees.

### Q29 ⭐⭐ 🟢 Where does a hospital earn its revenue (consultations, room rent, procedures, pharmacy, diagnostics), and why does the revenue mix matter for analysis?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the revenue streams and that averages hide differences between them.
**Say this in the interview:** "Hospital revenue comes from consultations, room and nursing charges, procedures and surgeries, pharmacy, and diagnostics such as lab and imaging. The mix matters because each stream has different volume, margin and drivers."
**Explain simply:**
- *OPD (outpatient) revenue:* consultations, tests, pharmacy; many small bills.
- *IPD (inpatient) revenue:* room rent, nursing, doctor fees, procedures, implants, drugs; fewer, larger bills.
- Pharmacy and diagnostics often bring volume but at different margins than procedures (stated as a general idea, unverified for any hospital).
- Why mix matters: a rise in total revenue could be more patients, a higher price, or a shift to costlier procedures. Analyst view: split revenue by stream, by payer type (cash, insurance, government schemes) and by specialty, then compare with volumes.
- It also changes metrics such as revenue per occupied bed (Q12).
**Likely follow-ups:** 1) *Why look at payer mix?* Different payers pay differently and deny differently. 2) *What is a mix effect?* Total changes just from the share of streams shifting.
**Common mistakes:** Looking only at total revenue; ignoring pharmacy sales that run outside the main bill.

### Q30 ⭐⭐ 🟡 Explain the difference between ICD-10, CPT, SNOMED CT, LOINC and MedDRA in one line each, and say which kind of analyst meets which.
**Asked at:** commonly asked (no company-specific report found); ICD-10 and CPT appear in healthcare analyst postings, MedDRA in clinical data prep blogs (unverified).
**What the interviewer is checking:** That you can name the main code systems and tie each to a job type.
**Say this in the interview:** "Each is a standard code list: ICD-10 for diagnoses, CPT for procedures, SNOMED CT for detailed clinical terms, LOINC for lab tests, and MedDRA for adverse events in trials and drug safety."
**Explain simply:**
- *ICD-10:* codes for diseases and conditions, used for statistics and claims. Hospital, claims and insurance analysts.
- *CPT:* codes for procedures and services, mainly used in US billing (from memory, unverified); India often uses other procedure lists. Revenue cycle analysts on US work.
- *SNOMED CT:* a very detailed clinical vocabulary inside electronic records. Health-informatics and EMR data analysts.
- *LOINC:* identifiers for lab tests and measurements, so "blood sugar" means the same everywhere. Lab and EMR data analysts.
- *MedDRA:* a dictionary for coding adverse events and medical history. Clinical data and pharmacovigilance analysts.
- Why they matter: without a standard code you cannot group or compare across systems.
**Likely follow-ups:** 1) *Which is closest to billing?* ICD-10 and CPT. 2) *Do you memorise codes?* No, use a lookup table.
**Common mistakes:** Treating all as diagnosis lists; assuming every country uses the same procedure code set.

### Q31 ⭐⭐ 🟡 Why can bed occupancy be reported with different denominators (available beds vs staffed beds), and how would you make the dashboard unambiguous?
**Asked at:** commonly asked (no company-specific report found); the denominator caveat is noted on hospital KPI blogs (unverified).
**What the interviewer is checking:** Whether you see that one name can hide two definitions, and that you fix it.
**Say this in the interview:** "Occupancy is occupied bed-days divided by bed-days available, but 'available' can mean beds on the license, beds physically set up, or beds with staff. The same hospital looks fuller on staffed beds, so I would label the denominator and show both."
**Explain simply:**
- Three common denominators: licensed or sanctioned beds, beds physically installed, beds staffed and usable today.
- Same occupied beds, different percentage. If 80 beds are occupied: out of 100 is 80.0%, out of 90 is 88.9%, out of 80 is 100.0% (computed, invented numbers).
- Staffed-bed occupancy shows real pressure on capacity; licensed-bed occupancy shows how well the asset is used. Management may want different views.
- Dashboard fixes: write the denominator in the title ("occupancy on staffed beds"), show beds, bed-days and occupied beds beside the %, keep a metric definition note, and never change the definition mid-year without marking it.
- Also state the timing: midnight census or daily average (Q32).
**Likely follow-ups:** 1) *Which one do you pick?* Ask management; show both if unsure. 2) *Beds under maintenance?* Exclude from staffed, and record why.
**Common mistakes:** Comparing hospitals using different denominators; a bare "Occupancy 88%" tile.

### Q32 ⭐⭐ 🟡 How do you count inpatient days when a patient is admitted at 11 pm and discharged at 10 am two days later, and why do hospitals agree a counting rule?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know how bed-days are counted and that a written rule is needed.
**Say this in the interview:** "Under the common midnight census rule, a patient counts one day for each midnight spent in the hospital. 11 pm to 10 am two days later crosses two midnights, so 2 inpatient days. The key is that everyone uses the same rule."
**Explain simply:**
- Worked example (invented dates): admitted 1 March 11 pm, discharged 3 March 10 am. Midnights crossed: night of 1-2 March and night of 2-3 March, so 2 days. Same as date difference, 3 March minus 1 March = 2 days (computed).
- Elapsed time is 35 hours, or 1.46 days (computed). Different rules give 1.46, 2 or even 3 (counting both calendar dates), so totals, occupancy and ALOS (average length of stay) shift.
- Other rules exist: counting the admission day and not the discharge day (same result here), or counting by bed charges. Same-day admissions and discharges are handled by a separate rule (often counted as 1 day, from memory, unverified).
- Agreeing a rule keeps occupancy, ALOS and revenue per bed comparable across months, wards and hospitals, and matches room billing.
**Likely follow-ups:** 1) *What about ward transfers?* Count each day once, in the ward at midnight. 2) *How do you code it in data?* Subtract dates, and test same-day cases.
**Common mistakes:** Counting both admission and discharge dates (inflates days); using hours/24 in one report and midnights in another.

### Q33 ⭐⭐ 🟡 Lab turnaround time (TAT) for blood tests is reported as an average. What does the data below suggest and what would you report instead?
Seven samples, TAT in minutes: 30, 35, 40, 45, 50, 55, 240.
**Asked at:** commonly asked (no company-specific report found); TAT is named as a likely hospital-MIS topic in prep blogs (unverified).
**What the interviewer is checking:** Whether you know one extreme value can drag an average, and which summary you would use instead.
**Say this in the interview:** "The average is 70.7 minutes, but six of the seven samples are 55 minutes or less. One 240-minute sample inflates it. I would report the median, 45 minutes, plus the 90th percentile, and investigate the outlier."
**Explain simply:**
- **TAT (turnaround time):** minutes from sample collection (or registration) to the report being released. Define the start and stop points first; labs differ.
- **Average vs median:** the median is the middle value when sorted. Think of one employee on a Rs 50 lakh salary in a team of seven: the average salary misleads, the median does not.
- **What to report:** the median, a high percentile (the 90th means 9 in 10 samples are at or under it) and the share done within the promised time. Patients feel the slow tail, not the average.
- **The outlier:** 240 minutes may be a machine breakdown, a recollected sample or a data error. Look into it; do not silently delete it.
**Worked example:** Sum = 495 minutes. Mean = 495 / 7 = 70.7. Median = 45 (4th of 7 sorted values). Mean without the outlier = 42.5. 90th percentile (linear interpolation) = 129. Rounded to one decimal.
**Likely follow-ups:** 1) *Should you drop 240?* Not silently; report it separately with its cause. 2) *Why a percentile?* It shows how bad the slow cases get, which a median hides. 3) *Split by what?* Test type, hour of day, urgent versus routine.
**Common mistakes:** Reporting only the mean; mixing urgent and routine tests in one number; not defining when the clock starts.

### Q34 ⭐⭐ 🟡 Calculate the OPD no-show rate and explain what you would do with it.
500 appointments were booked in a week. 40 were cancelled in advance, 90 patients did not turn up, and 370 were seen.
**Asked at:** commonly asked (no company-specific report found); OPD (outpatient department, patients who visit but are not admitted) throughput is a listed hospital-MIS topic (unverified).
**What the interviewer is checking:** Whether you choose the denominator carefully and turn the number into an action.
**Say this in the interview:** "Of 460 appointments that were still active on the day, 90 no-shows is 19.6%. If I divide by all 500 booked it is 18.0%. I would state which definition I use, then look at who no-shows and why."
**Explain simply:**
- **No-show:** the patient booked, did not cancel and did not come. An advance cancellation frees the slot for someone else, so it is not the same problem.
- **Denominator:** my definition is no-shows / (booked minus cancelled in advance). Some hospitals use all booked; definitions differ, so say yours.
- **Check:** 40 + 90 + 370 = 500, so the numbers are consistent.
- **Use it:** split by doctor, day, time slot, booking lead time and new versus follow-up patients. Typical responses are reminder messages and calls, controlled overbooking in high no-show slots, and easy rescheduling. It is the same logic as unplanned absence in HR: find the pattern before choosing the fix.
**Worked example:** 90 / 460 = 19.57%, rounded to 19.6%. Seen rate on active slots = 370 / 460 = 80.4%. Against all booked: 90 / 500 = 18.0%. Advance cancellations = 40 / 500 = 8.0%.
**Likely follow-ups:** 1) *Is overbooking safe?* Only with data on slot-level no-show rates; too much causes long waits. 2) *Which cut first?* Lead time: far-ahead bookings usually no-show more (a hypothesis to test).
**Common mistakes:** Counting advance cancellations as no-shows; a single hospital-wide rate that hides high-risk slots; not stating the denominator.

### Q35 ⭐⭐ 🟡 Calculate the OPD-to-IPD conversion rate and explain how a doctor-wise view could mislead.
A hospital had 6,000 OPD visits in a month and 300 of those patients were admitted.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute a conversion rate and spot the traps in slicing it by doctor.
**Say this in the interview:** "300 / 6,000 is 5%. By doctor it can mislead because specialties, case severity and referral patterns differ, and small volumes make rates swing."
**Explain simply:**
- **OPD (outpatient department):** patients who see a doctor and go home. **IPD (inpatient department):** patients admitted to a bed.
- **Conversion rate** here is admissions that came from OPD divided by OPD visits. It matters for bed planning and revenue.
- **Why doctor-wise misleads:** a surgeon sees patients who often need admission, a general physician sees mostly minor illness, so comparing them is unfair. A senior doctor who receives referrals sees sicker patients. A doctor with 20 visits and 4 admissions shows 20%, which is mostly noise.
- **Also:** "visits" may count one patient several times, while "admitted patients" count people. Use the same unit on both sides and a consistent time window (admission may happen days after the visit).
**Worked example:** 300 / 6,000 = 0.05 = 5.0%.
**Likely follow-ups:** 1) *Is a higher rate good?* Not by itself; it could mean over-admission or just sicker patients. 2) *Fair comparison?* Within the same specialty, with case mix and volume shown.
**Common mistakes:** Ranking doctors on the raw rate; mixing visits with unique patients; ignoring the admission-timing window.

### Q36 ⭐⭐ 🟡 Calculate operating theatre utilisation and explain why booked time and actual time differ.
One theatre is available 10 hours (600 minutes) on a day. Four cases took 120, 90, 150 and 60 minutes of surgery time.
**Asked at:** commonly asked (no company-specific report found); theatre utilisation is a common hospital-operations metric in prep material (unverified).
**What the interviewer is checking:** Whether you know the formula and understand the gap between plan and reality.
**Say this in the interview:** "Surgery time is 420 minutes out of 600 available, so utilisation is 70%. The other 180 minutes are cleaning, turnover, delays and idle gaps."
**Explain simply:**
- **OT (operating theatre) utilisation** = minutes used for surgery / minutes available. Definitions vary: some count only cut-to-close surgery time, some include anaesthesia and setup. State yours.
- **Booked vs actual:** a case booked for 2 hours may take 1.5 or 3. Reasons include late starts, delayed patient or surgeon, cleaning and turnover between cases, emergency cases pushing the list, and cancellations.
- **Reading it:** 70% with no delays may be fine; it is not automatically "30% waste", because some turnover time is unavoidable.
- **HR angle:** it is the same as comparing booked shift hours with productive hours.
**Worked example:** 120 + 90 + 150 + 60 = 420 minutes. 420 / 600 = 70.0%. Unused = 600 - 420 = 180 minutes (3 hours), or 30.0%.
**Likely follow-ups:** 1) *What else to track?* First-case on-time start, turnover time and cancellation rate. 2) *Booked-time utilisation?* Booked minutes / available minutes, compared with actual, shows planning accuracy.
**Common mistakes:** Mixing definitions across theatres; treating all unused time as waste; ignoring emergency cases.

### Q37 ⭐⭐ 🟡 Calculate the nurse-to-patient ratio and name two other workforce metrics you would pair with it.
On the morning shift a ward has 90 occupied beds and 18 nurses on duty.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute a staffing ratio and know it needs context.
**Say this in the interview:** "90 patients and 18 nurses gives 5 patients per nurse, a 1:5 ratio on that shift. I would pair it with nursing hours per patient day and absenteeism or overtime."
**Explain simply:**
- **Ratio** = occupied beds (patients) / nurses on duty, for one shift. It changes by shift, so night and morning must be reported separately.
- **Why a ratio alone misleads:** a general ward and an ICU need very different numbers (ICU patients are sicker and need more nurses per patient), so compare like with like. Nurses "on duty" should be those actually present, not rostered.
- **Pair with:** (1) nursing hours per patient day (total nursing hours worked / patient days, one patient day = one patient in a bed for one day); (2) absenteeism, overtime hours or vacancy rate; skill mix (share of senior versus junior nurses) is another good one.
**Worked example:** 90 / 18 = 5.0 patients per nurse (1:5). Inverse: 18 / 90 = 0.2 nurses per patient. Ratios shown as exact.
**Likely follow-ups:** 1) *Is 1:5 safe?* I cannot say without the ward type and acuity; statutory or accreditation norms exist (from memory, unverified, confirm with the nursing leadership). 2) *Which beds in the denominator?* Occupied beds, not available beds.
**Common mistakes:** Using rostered rather than present nurses; one hospital-wide ratio; comparing ICU with general wards.

### Q38 ⭐⭐ 🟡 What data would you use to study nurse attrition in a hospital and its link to patient care, and what cautions apply?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can join HR data with operational data sensibly and avoid over-claiming a link.
**Say this in the interview:** "I would build a ward-by-month table of nurse exits, vacancies, overtime and absenteeism, and join it to patient-care indicators like falls, infections, complaints and readmissions. I would present it as an association, not proof of cause."
**Explain simply:**
- **HR data (my home ground):** employee master (joining date, ward, grade, experience), exits with reasons and dates, roster and attendance, overtime, vacancy and hiring, exit-interview themes.
- **Patient-care data:** occupancy, patient days, falls, medication errors, hospital-acquired infection counts, complaints, patient feedback, readmissions. Use rates per 1,000 patient days, not raw counts, so busy wards are fair.
- **Grain:** ward x month is a practical level; one row per ward-month.
- **Cautions:** association is not causation (high workload can cause both exits and poor care). Time lag matters (exits may affect care weeks later). Sicker patients and new staff change the picture. Small wards give noisy rates. Keep it at ward level and protect identities of staff and patients.
**Data and tables involved:** `employee_master`, `exits`, `roster_attendance`, `ward_daily_census`, `incident_log`, `patient_feedback`; keys are ward and month.
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team: patient records are sensitive personal data; use only what the purpose needs, mask patient identifiers, and report in aggregate. Staff data also needs care with access and purpose.
**Likely follow-ups:** 1) *Which method?* Compare ward-level trends with a lag, then consider a regression adjusting for patient mix. 2) *Who sees ward-level results?* Limited, role-based access.
**Common mistakes:** Claiming that attrition causes poor care from one chart; raw counts instead of rates; ignoring lag and case mix.

### Q39 ⭐⭐ 🟡 Calculate days in accounts receivable (A/R) and say what a rising number means.
Outstanding insurer receivables are Rs 6 crore. Average monthly billing to insurers is Rs 3 crore (use a 30-day month).
**Asked at:** commonly asked (no company-specific report found); A/R days is a core revenue-cycle metric in healthcare analyst job postings (unverified).
**What the interviewer is checking:** That you can compute it and read a rising value as slower collection.
**Say this in the interview:** "Days in A/R is 60: it takes about two months on average to collect what we bill insurers. A rising number means slower payment, so cash is stuck."
**Explain simply:**
- **Accounts receivable:** money the hospital has billed but not yet received, like salary arrears owed to staff but in reverse.
- **Formula (my definition):** outstanding receivables / average daily billing. Daily billing = 3 crore / 30 = Rs 0.1 crore.
- **Rising means:** insurers or TPAs (third-party administrators who process claims for insurers) are paying slower, more claims are being queried or denied, or billing and documentation are slow. Check the ageing split (0-30, 31-60, 61-90, over 90 days) and the payer.
- **Why it matters:** cash flow and risk of write-offs. Definitions vary by organisation.
**Worked example:** 6 / (3 / 30) = 6 / 0.1 = 60 days. 1 crore = 10 million rupees, so units cancel.
**Likely follow-ups:** 1) *Is 60 good?* Compare with payment terms and past trend; there is no universal benchmark I can quote. 2) *Why use ageing?* One old bucket can hide behind an average.
**Common mistakes:** Mixing annual billing with a 30-day month; including cash patients in an insurer A/R; ignoring the ageing breakdown.

### Q40 ⭐⭐ 🟡 Calculate the clean claim (first-pass acceptance) rate and say what low values usually point to.
A billing team submitted 5,000 claims; 4,200 were accepted on first submission.
**Asked at:** commonly asked (no company-specific report found); revenue-cycle management (RCM) postings mention claim denials and rework (unverified).
**What the interviewer is checking:** The formula and an understanding of why claims fail.
**Say this in the interview:** "4,200 / 5,000 is 84% first-pass acceptance, so 16% needed rework. Low values usually point to documentation, coding, eligibility or process problems upstream."
**Explain simply:**
- **Claim:** the hospital's bill sent to the insurer or TPA for payment. A **clean claim** is accepted the first time without correction or query.
- **Why claims bounce:** missing or wrong patient or policy details, no pre-authorisation (the insurer's advance approval) where required, incorrect diagnosis or procedure codes, missing documents, late submission.
- **Use it:** break down rejections by reason code, payer and department, and fix the top few reasons.
- **Rejection vs denial:** definitions differ; a rejection may fail before processing, a denial after review. Say which you track.
**Worked example:** 4,200 / 5,000 = 84.0%. Not clean = 800 claims = 16.0%.
**Likely follow-ups:** 1) *Next metric?* Denial rate and the share eventually recovered after appeal. 2) *Who owns the fix?* Often front desk and clinical documentation, not just billing.
**Common mistakes:** Counting claims paid eventually as clean; not splitting by payer; reporting one blended figure.

### Q41 ⭐⭐ 🟡 Calculate payer mix and say why it matters for hospital revenue planning.
Monthly revenue of Rs 20 crore: cash-paying patients Rs 8 crore, private insurance Rs 7 crore, government schemes such as PM-JAY Rs 3 crore, corporate tie-ups Rs 2 crore.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute shares and link them to cash flow and risk.
**Say this in the interview:** "Cash is 40%, private insurance 35%, government schemes 15% and corporate 10%. The mix matters because each payer pays at different rates and speeds."
**Explain simply:**
- **Payer:** who pays the bill. **Payer mix** is each payer's share of revenue (or of patients, say which).
- **Why it matters:** cash is collected quickly; insurers pay slower and may deny part of a claim; government schemes such as PM-JAY (a government health insurance scheme, from memory, unverified) usually pay fixed package rates; corporate tie-ups often negotiate discounts. A shift toward one payer changes cash flow, margins and collection risk.
- **Use:** forecast cash, plan staffing for insurance desks, and see dependence risk. Revenue share is not profit share; look at margin by payer too.
**Worked example:** 8 / 20 = 40%; 7 / 20 = 35%; 3 / 20 = 15%; 2 / 20 = 10%. Total = 100% (8 + 7 + 3 + 2 = 20 crore).
**Likely follow-ups:** 1) *Revenue or patient mix?* Both; a payer may be 15% of revenue but 30% of patients. 2) *What if government share grows?* Check package-rate margins and payment delay.
**Common mistakes:** Shares not adding to 100%; confusing revenue share with profit; ignoring payment delay.

### Q42 ⭐⭐ 🟡 Calculate target achievement and year-on-year growth for a pharma sales territory and explain what else you would check.
Region target Rs 5 crore, achieved Rs 4.6 crore; same period last year Rs 4.0 crore.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct percentages and a habit of looking behind the headline.
**Say this in the interview:** "Achievement is 92% of target, a Rs 0.4 crore shortfall, and growth over last year is 15%."
**Explain simply:**
- **Target achievement** = achieved / target. **Year-on-year (YoY) growth** = (this year - last year) / last year, same period.
- **Both can be true:** the region missed its target yet grew, which suggests the target was ambitious.
- **Check next:** the split by brand and territory, primary versus secondary sales (primary is company to distributor, secondary is distributor to chemist), price versus volume, whether the target was fair, and one-off effects such as stock loading or a new product.
**Worked example:** 4.6 / 5.0 = 92.0%. Shortfall = 5.0 - 4.6 = 0.4 crore. Growth = (4.6 - 4.0) / 4.0 = 0.6 / 4.0 = 15.0%. Rounded to one decimal.
**Likely follow-ups:** 1) *Is 92% bad?* Depends on the typical spread; compare with other regions. 2) *Growth vs market growth?* If the market grew faster, share fell.
**Common mistakes:** Dividing growth by this year instead of last year; comparing different periods; ignoring price and volume.

### Q43 ⭐⭐ 🟡 What is MAT (moving annual total) in pharma sales reporting, why is it used, and what is MAT growth in the example below?
MAT value last year Rs 48 crore; MAT value this year Rs 54 crore.
**Asked at:** commonly asked (no company-specific report found); MAT appears in pharma sales-reporting prep material (unverified).
**What the interviewer is checking:** That you know the term and why it smooths noise.
**Say this in the interview:** "MAT is the total of the last 12 months, rolled forward each month. Growth here is 12.5%. It removes seasonality, so the comparison is fair."
**Explain simply:**
- **MAT (moving annual total):** sales for the latest 12 months. Each new month, add it and drop the same month a year ago.
- **Why:** pharma sales have seasonal peaks (for example flu or monsoon illnesses). Comparing one month with another is noisy; 12 months always contain all seasons. It is like using annual attrition instead of a single month's.
- **Limit:** it reacts slowly to recent changes, so also look at the latest quarter or month.
**Worked example:** (54 - 48) / 48 = 6 / 48 = 12.5% MAT growth (this MAT versus the same 12-month window a year earlier).
**Likely follow-ups:** 1) *Month-on-month?* Too noisy for brands with seasons. 2) *Why show both?* MAT shows the trend, the recent month shows momentum.
**Common mistakes:** Calling MAT a calendar-year total; mismatched windows; reading MAT growth as latest-month growth.

### Q44 ⭐⭐ 🟡 Calculate doctor coverage and call frequency for a field-force dashboard and explain what each shows.
An MR has 200 doctors on the call list; 170 were visited at least once in the month; total calls made were 510.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Two related field metrics and how they differ.
**Say this in the interview:** "Coverage is 85% (170 of 200 doctors seen at least once). Call frequency is 3.0 calls per visited doctor in the month."
**Explain simply:**
- **MR (medical representative):** the company's field person who visits doctors to present medicines. The **call list** is the doctors assigned to them.
- **Coverage** = doctors visited at least once / doctors on list. It shows reach: how many we touched.
- **Call frequency** = calls / doctors visited. It shows depth: how often. (Per listed doctor it would be 2.55, so state the base.)
- **Together:** high coverage with low frequency is shallow; a few doctors with many calls and low coverage is concentrated. Compare with targets by doctor tier (the most valuable doctors usually get more visits).
**Worked example:** 170 / 200 = 85.0%. 510 / 170 = 3.0. 510 / 200 = 2.55 per listed doctor. Not visited = 30 doctors (15.0%).
**Likely follow-ups:** 1) *Do more calls mean more sales?* Not necessarily; check call quality and doctor tier. 2) *How verified?* Reports from the field tool or app.
**Common mistakes:** Mixing the two denominators; counting calls as doctors; no tiering.

### Q45 ⭐⭐ 🟡 Primary sales in a pharma company jump at every quarter end. What could explain this, and what data would you compare to check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can separate real demand from sales pushed into the channel.
**Say this in the interview:** "It may be channel stuffing or target-driven loading at quarter end, not real demand. I would compare primary sales with secondary sales and stock at distributors."
**Explain simply:**
- **Primary sales:** company to its distributor or stockist. **Secondary sales:** distributor to chemist. **Tertiary:** chemist to patient (often available only from audits).
- **Possible reasons:** sales teams chasing quarterly targets and incentives, distributors given discounts or credit to buy more, scheme timing, or genuine seasonality or price-change announcements.
- **Check:** (1) primary versus secondary by month: if primary spikes but secondary stays flat, stock is piling up. (2) Distributor stock days (inventory / daily secondary sales). (3) Returns and credit notes after quarter start. (4) Scheme and discount calendar. (5) Prescription or market data as a demand signal.
- **Why it matters:** reported revenue may be pulled forward and reversed later.
**Data and tables involved:** `primary_invoices`, `secondary_sales`, `distributor_stock`, `returns_credit_notes`, `schemes`, `targets`; compare by month and distributor.
**Likely follow-ups:** 1) *Is it always wrong?* No; seasonality is legitimate, so compare with past years. 2) *Who decides action?* Sales and finance leadership; I give evidence.
**Common mistakes:** Accusing the team without data; ignoring returns after quarter end; looking only at primary.

### Q46 ⭐⭐ 🟡 What tables and fields would you need to build a pharma sales-force dashboard by territory and brand?
**Asked at:** commonly asked (no company-specific report found); a pharma sales-analyst posting is among the sources (unverified).
**What the interviewer is checking:** Whether you can design a simple star-style data model and know the key joins.
**Say this in the interview:** "I need a sales fact table at date, territory, brand and product level, plus targets, calls, and lookup tables for territory, brand and employee."
**Explain simply:**
- **Territory:** a geographic patch assigned to one MR, rolling up to area, region and zone.
- **Facts:** `secondary_sales` and `primary_sales` (date, territory_id, product_id, units, value); `targets` (month, territory, brand, target value); `call_activity` (date, MR, doctor, call count).
- **Dimensions:** `territory` (territory, area, region, zone), `product` (SKU, brand, therapy area, price), `employee` (MR id, grade, joining date, manager), `doctor` (id, speciality, tier), `calendar`.
- **Typical first cuts:** achievement versus target and YoY by territory and brand, coverage and frequency, and market share if market data exists.
- **Caution:** territories are reorganised, so keep effective dates; MR vacancies leave territories with no owner.
**Data and tables involved:** as listed; join on territory_id, product_id and a date key.
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team: doctor and employee details are personal data; limit access by role.
**Likely follow-ups:** 1) *Biggest data problem?* Territory mapping changes over time. 2) *Which date?* Invoice date for primary, recorded sale date for secondary; say so.
**Common mistakes:** One flat table with mixed grains; no effective dates; ignoring vacant territories.

### Q47 ⭐⭐ 🟡 Calculate the adverse event rate per treatment arm and explain why you must be careful in interpreting it.
Arm A: 12 of 60 patients reported at least one AE. Arm B: 6 of 60 patients reported at least one AE.
**Asked at:** commonly asked (no company-specific report found); clinical-data prep blogs cover adverse-event (AE) tables (unverified).
**What the interviewer is checking:** The calculation and statistical caution; this is analytics, not medical judgement.
**Say this in the interview:** "Arm A has 20% and Arm B has 10%, a 10 percentage point gap. With only 60 patients per arm that difference could be chance, so I would report it with context and leave interpretation to the clinical team."
**Explain simply:**
- **Adverse event (AE):** any unwanted medical event during a trial, not necessarily caused by the drug. **Arm:** a group of trial participants given one treatment.
- **Rate** = patients with at least one AE / patients in the arm (patients, not events).
- **Cautions:** small numbers; AE severity and seriousness differ; follow-up time may differ by arm; reporting can vary by site; the trial may be blinded, so access is restricted.
- **Plain statistics:** the gap is a 10 percentage-point difference, or a relative ratio of 2.0 (20% is twice 10%). A Fisher exact test (a test for small counts) gives p about 0.20, so the gap is not clearly beyond chance. Only a statistician or clinician should draw conclusions.
**Worked example:** Arm A: 12 / 60 = 20.0%. Arm B: 6 / 60 = 10.0%. Difference = 10.0 percentage points; ratio = 2.0. Fisher exact p = 0.20 (rounded to two decimals).
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the clinical/compliance team: trial data is sensitive, usually pseudonymised, and access follows the trial protocol and consent.
**Likely follow-ups:** 1) *Event count or patient count?* Patients with at least one AE; events counted separately. 2) *Is 20% vs 10% significant?* Not by this test with n = 60 each.
**Common mistakes:** Saying "double the risk" without noting the small sample; counting events instead of patients; giving medical conclusions.

### Q48 ⭐⭐ 🟡 Calculate the dropout rate in a trial and say how a dashboard should handle dropouts versus completers.
240 patients were enrolled; 36 left the study before completion.
**Asked at:** commonly asked (no company-specific report found); dropout and retention metrics appear in clinical-trial trade press (unverified).
**What the interviewer is checking:** The calculation and that you treat dropouts as information, not noise.
**Say this in the interview:** "36 of 240 is 15% dropout, so 204 completers or 85%. The dashboard should show both and the reasons, not just drop the leavers."
**Explain simply:**
- **Dropout:** an enrolled participant who leaves before the study ends. **Completer:** one who finishes.
- **Dashboard should show:** dropout rate overall and by site and arm, reasons (adverse event, consent withdrawn, lost to follow-up, moved), and timing (when they left).
- **Why it matters:** if one arm loses more patients, results among completers may be biased, so analysis teams usually also look at everyone who was enrolled. Treat that as a statistician's call.
- **HR parallel:** like analysing only the employees who stayed and ignoring those who left.
**Worked example:** 36 / 240 = 15.0% dropout. Completers = 240 - 36 = 204; 204 / 240 = 85.0%.
**Likely follow-ups:** 1) *Why by arm?* Unequal dropout can signal tolerability or bias. 2) *Rate against enrolled or randomised?* State the base; definitions differ.
**Common mistakes:** Showing completers only; no reasons; mixing screen failures with dropouts (screen failures never enrolled).

### Q49 ⭐⭐ 🟡 What basic data checks would you run on a hospital admission-discharge table before reporting any length-of-stay figure?
**Asked at:** commonly asked (no company-specific report found); healthcare analyst guides stress data validation before reporting (prep-site level, unverified).
**What the interviewer is checking:** Whether you clean data before quoting a number, and know what typically breaks in hospital records.
**Say this in the interview:** "Before any length-of-stay (LOS) number I check for missing discharge dates, discharge before admission, duplicate admissions, same-day cases, and patients still in hospital. Then I state how I handled each."
**Explain simply:**
- **LOS** is discharge date minus admission date, in days. **ALOS** is the average of that across patients.
- Patients still admitted have no discharge date. If you drop them, ALOS is understated (short stays leave first); if you count them to today, it is a different measure. Say which you chose.
- Same-day (day-case) patients can have LOS 0; decide whether they are in or out, and label it.
- Also check: transfers between wards that create several rows for one stay, a patient re-admitted the same day (one stay or two?), test patients, and extreme values (a 400-day stay is usually a data error or a long-stay case to review separately).
- HR parallel: like checking an attendance sheet for missing punch-outs and duplicate swipes before computing average hours.
**Worked example:** a tiny 7-row table (illustrative). One query counts the problems.
```sql
select sum(discharge_dt is null)           as missing_discharge,
       sum(discharge_dt < admit_dt)        as discharge_before_admit,
       sum(discharge_dt = admit_dt)        as same_day,
       count(*) - count(distinct adm_id)   as duplicate_ids
from admissions;
```
Output: 1, 1, 1, 1. Plain words: of 7 rows, one has no discharge, one is impossible, one is a day case and one admission ID is repeated, so only 4 rows are clean stays.
**Likely follow-ups:** 1) *Do you delete bad rows?* No, I log them, report the count and ask the owner to fix at source. 2) *Calendar days or hours?* Ask the hospital's definition; count nights or days consistently.
**Common mistakes:** Averaging with open stays silently dropped; mixing day cases with inpatients; deleting outliers without telling anyone.

### Q50 ⭐⭐ 🟡 Why is comparing ALOS across two hospitals or two doctors unfair without case mix, and how would you adjust in a simple way?
**Asked at:** commonly asked (no company-specific report found); ALOS is named in hospital KPI sources (vendor blogs, unverified).
**What the interviewer is checking:** That you understand "like for like" comparison and can compute an expected value.
**Say this in the interview:** "Different hospitals treat different mixes of patients, so a longer ALOS may just mean sicker or more complex cases. I compare actual ALOS with the ALOS expected for each hospital's own mix."
**Explain simply:**
- **Case mix** means the blend of conditions and severity a hospital treats. A hospital with many bypass surgeries will always show a longer average than one doing mostly minor procedures.
- Simple fix (called indirect standardisation): take a benchmark ALOS per case type (for example the all-hospital average), apply it to each hospital's own case counts to get an **expected** ALOS, then compare actual with expected.
- Group by diagnosis or procedure group, age band and admission type (emergency or planned). Small groups are noisy, so merge them.
- Same logic for doctors: a surgeon who takes referrals for hard cases looks "slow".
**Worked example:** benchmark: simple cases 3 days, complex 9 days. Hospital A: 80 simple, 20 complex. Hospital B: 20 simple, 80 complex. Actual ALOS: A 4.2, B 8.24.
- Raw: B is 4.04 days longer than A.
- Expected A = (80x3 + 20x9)/100 = 4.2; expected B = (20x3 + 80x9)/100 = 7.8.
- Actual / expected: A = 1.00; B = 8.24/7.8 = 1.056, about 5.6% above expectation (rounded to 1 decimal).
So most of B's gap is case mix; a small real excess remains.
**Likely follow-ups:** 1) *Better method?* Regression or standard risk-adjustment groups, but start simple. 2) *Where do you get severity?* Diagnosis and procedure codes, age, comorbidity flags.
**Common mistakes:** Ranking doctors on raw ALOS; benchmarks built from groups with a handful of cases.

### Q51 ⭐⭐ 🟡 What is a coding error or upcoding in healthcare data, and how can an analyst spot unusual patterns without accusing anyone?
**Asked at:** commonly asked (no company-specific report found); claims and revenue-cycle postings mention ICD-10/CPT coding (unverified).
**What the interviewer is checking:** Awareness of coding integrity and a professional, evidence-first tone.
**Say this in the interview:** "A coding error is a wrong code on a record. Upcoding is billing a more serious or expensive code than the care delivered. I would flag statistical outliers for the coding and compliance team to review, never label a person."
**Explain simply:**
- Hospitals convert diagnoses and procedures into **codes** (ICD-10 for diagnoses, other code sets for procedures; from memory, unverified). Codes drive billing, so wrong codes change money and statistics.
- Errors are often honest: wrong code picked, missing comorbidity, copy-paste notes. Upcoding is the intentional or careless pushing to a higher-paid code.
- Spot patterns: a doctor or ward whose share of high-severity codes is far above peers with similar patients; sudden jumps after a pricing change; very short stays billed at high severity; the same code for nearly every patient.
- Report as "this pattern differs from peers; reasons could be case mix, documentation or coding practice; please review", with the data and caveats.
**Regulation / privacy note (awareness only):** billing fraud rules exist in most countries; from memory, unverified, confirm with the compliance/legal team. Share patient-level detail only with authorised reviewers.
**Likely follow-ups:** 1) *How to compare fairly?* Against peers with similar case mix (Q50). 2) *Who gets the finding?* Compliance or the coding lead, not the doctor's manager directly.
**Common mistakes:** Calling an outlier "fraud"; ignoring case mix; sending patient lists widely.

### Q52 ⭐⭐ 🟡 In plain words, what do India's DPDP Act and the US HIPAA rule try to protect, and how do they affect an analyst who works with patient data?
**Asked at:** commonly asked (no company-specific report found); healthcare analyst guides stress governance and compliance (prep-site level, unverified).
**What the interviewer is checking:** That you respect patient privacy and know the basic habits, without playing lawyer.
**Say this in the interview:** "Both protect personal information: DPDP is India's general personal-data law, HIPAA is the US rule for health information held by healthcare organisations and their partners. As an analyst I use only the data I need, for the stated purpose, with access controls."
**Explain simply:**
- **DPDP Act** (Digital Personal Data Protection Act, India): consent and purpose-based handling of personal data, with duties on the organisations that decide why data is used. Details and enforcement dates: from memory, unverified.
- **HIPAA** (US): protects "protected health information" (health data tied to a person). It covers things like who may see it and how it is secured; specifics unverified.
- Effects on you: request minimum columns (no name or phone if not needed), work in approved systems only (no emailing patient files or personal laptops), do not copy data to personal tools, report any leak at once, and follow retention rules.
- Like payroll data in HR: salary details are shared on a need-to-know basis; patient data is even more sensitive.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team. This is not legal advice.
**Likely follow-ups:** 1) *Does it apply to you personally?* Your employer is responsible, but you must follow its policy. 2) *Practical habit?* Mask identifiers and aggregate early.
**Common mistakes:** Pasting patient rows into public AI or chat tools; thinking removing the name alone makes data safe.

### Q53 ⭐⭐ 🟡 Patient data was collected for treatment. A manager now wants to use it for marketing analytics. What concerns would you raise?
**Asked at:** commonly asked (no company-specific report found); secondary-use risk is a recurring theme in privacy guidance (unverified).
**What the interviewer is checking:** Whether you spot purpose limitation and escalate rather than just comply.
**Say this in the interview:** "The data was collected for care, so using it for marketing is a new purpose that may need fresh consent or a legal review. I would pause, raise it with compliance or the data protection officer, and offer a safer option such as aggregated or consented data."
**Explain simply:**
- **Purpose limitation** means data collected for one reason should not be reused for another unrelated one without a valid basis. Patients agreed to treatment, not to being targeted by offers.
- Concerns: consent; sensitivity (diagnosis can reveal a condition and cause distress or discrimination); trust and reputation; whether patients were told; who else would see it (agencies, vendors).
- Safer options: use only consented contacts, aggregate trends (visits by area and service), de-identified data (Q54), or general public-health messages.
- Be constructive: note the business goal and propose a compliant route.
**Regulation / privacy note (awareness only):** rules on secondary use and marketing differ by country and are tighter for health data; from memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *Manager insists?* Escalate in writing to compliance; do not proceed alone. 2) *What can you do meanwhile?* Aggregate, non-identifying analysis.
**Common mistakes:** Quietly doing it because "it's internal data"; refusing without offering alternatives.

### Q54 ⭐⭐ 🟡 What is the difference between anonymised, de-identified and pseudonymised data, and which one would you ask for when you only need trends?
**Asked at:** commonly asked (no company-specific report found); privacy concepts in healthcare analytics guides (unverified).
**What the interviewer is checking:** Correct vocabulary and the habit of asking for the least identifying data.
**Say this in the interview:** "Pseudonymised data swaps identifiers for codes but can be linked back; de-identified data has identifiers removed under a defined rule; anonymised data cannot reasonably be traced to a person. For trends I would ask for de-identified or aggregated data."
**Explain simply:**
- **Pseudonymised:** name replaced by a code (P8841); a separate key table can restore identity. Still treated as personal data in most regimes.
- **De-identified:** direct identifiers (name, phone, address, full dates, ID numbers) removed or generalised following a defined standard. HIPAA has a named method for this; DPDP has no health-specific standard yet (from memory, unverified).
- **Anonymised:** irreversibly cut off from the person; hard to prove, as rare combinations (age, pin code, rare disease) can re-identify someone.
- For trends (monthly admissions by department) I need counts, not people: ask for aggregates, or row-level data with age bands, month instead of date, and no names.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *Is a patient ID enough protection?* No, if linkable. 2) *Small groups?* Suppress or merge counts below a small threshold (often under 5 or so; policy varies).
**Common mistakes:** Calling pseudonymised data "anonymous"; leaving exact dates and pin codes in.

### Q55 ⭐⭐ 🟡 What does role-based access mean in a hospital reporting setting, and which of your reports would need restricted access?
**Asked at:** commonly asked (no company-specific report found); data governance is stressed in healthcare analyst guides (unverified).
**What the interviewer is checking:** That you design reports with the audience and sensitivity in mind.
**Say this in the interview:** "Role-based access means each person sees only the data their job needs: a ward nurse sees their ward, finance sees billing, the CEO sees summaries. Anything with patient identity or diagnosis, or staff pay and performance, needs restricted access."
**Explain simply:**
- Access is given by **role** (job type), not person by person, so when someone changes jobs the permissions change with the role.
- Open to many: aggregate dashboards (bed occupancy, ALOS, wait times by department).
- Restricted: patient-level lists with names or IDs, diagnosis detail (especially sensitive conditions), doctor-wise performance, denial lists by patient, nurse-wise attrition or pay.
- In Power BI or similar tools this is done with row-level security (users see only their rows) and separate workspaces; log who accessed what.
- HR parallel: managers see their team's leave, not everyone's salary.
**Regulation / privacy note (awareness only):** "minimum necessary" access is a common principle in health privacy rules; from memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *How do you test it?* Log in as sample roles and check nothing extra appears. 2) *Shared exports?* Avoid; share the dashboard link instead.
**Common mistakes:** One report for everyone with all columns; exporting to Excel and emailing.

### Q56 ⭐⭐ 🔴 The average length of stay rose from 4.2 to 5.1 days over three months. How would you investigate?
**Asked at:** commonly asked (no company-specific report found); ALOS is a core hospital KPI (vendor sources, unverified).
**What the interviewer is checking:** A structured breakdown: data first, then mix, then process.
**Say this in the interview:** "First confirm the data and definition did not change. Then split by case type, department, doctor, admission source and discharge day, to see whether it is a mix shift or a real slowdown in the process."
**Explain simply:**
- Step 1, data: new open stays, missing discharge dates, a changed rule for day cases, a new ward feeding in (Q49).
- Step 2, mix: did more complex cases arrive (more emergencies, older patients, a new specialty)? Compare ALOS within each case type.
- Step 3, process: discharge delays (pending tests, paperwork, insurance approval, no transport), weekend discharges, bed or staff shortages, a few extreme stays dragging the mean (check the median and top 10 longest stays).
- Step 4, report: split of the 0.9-day rise into mix and rate, plus a short list of actions for the operations team.
**Worked example:** two groups (illustrative): routine 3 days, complex 7 days. ALOS = 3 + 4 x (share complex).
- Before: 4.2 means complex share = (4.2 - 3)/4 = 30%.
- After: 5.1 means complex share = (5.1 - 3)/4 = 52.5%.
So with no slowdown inside either group, the rise from 4.2 to 5.1 can come entirely from mix; if within-group ALOS also rose, that part is a process issue.
**Likely follow-ups:** 1) *Which is the better KPI?* ALOS plus median and mix-adjusted view. 2) *Is longer always bad?* Not if cases are sicker; too short can mean readmissions.
**Common mistakes:** Jumping to "doctors are slow"; ignoring outliers and open stays.

### Q57 ⭐⭐ 🔴 Bed occupancy is 92 percent, yet revenue per occupied bed is falling. What would you check?
**Asked at:** commonly asked (no company-specific report found); ARPOB appears in hospital MIS prep material (blogs, figures unverified).
**What the interviewer is checking:** Whether you know occupancy measures volume, not value, and can break revenue per bed apart.
**Say this in the interview:** "Occupancy says beds are full, not what each bed earns. I would split revenue per occupied bed into patient mix, payer mix, pricing and discounts, length of stay and billing completeness."
**Explain simply:**
- **Bed occupancy** = occupied bed-days / available bed-days. **ARPOB** (average revenue per occupied bed per day) = revenue / occupied bed-days. Definitions vary (available vs staffed beds), so state yours.
- Likely causes: more low-priced cases (package-rate or government-scheme patients), longer stays of stable low-billing patients, fewer high-value surgeries, bigger discounts, delayed or missed billing, rising denials, more day-care in beds.
- Check by department, payer type, and procedure type; compare the same months last year.
**Worked example:** 100 beds, 90 days, 92% occupancy: occupied bed-days = 100 x 90 x 0.92 = 8,280. If revenue is ₹4.5 crore, ARPOB = ₹45,000,000 / 8,280 = about ₹5,435 per day (rounded).
Mix effect (illustrative): package patients earn ₹4,000 per day, others ₹7,000. At 40% package share ARPOB = 0.4x4,000 + 0.6x7,000 = ₹5,800; at 55% it is 0.55x4,000 + 0.45x7,000 = ₹5,350, a fall of 7.8% with occupancy unchanged.
**Likely follow-ups:** 1) *Is high occupancy then good?* Only if the right cases fill the beds. 2) *Cost side?* Add cost per occupied bed to see margin.
**Common mistakes:** Treating occupancy as profit; mixing outpatient revenue into a bed metric.

### Q58 ⭐⭐ 🔴 The claim denial rate rose from 8 percent to 14 percent in one quarter. How would you break this down and what would you report?
**Asked at:** commonly asked (no company-specific report found); denials and revenue-cycle analysis appear in US-healthcare analyst postings (unverified).
**What the interviewer is checking:** Segmented thinking, mix versus rate, and clear reporting of a 6-point rise.
**Say this in the interview:** "A denial is a claim the insurer refuses to pay. I would first define the rate, then split by insurer, denial reason, department, claim size and submission month to find where the 6 percentage points come from."
**Explain simply:**
- **Denial rate** = denied claims / claims submitted (by count or by value; state which, and which date it is tied to).
- Cuts: payer (insurer or TPA, the middleman that processes claims), reason code (missing documents, pre-authorisation not taken, coding error, ineligible cover), department, doctor, intake desk.
- Check timing: claims still pending look neither paid nor denied and can distort a quarter.
- Report: the rise in percentage points, the top two or three drivers, rupees at risk, what share is fixable (documentation, pre-auth), and actions with owners.
**Worked example:** 10,000 claims each quarter (illustrative).
| Payer | Q1 claims, rate | Q2 claims, rate |
|---|---|---|
| X | 5,000 at 4% | 3,000 at 4% |
| Y | 3,000 at 8% | 3,000 at 8% |
| Z | 2,000 at 18% | 4,000 at 26% |
- Q1 denied: 200+240+360 = 800 (8.0%). Q2: 120+240+1,040 = 1,400 (14.0%). Rise = 6.0 percentage points.
- Payer Z explains nearly all of it. Holding Z's Q1 rate (18%) with Q2 volumes gives 1,080 denials (10.8%): mix adds 2.8 points; Z's own rate rise adds 3.2 points.
**Likely follow-ups:** 1) *Percent or points?* 8% to 14% is +6 points, a 75% relative increase. 2) *First action?* Review Z's top denial reasons.
**Common mistakes:** Blending value and count rates; ignoring pending claims; blaming one team without the split.

### Q59 ⭐⭐ 🔴 A brand's sales fell in one region while the therapy market grew there. What cuts would you do and what data would you need?
**Asked at:** commonly asked (no company-specific report found); IQVIA candidate reports (anonymous, snippet-level, unverified) mention market-share and drug-sales driver cases.
**What the interviewer is checking:** Market share logic and an organised hunt for the cause.
**Say this in the interview:** "If the market grew and we fell, we lost share. I would cut by competitor, product pack, territory, doctor segment and channel, and check supply, pricing and field activity in that region."
**Explain simply:**
- **Therapy market** = all brands treating one condition (for example diabetes). **Market share** = our sales / market sales. **Primary sales** are our sales to distributors; **secondary sales** are distributors to chemists. Prescriptions show real demand.
- Cuts: share by competitor and by new launches; by city or territory; by doctor specialty and prescriber decile; by pack or strength; by channel; month trend.
- Internal factors: stock-outs, field-force vacancies or attrition in that region (an HR link: rep turnover), call frequency, promotion spend, price or discount changes, distributor issues.
- Data needed: third-party audit data (Q63), internal primary and secondary sales, call reports, stock and supply logs, price history, competitor activity.
**Likely follow-ups:** 1) *How to tell stocking from demand?* Compare primary and secondary sales; large gaps suggest channel stock build or shortage. 2) *Rule out?* One-off tender or reporting changes.
**Common mistakes:** Looking only at our own sales; mixing primary and secondary sales; ignoring territory vacancies.

### Q60 ⭐⭐ 🔴 A clinical trial site is far behind its enrollment target. What would you analyse and what would you tell the study team?
**Asked at:** commonly asked (no company-specific report found); one anecdotal Novartis Hyderabad report mentions clinical trials and drug pipeline topics (unverified).
**What the interviewer is checking:** Funnel thinking and practical, honest recommendations.
**Say this in the interview:** "I would compare the site's funnel (patients identified, screened, passed screening, enrolled) with other sites, find the weakest step, and project whether the target is still reachable at the current rate."
**Explain simply:**
- **Enrollment** = patients formally entered into the study. **Screening** = checking whether a patient qualifies; **screen failure** = fails the checks.
- Analyse: enrollment per month versus plan; funnel conversion per step; reasons for screen failure (criteria too strict?); referral sources; site staffing; time from consent to enrollment; dropouts.
- Compare with similar sites, using their own conversion rates.
- Tell the team: where patients are lost, whether to add outreach, extra staff, relax a protocol rule (only through proper approvals), or add other sites. Do not hide a problem.
**Worked example:** target 30 enrolled in 6 months (5 per month); after 4 months only 8 enrolled.
- Current rate = 8/4 = 2 per month. Needed: (30 - 8)/2 = 11 per month, 5.5 times the current rate.
- If 40% fail screening, reaching 30 needs 30/(1 - 0.4) = 50 screened.
**Likely follow-ups:** 1) *Extend the timeline?* Possible, but it costs time and money; compare against adding sites. 2) *Privacy?* Use site-level counts, not patient names.
**Common mistakes:** Judging by raw count without the funnel; ignoring screen-failure reasons.

### Q61 ⭐ 🟢 What is the difference between a generic drug, a branded generic and a biosimilar, and what is a patent cliff?
**Asked at:** commonly asked (no company-specific report found); basic pharma vocabulary.
**What the interviewer is checking:** Domain vocabulary in plain words.
**Say this in the interview:** "A generic is a copy of an off-patent drug sold by its chemical name; a branded generic is the same copy sold under a company brand name; a biosimilar is a close, not identical, copy of a biological drug. A patent cliff is the sharp sales drop when a blockbuster loses patent protection."
**Explain simply:**
- **Originator (innovator) drug:** the first company's patented product. A **patent** gives years of exclusivity.
- **Generic:** same active ingredient, strength and use; usually much cheaper. A **branded generic** carries a brand name and is promoted to doctors, common in India.
- **Biosimilar:** biologics are made in living cells, so copies cannot be exact; regulators require evidence of similarity (details unverified).
- **Patent cliff:** when patents expire, generics enter and the originator's sales and price fall fast. Analysts forecast it and track launch dates.
**Likely follow-ups:** 1) *Why does it matter to analysts?* Forecasts and share are re-based after generic entry. 2) *Same quality?* Regulators set standards; confirm specifics.
**Common mistakes:** Calling biosimilars "generics" interchangeably; thinking generics are lower quality by default.

### Q62 ⭐ 🟢 Why do most drug candidates never reach the market, and what does the drug pipeline funnel look like?
**Asked at:** commonly asked (no company-specific report found); one anecdotal Novartis Hyderabad report mentions clinical trials and drug pipeline (unverified).
**What the interviewer is checking:** That you understand the stages and attrition (drop-off) at each.
**Say this in the interview:** "Most candidates fail because they are not safe enough, do not work well enough, or are not worth the cost. The pipeline narrows from many early ideas to a few approved drugs."
**Explain simply:**
- Stages: discovery and lab testing; preclinical (animal and lab safety); Phase 1 (small group, safety); Phase 2 (patients, does it work and dose); Phase 3 (large trial against standard care); regulatory review; approval and launch.
- Each stage is a filter, so the funnel narrows sharply; exact success rates differ by source and disease, so I would quote none without a reference.
- Reasons for failure: toxicity, weak effect, poor dosing, trial cost, a competitor winning first.
- Analyst angle: track the count of candidates per phase, time spent in each phase, cost per phase, and failure reasons.
**Likely follow-ups:** 1) *Why is drug pricing high?* Failed attempts are paid for by the few successes (a common argument). 2) *Measure?* Phase-to-phase transition rate.
**Common mistakes:** Quoting precise success rates from memory; forgetting approval does not end monitoring after launch.

### Q63 ⭐ 🟢 What is IQVIA known for in the pharma world, and what kind of data do companies buy from audit firms?
**Asked at:** IQVIA analyst candidate reports (Glassdoor, AmbitionBox and others, anonymous, snippet-level) mention market-share, sales and promotion cases; unverified.
**What the interviewer is checking:** Whether you know where market data comes from.
**Say this in the interview:** "IQVIA is known as a major provider of healthcare market data, analytics and clinical-research services. Pharma firms buy audit data to see sales, prescriptions and market share across the whole market, not just their own."
**Explain simply:**
- Your own sales system shows only your brands. Competitors' numbers come from outside **audit firms**, which collect sales from chemists, distributors and prescription samples (methods and coverage unverified).
- Typical datasets: retail and hospital sales by product, pack, region and month; prescription counts by doctor specialty; market share and growth; sometimes promotion tracking.
- Used for market share, territory targeting, forecasting, and checking internal numbers.
- Caveats: samples are estimates and coverage varies; definitions (units vs value) must match your internal data.
- Privacy: prescriber-level data is sensitive; access is usually restricted (practice varies; confirm with compliance).
**Likely follow-ups:** 1) *Primary vs audit sales?* Primary is our shipments; audit is market view. 2) *MAT?* Moving annual total: last 12 months, which smooths seasonality.
**Common mistakes:** Treating audit numbers as exact; comparing units with value.

### Q64 ⭐ 🟢 Why is hospital demand seasonal, and how does that affect how you compare months?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Fair comparison over time.
**Say this in the interview:** "Demand moves with seasons: monsoon fevers, winter breathing problems, festival and holiday periods, planned surgeries timed around leave. So I compare a month with the same month last year, or use per-day rates and a seasonal index."
**Explain simply:**
- Causes (illustrative, vary by region): infections and vector-borne illness in rainy months, cold-weather respiratory cases, elective surgery dips around festivals, school-holiday scheduling.
- Month lengths differ too: 28 to 31 days, so use per-day figures.
- A **seasonal index** = month value / average month. Above 1 means a busier-than-average month.
- HR parallel: like attendance and leave patterns that rise before holidays; you would not compare December leave to March.
**Worked example:** admissions (illustrative) per month: Jan 620, Feb 600, Mar 640, Apr 680, May 700, Jun 760, Jul 820, Aug 840, Sep 780, Oct 700, Nov 650, Dec 640; average 702.5.
- Aug index = 840/702.5 = 1.20; Feb = 600/702.5 = 0.85 (2 decimals).
- Per day: Jan 620/31 = 20.0; Feb 600/28 = 21.4, so February is actually busier per day than January.
**Likely follow-ups:** 1) *How many years?* At least two to three to see the pattern. 2) *Alternative?* Compare with the same month last year (year on year).
**Common mistakes:** Month-on-month comparison without adjusting; reading one year's pattern as permanent.

### Q65 ⭐ 🟡 What are EDI 837 and 835 files in US healthcare billing, and how do they relate to claims analysis?
**Asked at:** commonly asked (no company-specific report found); EDI 837/835 appear in US healthcare revenue-cycle analyst job postings (unverified).
**What the interviewer is checking:** Whether you know which file is the bill and which is the payer's answer, so you can follow one claim end to end.
**Say this in the interview:** "An 837 is the electronic claim a provider sends to the insurer. An 835 is the electronic payment and remittance advice that comes back, showing what was paid, adjusted or denied. Claims analysis joins the two."
**Explain simply:**
- **EDI (electronic data interchange):** a fixed, standard text format that lets two computer systems swap business documents without people retyping them. Like a standard leave form that every department accepts.
- **837 (from memory, unverified):** the claim; carries patient, provider, diagnosis codes, procedure codes and billed amount.
- **835 (from memory, unverified):** the explanation of payment; carries paid amount, patient share, adjustment and denial reason codes.
- **Analyst use:** after the files are parsed into tables, match claim ID from the 837 to the 835 to compute denial rate, paid versus billed, and days from submission to payment.
**Likely follow-ups:** 1) *Why might one 837 match several 835 lines?* Payers can pay or adjust line by line, and in parts. 2) *Why is the match not always one to one?* Resubmissions, partial payments and reversals.
**Common mistakes:** Treating billed amount as revenue; ignoring that a claim can be resubmitted and appear twice.

### Q66 ⭐ 🟡 In plain words, what is the difference between CDISC SDTM and ADaM datasets in clinical trial reporting?
**Asked at:** commonly asked (no company-specific report found); SDTM/ADaM appear in clinical data prep blogs (unverified).
**What the interviewer is checking:** That you know raw-but-standardised data versus analysis-ready data.
**Say this in the interview:** "SDTM is the trial's collected data, organised into a standard layout by topic. ADaM is built from SDTM and shaped for the statistical analysis, with derived columns such as treatment group and change from baseline."
**Explain simply:**
- **CDISC:** a standards body that defines common formats for clinical trial data so regulators and companies read them the same way (from memory, unverified).
- **SDTM (study data tabulation model):** one table per topic (for example adverse events, lab results, demographics). Records what happened, little calculation. Like the raw attendance register.
- **ADaM (analysis data model):** analysis-ready tables, with flags and derived values so each result in the report traces back to a row. Like the monthly attendance summary built from the register.
- Traceability matters: a reviewer should be able to go from a reported number back to the raw record.
**Likely follow-ups:** 1) *Which comes first?* SDTM, then ADaM. 2) *Why standardise?* Regulators can review many submissions with the same tools.
**Common mistakes:** Thinking they are two names for the same thing; forgetting ADaM is derived, not collected.

### Q67 ⭐ 🟡 What does an audit trail mean in clinical data systems, and why do regulators care about it (GCP and 21 CFR Part 11 at awareness level)?
**Asked at:** commonly asked (no company-specific report found); GCP and Part 11 feature in clinical data management prep blogs (unverified).
**What the interviewer is checking:** Whether you understand that every data change must be traceable, not just correct.
**Say this in the interview:** "An audit trail is a time-stamped record of who changed which data, what the old and new values were, and why. Regulators want proof that trial data was not altered silently, so results can be trusted."
**Explain simply:**
- Like an HR system that logs who edited a salary field, when, and the reason; the old value is never erased.
- **GCP (good clinical practice):** an international quality standard for running trials ethically with reliable data (from memory, unverified).
- **21 CFR Part 11:** a US rule on electronic records and signatures, which expects secure, computer-generated audit trails (from memory, unverified).
- For an analyst: never overwrite source data; keep changes in a log with user, date and reason.
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team. Specific clauses and how they apply to your company are not covered here.
**Likely follow-ups:** 1) *Can an audit trail be edited?* It should not be. 2) *Does it help data cleaning?* Yes, queries and corrections are visible.
**Common mistakes:** Fixing data in a spreadsheet copy with no record; thinking the audit trail is only for fraud.

### Q68 ⭐ 🟡 What is HL7 or FHIR, and why would an analyst hear about them when hospital systems are integrated?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know how hospital systems exchange data and what that means for data quality.
**Say this in the interview:** "HL7 and FHIR are standard formats for sending health data between systems, such as registration, lab and billing. As an analyst I would hear about them because my data usually arrives through these feeds."
**Explain simply:**
- **HL7 (from memory, unverified):** an older message standard; systems send short coded messages such as 'patient admitted' or 'lab result ready'.
- **FHIR (from memory, unverified):** a newer, web-style standard that exposes items such as patient, observation or encounter that other apps can request.
- **Why it matters:** hospitals run separate systems (registration, lab, pharmacy, billing). A standard feed lets them agree on fields and codes.
- Analyst angle: missing messages, duplicate patient IDs and mismatched codes show up as data gaps in your report.
**Likely follow-ups:** 1) *Are you expected to code it?* Usually no; know what it is and ask engineers about feed delays. 2) *What breaks reports?* Late or dropped messages.
**Common mistakes:** Assuming a standard format guarantees clean data; skipping a reconciliation of counts between source and warehouse.

### Q69 ⭐ 🟡 What is real-world data (RWD) in healthcare, and what are its strengths and limits compared with trial data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can judge when everyday data can answer a question and when it misleads.
**Say this in the interview:** "RWD is data from normal care, such as hospital records, claims, pharmacy sales and registries. It shows many real patients over long periods, but it was not collected to answer my question, so it is messier and biased in ways a trial is not."
**Explain simply:**
- **Strengths:** large numbers, includes older or sicker patients that trials often exclude, shows how treatment is used in practice, and is cheaper.
- **Limits:** patients are not randomly assigned, so sicker patients may get one drug and the comparison is unfair (confounding); missing fields; coding inconsistent across hospitals; follow-up can be lost when patients move.
- **Trial data:** carefully collected and randomised, strong for cause and effect, but small, short and on selected patients.
- Neither replaces the other; they answer different questions.
**Regulation / privacy note (awareness only):** Patient-level RWD needs consent or a lawful basis and de-identification; rules differ by country (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Can RWD prove a drug works?* It can suggest, but bias makes proof hard. 2) *Example source?* Claims or EMR records.
**Common mistakes:** Reading a difference between two groups as the drug's effect; ignoring missing data.

### Q70 ⭐ 🟡 What is pharmacovigilance, and why does safety data live in a separate database from the trial database?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand safety monitoring as a continuous, regulated duty separate from study analysis.
**Say this in the interview:** "Pharmacovigilance is watching for side effects of medicines, during trials and after launch. Safety reports must be handled fast and from many sources, so they sit in a dedicated safety system rather than only in the trial database."
**Explain simply:**
- **Adverse event:** any unwanted medical event after taking a medicine, whether or not the medicine caused it. A **serious** one (for example hospitalisation) has tight reporting timelines to regulators (from memory, unverified).
- **Why separate:** reports arrive after launch from doctors, patients and literature, not only from trial sites; the system supports coding, causality review, duplicate checks and regulatory submissions.
- **Trial database:** built for one study's analysis; the **safety database** covers the product across all sources and studies.
- The two are periodically reconciled so serious events match, a routine data check.
**Likely follow-ups:** 1) *What is reconciliation?* Matching serious events across both systems. 2) *Who uses safety data?* Safety physicians and regulatory teams, not marketing.
**Common mistakes:** Assuming every adverse event was caused by the drug; counting duplicate reports as separate cases.

### Q71 ⭐ 🟡 A report shows a rare-disease group with only 2 patients in a ward-and-age cell. What should you do before sharing it?
**Asked at:** commonly asked (no company-specific report found); gap-fill question on small numbers and privacy.
**What the interviewer is checking:** That you notice a person could be identified from a tiny group.
**Say this in the interview:** "I would not share it as is. A cell of two in a rare disease can point to real individuals, so I would combine categories or hide small cells, and check who the audience is and what access they have."
**Explain simply:**
- Few patients plus ward plus age plus a rare diagnosis: colleagues may guess who they are. Like publishing 'the only two employees on long medical leave in one small team'.
- **Options:** merge age bands or wards; show 'fewer than 5' instead of the number; drop the cut; or limit the report to an approved viewer.
- Also guard against hiding a number in one cell that can be worked out from totals (subtract known cells from the total).
- The threshold (such as 5 or 10) is a local policy choice; ask the privacy or compliance owner.
**Regulation / privacy note (awareness only):** Principle: share the minimum needed for the purpose. India's DPDP Act and other laws may apply to health data (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Is removing the name enough?* No, combined details can still identify. 2) *What threshold?* Follow policy.
**Common mistakes:** Suppressing one cell but leaving the total that reveals it; sharing the report widely first and asking later.

### Q72 ⭐ 🟡 Calculate the hospital pharmacy wastage percentage and say what you would investigate.
Average pharmacy stock value is Rs 50 lakh; stock worth Rs 1.5 lakh expired and was written off in the month.
**Asked at:** commonly asked (no company-specific report found); gap-fill calculation.
**What the interviewer is checking:** That you can compute a simple ratio and ask why money was lost.
**Say this in the interview:** "Wastage is 1.5 divided by 50, which is 3 percent of average stock value in the month. I would then look at which items expired and why."
**Explain simply:**
- **Expiry write-off:** medicines kept past their use-by date and removed from stock; the hospital loses their cost.
- **Average stock value:** the typical value held during the month, so one month-end spike does not distort the ratio.
- Definitions vary; some hospitals divide by purchases or sales instead. I use average stock.
**Worked example:** Wastage % = 1.5 lakh / 50 lakh x 100 = 3.0 percent (computed; 3.0% exactly, so no rounding). Same unit (Rs lakh) in both parts.
**Data and tables involved:** Stock register (item, batch, expiry date, quantity, cost), purchase orders, issue and sales records, supplier returns. First cuts: wastage by item, by supplier, by batch age at receipt, by ward store versus main store.
**What I would investigate:** a few high-cost items versus many small ones; items bought in large lots with slow use; short-expiry stock received; poor first-expiry-first-out; demand forecasts; whether returns to supplier were possible.
**Likely follow-ups:** 1) *Is 3% good?* Needs a benchmark from the hospital's own history. 2) *Month or year?* Track monthly and rolling.
**Common mistakes:** Using total purchases as the base without saying so; ignoring that the percentage hides a few expensive items.

### Q73 ⭐ 🟡 What is case mix index (CMI) and how does it change how you read ALOS and revenue per patient?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you adjust hospital metrics for how complex the patients are.
**Say this in the interview:** "CMI is the average complexity weight of the patients treated. A hospital with a high CMI treats sicker patients, so longer stays and higher revenue per patient are expected and shouldn't be read as inefficiency or better performance by themselves."
**Explain simply:**
- **CMI (case mix index):** each case gets a weight for expected resource use (for example by diagnosis group); CMI is the average weight. Weights are defined by the system in use (from memory, unverified).
- **ALOS (average length of stay):** total inpatient days divided by discharges.
- Comparing ALOS across hospitals or units without CMI is like comparing average processing time of two HR teams when one handles complex disputes.
- A simple adjustment: ALOS divided by CMI, or compare within the same case type.
**Worked example (invented figures):** Cardiac unit ALOS 6.0 days, CMI 2.0; general unit ALOS 3.0 days, CMI 1.0. Adjusted ALOS: 6.0 / 2.0 = 3.0 and 3.0 / 1.0 = 3.0 days per unit of complexity. Cardiac looks twice as slow, but after adjustment they are equal.
**Likely follow-ups:** 1) *Does CMI change revenue per patient?* Yes, the same logic: higher CMI, higher expected revenue. 2) *Where do weights come from?* A grouping scheme.
**Common mistakes:** Ranking units on raw ALOS; treating the adjustment as exact.

### Q74 ⭐ 🟡 Which metrics would you track for a telemedicine or online pharmacy service, beyond number of consultations or orders?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you look at repeat use, quality and fulfilment, not volume only.
**Say this in the interview:** "Volume can grow while quality drops, so I would add repeat rate, completion and fulfilment measures, wait times, and safety or complaint signals."
**Explain simply:**
- **Demand side:** new versus repeat users, repeat within 30 days, cost to acquire a user.
- **Telemedicine:** time to first available doctor, consult completion rate (started versus finished), follow-up booked, patient rating, prescription issued rate.
- **Online pharmacy:** order fulfilment rate, delivery time, substitution and cancellation rate, return and refill rate, share of orders with a valid prescription where required.
- **Money:** revenue per active user, discounts used, cost per order.
- **Quality and risk:** complaints, escalations, adverse-event reports.
**Likely follow-ups:** 1) *Which one first?* Repeat rate, it shows value. 2) *Need a denominator?* Yes, always state it.
**Common mistakes:** Reporting totals only; mixing app downloads with active users.

### Q75 ⭐ 🟡 How would you measure doctor productivity in an OPD, and what would be unfair about ranking doctors on a single number?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you build a fair, multi-measure view and avoid blame on one number.
**Say this in the interview:** "I would use several measures such as patients seen per session, consultation time and follow-up rate, and compare doctors only within the same speciality. One number rewards speed over quality and hides case mix."
**Explain simply:**
- **OPD (outpatient department):** patients who come, see the doctor and leave the same day.
- **Measures:** patients per clinic hour, utilisation of booked slots, waiting time, no-show rate, share of new versus review cases, patient feedback, revenue per consultation.
- **Why a single number is unfair:** specialities differ; a doctor with complex cases takes longer; clinic days and support staff differ; some doctors teach or see referrals.
- Use it for conversation and resource planning, not punishment. Same care you would take ranking HR recruiters on offers closed alone.
**Likely follow-ups:** 1) *Fair comparison?* Within speciality and similar case mix. 2) *Include quality?* Yes, repeat visits and feedback.
**Common mistakes:** Ranking by patient count; ignoring that some visits are procedures.

### Q76 ⭐ 🟡 What share of sales do the top 20 percent of brands give in the example below, and what would you do with a Pareto finding like this?
Example: a company has 50 brands; the top 10 brands give Rs 72 crore of Rs 90 crore total sales.
**Asked at:** commonly asked (no company-specific report found); sales-concentration questions are common in pharma sales analysis (unverified).
**What the interviewer is checking:** Simple share arithmetic and a sensible business action.
**Say this in the interview:** "Top 20 percent of 50 brands is 10 brands. They give 72 of 90 crore, which is 80 percent of sales, so a classic Pareto split."
**Explain simply:**
- **Pareto (80/20 rule):** a small group often gives most of the result. It is an observation, not a law.
- Action: protect and invest in the top brands, review the long tail (prune, bundle, or give less field effort), and check concentration risk if one brand is a large part of the top.
**Worked example:** Top 20% of 50 brands = 10 brands. Share = 72 / 90 = 0.80 = 80.0 percent. The other 40 brands give 90 - 72 = Rs 18 crore, 20.0 percent. Average per top brand = Rs 7.2 crore; average per tail brand = Rs 0.45 crore, so a top brand sells 16 times a tail brand on average.
**Likely follow-ups:** 1) *Should you cut the tail?* Not blindly; some are new or strategic. 2) *What next?* Look at growth, margin and trend of each.
**Common mistakes:** Mixing up percent of brands and percent of sales; assuming exactly 80/20 always holds.

### Q77 ⭐ 🔴 Outline how you would size the market for a new cancer drug in India, and what data sources you would use.
**Asked at:** an oral cancer drug market-sizing case is reported on anonymous candidate pages for IQVIA (snippet only, unverified); otherwise commonly asked.
**What the interviewer is checking:** A structured funnel, clear assumptions and sensible sources.
**Say this in the interview:** "I would go from the number of patients to the number actually treated with this drug, then multiply by price and treatment duration. I would state each assumption and test it against sales data."
**Explain simply:**
- **Funnel:** cases per year for the cancer type, then the share eligible by stage or biomarker, then the share diagnosed and reaching treatment, then the share who would get this drug (versus existing options), then months of therapy, then price per month.
- **Sources:** cancer registries and published incidence estimates, hospital and treatment guidelines, pharma sales audit data for competitor drugs, expert interviews with oncologists, price lists (all to be verified).
- **Cross-check:** top down (patients) versus bottom up (sales of similar drugs, number of centres x patients per centre).
- Give a range: low, base, high.
**Worked example (all figures invented):** 100,000 new cases x 40% eligible = 40,000; x 70% diagnosed and treated = 28,000; x 50% choose this drug = 14,000 patients. Multiply by months on treatment and price per month to get value.
**Likely follow-ups:** 1) *Biggest uncertainty?* Treated share and drug uptake. 2) *Out-of-pocket versus insurance?* Affects who can pay.
**Common mistakes:** Using total cases as the market; one number, no range.

### Q78 ⭐ 🔴 A hospital group wants to reduce 30-day readmissions. What analysis would you propose, and how would you avoid blaming individual doctors?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Definitions, risk adjustment and system thinking.
**Say this in the interview:** "I would first fix the definition, then find which patient groups and processes drive readmissions, adjusting for how sick patients are. I would look at systems such as discharge and follow-up, and compare doctors only with fair adjustment."
**Explain simply:**
- **30-day readmission:** a patient returns as an inpatient within 30 days of discharge. Definitions differ (all cause versus related, planned versus unplanned); I state mine.
- Steps: build index admission and next admission from patient ID and dates; compute rate by diagnosis, ward, age, day of discharge, length of stay, payer.
- Drivers: weak discharge planning, missing follow-up, medicine issues, early discharge.
- To avoid blame: adjust for case mix, show confidence ranges for small volumes, report at unit and pathway level, and use findings for process fixes.
**Data and tables involved:** Admissions (patient ID, admit and discharge date, diagnosis, ward, doctor, discharge type), billing, lab and pharmacy records. Beware missing readmissions at other hospitals.
**Regulation / privacy note (awareness only):** Patient-level data should be used only by authorised people for the stated purpose (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Excluded cases?* Deaths and planned returns, such as chemotherapy cycles. 2) *Next step?* Pilot a fix and compare.
**Common mistakes:** Counting planned returns; ranking doctors on tiny samples.

### Q79 ⭐ 🔴 Design a monthly management report for a hospital CEO using only data you can get from billing, admission and lab systems. What goes on page one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Choosing a few decision-ready metrics from available data.
**Say this in the interview:** "Page one is one screen of six to eight headline numbers with trend and target, plus three or four lines on what changed and what needs a decision. Detail goes behind it."
**Explain simply:**
- **Page one, from admission data:** admissions, bed occupancy, ALOS, discharges before noon.
- **From billing:** revenue, ARPOB (average revenue per occupied bed per day), payer mix, claim denials or pending bills.
- **From lab:** test volume and turnaround time (order to result).
- Each metric: this month, last month, same month last year (hospital demand is seasonal), and target.
- **Pages behind:** by department, by payer, outliers and a definitions page.
- Be honest about what these systems cannot show: patient outcomes, satisfaction, staff data.
**Likely follow-ups:** 1) *How to avoid clutter?* Few metrics, red and green flags. 2) *Who validates numbers?* Finance and department heads.
**Common mistakes:** Too many metrics; no definitions or comparison period; mixing booked bed counts with staffed beds.
