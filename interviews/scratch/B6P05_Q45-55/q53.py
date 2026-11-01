import numpy as np
from scipy import stats, optimize
stock=100; p_out=0.40; mean_in=70
avg_sales=p_out*stock+(1-p_out)*mean_in
print("average sales:",avg_sales)
assert abs(avg_sales-82)<1e-9

# Model 1: demand ~ Normal(mu, sigma). Unknowns solved from: P(D>=100)=0.4 and E[D | D<100]=70
a=stats.norm.ppf(1-p_out)       # (100-mu)/sigma
lam=stats.norm.pdf(a)/stats.norm.cdf(a)
# mu - sigma*lam = 70 and mu = 100 - a*sigma
sigma=(stock-mean_in)/(a+lam); mu=stock-a*sigma
print(f"Normal fit: mu={mu:.1f}, sigma={sigma:.1f}")
assert abs(mu-91.5)<0.1 and abs(sigma-33.4)<0.1
chk_out=1-stats.norm.cdf(stock,mu,sigma)
chk_in=stats.truncnorm.mean(-np.inf,(stock-mu)/sigma,loc=mu,scale=sigma)
chk_sales=p_out*stock+(1-p_out)*chk_in
print(f"  check: P(sell out) {chk_out:.3f}, mean of non-stockout days {chk_in:.1f}, mean sales {chk_sales:.1f}")
assert abs(chk_out-0.4)<1e-9 and abs(chk_in-70)<1e-6 and abs(chk_sales-82)<1e-6
q80=stats.norm.ppf(0.8,mu,sigma)
print(f"  mean demand {mu:.1f} (vs 82 from sales); 80th percentile {q80:.1f}")
assert mu>82 and q80>stock

# Model 2: lognormal demand, same two facts
def eqs(x):
    m,s=x
    d=stats.lognorm(s,scale=np.exp(m))
    p=d.sf(stock)-p_out
    # E[D | D<100] = integral of x f(x) dx / cdf
    k=(np.log(stock)-m-s*s)/s
    tm=np.exp(m+s*s/2)*stats.norm.cdf(k)/d.cdf(stock)
    return [p,tm-mean_in]
sol=optimize.fsolve(eqs,[4.4,0.4])
m,s=sol; d=stats.lognorm(s,scale=np.exp(m))
print(f"Lognormal fit: mean demand {d.mean():.1f}, 80th percentile {d.ppf(0.8):.1f}")
assert max(abs(np.array(eqs(sol))))<1e-6 and d.mean()>82

# Simulation: what a planner who uses sales as demand does
rng=np.random.default_rng(5)
D=rng.normal(mu,sigma,400_000); D=D[D>=0]
S=np.minimum(D,stock)
print(f"\nSimulated: sell-out share {(D>=stock).mean():.3f}, mean sales {S.mean():.1f}, mean of non-stockout days {D[D<stock].mean():.1f}, true mean demand {D.mean():.1f}")
assert abs(S.mean()-82)<0.6 and abs(D[D<stock].mean()-70)<0.6
# stock level for critical ratio 0.8: planner (mean 82, same sigma) vs censored fit
plan=S.mean()+stats.norm.ppf(0.8)*S.std()
print(f"stock for CR 0.8: planner using sales mean and sd {plan:.0f} (about today's 100) vs fitted 80th percentile {q80:.0f}")
assert abs(plan-100)<2 and plan<q80
# and the 'sales-only' sample sigma is also too small
print("sd of sales (capped at 100):",round(S.std(),1),"vs true demand sd",round(D.std(),1))
assert S.std()<D.std()
