# Q23 rare-disease screening: positive predictive value (illustrative)
N, prev, sens, spec = 20_000, 0.005, 0.90, 0.95
cases = round(N * prev); healthy = N - cases
tp = round(cases * sens); fn = cases - tp
fp = round(healthy * (1 - spec)); tn = healthy - fp
print(f"cases {cases}, healthy {healthy}")
print(f"TP {tp}, FN {fn}, FP {fp}, TN {tn}")
ppv = tp / (tp + fp); npv = tn / (tn + fn)
print(f"flagged {tp+fp}; PPV {ppv:.3%}; NPV {npv:.3%}; false alarms per true case {fp/tp:.1f}")
assert (cases, healthy, tp, fn, fp, tn) == (100, 19_900, 90, 10, 995, 18_905)
assert abs(ppv - 90 / 1085) < 1e-12 and round(ppv, 3) == 0.083
assert round(fp / tp, 1) == 11.1

# PPV changes with prevalence (same test)
print("prevalence -> PPV")
for pv in [0.001, 0.005, 0.02, 0.10, 0.30]:
    p = pv * sens / (pv * sens + (1 - pv) * (1 - spec))
    print(f"  {pv:6.1%} -> {p:.1%}")
assert abs(0.10 * sens / (0.10 * sens + 0.90 * 0.05) - 0.667) < 0.001

# Two-stage workflow: only flagged patients get a second, independent test with the same sens/spec
tp2 = tp * sens; fp2 = fp * (1 - spec)
ppv2 = tp2 / (tp2 + fp2)
print(f"after a second independent test: TP {tp2:.1f}, FP {fp2:.2f}, PPV {ppv2:.1%}, cases still caught {tp2:.0f} of {cases}")
assert abs(ppv2 - 81 / 130.75) < 1e-12 and round(tp2, 1) == 81.0
# Specificity needed for PPV 50% at this prevalence
# PPV=0.5 -> FP = TP = 90 -> 90/19900 false positive rate
need_spec = 1 - 90 / healthy
print(f"specificity needed for PPV 50%: {need_spec:.4f}")
assert round(need_spec, 4) == 0.9955
