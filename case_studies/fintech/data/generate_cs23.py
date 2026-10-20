"""
SYNTHETIC DATA GENERATOR - CASE STUDY 23 (YES Bank-style transaction-purpose classification)
============================================================================================
THIS DATA IS SYNTHETIC. Bank transaction narrations are confidential.

Debit transactions of 8,000 retail customers over 6 months, each with a raw bank NARRATION as it appears
in Indian statements, e.g.  "UPI/412345678901/ghar kiraya oct/ramesh.k@okhdfc/HDFC",
"NACH DR TP ACH BAJAJFIN 4567", "NEFT-SCHOOLFEES-DPS RKPURAM-Q2", "POS 4521XX DMART PUNE".
Purpose classes: rent, school_fees, emi_loan, utilities, groceries, fuel, insurance_premium, mf_sip, medical,
family_transfer, online_shopping, dining, travel, salary_to_self (own-account). Narrations are messy: Hinglish,
abbreviations, typos, truncation at 30-40 characters, generic remarks ("payment", "ok").
Labels: a hand-labelled sample (with ~5% labelling errors) for training/validation, and a clean audited test set.
Customer outcome for the downstream test: took a home loan / education loan within 6 months (life-event value).

Calibration anchors (reference file, Case Study 23): "What is each transaction *for* (rent, school fees, etc.)";
~1,000 engineered features; neural networks; accuracy ND; "$250,000 saved annually" from the loyalty programme.
Rates are our assumptions (decision.md D-23-02). Hidden truth columns start with "_".

Outputs: data/cs23/transactions.csv.gz, data/cs23/customers.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
CLASSES = ["rent", "school_fees", "emi_loan", "utilities", "groceries", "fuel", "insurance_premium", "mf_sip", "medical", "family_transfer", "online_shopping", "dining", "travel", "salary_to_self"]
WORDS = {
    "rent": ["rent", "house rent", "kiraya", "ghar kiraya", "flat rent", "rent oct", "pg rent", "room rent", "maintenance+rent", "rnt"],
    "school_fees": ["school fees", "schoolfees", "tuition fee", "term fee", "fees q2", "dps", "kendriya vidyalaya", "admission fee", "school", "fee"],
    "emi_loan": ["emi", "loan emi", "bajajfin", "hdfcltd", "home loan", "tp ach", "achdr", "nach dr", "car loan", "pl emi"],
    "utilities": ["electricity", "bijli bill", "bescom", "msedcl", "tata power", "water bill", "piped gas", "broadband", "jio fiber", "airtel postpaid"],
    "groceries": ["dmart", "big bazaar", "reliance fresh", "kirana", "more retail", "bigbasket", "grocery", "sabzi", "ration", "zepto"],
    "fuel": ["hpcl", "bpcl", "indian oil", "iocl", "petrol", "fuel", "shell", "diesel", "petrol pump", "fuelstation"],
    "insurance_premium": ["lic premium", "lic", "hdfc life", "icici pru", "star health", "policy premium", "insurance", "term plan", "mediclaim", "renewal prem"],
    "mf_sip": ["sip", "mutual fund", "bse star mf", "nse mfss", "groww mf", "zerodha coin", "kuvera", "nippon mf", "axis mf", "icclmf"],
    "medical": ["apollo pharmacy", "hospital", "clinic", "medplus", "1mg", "pharmeasy", "dr ", "diagnostic", "lab test", "medicine"],
    "family_transfer": ["papa", "mummy", "bhai", "didi", "for home", "ghar kharch", "maa", "family", "beta", "send to mom"],
    "online_shopping": ["amazon", "flipkart", "myntra", "meesho", "ajio", "nykaa", "amzn", "fkrt", "snapdeal", "tatacliq"],
    "dining": ["swiggy", "zomato", "restaurant", "cafe", "dominos", "mcdonalds", "dhaba", "food", "kfc", "barbeque"],
    "travel": ["irctc", "makemytrip", "ola", "uber", "redbus", "indigo", "goibibo", "rapido", "metro card", "fastag"],
    "salary_to_self": ["self", "own a/c", "to my sbi", "trf to self", "own account", "savings tfr", "self transfer", "my acct", "to self", "selftrf"],
}
GENERIC = ["payment", "ok", "paid", "upi", "transfer", "pay", "na", "sent", "done", "thanks"]
CH_AMT = {"rent": ("UPI", 15000), "school_fees": ("NEFT", 22000), "emi_loan": ("NACH", 12000), "utilities": ("UPI", 1800), "groceries": ("POS", 1400), "fuel": ("POS", 1600),
          "insurance_premium": ("NACH", 9000), "mf_sip": ("NACH", 5000), "medical": ("UPI", 1500), "family_transfer": ("UPI", 6000), "online_shopping": ("UPI", 1700),
          "dining": ("UPI", 650), "travel": ("UPI", 2200), "salary_to_self": ("IMPS", 20000)}


def _typo(rng, w):
    if len(w) < 5 or rng.random() > 0.15: return w
    i = rng.integers(1, len(w) - 1); return w[:i] + w[i + 1:]


def narration(rng, cls):
    ch, _ = CH_AMT[cls]
    if rng.random() < 0.15: ch = rng.choice(["UPI", "IMPS", "NEFT"])
    kw = _typo(rng, rng.choice(WORDS[cls])) if rng.random() > 0.12 else rng.choice(GENERIC)
    ref = str(rng.integers(10 ** 11, 10 ** 12))
    if ch == "UPI":
        vpa = rng.choice(["ramesh.k", "flatowner", "dmart", "merchant", "9876543210", "paytmqr", "bharatpe", "anita.s", "school.fees", "lic"]) + "@" + rng.choice(["okhdfc", "ybl", "paytm", "okaxis", "oksbi", "ibl"])
        s = f"UPI/{ref}/{kw}/{vpa}/{rng.choice(['HDFC', 'SBIN', 'ICIC', 'UTIB', 'YESB'])}"
    elif ch == "NACH": s = f"NACH DR {rng.choice(['TP ACH', 'ACH D-', 'ECS'])} {kw.upper()} {rng.integers(1000, 9999)}"
    elif ch == "NEFT": s = f"NEFT-{kw.upper().replace(' ', '')}-{rng.choice(['DPS', 'SHARMA', 'CORP', 'TRUST', 'PVT LTD'])}-{ref[:6]}"
    elif ch == "IMPS": s = f"IMPS/P2A/{ref}/{kw}/{rng.choice(['XXXX1234', 'XXXX9876'])}"
    else: s = f"POS {rng.integers(4000, 4999)}XX {kw.upper()} {rng.choice(['PUNE', 'BLR', 'MUM', 'DEL', 'HYD'])}"
    return s[: rng.integers(32, 60)], ch


def generate(seed=SEED, n_cust=8_000):
    rng = np.random.default_rng(seed)
    renter = rng.random(n_cust) < 0.32; parent = rng.random(n_cust) < 0.28; borrower = rng.random(n_cust) < 0.35; investor = rng.random(n_cust) < 0.22
    income = np.exp(rng.normal(np.log(55000), 0.5, n_cust))
    rows = []
    for c in range(n_cust):
        mix = {"utilities": 3, "groceries": 6, "fuel": 3, "medical": 1, "family_transfer": 2, "online_shopping": 4, "dining": 4, "travel": 2, "salary_to_self": 1,
               "rent": 6 * renter[c], "school_fees": 1.5 * parent[c], "emi_loan": 6 * borrower[c], "insurance_premium": 1, "mf_sip": 6 * investor[c]}
        k = rng.poisson(30); p = np.array([mix[x] for x in CLASSES], float); p /= p.sum()
        for cls in rng.choice(CLASSES, k, p=p):
            nar, ch = narration(rng, cls); amt = np.round(CH_AMT[cls][1] * np.exp(rng.normal(0, 0.5)), 0)
            rows.append((f"C{c:05d}", nar, ch, amt, cls))
    tx = pd.DataFrame(rows, columns=["customer_id", "narration", "channel", "amount_inr", "_purpose"])
    tx.insert(0, "txn_id", [f"T{i:07d}" for i in range(len(tx))])
    # labelling: 12% hand-labelled (train/val, 5% label noise), 4% audited test (clean)
    u = rng.random(len(tx)); tx["split"] = np.where(u < 0.12, "labelled", np.where(u < 0.16, "audited_test", "unlabelled"))
    noisy = (tx.split == "labelled") & (rng.random(len(tx)) < 0.05)
    tx["label"] = np.where(tx.split == "unlabelled", "", tx._purpose)
    tx.loc[noisy, "label"] = rng.choice(CLASSES, noisy.sum())
    # customer outcomes for the downstream test (life events -> loans)
    cust = pd.DataFrame({"customer_id": [f"C{c:05d}" for c in range(n_cust)], "monthly_income": np.round(income, -2), "age": np.clip(rng.normal(36, 9, n_cust), 21, 65).round(),
                         "_renter": renter.astype(int), "_parent": parent.astype(int)})
    cust["took_home_loan_6m"] = (rng.random(n_cust) < expit(-4.4 + 1.6 * renter + 0.4 * np.log(income / 55000) + 0.02 * (cust.age - 36))).astype(int)
    cust["took_education_loan_6m"] = (rng.random(n_cust) < expit(-4.8 + 1.8 * parent + 0.2 * np.log(income / 55000))).astype(int)
    # data-quality defects
    tx.loc[tx.sample(n=300, random_state=seed).index, "narration"] = ""                                # blank narrations from a legacy core system
    tx = pd.concat([tx, tx.sample(n=400, random_state=seed + 1)], ignore_index=True)
    return tx, cust


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs23"), exist_ok=True)
    t, c = generate(); t.to_csv(os.path.join(here, "cs23", "transactions.csv.gz"), index=False); c.to_csv(os.path.join(here, "cs23", "customers.csv.gz"), index=False)
    print(len(t), "txns |", t.split.value_counts().to_dict()); print(t.sample(8, random_state=3)[["narration", "_purpose"]].to_string())
    print(c[["took_home_loan_6m", "took_education_loan_6m"]].mean().round(4).to_dict())
