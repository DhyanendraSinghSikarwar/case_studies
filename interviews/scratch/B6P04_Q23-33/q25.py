# Q25: 50,000 of 1,000,000 users sit in both arms (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(25)
N, MIX = 1_000_000, 50_000
pure = N - MIX                                   # 950,000 users on one device only
T_pure = C_pure = pure // 2                      # 475,000 each
print("mixed users as a share of all users:", MIX / N, "; as a share of each arm:", round(MIX / (T_pure + MIX), 4))
assert abs(MIX / (T_pure + MIX) - 0.0952) < 1e-3

mu, sd, tau = 10.0, 5.0, 0.022                    # revenue per user; true effect +2.2%
# model: a mixed user has ONE outcome (own behaviour, exposed to treatment on one device), counted in both arms
y_tp = rng.normal(mu * (1 + tau), sd, T_pure)
y_cp = rng.normal(mu, sd, C_pure)
y_mix = rng.normal(mu * (1 + tau), sd, MIX)      # exposed, so they show the treated level in BOTH arms
mean_T = np.concatenate([y_tp, y_mix]).mean()
mean_C = np.concatenate([y_cp, y_mix]).mean()
obs = mean_T / mean_C - 1
clean = y_tp.mean() / y_cp.mean() - 1
print(f"all-users lift {obs*100:.2f}%; clean lift (pure users only) {clean*100:.2f}%; true {tau*100:.2f}%")
# diluted lift is roughly tau * 475/525
print("dilution factor 475,000/525,000 =", round(T_pure / (T_pure + MIX), 4), "; observed/clean =", round(obs / clean, 3))
assert abs(obs / clean - T_pure / (T_pure + MIX)) < 0.02
assert obs < clean

# the plain-text rule of thumb in the answer: 2% observed implies about 2.2% clean
print("2% / 0.905 =", round(2 / (T_pure / (T_pure + MIX)), 2))
assert abs(2 / (T_pure / (T_pure + MIX)) - 2.21) < 0.01
