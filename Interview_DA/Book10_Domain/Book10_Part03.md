# Book 10 — Domain Knowledge | Part 3: BFSI (Banking, Credit, Fintech, Insurance, Capital Markets, Risk) 🟢🟡🔴

**Target:** 100 questions | **Actual:** 113 questions
**Scope:** banking, credit and lending, collections, fintech and UPI, insurance, capital-markets basics, risk, KYC and fraud, and regulation and data privacy in plain words (awareness level only, no legal or financial advice).

### Q1 ⭐⭐⭐ 🟢 How does a bank make money? Explain interest income and non-interest (fee) income in plain words.
**Asked at:** commonly asked (no company-specific report found); "how does a bank earn" is a staple of BFSI fresher guides (unverified).
**What the interviewer is checking:** Whether you understand the basic business model before touching bank data.
**Say this in the interview:** "A bank borrows money cheaply from depositors and lends it at a higher rate; the gap is interest income. It also charges fees for services, which is non-interest income."
**Explain simply:**
- **Interest income:** money earned on loans and investments. Think of it as rent on money. If a bank pays 3% on savings and charges 10% on a loan, the 7-point gap is its spread.
- **Non-interest (fee) income:** processing fees on loans, card and ATM charges, account fees, insurance and mutual-fund commissions, foreign-exchange and trading gains.
- **Costs against this:** interest paid to depositors, salaries and rent (the bank's HR bill is a big cost), and money set aside for loans that may go bad (provisions, meaning a cushion held back as an expected loss).
- Profit is roughly interest income + fee income - interest paid - operating costs - provisions.
**Likely follow-ups:** 1) *Which is more stable?* Interest income is usually the bigger and steadier part; fees vary with activity. 2) *What is the spread called as a metric?* Net interest margin (see Q18).
**Common mistakes:** Forgetting that deposits are a cost to the bank (it pays interest on them); thinking fees are the main income for a typical lender.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a bank, an NBFC and a fintech app, and what can each of them do with your money?
**Asked at:** commonly asked (no company-specific report found); fintech loops reportedly stress understanding who holds the licence (unverified).
**What the interviewer is checking:** That you know who is regulated to do what, because that decides what data exists and who owns it.
**Say this in the interview:** "A bank takes deposits and lends. An NBFC (non-banking finance company) lends but generally cannot take ordinary savings deposits. A fintech app is usually a technology front end that works with a licensed bank or NBFC."
**Explain simply:**
- **Bank:** licensed to accept deposits (savings, current, fixed) and lend; it also runs payments. Deposits are the cheap raw material.
- **NBFC:** lends, finances vehicles, gold, small business and so on, but funds itself from banks, bonds and investors rather than from savings accounts (from memory, unverified; exact permissions vary by NBFC type, confirm with compliance).
- **Fintech app:** the app you tap. It may be a lender's sales channel, a payment app, or a broker's front end. The money usually sits with the partner bank or NBFC, not the app itself.
- For an analyst: the same customer can appear in three systems (app, partner NBFC, bank), so IDs and reconciliation matter.
**Likely follow-ups:** 1) *Can an NBFC issue a cheque book?* Generally no, as it is not a deposit-taking bank account (from memory, unverified). 2) *Who bears the loan loss in a fintech partnership?* Depends on the contract; ask.
**Common mistakes:** Saying fintech apps always lend their own money; treating NBFC as just a small bank.

### Q3 ⭐⭐⭐ 🟢 What is an NPA (non-performing asset), and after how many days of non-payment does a loan usually become one?
**Asked at:** commonly asked (no company-specific report found); NPA is named in most BFSI prep guides (unverified).
**What the interviewer is checking:** Core vocabulary and whether you know the 90-day idea.
**Say this in the interview:** "An NPA is a loan where the borrower has stopped paying. In India a loan generally turns NPA when interest or instalments stay overdue for more than 90 days (from memory, unverified; confirm the current rule with the risk team)."
**Explain simply:**
- A loan is an **asset** for the bank, because the borrower owes it money. "Non-performing" means it has stopped earning.
- The counter starts from the first missed due date. Day 91 of continuous non-payment is the usual tipping point for term loans; some products, such as agricultural loans, follow different seasonal rules (from memory, unverified).
- After NPA, the bank must stop counting the unpaid interest as income and set aside provisions (money held back against likely loss).
- HR analogy: like an employee absent without notice for 90 days; at some point the record has to be reclassified.
**Likely follow-ups:** 1) *What is "SMA"?* An early-warning label before NPA, for accounts 1-90 days overdue (from memory, unverified). 2) *Is an NPA the same as a write-off?* No, see Q40.
**Common mistakes:** Quoting 30 or 60 days; saying the borrower must be missing all payments (a single overdue amount can start the count).

### Q4 ⭐⭐⭐ 🟢 What are CASA deposits, and why does a bank want a high CASA share?
**Asked at:** commonly asked (no company-specific report found); CASA appears in banking-ratio guides (unverified).
**What the interviewer is checking:** Whether you connect a ratio to bank profit.
**Say this in the interview:** "CASA means Current Account and Savings Account money. It is the cheapest funding a bank has, so a higher CASA share means a lower cost of funds."
**Explain simply:**
- **Current account:** used by businesses; usually pays no interest.
- **Savings account:** individuals; pays a low interest rate.
- **Term (fixed) deposits** pay higher rates because the money is locked in, so they cost the bank more.
- CASA share = (current + savings balances) / total deposits. High CASA = cheap, sticky funding, and a better margin on the same loans.
- Salary accounts matter here: an employer's payroll file brings in steady savings balances. That is why banks chase corporate salary tie-ups.
**Likely follow-ups:** 1) *Is CASA always good?* It is balances that can leave quickly, so banks also watch stability. 2) *What affects it?* Interest-rate gaps; when fixed deposits pay much more, people move money out of savings.
**Common mistakes:** Calling CASA a loan product; forgetting it is a share of deposits, not of total balance sheet.

### Q5 ⭐⭐⭐ 🟢 What is KYC, and why must banks and fintech apps do it before opening an account or giving a loan?
**Asked at:** commonly asked (no company-specific report found); KYC/AML analyst question lists exist (unverified).
**What the interviewer is checking:** That you know KYC is a legal duty and a data source, not just a form.
**Say this in the interview:** "KYC means Know Your Customer: confirming who the person is and where they live before doing business. It is required to prevent fraud, money laundering and misuse of accounts."
**Explain simply:**
- Typical steps: collect identity and address proof, verify them (document check, face match, OTP-based or video checks), then store the result.
- Why: criminals open accounts under false names to move illegal money; lenders also need a real person to chase for repayment.
- In India the rules come from the RBI and the anti-money-laundering law (PMLA); specifics such as accepted documents and re-KYC cycles are from memory, unverified, confirm with the compliance team.
- Data angle: KYC creates the customer master (name, ID numbers, address), which every other table joins to. Bad KYC data breaks everything downstream (see Q23).
**Likely follow-ups:** 1) *What is re-KYC?* Periodic refresh of details. 2) *Full KYC vs minimal KYC?* Lower-verification accounts get tighter limits (from memory, unverified).
**Common mistakes:** Treating KYC as a one-time sales formality; ignoring that KYC data is itself sensitive (see Q22).

### Q6 ⭐⭐⭐ 🟢 What is DPD (days past due), and how are delinquency buckets such as 0, 1-30, 31-60, 61-90 and 90+ used in reports?
**Asked at:** commonly asked (no company-specific report found); collections-analytics job listings mention DPD distribution (unverified).
**What the interviewer is checking:** Whether you can read a delinquency report.
**Say this in the interview:** "DPD is the number of days since a due payment was missed. Buckets group loans by how late they are, so we can see how many are healthy and how many are sliding toward NPA."
**Explain simply:**
- Example: EMI due 5 March, unpaid on 20 March, so DPD = 15, bucket 1-30.
- **0 (current):** paid on time. **1-30:** mildly late, often forgetfulness. **31-60 and 61-90:** real trouble, collections effort rises. **90+:** usually NPA territory (Q3).
- Reports show count and balance by bucket, month by month. A shift from 1-30 into 31-60 is an early warning.
- When an overdue amount is paid, DPD resets, so the same loan can move back.
**Likely follow-ups:** 1) *Is the bucket on count or amount?* Show both; a few big loans can distort amount. 2) *How do you track movement?* Roll rates (not asked here; see the roll-rate question later in this part).
**Common mistakes:** Measuring DPD from the loan start rather than the due date; mixing buckets on a different cut-off date.

### Q7 ⭐⭐⭐ 🟢 Name the main retail loan products (home, personal, auto, two-wheeler, gold, credit card) and say how their risks differ.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know risk follows security, size and customer type.
**Say this in the interview:** "Secured loans have an asset behind them, so losses are lower; unsecured loans and cards have nothing to recover, so lenders charge more and expect more losses."
**Explain simply:**
- **Home loan:** large, long (15-30 years), secured by the house. Low default rate, slow to recover if it fails.
- **Auto and two-wheeler:** secured by the vehicle, which loses value quickly; two-wheeler borrowers are often first-time, lower-income customers, so default rates tend to be higher than car loans (a general pattern, unverified).
- **Gold loan:** short, secured by gold, which is easy to value and sell. Risk is falling gold price.
- **Personal loan:** unsecured, quick, higher rate, higher default risk.
- **Credit card:** revolving, unsecured; the customer can borrow, repay and borrow again. Risk and interest rates are highest.
- Dashboards should compare products on delinquency and recovery separately, never in one blended number.
**Likely follow-ups:** 1) *Which has the highest ticket size?* Home loans. 2) *Which is most data-rich for scoring?* Cards and personal loans, as behaviour is visible.
**Common mistakes:** Saying secured means no risk; blending products into one NPA figure.

### Q8 ⭐⭐⭐ 🟢 What is UPI, and which parties are involved when one person pays another through a UPI app?
**Asked at:** commonly asked (no company-specific report found); fintech guides say to learn UPI structure (unverified).
**What the interviewer is checking:** Whether you understand a payment as a chain with several data owners.
**Say this in the interview:** "UPI is an instant, bank-to-bank payment system run by NPCI. The app only sends the instruction; the money moves between the two banks."
**Explain simply:**
- **Payer and payee:** the two people, each with a UPI ID linked to a bank account.
- **PSP app (payment service provider app):** the app on the phone, such as a payment or bank app, with a sponsor bank behind it (from memory, unverified).
- **Payer's bank (remitter):** checks PIN and balance, debits the account.
- **Payee's bank (beneficiary):** receives and credits.
- **NPCI (National Payments Corporation of India):** runs the switch that routes the message and settles between banks.
- A failed payment can fail at any of these steps, so failure analysis needs each party's response code.
**Likely follow-ups:** 1) *Where does a payment get "stuck"?* Often when one bank's response is delayed. 2) *Why do apps not earn fees?* Merchant fees are largely not charged on UPI (policy position changes; from memory, unverified).
**Common mistakes:** Believing the app holds the money; leaving NPCI out.

### Q9 ⭐⭐⭐ 🟢 What are credit risk, market risk and operational risk? Give one everyday example of each.
**Asked at:** commonly asked (no company-specific report found); risk-analytics guides list these three (unverified).
**What the interviewer is checking:** Whether you can separate the main risk families.
**Say this in the interview:** "Credit risk is a borrower not repaying; market risk is losses from price or rate moves; operational risk is losses from broken processes, people, systems or fraud."
**Explain simply:**
- **Credit risk:** a customer stops paying a personal loan.
- **Market risk:** a bank holds government bonds; interest rates rise and the bonds lose value.
- **Operational risk:** a payroll or payment file is processed twice by mistake, or an employee misuses access.
- HR link: operational risk includes people issues (staff errors, internal fraud, weak access control).
- Each has its own data: loan tables, price and rate data, incident and loss logs.
**Likely follow-ups:** 1) *Which is the largest for a retail lender?* Usually credit risk. 2) *Is fraud credit or operational?* Often operational, though loan-application fraud shows up as credit loss.
**Common mistakes:** Calling every loss "credit risk"; forgetting the third family.

### Q10 ⭐⭐⭐ 🟢 What do PD, LGD and EAD mean in plain words, and how do they combine into expected loss?
**Asked at:** commonly asked (no company-specific report found); PD/LGD/EAD appear in most credit-risk guides (unverified).
**What the interviewer is checking:** Whether you can state and multiply the three.
**Say this in the interview:** "PD is the chance the borrower defaults, LGD is the share of the exposure lost if they do, and EAD is the amount owed at that time. Expected loss = PD x LGD x EAD."
**Explain simply:**
- **PD (probability of default):** for example 2% over the next year.
- **LGD (loss given default):** after selling collateral and collecting, how much is lost; 45% means 55% is recovered.
- **EAD (exposure at default):** the outstanding amount when default occurs.
**Worked example:** invented inputs: PD 2% (0.02), LGD 45% (0.45), EAD Rs 10,00,000. Expected loss = 0.02 x 0.45 x 10,00,000 = Rs 9,000 (computed by code). Banks use such figures to size provisions; this is awareness only, not a lending recommendation.
**Likely follow-ups:** 1) *Is expected loss the worst case?* No, it is the average; unexpected loss needs capital. 2) *What lowers LGD?* Better collateral.
**Common mistakes:** Mixing LGD as a Rupee amount (it is a percentage); using the original loan amount instead of the amount outstanding.

### Q11 ⭐⭐⭐ 🟢 What is a credit score (for example a CIBIL score), what data feeds it, and how do lenders use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can describe a score as a summary of behaviour, with care about privacy.
**Say this in the interview:** "A credit score is a three-digit number from a credit bureau that summarises a person's repayment history; lenders use it to decide approval and pricing."
**Explain simply:**
- **Bureau:** a company that collects loan and card repayment data from lenders (CIBIL is one in India). Range is commonly quoted as 300-900 (from memory, unverified).
- **Data feeding it:** repayment history, amount of credit used against limits, number of loans and recent enquiries, age of credit accounts, and mix of secured and unsecured loans.
- **Use:** auto-approve above a cut-off, refer the middle band for manual checks, decline or price higher below it. It is one input, not the whole decision.
- Customers have consent and access rights over their credit data (from memory, unverified).
**Likely follow-ups:** 1) *Why does applying for many loans hurt?* Many enquiries signal credit hunger. 2) *Is a thin file bad?* Not bad, just unknown.
**Common mistakes:** Saying the score includes income or salary; treating it as a guarantee.

### Q12 ⭐⭐⭐ 🟢 What is the difference between life insurance and general insurance? Explain premium, sum assured and claim.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic insurance vocabulary.
**Say this in the interview:** "Life insurance pays on death or maturity of a policy; general insurance covers losses such as health, motor or fire, usually for one year at a time."
**Explain simply:**
- **Premium:** the price the customer pays for cover (monthly or yearly).
- **Sum assured:** the amount the insurer promises to pay if the insured event happens (for life) or the maximum cover (general uses "sum insured").
- **Claim:** the request to be paid after the event; the insurer checks and then settles or rejects it.
- **Life:** long-term (10-30 years), payout is for death or survival.
- **General:** short-term, renewed yearly, pays actual loss (hospital bill, car repair).
- Regulator in India is IRDAI (from memory, unverified).
**Likely follow-ups:** 1) *Is health insurance life or general?* General, by usual classification. 2) *Why track renewals?* Because insurers earn from continuing customers.
**Common mistakes:** Using sum assured and premium interchangeably; assuming a claim is always paid.

### Q13 ⭐⭐⭐ 🟢 What is the difference between gross NPA and net NPA?
**Asked at:** commonly asked (no company-specific report found); GNPA/NNPA are named in banking-ratio guides (unverified).
**What the interviewer is checking:** Whether you see that net accounts for the cushion already set aside.
**Say this in the interview:** "Gross NPA is all bad loans; net NPA is gross NPA minus the provisions the bank has already set aside against them, so it shows the loss still uncovered."
**Explain simply:**
- Gross NPA ratio = gross NPAs / gross advances.
- Net NPA ratio = (gross NPAs - provisions) / (gross advances - provisions). Exact formulas differ slightly between sources; the question's definition is used in Q15.
- Simple picture: Rs 1,500 crore of bad loans; the bank has already put Rs 900 crore aside. Net bad loans = Rs 600 crore.
- A bank with high gross but strong provisions can look safer on a net basis.
**Likely follow-ups:** 1) *Which is higher?* Gross is always at least net. 2) *What is the provision coverage ratio?* Provisions / gross NPAs (60% in Q15).
**Common mistakes:** Treating net NPA as "after recoveries"; subtracting provisions from the numerator only and forgetting the denominator.

### Q14 ⭐⭐⭐ 🟢 What are the common types of fraud in banking and fintech (card fraud, account takeover, loan application fraud, first-party fraud)?
**Asked at:** commonly asked (no company-specific report found); fraud analytics appears in fintech and insurer guides (unverified).
**What the interviewer is checking:** Whether you can tell who the fraudster is in each case.
**Say this in the interview:** "The key split is who commits it: a stranger using stolen details (card fraud, account takeover), a stranger faking an identity to get a loan (application fraud), or the real customer deceiving the lender (first-party fraud)."
**Explain simply:**
- **Card fraud:** stolen card details used online or in a shop; the true owner disputes the charge.
- **Account takeover:** a criminal gains control of a real account (stolen password, OTP, SIM swap) and moves money out.
- **Loan application fraud:** fake or stolen documents, synthetic identities, inflated income.
- **First-party fraud:** the real customer borrows with no intention to repay, or falsely claims a payment was not theirs.
- Signals for analysts: new device, many applications from one phone number, sudden address change, fast withdrawals after a login change.
**Likely follow-ups:** 1) *Which is hardest to spot?* First-party fraud, because it looks like normal default. 2) *How measure it?* Fraud loss as a share of volume (basis points).
**Common mistakes:** Treating all defaults as fraud; blocking too aggressively and hurting real customers.

### Q15 ⭐⭐⭐ 🟡 Calculate gross NPA % and net NPA % and explain what each tells a manager.
Data (Rs crore): gross advances 50,000; gross NPAs 1,500; provisions held against those NPAs 900. (Net NPA ratio uses net advances = gross advances minus provisions.)
**Asked at:** commonly asked (no company-specific report found); GNPA/NNPA appear in ratio guides (unverified).
**What the interviewer is checking:** Whether you apply the stated formula correctly and read the result.
**Say this in the interview:** "Gross NPA is 3.0% and net NPA is about 1.22%. Gross shows how much of the book has gone bad; net shows how much is still uncovered after provisions."
**Explain simply:**
- Gross NPA % = 1,500 / 50,000 = 3.00%.
- Net NPAs = 1,500 - 900 = 600. Net advances = 50,000 - 900 = 49,100.
- Net NPA % = 600 / 49,100 = 1.22% (rounded to 2 decimals).
- Provision coverage = 900 / 1,500 = 60%.
- **Manager reading:** asset quality problem is 3% of loans; 60% of it already cushioned, so the remaining hit to profit is smaller.
**Worked example:** all figures above computed by code. Note that other definitions (for example net NPA / gross advances = 1.20%) exist; always state which you use.
**Likely follow-ups:** 1) *If provisions rise?* Net NPA falls but profit falls too, since provisions are a cost. 2) *Percent or points?* A move from 3.0% to 2.5% is a 0.5 percentage-point fall.
**Common mistakes:** Using 600/50,000; forgetting net advances; mixing crore and lakh.

### Q16 ⭐⭐⭐ 🟡 Calculate collection efficiency two ways (current demand only, and including arrears) and say which one the collections head should watch.
Data (Rs crore, one month): EMIs falling due this month (current demand) 120; collected against current demand 108; arrears from earlier months collected 6.
**Asked at:** commonly asked (no company-specific report found); collection efficiency is listed among collections KPIs in job listings and prep guides (unverified).
**What the interviewer is checking:** Whether you notice that adding arrears to the numerator flatters the number.
**Say this in the interview:** "Current-demand efficiency is 90%. Including arrears it is 95%. I would watch the 90%, because it shows whether this month's customers are paying on time."
**Explain simply:**
- Current-demand efficiency = 108 / 120 = 90.0%.
- Including arrears = (108 + 6) / 120 = 114 / 120 = 95.0%.
- The second divides by only this month's demand while its numerator includes old money, so it blends two groups. That is a common company convention, but definitions differ; state yours.
- The 5-point gap is purely recovery of old dues; useful, but it can hide a fresh slide. A strong recovery month can even exceed 100%.
- The collections head should watch both: 90% for fresh slippage, the arrears recovery separately.
**Worked example:** computed by code; percentages rounded to one decimal.
**Likely follow-ups:** 1) *What if 108 dropped to 100?* Current-demand efficiency would be 83.3%, a warning. 2) *Count or amount?* Track both.
**Common mistakes:** Reporting the flattering number only; counting prepayments as collections.

