import numpy as np
from scipy.stats import pearsonr,spearmanr
rng=np.random.default_rng(0)
x=rng.uniform(0,5,200); y=np.exp(x)+rng.normal(0,1,200)
print("monotone nonlinear: pearson %.2f spearman %.2f"%(pearsonr(x,y)[0],spearmanr(x,y)[0]))
x=rng.uniform(-3,3,200); y=x**2+rng.normal(0,.1,200)
print("U-shape: pearson %.2f spearman %.2f"%(pearsonr(x,y)[0],spearmanr(x,y)[0]))
x=rng.normal(size=50); y=x+rng.normal(0,.5,50); x2=np.append(x,20); y2=np.append(y,-20)
print("outlier: pearson %.2f -> %.2f ; spearman %.2f -> %.2f"%(pearsonr(x,y)[0],pearsonr(x2,y2)[0],spearmanr(x,y)[0],spearmanr(x2,y2)[0]))
