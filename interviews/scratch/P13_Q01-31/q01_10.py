import numpy as np
from scipy import stats
print("--- Q1")
rng = np.random.default_rng(0)
a = rng.normal(10.0, 2, 200); b = rng.normal(10.5, 2, 200)
t, p = stats.ttest_ind(a, b)
print(round(t,3), round(p,4))
# p-value as "how often would chance alone look this extreme"
diffs = [rng.normal(10,2,200).mean()-rng.normal(10,2,200).mean() for _ in range(5000)]
print(np.mean(np.abs(diffs) >= abs(a.mean()-b.mean())).round(4))
# p-values are uniform when H0 is true
ps = [stats.ttest_ind(rng.normal(0,1,50), rng.normal(0,1,50)).pvalue for _ in range(5000)]
print(np.mean(np.array(ps) < 0.05).round(3))

print("--- Q2")
from statsmodels.stats.power import TTestIndPower
def rejection_rate(delta, n=50, sims=4000):
    rej = 0
    for _ in range(sims):
        x = rng.normal(0, 1, n); y = rng.normal(delta, 1, n)
        rej += stats.ttest_ind(x, y).pvalue < 0.05
    return rej / sims
alpha_hat = rejection_rate(0.0)
power_hat = rejection_rate(0.5)
print(alpha_hat, power_hat, 1-power_hat)
print(TTestIndPower().power(effect_size=0.5, nobs1=50, alpha=0.05))

print("--- Q3")
x = rng.normal(100, 15, 400)
sd = x.std(ddof=1); se = sd/np.sqrt(len(x))
print(round(sd,2), round(se,2), round(stats.sem(x),2))

print("--- Q4")
pop = rng.exponential(1.0, 1_000_000)
print("pop skew", round(stats.skew(pop),2))
for n in (2, 30, 500):
    means = rng.choice(pop, (10000, n)).mean(axis=1)
    print(n, round(stats.skew(means),2), round(means.std(),3), round(1/np.sqrt(n),3))
# CLT breaks: Cauchy
c = rng.standard_cauchy((10000, 500)).mean(axis=1)
print("cauchy mean-of-500 IQR", np.round(np.subtract(*np.percentile(c,[75,25])),2))

print("--- Q5")
true_mu, n, hits = 50, 25, 0
for _ in range(10000):
    s = rng.normal(true_mu, 10, n)
    lo, hi = stats.t.interval(0.95, n-1, loc=s.mean(), scale=stats.sem(s))
    hits += lo <= true_mu <= hi
print(hits/10000)
s = rng.normal(50,10,25); print(np.round(stats.t.interval(0.95, 24, loc=s.mean(), scale=stats.sem(s)),2))

print("--- Q6")
a = rng.normal(0.3,1,40); b = rng.normal(0,1,40)
print(stats.ttest_ind(a,b).pvalue.round(4),
      stats.ttest_ind(a,b,alternative='greater').pvalue.round(4),
      stats.ttest_ind(a,b,alternative='less').pvalue.round(4))

print("--- Q7")
h = rng.normal(170, 10, 500); w = 0.5*h + rng.normal(0, 5, 500)
print(np.cov(h,w)[0,1].round(2), np.corrcoef(h,w)[0,1].round(3))
print(np.cov(h/100,w)[0,1].round(3), np.corrcoef(h/100,w)[0,1].round(3))

print("--- Q8")
z = stats.norm
print([round(z.cdf(k)-z.cdf(-k),4) for k in (1,2,3)], round(z.ppf(0.975),3))
x = rng.normal(60, 8, 300)
zs = (x - x.mean())/x.std(ddof=1); print(zs.mean().round(6), zs.std(ddof=1).round(3))
print(stats.shapiro(x).pvalue.round(3), stats.shapiro(rng.lognormal(0,1,300)).pvalue)
print(stats.probplot(x, dist='norm', fit=True)[1][2].round(4))

print("--- Q9")
x = rng.normal(52, 10, 20)
t = (x.mean()-50)/(x.std(ddof=1)/np.sqrt(20)); print(round(t,3), round(2*stats.t.sf(abs(t),19),4), stats.ttest_1samp(x,50))
print(stats.t.ppf(0.975,[5,20,100,10000]).round(3), stats.norm.ppf(0.975).round(3))

print("--- Q10")
n=200000
a = rng.normal(100,20,n); b = rng.normal(100.4,20,n)
r = stats.ttest_ind(b,a)
d = (b.mean()-a.mean())/np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
diff = b.mean()-a.mean(); se = np.sqrt(a.var(ddof=1)/n + b.var(ddof=1)/n)
print(r.pvalue, round(d,3), round(diff,3), np.round([diff-1.96*se, diff+1.96*se],3))