### Q17 ⭐⭐⭐ 🟡 An insurer has the figures below. Calculate the loss ratio, expense ratio and combined ratio, and say whether it made an underwriting profit.
Data (Rs crore): earned premium 200; claims incurred 150; expenses (commission plus operating cost) 56. Use expense ratio = expenses divided by earned premium.
**Asked at:** commonly asked (no company-specific report found); the combined ratio is a staple of insurance interview guides (unverified).
**What the interviewer is checking:** Whether you read 100% as the break-even line.
**Say this in the interview:** "Loss ratio is 75%, expense ratio is 28%, combined ratio is 103%. Above 100% means an underwriting loss of Rs 6 crore."
**Explain simply:**
- **Earned premium:** the part of premiums that relates to cover already provided.
- Loss ratio = 150 / 200 = 75.0%. Expense ratio = 56 / 200 = 28.0%.
- Combined ratio = 75% + 28% = 103.0%.
- Underwriting result = 200 - 150 - 56 = -6, a loss of Rs 6 crore (3% of earned premium).
- The insurer may still be profitable overall if it earns enough investment income on premiums it holds before paying claims. This is about the underwriting side only.
**Worked example:** computed by code; the underwriting loss equals (103% - 100%) of 200 = Rs 6 crore.
**Likely follow-ups:** 1) *What fixes it?* Better pricing, lower claims through fraud checks, lower expenses. 2) *Percentage or points?* A change from 103% to 99% is 4 percentage points.
**Common mistakes:** Using written instead of earned premium; calling a 103% combined ratio a profit.

### Q18 ⭐⭐⭐ 🟡 A bank's figures are below. Calculate net interest income and net interest margin (NIM) and explain what NIM means.
Data (Rs crore, one year): interest earned 9,000; interest paid on deposits and borrowings 5,400; average interest-earning assets 1,20,000.
**Asked at:** commonly asked (no company-specific report found); NIM appears in investor-education and prep-site ratio lists (unverified).
**What the interviewer is checking:** Whether you know the bank's basic profit engine and can compute a ratio on an average base.
**Say this in the interview:** "Net interest income is interest earned minus interest paid: 3,600 crore. NIM divides that by average interest-earning assets, so it is 3.0%. It tells me how much the bank keeps per rupee it has put to work."
**Explain simply:**
- **Interest-earning assets** are things that pay the bank interest: mainly loans, plus bonds and balances placed with other banks. A branch building or cash in the vault earns nothing, so it is excluded.
- **Net interest income (NII)** = interest earned minus interest paid to depositors and lenders. It is the bank's "spread income".
- **NIM** = NII / average interest-earning assets. We use the average of the year because the balance sheet grows or shrinks during the year.
- HR comparison: it is like revenue per employee, but for money: how much margin each rupee of working money produced.
**Worked example:**
- NII = 9,000 - 5,400 = 3,600 crore.
- NIM = 3,600 / 1,20,000 = 0.03 = 3.00% (shown to two decimals).
- Definitions differ slightly across banks (some use total assets as the base); I state mine.
**Likely follow-ups:** 1) *What lowers NIM?* Deposits getting costlier faster than loans reprice, or more money sitting in low-yield assets. 2) *Is higher always better?* Not if it comes from lending to very risky borrowers who may default.
**Common mistakes:** Dividing by total assets without saying so; using year-end instead of average assets; treating NII and net profit as the same thing.

### Q19 ⭐⭐⭐ 🟡 Which tables and fields would you need to build a loan portfolio health dashboard, and what first cuts would you show?
**Asked at:** commonly asked (no company-specific report found); portfolio segmentation and early-warning reporting appear in BFSI analyst job listings (unverified).
**What the interviewer is checking:** Whether you can think in terms of tables, keys and grain, and know which cuts a risk or collections manager actually wants.
**Say this in the interview:** "I would start from a monthly loan snapshot table with outstanding balance and days past due, join it to the loan master and customer master for product, branch and segment, and add a repayment table. First cuts: balance by product, DPD bucket distribution, and early delinquency by month of disbursal."
**Explain simply:**
- A **portfolio** is simply all the loans the lender currently has on its books. "Health" means how many are being repaid on time.
- **DPD (days past due)** is the number of days a payment is overdue; 0 means on time.
**Data and tables involved:**
- **Loan master:** loan_id, customer_id, product, branch, channel, disbursal date, sanctioned amount, interest rate, tenure, secured flag.
- **Monthly loan snapshot:** loan_id, month-end date, outstanding principal, DPD, bucket, status. One row per loan per month; this is the grain most metrics need.
- **Repayment / demand table:** loan_id, due date, amount due, amount paid, paid date (for collection efficiency).
- **Customer master:** customer_id, age band, city, income band, score band (masked of direct identifiers).
- **First cuts:** (1) total outstanding by product and branch; (2) share of balance in each DPD bucket (0, 1-30, 31-60, 61-90, 90+) as a trend; (3) gross NPA % by product; (4) collection efficiency by month; (5) early delinquency by disbursal month (vintage); (6) roll rates between buckets.
- Before anything, reconcile the total outstanding to the finance team's figure.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance team: customer-level dashboards should use masked or coded IDs and role-based access.
**Likely follow-ups:** 1) *Why a snapshot table?* Without month-end history you cannot see movement between buckets. 2) *What is your first check?* Row count and total balance against finance.
**Common mistakes:** Showing only today's balance with no trend; mixing loan-level and customer-level grain so customers are double counted; averaging percentages across products.

### Q20 ⭐⭐⭐ 🟡 Calculate the roll rate, cure rate and stay rate for the 30-DPD bucket and say what a rising roll rate warns about.
Data: accounts in the 1-30 DPD bucket at month start 2,000. At month end: 500 moved to the 31-60 bucket, 900 paid up and became current, 600 stayed in 1-30.
**Asked at:** commonly asked (no company-specific report found); roll rate and cure rate appear in collections KPI guides (unverified).
**What the interviewer is checking:** Whether you divide by the right starting base and understand that the three rates describe where the same accounts went.
**Say this in the interview:** "Out of 2,000 accounts, 25% rolled worse, 45% cured, and 30% stayed. They add to 100% because they are the same starting group."
**Explain simply:**
- **Roll rate:** share of accounts that move to a worse bucket (here 1-30 to 31-60).
- **Cure rate:** share that return to current (0 DPD) after paying.
- **Stay rate:** share that remain in the same bucket.
- Think of an HR parallel: of 2,000 employees on a late-attendance warning last month, how many got worse, how many fixed it, how many stayed the same.
- A **rising roll rate** warns that fewer late payers are recovering and more slide toward NPA (non-performing asset, a loan unpaid for long enough, commonly 90 days). It is an early warning before the NPA number moves.
**Worked example:** Roll = 500/2,000 = 25.0%; cure = 900/2,000 = 45.0%; stay = 600/2,000 = 30.0%; total 100%. The base is the month-start count for all three.
**Likely follow-ups:** 1) *If roll rate went from 25% to 30%?* A 5 percentage-point rise; check which product, branch or channel drives it. 2) *Why not count by amount?* You can; compare both count-based and balance-based.
**Common mistakes:** Dividing by month-end accounts; ignoring new accounts that entered the bucket during the month; saying "5% rise" when it is 5 percentage points.

### Q21 ⭐⭐⭐ 🟡 A lender approves 4,000 of 10,000 applications and disburses 3,200 of them. Calculate the approval rate and the application-to-disbursal rate, and name two reasons approved customers do not take the loan.
Data: applications 10,000; approved 4,000; disbursed 3,200.
**Asked at:** commonly asked (no company-specific report found); funnel metrics are common in fintech analytics prep (unverified).
**What the interviewer is checking:** Whether you pick the right denominator for each rate.
**Say this in the interview:** "Approval rate is 40%. Application-to-disbursal is 32%. Of approved customers, 80% took the loan, so 800 approved applicants dropped off."
**Explain simply:**
- **Approval rate** = approved / applications = 4,000/10,000 = 40%.
- **Application-to-disbursal** = disbursed / applications = 3,200/10,000 = 32%.
- **Approved-to-disbursed** = 3,200/4,000 = 80%; the 800 lost are approved customers the lender worked to win.
- Two reasons approved customers do not take the loan: they found a cheaper rate or better offer elsewhere; or the final steps (documents, e-mandate set-up, verification, app friction) were not completed. Other reasons: the need passed, or the approved amount was lower than asked.
**Likely follow-ups:** 1) *Where would you look first?* The 800 drop: split by channel, offer amount, and days from approval to drop. 2) *Is a higher approval rate good?* Only alongside the later default rate.
**Common mistakes:** Dividing disbursed by approved and calling it the conversion of the whole funnel; ignoring rejected cases that could not be recovered.

### Q22 ⭐⭐⭐ 🟡 Why is customer data such as Aadhaar, PAN, account number and phone number sensitive, and how should an analyst handle it in files and dashboards? Answer at awareness level in plain words.
**Asked at:** commonly asked (no company-specific report found); data privacy of customer data is a standard BFSI expectation (unverified).
**What the interviewer is checking:** Whether you treat customer data with care and know simple safe habits.
**Say this in the interview:** "These identifiers can be used to impersonate someone or reach their money, so I only use what I need, mask the rest, and never share raw files outside approved systems."
**Explain simply:**
- **Aadhaar** (India's 12-digit national ID) and **PAN** (permanent account number used for tax) tie a person to government and financial records. An account number plus a phone number can help a fraudster impersonate someone or trick them into sharing a one-time password.
- Leaked data is hard to take back; the customer can be harmed and the company can face penalties and loss of trust.
- Safe habits: ask whether you need the field at all (often an anonymous customer code is enough); mask it (show last 4 characters only) or replace with a coded ID; share aggregates, not rows; keep files in approved shared drives, not personal email or pen drives; limit access to those who need it; do not paste real data into public tools.
- HR parallel: you would not circulate a sheet with employees' salaries and bank accounts to everyone.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: India has a data protection law (the DPDP Act) and Aadhaar-specific rules limiting how it may be stored and displayed. I would follow the company's data policy rather than my own reading.
**Likely follow-ups:** 1) *Is masking the same as anonymising?* No; masked data can sometimes be traced back by combining fields. 2) *What if a manager asks for the raw file?* Confirm the purpose and approval path first.
**Common mistakes:** Leaving PAN or phone columns in a dashboard extract "just in case"; emailing files to personal accounts; thinking hidden columns in Excel are removed.

### Q23 ⭐⭐⭐ 🟡 What data-quality problems usually appear in KYC and customer master data (duplicate customers, mismatched names, missing fields), and how would you check for them?
**Asked at:** commonly asked (no company-specific report found); data quality in KYC/AML roles is mentioned in job listings (unverified).
**What the interviewer is checking:** Whether you can turn "messy data" into specific checks you can run.
**Say this in the interview:** "I check uniqueness, completeness, consistency and validity: the same person twice, blanks in mandatory fields, names that differ between documents, and impossible formats."
**Explain simply:**
- **KYC (know your customer)** is the identity and address check a bank must complete before dealing with a customer. The **customer master** is the central table of customers.
- Typical problems: the same person with two customer IDs; spelling and initials differences ("Ravi Kumar" vs "Ravi K"); missing PAN or date of birth; one phone number shared across unrelated customers; invalid PAN format; expired KYC documents; address changed in one system only.
- A short check (SQL on a sample table, which flagged one repeated PAN, one missing PAN and one missing date of birth):
```sql
-- PAN numbers that appear on more than one customer record
select pan, count(*) as records_with_this_pan
from customers
where pan is not null
group by pan
having count(*) > 1;
```
Output: `ABCDE1234F | 2`. Plain words: two customer IDs share one PAN, so they are probable duplicates to review, not to delete automatically.
- Other checks: count of blanks per mandatory column; phone used by more than one distinct name; PAN format pattern (5 letters, 4 digits, 1 letter, from memory); name similarity between customer master and KYC record.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance team: KYC records carry sensitive identifiers, so run checks inside approved systems and report counts, not raw IDs.
**Likely follow-ups:** 1) *Do you delete duplicates?* No; flag them, and let the data owner merge. 2) *How do you measure improvement?* Duplicate rate and mandatory-field completeness month on month.
**Common mistakes:** Treating the same name as proof of duplicate (different people share names); deleting records without owner approval; ignoring case and spacing differences.

### Q24 ⭐⭐⭐ 🟡 Calculate the cost-to-income ratio and say whether lower or higher is better and why.
Data (Rs crore, one year): operating expenses 4,200; net interest income 6,000; other (fee and treasury) income 1,500. Use operating income = net interest income plus other income.
**Asked at:** commonly asked (no company-specific report found); cost-to-income is in banking ratio lists (unverified).
**What the interviewer is checking:** Whether you know the formula and which direction means efficiency.
**Say this in the interview:** "Operating income is 7,500 crore, so cost-to-income is 56%. Lower is better: the bank spends 56 paise to earn each rupee of income."
**Explain simply:**
- **Operating expenses** are running costs: salaries, rent, technology, branch costs (staff cost is usually the biggest, which is why HR data matters here).
- **Operating income** = net interest income + other income (fees, treasury gains).
- A lower ratio means more of each rupee of income is left to cover loan losses and make profit.
**Worked example:** Operating income = 6,000 + 1,500 = 7,500. Ratio = 4,200 / 7,500 = 0.56 = 56.0%. Left over before provisions: 3,300 crore (44%).
**Likely follow-ups:** 1) *Can a bank be too low?* Yes, if it under-invests in technology or staff. 2) *What if income drops?* The ratio rises even if costs are unchanged.
**Common mistakes:** Using total income including interest paid; calling higher "better because bigger"; forgetting the definition varies by bank.

### Q25 ⭐⭐⭐ 🟡 Calculate the CASA ratio and explain how a falling CASA ratio would affect the bank's profit.
Data (Rs crore): current account deposits 20,000; savings account deposits 60,000; term (fixed) deposits 70,000.
**Asked at:** commonly asked (no company-specific report found); CASA appears in investor-education ratio lists (unverified).
**What the interviewer is checking:** Whether you can compute the share and link it to cost of funds.
**Say this in the interview:** "CASA is current plus savings divided by total deposits: 80,000 / 1,50,000, which is 53.3%. If it falls, the bank replaces cheap money with costlier term deposits and its margin shrinks."
**Explain simply:**
- **CASA** = current account and savings account deposits. Current accounts usually pay no interest and savings pay a low rate; term deposits pay more.
- Total deposits = 20,000 + 60,000 + 70,000 = 1,50,000.
- **Illustration with invented rates:** assume savings and current money costs 3% on average and term deposits 6.5%. If 10,000 crore moves from CASA to term deposits, CASA falls from 53.3% to 46.7% and interest cost rises by 10,000 x (6.5% - 3%) = 350 crore a year, unless lending rates also rise.
- Salary accounts are a major source of CASA, which links to the HR teams of corporate customers.
**Worked example:** CASA = 80,000/1,50,000 = 53.33%; after the shift, 70,000/1,50,000 = 46.67%, a fall of 6.67 percentage points.
**Likely follow-ups:** 1) *Does a higher CASA always mean more profit?* It lowers funding cost, but the bank must lend the money well. 2) *Why might CASA fall?* Customers move savings to higher-rate options.
**Common mistakes:** Dividing by CASA instead of total deposits; including term deposits in the numerator; stating the effect without a number.

### Q26 ⭐⭐⭐ 🟡 A transaction-monitoring system raises alerts for possible money laundering. Calculate the precision before and after a rule change and say what you would check before accepting the change.
Data: before, 1,000 alerts in a month of which 40 were confirmed suspicious on review. After the rule change, 600 alerts of which 36 were confirmed suspicious. (Assume the same 40 truly suspicious cases existed in both months.)
**Asked at:** commonly asked (no company-specific report found); false-positive reduction and threshold tuning appear in AML analyst prep material (unverified).
**What the interviewer is checking:** Whether you see that better precision can hide missed cases (lower recall).
**Say this in the interview:** "Precision rose from 4% to 6%, but recall fell from 100% to 90%: we lost 4 genuine cases. I would not accept the change until we understand those 4."
**Explain simply:**
- **Money laundering** is disguising illegally earned money as clean money; banks monitor transactions and raise **alerts** for human review.
- **Precision** = confirmed suspicious / alerts raised. It shows how much reviewer time is wasted on false alarms.
- **Recall** = confirmed suspicious caught / all truly suspicious (40). It shows how many bad cases the system finds.
- Alert volume fell 40% (1,000 to 600), which saves review effort.
**Worked example:** Before: 40/1,000 = 4.0%. After: 36/600 = 6.0% (up 2 percentage points). Recall before 40/40 = 100%; after 36/40 = 90%. Missed: 4.
**What I would check:** what the 4 missed cases looked like (a pattern?); whether this is one month only; test on past data before go-live; whether the regulator or compliance head must approve rule changes (from memory, unverified, confirm with compliance).
**Likely follow-ups:** 1) *Is missing 4 acceptable?* That is a compliance decision, not an analyst one. 2) *How else to cut false alerts?* Better segmentation of customers.
**Common mistakes:** Celebrating precision alone; assuming 40 "true" cases is the full truth (some may never be found).

### Q27 ⭐⭐⭐ 🟡 Calculate the claim settlement ratio two ways and explain why this single number can mislead a customer comparing insurers.
Data (health insurer, one year): claims received 12,000; settled (paid) 10,200; rejected 900; still pending 900.
**Asked at:** commonly asked (no company-specific report found); CSR and its limits are discussed in insurance news and prep pages (unverified).
**What the interviewer is checking:** Whether you handle the denominator and pending claims honestly.
**Say this in the interview:** "Settled over received is 85%. Settled over claims that were decided (settled plus rejected) is 91.9%. The definition changes the answer, so I compare insurers only on the same definition."
**Explain simply:**
- A **claim** is a customer's request to the insurer to pay for a covered loss; **settled** means paid.
- Way 1: 10,200/12,000 = 85.0% (pending counted as not settled).
- Way 2: 10,200/(10,200+900) = 91.89%, about 91.9% (only decided claims).
- Why misleading: it is a company-wide average (not per product or per age group); it ignores the amount paid versus claimed, the time taken, partial payments, and pending cases; different insurers may use different denominators. Rejection reasons (for example waiting periods) matter to a customer.
- Rates: pending 7.5%, rejected 7.5%, settled 85%.
**Likely follow-ups:** 1) *What else would you compare?* Settlement time, amount-based ratio, complaints. 2) *What if pending is large at year-end?* Way 2 flatters the insurer.
**Common mistakes:** Not saying which denominator; reporting a rounded 92%; picking the insurer with the highest number alone.

### Q28 ⭐⭐⭐ 🟡 Explain the 13th-month persistency ratio of a life insurer and calculate it from the data.
Data: 10,000 policies were issued in April 2025. At the 13th month (first renewal due), 8,200 of them are still in force (premium paid).
**Asked at:** commonly asked (no company-specific report found); persistency checkpoints appear in insurer explainers (unverified).
**What the interviewer is checking:** Whether you understand it as a retention measure of one cohort.
**Say this in the interview:** "It is the share of policies from one issue cohort that are still active and paid at the first renewal: 8,200 of 10,000, so 82%."
**Explain simply:**
- **Premium** is the regular payment that keeps the policy active. If a customer stops paying, the policy **lapses**.
- **Persistency** is retention for policies: like the one-year retention rate for new joiners in HR.
- 13th month is the first renewal; insurers also track later checkpoints (25th, 37th, from memory, unverified). Definitions (count-based or premium-based) differ across insurers.
- Low persistency may signal mis-selling (customer did not understand the product) or affordability problems.
**Worked example:** 8,200/10,000 = 82.0%; lapsed = 1,800 (18.0%).
**Likely follow-ups:** 1) *Cuts?* Channel, product, premium size, agent. 2) *Count or premium?* Both; premium-weighted can differ.
**Common mistakes:** Using policies due in a different month as base; mixing cohorts; confusing with claim ratio.

### Q29 ⭐⭐⭐ 🟡 What is a vintage (cohort) analysis for loans, and which of the two cohorts below is performing worse?
Data: January 2025 cohort: 1,000 loans, 20 were 30+ DPD at month-on-book 3 (MOB 3). February 2025 cohort: 1,000 loans, 35 were 30+ DPD at month-on-book 3 (MOB 3).
**Asked at:** commonly asked (no company-specific report found); vintage analysis appears in credit-risk prep material (unverified).
**What the interviewer is checking:** Whether you compare groups at the same age.
**Say this in the interview:** "A vintage groups loans by the month they were disbursed and tracks them at equal age. At MOB 3, February is 3.5% against January's 2.0%, so February is worse."
**Explain simply:**
- **MOB (months on book)** is how many months since the loan started. Comparing at the same MOB is fair; comparing today's snapshot is not, because older loans have had longer to go wrong.
- Gap: 1.5 percentage points, or 75% higher in relative terms.
- With only 1,000 loans each, 20 versus 35 is suggestive, not proof; a quick test gives about p = 0.055 (borderline). I would watch MOB 6 and the next cohorts, and check whether the Feb mix (channel, product, score) changed.
**Worked example:** Jan 20/1,000 = 2.0%; Feb 35/1,000 = 3.5%.
**Likely follow-ups:** 1) *Why might Feb be worse?* A looser cut-off, a new channel, a campaign. 2) *Next step?* Split by channel and score band.
**Common mistakes:** Comparing at different MOBs; calling the gap "1.5%" instead of 1.5 points; over-reading small numbers.

### Q30 ⭐⭐⭐ 🟡 In plain words, what does the RBI do, and why should a bank analyst know that regulatory reporting formats and definitions exist?
**Asked at:** commonly asked (no company-specific report found); regulatory risk reporting appears in BFSI job listings (unverified).
**What the interviewer is checking:** Awareness that bank numbers follow official definitions.
**Say this in the interview:** "The RBI is India's central bank and banking regulator. It sets rules, and banks must report to it in prescribed formats, so my internal numbers must match those definitions."
**Explain simply:**
- From memory, unverified: the RBI issues currency, runs monetary policy (such as the repo rate), supervises banks and NBFCs, and oversees payment systems.
- Regulatory returns define terms like NPA and capital ratios exactly. If my dashboard defines NPA differently, it will not reconcile.
- So I would ask for the official definition, the reporting calendar, and who signs off.
- Awareness only; confirm details with the compliance team.
**Likely follow-ups:** 1) *What if internal and regulatory numbers differ?* Document the reconciliation. 2) *Who owns it?* Finance/compliance.
**Common mistakes:** Inventing a definition; quoting circular numbers as certain.

