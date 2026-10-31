import math

def wilson(k, n, z=1.96):
    ph = k / n; d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

n = 200
for name, k in (("omitted medication", 14), ("invented detail", 6)):
    lo, hi = wilson(k, n)
    print(f"{name}: {k}/{n} = {k/n:.3f} | 95% Wilson {lo:.3f} to {hi:.3f}")
assert 14 / n == 0.07 and 6 / n == 0.03
lo14, hi14 = wilson(14, n); lo6, hi6 = wilson(6, n)
assert round(lo14, 3) == 0.042 and round(hi14, 3) == 0.114 and round(lo6, 3) == 0.014 and round(hi6, 3) == 0.064

# the two error types may overlap: summaries with any error is between 14 and 20 of 200
print("any error: between", 14 / n, "and", 20 / n, "(overlap unknown)")
assert 14 / n == 0.07 and 20 / n == 0.10

# zero-error audit sizes: how many clean summaries to show the true rate is below a target (95% one-sided)
for target in (0.05, 0.02, 0.01):
    m = math.ceil(math.log(0.05) / math.log(1 - target))
    print(f"target rate below {target:.0%}: need {m} audited summaries with zero errors (rule of three: 3/{target} = {3/target:.0f})")
assert math.ceil(math.log(0.05) / math.log(0.99)) == 299
assert math.ceil(math.log(0.05) / math.log(0.98)) == 149
assert math.ceil(math.log(0.05) / math.log(0.95)) == 59

# with the observed 7%, how big an audit to pin the rate within +-1 point?
m = math.ceil(1.96 ** 2 * 0.07 * 0.93 / 0.01 ** 2)
print("audit size for +-1 point at p=7%:", m)
assert m == 2501

# severity-weighted harm (invented weights and severity mix, to be set by clinical safety)
w = {"omitted: high-risk drug": 10, "omitted: other": 2, "invented: any": 5}
mix_omit_high = 0.2                      # assumption: 20% of omissions involve a high-risk drug
per_summary = 0.07 * (mix_omit_high * w["omitted: high-risk drug"] + (1 - mix_omit_high) * w["omitted: other"]) + 0.03 * w["invented: any"]
print("severity-weighted harm points per summary:", round(per_summary, 3))
assert round(per_summary, 3) == 0.402
# per 10,000 summaries: errors that reach the patient depend on clinician catch rate
for catch in (0.9, 0.5):
    reach_omit = 10000 * 0.07 * (1 - catch); reach_inv = 10000 * 0.03 * (1 - catch)
    print(f"if signing clinicians catch {catch:.0%} of errors: reaching the record per 10,000 summaries: omissions {reach_omit:.0f}, inventions {reach_inv:.0f}")
assert round(10000 * 0.07 * 0.1) == 70 and round(10000 * 0.07 * 0.5) == 350 and round(10000 * 0.03 * 0.5) == 150

# time: drafting 'saves 4 of 10 min' is a clinician statement, not measured; review time eats it
saved = 4 / 10
print("claimed saving", saved, "= 4 of 10 minutes; if careful checking costs 3 extra minutes the net saving is", 4 - 3, "minutes (", (4 - 3) / 10, ")")
assert (4 - 3) / 10 == 0.1
