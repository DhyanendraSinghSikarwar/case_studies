import numpy as np
from scipy import stats
from scipy.optimize import minimize
rng = np.random.default_rng(1)
x = rng.normal(5, 2, 1000)
nll = lambda th: -stats.norm.logpdf(x, th[0], np.exp(th[1])).sum()   # th = (mu, log sigma)
r = minimize(nll, [0, 0])
print(r.x[0].round(4), np.exp(r.x[1]).round(4))        # numeric MLE
print(x.mean().round(4), x.std(ddof=0).round(4))       # closed form: same (ddof=0!)
b = rng.binomial(1, 0.3, 500)
grid = np.linspace(0.01, 0.99, 99)
ll = b.sum()*np.log(grid) + (500 - b.sum())*np.log(1 - grid)
print(grid[ll.argmax()], b.mean())                     # grid MLE = sample proportion
