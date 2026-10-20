"""
SYNTHETIC DATA GENERATOR - CASE STUDY 29 (Zerodha-style point-of-trade "Nudge" against penny-stock trading)
==========================================================================================================
THIS DATA IS SYNTHETIC. Broker trade data are confidential.

Daily penny-stock trades by FIRST-TIME investors on a broker's three platforms (web, Android, iOS) over
~18 months, plus the same series for a group of OTHER BROKERS that never introduced a nudge (control).
Market-wide speculative interest in penny stocks rises sharply (a small-cap boom), peaks, then fades -
so a simple before/after comparison around the nudge launch mixes the nudge with the market cycle.
The nudge (a warning when a risky trade is attempted) rolls out in a STAGGERED way: web first, then
Android, then iOS. The TRUE effect is a ~30% reduction in penny trades on a platform once its nudge is live.
A user-level dataset adds what a careful team would also run: a 5% randomised HOLDOUT that never sees nudges.

Calibration anchors (reference file, Case Study 29): "Penny stock trading volumes on Kite have dropped by
more than 50%"; before/after only, "No control group is stated"; nudges at the point of trade; no ML.
Rates are our assumptions (decision.md D-29-02). Hidden truth columns start with "_".

Outputs: data/cs29/daily_trades.csv.gz, data/cs29/user_holdout.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
START = pd.Timestamp("2020-01-01"); DAYS = 540
LAUNCH = {"web": 230, "android": 262, "ios": 300}          # nudge go-live day index per platform (staggered)
TRUE_EFFECT = 0.30


def market_index(d):
    """Speculative penny-stock interest: boom to a peak around day 200, then a fade (the confounder)."""
    return 1.0 + 1.8 * np.exp(-((d - 200) / 70.0) ** 2) + 0.25 * (d / DAYS)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    d = np.arange(DAYS); dates = START + pd.to_timedelta(d, unit="D"); wd = dates.weekday.values; trading = wd < 5
    M = market_index(d) * np.exp(rng.normal(0, 0.04, DAYS))
    rows = []
    base = {"web": 1800, "android": 2600, "ios": 900, "other_brokers": 9000}
    beta = {"web": 1.0, "android": 1.0, "ios": 1.0, "other_brokers": 1.0}
    growth = {"web": 0.0006, "android": 0.0012, "ios": 0.0010, "other_brokers": 0.0009}       # customer-base growth
    for p, b0 in base.items():
        post = (d >= LAUNCH[p]) if p in LAUNCH else np.zeros(DAYS, bool)
        ramp = np.clip((d - LAUNCH.get(p, 10 ** 6)) / 10, 0, 1)                                  # effect builds over 10 days
        lam = b0 * M ** beta[p] * np.exp(growth[p] * d) * (1 - TRUE_EFFECT * ramp) * np.exp(rng.normal(0, 0.06, DAYS))
        trades = np.where(trading, rng.poisson(lam), 0)
        rows.append(pd.DataFrame({"date": dates, "platform": p, "penny_trades_first_time": trades, "active_first_time_investors": np.where(trading, np.round(lam / 0.12 * rng.uniform(0.97, 1.03, DAYS)), 0),
                                  "nudge_live": post.astype(int), "_market_index": M}))
    daily = pd.concat(rows, ignore_index=True)
    daily = daily[daily.date.dt.weekday < 5].reset_index(drop=True)
    # user-level holdout over the 90 days after full rollout (day 300-390)
    n = 120_000; hold = (rng.random(n) < 0.05).astype(int)
    spec = rng.normal(0, 1, n); age = np.clip(rng.normal(27, 6, n), 18, 65).round(); capital = np.exp(rng.normal(np.log(15000), 0.9, n))
    p_trade = expit(-1.4 + 0.9 * spec - 0.02 * (age - 27) - 0.1 * np.log(capital / 15000)) * np.where(hold == 1, 1.0, 1 - TRUE_EFFECT)
    traded = (rng.random(n) < p_trade).astype(int)
    loss = np.where(traded == 1, np.round(np.exp(rng.normal(np.log(2200), 1.0, n)), 0), 0)
    users = pd.DataFrame({"user_id": [f"Z{i:06d}" for i in range(n)], "holdout_no_nudge": hold, "age": age, "starting_capital_inr": np.round(capital, -2),
                          "traded_penny_90d": traded, "penny_loss_90d_inr": loss, "_spec": spec})
    # data-quality defects
    daily.loc[daily.sample(n=6, random_state=seed).index, "penny_trades_first_time"] = 0                      # exchange file not received -> zero
    daily = pd.concat([daily, daily.sample(n=20, random_state=seed + 1)], ignore_index=True)
    return daily, users


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs29"), exist_ok=True)
    dly, us = generate(); dly.to_csv(os.path.join(here, "cs29", "daily_trades.csv.gz"), index=False); us.to_csv(os.path.join(here, "cs29", "user_holdout.csv.gz"), index=False)
    z = dly[dly.platform != "other_brokers"].groupby("date").penny_trades_first_time.sum()
    pre = z[(z.index >= START + pd.Timedelta(days=170)) & (z.index < START + pd.Timedelta(days=230))].mean(); post = z[(z.index >= START + pd.Timedelta(days=330)) & (z.index < START + pd.Timedelta(days=390))].mean()
    print("broker pre (60d before web launch) vs post (60d after full rollout+30):", round(pre), round(post), "change", round(post / pre - 1, 3))
    print(us.groupby("holdout_no_nudge").traded_penny_90d.mean().round(4).to_dict())
