# Q3 prevalence and PPV: illustrative numbers
def table(prev, n=10_000, se=0.90, sp=0.95):
    d = round(n * prev); h = n - d
    tp = round(d * se); fn = d - tp
    fp = round(h * (1 - sp)); tn = h - fp
    return dict(sick=d, tp=tp, fn=fn, fp=fp, tn=tn, ppv=tp / (tp + fp), npv=tn / (tn + fn), pos=tp + fp)
ref, clinic = table(0.20), table(0.01)
for name, t in (("referral 20%", ref), ("clinic 1%", clinic)):
    print(f"{name}: sick {t['sick']}, TP {t['tp']}, FP {t['fp']}, FN {t['fn']}, positives {t['pos']}, PPV {t['ppv']:.1%}, NPV {t['npv']:.2%}")
print(f"patients flagged per true case found: referral {ref['pos']/ref['tp']:.2f}, clinic {clinic['pos']/clinic['tp']:.2f}")
# the same result from Bayes' rule on a single patient
p = 0.01 * 0.90 / (0.01 * 0.90 + 0.99 * 0.05)
print(f"Bayes check at 1%: {p:.1%}")
# what prevalence would be needed for a PPV of 50%?
prev50 = 0.05 / (0.90 + 0.05)  # solve prev*0.9 = (1-prev)*0.05
print(f"prevalence at which PPV = 50%: {prev50:.1%}")
assert (ref['tp'], ref['fp'], ref['fn']) == (1800, 400, 200) and round(ref['ppv'], 3) == 0.818
assert (clinic['tp'], clinic['fp'], clinic['fn']) == (90, 495, 10) and round(clinic['ppv'], 3) == 0.154
assert clinic['pos'] == 585 and ref['pos'] == 2200
assert abs(p - clinic['ppv']) < 1e-3
assert round(prev50, 4) == 0.0526 and round(ref['npv'], 4) == 0.9744 and round(clinic['npv'], 4) == 0.9989
assert round(clinic['pos'] / clinic['tp'], 1) == 6.5 and round(ref['pos'] / ref['tp'], 2) == 1.22
