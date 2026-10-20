import re
p = "_build/src/cs16.src"; s = open(p, encoding="utf-8").read()
def rep(a, b):
    global s
    assert a in s, a[:70]; s = s.replace(a, b)
rep("| Loans | 12,000 in month 12; legacy size = 0.5–1.6 × average monthly QR (varied);", "| Loans | 12,000 in month 12; legacy size = 0.25–1.7 × average monthly QR (varied by officer/campaign);")
rep("On the 12,000 legacy loans (whose sizes varied 0.5–1.6× monthly inflow)", "On the 12,000 legacy loans (whose sizes varied 0.25–1.7× monthly inflow)")
rep("[0, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.30, 5]", "[0, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 5]")
i = s.index("Evaluated on the 30,000 labelled pairs"); j = s.index("#%% code", i)
s = s[:i] + """Evaluated on the 30,000 labelled pairs: AUC, recall by variant type, and **McNemar** for paired error comparison. The decision policy has **two zones**:
- **Auto-accept** at or above a threshold set so that false accepts are ≤ 0.5% of different-person pairs.
- **Manual review** for everything else, including blank names.

We do not auto-*reject*: a name mismatch is a reason to check, not to refuse a merchant who may simply be "Mohd" on one document and "Mohammed" on another.

""" + s[j:]
i = s.index("def zones(score, y, fa_max=0.005):"); j = s.index("a1, a2 = ACC[", i)
s = s[:i] + '''def accept_threshold(score, y, fa_max=0.005):
    neg = score[y == 0]; ok = [t for t in np.unique(score) if (neg >= t).mean() <= fa_max]     # smallest threshold with ≤ 0.5% impostors at/above it
    return min(ok) if ok else np.inf
mrows, ACC = [], {}
for m_ in MATCHERS:
    s = names[m_].values[nb]; yy = y[nb]; hi = accept_threshold(s, yy); acc = s >= hi; ACC[m_] = acc
    fa = (acc & (yy == 0)).sum(); fa_hi = proportion_confint(fa, (yy == 0).sum(), method="wilson")[1]
    mrows.append((m_, roc_auc_score(yy, s), hi, fa / (yy == 0).sum(), fa_hi, acc[yy == 1].mean(), (~acc).mean(), int(((s >= 99.999) & (yy == 0)).sum())))
mt = pd.DataFrame(mrows, columns=["matcher", "AUC", "accept at/above", "false-accept rate", "FA CI high", "genuine auto-accepted", "share sent to review", "impostors scoring 100"]).set_index("matcher")
''' + s[j:]
rep('''s_h = names["hybrid (set + Jaro–Winkler + initials)"].values; lo, hi = mt.loc["hybrid (set + Jaro–Winkler + initials)", ["reject below", "accept at/above"]]
zone = np.where(blank.values, "review", np.where(s_h >= hi, "auto-accept", np.where(s_h < lo, "auto-reject", "review")))''',
'''s_h = names["hybrid (set + Jaro–Winkler + initials)"].values; hi = mt.loc["hybrid (set + Jaro–Winkler + initials)", "accept at/above"]
zone = np.where(blank.values, "review", np.where(s_h >= hi, "auto-accept", "review"))''')
i = s.index("REVIEW_COST, WRONG_PAYEE_LOSS"); j = s.index("money.round(3)", i)
s = s[:i] + '''avg_loan = pol.loc["4 P20 + risk-tiered cap (12/10/7% / no offer)", "avg loan ₹"]
REVIEW_COST, ABANDON, WRONG_PAYEE_LOSS = 40, 0.05, 0.6 * avg_loan               # ₹40 per review; 5% of reviewed genuine merchants drop out (delay); wrong payee loses 60%
nm_cost = []
for m_ in MATCHERS:
    r = mt.loc[m_]; n_pairs = 1e5; gen_rev = 0.85 * (1 - r["genuine auto-accepted"])
    cost = n_pairs * r["share sent to review"] * REVIEW_COST + n_pairs * gen_rev * ABANDON * 0.12 * avg_loan + n_pairs * 0.15 * r["false-accept rate"] * WRONG_PAYEE_LOSS
    nm_cost.append((m_, r["share sent to review"], cost / 1e5))
print(f"Name-matching cost per 1 lakh disbursals (review ₹{REVIEW_COST}; {ABANDON:.0%} of reviewed genuine merchants abandon, losing a 12% fee on ₹{avg_loan:,.0f}; wrong-payee loss ₹{WRONG_PAYEE_LOSS:,.0f}):")
print(pd.DataFrame(nm_cost, columns=["matcher", "share reviewed", "₹ lakh"]).set_index("matcher").round(3).to_string())
''' + s[j:]
rep("| Token-set ratio | max similarity among {shared words, shared + rest of A, shared + rest of B} |",
    "| Token-set ratio | max similarity among {shared words, shared + rest of A, shared + rest of B}; scores 100 whenever one name's words are a subset of the other's |")
open(p, "w", encoding="utf-8").write(s); print("patched")