### Q31 ⭐⭐ 🟢 What is the difference between NEFT, RTGS, IMPS and UPI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic payments literacy.
**Say this in the interview:** "All four move money between bank accounts; they differ in speed, amount, timing and how you initiate."
**Explain simply (from memory, unverified):**
- **NEFT:** batch-based transfers, suitable for ordinary amounts.
- **RTGS:** real-time, intended for large-value payments, with a minimum amount.
- **IMPS:** instant, round the clock, using account number or mobile.
- **UPI:** instant, uses a virtual payment address or QR code, run by NPCI.
- Limits, charges and timings change; confirm current ones.
**Likely follow-ups:** 1) *Which for a Rs 50 lakh payment?* Typically RTGS. 2) *What is NPCI?* The body that runs UPI and IMPS.
**Common mistakes:** Quoting limits as fixed; thinking UPI is a bank.

### Q32 ⭐⭐ 🟢 What are secured and unsecured loans, and which is riskier for the lender?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding of collateral.
**Say this in the interview:** "Secured loans are backed by an asset the lender can claim; unsecured loans are not. Unsecured is riskier, so it usually costs more."
**Explain simply:**
- **Collateral** is the asset pledged: house, car, gold.
- Home, auto and gold loans are secured; personal loans and credit cards are unsecured.
- If a secured borrower defaults, the lender can sell the asset to recover money, though selling takes time and may fetch less than owed.
- Unsecured lenders rely on the borrower's income and credit history, so loss given default is higher.
**Likely follow-ups:** 1) *Why charge more on unsecured?* To cover higher expected losses. 2) *Is secured risk-free?* No: asset values fall.
**Common mistakes:** Saying secured loans cannot default.

### Q33 ⭐⭐ 🟢 What is the repo rate in plain words, and how can a change in it affect loan EMIs and deposit rates?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Link between the central bank's rate and customer rates.
**Say this in the interview:** "The repo rate is the rate at which the RBI lends short-term money to banks. When it changes, banks' funding costs change, and over time loan and deposit rates tend to follow."
**Explain simply:**
- **EMI** (equated monthly instalment) is the fixed monthly payment of a loan.
- A fall in repo usually means cheaper floating-rate loans (lower EMI or shorter tenure); a rise does the opposite.
- Deposit rates usually move in the same direction, but not instantly or by the same amount.
- How quickly depends on the loan type (floating, linked to an external benchmark, or fixed). From memory, unverified; this is awareness, not advice.
**Likely follow-ups:** 1) *Fixed-rate loans?* Not affected. 2) *Why does NIM matter here?* Loans and deposits reprice at different speeds.
**Common mistakes:** Saying EMI changes instantly for every loan.

### Q34 ⭐⭐ 🟢 What is a payment gateway, and how does it earn money (MDR, take rate)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding of payment revenue.
**Say this in the interview:** "A payment gateway securely carries card or UPI payment details from the customer's checkout to the banks and returns the result. It earns a small percentage of each transaction."
**Explain simply:**
- **MDR (merchant discount rate)** is the fee the merchant pays on a payment, shared among the gateway, the merchant's bank and the card network (from memory, unverified; UPI rules differ).
- **Take rate** = the gateway's own revenue / total payment value processed. Example with invented numbers: Rs 2 crore processed, Rs 2 lakh revenue = 1.0%.
- Extra income: setup or subscription fees, fast settlement, and fraud tools.
**Likely follow-ups:** 1) *Is MDR all the gateway's income?* No, banks and networks take a share. 2) *Why track success rate?* Failed payments lose merchant sales.
**Common mistakes:** Mixing MDR with take rate; thinking the gateway holds the customer's money permanently.

### Q35 ⭐⭐ 🟢 What is the difference between a debit card, a credit card, a prepaid wallet and a BNPL (buy now pay later) product?
**Asked at:** commonly asked (no company-specific report found); payment-product basics appear in fintech guides (unverified).
**What the interviewer is checking:** Whether you know whose money is being spent in each product, because that decides the risk and the data.
**Say this in the interview:** "Debit and prepaid spend your own money, credit and BNPL spend the lender's money first and you repay later. So the first two carry no credit risk for the provider and the last two do."
**Explain simply:**
- **Debit card:** linked to your bank account; each purchase cuts your balance straight away. Like paying from your own salary.
- **Credit card:** the bank gives a credit limit; you spend, get a bill, and repay by the due date (or pay interest on what is left). Like an advance from the employer that you settle at month end.
- **Prepaid wallet:** you load money first, then spend only that amount. Like a canteen coupon balance. Rules on KYC and load limits apply (details from memory, unverified).
- **BNPL:** a small, short loan at checkout, often split into a few instalments. It is credit, so the provider needs underwriting (checking whether you can repay) and collections.
**Likely follow-ups:** 1) *Which has most delinquency data?* Credit card and BNPL, because only they have repayment behaviour. 2) *Is BNPL a loan?* Yes in substance; the regulatory treatment depends on who lends (from memory, unverified).
**Common mistakes:** Calling a wallet and a debit card the same thing; forgetting that BNPL creates credit risk even when the ticket size is small.

### Q36 ⭐⭐ 🟢 What are the stages of the loan life cycle (sourcing, underwriting, disbursal, servicing, collections, closure) and what data does each stage create?
**Asked at:** commonly asked (no company-specific report found); the funnel and collections stages feature in BFSI analyst job descriptions (unverified).
**What the interviewer is checking:** Whether you can map a loan to the tables an analyst will query later.
**Say this in the interview:** "A loan moves through six stages and each leaves its own data trail. If I know the stage, I know which table and which metric to look at."
**Explain simply:**
- **Sourcing:** finding customers (ads, agents, app). Creates lead and channel data: source, campaign, lead date.
- **Underwriting:** deciding yes or no and on what terms. Creates application data, bureau score, income documents, KYC result, decision and reason.
- **Disbursal:** money is paid out. Creates loan account, amount, rate, tenure, EMI schedule, disbursal date.
- **Servicing:** the loan runs month to month. Creates instalment, payment and balance records, mandate status.
- **Collections:** chasing missed payments. Creates DPD (days past due), contact attempts, promises to pay, recoveries.
- **Closure:** loan is paid off, settled or written off. Creates closure date and type, and feeds the customer's credit history.
**Likely follow-ups:** 1) *Which key joins the stages?* Application ID, then loan account ID, then customer ID. 2) *Where do approval rates come from?* Underwriting.
**Common mistakes:** Treating "disbursed" and "approved" as the same; forgetting that rejected applications are data too and are needed to study approval rates.

### Q37 ⭐⭐ 🟢 What is a demat account and what role do a stock exchange, a broker and a depository play when someone buys a share?
**Asked at:** commonly asked (no company-specific report found); capital-markets basics are a gap-fill question for wealth and broking roles.
**What the interviewer is checking:** That you understand who holds what in a share purchase.
**Say this in the interview:** "A demat account holds shares in electronic form, like a bank account holds money. The broker places my order, the exchange matches it with a seller, and the depository records that the shares are now mine."
**Explain simply:**
- **Demat account:** short for dematerialised; shares are stored electronically instead of as paper certificates.
- **Broker:** the middleman through whom you place the order; earns brokerage and other fees.
- **Stock exchange (for example NSE or BSE):** the marketplace that matches buyers and sellers and sets the trade price through that matching.
- **Depository (for example NSDL or CDSL, from memory, unverified):** the record keeper that moves shares between demat accounts after the trade settles.
- A trading account (to place orders) and a bank account (to pay) usually sit alongside the demat account.
**Likely follow-ups:** 1) *Does the broker hold my shares?* No, the depository record shows you as the holder. 2) *What data does this create?* Orders, trades, holdings and settlement records.
**Common mistakes:** Mixing up the depository (records ownership) with the exchange (matches trades).

### Q38 ⭐⭐ 🟢 What is a mutual fund, and what do NAV, AUM and SIP mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic vocabulary of the asset-management business.
**Say this in the interview:** "A mutual fund pools money from many people and invests it in shares or bonds. NAV is the price of one unit, AUM is the total money managed, and SIP is a fixed amount invested every month."
**Explain simply:**
- **Mutual fund:** like a common kitty; a fund manager invests it and each investor owns units in proportion to their money.
- **NAV (net asset value):** value of all the fund's holdings minus costs, divided by the number of units; effectively the price per unit, usually computed daily.
- **AUM (assets under management):** total market value of money the fund house manages. It grows from new investments and from market gains.
- **SIP (systematic investment plan):** an auto-debit that buys units regularly, for example Rs 5,000 a month. Like a recurring deposit in style, but the value moves with markets.
- Analyst angle: SIP count, SIP stop rate and AUM by investor segment are common metrics.
**Likely follow-ups:** 1) *Does a lower NAV mean cheaper?* No, NAV is only a unit price, not a measure of value. 2) *Is a SIP a guaranteed return?* No, returns depend on markets.
**Common mistakes:** Thinking a low NAV fund is a bargain; confusing AUM growth from inflows with growth from market gains (see Q62).

### Q39 ⭐⭐ 🟢 What is the difference between term insurance, endowment and ULIP in plain words?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can separate pure protection from savings-linked products.
**Say this in the interview:** "Term is pure cover: you pay a small premium and your family gets money only if you die in the term. Endowment adds a savings part with a maturity payout. A ULIP mixes insurance with market investing, so its value moves with markets."
**Explain simply:**
- **Term insurance:** premium is low because there is no payout if you outlive the term. Pure protection.
- **Endowment:** insurance plus saving; pays a lump sum on maturity or on death. Premium is higher because part goes to savings.
- **ULIP (unit linked insurance plan):** part of the premium buys life cover and the rest is invested in funds you choose. Maturity value depends on market performance.
- Product features, charges and tax rules are from memory, unverified; this is awareness, not advice on what anyone should buy.
- Analyst angle: persistency (do customers keep paying) differs a lot by product.
**Likely follow-ups:** 1) *Why is term cheapest?* No savings component. 2) *Which products have more fee data?* ULIPs, with several charge types.
**Common mistakes:** Calling endowment and ULIP the same; saying term insurance gives money back at the end (plain term does not).

### Q40 ⭐⭐ 🟢 What is the difference between write-off and NPA, and why do banks still track written-off loans?
**Asked at:** commonly asked (no company-specific report found); "flow to write-off" is a collections KPI named in listings (unverified).
**What the interviewer is checking:** That you know a write-off is an accounting step, not forgiveness.
**Say this in the interview:** "An NPA is a loan that has stopped being paid. A write-off is when the bank removes it from its balance sheet as a loss. The borrower still owes the money, so recovery continues."
**Explain simply:**
- **NPA (non-performing asset):** a loan with overdue payments beyond the regulatory limit (commonly 90 days, from memory, unverified). It is still shown as an asset, with provisions (money set aside for expected loss).
- **Write-off:** after the bank has provided heavily and sees little hope, it removes the loan from its books. Think of an employer removing an unrecoverable salary advance from the receivables list, while still asking the employee to repay.
- Banks keep tracking written-off accounts because **recoveries after write-off** are real income, and because the history feeds credit scores and recovery strategy.
- Reports often show "flow to write-off" as the last delinquency bucket.
**Likely follow-ups:** 1) *Does write-off cancel the debt?* No. 2) *Does it improve reported NPA?* Yes, it lowers the stock of NPAs, which is why analysts look at write-offs alongside NPA.
**Common mistakes:** Saying the loan is waived; ignoring write-offs when comparing banks' asset quality.

### Q41 ⭐⭐ 🟢 What is underwriting in lending and in insurance, and how do the two differ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you see underwriting as risk selection and pricing in both industries.
**Say this in the interview:** "Underwriting means deciding whether to take a risk and at what price. A lender asks whether this person will repay; an insurer asks how likely a claim is and what premium covers it."
**Explain simply:**
- **Lending:** checks income, existing loans, credit score and documents; decision is approve, reject or approve with changed amount or rate. Risk is that the borrower does not repay.
- **Insurance:** checks age, health, vehicle, occupation or claims history; decision is accept, load the premium (charge more), exclude something, or decline. Risk is that a claim occurs.
- **Difference:** a loan's loss is a default on money already paid out, while an insurer's loss is a claim on a promise. Lending decisions lean on a credit score; insurance leans on actuarial (statistical) pricing and medical or asset details.
- Similarity: both use past data to estimate probability and both can be partly automated.
**Likely follow-ups:** 1) *What does an analyst do?* Monitor approval rates and bad rates by segment. 2) *What is adverse selection?* Risky people being more likely to apply.
**Common mistakes:** Saying underwriting is only paperwork checking; forgetting the pricing side.

### Q42 ⭐⭐ 🟢 What is a chargeback, and who bears the loss in a card or payment dispute?
**Asked at:** commonly asked (no company-specific report found); chargebacks appear in payment-product analytics guides (unverified).
**What the interviewer is checking:** That you understand the dispute chain between cardholder, bank and merchant.
**Say this in the interview:** "A chargeback is when a cardholder disputes a payment and the money is pulled back from the merchant through the banks. Usually the merchant bears it unless they can prove the sale was valid; in fraud cases the loss can sit elsewhere depending on the rules."
**Explain simply:**
- The cardholder tells their bank (the **issuer**) that a charge is wrong: fraud, item not delivered, duplicate charge.
- The issuer raises a dispute with the merchant's bank (the **acquirer**), which debits the merchant, often with a dispute fee.
- The merchant can submit evidence (delivery proof, signed receipt). If accepted, the money goes back to the merchant.
- Who finally bears the loss depends on card network rules, the type of fraud and whether the payment was authenticated (for example with an OTP). Exact liability rules are from memory, unverified.
- Analysts track the **chargeback ratio** (disputes divided by transactions) because too high a ratio can bring penalties (see Q59).
**Likely follow-ups:** 1) *Is a refund the same?* No, a refund is merchant-initiated. 2) *What data is needed?* Transaction ID, reason code, dates, evidence status.
**Common mistakes:** Assuming the bank always absorbs the loss; mixing up refund and chargeback.

### Q43 ⭐⭐ 🟢 What is reinsurance in plain words, and why do insurers buy it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand how insurers protect themselves against very large losses.
**Say this in the interview:** "Reinsurance is insurance for insurance companies. An insurer passes part of its risk and premium to a reinsurer so one big event cannot sink it."
**Explain simply:**
- Example: an insurer covers thousands of homes in one flood-prone city. One flood could cause huge claims at once, so it shares part of that risk with a reinsurer.
- The insurer pays the reinsurer a share of premium; the reinsurer pays back a share of claims.
- Reasons to buy: protect against rare, huge losses; free up capital so the insurer can write more policies; add expertise on new risks.
- Two common forms: sharing a fixed percentage of every policy, or covering only losses above a limit (details from memory, unverified).
- Analyst angle: loss ratios are reported both gross (before reinsurance) and net (after it).
**Likely follow-ups:** 1) *Does the customer deal with the reinsurer?* No, the insurer stays responsible to the customer. 2) *Does reinsurance remove all risk?* No, the insurer keeps a part.
**Common mistakes:** Thinking customers claim from the reinsurer; ignoring gross versus net figures.

### Q44 ⭐⭐ 🟢 What is a salary account, and why do banks compete for corporate salary accounts? Connect it to what an HR team provides to the bank.
**Asked at:** commonly asked (no company-specific report found); this is an HR-flavoured gap-fill question, not from a specific interview report.
**What the interviewer is checking:** Whether you can link your HR background to the bank's business.
**Say this in the interview:** "A salary account is a savings account where an employer pays wages each month. Banks compete for it because one corporate deal brings hundreds of customers with steady income, whom they can later sell cards, loans and insurance."
**Explain simply:**
- The employer signs a deal with a bank; employees get accounts, often with perks such as lower minimum-balance rules (terms are from memory, unverified).
- **Why it is valuable:** salary credits are a stable deposit, often low-cost money (CASA means current and savings account money, which is cheaper for the bank than term deposits), and regular income makes customers easier to underwrite.
- **What HR provides:** employee list with name, ID, date of joining, KYC documents for onboarding, bank details, and the monthly payroll file with net pay per person.
- Data caution: this is personal data shared for a stated purpose; the bank should use it only as agreed and with consent for marketing (awareness only).
- Analyst metrics: salary accounts opened per company, activation rate, retention after job change, cross-sell rate.
**Likely follow-ups:** 1) *What happens when an employee leaves?* The account may drop to a normal savings account and the salary flow stops. 2) *How can a bank spot a salary account without being told?* By regular monthly credits from the same employer.
**Common mistakes:** Treating it as a simple account type and missing the corporate relationship and cross-sell value.

### Q45 ⭐⭐ 🟡 Calculate the provision coverage ratio and say what a low value would signal.
Data (Rs crore): gross NPAs 1,500; provisions held against NPAs 900.
**Asked at:** commonly asked (no company-specific report found); provision coverage appears with GNPA and NNPA in investor-education pages (unverified, formulas differ by source).
**What the interviewer is checking:** That you can compute the ratio and read it as a cushion against bad loans.
**Say this in the interview:** "Provision coverage is provisions divided by gross NPAs: 900 over 1,500 is 60%. A low value means the bank has set aside less money than the bad loans could cost."
**Explain simply:**
- **Provisions:** money the bank sets aside from profit to cover expected losses on loans that have gone bad. Like an HR department keeping a reserve for pending claims.
- Higher coverage means a thicker cushion; lower means a future hit to profit if the loans really are lost.
- Definition used here: provisions against NPAs divided by gross NPAs. Some banks and sources include technical write-offs in the numerator, so state your definition.
**Worked example:** 900 / 1,500 = 0.60 = 60.0% (unit: Rs crore cancels; no rounding needed). The uncovered part is 1,500 minus 900 = Rs 600 crore, which is also the net NPA before any other adjustments.
**Likely follow-ups:** 1) *Is lower always bad?* Not always: collateral-backed NPAs may need less provision, so check the secured share. 2) *Is there a required level?* Regulators set provisioning norms (from memory, unverified).
**Common mistakes:** Dividing by net NPA; reading coverage in isolation from NPA trend.

### Q46 ⭐⭐ 🟡 Calculate the credit-deposit ratio and say what it tells a bank about how much of its deposits it has lent.
Data (Rs crore): total advances 90,000; total deposits 1,50,000.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute and interpret a lending-intensity measure.
**Say this in the interview:** "Credit-deposit ratio is advances divided by deposits: 90,000 over 1,50,000 is 60%. So the bank has lent out 60 paise of every rupee it collected as deposits."
**Explain simply:**
- **Advances:** loans given out. **Deposits:** money customers have placed with the bank.
- A high ratio means more of the deposit money is working as loans (more interest income, but less spare liquidity). A low ratio means lots of idle money or a cautious bank.
- Compare with the bank's own history and peers; the right level depends on strategy and regulation (from memory, unverified).
**Worked example:** 90,000 / 1,50,000 = 0.60 = 60%. Remaining 40% of deposits is held as cash, reserves with the central bank and investments (such as government securities).
**Likely follow-ups:** 1) *Can it exceed 100%?* Yes, if the bank also funds loans from borrowings. 2) *Is higher better?* More profitable up to a point, but riskier on liquidity.
**Common mistakes:** Reading 60% as "40% of money is lost"; ignoring that unlent money is usually invested, not idle.

### Q47 ⭐⭐ 🟡 Calculate yield on advances, cost of funds and spread, and explain why spread differs from NIM.
Data: average yield earned on loans 10.5% a year; average cost of deposits and borrowings 6.5% a year.
**Asked at:** commonly asked (no company-specific report found); formulas vary across sources (unverified).
**What the interviewer is checking:** That you can separate spread from NIM and know why they differ.
**Say this in the interview:** "Yield on advances is given as 10.5% and cost of funds as 6.5%, so the spread is 4.0 percentage points. NIM is a different ratio, net interest income over average earning assets, so it accounts for all assets and for free funds like equity and current accounts."
**Explain simply:**
- **Yield on advances:** interest earned as a share of average loans.
- **Cost of funds:** interest paid as a share of average interest-paying money (deposits and borrowings).
- **Spread:** yield minus cost. It compares two rates directly.
- **NIM** (net interest margin): net interest income divided by average earning assets. It differs because earning assets include investments at other yields, and part of the bank's money (equity, current accounts) costs nothing, which lifts NIM above a simple spread.
- NIM cannot be calculated from the two rates alone; it needs the balance sizes.
**Worked example:** 10.5% minus 6.5% = 4.0 percentage points (not 4%, because it is a gap between two percentages). On Rs 100 lent and funded at these rates, interest earned 10.50 minus interest paid 6.50 gives 4.00 net.
**Likely follow-ups:** 1) *Which is more used?* NIM, because it covers the whole balance sheet. 2) *What squeezes spread?* Deposit rates rising faster than loan rates.
**Common mistakes:** Writing "4%" instead of 4 percentage points; calling spread and NIM the same.

