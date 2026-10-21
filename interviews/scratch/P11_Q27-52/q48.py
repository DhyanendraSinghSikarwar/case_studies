import numpy as np
rng = np.random.default_rng(4)
n = 100_000
conv = rng.random(n) < 0.05                     # true eventual converters
delay = rng.exponential(3, n)                   # days from click to conversion
age = rng.uniform(0, 14, n)                     # days since click when we train
seen_pos = conv & (delay <= age)
print("true CVR:", round(conv.mean(), 4), "| naive observed CVR:", round(seen_pos.mean(), 4))
# fix: only trust clicks older than a window, and use delay CDF to correct younger ones
F = 1 - np.exp(-age / 3)                        # P(conversion already observed | converter)
adj = (seen_pos / np.clip(F, 0.05, 1)).mean()
print("delay-corrected CVR:", round(adj, 4))
