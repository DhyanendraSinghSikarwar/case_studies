# Q25: spot training Monte Carlo. Interruption modelled as one job-level event per hazard (assumption stated). Relative cost units.
import math, random, statistics
SEED = 25
WORK = 10.0                      # hours of work, 8 GPUs (invented)
P_HOUR = 0.15                    # chance of at least one interruption in an hour (job level)
LAM = -math.log(1 - P_HOUR)      # hazard per hour, so that 1 - exp(-LAM) = 0.15
RESTART = 0.25                   # 15 min to get capacity back, reload and resume
GPUS = 8
SPOT_RATE = 0.35                 # spot price as a fraction of on-demand per GPU-hour: an assumed parameter, not a real price
def one(rng, ckpt, ov):
    done = 0.0; clock = 0.0       # done = saved progress
    while done < WORK:
        step = min(ckpt, WORK - done) if ckpt else WORK - done
        cost_step = step + (ov if ckpt and done + step < WORK else 0.0)     # checkpoint write time after each interval
        x = rng.expovariate(LAM)
        if x >= cost_step:
            clock += cost_step; done += step
        else:
            clock += x + RESTART  # lost everything since the last checkpoint
    return clock
def mc(ckpt, ov, n=20000):
    rng = random.Random(SEED)
    t = sorted(one(rng, ckpt, ov) for _ in range(n))
    return statistics.mean(t), t[int(0.95 * n)]
print(f"hazard/hour={LAM:.4f}  P(no interruption in 10h)={math.exp(-LAM*WORK):.3f}  (0.85^10={0.85**10:.3f})")
print(f"on-demand baseline: {WORK:.1f} h, cost {WORK*GPUS:.1f} GPU-hour units at rate 1.0")
print(f"{'policy':<26}{'mean_h':>8}{'p95_h':>8}{'wasted_h(mean)':>15}{'cost_units':>11}{'vs_on_demand':>13}")
for name, ck, ov in [("no checkpoint", None, 0), ("hourly, 1 min overhead", 1.0, 1/60), ("10 min, 1 min overhead", 1/6, 1/60)]:
    m, p95 = mc(ck, ov)
    cost = m * GPUS * SPOT_RATE
    print(f"{name:<26}{m:>8.2f}{p95:>8.2f}{m-WORK:>15.2f}{cost:>11.1f}{cost/(WORK*GPUS):>13.2f}")
# closed form for no checkpoint: E = (1/lam + restart) * (exp(lam*T) - 1)
print(f"closed-form mean, no checkpoint: {(1/LAM + RESTART)*(math.exp(LAM*WORK)-1):.2f} h")
# break-even: spot is worth it while mean wall-clock x SPOT_RATE < 1
for name, ck, ov in [("no checkpoint", None, 0), ("hourly", 1.0, 1/60), ("10 min", 1/6, 1/60)]:
    m, _ = mc(ck, ov); print(f"{name:<14} break-even spot rate = {WORK/m:.2f} of on-demand")