### Q48 ⭐⭐ 🟡 A lender compares two score cut-offs. Calculate the marginal bad rate of the extra customers approved by lowering the cut-off, and say how you would present the trade-off.
Data: cut-off 700 approves 3,500 applicants with a bad rate of 2.5%. Cut-off 650 approves 5,000 applicants with a bad rate of 4%.
**Asked at:** commonly asked (no company-specific report found); cut-off and scorecard tuning appear in credit-risk guides (unverified).
**What the interviewer is checking:** That you look at the incremental group, not just the average.
**Say this in the interview:** "Lowering the cut-off adds 1,500 customers. Their bad rate is about 7.5%, far above the 4% average, so the average hides how risky the new group is."
**Explain simply:**
- **Score cut-off:** the minimum credit score for approval; lower cut-off means more customers and more risk.
- **Bad rate:** share of customers who default (definition must be fixed, for example 90+ days past due within 12 months).
- **Marginal bad rate:** the bad rate among only the extra customers added.
- Assumption: the 3,500 are included in the 5,000 and bad rates use the same definition and window.
**Worked example:** Bads at 700: 3,500 x 2.5% = 87.5. Bads at 650: 5,000 x 4% = 200. Extra customers: 1,500. Extra bads: 200 minus 87.5 = 112.5. Marginal bad rate = 112.5 / 1,500 = 7.5% (a count of 87.5 is an expected figure, so fractions are fine).
How to present: show a small table of approvals, bad rate, marginal bad rate and extra volume, then add expected profit per good customer versus loss per bad one so management can decide. Show the number of extra good customers: 1,500 minus 112.5 = 1,387.5.
**Likely follow-ups:** 1) *Would you recommend 650?* That depends on margin per good loan versus loss per bad one; I present options, not a verdict. 2) *Is the sample reliable?* Check sample size and time period.
**Common mistakes:** Quoting only the 4% average; ignoring that the bad rate is measured on old data.

### Q49 ⭐⭐ 🟡 Calculate expected loss for one loan and for a pool, and say what the result is used for.
Data: PD 2%; LGD 70%; EAD Rs 10 lakh per loan; pool of 1,000 such loans.
**Asked at:** commonly asked (no company-specific report found); PD, LGD and EAD are repeated across credit-risk guides (unverified).
**What the interviewer is checking:** That you can multiply the three parts and say why a lender wants the number.
**Say this in the interview:** "Expected loss is PD times LGD times EAD. For one loan that is 2% x 70% x Rs 10 lakh = Rs 14,000, and for 1,000 loans it is Rs 1.4 crore."
**Explain simply:**
- **PD:** probability the borrower defaults. **LGD:** share of the exposure lost after recoveries. **EAD:** amount owed at the time of default.
- Expected loss is an average over many loans, not a forecast for one: most loans lose nothing, a few lose a lot.
- Uses: setting provisions, pricing (interest rate must cover expected loss), and setting limits. Specific accounting and capital rules are from memory, unverified.
**Worked example:** One loan: 0.02 x 0.70 x 10,00,000 = Rs 14,000. Pool: Rs 14,000 x 1,000 = Rs 1,40,00,000 = Rs 1.4 crore. As a share of the pool exposure (Rs 100 crore), that is 1.4%.
**Likely follow-ups:** 1) *What is unexpected loss?* Variation around the average, covered by capital. 2) *Does it assume loans are independent?* The simple sum does; in a downturn defaults rise together.
**Common mistakes:** Using 70% as if it were the default probability; treating Rs 14,000 as the loss on a specific loan.

### Q50 ⭐⭐ 🟡 Calculate the FOIR (fixed obligation to income ratio) and the loan-to-value (LTV) ratio, and say how a lender uses each. (Here LTV means loan-to-value, not customer lifetime value.)
Data: monthly income Rs 60,000; existing EMIs Rs 12,000; proposed new EMI Rs 15,000. Property value Rs 50 lakh; loan Rs 40 lakh.
**Asked at:** commonly asked (no company-specific report found); a gap-fill question on lending basics.
**What the interviewer is checking:** That you can compute both and know one tests affordability and the other tests collateral cover.
**Say this in the interview:** "FOIR is total monthly obligations over monthly income: 27,000 over 60,000 is 45%. LTV is loan over property value: 40 over 50 lakh is 80%. FOIR checks whether the person can pay; LTV checks how much cushion the property gives."
**Explain simply:**
- **FOIR:** share of income already committed to fixed repayments, including the new EMI. Lower is safer.
- **LTV:** how much of the property's value is being lent. Higher means a thinner cushion if the property must be sold.
- Lenders set their own limits and regulatory caps may exist (from memory, unverified); here we only compute and interpret.
**Worked example:** FOIR = (12,000 + 15,000) / 60,000 = 27,000 / 60,000 = 45.0%. LTV = 40 lakh / 50 lakh = 80.0%. Remaining income after fixed EMIs is Rs 33,000 a month. Both are percentages of different bases, so they are not added together.
**Likely follow-ups:** 1) *Does FOIR use gross or net income?* It differs by lender; state which. 2) *What if the borrower has two incomes?* Use combined income and combined obligations.
**Common mistakes:** Leaving the new EMI out of FOIR; calling LTV "lifetime value" in a lending interview.

### Q51 ⭐⭐ 🟡 Two credit card customers are below. What is the average of their individual utilisation, what is the portfolio utilisation, and which one should a risk analyst report?
Data: customer A limit Rs 1,00,000, balance Rs 90,000. Customer B limit Rs 9,00,000, balance Rs 90,000.
**Asked at:** commonly asked (no company-specific report found); a gap-fill question on averaging ratios.
**What the interviewer is checking:** The classic "average of ratios versus ratio of totals" trap.
**Say this in the interview:** "The simple average of the two customers' utilisation is 50%, but the portfolio utilisation is 18%. I would report the portfolio figure for the book, and also show the distribution because customer A at 90% is the real risk flag."
**Explain simply:**
- **Credit utilisation:** balance divided by credit limit; high use usually signals stress.
- Average of ratios treats a Rs 1 lakh limit and a Rs 9 lakh limit as equal; the pooled ratio weights each by its limit.
- Neither number alone is complete: the pooled ratio describes how much of the book's limits is in use, while customer-level values spot the stretched customers.
**Worked example:** A = 90,000 / 1,00,000 = 90%. B = 90,000 / 9,00,000 = 10%. Simple average = (90% + 10%) / 2 = 50%. Portfolio = (90,000 + 90,000) / (1,00,000 + 9,00,000) = 1,80,000 / 10,00,000 = 18%.
**Likely follow-ups:** 1) *Which is better for the company's exposure?* Portfolio (limit-weighted). 2) *How would you flag risk?* Count customers above a threshold, such as above 80% utilisation.
**Common mistakes:** Averaging percentages across unequal bases; hiding stretched customers behind a low pooled figure.

### Q52 ⭐⭐ 🟡 A loan funnel is below. Calculate stage-to-stage and overall conversion and say where you would look first for improvement.
Data: leads 20,000; applications started 8,000; sanctioned 4,000; disbursed 3,200.
**Asked at:** commonly asked (no company-specific report found); funnel conversion appears in fintech and lending prep guides (unverified).
**What the interviewer is checking:** Whether you can turn four counts into rates and then choose where to act using volume, cost and effort, not just the lowest percentage.
**Say this in the interview:** "Conversion is 40% from lead to application, 50% from application to sanction, 80% from sanction to disbursal, and 16% overall. I would look first at lead to application, because it loses the most people, then at the 800 already-sanctioned customers who did not take the loan."
**Explain simply:**
- A **funnel** is a chain of steps; each step keeps only part of the previous step, like applicants dropping out between job posting, application, interview and joining.
- A **lead** is someone who showed interest; **sanctioned** means the lender approved the loan; **disbursed** means the money was actually paid out.
- Stage-to-stage conversion = this stage divided by the previous stage. Overall = last stage divided by first stage.
- Biggest loss in people: 12,000 leads never start an application. Biggest loss relative to cost: 800 sanctioned customers walked away after the lender had already spent on checks.
**Worked example:** (all rates are percentages, exact, no rounding needed)
- Leads to started: 8,000 / 20,000 = 40%
- Started to sanctioned: 4,000 / 8,000 = 50%
- Sanctioned to disbursed: 3,200 / 4,000 = 80%
- Overall: 3,200 / 20,000 = 16%; check: 40% x 50% x 80% = 16%.
**Likely follow-ups:** 1) *Why not just fix the lowest rate?* The lowest rate is not always the cheapest to fix; check volume, cost and cause. 2) *What would you cut the funnel by?* Channel, product, city, device, loan amount, week. 3) *Is the 80% good?* No benchmark is given; compare with past months and with other channels.
**Common mistakes:** Dividing every stage by the leads number and calling it stage conversion; ignoring that the leads may differ in quality by source; forgetting that sanction-to-disbursal drop-off often has fixable reasons (documents, offer terms, slow process).

### Q53 ⭐⭐ 🟡 Compare two loan sourcing channels using the data below. Which is better for the business, and what else would you check before deciding?
Data: DSA (direct sales agent) channel 2,000 loans disbursed, 90 went 90+ DPD. Digital channel 3,000 loans disbursed, 90 went 90+ DPD. Observation window is 12 months for both.
**Asked at:** commonly asked (no company-specific report found); channel comparison is a standard lending analytics case (unverified).
**What the interviewer is checking:** Whether you compare on a fair rate (bad loans divided by loans given), not raw counts, and know what else could change the answer.
**Say this in the interview:** "Both channels have 90 bad loans, but the DSA channel's 90+ DPD rate is 4.5% against 3.0% for digital. On this one measure digital is better, but I would check loan size, cost per loan, customer mix and loan age before deciding."
**Explain simply:**
- A **DSA** (direct sales agent) is an outside agent who brings in customers and is usually paid commission; a **digital channel** is the lender's app or website.
- **90+ DPD** (days past due) means the borrower is more than 90 days late; it is the usual marker of a seriously bad loan.
- Equal counts (90 and 90) mislead because digital sold 1,000 more loans; rate = bad loans / loans disbursed.
**Worked example:** DSA: 90 / 2,000 = 4.5%. Digital: 90 / 3,000 = 3.0%. Difference = 1.5 percentage points (DSA is 1.5 times as bad: 4.5 / 3.0 = 1.5).
**Data and tables involved:** loan table (loan id, channel, disbursal date, amount, product, interest rate), repayment table (days past due by month), customer table (income band, score band, city), cost table (commission, marketing). First cuts: bad rate by channel and score band, by loan amount, and by month of disbursal.
**Likely follow-ups:** 1) *What else do you check?* Rupee amount that went bad (not just count), total cost to acquire, approval criteria per channel, early signs such as first-payment default, fraud share. 2) *Is a 12-month window fair?* Only if loans in both channels are about the same age; loans disbursed late in the window have had less time to go bad. 3) *Could mix explain it?* Yes; if DSA serves riskier customers, compare within the same score band.
**Common mistakes:** Comparing counts; ignoring that DSA customers may be a different risk group; picking a winner without cost and profit, since a channel with higher losses can still earn more.

### Q54 ⭐⭐ 🟡 Calculate the first-payment-default rate and the NACH/e-mandate bounce rate, and explain why early-delinquency measures matter to a lender.
Data: 5,000 loans disbursed last month, 150 missed the first EMI. Separately, 10,000 auto-debit mandates were presented this month and 1,200 bounced.
**Asked at:** commonly asked (no company-specific report found); first-payment default and mandate bounce appear among early-warning KPIs in lending guides (unverified).
**What the interviewer is checking:** Whether you use the right denominator for each rate and understand why early signals matter.
**Say this in the interview:** "First-payment default is 3.0% (150 of 5,000), and the auto-debit bounce rate is 12% (1,200 of 10,000). They use different denominators, loans in one case and mandate presentations in the other, so I would not combine them."
**Explain simply:**
- **First-payment default (FPD):** a borrower misses the very first EMI (monthly instalment). It often points to fraud, wrong targeting or someone who never meant to repay.
- **NACH / e-mandate:** a standing instruction that lets the lender automatically pull the EMI from the borrower's bank account on the due date. A **bounce** means the pull failed, usually for low balance.
- Early measures matter because they show trouble within weeks, long before a loan is officially a bad loan (NPA), giving time to act: change approval rules, call earlier, fix the channel.
**Worked example:** FPD = 150 / 5,000 = 3.0%. Bounce rate = 1,200 / 10,000 = 12.0%. Many bounces are one-off timing issues (salary not yet credited), so a 12% bounce rate is not 12% default; check how many succeeded on re-presentation. An HR parallel: salary credit date versus EMI date matters.
**Likely follow-ups:** 1) *How would you cut FPD?* By channel, product, score band, city, disbursal week. 2) *Is a bounce the same as default?* No, many recover within days. 3) *Why measure disbursal month?* So FPD is on a fixed cohort (the same loans each time).
**Common mistakes:** Mixing the two denominators; counting loans that are not yet due for their first EMI in the denominator; treating a bounce as a permanent loss.

### Q55 ⭐⭐ 🟡 Walk through the collections contact funnel below and calculate each rate. Where would you intervene?
Data (one week): dial attempts 10,000; calls connected 3,000; right-party contacts (spoke to the actual borrower) 1,800; promises to pay 900; promises kept 540.
**Asked at:** commonly asked (no company-specific report found); contact rate, right-party contact and promise-to-pay kept appear in collections KPI guides (unverified).
**What the interviewer is checking:** Whether you can read a funnel step by step and say where effort is wasted.
**Say this in the interview:** "Only 30% of dials connect, 60% of connected calls reach the right person, half of those give a promise, and 60% of promises are kept. Overall 5.4% of dials end in a kept promise. I would intervene first on the connect rate, then on promise-keeping."
**Explain simply:**
- **Collections** means contacting borrowers who are late and getting them to pay.
- **Right-party contact (RPC):** you spoke to the actual borrower, not a relative or a wrong number.
- **Promise to pay (PTP):** the borrower commits to pay by a date; **kept** means they actually paid.
- Dialling blind at all hours wastes agent time; calling when people answer helps.
**Worked example:** (week data, exact)
- Connect rate: 3,000 / 10,000 = 30%
- RPC rate: 1,800 / 3,000 = 60% of connected calls (18% of dials)
- Promise rate: 900 / 1,800 = 50% of RPCs
- Kept rate: 540 / 900 = 60% of promises
- Overall: 540 / 10,000 = 5.4% of dials
**Where to intervene:** connect rate (70% of dials are lost; fix call timing, phone number quality, dialler settings) and the 40% broken promises (reminder messages the day before, payment links). Agent skill matters most at the promise step.
**Likely follow-ups:** 1) *Does a kept promise equal recovery?* Not always; check the amount paid versus the amount promised. 2) *How do HR facts connect?* New or high-attrition agent teams usually show lower promise rates. 3) *What cuts?* Time of day, bucket, agent, region.
**Common mistakes:** Using dials as the denominator for every step; ignoring amounts; blaming agents for number quality.

### Q56 ⭐⭐ 🟡 Calculate cost to collect and explain how a collections head uses it when choosing between tele-calling and field visits.
Data: collections team cost Rs 12 lakh in a month; amount recovered Rs 4 crore in the same month.
**Asked at:** commonly asked (no company-specific report found); cost-to-collect style efficiency measures appear in collections guides (unverified; definitions vary by company).
**What the interviewer is checking:** Whether you can compute a cost ratio and then reason about it, rather than just reading it.
**Say this in the interview:** "Cost to collect is Rs 12 lakh divided by Rs 4 crore, which is 3%, or Rs 3 spent for every Rs 100 recovered. I would compare that for tele-calling and field visits within the same overdue bucket, not overall."
**Explain simply:**
- Rs 1 crore = Rs 100 lakh, so Rs 4 crore = Rs 400 lakh. 12 / 400 = 3%.
- **Tele-calling** is cheap per account but works for small, early-overdue cases. **Field visits** cost more per account but can recover larger or older dues.
- A fair comparison uses the same bucket and amount band, and counts only recovery caused by the effort (some borrowers pay anyway).
- Team cost includes salary, incentives, dialler, travel; this is where HR cost data enters.
**Worked example:** 12 / 400 = 0.03 = 3.0%. If tele-calling cost Rs 5 lakh for Rs 2 crore (2.5%) and field cost Rs 7 lakh for Rs 2 crore (3.5%), that would be an invented comparison showing field is dearer per rupee; check what field recovers from accounts calls could not.
**Likely follow-ups:** 1) *Is lower always better?* No; too little spend can leave money unrecovered; look at marginal cost. 2) *What about write-offs?* Recovered amount from bad loans should be tracked separately. 3) *What if costs are shared?* Allocate clearly and state the rule.
**Common mistakes:** Comparing channels across different buckets; ignoring self-cure; counting cost per account instead of per rupee recovered.

### Q57 ⭐⭐ 🟡 Calculate claim frequency, average claim size (severity) and pure premium, and explain what a pricing analyst does with them.
Data (motor policies, one year): policies 5,000; claims filed 400; total claim cost Rs 2 crore.
**Asked at:** commonly asked (no company-specific report found); frequency and severity appear in insurance analytics prep guides (unverified, mostly US/UK-oriented).
**What the interviewer is checking:** Whether you know the three building blocks of insurance pricing and how they link.
**Say this in the interview:** "Frequency is 8% (400 claims on 5,000 policies), severity is Rs 50,000 per claim, and pure premium is Rs 4,000 per policy, which is 8% times Rs 50,000."
**Explain simply:**
- **Frequency:** how often a policy has a claim. **Severity:** how big an average claim is. **Pure premium:** expected claim cost per policy, the minimum needed just to pay claims.
- The actual price (gross premium) adds the insurer's expenses, commission, taxes and a profit margin on top.
- A pricing analyst calculates these by segment (vehicle age, city, driver age, claim history) to charge higher premiums for riskier groups.
**Worked example:** Total claim cost Rs 2 crore = Rs 2,00,00,000.
- Frequency = 400 / 5,000 = 0.08 = 8%
- Severity = 2,00,00,000 / 400 = Rs 50,000
- Pure premium = 2,00,00,000 / 5,000 = Rs 4,000 (check: 0.08 x 50,000 = 4,000)
**Likely follow-ups:** 1) *Why split frequency and severity?* They have different causes: more accidents versus costlier repairs. 2) *Does this use claims filed or paid?* Ideally incurred (paid plus reserves); state which. 3) *Can few large claims distort severity?* Yes; use medians or capped values as a check.
**Common mistakes:** Dividing claim cost by policies and calling it severity; using policy count when exposure (policy years) differs; forgetting claims reported late.

### Q58 ⭐⭐ 🟡 Calculate the motor insurance renewal rate and list three data cuts you would use to find why renewals are low.
Data: 20,000 policies fell due for renewal this quarter; 14,000 renewed.
**Asked at:** commonly asked (no company-specific report found); renewal analysis is a routine insurance analytics task (unverified).
**What the interviewer is checking:** The basic rate plus a diagnostic mindset about segmenting.
**Say this in the interview:** "Renewal rate is 14,000 / 20,000 = 70%. I would cut it by channel, by policy age and claim history, and by premium change, to see where the 30% are leaving."
**Explain simply:**
- **Renewal rate** = policies renewed divided by policies that fell due in the period (count-based here; a premium-based version weights by money).
- Insurance is a yearly repeat purchase; losing a customer costs the sales effort already spent.
- Definitions differ by company (for example whether a late renewal within a grace period counts).
**Worked example:** 14,000 / 20,000 = 0.70 = 70%. The lapse rate is 30% (6,000 policies).
**Data cuts (three or more):**
1. **Channel and agent or dealer:** a car dealer who bundled the first policy may not follow up at renewal.
2. **Policy age and claim history:** first renewals are usually weaker; customers who had a claim may be unhappy with claim handling or hit by a lower no-claim discount.
3. **Premium change:** compare the new quote against last year's and against competitors; check also reminder timing and payment mode.
**Likely follow-ups:** 1) *Count or premium renewal?* Report both. 2) *How do you spot reasons?* Lapse survey, call-centre notes. 3) *What if renewal is low only in one city?* Look at local competition and branch service.
**Common mistakes:** Mixing in new policies; ignoring policies that left through sale of vehicle; treating 70% as good or bad without a past comparison.

### Q59 ⭐⭐ 🟡 Calculate the gateway take rate and the chargeback ratio, and say why payment companies watch both.
Data: payment volume processed Rs 500 crore; gateway revenue Rs 6.5 crore. Separately 40,000 card transactions and 120 chargebacks.
**Asked at:** commonly asked (no company-specific report found); take rate and chargeback ratio appear in payments analytics guides (unverified).
**What the interviewer is checking:** Whether you separate revenue efficiency from risk and use the right base for each.
**Say this in the interview:** "Take rate is 1.3% (Rs 6.5 crore on Rs 500 crore), and chargeback ratio is 0.3% (120 of 40,000 card transactions). One is how much the gateway earns, the other is how much dispute risk comes with it."
**Explain simply:**
- **Payment gateway:** the service that carries card or UPI details from the shopper to the banks and back for an online merchant.
- **Take rate:** revenue divided by payment volume processed. **Chargeback:** a customer disputes a card payment with the bank and the money is pulled back from the merchant.
- Networks and banks set limits on chargeback ratios; exceeding them can bring penalties or loss of access (specifics: from memory, unverified, confirm with the risk team).
**Worked example:**
- Take rate = 6.5 / 500 = 0.013 = 1.3% (130 basis points)
- Chargeback ratio = 120 / 40,000 = 0.003 = 0.3% (30 basis points; one basis point = 0.01%)
- The two numbers use different bases: the take rate covers all payment volume in rupees, the chargeback ratio covers card transactions in counts.
**Likely follow-ups:** 1) *Why watch both?* A high take rate with rising chargebacks may mean the business is taking bad merchants. 2) *Count or value?* Track both. 3) *Who bears the loss?* Usually the merchant, sometimes the gateway if the merchant cannot pay.
**Common mistakes:** Dividing chargebacks by successful payments of another period; mixing counts and rupees; treating take rate as profit (it is before bank and network costs).

