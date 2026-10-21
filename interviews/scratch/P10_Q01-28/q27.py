import numpy as np
rng = np.random.default_rng(0)
U = 5000
sess = rng.poisson(5, U) + 1                    # sessions per user
p_user = rng.beta(1, 9, U) * (sess / 6)         # heavy users click more, users differ a lot
p_user = np.clip(p_user, 0, 1)
clicks = rng.binomial(sess, p_user)

ctr = clicks.sum() / sess.sum()
n, mc, ms = U, clicks.mean(), sess.mean()
var = (clicks.var(ddof=1) / ms**2
       - 2 * mc * np.cov(clicks, sess)[0, 1] / ms**3
       + mc**2 * sess.var(ddof=1) / ms**4) / n
se_delta = np.sqrt(var)
se_naive = np.sqrt(ctr * (1 - ctr) / sess.sum())   # treats each session as independent
print(f"CTR={ctr:.4f}  delta SE={se_delta:.5f}  naive session-level SE={se_naive:.5f}")
