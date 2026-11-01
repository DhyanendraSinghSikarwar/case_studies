# Q29: lowering a credit cut-off (illustrative)
n, gain, loss = 4000, 150.0, 600.0
def band(pd_):
    per = (1 - pd_) * gain - pd_ * loss
    return per, per * n
for pd_ in (0.12, 0.22):
    per, tot = band(pd_)
    print(f"default rate {pd_:.0%}: profit per loan {per:+.2f}; monthly band profit {tot:+,.0f}")
assert abs(band(0.12)[0] - 60) < 1e-9 and abs(band(0.12)[1] - 240_000) < 1e-6
assert abs(band(0.22)[0] + 15) < 1e-9 and abs(band(0.22)[1] + 60_000) < 1e-6
be = gain / (gain + loss)
print(f"break-even default rate {be:.1%} (the interval 12% to 22% straddles it)")
assert abs(be - 0.2) < 1e-12 and 0.12 < be < 0.22

# monitoring: how many loans do you need to tell 12% from 20%? pilot default counts with a binomial
from scipy import stats
for m in (300, 1000, 3000):
    se = (0.12 * 0.88 / m) ** 0.5
    # one-sided: P(observed rate >= break-even 20% | true 12%)
    k = int(be * m)
    p_fp = stats.binom.sf(k - 1, m, 0.12)
    # P(observed rate < 20% | true 22%): would wrongly look fine
    p_fn = stats.binom.cdf(k - 1, m, 0.22)
    print(f"pilot {m}: SE at 12% = {se*100:.2f} pts; P(see >=20% if truth 12%) = {p_fp:.4f}; P(see <20% if truth 22%) = {p_fn:.3f}")
assert stats.binom.sf(int(be*1000) - 1, 1000, 0.12) < 1e-4
assert stats.binom.cdf(int(be*1000) - 1, 1000, 0.22) < 0.25

# expected loss of a 1,000-loan pilot at the worst case vs full launch at the worst case
pilot_loss = band(0.22)[0] * 1000
print(f"worst-case pilot of 1,000 loans: {pilot_loss:+,.0f}; worst-case full month: {band(0.22)[1]:+,.0f}")
assert pilot_loss == -15000
# expected value at 50/50 between 12% and 22%
ev = 0.5 * band(0.12)[1] + 0.5 * band(0.22)[1]
print(f"expected monthly profit if 12% and 22% are equally likely: {ev:+,.0f}")
assert ev == 90_000
