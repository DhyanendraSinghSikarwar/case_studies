"""
SYNTHETIC DATA GENERATOR - CASE STUDY 4 (Razorpay-style adaptive anomaly detection)
==================================================================================
THIS DATA IS SYNTHETIC. Razorpay's event streams are private, and no public dataset
has merchant x gateway payment-health time series with labelled incidents.

We simulate 48 series (16 merchants x 3 gateways) in 5-minute windows for 6 weeks
(29 Sep - 9 Nov 2025: Dussehra 1-2 Oct, Diwali week 18-21 Oct) with:
  * time-of-day and day-of-week volume/SR patterns, festive load
  * overdispersion and autocorrelation (an AR(1) wobble on the log-odds of success)
  * ~40 labelled incidents of 5 types: gateway outage, merchant integration failure,
    latency spike, card-testing burst, slow degradation
Calibration anchors (reference file, Case Study 4): metrics monitored = success rate,
latency regressions, card testing, velocity abuse, gateway x merchant degradation;
baselines must be calendar-aware (time of day, day of week, holidays).
All effect sizes are our assumptions (decision.md D-4-02 ... D-4-04).

Outputs: data/cs04/payment_health_5min.csv.gz and data/cs04/incidents.csv
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit, logit

SEED = 42
START, DAYS, SLOT_MIN = pd.Timestamp("2025-09-29"), 42, 5
MERCHANTS, GATEWAYS = [f"M{i:02d}" for i in range(1, 17)], ["GW_A", "GW_B", "GW_C"]
FESTIVE = {"2025-10-01": 1.3, "2025-10-02": 1.4, "2025-10-18": 1.8, "2025-10-19": 1.6, "2025-10-20": 1.7, "2025-10-21": 1.5}
HOUR_VOL = np.array([0.35, 0.22, 0.15, 0.12, 0.12, 0.18, 0.35, 0.60, 0.85, 1.00, 1.10, 1.20,
                     1.30, 1.25, 1.10, 1.05, 1.05, 1.10, 1.25, 1.45, 1.60, 1.65, 1.40, 0.85])
HOUR_SR = np.where(np.arange(24) < 5, -0.30, np.where((np.arange(24) >= 19) & (np.arange(24) < 23), -0.06, 0.0))


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    ts = pd.date_range(START, periods=DAYS * 24 * 60 // SLOT_MIN, freq=f"{SLOT_MIN}min")
    T = len(ts); hours = ts.hour.to_numpy(); day = ts.strftime("%Y-%m-%d")
    fest = pd.Series(day).map(FESTIVE).fillna(1.0).to_numpy()
    weekend = np.asarray(ts.dayofweek >= 5)
    size = np.exp(rng.normal(np.log(14), 0.6, len(MERCHANTS)))                 # merchant size (attempts / 5 min at peak)
    share = rng.dirichlet([4, 3, 2], len(MERCHANTS))                          # gateway split per merchant
    frames, s_id = [], 0
    base_sr = {}
    for mi, m in enumerate(MERCHANTS):
        for gi, g in enumerate(GATEWAYS):
            lam = size[mi] * share[mi, gi] * 3 * HOUR_VOL[hours] * fest * np.where(weekend, 1.1, 1.0)
            b = logit(rng.uniform(0.80, 0.90))
            base_sr[(m, g)] = b
            ar = np.zeros(T); eps = rng.normal(0, 0.06, T)                    # AR(1) wobble -> overdispersion + autocorrelation
            for t in range(1, T):
                ar[t] = 0.9 * ar[t - 1] + eps[t]
            z = b + HOUR_SR[hours] - 0.15 * (fest > 1) + ar
            lat = np.exp(np.log(900 + 150 * gi) + 0.25 * np.log(fest) + 0.12 * (HOUR_VOL[hours] > 1.3) + rng.normal(0, 0.10, T))
            frames.append(dict(series=s_id, merchant=m, gateway=g, lam=lam, z=z, lat=lat))
            s_id += 1
    S = len(frames)
    Z = np.stack([f["z"] for f in frames]); LAM = np.stack([f["lam"] for f in frames]); LAT = np.stack([f["lat"] for f in frames])

    # ---- incidents (ground truth) ----
    inc = []
    def add(kind, series_idx, start_slot, dur_slots, **kw):
        inc.append(dict(kind=kind, series=list(series_idx), start=int(start_slot), dur=int(dur_slots), **kw))
    slots_per_day = 288
    def rand_start(lo_day=3, hi_day=DAYS - 1):
        return rng.integers(lo_day * slots_per_day, hi_day * slots_per_day)
    for _ in range(8):   # gateway outage: every merchant on that gateway
        g = rng.integers(0, 3); add("gateway_outage", [i for i in range(S) if i % 3 == g], rand_start(), rng.integers(3, 25), drop=rng.uniform(1.5, 3.0))
    for _ in range(10):  # merchant integration failure on one gateway
        add("merchant_failure", [rng.integers(0, S)], rand_start(), rng.integers(6, 48), drop=rng.uniform(1.2, 2.5))
    for _ in range(8):   # latency spike
        add("latency_spike", [rng.integers(0, S)], rand_start(), rng.integers(3, 12), mult=rng.uniform(2.0, 3.5))
    for _ in range(8):   # card testing: attempt burst, most fail
        add("card_testing", [rng.integers(0, S)], rand_start(), rng.integers(2, 8), burst=rng.uniform(4, 8))
    for _ in range(6):   # slow degradation: small drop for hours
        add("slow_degradation", [rng.integers(0, S)], rand_start(), rng.integers(36, 72), drop=rng.uniform(0.35, 0.6))
    # one guaranteed outage during Diwali evening peak (the hardest time for static rules)
    add("gateway_outage", [i for i in range(S) if i % 3 == 1], 20 * slots_per_day + 20 * 12, 18, drop=2.2)
    extra_att = np.zeros_like(LAM)
    for e in inc:
        sl = slice(e["start"], min(e["start"] + e["dur"], T))
        for s in e["series"]:
            if e["kind"] in ("gateway_outage", "merchant_failure", "slow_degradation"):
                Z[s, sl] -= e["drop"]
            elif e["kind"] == "latency_spike":
                LAT[s, sl] *= e["mult"]
            elif e["kind"] == "card_testing":
                extra_att[s, sl] = LAM[s, sl] * e["burst"]

    att = rng.poisson(LAM)
    succ = rng.binomial(att, expit(Z))
    bot = rng.poisson(extra_att)                                                  # card-testing attempts: ~5% succeed
    att = att + bot; succ = succ + rng.binomial(bot, 0.05)
    lat_p95 = np.round(LAT * np.exp(rng.normal(0, 0.05, LAT.shape)))
    lat_p95 = np.where(att == 0, np.nan, lat_p95)

    rows = pd.DataFrame({
        "timestamp": np.tile(ts.values, S),
        "merchant_id": np.repeat([f["merchant"] for f in frames], T),
        "gateway": np.repeat([f["gateway"] for f in frames], T),
        "attempts": att.ravel(), "successes": succ.ravel(), "latency_p95_ms": lat_p95.ravel()})
    # ---- data-quality issue: a collector restart duplicated 2 hours of windows for GW_C on 24 Oct ----
    dup = rows[(rows.gateway == "GW_C") & rows.timestamp.between("2025-10-24 10:00", "2025-10-24 11:55")]
    rows = pd.concat([rows, dup], ignore_index=True).sort_values(["merchant_id", "gateway", "timestamp"], kind="stable").reset_index(drop=True)
    inc_df = pd.DataFrame([{"incident_id": i + 1, "type": e["kind"],
                            "start": ts[e["start"]], "end": ts[min(e["start"] + e["dur"], T) - 1] + pd.Timedelta(minutes=SLOT_MIN),
                            "series": ";".join(f"{frames[s]['merchant']}|{frames[s]['gateway']}" for s in e["series"])}
                           for i, e in enumerate(inc)])
    return rows, inc_df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs04"), exist_ok=True)
    d, i = generate()
    d.to_csv(os.path.join(here, "cs04", "payment_health_5min.csv.gz"), index=False)
    i.to_csv(os.path.join(here, "cs04", "incidents.csv"), index=False)
    print(len(d), "rows;", len(i), "incidents; overall SR", round(d.successes.sum() / d.attempts.sum(), 4))
