import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC data from a known power law L = a * N^(-alpha) with noise; recover alpha by log-log fit
N = np.logspace(6, 10, 9); alpha, a = 0.076, 20.0
L = a * N**(-alpha) * np.exp(rng.normal(0, 0.003, N.size))
slope, icpt = np.polyfit(np.log(N), np.log(L), 1)
print("recovered alpha:", round(-slope, 3), "(true 0.076)")
print("loss ratio when N x10:", round(10**slope, 3))
# extrapolate
print("predicted L at N=1e11:", round(float(np.exp(icpt) * 1e11**slope), 3), " true noiseless:", round(a*1e11**-alpha, 3))
