import numpy as np
rng = np.random.default_rng(2)
# SYNTHETIC classifier: P(unsafe) for 200 truly unsafe and 2000 truly safe messages.
unsafe = rng.beta(5, 2, 200)     # skews high
safe   = rng.beta(1.5, 6, 2000)  # skews low, some overlap
y = np.r_[np.ones(200), np.zeros(2000)]; s = np.r_[unsafe, safe]
print(" thr  precision recall  flagged")
for t in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    pred = s >= t
    tp = (pred & (y==1)).sum(); fp = (pred & (y==0)).sum(); fn = (~pred & (y==1)).sum()
    print(f"{t:.1f}   {tp/max(tp+fp,1):8.3f} {tp/(tp+fn):6.3f}  {pred.sum():6d}")
# synthetic obfuscation: attacker lowers unsafe score by a fixed shift
shifted = np.clip(unsafe - 0.3, 0, 1)
print("recall at 0.5 clean:", round(float((unsafe>=0.5).mean()),3), " obfuscated:", round(float((shifted>=0.5).mean()),3))
