# Q41: label-shift estimate (confusion-matrix / BBSE style). Illustrative numbers.
import numpy as np
tpr, fpr = 0.80, 0.10
flag_rate = 0.29          # production share flagged positive (no labels)
train_prior = 0.20

# flag_rate = pi*TPR + (1-pi)*FPR  ->  pi = (flag_rate - FPR) / (TPR - FPR)
pi = (flag_rate - fpr) / (tpr - fpr)
print(f"estimated production prior = {pi:.4f}")
assert abs(pi - 0.19/0.70) < 1e-12 and round(pi, 3) == 0.271

# naive reading would say 29% positive; flag rate at the training prior would have been:
exp_flag_train = train_prior*tpr + (1-train_prior)*fpr
print(f"expected flag rate at prior 0.20 = {exp_flag_train:.3f} (observed {flag_rate})")
assert abs(exp_flag_train - 0.24) < 1e-12

# precision before and after the shift (TPR, FPR assumed unchanged)
prec_old = train_prior*tpr/exp_flag_train
prec_new = pi*tpr/flag_rate
print(f"precision at prior 0.20 = {prec_old:.3f}, at prior {pi:.3f} = {prec_new:.3f}")
assert round(prec_old, 3) == 0.667 and round(prec_new, 3) == 0.749

# prior-odds correction for calibrated probabilities
w = (pi/(1-pi)) / (train_prior/(1-train_prior))
print(f"odds multiplier w = {w:.3f}")
assert round(w, 3) == 1.490
t_old = 0.5
# adjusted p' = p*w/(p*w+1-p); p' >= 0.5  <=>  p >= 1/(1+w)
t_equiv = 1/(1+w)
print(f"a 0.50 cut on adjusted probability = {t_equiv:.3f} on the old probability")
assert round(t_equiv, 3) == 0.402
p = t_equiv; assert abs(p*w/(p*w+1-p) - 0.5) < 1e-12

# uncertainty: n production cases, bootstrap of the flag rate
rng = np.random.default_rng(41)
n = 10_000
flags = rng.random(n) < flag_rate
boots = []
for _ in range(2000):
    fr = rng.choice(flags, n).mean()
    boots.append((fr - fpr)/(tpr - fpr))
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"n={n}: prior 95% interval ({lo:.3f}, {hi:.3f})")
se = np.sqrt(flag_rate*(1-flag_rate)/n)/(tpr-fpr)
print(f"analytic SE = {se:.4f}")
assert 0.0055 < se < 0.0075 and lo < 0.271 < hi

# check the method on simulated data where we know the truth (true prior 0.2714)
true_pi = 0.19/0.70
y = rng.random(200_000) < true_pi
pred = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < fpr)
est = (pred.mean() - fpr)/(tpr - fpr)
print(f"simulation: flag rate {pred.mean():.3f}, estimate {est:.3f}, truth {true_pi:.3f}")
assert abs(est - true_pi) < 0.01
# if the class-conditionals also moved, the estimate is wrong: FPR drifts to 0.14
pred2 = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < 0.14)
est2 = (pred2.mean() - fpr)/(tpr - fpr)
print(f"with FPR secretly 0.14 the same formula says {est2:.3f} (truth {true_pi:.3f})")
assert est2 > true_pi + 0.04
