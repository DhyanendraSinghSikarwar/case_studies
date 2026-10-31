import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

hours = 14                                   # 08:00 to 22:00
sold_out_at = 18 - 8                         # hours open before sell-out
assert sold_out_at == 10
rate_per_hour = 400 / sold_out_at
uncensored = rate_per_hour * hours
assert rate_per_hour == 40 and uncensored == 560
daily = [400] * 5 + [560, 540]
avg_sales = sum(daily) / 7
avg_demand = (5 * uncensored + 560 + 540) / 7
gap = 1 - avg_sales / avg_demand
print("avg sales:", round(avg_sales, 1), "avg uncensored demand:", round(avg_demand, 1), "understatement:", round(gap, 3))
assert round(avg_sales) == 443 and round(avg_demand, 1) == 557.1 and round(gap, 3) == 0.205
print("hourly rate on non-sellout days:", round(560 / 14, 1), round(540 / 14, 1))

# Test of the flat-hours assumption with a simulated evening peak
profile = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2], float)   # last 4 hours twice as busy (illustrative)
profile /= profile.sum()
total = 720                                  # illustrative true demand; 10/18 of it falls in the first 10 hours
cum = np.cumsum(profile * total)
k = int(np.argmax(cum >= 400 - 1e-9))        # index of the hour in which the stock of 400 runs out
print("peak case: stock-out after hour", k + 1, "of 14; true demand", total)
flat_est = 400 / (k + 1) * hours
print("flat extrapolation from the stock-out hour:", round(flat_est, 1))
assert (k + 1) == 10 and flat_est == 560 and flat_est < total   # evening peak: flat rule understates (560 vs 720)

# Censored model on daily data: normal demand, stock 400 on 5 days (censored), 2 uncensored days
y = np.array(daily, float); cens = np.array([True] * 5 + [False] * 2)
def nll(p):
    mu, ls = p; s = np.exp(ls)
    ll = norm.logpdf(y[~cens], mu, s).sum() + norm.logsf(400, mu, s) * cens.sum()
    return -ll
fit = minimize(nll, [450.0, np.log(80.0)], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-9, "maxiter": 5000})
mu, s = fit.x[0], float(np.exp(fit.x[1]))
print("censored-normal fit on 7 days: mean", round(float(mu), 1), "sd", round(s, 1))
assert mu > avg_sales
assert abs(mu - 550) < 1 and s < 15      # with 2 uncensored days the fit is overconfident: do not trust this sd
