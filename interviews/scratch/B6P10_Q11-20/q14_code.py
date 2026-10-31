import math

# Prompt arithmetic: Little's law L = lambda * W
calls_day, share_window, window_h, call_s, per_server = 100_000, 0.60, 8, 180, 25
calls_window = calls_day * share_window
lam = calls_window / (window_h * 3600)
L = lam * call_s
assert calls_window == 60_000 and abs(lam - 2.0833333) < 1e-6 and round(L) == 375
servers_flat = math.ceil(L / per_server)
assert servers_flat == 15
print("calls in window:", int(calls_window), "| arrival rate/s:", round(lam, 3), "| mean concurrent calls:", round(L, 1))
print("servers at 100% load (mean concurrency):", servers_flat)

# Off-window traffic for comparison
lam_off = calls_day * (1 - share_window) / (16 * 3600)
print("off-window mean concurrent calls:", round(lam_off * call_s, 1))
assert round(lam_off * call_s) == 125

# Random fluctuation: concurrency of Poisson arrivals is Poisson(L) (M/G/infinity); find the 99.9th percentile exactly
def poisson_ppf(q, mu):
    p = math.exp(-mu); c = p; k = 0
    while c < q:
        k += 1; p *= mu / k; c += p
    return k
k999 = poisson_ppf(0.999, L)
s999 = math.ceil(k999 / per_server)
s_hr = math.ceil(L / (per_server * 0.70))
print("99.9th percentile concurrent calls:", k999, "-> servers:", s999, "| servers at 70% target utilisation:", s_hr)
assert 420 < k999 < 450 and s999 == 18 and s_hr == 22

# Sensitivity to the 'evenly spread' assumption: if the busiest hour carries 1.5x the window average (assumed)
peak_L = L * 1.5
print("if busiest hour is 1.5x average: concurrent", round(peak_L), "-> servers", math.ceil(peak_L / per_server))
assert math.ceil(peak_L / per_server) == 23

# Latency: one conversational turn budget of 1.5 s, split (illustrative)
split = {"speech recognition": 0.5, "language understanding + answer": 0.6, "speech synthesis first audio": 0.3, "network + overhead": 0.1}
assert abs(sum(split.values()) - 1.5) < 1e-9
print("illustrative split of 1.5 s:", split)

# Follow-up check: 4-minute calls
L4 = round(lam * 240, 6)
assert round(L4) == 500 and math.ceil(L4 / per_server) == 20
print("4-minute calls: concurrent", round(L4), "servers", math.ceil(L4 / per_server))
