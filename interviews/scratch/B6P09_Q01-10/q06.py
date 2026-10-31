from scipy.stats import norm
# Q6 thin-file pilot: illustrative numbers
apps, thin = 100_000, 30_000
pilot, limit, profit, loss = 2_000, 5_000, 1_200, 4_000
exposure = pilot * limit                     # all limits drawn, no recovery: upper bound on balances at risk
max_loss_stated = pilot * loss               # if every pilot customer defaulted at the stated loss per defaulter
be = profit / (profit + loss)                # (1-d)*profit = d*loss
def pilot_profit(d): return pilot * ((1 - d) * profit - d * loss)
print(f"thin-file share {thin/apps:.0%}; pilot is {pilot/thin:.1%} of monthly thin-file applicants")
print(f"exposure upper bound {exposure:,}; loss if all default at stated 4,000 each {max_loss_stated:,}")
print(f"break-even default rate {be:.2%}")
for d in (0.05, 0.10, 0.20, be, 0.30):
    print(f"  default rate {d:5.1%}: pilot profit per month {round(pilot_profit(d)) + 0:>12,}")
se = (0.10 * 0.90 / pilot) ** 0.5
print(f"SE of a 10% default rate on {pilot} loans: {se*100:.2f} points")
# what AUC 0.66 vs 0.82 means: share of defaulters in the worst-scored 20% (equal-variance normal scores)
def capture(auc, p_def=0.10, frac=0.20):
    # scores: good ~ N(0,1), bad ~ N(d,1). Find threshold so that the top `frac` of ALL applicants is flagged.
    d = 2 ** 0.5 * norm.ppf(auc)
    from scipy.optimize import brentq
    t = brentq(lambda t: (1 - p_def) * norm.sf(t) + p_def * norm.sf(t - d) - frac, -5, 8)
    return norm.sf(t - d)
c82, c66 = capture(0.82), capture(0.66)
print(f"defaulters caught in the riskiest 20% of applicants: AUC 0.82 -> {c82:.0%}, AUC 0.66 -> {c66:.0%} (illustrative binormal model)")
assert thin / apps == 0.30 and round(pilot / thin, 3) == 0.067
assert exposure == 10_000_000 and max_loss_stated == 8_000_000
assert round(be, 4) == 0.2308 and abs(pilot_profit(be)) < 1e-6
assert round(pilot_profit(0.05)) == 1_880_000 and round(pilot_profit(0.10)) == 1_360_000 and round(pilot_profit(0.20)) == 320_000
assert round(pilot_profit(0.30)) == -720_000 and round(se * 100, 2) == 0.67
assert c82 > c66 + 0.15
