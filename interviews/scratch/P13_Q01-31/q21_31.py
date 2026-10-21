import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
print("--- Q21")
x = rng.exponential(1,200000)
for n in (10,100,10000,200000): print(n, round(x[:n].mean(),4))
print("--- Q22")
u = rng.uniform(0,1,200000); print(u.mean().round(3), u.var().round(4), 1/12)
lam=2.0; e = -np.log(1-u)/lam; print(e.mean().round(3), stats.kstest(e, 'expon', args=(0,1/lam)).pvalue.round(3))
print("--- Q23")
t = rng.exponential(10, 500000)  # mean 10
print(t[t>10].__sub__(10).mean().round(2), t.mean().round(2))
gaps = rng.exponential(1/5, 100000)  # rate 5/hr
arr = np.cumsum(gaps); counts = np.bincount(np.floor(arr[arr<20000]).astype(int))
print(counts.mean().round(3), counts.var().round(3))
print("--- Q24")
before = rng.normal(100,15,30); after = before + rng.normal(3,4,30)
print(stats.ttest_rel(after,before).pvalue, stats.ttest_ind(after,before).pvalue.round(4))
print("--- Q25")
a = rng.normal(0,1,15); b = rng.normal(0.5,4,60)
print(stats.ttest_ind(a,b).pvalue.round(4), stats.ttest_ind(a,b,equal_var=False).pvalue.round(4))
# type I rate check
f=g=0
for _ in range(4000):
    a=rng.normal(0,1,15); b=rng.normal(0,4,60)
    f+=stats.ttest_ind(a,b).pvalue<0.05; g+=stats.ttest_ind(a,b,equal_var=False).pvalue<0.05
print(f/4000,g/4000)
print("--- Q26")
g1,g2,g3 = rng.normal(10,2,30),rng.normal(10.5,2,30),rng.normal(12,2,30)
print(stats.f_oneway(g1,g2,g3))
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
vals = np.concatenate([g1,g2,g3]); lab = np.repeat(['A','B','C'],30)
print(pairwise_tukeyhsd(vals, lab))
print("--- Q27")
t = np.array([[8,2],[1,5]])
print(stats.fisher_exact(t), stats.chi2_contingency(t, correction=False)[1:3:1][0], stats.chi2_contingency(t,correction=False)[3])
print("--- Q28")
x = rng.exponential(1,200); print(stats.shapiro(x).pvalue)
big = rng.standard_t(8, 20000); print(stats.shapiro(big[:5000]).pvalue)
rej=0
for _ in range(4000):
    a=rng.exponential(1,40); b=rng.exponential(1,40); rej+=stats.ttest_ind(a,b).pvalue<0.05
print(rej/4000)
print("--- Q29")
ref = rng.normal(0,1,5000); live = rng.normal(0.3,1,5000)
print(stats.kstest(ref,'norm'), stats.ks_2samp(ref, live))
print("--- Q30")
import pandas as pd
df = pd.DataFrame({'seg':rng.choice(['A','B','C'],100000,p=[.7,.2,.1])})
df['y'] = df.seg.map({'A':10,'B':30,'C':80}) + rng.normal(0,5,len(df))
srs=[df.y.sample(300,random_state=i).mean() for i in range(500)]
strat=[]
for i in range(500):
    s=df.groupby('seg',group_keys=False).sample(frac=300/len(df),random_state=i); strat.append(s.y.mean())
print(np.std(srs).round(3), np.std(strat).round(3), df.y.mean().round(2))
print("--- Q31")
x = rng.uniform(1,10,200); y = np.exp(x/2)+rng.normal(0,.5,200)
print(stats.pearsonr(x,y)[0].round(3), stats.spearmanr(x,y)[0].round(3), stats.kendalltau(x,y)[0].round(3))
y2 = y.copy(); y2[0]=500; x2=x.copy(); x2[0]=1
print(stats.pearsonr(x2,y2)[0].round(3), stats.spearmanr(x2,y2)[0].round(3))