### Q60 ⭐⭐ 🟡 Calculate the fraud rate in basis points and say what you would compare it with.
Data: card fraud losses Rs 2.4 crore on total card spend of Rs 1,200 crore in a quarter. (One basis point = 0.01%.)
**Asked at:** commonly asked (no company-specific report found); fraud in basis points is a common risk reporting style (unverified).
**What the interviewer is checking:** Unit handling (crore, percent, basis points) and a sensible comparison set.
**Say this in the interview:** "Rs 2.4 crore on Rs 1,200 crore of spend is 0.2%, which is 20 basis points. I would compare it with the previous quarters, with the bank's own limit, and across channels."
**Explain simply:**
- One basis point (bp) is 0.01%, so 0.2% is 20 bp. Banks use bp because fraud is a very small share of spend.
- Compare: earlier quarters (is it rising?), by card type and channel (online versus in-store, domestic versus international), against the internal fraud budget, and against published industry figures (do not quote any from memory; look them up).
- Also track count-based fraud rate, since a few big cases can swing a value-based number.
**Worked example:** 2.4 / 1,200 = 0.002 = 0.2% = 20 bp. Both amounts are in crore so the units cancel.
**Likely follow-ups:** 1) *Percent or percentage point?* If it moves from 20 to 25 bp, that is up 5 bp, or 25% in relative terms. 2) *Is it gross or net of recoveries?* State which. 3) *Does timing matter?* Frauds are reported late, so recent quarters look lower at first.
**Common mistakes:** Mixing crore and lakh; forgetting the 100 when converting percent to bp; comparing quarters without allowing for late-reported fraud.

### Q61 ⭐⭐ 🟡 A payment gateway report and a bank settlement file are below. How would you reconcile them and what are the likely causes of the gap?
Data: gateway shows 10,000 successful payments worth Rs 1.20 crore. Bank settlement file shows 9,940 payments worth Rs 1.19 crore.
**Asked at:** commonly asked (no company-specific report found); reconciliation appears in payments and finance-operations JDs and guides (unverified).
**What the interviewer is checking:** A structured matching approach, not guessing at causes.
**Say this in the interview:** "The gap is 60 payments and about Rs 1 lakh. I would match both files line by line on the transaction reference, split the differences into missing on either side and amount mismatches, and then explain each group."
**Explain simply:**
- **Reconciliation** means checking that two independent records of the same money agree.
- Gateway shows 10,000 payments, Rs 1.20 crore (average Rs 1,200). Bank shows 9,940, Rs 1.19 crore. Gap: 60 payments and Rs 1.00 lakh (average Rs 1,667 each; the figures are rounded to the nearest 0.01 crore, so the true gap could differ somewhat).
- Likely causes: timing (a payment on the last day settled on the next day), payments still pending or reversed, refunds or chargebacks netted off, fees deducted before settlement, duplicates, or a status mismatch (gateway says success, bank never received).
**Data and tables involved:** gateway transaction table (reference id, amount, status, timestamp) and bank settlement file (UTR or reference, amount, settlement date). First cuts: unmatched by date, by status, by amount band.
**Worked example:** a tiny sample, matched on reference:
```sql
-- Match both files on the transaction reference and show only the differences
SELECT COALESCE(g.txn_id, b.txn_id) AS txn_id,
       g.amount AS gateway_amount,
       b.amount AS bank_amount,
       CASE
         WHEN b.txn_id IS NULL THEN 'missing in bank file'
         WHEN g.txn_id IS NULL THEN 'missing in gateway report'
         WHEN g.amount <> b.amount THEN 'amount differs'
       END AS issue
FROM gateway g
FULL OUTER JOIN bank b ON g.txn_id = b.txn_id
WHERE b.txn_id IS NULL OR g.txn_id IS NULL OR g.amount <> b.amount
ORDER BY txn_id;
```
Output on the sample:
```
T2 | 2000 | 1950 | amount differs
T4 | 3000 | NULL | missing in bank file
T9 | NULL | 800  | missing in gateway report
```
Each row is a case to explain; the totals gap is just the sum of these.
**Likely follow-ups:** 1) *What if no common id?* Match on amount plus time plus card last four digits, with care. 2) *Who fixes it?* Finance operations with the bank. 3) *What do you report?* Count and value by cause.
**Common mistakes:** Comparing only totals; treating rounded crore figures as exact; forgetting timing differences around month end.

### Q62 ⭐⭐ 🟡 Calculate the change in mutual fund AUM from flows versus market movement and explain why distributors track both.
Data (Rs crore): opening AUM 10,000; net inflows (purchases minus redemptions) 600; market gain on holdings 400.
**Asked at:** commonly asked (no company-specific report found); AUM change decomposition appears in asset-management analytics (unverified).
**What the interviewer is checking:** Whether you separate what the business controls (money in and out) from what it does not (markets).
**Say this in the interview:** "AUM rose by Rs 1,000 crore, from 10,000 to 11,000, a 10% rise. Rs 600 crore (6 points) came from net inflows and Rs 400 crore (4 points) from market gains. Distributors care mainly about the flow part, because it reflects customer behaviour."
**Explain simply:**
- **Mutual fund:** a pool of many investors' money managed by a professional. **AUM** (assets under management) is the total value of that pool.
- **Net inflow:** purchases minus redemptions (money withdrawn).
- Distributors earn a commission on AUM, so a rising market raises their income even if they sold nothing, and a falling market can hide good selling. Tracking both shows true business growth versus luck.
**Worked example:** (Rs crore)
- Change = 600 + 400 = 1,000; closing AUM = 10,000 + 1,000 = 11,000.
- Growth = 1,000 / 10,000 = 10%; from flows 600 / 10,000 = 6%; from market 400 / 10,000 = 4%.
- Percentages are shares of opening AUM, so 6% + 4% = 10%.
**Likely follow-ups:** 1) *Is the market gain net of costs?* State it. 2) *What about timing of flows?* This simple split ignores when money moved in the month. 3) *Switches between funds?* Treat them as flows between schemes, not as new money for the company.
**Common mistakes:** Calling the whole increase "sales"; dividing by closing instead of opening AUM; ignoring redemptions.

### Q63 ⭐⭐ 🟡 Calculate NAV per unit and explain what NAV does and does not tell an investor.
Data (Rs crore): fund assets 1,050; fund liabilities 50; units outstanding 50 crore.
**Asked at:** commonly asked (no company-specific report found); NAV calculation appears in mutual fund basics guides (unverified).
**What the interviewer is checking:** The formula and the common misconception that a low NAV means a cheap fund.
**Say this in the interview:** "NAV per unit is (assets minus liabilities) divided by units, so (1,050 - 50) / 50 = Rs 20. It is the value of one unit on the day; it does not tell you whether the fund is good or cheap."
**Explain simply:**
- **NAV** (net asset value) is the fund's net worth per unit: what the fund owns minus what it owes, divided by units outstanding.
- Think of it as the price of one slice of the pooled money; investors get units at NAV (plus any costs).
- It does **not** tell you the return (compare NAV across dates for that), the risk, the fees, or whether Rs 20 is cheap compared with Rs 200 in another fund. A fund with a lower NAV is not a better bargain.
- (From memory, unverified: funds in India publish NAV each business day.)
**Worked example:** (Rs crore, units in crore) Net assets = 1,050 - 50 = 1,000. NAV = 1,000 / 50 = Rs 20.00 per unit. If NAV was Rs 18 a year ago, the rise is (20 - 18) / 18 = 11.1% (invented past figure, rounded to one decimal).
**Likely follow-ups:** 1) *Why does NAV change daily?* The market value of holdings changes. 2) *Does a dividend change NAV?* Payouts reduce NAV. 3) *Is this advice?* No; this explains the metric only.
**Common mistakes:** Comparing NAVs across funds; forgetting to subtract liabilities; mixing units in crore with rupees.

### Q64 ⭐⭐ 🟡 Calculate the SIP stoppage ratio and explain why distributors watch it.
Data: in a month, 1,00,000 new SIPs registered and 60,000 existing SIPs were stopped or expired.
**Asked at:** commonly asked (no company-specific report found); SIP stoppage ratio appears in mutual fund distribution reporting (unverified; definitions vary).
**What the interviewer is checking:** The ratio and its definition, and awareness of what it means for the business.
**Say this in the interview:** "Using the definition stoppages divided by new registrations, the ratio is 60,000 / 1,00,000 = 60%. Net SIP additions are still 40,000, but a high ratio warns that the SIP book is leaky."
**Explain simply:**
- A **SIP** (systematic investment plan) is a standing monthly instruction to invest a fixed amount in a fund. It gives steady, predictable inflows.
- **Stopped or expired:** a customer cancelled, a payment failed repeatedly, or the SIP reached its end date. Expiry is natural; early stoppage is the warning.
- Distributors watch it because lost SIPs mean lost future AUM and commission. Split stoppages by reason (bank bounce, cancelled, expired), age of SIP and channel.
**Worked example:** 60,000 / 1,00,000 = 0.60 = 60%. Some firms divide by the active SIP base instead, which would give a much smaller number; state your definition. This is a monthly ratio; it does not mean 60% of investors quit.
**Likely follow-ups:** 1) *What is a better cut?* Stoppage within the first six months, by channel. 2) *How reduce bounces?* Reminders before debit date. 3) *Compare across months?* Yes, trend matters more than one value.
**Common mistakes:** Treating expiries as failures; comparing ratios with different denominators; ignoring the net addition.

### Q65 ⭐⭐ 🟡 Calculate the cross-sell ratio (products per customer) and explain how a retail bank uses it.
Data: 50,000 active customers hold 90,000 products in total (accounts, cards, loans, insurance).
**Asked at:** commonly asked (no company-specific report found); products per customer is a standard retail banking measure (unverified).
**What the interviewer is checking:** The ratio and its business use, and its limits.
**Say this in the interview:** "90,000 products over 50,000 customers is 1.8 products per customer. The bank uses it to see how deeply customers are served, and to target single-product customers for a second product."
**Explain simply:**
- **Cross-sell** means selling an existing customer another product: a credit card to a salary-account holder, insurance to a loan customer.
- Customers with more products tend to stay longer (a hypothesis to test in the bank's data, not a given), and acquiring a new customer costs more than selling to an existing one.
- Look at the spread too: an average of 1.8 can hide 30,000 customers with one product and a few with many.
**Worked example:** 90,000 / 50,000 = 1.8 products per customer (exact). Counts do not show value; a zero-balance account counts as much as a home loan.
**Likely follow-ups:** 1) *How would you cut it?* By tenure, segment, branch, salary-account holders. 2) *What caution?* Pushing unwanted products creates mis-selling and complaints. 3) *Do auto-created products count?* Decide and state a rule.
**Common mistakes:** Counting inactive customers or closed products; reading the average without the distribution; using accounts per customer and products per customer interchangeably.

### Q66 ⭐⭐ 🟡 Calculate the complaint rate per 10,000 policies and say which grievance data an insurer would track.
Data: 180 complaints received in a quarter; 60,000 policies in force.
**Asked at:** commonly asked (no company-specific report found); grievance rates are common in insurance service reporting (unverified).
**What the interviewer is checking:** Scaling a small count to a standard base and knowing which grievance fields matter.
**Say this in the interview:** "180 complaints on 60,000 policies in force is 30 per 10,000 policies for the quarter. I would track complaints by type, channel, product, resolution time and escalations."
**Explain simply:**
- Dividing by policies puts big and small insurers or products on the same scale; per 10,000 is used because the raw rate is tiny.
- **Policies in force** means policies currently active; ideally use the average over the quarter.
- Fields to track: complaint category (claim delay or rejection, mis-selling, premium or service issue), product, sales channel, region, date received and closed (turnaround time), repeat or reopened, escalated outside the company (such as to a regulator or ombudsman; from memory, unverified, confirm the current channels).
**Worked example:** 180 / 60,000 x 10,000 = 30.0 complaints per 10,000 policies (for one quarter; do not multiply by 4 to annualise without saying so).
**Likely follow-ups:** 1) *Why not complaints per claim?* Claim complaints can use a claims base; use both. 2) *Privacy?* Complaints hold personal and health details; limit access. 3) *Good or bad?* Needs trend and peer context.
**Common mistakes:** Comparing raw counts across products; ignoring resolution time; using end-of-period policies when the book changed a lot.

### Q67 ⭐⭐ 🟡 What are the main KYC, AML and fraud screening checks in a customer onboarding flow, and which data points does each use?
**Asked at:** commonly asked (no company-specific report found); onboarding checks appear in KYC, AML and fintech risk prep pages (unverified).
**What the interviewer is checking:** Whether you can separate the three families of checks and name the data each one uses.
**Say this in the interview:** "KYC proves who the person is, AML checks whether they or their money look risky from a crime or sanctions view, and fraud screening asks whether this application is genuine or fake. They overlap in data but answer different questions."
**Explain simply:**
- **KYC (know your customer):** identity and address proof (such as PAN and Aadhaar or other accepted documents), photo and liveness or video check, name and date-of-birth match, a lookup in a central KYC record where one exists (details: from memory, unverified, confirm with compliance).
- **AML (anti-money-laundering):** screening against sanctions and watch lists, checks whether the person is a **PEP** (politically exposed person), adverse news, a risk rating from occupation, income, country and product, and the declared source of funds.
- **Fraud screening:** device and IP signals, phone number and email age, many applications from one device or address, tampered documents, mismatch between stated details and bureau data, internal blocklists.
- An analyst usually measures pass rates, drop-offs, manual-review volumes and false alarms, not the personal documents themselves.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: collect only what is needed, keep identity numbers masked in reports, and share them only with approved teams.
**Likely follow-ups:** 1) *Which check rejects most?* Count rejections by reason. 2) *Too strict?* Drop-off rises. 3) *Same as sanctions screening?* That is one AML part.
**Common mistakes:** Blending the three terms; showing full ID numbers in dashboards; ignoring drop-off cost of checks.

### Q68 ⭐⭐ 🟡 What is a velocity rule in fraud detection, and how would you pick a threshold for it using data?
**Asked at:** commonly asked (no company-specific report found); velocity rules and threshold tuning appear in fraud analytics guides (unverified).
**What the interviewer is checking:** Whether you pick a threshold with evidence on both caught fraud and false alarms, not by gut feel.
**Say this in the interview:** "A velocity rule flags an unusual number or amount of events by one entity in a short time, for example more than 5 transactions on one card in 10 minutes. I would choose the threshold by testing several values on past data and balancing fraud caught against genuine customers disturbed."
**Explain simply:**
- **Velocity** means speed of activity: transactions, logins, failed OTPs or applications per card, device, phone or account within a time window.
- Fraudsters test stolen cards with rapid small purchases; real customers rarely behave like that.
- Steps: build the count per entity per window; label past cases as fraud or genuine; try thresholds; for each, compute alerts, frauds caught (recall) and the share of alerts that are fraud (precision); check by segment (a shop-owner account is naturally busier than a student's); also check how many alerts the review team can handle.
- Re-test over time because fraud patterns change.
**Worked example:** invented test on 10,000 card-days with 100 known frauds:
| Threshold (transactions in 10 min) | Alerts | Frauds caught | Precision | Recall |
|---|---|---|---|---|
| 3 or more | 900 | 90 | 10.0% | 90% |
| 4 or more | 400 | 82 | 20.5% | 82% |
| 5 or more | 160 | 70 | 43.8% | 70% |
| 6 or more | 70 | 40 | 57.1% | 40% |
Choice: a threshold of 4 or 5 depends on team capacity and the cost of a missed fraud versus an annoyed customer; precision is rounded to one decimal.
**Likely follow-ups:** 1) *One rule for everyone?* Use segment thresholds. 2) *Why not the lowest threshold?* Alert overload and blocked genuine customers. 3) *Who decides?* Fraud and business heads with the data.
**Common mistakes:** Choosing a threshold on fraud found alone; ignoring segments and review capacity; never re-testing.

### Q69 ⭐⭐ 🟡 What are SMA-0, SMA-1 and SMA-2 categories of stressed loans, and why are they watched before a loan becomes an NPA?
**Asked at:** commonly asked (no company-specific report found); stressed-asset vocabulary appears in BFSI prep guides (unverified).
**What the interviewer is checking:** Whether you know that "bad loans" are tracked in stages and that early stages are where action still works.
**Say this in the interview:** "SMA means Special Mention Account: a loan that is overdue but not yet an NPA. SMA-0, 1 and 2 are early-warning buckets for roughly 1-30, 31-60 and 61-90 days overdue, and we watch them because recovery is far easier before day 90."
**Explain simply:**
- **DPD (days past due)** is the number of days a payment is late. Think of it as the "days absent without leave" counter for a loan.
- **NPA (non-performing asset)** is a loan overdue for more than 90 days (from memory, unverified); from then the bank must stop counting the interest as income and set money aside.
- **SMA buckets (from memory, unverified):** SMA-0 is overdue up to 30 days, SMA-1 is 31-60, SMA-2 is 61-90. Exact rules differ by loan type and have been refined by RBI over time.
- **Why watch them:** a borrower who is 20 days late can often be reached with a reminder or a restructured date; one who is 80 days late is about to become an NPA with a loss attached. The SMA-2 pool is the "next month's NPA" forecast.
- Analysts track how many accounts and how much money move from SMA-0 to SMA-1 to SMA-2 (the "roll" between buckets).
**Worked example:** days overdue by code: 0 days = standard (on time); 5 days = SMA-0; 35 days = SMA-1; 65 days = SMA-2; 95 days = NPA.
**Regulation / privacy note (awareness only):** day-count rules and reporting thresholds are from memory, unverified; confirm with the risk or compliance team.
**Likely follow-ups:** 1) *What is a roll rate?* The share of accounts in one bucket that move to the next worse bucket in a month. 2) *Do you count accounts or rupees?* Both; a few large accounts can distort the rupee view.
**Common mistakes:** Treating SMA as the same thing as NPA; forgetting a payment resets the day counter; mixing "overdue" with "outstanding" (the full loan balance).

### Q70 ⭐⭐ 🟡 What are the main differences between a bank deposit customer metric set and a lending customer metric set?
**Asked at:** commonly asked (no company-specific report found); CASA and NPA style metrics appear across BFSI guides (unverified).
**What the interviewer is checking:** Whether you understand that deposits and loans are different businesses with different risks.
**Say this in the interview:** "Deposit metrics are about balances, stickiness and cost of funds; lending metrics are about growth, repayment quality and loss. One brings money in, the other lends it out and risks not getting it back."
**Explain simply:**
- **Deposit side:** average balance, **CASA** share (current and savings accounts, the cheap, low-interest money banks like), cost of funds (interest the bank pays), account activity, dormancy, balance attrition (money leaving).
- **Lending side:** disbursement (money given out), outstanding balance, yield (interest earned), **DPD** buckets, **GNPA/NNPA** (gross and net non-performing loans), collection efficiency, provision coverage, loss rate.
- The deposit customer's risk is "will they leave?"; the lending customer's risk is "will they repay?"
- The same person can be both, which is why a combined (customer 360) view matters.
- HR parallel: deposits are like retention (do people stay and stay engaged), lending is like hiring quality (did we pick right, and how are they performing).
**Likely follow-ups:** 1) *What is cost of funds?* The average interest a bank pays to raise money. 2) *Which is more profitable?* Neither alone; the gap between loan yield and cost of funds (the margin) is the core earning, and definitions of margin vary by bank.
**Common mistakes:** Using NPA for a deposit customer; quoting "balance" without saying average or closing; mixing cheap (CASA) and costly (term) deposits.

### Q71 ⭐⭐ 🟡 What does UPI "zero MDR" mean, and how do UPI apps still earn revenue?
**Asked at:** commonly asked (no company-specific report found); UPI structure is flagged as useful prep for fintech loops (unverified).
**What the interviewer is checking:** That you understand the payments business model and why transaction volume alone is not revenue.
**Say this in the interview:** "MDR is the fee a merchant pays on each payment. Zero MDR means the merchant pays nothing to accept UPI, so apps earn from other products built on the user base, not from the payment itself."
**Explain simply:**
- **MDR (Merchant Discount Rate)** is the percentage a shop pays the bank for accepting a card or digital payment. Cards charge it; UPI person-to-merchant payments carry none (from memory, unverified: a government policy since 2020, which could change).
- If payments are free, the app needs other income. Typical routes: lending referrals or loans, insurance and investment distribution, bill-payment and recharge commissions, merchant services (card-machine style devices, soundbox rentals), advertising and cashback-funded brand tie-ups, and wallet or prepaid-instrument fees.
- Payments are therefore often a **customer acquisition** tool; the analyst question becomes "how much revenue per active user from the other products?"
- An analyst tracks cost per transaction (infrastructure, cashback, support) against revenue per user.
**Likely follow-ups:** 1) *Can an app be profitable on UPI alone?* Hard when MDR is zero; hence the push into financial products. 2) *What is take rate?* Revenue divided by transaction value.
**Common mistakes:** Saying "UPI is free so apps earn nothing"; stating a current MDR rule as certain; ignoring cashback cost.

