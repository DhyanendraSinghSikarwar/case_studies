# Q11: outliers vs entry errors in a payments table (illustrative numbers)
import numpy as np
rng = np.random.default_rng(11)
N = 100_000
# 99,800 ordinary retail rows, median about 800 rupees
retail = rng.lognormal(np.log(800), 1.0, 99_800)
# 80 genuine corporate payments (customers with a history of large payments)
corp_prior_max = rng.uniform(1.0e6, 6.0e6, 80)
corp_amt = corp_prior_max * rng.uniform(0.5, 1.5, 80)
corp_amt = np.maximum(corp_amt, 1.05e6)
# 120 entry errors: a retail amount typed with three extra zeros
true_small = rng.uniform(1_100, 5_000, 120)
err_amt = true_small * 1000
err_prior_max = rng.uniform(2_000, 20_000, 120)       # retail customers' own history
# the 10 corporate rows below are first-time large payers: no history to compare with
new_big = rng.choice(80, 10, replace=False)
corp_prior_max[new_big] = 0

amount = np.concatenate([retail, corp_amt, err_amt])
prior_max = np.concatenate([np.full(99_800, 5_000.0), corp_prior_max, err_prior_max])
is_error = np.concatenate([np.zeros(99_800 + 80, bool), np.ones(120, bool)])
settled = np.where(is_error & (np.arange(N) >= 99_880), amount / 1000, amount)  # bank ledger amount

big = amount > 1_000_000
print("rows > 1,000,000:", big.sum(), "share:", f"{big.mean():.3%}", " median:", round(float(np.median(amount))))
assert big.sum() == 200 and abs(np.median(amount) - 800) < 20

# Evidence 1: ledger mismatch.  Evidence 2: amount versus the customer's own largest earlier payment.
mismatch = big & (np.abs(settled - amount) / amount > 0.5)
ratio = np.where(prior_max > 0, amount / np.maximum(prior_max, 1), np.inf)
history_ok = big & (ratio <= 3)                      # in line with own history
auto_error = mismatch | (big & (prior_max > 0) & (ratio >= 100))       # far above own history, or ledger disagrees
review = big & ~auto_error & (prior_max == 0)        # no history and no mismatch: a human looks
keep = big & ~auto_error & ~review
print(f"auto-error {auto_error.sum()}  keep {keep.sum()}  review queue {review.sum()}")
tp = (auto_error & is_error).sum(); fp = (auto_error & ~is_error).sum()
print(f"auto-error rule: caught {tp} of {is_error.sum()} errors, wrongly flagged {fp} genuine")
assert auto_error.sum() == 120 and tp == 120 and fp == 0 and review.sum() == 10 and keep.sum() == 70

# Repair the errors: divide by 1000 (the ledger value) and keep a flag column
fixed = np.where(auto_error, settled, amount)
def mean_log(a): return float(np.mean(np.log1p(a)))
cap = np.quantile(amount, 0.999)
clipped = np.minimum(amount, cap)
print(f"mean amount: raw {amount.mean():,.0f}  fixed {fixed.mean():,.0f}  clipped at p99.9 ({cap:,.0f}) {clipped.mean():,.0f}")
print(f"genuine corporate rows after clip: largest {clipped[~is_error & big].max():,.0f} vs real {amount[~is_error & big].max():,.0f}")
assert 1.9 < amount.mean() / fixed.mean() < 2.0
assert clipped[~is_error & big].max() < amount[~is_error & big].max()
print("log-scale mean: raw", round(mean_log(amount), 3), "fixed", round(mean_log(fixed), 3))
