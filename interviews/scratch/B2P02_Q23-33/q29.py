import numpy as np
rng = np.random.default_rng(0)           # SYNTHETIC loss curve, not a real run
steps = np.arange(1, 2001)
loss = 2.0 + 6*steps**-0.35 + rng.normal(0, 0.01, steps.size)
loss[1200:1210] += 1.5 * np.exp(-np.arange(10)/4)        # injected spike
def flag_spikes(l, win=50, k=6):
    out = []
    for i in range(win, len(l)):
        base = l[i-win:i]; med = np.median(base); mad = np.median(abs(base-med))*1.4826 + 1e-6
        if l[i] > med + k*mad: out.append(i+1)
    return out
f = flag_spikes(loss); print("flagged steps:", f[0], "to", f[-1], "count", len(f))
print("loss at 1000/1199/1205/2000:", [round(loss[i-1], 3) for i in (1000, 1199, 1205, 2000)])