### Q72 ⭐⭐ 🟡 How would you define an active customer for a bank, a UPI app and an insurer, and why do the definitions differ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you tie a metric to how the product is used, and know "active" has no universal definition.
**Say this in the interview:** "Active means the customer did the thing the business depends on within a time window. That is a transaction for a UPI app, a customer-initiated transaction or balance for a bank, and an in-force policy for an insurer, so I always state the definition first."
**Explain simply:**
- **UPI app:** at least one successful payment in the last 30 days (monthly active users). Use frequent windows because usage is daily.
- **Bank:** at least one customer-initiated transaction (not interest credit or fees) in the last 90 days, or a minimum balance. Salary accounts may be "active" by salary credit.
- **Insurer:** a policy currently in force (premium paid, not lapsed). Customers interact once a year, so a 30-day rule would call almost everyone inactive.
- The time window should match natural usage frequency, like measuring HR "active employees" by payroll status rather than by last login.
- Document the definition; these are choices, not facts, and they differ across companies.
**Likely follow-ups:** 1) *Why exclude bank-initiated entries?* Interest and charges happen without the customer acting. 2) *What if the definition changes?* Restate history, or trend comparisons break.
**Common mistakes:** One window for all products; counting logins as activity; counting dormant accounts as customers.

### Q73 ⭐⭐ 🟡 What are P2P and P2M payments, and how do the metrics you track differ for each?
**Asked at:** commonly asked (no company-specific report found); UPI analytics listed in fintech prep guides (unverified).
**What the interviewer is checking:** Whether you separate the two payment types, because they behave and earn differently.
**Say this in the interview:** "P2P is person to person, like splitting dinner; P2M is person to merchant, like paying a shop. P2P is about network and frequency; P2M is about merchants, ticket size and repeat spending."
**Explain simply:**
- **P2P:** metrics are sender and receiver counts, average amount, new-contact growth, share of "first-time payee". Revenue is usually nil, so it is an engagement driver.
- **P2M:** metrics are merchants onboarded and active, repeat rate, average ticket size, category mix (grocery, food, travel), merchant retention. This is where monetisable behaviour sits.
- **Shared metrics:** success rate, failure reasons, volume and value (count of payments and rupees moved).
- Fraud patterns differ: P2P suffers from impersonation and collect-request scams; P2M from fake merchants and refund abuse.
**Likely follow-ups:** 1) *Which would you grow first?* Depends on strategy; P2M brings revenue chances, P2P brings users. 2) *Why track count and value separately?* A few large P2P transfers can hide a drop in everyday P2M usage.
**Common mistakes:** Reporting one blended average ticket; treating both as equally monetisable; ignoring merchant-side churn.

### Q74 ⭐⭐ 🟡 What are the main reasons for UPI or card payment failures (technical decline vs business decline), and how does the failure code field help an analyst?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can separate failures the user caused from failures the system caused, because the fix differs.
**Say this in the interview:** "A business decline is the bank saying no for a rule or customer reason, like insufficient funds. A technical decline is the system failing, like a timeout. The failure code lets me split them and focus on what we can actually fix."
**Explain simply:**
- **Business decline:** insufficient balance, wrong PIN, daily limit exceeded, account blocked, risk rule triggered. The customer or bank policy is the cause.
- **Technical decline:** bank server down, network timeout, app error, slow response. The infrastructure is the cause and it is often fixable.
- **Failure code:** each failed attempt carries a code (the actual code lists belong to the payment network and vary; from memory, unverified). Group by code, bank and time to find patterns, such as one bank spiking at 8pm.
- Analysts usually look at technical failures first, since the customer wanted to pay and the system let them down.
**Worked example:** invented 10,000 attempts: 9,000 succeeded (90.0%). Of the 1,000 failures: technical 400 (bank down 250, timeout 150) = 40% of failures, business 560 (funds 300, PIN 200, limit 60) = 56%, other 40 = 4%. Overall technical failure rate = 400 / 10,000 = 4.0% of all attempts. Percentages are of failures unless stated.
**Likely follow-ups:** 1) *Do retries matter?* Yes: count unique user intentions, not attempts. 2) *Who owns each type?* Technical: engineering and bank partners; business: customer education and risk policy.
**Common mistakes:** One blended "failure rate"; ignoring "other/unknown" codes; counting retries as separate customers.

### Q75 ⭐⭐ 🟡 What data would you pull to build a customer 360 view for a retail bank, and what privacy caution applies?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know which sources to join and that more data is not always allowed or wise.
**Say this in the interview:** "I would join one row per customer from accounts, transactions, loans, cards, channel usage and service history, but only fields needed for the purpose, with masked identifiers and access controls."
**Explain simply:**
- Customer 360 means one customer, all products and interactions in one place.
**Data and tables involved:**
- **Customer master:** customer ID, age band, city, account opening date, KYC status (the identity check banks must do).
- **Accounts and balances:** product, average balance, status, dormancy.
- **Transactions:** counts, amounts, channel (UPI, card, branch), salary credit.
- **Loans and cards:** outstanding, DPD, limits, utilisation.
- **Service and channel:** complaints, app logins, branch visits, campaign responses.
- First cuts: number of products per customer, tenure, active versus dormant, high balance but low usage.
**Regulation / privacy note (awareness only):** use data only for the purpose the customer agreed to, use the minimum fields, mask names and phone numbers, restrict access and log who views it. Specific laws (such as India's data protection act) are from memory, unverified; confirm with the compliance team.
**Likely follow-ups:** 1) *Key to join on?* A customer ID, not a name. 2) *Duplicates?* One person with several IDs needs de-duplication.
**Common mistakes:** Pulling every column; using names as join keys; ignoring that consent may cover only certain uses.

### Q76 ⭐⭐ 🟡 What is a scorecard in credit underwriting, what do Gini and KS tell you, and how would you explain them to a non-technical manager?
**Asked at:** commonly asked (no company-specific report found); scorecards and model-quality measures appear in credit-risk prep guides (unverified).
**What the interviewer is checking:** Whether you can explain model quality in plain words, not just recite names.
**Say this in the interview:** "A scorecard gives each applicant a score that ranks how likely they are to repay. KS and Gini both measure how well that ranking separates good borrowers from bad ones: higher means better sorting."
**Explain simply:**
- **Scorecard:** a points-based model using things like past repayment, income stability and existing debt to produce one number. Lower score, higher risk.
- **KS (Kolmogorov-Smirnov):** sort applicants from riskiest to safest; KS is the biggest gap between the cumulative share of bad and good borrowers caught so far.
- **Gini:** a 0 to 1 measure of overall ranking power (0 = random, 1 = perfect); Gini = 2 x AUC - 1, where AUC is the chance a random bad borrower scores worse than a random good one.
- Manager version: "If we reject the riskiest 40% of applicants, how many bad ones do we avoid compared with good ones we turn away?"
**Worked example:** invented 1,300 borrowers in 10 score bands (riskiest first): 1,040 good, 260 bad (20% bad). By band 4 we hold 80.8% of bads but only 19.2% of goods: gap 61.5%, so KS = 61.5 points. Trapezoid area under that cumulative curve gives AUC = 0.881, so Gini = 0.761 (rounded to three decimals).
**Likely follow-ups:** 1) *Is a high Gini always good?* Suspiciously high may mean leakage; check on new data. 2) *Why watch it over time?* Scores drift as the economy and customers change.
**Common mistakes:** Mixing up Gini of a model with Gini inequality; reading KS as a percent of bad borrowers; judging on training data only.

### Q77 ⭐⭐ 🟡 What is IND AS 109 or IFRS 9 expected credit loss in plain words, and what are stage 1, stage 2 and stage 3 loans?
**Asked at:** commonly asked (no company-specific report found); IFRS 9 stages appear in credit-risk guides (unverified).
**What the interviewer is checking:** Whether you understand provisioning as expected, forward-looking, not waiting for losses.
**Say this in the interview:** "Expected credit loss means setting money aside for losses we expect, before they happen. Loans are put in three stages by how much their credit quality has worsened, and the worse the stage, the bigger the set-aside."
**Explain simply:**
- **ECL = PD x LGD x EAD:** probability of default (chance the borrower stops paying), loss given default (share we lose after recoveries), exposure at default (amount owed at that point).
- **Stage 1:** performing; provision for losses expected in the next 12 months.
- **Stage 2:** credit risk has risen significantly (for example, overdue beyond about 30 days is a common trigger, from memory, unverified); provision for losses over the whole remaining life of the loan.
- **Stage 3:** credit-impaired, commonly default at about 90 days; lifetime loss, with interest usually recognised only on the net amount.
- Stage migration hits profit: a loan moving from 1 to 2 raises the provision.
**Worked example:** invented Rs 10,00,000 loan, LGD 45%. Stage 1 with 12-month PD 2%: ECL = 0.02 x 0.45 x 10,00,000 = Rs 9,000. Moved to stage 2 with lifetime PD 8%: ECL = Rs 36,000. Stage 3, PD treated as 100%: Rs 4,50,000.
**Regulation / privacy note (awareness only):** which entities apply this (NBFCs versus banks, and bank timelines) is from memory, unverified; confirm with the finance team.
**Likely follow-ups:** 1) *Why forward-looking?* So losses are recognised earlier. 2) *Who sets PD?* Models plus economic scenarios, reviewed by risk.
**Common mistakes:** Calling stage 3 "any NPA"; omitting LGD; thinking provisions are actual losses.

### Q78 ⭐⭐ 🟡 What is a bank's capital adequacy ratio in plain words, and why does a regulator care about it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you grasp the bank's "cushion against losses" idea without needing to be a risk specialist.
**Say this in the interview:** "Capital adequacy ratio compares a bank's own capital with its risk-weighted assets. It shows how big a loss the bank can absorb before depositors are at risk, which is why regulators set a minimum."
**Explain simply:**
- A bank lends mostly other people's money (deposits). Its own **capital** is the shock absorber.
- **Risk-weighted assets (RWA):** loans counted by riskiness; safer ones weigh less (for example, government bonds near zero, a risky loan 100% or more). Weights here are illustrative; actual ones are set by the regulator.
- **Capital adequacy ratio = capital / RWA.** A minimum applies (from memory, unverified: roughly 9% in India plus buffers, 8% under the international Basel standard).
- The regulator cares because bank failures hurt depositors and the wider economy.
**Worked example:** invented bank: Rs 400 cr corporate loans (weight 100%), Rs 300 cr home loans (50%), Rs 300 cr retail loans (75%). RWA = 400 + 150 + 225 = Rs 775 cr. With capital Rs 100 cr, ratio = 12.9%. After a Rs 20 cr loss, capital 80 / 775 = 10.3%. Rounded to one decimal.
**Likely follow-ups:** 1) *Does lending more lower the ratio?* Yes, RWA rises. 2) *What is Tier 1?* The highest-quality capital, mainly shareholders' equity.
**Common mistakes:** Dividing by total assets, not RWA; forgetting that rising NPAs eat capital; quoting minimums as certain.

### Q79 ⭐⭐ 🟡 What is the India Digital Personal Data Protection Act in plain words, and what two habits should a BFSI analyst follow because of it? (From memory: awareness only, not legal advice.)
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you treat personal data responsibly, not whether you know legal clauses.
**Say this in the interview:** "From memory, it is India's law on handling personal data: take it with consent, use it only for the stated purpose, and protect it. I would follow two habits: use only the data I need, and keep it masked and access-controlled."
**Explain simply:**
- **Personal data** is anything that identifies a person: name, phone, account number, PAN.
- The Act (passed 2023; its rules and timelines are from memory, unverified) is built on consent, a stated purpose, limited collection, accuracy, security and the person's right to ask about, correct or delete their data.
- **Habit 1, minimise:** pull only the columns needed for the analysis; avoid names and phone numbers when an anonymous ID will do.
- **Habit 2, protect and respect purpose:** mask or hash identifiers, share files only through approved channels, and do not reuse data for a purpose the customer did not agree to.
- Employee data deserves the same care, which an HR person already knows well.
**Regulation / privacy note (awareness only):** this is a plain-language summary from memory, unverified, not legal advice; confirm with the legal or compliance team.
**Likely follow-ups:** 1) *Is anonymised data covered?* Truly anonymous data usually falls outside personal-data rules, but weak masking can be reversed. 2) *Who is the owner?* The organisation deciding the purpose; your compliance team can say.
**Common mistakes:** Emailing raw extracts; assuming internal use needs no consent basis; confusing masking with real anonymisation.

### Q80 ⭐⭐ 🟡 What is the PMLA and the purpose of suspicious transaction reporting, in plain words, and where does an analyst's work touch it?
**Asked at:** commonly asked (no company-specific report found); AML alert work appears in KYC/AML prep lists (unverified).
**What the interviewer is checking:** Whether you know the purpose of anti-money-laundering controls and the analyst's careful role.
**Say this in the interview:** "PMLA is India's anti-money-laundering law (the Prevention of Money Laundering Act, from memory). Banks must report suspicious transactions to the financial intelligence authority. As an analyst I help find unusual patterns, but humans decide what is reported."
**Explain simply:**
- **Money laundering** means making illegally earned money look legitimate, often by moving it through many accounts.
- A **suspicious transaction report (STR)** is a confidential filing to the authority (from memory, FIU-IND, unverified) when activity looks unusual for the customer.
- **Where analysts touch it:** building and tuning monitoring rules, such as many small deposits just under a limit, sudden activity on a dormant account, or money in and out quickly; measuring alert volume and false positives; supporting investigators with clean data.
- Alerts are leads, not proof; most turn out harmless.
- **Never tell the customer** an STR is being considered (called "tipping off" in the rules, from memory, unverified).
**Regulation / privacy note (awareness only):** thresholds, timelines and reporting forms are from memory, unverified; confirm with the compliance team. Not legal advice.
**Likely follow-ups:** 1) *What is a false positive?* An alert that turns out normal; too many swamp investigators. 2) *Do you decide to file?* No, the compliance officer does.
**Common mistakes:** Calling every alert fraud; discussing cases outside the team; tuning thresholds only to cut volume.

### Q81 ⭐⭐ 🟡 What are the RBI digital lending guidelines about, at awareness level, and which data fields would a lender need to keep to show the rules are followed?
**Asked at:** commonly asked (no company-specific report found); PhonePe's expansion into lending is noted in the sources, nothing on regulation questions (unverified).
**What the interviewer is checking:** Whether you understand that lending apps must be transparent and auditable.
**Say this in the interview:** "From memory, the guidelines aim to protect borrowers using lending apps: clear cost disclosure, money moving directly between lender and borrower, consent for data use, and a way to complain. An analyst should know which fields prove compliance."
**Explain simply:**
- **Lending service provider (LSP):** the app or firm that finds borrowers for a bank or NBFC (non-bank lender).
- Points usually recalled (from memory, unverified; rules have been revised): a **key fact statement** showing the full cost and charges before the loan; disbursal and repayment directly with the lender's account, not through a third party's pool; a cooling-off period to exit; limits on data collected and storing it with consent; named grievance contact; no hidden fees.
**Data and tables involved:**
- Loan ID, lender, LSP name, application timestamp.
- Key fact statement shown (yes/no, timestamp, version) and APR disclosed.
- Consent log: what data, purpose, time, channel.
- Disbursal account and repayment account, date, amount.
- Fees and charges levied; cooling-off exercised.
- Complaint ID, date, resolution date.
**Regulation / privacy note (awareness only):** details above are from memory, unverified, and change over time; confirm with the compliance team. Not legal advice.
**Likely follow-ups:** 1) *Why timestamps?* To prove order of events. 2) *Why log versions?* To show what the customer actually saw.
**Common mistakes:** Keeping only the final loan table; no consent timestamp; overwriting history.

### Q82 ⭐⭐ 🟡 What is the Account Aggregator framework in plain words, and what does it change for lenders' data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand consent-based data sharing and why it helps lending.
**Say this in the interview:** "From memory, Account Aggregator is an RBI-regulated system where a customer gives consent for their financial data to move from one institution to another, like a bank to a lender. It replaces paper statements with consented, digital data."
**Explain simply:**
- Three roles: the **data provider** (bank holding the data), the **data user** (lender wanting to see it), and the **aggregator**, which carries the data under the customer's consent. The aggregator is meant to pass it on without reading it (from memory, unverified).
- Consent states what data, for how long and for what purpose; the customer can revoke it.
- For lenders: richer, verified, real-time data (bank statements, deposits), less document fraud, better assessment of thin-file people (those without credit history), faster approvals.
- It changes the analyst's inputs: more standardised data, but you must honour the consent's purpose and period.
- Compare: employees giving a payslip to a bank is the manual version.
**Regulation / privacy note (awareness only):** the structure above is from memory, unverified; confirm with the compliance team.
**Likely follow-ups:** 1) *Does the lender keep it forever?* Only as long as the consent allows. 2) *Is it just bank statements?* Other financial data types are included, per memory, unverified.
**Common mistakes:** Treating consent as a one-time tick; keeping data past expiry; thinking the aggregator profits from the data.

### Q83 ⭐⭐ 🟡 What is data-sharing consent, and how should an analyst treat customer data when handing it to an outside vendor or consultant?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Your instinct to protect data when it leaves the organisation.
**Say this in the interview:** "Consent is the customer's clear permission to use their data for a stated purpose. Before sharing with a vendor, I check consent covers it, strip what is not needed, mask identifiers, and use an approved channel and agreement."
**Explain simply:**
- **Consent** should be specific (this purpose), informed (plain language), and withdrawable.
- **Before sharing, check:** is there a business reason, does consent cover this use, is there a signed contract with data-protection terms, has compliance or the data owner approved?
- **Prepare the data:** remove direct identifiers (name, phone, account number); replace with a random ID you can map back internally; share only needed columns and rows; consider aggregated numbers instead.
- **Transfer and track:** approved secure transfer, not personal email; record what was sent, to whom, when; agree on deletion after the work.
- Compare employee data: you would not send raw payroll with names to a consultant.
**Regulation / privacy note (awareness only):** legal duties on sharing with processors are from memory, unverified; confirm with legal and compliance.
**Likely follow-ups:** 1) *Anonymised or masked?* Masked can be reversed with a key; anonymised cannot, but is hard to do well. 2) *What if the consultant asks for everything?* Ask for the purpose and share the minimum.
**Common mistakes:** Sharing "just this once" over email; masking one column but leaving a unique combination such as age, city and salary.

### Q84 ⭐⭐ 🟡 A salary-advance (earned wage access) product uses employer payroll data. What data would you need, what risks exist, and how does an HR background help?
**Asked at:** commonly asked (no company-specific report found); this is a gap-fill question grounded in HR-to-fintech crossover, not a reported question (judgement).
**What the interviewer is checking:** Whether you can use your HR knowledge as a domain edge and spot data and privacy risks.
**Say this in the interview:** "Earned wage access lets employees draw part of salary already earned before payday. I would need payroll and attendance data to know how much is earned, and I would watch data accuracy, repayment and employee privacy."
**Explain simply:**
- **Earned wage access (EWA):** an employee takes, say, 40% of earned-to-date pay early; the amount is recovered from the next salary.
**Data and tables involved:**
- Employee ID, employer ID, date of joining, employment status, grade.
- Payroll: gross and net pay, deductions, pay cycle, last paid date.
- Attendance and leave: days worked to date (earned-to-date estimate).
- Advances: amount, date, recovered or not, repeat usage.
- Exit and notice data: to catch advances to leavers.
- **Risks:** wrong attendance means over-advancing; resignation or termination before payday leaves a recovery gap; repeat users may signal financial stress; employers sharing data without proper employee consent; employees feeling surveilled.
- **Where HR helps:** you know pay cycles, deductions, full-and-final settlement, attrition patterns (early-tenure exits are riskiest), data quality issues in HRIS, and the sensitivity of pay data.
**Regulation / privacy note (awareness only):** whether this is treated as lending or a payroll feature, and consent rules, are from memory, unverified; confirm with compliance and legal. No advice on the product.
**Likely follow-ups:** 1) *Key risk metric?* Share of advances not recovered at payday, by employer and tenure. 2) *What cap would you set?* A policy decision for risk and compliance, not an analyst's call.
**Common mistakes:** Using gross pay as available pay; ignoring leavers; forgetting employee consent and who sees the data.

### Q85 ⭐⭐ 🟡 What workforce metrics would you track for a collections call-centre team (attrition, agent productivity, attendance), and how would they connect to recovery numbers?
**Asked at:** commonly asked (no company-specific report found); collections KPI vocabulary appears in prep guides and a collections analytics job listing (unverified); the workforce link is a gap-fill (judgement).
**What the interviewer is checking:** Whether you can link people data to business outcomes, an HR-to-analytics strength.
**Say this in the interview:** "I would track attrition, tenure mix, attendance and productivity per agent, then show that recovery depends on how many experienced agents are present and working accounts, so staffing problems turn into recovery gaps."
**Explain simply:**
- **Collections:** contacting borrowers who are late and getting them to pay.
- **Attrition:** agents leaving; monthly = leavers / average headcount. Annualising simply multiplies by 12 (about 147% in the example); say which you use.
- **Attendance and absenteeism:** absent agent-days / scheduled agent-days.
- **Productivity:** calls per hour, **right-party contacts** (reaching the actual borrower), promises to pay and share kept, recovery per present agent-day.
- **Tenure mix:** new agents usually recover less and need training, so heavy attrition lowers recovery even if headcount is topped up.
**Worked example:** invented team: 50 agents at month start, 6 leave, 4 join; 48 at end, average 49. Attrition = 6 / 49 = 12.2% monthly. Scheduled agent-days 1,100, absent 110, so absenteeism = 10.0%. Recovery: 12 new agents at Rs 60,000 each (Rs 7,20,000) plus 38 experienced at Rs 1,00,000 each (Rs 38,00,000) = Rs 45,20,000. Replacing 6 experienced with new agents loses 6 x Rs 40,000 = Rs 2,40,000, or 5.3% of recovery. Figures are exercise inputs, not benchmarks.
**Likely follow-ups:** 1) *Correlation or cause?* Control for account mix and bucket difficulty. 2) *Cut by what?* Tenure, team, shift, portfolio bucket.
**Common mistakes:** Comparing agents on different portfolios; counting headcount, not present agents; ignoring ramp-up time.

