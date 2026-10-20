"""
SYNTHETIC DATA GENERATOR - CASE STUDY 26 (Policybazaar-style chat channel and motor-insurance conversion)
========================================================================================================
THIS DATA IS SYNTHETIC. Marketplace visitor and sales data are confidential.

Motor-insurance visitors over 8 weeks. A hidden purchase INTENT drives both whether a visitor starts a chat
and whether they buy (self-selection). Observed intent signals: days until the current policy expires,
quotes viewed, return visits, traffic source, add-ons viewed, car age, claim-free (NCB) status.
Some intent is NOT observed (e.g., a dealer already pushing a renewal) - residual confounding.
From week 3 a RANDOMISED ENCOURAGEMENT runs: 50% of visitors see a proactive chat pop-up (Z = 1), which
raises chat uptake but has no direct effect on buying - an instrument for the causal effect of chatting.
From week 5 a BOT (PBee-style) answers most chats: response delays fall; long delays reduce conversion.
The TRUE causal effect of chatting is modest (+0.35 log-odds, about +30% relative), far below the raw 2x.

Calibration anchors (reference file, Case Study 26): chat users converted at "about 2x" non-chat users but
were "only 8-9%" of customers; bot share of responses 20% -> 75-80%; response delays 35% -> 7-8%; agent output
1.5-2 -> 7-8 sales/day; ~$1M premium/month via the bot. Rates are our assumptions (decision.md D-26-02).
Hidden truth columns start with "_".

Output: data/cs26/visitors.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
CHAT_EFFECT = 0.35


def generate(seed=SEED, n=300_000):
    rng = np.random.default_rng(seed)
    week = rng.integers(1, 9, n)
    intent = rng.normal(0, 1, n)                                                     # hidden purchase intent
    u_hidden = rng.normal(0, 1, n)                                                   # unobserved part of intent (residual confounder)
    days_to_expiry = np.clip(np.round(np.exp(rng.normal(np.log(25), 0.9, n) - 0.45 * intent)), 0, 365)
    quotes = rng.poisson(np.exp(0.6 + 0.35 * intent))
    returning = (rng.random(n) < expit(-0.8 + 0.6 * intent)).astype(int)
    source = rng.choice(["search", "renewal_email", "display_ad", "direct", "affiliate"], n, p=[0.38, 0.15, 0.22, 0.15, 0.10])
    src_eff = pd.Series(source).map({"search": 0.2, "renewal_email": 0.6, "display_ad": -0.6, "direct": 0.3, "affiliate": -0.2}).values
    addons = rng.poisson(np.exp(-0.2 + 0.3 * intent))
    car_age = np.clip(rng.gamma(2.2, 2.2, n), 0, 18).round(1)
    ncb = (rng.random(n) < 0.55).astype(int)
    mobile = (rng.random(n) < 0.72).astype(int)
    Z = np.where(week >= 3, (rng.random(n) < 0.5).astype(int), 0)                     # randomised proactive chat pop-up
    z_chat = -3.0 + 0.55 * intent + 0.35 * u_hidden + 0.25 * returning + 0.15 * np.log1p(quotes) - 0.2 * mobile + 1.05 * Z
    chat = (rng.random(n) < expit(z_chat)).astype(int)
    bot_era = week >= 5
    bot_handled = np.where(chat == 1, (rng.random(n) < np.where(bot_era, 0.78, 0.20)).astype(int), 0)
    delay_min = np.where(chat == 1, np.where(bot_handled == 1, rng.exponential(0.3, n), rng.exponential(np.where(bot_era, 4, 9), n)), np.nan)
    z_buy = (-3.2 + 0.85 * intent + 0.45 * u_hidden + src_eff - 0.012 * np.clip(days_to_expiry, 0, 120) + 0.1 * ncb - 0.03 * car_age
             + CHAT_EFFECT * chat - 0.06 * np.nan_to_num(np.clip(delay_min - 2, 0, 30)))
    buy = (rng.random(n) < expit(z_buy)).astype(int)
    premium = np.where(buy == 1, np.round(np.exp(rng.normal(np.log(9500), 0.45, n)) * (1 + 0.04 * addons), -1), 0)
    df = pd.DataFrame({"visitor_id": [f"V{i:07d}" for i in range(n)], "week": week, "traffic_source": source, "device": np.where(mobile == 1, "mobile", "desktop"),
                       "days_to_expiry": days_to_expiry, "quotes_viewed": quotes, "returning_visitor": returning, "addons_viewed": addons, "car_age_years": car_age,
                       "claim_free_ncb": ncb, "chat_popup_shown": Z, "chatted": chat, "bot_handled": bot_handled, "first_response_min": np.round(delay_min, 2),
                       "purchased": buy, "premium_inr": premium, "_intent": intent, "_u": u_hidden})
    # data-quality defects
    df.loc[df.sample(n=1200, random_state=seed).index, "days_to_expiry"] = -1                 # unknown expiry coded -1
    df = pd.concat([df, df.sample(n=1000, random_state=seed + 1)], ignore_index=True)        # duplicate sessions
    df.loc[df[(df.chatted == 1)].sample(n=200, random_state=seed + 2).index, "first_response_min"] = np.nan
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs26"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs26", "visitors.csv.gz"), index=False)
    dd = d.drop_duplicates("visitor_id")
    print(len(dd), "visitors | chat share", dd.chatted.mean().round(4), "| conversion", dd.purchased.mean().round(4))
    print("conv by chat", dd.groupby("chatted").purchased.mean().round(4).to_dict(), "ratio", round(dd[dd.chatted == 1].purchased.mean() / dd[dd.chatted == 0].purchased.mean(), 2))
    print("chat share by Z (wk>=3)", dd[dd.week >= 3].groupby("chat_popup_shown").chatted.mean().round(4).to_dict(), "conv by Z", dd[dd.week >= 3].groupby("chat_popup_shown").purchased.mean().round(4).to_dict())
