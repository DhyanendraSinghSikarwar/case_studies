# Judge versus human: agreement, rates, kappa, bootstrap interval. Seeded.
import numpy as np
bp, bf, jp_hf, jf_hp = 110, 50, 30, 10
n = bp + bf + jp_hf + jf_hp
assert n == 200
agree = (bp + bf) / n
judge_pass = (bp + jp_hf) / n
human_pass = (bp + jf_hp) / n
pe = judge_pass*human_pass + (1-judge_pass)*(1-human_pass)
kappa = (agree - pe) / (1 - pe)
print("agreement", agree, "judge pass", judge_pass, "human pass", human_pass)
print("chance agreement", round(pe, 4), "kappa", round(kappa, 4))
assert agree == 0.8 and judge_pass == 0.7 and human_pass == 0.6
assert round(pe, 2) == 0.54 and round(kappa, 3) == 0.565
# Error structure
sens = bp / (bp + jf_hp)           # judge passes when human passes
spec = bf / (bf + jp_hf)           # judge fails when human fails
false_pass = jp_hf / (bf + jp_hf)  # judge passes a human-fail output
prec = bp / (bp + jp_hf)           # of judge passes, share human also passes
print("judge pass given human pass", round(sens, 3), "judge fail given human fail", spec, "false-pass rate", false_pass, "precision of judge pass", round(prec, 3))
assert round(sens, 3) == 0.917 and spec == 0.625 and false_pass == 0.375 and round(prec, 3) == 0.786
# Gating risk: of 1,000 outputs with 60% truly good, how many bad ones does the judge pass (illustrative)
bad_passed = 1000 * 0.4 * false_pass
print("bad outputs passed per 1,000 (40% truly bad):", bad_passed)
assert bad_passed == 150
# Bootstrap interval for kappa
rng = np.random.default_rng(11)
cells = np.array([bp, bf, jp_hf, jf_hp])
def k(c):
    c = np.asarray(c, float); nn = c.sum()
    a = (c[0]+c[1])/nn; jp = (c[0]+c[2])/nn; hp = (c[0]+c[3])/nn
    pe = jp*hp + (1-jp)*(1-hp)
    return (a-pe)/(1-pe)
ks = [k(rng.multinomial(n, cells/n)) for _ in range(5000)]
lo, hi = np.percentile(ks, [2.5, 97.5])
print("bootstrap 95% interval for kappa", round(lo, 3), round(hi, 3))
assert 0.43 < lo < 0.50 and 0.64 < hi < 0.70
# Judge net bias: passes 10 points more than humans
print("judge minus human pass rate", round(judge_pass - human_pass, 2))
assert round(judge_pass - human_pass, 2) == 0.10
