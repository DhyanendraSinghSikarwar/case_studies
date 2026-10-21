import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
print("--- Q11")
from statsmodels.stats.power import TTestIndPower
p = TTestIndPower()
for d in (0.2,0.5): print(d, round(p.power(d, 50, 0.05),3), round(p.solve_power(d, power=0.8, alpha=0.05)))
print(round(p.power(0.5,100,0.05),3), round(p.power(0.5,50,0.01),3))

print("--- Q12")
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower
es = proportion_effectsize(0.11, 0.10)
n = NormalIndPower().solve_power(es, power=0.8, alpha=0.05, ratio=1, alternative='two-sided')
print(round(es,4), int(np.ceil(n)))
p1,p2=0.10,0.11; za,zb=stats.norm.ppf(0.975),stats.norm.ppf(0.8)
n2=(za+zb)**2*(p1*(1-p1)+p2*(1-p2))/(p2-p1)**2; print(int(np.ceil(n2)))

print("--- Q13")
from statsmodels.stats.multitest import multipletests
pv = np.concatenate([rng.uniform(0,0.0005,10)*1, rng.uniform(0,1,990)])
print((pv<0.05).sum())
for m in ('bonferroni','holm','fdr_bh'):
    rej = multipletests(pv, alpha=0.05, method=m)[0]; print(m, rej.sum(), rej[:10].sum(), rej[10:].sum())
print(1-0.95**20)

print("--- Q14")
obs = np.array([[90,110],[60,140]])
chi2, p, dof, exp = stats.chi2_contingency(obs, correction=False); print(round(chi2,3), round(p,4), dof); print(exp)
print(stats.chisquare([18,22,20,25,15], f_exp=[20]*5))

print("--- Q15")
x = rng.lognormal(3,1,60); y = rng.lognormal(3.4,1,60)
print(stats.ttest_ind(x,y,equal_var=False).pvalue.round(4), stats.mannwhitneyu(x,y,alternative='two-sided').pvalue.round(4))

print("--- Q16")
data = rng.exponential(30, 80)
boots = np.array([rng.choice(data, data.size, replace=True).mean() for _ in range(10000)])
print(np.percentile(boots,[2.5,97.5]).round(2), data.mean().round(2), boots.std().round(2), stats.sem(data).round(2))
print(stats.bootstrap((data,), np.mean, n_resamples=9999, random_state=0, method='percentile').confidence_interval)

print("--- Q17")
n,p = 1000, 0.003
k = np.arange(0,8)
print(np.round(stats.binom.pmf(k,n,p),4)); print(np.round(stats.poisson.pmf(k,n*p),4))
print(stats.binom.stats(100,0.3), stats.poisson.stats(3))
x = rng.poisson(4,10000); print(x.mean().round(2), x.var().round(2))

print("--- Q19")
pop_var = 4.0; n=5
v0=[];v1=[]
for _ in range(100000):
    s = rng.normal(0,2,n); v0.append(s.var(ddof=0)); v1.append(s.var(ddof=1))
print(np.mean(v0).round(3), np.mean(v1).round(3), np.var(v0).round(3), np.var(v1).round(3))
print(np.mean((np.array(v0)-4)**2).round(3), np.mean((np.array(v1)-4)**2).round(3))

print("--- Q20")
from scipy.optimize import minimize
x = rng.normal(5, 2, 1000)
nll = lambda th: -stats.norm.logpdf(x, th[0], np.exp(th[1])).sum()
r = minimize(nll, [0,0]); print(r.x[0].round(4), np.exp(r.x[1]).round(4), x.mean().round(4), x.std(ddof=0).round(4))
b = rng.binomial(1,0.3,500); print(b.mean())
grid = np.linspace(0.01,0.99,99); ll = b.sum()*np.log(grid)+(500-b.sum())*np.log(1-grid); print(grid[ll.argmax()])
