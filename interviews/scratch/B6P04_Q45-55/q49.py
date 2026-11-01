# Q49: LLM judge vs humans, self-preference (illustrative)
import numpy as np
from scipy import stats
rng = np.random.default_rng(49)
print("judge win rate:", 1160/2000, " humans:", round(153/300, 3))
assert 1160/2000 == 0.58 and round(0.51*300) == 153
se_j = np.sqrt(.58*.42/2000); se_h = np.sqrt(.51*.49/300)
print("judge 95% CI:", round(.58-1.96*se_j, 3), round(.58+1.96*se_j, 3), "| human 95% CI:", round(.51-1.96*se_h, 3), round(.51+1.96*se_h, 3))
z = (.58-.51)/np.sqrt(se_j**2 + se_h**2); print("two-sample z", round(z, 2), "p =", round(2*stats.norm.sf(z), 3))
assert 0.45 < .51-1.96*se_h < 0.46 and .51+1.96*se_h > .5
# simulate a judge with real signal + self-preference + position bias; humans see only quality
N = 20_000
quality = rng.normal(0.05, 1.0, N)                    # treatment's true quality edge per pair (tiny)
human_p = 1/(1+np.exp(-0.2*quality))
human = rng.random(N) < human_p
def judge(self_bonus, pos_bonus, swap):
    # swap=True means treatment is shown second; position bias favours slot A
    pos = -pos_bonus if swap else pos_bonus
    p = 1/(1+np.exp(-(0.9*quality + self_bonus + pos)))
    return rng.random(N) < p
j1 = judge(0.35, 0.15, swap=False); j2 = judge(0.35, 0.15, swap=True)
both = (j1 & j2)                                        # treatment wins in BOTH orders
print("judge treatment win, treatment in slot A:", round(j1.mean(), 3), " slot B:", round(j2.mean(), 3))
print("average over both orders:", round((j1.mean() + j2.mean())/2, 3))
cross = judge(0.0, 0.15, swap=False); cross2 = judge(0.0, 0.15, swap=True)
print("cross-family judge (no self bonus), averaged over orders:", round((cross.mean()+cross2.mean())/2, 3), "| human:", round(human.mean(), 3))
assert j1.mean() > j2.mean()                           # position bias visible
assert (j1.mean()+j2.mean())/2 - (cross.mean()+cross2.mean())/2 > 0.05
# calibrate on 300 human-labelled pairs: use judge order-averaged verdict; check agreement
idx = rng.choice(N, 300, replace=False)
jv = j1[idx]                                          # the judge's single verdict, treatment shown first
hv = human[idx]
agree = (jv == hv).mean(); pe = jv.mean()*hv.mean() + (1-jv.mean())*(1-hv.mean())
print("raw agreement", round(agree, 3), "Cohen kappa", round((agree-pe)/(1-pe), 3))
assert (agree-pe)/(1-pe) < 0.4
