"""
SYNTHETIC DATA GENERATOR - CASE STUDY 16 (Swiggy-style dish search, query understanding and ranking)
====================================================================================================
THIS DATA IS SYNTHETIC. Swiggy's search logs, taxonomy and relevance labels are confidential.

Documented context (Swiggy Bytes 2021 and 2024 posts, see the reference file): Indian dish names have no standard
English spelling ("biryani" typed as biriyani, biriani, beriani, briyani); text matching returns no results for many
misspellings; some searched dishes are not available locally; the production backend was fuzzy text retrieval
(ElasticSearch); a food taxonomy of 300+ dish families in 6 dish categories exists; complex queries (diet, mood) are
a later problem. Our assumption: the scale below, the noise model, the click model and every rate.

Simulation (one city, 5 delivery areas):
  * Taxonomy: 120 dish families = 30 clusters x 4 families, in 6 categories. Each family has 10 menu names
    (the family alone plus 9 modifier variants, "chicken biryani").
  * Restaurants: 5 areas x 140 restaurants x 28 listings. Families are unevenly available by area (tail dishes are
    often missing locally, so some searches have no exact answer).
  * Sessions: 48,000 search sessions over 60 days. Query types: plain dish, dish + modifier, vague (a cluster word such
    as "tiffin"), multi-intent ("biryani near me"). 38% of dish queries are misspelled (transliteration rules and typing
    slips, more often for tail dishes). Zipf-distributed demand.
  * Hidden truth: graded relevance 0-3 of every listing for every query intent; a click model with position bias.
  * Serving: 90% of sessions are served by a fuzzy lexical ranker (the "production" system), 10% by a character
    n-gram trial arm. Clicks and orders are logged only for what was shown.
  * Defects: duplicate rows, a bot, messy casing and spacing, empty queries.
Hidden columns start with "_".
"""
import re
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer

SEED = 42
N_AREA, REST_PER_AREA, LIST_PER_REST, N_SESS, DAYS = 5, 140, 28, 48_000, 60
CATS = ["rice and biryani", "curries", "breads and rolls", "snacks and chaat", "chinese and fusion", "desserts and drinks"]
CLUSTERS = [
    ["Biryani", "Pulao", "Tehri", "Khichdi"], ["Curd Rice", "Lemon Rice", "Bisibele Bath", "Pongal"],
    ["Fried Rice", "Jeera Rice", "Rajma Chawal", "Kadhi Chawal"], ["Idli", "Dosa", "Uttapam", "Medu Vada"],
    ["Poha", "Upma", "Sabudana Khichdi", "Thalipeeth"],
    ["Butter Chicken", "Chicken Tikka Masala", "Kadai Chicken", "Chicken Korma"], ["Paneer Butter Masala", "Palak Paneer", "Kadai Paneer", "Shahi Paneer"],
    ["Dal Makhani", "Dal Tadka", "Chana Masala", "Rajma"], ["Fish Curry", "Prawn Masala", "Egg Curry", "Mutton Rogan Josh"], ["Sambar", "Rasam", "Kootu", "Avial"],
    ["Naan", "Roti", "Paratha", "Kulcha"], ["Kathi Roll", "Frankie", "Shawarma", "Wrap"], ["Burger", "Sandwich", "Club Sandwich", "Sub"],
    ["Pizza", "Garlic Bread", "Calzone", "Pasta"], ["Pav Bhaji", "Vada Pav", "Misal Pav", "Dabeli"],
    ["Samosa", "Kachori", "Pakora", "Bhajiya"], ["Pani Puri", "Sev Puri", "Bhel Puri", "Dahi Puri"], ["Chole Bhature", "Aloo Tikki", "Papdi Chaat", "Raj Kachori"],
    ["French Fries", "Nachos", "Onion Rings", "Chicken Wings"], ["Dhokla", "Khandvi", "Fafda", "Thepla"],
    ["Hakka Noodles", "Chowmein", "Schezwan Noodles", "Singapore Noodles"], ["Manchurian", "Chilli Paneer", "Chilli Chicken", "Dragon Chicken"],
    ["Momos", "Wonton", "Dim Sum", "Spring Roll"], ["Manchow Soup", "Hot and Sour Soup", "Sweet Corn Soup", "Tomato Soup"],
    ["Chicken Tikka", "Paneer Tikka", "Malai Tikka", "Reshmi Kebab"],
    ["Gulab Jamun", "Rasgulla", "Rasmalai", "Kala Jamun"], ["Jalebi", "Imarti", "Malpua", "Rabri"], ["Brownie", "Cake", "Pastry", "Cheesecake"],
    ["Ice Cream", "Kulfi", "Falooda", "Sundae"], ["Lassi", "Masala Chai", "Cold Coffee", "Milkshake"]]
