import numpy as np

rng = np.random.default_rng(21)
DAYS, PER_DAY, LAG, DRIFT_DAY = 120, 300, 30, 60
day = np.repeat(np.arange(DAYS), PER_DAY)
# model confidence and truth: before DRIFT_DAY the model is calibrated; after, labels flip more often
conf = rng.uniform(0.6, 0.95, len(day))                 # model's stated probability of being right
p_right = np.where(day < DRIFT_DAY, conf, conf - 0.25)   # real accuracy drops after the world changes
correct = rng.random(len(day)) < p_right
label_arrives = day + LAG

print("prediction-day accuracy (truth, nobody can see this yet) vs what is visible")
print(f"{'seen on day':>11} {'true acc, last 7 pred days':>27} {'matured acc (labels in hand)':>30} {'score-based estimate':>21}")
for t in (50, 70, 85, 89, 95, 110, 119):
    recent = (day > t - 7) & (day <= t)
    true_acc = correct[recent].mean()
    mature = (label_arrives <= t) & (day > t - LAG - 7)           # last 7 days of matured predictions
    mat = correct[mature].mean()
    est = conf[recent].mean()                                      # expected accuracy if calibrated
    print(f"{t:>11} {true_acc:27.3f} {mat:30.3f} {est:21.3f}")
# first day the matured weekly accuracy is clearly below the pre-drift level
base = correct[day < DRIFT_DAY].mean()
for t in range(DRIFT_DAY, DAYS):
    mature = (label_arrives <= t) & (day > t - LAG - 7)
    if mature.sum() and correct[mature].mean() < base - 0.05:
        print(f"\nbaseline acc {base:.3f}; drift began day {DRIFT_DAY}; matured accuracy first shows a 5-point drop on day {t} (lag {t - DRIFT_DAY} days)")
        break
