import numpy as np
from scipy.stats import norm
p1,p2,n=0.100,0.102,20000
se=np.sqrt(p1*(1-p1)/n+p2*(1-p2)/n); d=p2-p1
print("diff",d,"CI",(round(d-1.96*se,4),round(d+1.96*se,4)),"p",round(2*(1-norm.cdf(d/se)),2))