### Q86 ⭐⭐ 🔴 A personal-loan portfolio's 30+ DPD rate rose from 3% to 4.5% over three months. How would you investigate, and what cuts would you make first?
**Asked at:** commonly asked (no company-specific report found); DPD distribution and portfolio segmentation appear in BFSI analyst job listings (unverified).
**What the interviewer is checking:** Whether you break a headline number into parts before guessing at causes.
**Say this in the interview:** "First I would confirm the number is real and defined the same way in both periods. Then I would split the rise by vintage (month the loan was given), segment, channel, region and lender policy change, to see if it is one pocket or everywhere."
**Explain simply:**
- **DPD (days past due)** is how many days a customer is late. "30+ DPD rate" = loans late by 30 days or more, as a share of all active loans (or of the amount outstanding; say which you use).
- **Step 1, check the metric:** same denominator? Did the book stop growing (a shrinking denominator makes the rate rise with no new defaults)? Any data or system change?
- **Step 2, cut by vintage:** compare loans by the month they were disbursed. If only recent vintages are worse, the cause is how we underwrote (approved) them. If old vintages are worse too, suspect the economy, collections or a region.
- **Step 3, other cuts:** product, income band, bureau score band, channel (own app vs partner), region, employer type, ticket size.
- **Step 4, operations:** did collections capacity, call-centre attendance or attrition drop? Did a payment-mandate failure rise?
**Worked example:** The rise is 4.5 - 3.0 = 1.5 percentage points (a 50% relative rise). Invented book split into three segments (share of loans, old rate, new rate):

| Segment | Share | Old | New | Contribution to the 1.5 pp rise |
|---|---|---|---|---|
| Salaried, loans under 1 year old | 30% | 2.0% | 4.5% | 0.75 pp |
| Salaried, older loans | 50% | 3.0% | 3.5% | 0.25 pp |
| Self-employed | 20% | 4.5% | 7.0% | 0.50 pp |

Contribution = share x change. These sum to 1.5 pp (checked by code). Two pockets explain 1.25 pp (83%), so I would dig into recent salaried and self-employed loans first.
**Likely follow-ups:** 1) *How do you separate mix from behaviour?* Hold segment rates fixed and see how much the rate moves from share shifts alone. 2) *What if everything rose evenly?* Look outside the book: economy, a bureau-wide issue, or collections capacity.
**Common mistakes:** Jumping to "customers are weak" without checking the denominator; looking only at the overall rate; comparing loans of different ages (young loans have not had time to go late).

### Q87 ⭐⭐ 🔴 Collection efficiency in one region fell from 96% to 91% in a month. Walk through what you would check, in order.
**Asked at:** commonly asked (no company-specific report found); collection efficiency is a standard collections KPI in job listings and prep guides (unverified).
**What the interviewer is checking:** A calm, ordered checklist, from data checks to causes to action.
**Say this in the interview:** "I would rule out data and definition issues first, then see which branches, products or buckets lost the 5 points, then look at operations such as staffing, and only then outside causes like floods or festivals."
**Explain simply:**
- **Collection efficiency (CE)** here = money collected in the month divided by money that was due that month. Definitions differ across lenders (some include arrears, some do not); state yours.
- **Order of checks:** (1) Is the data complete: did a payment file or a day of collections fail to load? (2) Was the demand different, for example a large batch of instalments falling due? (3) Which branches, products, collectors or buckets account for the drop? (4) Was it payment mode, such as auto-debit (mandate) bounces rising? (5) Staffing: collector attendance, leave, attrition, vacant areas. (6) Local events: floods, strikes, festivals, a salary delay at a big employer.
- **Check the next month too:** a timing slip often recovers; a real drop does not.
**Worked example:** Invented demand of Rs 200 crore. At 96% CE, collection = 192 crore; at 91%, 182 crore. The gap is 10 crore, which is 5 percentage points of demand. If one branch with 20% of demand collected only 76%, it alone would explain a 4-point fall (0.20 x 20 points), so I would start there.
**Likely follow-ups:** 1) *What if only auto-debit fell?* A bank or mandate issue, not customer intent. 2) *How would staffing connect?* Fewer collectors means fewer contacts and fewer promises kept; compare against attendance data.
**Common mistakes:** Treating percentage points and percent as the same; blaming customers before checking the data load; ignoring changes in demand.

### Q88 ⭐⭐ 🔴 A health insurer's incurred claim ratio rose from 78% to 88% in a year. How would you find out whether it is frequency, severity, mix or pricing?
**Asked at:** commonly asked (no company-specific report found); loss ratio and frequency vs severity feature in insurance analytics prep guides (US/UK oriented, unverified).
**What the interviewer is checking:** Whether you can split a ratio into its ingredients.
**Say this in the interview:** "Incurred claim ratio is claims cost divided by premium earned. So it can rise because claims are more frequent, each claim is bigger, the customer mix changed, or premium per customer fell. I would split it into those four."
**Explain simply:**
- **Incurred claims:** claims paid plus an estimate for claims reported or expected but not yet paid. **Earned premium:** the part of premium that relates to the period of cover already passed.
- **Frequency:** claims per 100 policies. **Severity:** average cost per claim. **Premium per policy:** average earned premium.
- **Identity:** claim ratio = frequency x severity / premium per policy.
- **Mix:** a shift toward older members or costly cities raises the overall ratio even if each group is unchanged. Test by comparing segment by segment.
- **Pricing:** did average premium fall (discounts, a new cheaper plan) or did prices lag medical cost inflation?
**Worked example:** Invented year-on-year changes: frequency +5%, severity +6%, premium per policy -1.4%. Then 78% x 1.05 x 1.06 / 0.986 = 88.0% (checked by code). Share of the rise (log method, a standard way to split multiplied changes): frequency about 40%, severity about 48%, pricing about 12%. Then repeat the split inside each age band or plan to see whether mix explains part of it.
Mix illustration: two groups with claim ratios 70% and 95%. At a 70/30 member split the portfolio is 77.5%; at 50/50 it is 82.5%, a 5-point rise with no change inside either group.
**Likely follow-ups:** 1) *Why use earned premium?* It matches the premium to the cover period of the claims. 2) *Could the reserve estimate be the cause?* Yes, a change in the estimate for unpaid claims moves incurred claims.
**Common mistakes:** Comparing written premium with claims; ignoring mix; forgetting that unpaid-claim estimates are judgement.

### Q89 ⭐⭐ 🔴 A fintech lender's approval rate dropped from 45% to 35% after a model update. How do you tell whether this is good risk control or lost business?
**Asked at:** commonly asked (no company-specific report found); approval-rate and model-change questions are typical in fintech data loops (unverified).
**What the interviewer is checking:** Whether you weigh bad loans avoided against good customers lost.
**Say this in the interview:** "A lower approval rate is only good if the customers we stopped approving were riskier than the ones we kept. I would compare who the old model approved but the new one rejects, and estimate their expected losses against the profit we give up."
**Explain simply:**
- **Approval rate** = approved applications / total applications. A fall can come from the model or from a change in who applies (for example a new marketing channel).
- **Check the applicant mix first:** if applicant quality changed, the drop is not the model.
- **The key group is "old yes, new no".** We never see their repayment, because they were rejected. Estimating it is called reject inference (using similar approved customers, or a small controlled test where some of them are approved).
- **Then compare:** bad-rate of approved loans before and after, profit per good customer, loss per bad one, and conversion funnel changes.
**Worked example:** Per 1,000 applicants: 450 approved before, 350 after, so 100 fewer approvals (a 10 percentage-point fall). Invented assumption: those 100 have a 12% bad rate (12 bad, 88 good), profit Rs 3,000 per good loan, loss Rs 30,000 per bad loan. Lost profit = 88 x 3,000 = Rs 2,64,000; avoided loss = 12 x 30,000 = Rs 3,60,000; net +Rs 96,000, so the update helps under these made-up figures. If their bad rate were much lower, it would not. Sensitivity matters more than the single number.
**Likely follow-ups:** 1) *Which test is cleanest?* A champion-challenger test: route part of traffic to the old model. 2) *What else to watch?* Fairness across groups and approval by channel.
**Common mistakes:** Judging by approval rate alone; ignoring applicant mix; treating rejected applicants as definitely bad.

### Q90 ⭐⭐ 🔴 Fraud losses doubled after a cashback campaign. How would you separate genuine growth from abuse using data?
**Asked at:** commonly asked (no company-specific report found); fraud analytics appears in fintech and AML prep pages (unverified).
**What the interviewer is checking:** Whether you normalise for growth and then look for abuse patterns.
**Say this in the interview:** "I would first ask whether fraud rose faster than business volume. Then I would compare campaign users with non-campaign users and look for patterns such as many accounts per device, or accounts that only earn the cashback and leave."
**Explain simply:**
- **Normalise:** fraud loss per Rs 100 of transaction value (or per 1,000 users), before versus after.
- **Cohorts:** users acquired through the campaign against similar users acquired earlier or elsewhere.
- **Abuse signals:** several accounts on one device, phone, address or bank account; accounts that do the minimum qualifying action and go dormant; round-amount circular transfers between related accounts; unusually fast sign-up bursts.
- **Genuine growth looks like** normal repeat usage and a spread of devices and locations.
**Worked example:** Invented figures: fraud loss Rs 20 lakh to Rs 40 lakh (2.0x); transaction value index 100 to 130 (+30%). Fraud per 100 of value: 0.20 to 0.308, a 54% rise. So growth explains part of the doubling; the rest (a rise in the rate) needs explaining, and campaign cohorts are the first place to look.
**Likely follow-ups:** 1) *How to stop it?* Eligibility rules, limits, device checks, delayed payout; weigh friction against growth. 2) *How to measure incremental growth?* Compare against a holdout group that did not see the offer.
**Common mistakes:** Looking at absolute loss only; punishing all campaign users; forgetting genuine users share devices (families).

### Q91 ⭐ 🟢 What is a stock market index such as Nifty 50, and how is it different from a single share price?
**Asked at:** commonly asked (no company-specific report found); capital-markets basics are a gap-fill for fintech and broking roles.
**What the interviewer is checking:** Basic market literacy, stated simply.
**Say this in the interview:** "An index is a scoreboard that tracks a basket of shares together. Nifty 50 tracks 50 large companies listed on the National Stock Exchange. A share price tracks just one company."
**Explain simply:**
- Think of company-wide average attendance across 50 departments versus the attendance of one department.
- Each company counts in proportion to its size (market value of shares available to the public), so big companies move the index more (method from memory, unverified).
- The index level (for example 22,000) is a number on a scale, not a price you pay; you cannot buy "the index" directly, but funds and products track it.
- A rise in the index does not mean every share rose.
**Likely follow-ups:** 1) *Why do analysts use it?* As a benchmark: is a fund beating the market? 2) *Who decides the 50 companies?* The index provider, with periodic reviews (from memory, unverified).
**Common mistakes:** Treating an index as a company; assuming it is a simple average of prices.

### Q92 ⭐ 🟢 What is a bond, and why does its price fall when interest rates rise? Explain in plain words.
**Asked at:** commonly asked (no company-specific report found); capital-markets basics, gap-fill.
**What the interviewer is checking:** Whether you grasp the intuition without formulas. No investment advice.
**Say this in the interview:** "A bond is a loan to a government or company that pays fixed interest. If new bonds start paying more, my old lower-paying bond is less attractive, so buyers will pay less for it."
**Explain simply:**
- Bond: you lend Rs 100; the borrower pays a fixed interest (coupon) and returns the Rs 100 at the end (maturity).
- If market rates rise from 6% to 8%, a new bond pays Rs 8 a year, but my old one pays Rs 6, so nobody pays Rs 100 for mine; its price drops until its overall return looks competitive.
- Longer-maturity bonds fall more, because you are stuck with the low rate longer.
- HR analogy: an old offer letter at a lower salary looks worse after the market rate rises.
**Likely follow-ups:** 1) *If you hold to maturity?* You still get the face value and interest; the price fall is on paper, unless the borrower defaults. 2) *Why do banks care?* They hold bonds, so rate changes affect their balance sheets.
**Common mistakes:** Thinking bond prices and rates move the same way; forgetting credit risk is separate from rate risk.

### Q93 ⭐ 🟢 What are cash market and futures-and-options (F&O) trading, and why is F&O considered riskier?
**Asked at:** commonly asked (no company-specific report found); broking context, gap-fill.
**What the interviewer is checking:** Whether you can explain leverage plainly (awareness only, no advice).
**Say this in the interview:** "In the cash market you pay for the shares and own them. In F&O you trade contracts whose value depends on a share or index, putting down only a fraction of the value, so gains and losses are magnified."
**Explain simply:**
- **Cash market:** buy a share with full payment, hold as long as you like; the most you can lose is what you paid.
- **Futures:** an agreement to buy or sell at a fixed price on a future date. **Options:** a right, not an obligation, to buy or sell at a set price by a date; the buyer pays a premium. (Details of contract rules from memory, unverified.)
- **Why riskier:** leverage (a small deposit controls a large position), expiry dates (the contract ends), and, for sellers of options, losses can be larger than the money put in.
- Regulators have shown concern about retail losses in F&O (from memory, unverified); analysts at brokers watch activity and loss patterns as a customer-protection signal.
**Likely follow-ups:** 1) *What is margin?* The deposit required to hold a position. 2) *Which brokerage metric is linked?* F&O turnover drives broker revenue.
**Common mistakes:** Calling options "cheap shares"; ignoring expiry; assuming losses are capped in all cases.

### Q94 ⭐ 🟢 What is a co-lending or DLG (default loss guarantee) arrangement between a bank and a fintech, in plain words?
**Asked at:** commonly asked (no company-specific report found); fintech-lending context, gap-fill.
**What the interviewer is checking:** Whether you understand who carries the risk.
**Say this in the interview:** "In co-lending a bank and a fintech fund a loan together and share the interest and risk. In a DLG the fintech promises to cover part of the bank's losses if borrowers default."
**Explain simply:**
- The fintech finds and serves customers; the bank has cheap money and a licence. Co-lending lets both put money in, in an agreed split.
- **DLG:** like a partner saying "if your loans go bad, I will cover the first part of the loss, up to an agreed limit."
- Rules on these arrangements, including caps on guarantees, exist and have changed (from memory, unverified, confirm with the compliance team).
- **Analyst relevance:** reports must show portfolio by lender, share of each, and loss against the guarantee cap.
**Likely follow-ups:** 1) *Why would a bank agree?* New customers, lower acquisition cost. 2) *What would you track?* Delinquency of the shared book and guarantee usage.
**Common mistakes:** Assuming the fintech always lends its own money; ignoring that the guarantee is capped.

### Q95 ⭐ 🟢 What is a thin-file or new-to-credit customer, and what alternative data might a lender consider for them?
**Asked at:** commonly asked (no company-specific report found); credit-underwriting context in BFSI guides (unverified).
**What the interviewer is checking:** Awareness of both the opportunity and the privacy limits.
**Say this in the interview:** "A thin-file customer has little or no credit history, so a bureau score says little. A lender may look at other signs of reliability, but only with consent and where rules allow."
**Explain simply:**
- **Credit bureau:** a company that collects customers' loan and card repayment history and issues a score.
- A first-time borrower, a young employee or a homemaker may have no history, not bad history.
- **Possible alternative data:** salary credits and bank-statement patterns, utility and rent payment history, mobile recharge pattern, GST or business turnover, employer type, education. (Each item is a candidate to test, not a guarantee.)
- **Care points:** use only with consent and for a stated purpose; avoid data that proxies for protected traits; test for fairness (rules from memory, unverified, confirm with legal).
**Likely follow-ups:** 1) *How to start safely?* Small limits, then raise as behaviour builds. 2) *How to validate?* Compare repayment of such customers against the model's prediction.
**Common mistakes:** Treating "no history" as "bad"; using data customers did not consent to; ignoring bias.

### Q96 ⭐ 🟡 What is a broker's revenue model (brokerage, interest on margin funding, distribution fees), and what metrics would a broking analyst track (active clients, ARPU, turnover)?
**Asked at:** commonly asked (no company-specific report found); broking-specific, gap-fill.
**What the interviewer is checking:** That you know where the money comes from and what to measure.
**Say this in the interview:** "A broker earns a fee on trades, interest on money lent to clients to trade, and commissions for selling other products like mutual funds. I would track active clients, revenue per active client, and turnover."
**Explain simply:**
- **Brokerage:** a fee per trade (a flat fee or a percentage). More trades, more revenue.
- **Margin funding:** the broker lends money so clients can trade, charging interest.
- **Distribution fees:** commission from selling mutual funds, insurance or other products.
- **Active client:** someone who traded (or logged in) within a set period; definitions differ, so state yours.
- **ARPU** (average revenue per user) = revenue / active clients. **Turnover** = total value of trades. Also track new accounts, churn, share of F&O, and cost to acquire a client.
**Likely follow-ups:** 1) *Why is revenue volatile?* It follows market activity. 2) *Why track the mix?* F&O clients generate more brokerage per client than cash-only (assumption to test).
**Common mistakes:** Counting all accounts as active; ignoring that revenue follows market cycles.

### Q97 ⭐ 🟡 Calculate a broker's revenue per active client and explain why ARPU can move without new customers.
Data: quarterly revenue Rs 300 crore; active clients 20 lakh.
**Asked at:** commonly asked (no company-specific report found); broking metric, gap-fill.
**What the interviewer is checking:** Unit conversion care and understanding of numerator and denominator.
**Say this in the interview:** "Revenue per active client is Rs 1,500 for the quarter, about Rs 500 a month. It can move because revenue changes or because the count of active clients changes, even with no new sign-ups."
**Explain simply:**
- 1 crore = 1,00,00,000 and 1 lakh = 1,00,000. So Rs 300 crore = Rs 3,000,000,000 and 20 lakh = 2,000,000 clients.
- ARPU = revenue / active clients. It depends on how "active" is defined.
- **Without new customers:** more trading per client (volatile market), a different product mix, fee changes, higher interest income; or the denominator shrinks as clients go inactive (ARPU rises while the business is weaker).
**Worked example:** 3,000,000,000 / 2,000,000 = Rs 1,500 per active client per quarter; divided by 3 = Rs 500 per month; times 4 = Rs 6,000 annualised (a simple run-rate, not a forecast). Scenario A: revenue +10% to Rs 330 crore with the same clients gives Rs 1,650. Scenario B: revenue unchanged, active clients fall 10% to 18 lakh gives Rs 1,667 (rounded). Both raise ARPU; only A is good news.
**Likely follow-ups:** 1) *Better than a mean?* Use the median and bands, since a few heavy traders skew the average. 2) *What to pair with it?* Active-client count and churn.
**Common mistakes:** Mixing crore and lakh; mixing quarterly and annual figures; celebrating ARPU rise when clients are leaving.

### Q98 ⭐ 🟡 What is population stability index (PSI) in model monitoring, and when would a risk team worry about a high value?
**Asked at:** commonly asked (no company-specific report found); model monitoring appears in risk-analytics prep material (unverified).
**What the interviewer is checking:** That you know a model can quietly go stale when the customer population changes.
**Say this in the interview:** "PSI compares how a score or feature was distributed when the model was built with how it looks now. A high value means the population has shifted, so the model may no longer be reliable."
**Explain simply:**
- Split scores into bins. For each bin, compare the old share (expected) with the new share (actual): (actual - expected) x ln(actual / expected), then add up across bins.
- **Common rule of thumb (from memory, unverified):** below 0.1 stable, 0.1 to 0.25 some shift, above 0.25 major shift. Teams set their own limits.
- High PSI says "the inputs changed", not "the model is wrong"; check performance (bad rate by score) next.
- Typical causes: a new marketing channel, a policy change, seasonality, or a data pipeline fault.
**Worked example:** Four score bins, old shares 20%, 30%, 30%, 20%; new shares 10%, 25%, 35%, 30%. Bin terms: 0.069, 0.009, 0.008, 0.041; PSI = 0.127, a moderate shift worth review. With new shares 19%, 31%, 30%, 20%, PSI = 0.0008, stable.
**Likely follow-ups:** 1) *What if PSI is high but performance is fine?* Keep watching; the shift may be harmless. 2) *Can PSI be gamed?* Yes, by bin choice; keep bins consistent.
**Common mistakes:** Using PSI as a performance measure; changing bins between periods; empty bins (division by zero).

### Q99 ⭐ 🟡 What is concentration risk, and how would you measure it in a loan book by sector, geography or borrower?
**Asked at:** commonly asked (no company-specific report found); portfolio risk reporting appears in risk analyst job listings (unverified).
**What the interviewer is checking:** Whether you can put a number on "too many eggs in one basket".
**Say this in the interview:** "Concentration risk is the danger that a big part of the loan book depends on one sector, region or a few borrowers, so one shock hurts a lot. I would measure share of exposure for the top groups and a concentration index."
**Explain simply:**
- **Exposure** = amount lent and outstanding.
- **Simple measures:** share of the top 1, 5 and 10 borrowers; share by sector and by state; share against internal limits.
- **HHI (Herfindahl-Hirschman Index):** square each group's share and add. Higher means more concentrated.
- Like a company where one client pays most of the bills.
**Worked example:** Invented sector shares: Retail 40%, Real estate 25%, Textiles 20%, Power 15%. HHI = 0.4^2 + 0.25^2 + 0.2^2 + 0.15^2 = 0.285 (or 2,850 on the 10,000 scale). Lowest possible with four equal sectors is 0.25, so this book is only slightly more concentrated than equal spread; the effective number of sectors is 1/0.285 = 3.5. Top-3 borrowers of 12%, 8%, 6% = 26% of the book.
**Likely follow-ups:** 1) *Is concentration always bad?* A specialist lender may accept it; it needs limits and monitoring. 2) *Which cut matters?* All three, plus linked borrowers (same group).
**Common mistakes:** Looking only at counts, not amounts; forgetting borrowers under the same parent group; comparing HHI across different scales.

