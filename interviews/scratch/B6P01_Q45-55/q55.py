# Q55: a platform change resets a metric's baseline in week 40; estimate the counterfactual (illustrative, seeded)
import numpy as np
rng = np.random.default_rng(55)

T = 80; BREAK = 40; TRUE_DROP = 0.15; GROWTH = 0.003
t = np.arange(T)
season = 1 + 0.02 * np.sin(2 * np.pi * t / 52)
def series(level, affected):
    y = level * (1 + GROWTH) ** t * season * rng.normal(1, 0.01, T)
    if affected: y = np.where(t >= BREAK, y * (1 - TRUE_DROP), y)
    return y
ios = series(100, True)         # affected platform (new permission prompt)
andr = series(150, False)       # unaffected platform, same underlying trend

# 1) naive: last 8 pre weeks vs first 8 post weeks on the affected series
naive = ios[BREAK:BREAK+8].mean() / ios[BREAK-8:BREAK].mean() - 1
# 2) interrupted time series: fit log-linear trend on pre-break weeks only, project, compare
X = np.c_[np.ones(BREAK), t[:BREAK], np.sin(2*np.pi*t[:BREAK]/52), np.cos(2*np.pi*t[:BREAK]/52)]
beta = np.linalg.lstsq(X, np.log(ios[:BREAK]), rcond=None)[0]
Xp = np.c_[np.ones(8), t[BREAK:BREAK+8], np.sin(2*np.pi*t[BREAK:BREAK+8]/52), np.cos(2*np.pi*t[BREAK:BREAK+8]/52)]
its = np.mean(ios[BREAK:BREAK+8] / np.exp(Xp @ beta)) - 1
# 3) difference-in-differences against the unaffected platform (in logs)
did = np.exp((np.log(ios[BREAK:BREAK+8]).mean() - np.log(ios[BREAK-8:BREAK]).mean())
             - (np.log(andr[BREAK:BREAK+8]).mean() - np.log(andr[BREAK-8:BREAK]).mean())) - 1
print(f"true step {-TRUE_DROP:+.1%} | naive pre/post {naive:+.1%} | interrupted time series {its:+.1%} | diff-in-diff {did:+.1%}")
assert abs(its + TRUE_DROP) < 0.03 and abs(did + TRUE_DROP) < 0.03

# 4) bridge factor and honest YoY at week 60 (4-week averages)
factor = 1 + its                                      # estimated level step
raw_yoy = ios[56:60].mean() / ios[4:8].mean() - 1                  # compares post-break with pre-break
bridged_yoy = (ios[56:60].mean() / factor) / ios[4:8].mean() - 1   # restate to the old definition
true_yoy = (1 + GROWTH) ** 52 - 1
print(f"year-over-year at week 60: raw {raw_yoy:+.1%} | bridged {bridged_yoy:+.1%} | underlying growth {true_yoy:+.1%}")
assert abs(raw_yoy) < 0.06 and 0.10 < bridged_yoy < 0.24 and abs(true_yoy - 0.169) < 0.002