CLUSTER_WORDS = ["rice", "south rice", "fried rice", "tiffin", "breakfast", "chicken curry", "paneer", "dal", "seafood", "south curry", "bread", "roll", "burger", "pizza",
                 "pav", "snack", "chaat", "street food", "fried snack", "gujarati", "noodles", "starter", "momo", "soup", "kebab", "sweet", "mithai", "dessert", "frozen", "drink"]
MODS_FOOD = ["chicken", "veg", "paneer", "egg", "mutton", "special", "spicy", "classic", "homestyle", "mini", "jumbo", "butter", "cheese", "tandoori"]
MODS_SWEET = ["sugar free", "mini", "special", "classic", "chocolate", "mango", "rose", "royal", "premium", "kesar", "dry fruit", "homemade", "jumbo", "fresh"]
MODS = sorted(set(MODS_FOOD + MODS_SWEET)); MOD_ID = {m: i for i, m in enumerate(MODS)}
QUALIFIERS = ["near me", "under 200", "for 2", "today", "best", "cheap", "spicy", "late night"]
RULES = [("ee", "i"), ("i", "ee"), ("aa", "a"), ("a", "aa"), ("oo", "u"), ("u", "oo"), ("sh", "s"), ("s", "sh"), ("v", "w"), ("w", "v"), ("ph", "f"), ("f", "ph"),
         ("kh", "k"), ("dh", "d"), ("th", "t"), ("ck", "k"), ("ch", "c"), ("ai", "e"), ("e", "ai"), ("o", "au"), ("j", "z"), ("z", "j"), ("y", "i"), ("ie", "y")]
KEYB = {"a": "sq", "b": "vn", "c": "xv", "d": "sf", "e": "wr", "f": "dg", "g": "fh", "h": "gj", "i": "uo", "j": "hk", "k": "jl", "l": "k", "m": "n", "n": "bm", "o": "ip", "p": "o",
        "r": "et", "s": "ad", "t": "ry", "u": "yi", "v": "cb", "w": "qe", "y": "tu"}
A_REL = np.array([-5.0, -3.5, -2.1, -0.9]); EXAM = 1 / (1 + 0.35 * np.arange(20))   # examination probability by position 1..20


def tokens(s):
    return re.findall(r"[a-z0-9]+", str(s).lower())


