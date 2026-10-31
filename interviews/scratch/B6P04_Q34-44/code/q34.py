# Q34: bandit vs fixed A/B for 6 subject lines. Illustrative numbers, seeded.
import numpy as np

N, K, BATCHES = 600_000, 6, 14
rates = np.array([0.100, 0.104, 0.108, 0.112, 0.116, 0.120])   # invented true open rates
assert N // K == 100_000
se_pair = np.sqrt(2 * 0.11 * 0.89 / 100_000)
print(f"fixed A/B: 100,000 per line, SE of a difference ~ {se_pair*100:.2f} points")
assert abs(se_pair - 0.00140) < 1e-4

def run_fixed(rng):
    n = np.full(K, N // K)
    s = rng.binomial(n, rates)
    return n, s

def run_ts(rng):
    n = np.zeros(K); s = np.zeros(K)
    per = N // BATCHES
    for b in range(BATCHES):
        if b == 0:
            share = np.full(K, 1 / K)
        else:
            draws = rng.beta(1 + s, 1 + n - s, size=(2000, K))
            share = np.bincount(draws.argmax(1), minlength=K) / 2000
        send = rng.multinomial(per, share)
        s += rng.binomial(send, rates); n += send
    return n, s

R = 300
rng = np.random.default_rng(34)
res = {}
for name, f in [("fixed", run_fixed), ("thompson", run_ts)]:
    clicks, best, diff_err, win_bias, worst_n = [], [], [], [], []
    for _ in range(R):
        n, s = f(rng)
        clicks.append(s.sum()); est = s / np.maximum(n, 1)
        w = est.argmax(); best.append(w == K - 1)
        win_bias.append(est[w] - rates[w])
        # error on the gap between the two lines with the lowest rates (smallest sample under a bandit)
        diff_err.append(abs((est[1] - est[0]) - (rates[1] - rates[0])))
        worst_n.append(n[0])
    res[name] = dict(clicks=np.mean(clicks), best=np.mean(best), bias=np.mean(win_bias),
                     gap_err=np.mean(diff_err), n_worst=np.mean(worst_n))
    r = res[name]
    print(f"{name:9s} opens={r['clicks']:9.0f} picked_true_best={r['best']:.0%} "
          f"bias_of_winner_estimate={r['bias']*100:+.3f} pts  abs_err_on_gap(line1-line0)={r['gap_err']*100:.3f} pts  sends_to_worst_line={r['n_worst']:.0f}")

best_possible = N * rates.max()
print("opens if every send used the best line:", int(best_possible))
assert res["thompson"]["clicks"] > res["fixed"]["clicks"]
assert res["thompson"]["n_worst"] < 0.5 * res["fixed"]["n_worst"]
assert res["thompson"]["gap_err"] > res["fixed"]["gap_err"]
extra = res["thompson"]["clicks"] - res["fixed"]["clicks"]
print(f"extra opens from the bandit: {extra:.0f} ({extra/res['fixed']['clicks']:.1%})")
