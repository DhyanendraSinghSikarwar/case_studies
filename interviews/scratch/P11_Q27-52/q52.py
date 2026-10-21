import numpy as np
from scipy.stats import norm
mu, sigma = 40, 12                 # forecast demand until next delivery (units), illustrative
price, cost, waste = 100, 70, 70   # margin 30 if sold; unsold unit loses its cost (perishable)
cu, co = price - cost, waste       # underage / overage cost
crit = cu / (cu + co)
q = norm.ppf(crit, mu, sigma)
print("critical ratio:", round(crit, 3), "-> order up to", round(q, 1), "(mean demand 40)")
