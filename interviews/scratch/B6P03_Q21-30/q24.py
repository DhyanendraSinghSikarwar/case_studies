# Q24 LLM-labelled tickets: audit sizing and honest evaluation (illustrative; refund share is an assumption)
import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

audit, agree = 500, 440
err = audit - agree
lo, hi = wilson(agree, audit)
print(f"overall agreement {agree/audit:.1%}, 95% Wilson CI {lo:.1%} to {hi:.1%}; errors {err}")
assert err == 60 and abs(agree / audit - 0.88) < 1e-12 and 0.84 < lo < 0.85 and 0.90 < hi < 0.91

# Assume (illustrative) 100 of the 500 audited tickets truly belong to the refund class
refund_n, refund_err = 100, 45
oth_n, oth_err = audit - refund_n, err - refund_err
print(f"refund: {refund_n-refund_err}/{refund_n} correct = {(refund_n-refund_err)/refund_n:.0%}; others: {oth_n-oth_err}/{oth_n} = {(oth_n-oth_err)/oth_n:.2%}")
rl, rh = wilson(refund_n - refund_err, refund_n)
print(f"refund accuracy 95% CI {rl:.1%} to {rh:.1%}")
assert (oth_n, oth_err) == (400, 15) and abs(refund_err / err - 0.75) < 1e-12
assert (refund_n - refund_err) / refund_n == 0.55

# Audit size for +-5 percentage points on the refund accuracy (worst case p = 0.5)
need_refund_rows = math.ceil(1.96 ** 2 * 0.25 / 0.05 ** 2)
share = refund_n / audit
print(f"refund rows needed {need_refund_rows}; random audit size at {share:.0%} refund share: {math.ceil(need_refund_rows/share):,}")
assert need_refund_rows == 385 and math.ceil(385 / 0.2) == 1925

# A perfect copycat of the LLM labels copies its errors, so against the same humans it scores the LLM's own agreement
copycat_vs_llm, copycat_vs_human = 1.0, agree / audit
print(f"perfect copycat: {copycat_vs_llm:.0%} against LLM labels, {copycat_vs_human:.0%} against human labels")
assert copycat_vs_human == 0.88