### Q100 ⭐ 🟡 What is stress testing in a bank, and what simple what-if could an analyst run on a loan portfolio?
**Asked at:** commonly asked (no company-specific report found); stress testing is listed in BFSI risk guides (unverified).
**What the interviewer is checking:** That you see it as a structured "what if things go badly" exercise.
**Say this in the interview:** "Stress testing asks how much the bank would lose in a bad scenario, like a recession. A simple version raises default probabilities and loss severity by a set factor and recalculates expected loss."
**Explain simply:**
- **Expected loss** = exposure x probability of default (PD) x loss given default (LGD, the share not recovered).
- A scenario changes the inputs: PD up by 1.5 times, or only real estate PD doubles, or recovery falls.
- Regulators may require formal tests (from memory, unverified); an analyst's simple what-if is a first approximation, not a full model.
**Worked example:** Invented book Rs 1,000 crore: Retail 400 (PD 2%, LGD 45%), SME 300 (4%, 50%), Real estate 300 (3%, 40%). Expected loss = 3.6 + 6.0 + 3.6 = Rs 13.2 crore (1.32% of book). Stress A, all PDs x1.5: 19.8 crore (1.98%), up 6.6 crore. Stress B, only real-estate PD doubled: 16.8 crore. The test shows which segment is most sensitive.
**Likely follow-ups:** 1) *Stress versus forecast?* Stress is a severe but plausible case, not a prediction. 2) *What else changes?* Collateral values and capital needed.
**Common mistakes:** Stressing PD only and leaving LGD alone; treating one scenario as the answer; PD above 100% after multiplying.

### Q101 ⭐ 🟡 What is loan stacking or synthetic identity fraud, and what data signals can reveal it?
**Asked at:** commonly asked (no company-specific report found); fraud analytics in fintech prep pages (unverified).
**What the interviewer is checking:** Which linking keys you would use to spot suspicious patterns.
**Say this in the interview:** "Loan stacking is taking many loans from different lenders at nearly the same time before any shows up on the bureau. Synthetic identity fraud builds a fake person from mixed real and made-up details. In both, shared devices, phones and addresses give them away."
**Explain simply:**
- Lenders learn about other loans only when the bureau updates, which creates a gap that stackers use.
- **Signals:** many applications within days; the same device, phone, email or address across different "customers"; a very new bureau file with high limits; mismatched details such as an ID that does not fit the age.
- **Privacy:** use of device and identity data must follow consent and security rules (from memory, unverified, confirm with the compliance team).
**Worked example (code a candidate might write):**
```sql
-- devices used by more than one customer
select device_id, count(*) as applications,
       count(distinct customer_id) as customers,
       count(distinct lender) as lenders
from applications
group by device_id
having count(distinct customer_id) > 1
order by customers desc;
```
Output on a tiny invented table: D1 (2 applications, 2 customers, 2 lenders) and D4 (2, 2, 2). Plain words: two different people applying from one device across lenders is a lead to review, not proof (family members can share a phone).
**Likely follow-ups:** 1) *Reduce false alarms?* Use several signals together and a review step. 2) *Fix?* Faster bureau reporting and shared-signal checks.
**Common mistakes:** Treating one shared device as proof; ignoring genuine shared households.

### Q102 ⭐ 🟡 What is a mule account, and what patterns in account data can point to one?
**Asked at:** commonly asked (no company-specific report found); AML alert and false-positive analysis appears in prep pages (unverified).
**What the interviewer is checking:** Whether you know the typical "money passes through" pattern.
**Say this in the interview:** "A mule account is one used to move money for someone else, often stolen funds. The typical pattern is money arriving and leaving quickly, with little left behind."
**Explain simply:**
- The mule may be a willing person or an unaware victim lured by a "job offer".
- **Patterns:** a sudden burst after a dormant period; many different senders in, one or few destinations out; out-to-in ratio near 100% within hours; round amounts; new account with high turnover that does not fit the declared income.
- Alerts need human review: many are false alarms (salary passing through to rent, for example).
- Reporting duties exist for suspicious activity (from memory, unverified, confirm with the compliance team). Analysts handle customer data under confidentiality.
**Worked example (code a candidate might write):**
```sql
-- accounts that pass on almost everything they receive
select account_id,
       sum(case when direction = 'IN'  then amount end) as total_in,
       sum(case when direction = 'OUT' then amount end) as total_out,
       round(1.0 * sum(case when direction = 'OUT' then amount end)
                 / sum(case when direction = 'IN' then amount end), 2) as out_to_in
from txns
group by account_id
having out_to_in > 0.9 and total_in >= 50000;
```
Output on a tiny invented table: account 9 with total in 130,000, out 128,500, ratio 0.99. Plain words: it passed on 99% of what it received; add timing (minutes, not days) before flagging.
**Likely follow-ups:** 1) *How to cut false positives?* Combine ratio, speed, new-account age and counterparty count. 2) *What to track?* Precision of alerts reviewed.
**Common mistakes:** Flagging every pass-through; ignoring the time gap; treating every flagged customer as guilty.

### Q103 ⭐ 🟡 How can bias or unfair outcomes creep into credit decisions, and what checks can an analyst run at awareness level?
**Asked at:** commonly asked (no company-specific report found); responsible-lending and scorecard governance appear in risk analyst job descriptions (unverified).
**What the interviewer is checking:** Whether you know a model can be accurate overall and still treat groups unfairly, and that you would test for it.
**Say this in the interview:** "Bias creeps in through the data, the features and the process. As an analyst I would compare approval rates and error rates across groups and flag gaps for the model owner and compliance, not decide fairness on my own."
**Explain simply:**
- **Biased history:** if past loans were approved mostly for one kind of customer, the model learns that pattern. Like a hiring model trained only on past hires from one college.
- **Proxy features:** pin code, device type or employer name can quietly stand in for a protected trait such as religion, caste or gender, even when that trait is not used directly.
- **Missing data:** thin-file customers (little credit history) get declined more simply because there is less data on them.
- **Process bias:** different branches or agents applying overrides unevenly.
- **Awareness-level checks:** compare approval rate, average rate offered and default rate by group; check if a feature behaves very differently across groups; review manual overrides; document findings.
**Regulation / privacy note (awareness only):** Using sensitive personal data to check fairness needs a lawful basis and care; Indian lenders also follow RBI fair-practice expectations (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Equal approval rates mean fair?* Not necessarily; groups can differ in risk, so also compare error rates. 2) *What would you do on finding a gap?* Report it with numbers and let model risk and compliance decide.
**Common mistakes:** Assuming "we do not use gender, so no bias"; treating a gap as proof of discrimination without looking for legitimate causes; running the check without sharing it with compliance.

### Q104 ⭐ 🟡 What is earned versus written premium, and why do insurers report loss ratios on earned premium?
**Asked at:** commonly asked (no company-specific report found); loss ratio and combined ratio appear in insurance analyst prep guides (unverified).
**What the interviewer is checking:** Whether you match cost to the period it relates to.
**Say this in the interview:** "Written premium is the full premium billed when a policy is sold; earned premium is the part of it that belongs to the time already passed. Loss ratio uses earned premium because claims can only arise during cover that has actually happened."
**Explain simply:**
- **Written premium:** the policy price booked on the sale date. Like an annual gym fee paid up front.
- **Earned premium:** the slice for the days of cover already delivered. After 3 months of a 12-month policy, 3/12 is earned; the rest is **unearned** (still a liability, the insurer may have to refund it).
- Claims in a quarter relate to cover given in that quarter, so the matching denominator is earned premium. Using written premium would flatter a fast-growing book.
**Worked example (invented figures):** A 12,000 policy sold on 1 Oct, claims of 2,400 by 31 Dec.
- Earned premium = 12,000 x 3/12 = 3,000.
- Loss ratio on earned = 2,400 / 3,000 = 80%.
- Loss ratio on written = 2,400 / 12,000 = 20%, which hides the problem.
**Likely follow-ups:** 1) *Combined ratio?* Loss ratio plus expense ratio; definitions differ by company. 2) *Which one is higher in a growing book?* Written exceeds earned.
**Common mistakes:** Dividing claims by written premium; forgetting that earning is spread over the policy term.

### Q105 ⭐ 🟡 What is IBNR (incurred but not reported) in plain words, and why can a recent period's loss ratio be understated?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know recent data is incomplete and will move later.
**Say this in the interview:** "IBNR is the estimate for claims that have already happened but have not yet been reported or fully assessed. Recent periods look better than they are because those claims have not arrived in the data yet."
**Explain simply:**
- A claim has a lag: the accident happens, it is reported days or months later, and it is settled later still. Like staff expense claims submitted weeks after the trip.
- Actuaries (insurance statisticians) add a reserve called IBNR to cover this lag; the method is from memory, usually based on how past periods developed.
- If an analyst uses only reported claims for the latest quarter, the loss ratio is understated.
**Worked example (invented figures):** Latest quarter, earned premium 100 (in crore). Reported claims so far 55, so loss ratio 55%. Past patterns suggest final claims of about 70, so the real loss ratio is about 70%, a 15 percentage point gap.
**Likely follow-ups:** 1) *How do you spot it?* Compare the same period's ratio as seen at different dates; it climbs. 2) *Which products suffer most?* Those with slow reporting, such as liability or health.
**Common mistakes:** Celebrating a falling ratio in the newest month; comparing a mature year with an immature one.

### Q106 ⭐ 🟡 What are APE (annualised premium equivalent) and value of new business in life insurance, in plain words, and why are they used instead of total premium?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compare policies that are paid very differently.
**Say this in the interview:** "APE puts regular and one-time premiums on one yearly scale. Value of new business is the profit expected from the policies sold, so it measures quality, not just volume."
**Explain simply:**
- **APE:** regular premium for one year plus 10% of single premium (a common convention; from memory, unverified, companies may differ).
- **Why not total premium:** a single-premium policy brings a big one-time sum but is not repeated income; adding it fully to regular premiums overstates sales.
- **VNB (value of new business):** present value of expected future profit from new policies, after costs and assumptions. **VNB margin** = VNB divided by APE.
**Worked example (invented figures, Rs):** 200 policies at 50,000 a year = 1,00,00,000 regular. 50 single-premium policies at 4,00,000 = 2,00,00,000. Total premium = 3,00,00,000. APE = 1,00,00,000 + 10% of 2,00,00,000 = 1,20,00,000. At an assumed 25% margin, VNB = 30,00,000.
**Likely follow-ups:** 1) *Who sets VNB assumptions?* Actuaries; analysts take it as given. 2) *Can high APE be bad?* Yes, if margin is thin.
**Common mistakes:** Treating APE as revenue or profit; mixing definitions across companies.

### Q107 ⭐ 🟡 What is a bank branch productivity analysis, and which cuts (staff, deposits, loans, footfall) would you use? Include an HR-flavoured staffing metric.
**Asked at:** commonly asked (no company-specific report found); HR-flavoured branch staffing is a gap-fill question.
**What the interviewer is checking:** Whether you compare branches fairly and link business output to people.
**Say this in the interview:** "Branch productivity compares what each branch produces, such as deposits, loans and customer visits, against the staff and cost it uses. A key staffing metric is business per employee."
**Explain simply:**
- **Business per employee:** (deposits plus loans) divided by staff (FTE, full-time equivalents).
- **Footfall per staff per day:** customers entering divided by staff; shows workload.
- **Other cuts:** new accounts per staff, cost per branch, branch age, metro versus rural, vacancy and attrition rate (HR link), share of transactions moved to digital.
- Compare like with like: peer groups by region and size, not one league table.
**Worked example (invented figures, Rs crore, footfall per day):**

| Branch | Staff | Deposits | Loans | Footfall | Business/staff | Footfall/staff |
|---|---|---|---|---|---|---|
| A | 12 | 180 | 120 | 300 | 25.0 | 25.0 |
| B | 8 | 90 | 40 | 200 | 16.25 | 25.0 |
| C | 15 | 150 | 170 | 450 | 21.3 | 30.0 |

Branch A is most productive on business; C is busiest per person, so may be understaffed.
**Likely follow-ups:** 1) *Would you cut staff at B?* Not yet: check branch age and potential. 2) *HR data needed?* Headcount, vacancies, attrition, tenure.
**Common mistakes:** Ranking raw totals; ignoring branch maturity and location.

### Q108 ⭐ 🟡 What is a dormant or inactive account, how is it identified, and what do banks do with such data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can turn a business rule into a data filter.
**Say this in the interview:** "A dormant account has had no customer-initiated transaction for a set period. I identify it from the last transaction date, and banks use the data to reactivate customers and to control fraud risk."
**Explain simply:**
- **Inactive/dormant:** no customer-made debit or credit for a defined time. The exact periods (for example around 12 months inactive and 24 months dormant) are from memory, unverified; check the bank's policy.
- **Identification:** latest customer-initiated transaction date per account, ignoring bank-made entries such as interest credits or fees; days since then compared with the threshold.
- **Uses:** reactivation campaigns, extra checks before allowing a transaction (dormant accounts are a fraud target), and reporting. Like an employee who has not logged in for months.
**Regulation / privacy note (awareness only):** Rules on dormant accounts and unclaimed deposits come from the regulator (from memory, unverified, confirm with the compliance/legal team). Use customer contact data only for permitted purposes.
**Likely follow-ups:** 1) *Why exclude interest credits?* They are not customer activity. 2) *Which table?* Transactions joined to accounts.
**Common mistakes:** Counting any entry as activity; using account opening date instead of last transaction date.

### Q109 ⭐ 🔴 Design a weekly KPI pack for the head of collections of an NBFC: which metrics, which cuts, and which alerts would you include and why?
**Asked at:** collections analytics appears in an SMFG India job listing snippet (unverified); no interview report found.
**What the interviewer is checking:** Whether you can pick few metrics that drive action and define them.
**Say this in the interview:** "Collections means recovering missed loan payments. I would show how much was due versus collected, how accounts move between days-past-due buckets, and how efficient the team is, with alerts when any of them breaks its normal range."
**Explain simply:**
- **Money:** collection efficiency (collected divided by due, definition varies by company; I would state mine), recovery on written-off loans.
- **Movement:** DPD (days past due) bucket distribution and **roll rate** (share of accounts moving to a worse bucket) and cure rate (moving back to current).
- **Team activity:** right-party contact rate (reached the actual borrower), promise-to-pay kept rate, calls per agent, cost to collect.
- **Cuts:** product, region, branch, vintage (month of disbursal), agent or agency, bucket.
- **Alerts:** roll rate above the usual band, a vintage worsening faster than earlier ones, an agency with low kept promises. Keep the pack to one page.
**Likely follow-ups:** 1) *Daily or weekly?* Weekly for trends, plus a daily operations view. 2) *Workforce angle?* Accounts per collector and attrition.
**Common mistakes:** Too many metrics; no definitions; showing averages that hide a bad region or vintage.

### Q110 ⭐ 🔴 A bank wants to reduce false-positive alerts in transaction monitoring by 30% without missing real cases. How would you test and prove a new threshold is safe?
**Asked at:** false-positive threshold tuning appears in a community case (Dataford) and AML prep lists (unverified).
**What the interviewer is checking:** Whether you test on history, count misses and involve compliance.
**Say this in the interview:** "I would replay the new threshold on past alerts with known outcomes and check that confirmed suspicious cases are still caught. I cannot prove zero misses, so I would show the evidence, run it in parallel first, and let compliance approve."
**Explain simply:**
- **False positive:** an alert that investigation closed as not suspicious. Fewer of them frees investigator time.
- **Backtest:** apply the new threshold to a year of past transactions; compare against confirmed cases (including filed reports).
- **Check:** recall (share of real cases still caught) and precision (share of alerts that are real).
- **Safeguards:** shadow mode (run both rules side by side), sample alerts that would be dropped and have investigators review them, monitor after go-live.
**Worked example (invented figures):** Old rule: 1,000 alerts, 20 real, precision 2.0%. New rule: 700 alerts (30% fewer), 19 real, precision 2.7%, recall 95%. One real case is lost. Check what it was. With few real cases the estimate is shaky: if none were missed in 60 real cases, a rough rule of three says the true miss rate could still be up to about 5%.
**Regulation / privacy note (awareness only):** Anti-money-laundering rules expect a documented, risk-based approach; changes need compliance sign-off (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Segments?* Test by customer type, since one global threshold can hide gaps. 2) *After go-live?* Keep a random sample below the threshold under review.
**Common mistakes:** Judging only by fewer alerts; ignoring a lost real case; tuning on the same data used to test.

### Q111 ⭐ 🔴 Persistency fell in one sales channel (bancassurance) but not others. How would you investigate and what would you recommend?
**Asked at:** commonly asked (no company-specific report found); persistency is defined in insurance guides (unverified).
**What the interviewer is checking:** Whether you break a metric down logically before proposing fixes.
**Say this in the interview:** "Persistency is the share of policies still paid up after a set time, for example the 13th month. I would first confirm the drop is real and comparable, then compare the bancassurance mix, branches and sellers against other channels."
**Explain simply:**
- **Bancassurance:** insurance sold through a bank's branches. **Persistency (13th month):** policies still in force at month 13 divided by policies issued (definitions differ by company).
- **Steps:** (1) check the cohort and definition are the same; (2) split by product, premium size, branch, relationship manager, customer age, payment mode; (3) look for a sales-campaign cohort; (4) check complaints about mis-selling (a policy sold without the customer understanding it often lapses); (5) check reminder and auto-debit failures.
- **Recommend:** fix the cause found, such as seller training, mandate setup, or incentives that reward first-year sales only.
**Worked example (invented figures):** Bancassurance 1,500 of 2,000 policies persist = 75.0%; agency 2,610 of 3,000 = 87.0%; online 840 of 1,000 = 84.0%. Bancassurance sits 12 percentage points below agency.
**Likely follow-ups:** 1) *Could mix explain it?* Yes, test by product. 2) *Which data?* Policy, premium receipt, branch and complaints tables.
**Common mistakes:** Jumping to blame sellers; comparing different cohorts; averaging away a few bad branches.

### Q112 ⭐ 🔴 Design a simple early-warning signal set for a retail loan portfolio using repayment, bureau and transaction data, and explain how you would test it.
**Asked at:** early-warning signals appear in credit-risk job listings (unverified); no interview report found.
**What the interviewer is checking:** Whether you pick sensible signals and test them against what happened next.
**Say this in the interview:** "I would pick a few signals that tend to appear before a missed payment, and test whether accounts that trigger them go bad more often than those that do not."
**Explain simply:**
- **Repayment:** late by a few days, partial payments, bounced auto-debit, rising DPD (days past due).
- **Bureau (credit bureau, the shared record of a person's loans):** new loans taken elsewhere, rising enquiries, a drop in score.
- **Transactions:** salary credit stops or falls, balance dips below EMI date, cash withdrawals jump. Like noticing an employee's attendance slip before a resignation.
- **Test:** take past snapshots, record which signals fired, check the default rate over the next 3-6 months (lift versus baseline), alert volume, and false alarms. Check stability by month.
**Regulation / privacy note (awareness only):** Bureau and bank-transaction data must be used with customer consent and only for permitted purposes (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *How many signals?* Few, each explainable to a collector. 2) *What then?* Early contact, not penalty.
**Common mistakes:** Testing on the same period used to pick signals; ignoring alert volume; using data without consent.

### Q113 ⭐ 🔴 How would you build a first-cut risk score for a new-to-credit segment using only repayment history of the first three EMIs, and how would you validate it before use?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can build a simple, explainable score and validate it properly.
**Say this in the interview:** "With only three EMIs I would keep it simple: count missed or late EMIs among the first three and measure how many such borrowers later went bad. Then I would check it on a separate, later group of customers."
**Explain simply:**
- **New-to-credit:** borrowers with no earlier credit record, so repayment behaviour is all we have.
- **Define bad:** for example 90+ days past due within 12 months (state the definition).
- **Build:** features such as number of late EMIs (0 to 3), days late, partial payments; group them into bands and compute the bad rate per band.
- **Validate:** out-of-time test (build on older months, test on newer), check ranking power (does the bad rate rise with the band), stability and bands with few customers. Keep human review.
**Worked example (invented figures):** 10,000 customers, 720 later bad (7.2%).

| Missed of first 3 EMIs | Customers | Bad | Bad rate |
|---|---|---|---|
| 0 | 6,000 | 120 | 2.0% |
| 1 | 2,500 | 200 | 8.0% |
| 2 | 1,000 | 200 | 20.0% |
| 3 | 500 | 200 | 40.0% |

The 1,500 customers (15%) with 2 or 3 misses hold 400 of 720 bads (55.6%).
**Regulation / privacy note (awareness only):** Credit models are usually reviewed by model-risk and compliance teams; check fairness across groups (from memory, unverified).
**Likely follow-ups:** 1) *Why not just 3 EMIs?* Early data is thin; add bureau or income data later. 2) *Metric?* Ranking measures such as Gini or KS (from memory).
**Common mistakes:** Testing on the training data; ignoring customers who prepaid; a tiny band with a noisy rate.
