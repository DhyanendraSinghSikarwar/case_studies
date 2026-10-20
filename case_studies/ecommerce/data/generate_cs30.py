"""
SYNTHETIC DATA GENERATOR - CASE STUDY 30 (Buy Box winner selection and seller quality: an external audit)
=======================================================================================================
THIS DATA IS SYNTHETIC. Amazon's Buy Box algorithm and its seller data are proprietary.

Documented context (Dash, Chakraborty, Ghosh, Mukherjee, Gummadi, CSCW 2024, arXiv:2407.01732): scraped Buy Box
competitions from Amazon.in (20,553 competitions, 2,766 distinct sellers); Amazon / special merchants won 87.74% of
India's competitions (29.15% "out of position", i.e. not the lowest-price offer); in a survey 54% (407 of 750) of
first preferences went to the special merchants; 74.13% of low-rated reviews of Amazon-fulfilled sellers were struck
through; special merchant Appario's reported 87% positive feedback falls to 61% when struck reviews are counted; in a
survey of Indian participants the special-merchant share fell from ~54% (control) to 14.5% (number of ratings hidden),
6.93% (rectified metrics, no number of ratings) and 28.53% (rectified metrics with number of ratings).

Simulation (ours, calibrated to those documented figures; Amazon's real algorithm is NOT known):
  * 2,800 sellers: 2 special ("related") merchants with huge lifetime rating counts, 560 independent fulfilled-by-
    marketplace (FBA) sellers, 2,238 merchant-fulfilled (FBM) sellers; true seller quality is hidden.
  * Reviews: low-rated reviews of related/FBA sellers are struck through at a high rate, so the REPORTED positive
    feedback of those sellers is inflated relative to the RECTIFIED (all-review) value.
  * 4,000 products, 20,553 Buy Box competitions over 14 days; the hidden winner rule scores price gap, fast delivery,
    reported feedback, log number of ratings and a "related seller" bonus, plus noise.
  * Surveys: simulated respondents choose among the top-4 offers with a multinomial-logit utility; one control survey
    and three treatment arms (hide number of ratings; rectified metrics without; rectified metrics with number of ratings).
Hidden truth columns / values start with an underscore (used only to grade the audit).

Outputs (written by the notebook): data/cs30/offers.csv.gz, competitions.csv.gz, sellers.csv.gz, survey.csv.gz
"""
import numpy as np
import pandas as pd

SEED = 42
N_SELLERS, N_FBA, N_PRODUCTS, N_COMP, DAYS = 2800, 560, 4000, 20553, 14
# hidden winner rule (the auditor does not know these)
W_PRICE, W_FAST, W_POS, W_LOGN, W_RELATED, NOISE = 7.0, 0.9, 4.0, 0.30, 0.45, 0.35
# hidden survey respondent utility: price premium (per 1%), fast delivery, rating, positive % (per 10 pts), log10 n ratings
B_RELATED = -1.75  # calibration constant: residual wariness of the special merchants' offers, fitted to the documented shares
B_PRICE, B_FAST, B_RATING, B_POS, B_LOGN = -0.13, 0.0, 0.45, 0.60, 0.99
PARTICIPANT_SD = 0.5


def _stars(pos):
    return np.clip(4.95 - 2.9 * (1 - pos), 3.0, 5.0)


