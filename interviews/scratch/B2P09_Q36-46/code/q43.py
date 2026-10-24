# SYNTHETIC canary eval for a silent provider update. Mock provider; daily run of the same 150 prompts on the alias and on a pinned snapshot.
import math, random
random.seed(33)
N = 150
prompt_difficulty = [random.random() for _ in range(N)]          # fixed canary prompts (assumed latent difficulty)
def pass_prob(version, d, fmt_broken_subset):
    base = 0.97 - 0.5 * d ** 2                                   # easier prompts pass more often
    if version == "new" and fmt_broken_subset: base -= 0.35      # silent update breaks a slice (assumed: prompts with index % 5 == 0)
    return max(0.02, base)
def daily_run(version):
    return [random.random() < pass_prob(version, prompt_difficulty[i], i % 5 == 0) for i in range(N)]
def sign_test_p(b, c):                                           # exact two-sided sign test on discordant pairs (McNemar exact)
    n = b + c
    if n == 0: return 1.0
    k = min(b, c); p = 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, p)
# brute-force check of the sign test against direct enumeration of a fair coin
import itertools
bf = sum(1 for bits in itertools.product([0, 1], repeat=12) if min(sum(bits), 12 - sum(bits)) <= 2) / 2 ** 12
print("sign-test check: exact p(b=2,c=10) =", round(sign_test_p(2, 10), 5), " brute force:", round(bf, 5))
# A) false-alarm rate: 200 days where alias and pinned are the SAME model (both 'old'), alpha = 0.01
false_alarms = 0
for _ in range(200):
    x, y = daily_run("old"), daily_run("old")
    b = sum(1 for p, q in zip(x, y) if p and not q); c = sum(1 for p, q in zip(x, y) if q and not p)
    false_alarms += sign_test_p(b, c) < 0.01
print(f"no real change: {false_alarms}/200 days flagged at alpha=0.01 (expect about 2)")
# B) real silent update on day 10: alias becomes 'new', pinned snapshot stays 'old'
print("\nday  alias_acc  pinned_acc  only-pinned-right  only-alias-right  p_value  alert(0.01)")
tb = tc = 0
for day in range(8, 16):
    ver = "old" if day < 10 else "new"
    a, p = daily_run(ver), daily_run("old")
    b = sum(1 for x, y in zip(a, p) if y and not x); c = sum(1 for x, y in zip(a, p) if x and not y)
    pv = sign_test_p(b, c)
    if day >= 10 and day <= 12: tb += b; tc += c
    print(f"{day:3d}  {sum(a)/N:.3f}      {sum(p)/N:.3f}       {b:3d}                {c:3d}               {pv:.4f}  {'ALERT' if pv < 0.01 else '-'}")
print(f"pooled days 10-12: only-pinned-right {tb}, only-alias-right {tc}, p = {sign_test_p(tb, tc):.5f}")
# power: how often does ONE day alert at alpha=0.01, for canary sizes 150 vs 600 prompts? (same assumed 30%-slice, 0.35 drop)
def power(n_prompts, reps=300):
    global N, prompt_difficulty
    saveN, saved = N, prompt_difficulty
    N = n_prompts; prompt_difficulty = [random.random() for _ in range(N)]; hit = 0
    for _ in range(reps):
        a, p = daily_run("new"), daily_run("old")
        b = sum(1 for x, y in zip(a, p) if y and not x); c = sum(1 for x, y in zip(a, p) if x and not y)
        hit += sign_test_p(b, c) < 0.01
    N, prompt_difficulty = saveN, saved
    return hit / reps
print("single-day detection rate at alpha=0.01:  150 prompts", round(power(150), 3), "  600 prompts", round(power(600), 3))
# C) attribution: where did the drop come from?
a = daily_run("new"); p = daily_run("old")
for name, idx in [("index%5==0 slice", [i for i in range(N) if i % 5 == 0]), ("all other prompts", [i for i in range(N) if i % 5])]:
    print(f"slice {name:18} n={len(idx):3d}  alias {sum(a[i] for i in idx)/len(idx):.3f}  pinned {sum(p[i] for i in idx)/len(idx):.3f}")