def lev(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def misspell(text, rng, rule_n=len(RULES), typos=True):
    """Apply 1-3 edits: transliteration rules (first rule_n of RULES) and, if typos, typing slips."""
    out = text
    for _ in range(1 + min(2, rng.poisson(0.7))):
        cands = [(a, b) for a, b in RULES[:rule_n] if a in out]
        if cands and (not typos or rng.random() > 0.25):
            a, b = cands[rng.integers(len(cands))]; pos = [m.start() for m in re.finditer(a, out)]; p = pos[rng.integers(len(pos))]; out = out[:p] + b + out[p + len(a):]
        elif typos and len(out) > 3:
            p = int(rng.integers(1, len(out) - 1)); k = rng.integers(4)
            if k == 0: out = out[:p] + out[p + 1:]
            elif k == 1: out = out[:p] + out[p] + out[p:]
            elif k == 2: out = out[:p] + out[p + 1] + out[p] + out[p + 2:]
            else: out = out[:p] + KEYB.get(out[p], out[p])[0] + out[p + 1:]
    return out if out != text else text[:-1] if len(text) > 4 else text


class Lex:
    """Lexical matcher: exact tokens or ElasticSearch-AUTO fuzzy tokens (0 edits for 1-2 chars, 1 for 3-5, 2 for 6+)."""
    def __init__(self, names):
        toks = [tokens(n) for n in names]; self.vocab = sorted({t for ts in toks for t in ts}); self.vi = {t: i for i, t in enumerate(self.vocab)}
        rows, cols = [], []
        for i, ts in enumerate(toks):
            for t in set(ts): rows.append(i); cols.append(self.vi[t])
        df = np.bincount(cols, minlength=len(self.vocab)); self.idf = np.log(1 + len(names) / df)
        B = sparse.csr_matrix((self.idf[cols], (rows, cols)), shape=(len(names), len(self.vocab)))
        self.Nw = (sparse.diags(1 / np.sqrt([len(t) for t in toks])) @ B).tocsr(); self._m = {}

    def match(self, tok, fuzzy):
        key = (tok, fuzzy)
        if key not in self._m:
            allowed = 0 if (not fuzzy or len(tok) < 3) else (1 if len(tok) <= 5 else 2); res = []
            for v, w in enumerate(self.vocab):
                if abs(len(w) - len(tok)) <= allowed:
                    d = lev(tok, w)
                    if d <= allowed: res.append((v, 1 / (1 + d)))
            self._m[key] = res
        return self._m[key]

    def scores(self, qs, fuzzy=True):
        rows, cols, vals = [], [], []
        for i, q in enumerate(qs):
            best = {}
            for t in tokens(q):
                for v, w in self.match(t, fuzzy): best[v] = max(best.get(v, 0), w)
            for v, w in best.items(): rows.append(i); cols.append(v); vals.append(w)
        Q = sparse.csr_matrix((vals, (rows, cols)), shape=(len(qs), len(self.vocab)))
        return (Q @ self.Nw.T).toarray().astype(np.float32)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---- taxonomy and menu names
    fams = [(f, ci, ci // 5) for ci, cl in enumerate(CLUSTERS) for f in cl]; NF = len(fams)
    fam_name = [f[0].lower() for f in fams]; fam_cl = np.array([f[1] for f in fams]); fam_cat = np.array([f[2] for f in fams])
    rank = rng.permutation(NF); fam_w = 1 / (rank + 1.0) ** 1.0; fam_w /= fam_w.sum()
    nm_fam, nm_mod, nm_txt = [], [], []
    for f in range(NF):
        pool = MODS_SWEET if fam_cat[f] == 5 else MODS_FOOD; ms = [-1] + [MOD_ID[m] for m in rng.choice(pool, 9, replace=False)]
        for m in ms:
            nm_fam.append(f); nm_mod.append(m); nm_txt.append(fam_name[f] if m < 0 else MODS[m] + " " + fam_name[f])
    nm_fam, nm_mod = np.array(nm_fam), np.array(nm_mod); NN = len(nm_txt); nm_cl = fam_cl[nm_fam]; nm_cat = fam_cat[nm_fam]
    names = pd.DataFrame({"name_id": np.arange(NN), "dish_name": nm_txt, "_family": nm_fam, "_modifier": nm_mod})
    families = pd.DataFrame({"family_id": np.arange(NF), "family_name": fam_name, "cluster": fam_cl, "category": [CATS[c] for c in fam_cat], "_demand_weight": fam_w})
    avail_p = 0.62 + 0.36 * (1 - rank / NF); avail = rng.random((N_AREA, NF)) < avail_p[None, :]
    # ---- restaurants and listings
    NR = N_AREA * REST_PER_AREA; r_area = np.repeat(np.arange(N_AREA), REST_PER_AREA)
    rest = pd.DataFrame({"restaurant_id": np.arange(NR), "area": r_area, "rating": np.clip(rng.normal(4.0, 0.35, NR), 3.0, 4.9).round(1), "prep_min": rng.integers(12, 41, NR),
                         "dist_km": np.round(np.clip(rng.lognormal(0.9, 0.5, NR), 0.3, 12), 1), "cost_for_two": rng.integers(150, 901, NR) // 10 * 10, "_pop": rng.lognormal(0, 0.8, NR)})
    lst = []
    for r in range(NR):
        favs = rng.choice(6, 2, replace=False); w = fam_w[nm_fam] ** 0.5 * np.where(np.isin(nm_cat, favs), 3.0, 1.0) * avail[r_area[r], nm_fam]
        pick = rng.choice(NN, LIST_PER_REST, replace=False, p=w / w.sum()); lst.append(np.c_[np.full(LIST_PER_REST, r), pick])
    lst = np.vstack(lst); L = len(lst); l_rest, l_name = lst[:, 0], lst[:, 1]; l_area = r_area[l_rest]
    lp = np.log(rest._pop.values[l_rest]) + np.log(fam_w[nm_fam[l_name]] * NF) + rng.normal(0, 0.4, L)
    base_price = np.array([240, 260, 120, 110, 200, 130]); price = np.round(base_price[nm_cat[l_name]] * rng.lognormal(0, 0.35, L), 0)
    listings = pd.DataFrame({"listing_id": np.arange(L), "restaurant_id": l_rest, "name_id": l_name, "price_inr": price, "orders_norm": ((lp - lp.mean()) / lp.std()).round(3)})
    listings = listings.merge(rest[["restaurant_id", "area", "rating", "prep_min", "dist_km", "cost_for_two"]], on="restaurant_id", how="left")
    rz = (rest.rating.values[l_rest] - 4.0) / 0.35; dz = (rest.dist_km.values[l_rest] - 2.8) / 1.5; pz = listings.orders_norm.values
    # ---- sessions: intents and queries
    typ = rng.choice(4, N_SESS, p=[0.52, 0.28, 0.12, 0.08]); fam = rng.choice(NF, N_SESS, p=fam_w); clu = rng.integers(0, 30, N_SESS)
    mod = np.where(typ == 1, -1, -1); q, mis, ed, clean = [], np.zeros(N_SESS, bool), np.zeros(N_SESS, int), []
    p_mis = 0.30 + 0.20 * rank[fam] / NF
    for i in range(N_SESS):
        t = typ[i]
        if t == 2:
            c = CLUSTER_WORDS[clu[i]]; m_ = rng.random() < 0.20; s = misspell(c, rng) if m_ else c; q.append(s); clean.append(c); mis[i] = m_; fam[i] = -1
        else:
            f = fam[i]; base = fam_name[f]; m_ = rng.random() < p_mis[i]; s = misspell(base, rng) if m_ else base; mis[i] = m_
            cb = base
            if t == 1:
                mod[i] = MOD_ID[(MODS_SWEET if fam_cat[f] == 5 else MODS_FOOD)[rng.integers(14)]]; s = MODS[mod[i]] + " " + s; cb = MODS[mod[i]] + " " + base
            if t == 3:
                qq = QUALIFIERS[rng.integers(len(QUALIFIERS))]; s = s + " " + qq; cb = cb + " " + qq
            q.append(s); clean.append(cb)
        ed[i] = lev(clean[-1], q[-1])
    q = np.array(q, object); day = rng.integers(0, DAYS, N_SESS); area = rng.integers(0, N_AREA, N_SESS); user = rng.integers(0, 20_000, N_SESS)
    # bot: 700 identical sessions of "biryani" (family 0 is Biryani) on days 20-21, area 0; no clicks
    bi = np.arange(700); bot_q = np.array(["biryani"] * 700, object)
    typ = np.r_[typ, np.zeros(700, int)]; fam = np.r_[fam, np.zeros(700, int)]; clu = np.r_[clu, np.zeros(700, int)]; mod = np.r_[mod, np.full(700, -1)]; q = np.r_[q, bot_q]
    mis = np.r_[mis, np.zeros(700, bool)]; ed = np.r_[ed, np.zeros(700, int)]; day = np.r_[day, rng.integers(20, 22, 700)]; area = np.r_[area, np.zeros(700, int)]; user = np.r_[user, np.full(700, 99_999)]
    bot = np.r_[np.zeros(N_SESS, bool), np.ones(700, bool)]; NS = len(q)
    # ---- relevance of every name for every intent
    def rel_vec(t, f, m, c):
        if t == 2: return np.where(nm_cl == c, 3, np.where(nm_cat == CLUSTERS_CAT(c), 1, 0))
        if m < 0: return np.where(nm_fam == f, 3, np.where(nm_cl == fam_cl[f], 2, np.where(nm_cat == fam_cat[f], 1, 0)))
        return np.where((nm_fam == f) & (nm_mod == m), 3, np.where(nm_fam == f, 2, np.where(nm_cl == fam_cl[f], 1, 0)))
    def CLUSTERS_CAT(c): return c // 5
    keys = {}; intent = np.zeros(NS, int); RELM = []
    for i in range(NS):
        k = (2, -1, -1, int(clu[i])) if typ[i] == 2 else (0, int(fam[i]), int(mod[i]), -1);
        if k not in keys: keys[k] = len(keys); RELM.append(rel_vec(typ[i] == 2 and 2 or 0, k[1], k[2], k[3]).astype(np.int8))
        intent[i] = keys[k]
    RELM = np.array(RELM)
    # ---- serving: production fuzzy lexical (90%) vs character n-gram trial (10%), then clicks
    lx = Lex(nm_txt); tri = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 3), sublinear_tf=True).fit(nm_txt); Nv = tri.transform(nm_txt)
    arm = (rng.random(NS) < 0.10) & ~bot; uq, qi = np.unique(q, return_inverse=True)
    LEXF = lx.scores(list(uq), True); poprank = pd.Series(pz).rank(pct=True).values; area_l = [np.where(l_area == a)[0] for a in range(N_AREA)]
    TRI = {}
    ta = np.unique(qi[arm])
    if len(ta): TRI = dict(zip(ta, (tri.transform(uq[ta]) @ Nv.T).toarray().astype(np.float32)))
    shown_cache = {}; shown = [None] * NS
    for i in range(NS):
        key = (qi[i], area[i], arm[i])
        if key not in shown_cache:
            la = area_l[area[i]]
            if arm[i]:
                s = TRI[qi[i]][l_name[la]]; ok = s > 0.05
            else:
                s = LEXF[qi[i]][l_name[la]]; ok = s > 0; s = s + 0.02 * poprank[la]
            idx = np.where(ok)[0]
            if len(idx) > 20: idx = idx[np.argpartition(-s[idx], 20)[:20]]
            idx = idx[np.argsort(-s[idx], kind="stable")]; shown_cache[key] = la[idx]
        shown[i] = shown_cache[key]
    imp_s, imp_p, imp_l, imp_c = [], [], [], []; nclk = np.zeros(NS, int); fpos = np.zeros(NS, int); ordl = np.full(NS, -1)
    for i in range(NS):
        sl = shown[i]; n = len(sl)
        if n == 0: continue
        rel = RELM[intent[i]][l_name[sl]]; z = A_REL[rel] + 0.55 * rz[sl] - 0.25 * dz[sl] + 0.20 * pz[sl] + rng.normal(0, 0.3, n)
        c = (rng.random(n) < EXAM[:n] / (1 + np.exp(-z))) & ~bot[i]
        imp_s.append(np.full(n, i)); imp_p.append(np.arange(1, n + 1)); imp_l.append(sl); imp_c.append(c.astype(int)); nclk[i] = c.sum()
        if c.any():
            fpos[i] = int(np.argmax(c)) + 1
            if rng.random() < 0.45: ordl[i] = sl[np.argmax(c)]
    imps = pd.DataFrame({"session_id": np.concatenate(imp_s), "position": np.concatenate(imp_p), "listing_id": np.concatenate(imp_l), "clicked": np.concatenate(imp_c)})
    # ---- messy raw query text and defects
    raw = q.astype(object).copy()
    up = rng.random(NS) < 0.06; raw[up] = [s.upper() for s in raw[up]]; sp = rng.random(NS) < 0.03; raw[sp] = ["  " + s.replace(" ", "   ") + " " for s in raw[sp]]
    qm = rng.random(NS) < 0.01; raw[qm] = [s + "?" for s in raw[qm]]; emp = (rng.random(NS) < 0.003) & ~bot; raw[emp] = ""
    sess = pd.DataFrame({"session_id": np.arange(NS), "user_id": user, "day": day, "area": area, "query_raw": raw, "served_arm": np.where(arm, "ngram_trial", "production"),
                         "n_results": [len(s) for s in shown], "n_clicks": nclk, "first_click_pos": fpos, "ordered_listing": ordl,
                         "_type": np.array(["dish", "dish_modifier", "vague", "multi_intent"])[typ], "_family": fam, "_cluster": np.where(typ == 2, clu, np.where(fam >= 0, fam_cl[np.maximum(fam, 0)], -1)),
                         "_modifier": mod, "_intent": intent, "_misspelled": mis, "_edit_dist": ed, "_bot": bot})
    dup = sess.sample(n=900, random_state=seed); sess = pd.concat([sess, dup], ignore_index=True)
    return dict(sessions=sess, impressions=imps, listings=listings, names=names, families=families, restaurants=rest.drop(columns="_pop"), RELM=RELM, avail=avail, fam_cl=fam_cl, fam_cat=fam_cat)


if __name__ == "__main__":
    import os, time
    t0 = time.time(); D = generate(); s = D["sessions"]
    print(len(s), "session rows |", len(D["impressions"]), "impressions |", len(D["listings"]), "listings |", round(time.time() - t0), "s")
    print(s._type.value_counts(normalize=True).round(3).to_dict(), "| misspelled", s._misspelled.mean().round(3), "| zero-result", (s.n_results == 0).mean().round(3), "| clicks>0", (s.n_clicks > 0).mean().round(3))