def make_sellers(rng):
    S = N_SELLERS
    typ = np.array(["related"] * 2 + ["FBA"] * N_FBA + ["FBM"] * (S - 2 - N_FBA))
    n_rat = np.empty(S); pos_true = np.empty(S); strike = np.empty(S)
    n_rat[:2] = [620_000, 410_000]; pos_true[:2] = [0.61, 0.70]; strike[:2] = [0.77, 0.77]
    f = typ == "FBA"; m = typ == "FBM"
    n_rat[f] = np.exp(rng.normal(6.8, 1.4, f.sum())); pos_true[f] = 1 / (1 + np.exp(-(1.35 + 0.55 * rng.normal(size=f.sum())))); strike[f] = rng.beta(7, 3, f.sum())
    n_rat[m] = np.exp(rng.normal(5.3, 1.7, m.sum())); pos_true[m] = 1 / (1 + np.exp(-(1.55 + 0.60 * rng.normal(size=m.sum())))); strike[m] = rng.beta(0.5, 30, m.sum())
    n_rat = np.maximum(n_rat, 12).round().astype(int)
    rev12 = np.maximum((n_rat * rng.uniform(0.08, 0.20, S)).round().astype(int), 8)
    low = rng.binomial(rev12, 1 - pos_true); struck = rng.binomial(low, strike)
    pos_rep = (rev12 - low) / (rev12 - struck); pos_rect = (rev12 - low) / rev12
    late = np.clip(0.02 + 0.12 * (1 - pos_true) + rng.normal(0, 0.01, S), 0.002, 0.5) * np.where(typ == "FBM", 1.0, 0.3)
    defect = np.clip(0.01 + 0.15 * (1 - pos_true) + rng.normal(0, 0.01, S), 0.002, 0.5)
    cancel = np.clip(0.005 + 0.05 * (1 - pos_true) + rng.normal(0, 0.005, S), 0.0, 0.3) * np.where(typ == "FBM", 1.0, 0.4)
    sellers = pd.DataFrame({
        "seller_id": np.arange(S), "seller_type": typ, "n_ratings": n_rat, "reviews_12m": rev12, "low_rated_12m": low, "struck_low_12m": struck,
        "pos_feedback_reported": (pos_rep * 100).round(1), "avg_rating_reported": _stars(pos_rep).round(2),
        "pos_feedback_rectified": (pos_rect * 100).round(1), "avg_rating_rectified": _stars(pos_rect).round(2),
        "late_ship_rate": late.round(4), "defect_rate": defect.round(4), "cancel_rate": cancel.round(4),
        "_true_pos_rate": pos_true.round(4), "_strike_prob": strike.round(4)})
    return sellers


def make_competitions(rng, sellers):
    S = len(sellers); typ = sellers.seller_type.values; fba = typ != "FBM"
    pool = np.arange(2, S); w = sellers.n_ratings.values[2:] ** 0.3; w = w / w.sum()
    markup = np.where(typ == "related", -0.09, np.where(typ == "FBA", 0.00, -0.02)) + rng.normal(0, 1, S) * np.where(typ == "related", 0.04, 0.06)
    rows = []; comps = []
    comp_prod = np.sort(rng.integers(0, N_PRODUCTS, N_COMP)); base = np.clip(np.exp(rng.normal(np.log(1800), 0.9, N_PRODUCTS)), 150, 60_000)
    prod_sel = {}
    for cid, pid in enumerate(comp_prod):
        if pid not in prod_sel:
            m = int(np.clip(4 + rng.poisson(3), 4, 14)); sel = list(rng.choice(pool, m, replace=False, p=w))
            if rng.random() < 0.93:
                sel += [0, 1] if rng.random() < 0.35 else [int(rng.integers(0, 2))]
            sel = np.array(sel); pm = markup[sel] + rng.normal(0, 0.03, len(sel)); prod_sel[pid] = (sel, pm, int(rng.integers(0, 100)))
        sel, pm, kw = prod_sel[pid]
        pres = rng.random(len(sel)) < np.where(sel < 2, 0.97, 0.90)
        if pres.sum() < 3:
            pres[:3] = True
        ss, pmm = sel[pres], pm[pres]
        price = base[pid] * np.maximum(1 + pmm + rng.normal(0, 0.015, len(ss)), 0.55)
        fast = fba[ss]; days = np.where(fast, 1 + rng.poisson(0.7, len(ss)), 2 + rng.poisson(2.5, len(ss)))
        ship = np.where(fast, 0.0, np.where(rng.random(len(ss)) < 0.5, 0.0, rng.choice([40.0, 60.0, 80.0], len(ss))))
        total = price + ship; relp = total / total.min() - 1
        score = (-W_PRICE * relp + W_FAST * (days <= 2) + W_POS * (sellers.pos_feedback_reported.values[ss] / 100 - 0.85)
                 + W_LOGN * np.log10(sellers.n_ratings.values[ss]) + W_RELATED * (ss < 2) + NOISE * rng.gumbel(size=len(ss)))
        win = int(np.argmax(score)); day = int(rng.integers(0, DAYS))
        comps.append((cid, pid, kw, day, len(ss), int(ss[win])))
        for j in range(len(ss)):
            rows.append((cid, pid, int(ss[j]), round(float(price[j]), 2), float(ship[j]), int(days[j]), int(fast[j]), int(j == win)))
    offers = pd.DataFrame(rows, columns=["comp_id", "product_id", "seller_id", "price_inr", "shipping_inr", "delivery_days", "fulfilled_by_marketplace", "is_buy_box"])
    comps = pd.DataFrame(comps, columns=["comp_id", "product_id", "keyword_id", "day", "n_offers", "winner_seller_id"])
    return offers, comps


def make_survey(rng, sellers, offers):
    """60 competitions where a related seller won without the lowest total price; top-4 offers; five respondent groups."""
    o = offers.copy(); o["total"] = o.price_inr + o.shipping_inr
    o["is_min"] = o.total == o.groupby("comp_id").total.transform("min")
    win = o[(o.is_buy_box == 1) & (o.seller_id < 2) & (~o.is_min)]
    tasks = rng.choice(win.comp_id.unique(), 60, replace=False)
    sel = {}
    for t in tasks:
        d = o[o.comp_id == t].sort_values("total"); top = d.head(4)
        if not (top.is_buy_box == 1).any():
            top = pd.concat([d.head(3), d[d.is_buy_box == 1]])
        sel[t] = top.reset_index(drop=True)
    sd = sellers.set_index("seller_id"); rows = []
    arms = {"S1_control": ("rep", True), "T0_control": ("rep", True), "T1_hide_n": ("rep", False), "T2_rectified_no_n": ("rect", False), "T3_rectified_with_n": ("rect", True)}
    for arm, (metric, show_n) in arms.items():
        for p in range(50):
            pe = rng.normal(0, PARTICIPANT_SD)
            for t in rng.choice(tasks, 15, replace=False):
                d = sel[t]; s = sd.loc[d.seller_id.values]
                pos = (s.pos_feedback_reported if metric == "rep" else s.pos_feedback_rectified).values; rat = (s.avg_rating_reported if metric == "rep" else s.avg_rating_rectified).values
                prem = (d.total / d.total.min() - 1).values * 100; logn = np.log10(s.n_ratings.values)
                u = (B_PRICE * prem + B_FAST * d.fulfilled_by_marketplace.values + B_RATING * (rat - 4) + B_POS * (pos - 80) / 10
                     + (B_LOGN * logn if show_n else 0.0) + B_RELATED * (d.seller_id.values < 2) + pe * (d.seller_id.values < 2) + rng.gumbel(size=len(d)))
                ch = int(np.argmax(u))
                for j in range(len(d)):
                    rows.append((arm, f"{arm}_{p}", int(t), j, int(d.seller_id[j] < 2), round(float(prem[j]), 2), int(d.fulfilled_by_marketplace[j]), rat[j], pos[j],
                                 float(s.n_ratings.values[j]) if show_n else np.nan, int(j == ch)))
    return pd.DataFrame(rows, columns=["arm", "participant_id", "task_comp_id", "option", "is_related", "price_premium_pct", "fast_delivery", "avg_rating_shown", "pos_pct_shown", "n_ratings_shown", "chosen"])


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    sellers = make_sellers(rng); offers, comps = make_competitions(rng, sellers); survey = make_survey(rng, sellers, offers)
    hidden = {"w_price": W_PRICE, "w_fast": W_FAST, "w_pos": W_POS, "w_logn": W_LOGN, "w_related": W_RELATED, "noise": NOISE,
              "b_price": B_PRICE, "b_fast": B_FAST, "b_rating": B_RATING, "b_pos": B_POS, "b_logn": B_LOGN, "b_related": B_RELATED}
    # injected data-quality problems
    off = offers.copy(); idx = rng.choice(len(off), 60, replace=False); off.loc[idx, "price_inr"] *= 10
    idx = rng.choice(len(off), int(0.02 * len(off)), replace=False); off.loc[idx, "shipping_inr"] = np.nan
    off = pd.concat([off, off.sample(300, random_state=seed)], ignore_index=True)
    return off, comps, sellers, survey, hidden


if __name__ == "__main__":
    import time
    t = time.time(); off, comps, sellers, survey, hid = generate(); print(len(off), len(comps), len(survey), f"{time.time() - t:.0f}s")
