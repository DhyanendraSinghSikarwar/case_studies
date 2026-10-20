"""
SYNTHETIC DATA GENERATOR - CASE STUDY 14 (Myntra ShopLook: visual similar-item retrieval)
=========================================================================================
THIS DATA IS SYNTHETIC. No images and no neural networks are used: image embeddings are SIMULATED.

Documented context (Ravi et al., "Buy Me That Look", arXiv 2008.11638): four-stage pipeline (full-shot detection,
article localisation with Mask R-CNN, triplet-network embedding, cosine retrieval); about 20 apparel types;
Street2Shop pairs for hard positives; active learning lifted detection AP (topwear 82.65 -> 87.60, bottomwear
87.11 -> 90.25, skirts 51.42 -> 69.09, footwear 87.32 -> 88.47, bags 69.71 -> 78.37).

Simulation:
  * Catalogue: 6,000 items, 10 article types in the 5 documented groups, with colour (8 hues), pattern (6) and
    style (5) attributes. Each item has a hidden "true visual identity" vector z (14 dims).
  * "Frozen backbone" embeddings (64 dims) = linear mix of z + nuisance factors (background, pose, lighting)
    + noise. Catalogue photos are clean studio shots, model photos are noisier, street photos noisiest and
    shifted (domain shift). A colour histogram is also observed (the handcrafted baseline).
  * Outfits: 2,500 model images with 2 to 4 garments each. A detector finds each garment with probability equal
    to its group's AP before / after active learning (our assumption: AP used as detection probability); a
    badly localised crop leaks part of another garment's embedding into the query.
  * Training data: 3,600 train items x 2 street photos (Street2Shop-style hard anchors).
Hidden truth for a DIGITAL-TWIN online test: click and add-to-cart probability depend on the true visual
similarity (computed from z) and item popularity.

Outputs: data/cs14/items.csv.gz, garments.csv.gz, embeddings.npz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N_ITEMS, D, ZD, ND = 6000, 64, 14, 16
TYPES = ["tshirt", "shirt", "jacket", "jeans", "trousers", "skirt", "sneakers", "heels", "handbag", "backpack"]
GROUP = ["topwear", "topwear", "topwear", "bottomwear", "bottomwear", "skirts", "footwear", "footwear", "bags", "bags"]
AP_BEFORE = {"topwear": 0.8265, "bottomwear": 0.8711, "skirts": 0.5142, "footwear": 0.8732, "bags": 0.6971}
AP_AFTER = {"topwear": 0.8760, "bottomwear": 0.9025, "skirts": 0.6909, "footwear": 0.8847, "bags": 0.7837}
TYPE_P = np.array([0.17, 0.13, 0.08, 0.13, 0.09, 0.07, 0.10, 0.07, 0.10, 0.06])
COLOURS = ["black", "white", "blue", "red", "green", "yellow", "pink", "brown"]
COLOUR_P = np.array([0.24, 0.16, 0.18, 0.09, 0.08, 0.06, 0.09, 0.10])
PATTERNS = ["solid", "striped", "checked", "floral", "printed", "colourblock"]
PATTERN_P = np.array([0.42, 0.13, 0.11, 0.10, 0.16, 0.08])
N_STYLE = 5
SIG_CAT, SIG_MODEL, SIG_STREET = 0.7, 1.1, 1.6


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---- items and hidden visual identity z -------------------------------------------------
    typ = rng.choice(10, N_ITEMS, p=TYPE_P); col = rng.choice(8, N_ITEMS, p=COLOUR_P); pat = rng.choice(6, N_ITEMS, p=PATTERN_P); sty = rng.integers(0, N_STYLE, N_ITEMS)
    Tc = rng.normal(0, 1.6, (10, 4)); Pc = rng.normal(0, 1.2, (6, 3)); Sc = rng.normal(0, 1.0, (N_STYLE, 3))
    ang = np.arange(8) * 2 * np.pi / 8; Hue = 1.4 * np.stack([np.cos(ang), np.sin(ang)], 1)
    z = np.zeros((N_ITEMS, ZD))
    z[:, 0:4] = Tc[typ] + rng.normal(0, 0.3, (N_ITEMS, 4))
    z[:, 4:6] = Hue[col] + rng.normal(0, 0.18, (N_ITEMS, 2)); z[:, 6:8] = rng.normal(0, 0.5, (N_ITEMS, 2))
    z[:, 8:11] = Pc[pat] + rng.normal(0, 0.25, (N_ITEMS, 3))
    z[:, 11:14] = Sc[sty] + rng.normal(0, 0.5, (N_ITEMS, 3))
    pop = rng.pareto(1.5, N_ITEMS) + 1; logpop = np.log(pop); logpop = (logpop - logpop.mean()) / logpop.std()
    base_price = np.array([649, 899, 1799, 1199, 999, 799, 1499, 1299, 1399, 1099.0])
    price = np.round(base_price[typ] * np.exp(rng.normal(0, 0.45, N_ITEMS)), 0)
    # ---- simulated "frozen backbone" -------------------------------------------------------
    def orth(r, c):
        q, _ = np.linalg.qr(rng.normal(0, 1, (r, c))); return q
    A = 2.2 * orth(D, ZD); B = 2.0 * orth(D, ND)
    d_street = rng.normal(0, 0.8, D); d_model = 0.4 * d_street

    def embed(zz, sigma, offset):
        n = rng.normal(0, 1, (len(zz), ND)) * sigma
        return zz @ A.T + n @ B.T + offset[None, :] + rng.normal(0, 0.35, (len(zz), D))
    E_cat = embed(z, SIG_CAT, np.zeros(D))
    hue_soft = lambda c: np.exp(-0.5 * (np.minimum((np.arange(8)[None, :] - c[:, None]) % 8, (c[:, None] - np.arange(8)[None, :]) % 8) / 0.9) ** 2)
    H_cat = hue_soft(col); H_cat = np.abs(H_cat + rng.normal(0, 0.12, H_cat.shape)); H_cat /= H_cat.sum(1, keepdims=True)
    # ---- train / test split and street training photos -------------------------------------
    perm = rng.permutation(N_ITEMS); train_items = np.sort(perm[:3600]); test_items = np.sort(perm[3600:])
    tr_item = np.repeat(train_items, 2); E_tr = embed(z[tr_item], SIG_STREET, d_street)
    # ---- outfits and garments ----------------------------------------------------------------
    n_out = 2500; ng = rng.choice([2, 3, 4], n_out, p=[0.35, 0.40, 0.25]); rows = []
    by_type = {t: test_items[typ[test_items] == t] for t in range(10)}
    for o in range(n_out):
        ts = rng.choice(10, ng[o], replace=False, p=TYPE_P)
        for t in ts: rows.append((o, int(rng.choice(by_type[int(t)])), int(t)))
    g = pd.DataFrame(rows, columns=["outfit", "item", "article_type"]); Q = len(g)
    g["group"] = [GROUP[t] for t in g.article_type]
    ap_b = g.group.map(AP_BEFORE).values; ap_a = g.group.map(AP_AFTER).values
    u1, u2 = rng.random(Q), rng.random(Q)
    g["detected_before"] = (u1 < ap_b).astype(int); g["detected_after"] = (u1 < ap_a).astype(int)
    g["messy_before"] = (u2 < 1.2 * (1 - ap_b)).astype(int); g["messy_after"] = (u2 < 1.2 * (1 - ap_a)).astype(int)
    g["_leak_u"] = rng.uniform(0.25, 0.55, Q)
    # contaminating garment = another garment in the same outfit (first different row of the outfit)
    first = g.groupby("outfit").cumcount().values; start = g.index.values - first; size = g.groupby("outfit").item.transform("size").values
    other_pos = start + (first + 1) % size
    E_q_clean = embed(z[g.item.values], SIG_MODEL, d_model); E_q_other = E_q_clean[other_pos]
    qhist = hue_soft(col[g.item.values]); H_q = np.abs(qhist + rng.normal(0, 0.28, qhist.shape)); H_q /= H_q.sum(1, keepdims=True)
    # ---- items table incl. data-quality defects --------------------------------------------
    label = typ.copy(); wrong = rng.random(N_ITEMS) < 0.02; label[wrong] = rng.integers(0, 10, wrong.sum())
    items = pd.DataFrame({"item": np.arange(N_ITEMS), "article_type": [TYPES[t] for t in label], "colour": [COLOURS[c] for c in col], "pattern": [PATTERNS[p] for p in pat],
                          "price_inr": price, "units_90d": rng.poisson(12 * pop), "is_train": np.isin(np.arange(N_ITEMS), train_items).astype(int), "_true_type": typ, "_true_colour": col, "_true_pattern": pat, "_style": sty, "_log_pop_z": logpop})
    for k in range(ZD): items[f"_z{k}"] = z[:, k]
    # near-duplicate listings: 60 items re-listed with an almost identical embedding (a different item id)
    dsrc = rng.choice(test_items, 60, replace=False); dup_ids = np.arange(N_ITEMS, N_ITEMS + 60)
    dup_rows = items.loc[dsrc].copy(); dup_rows["item"] = dup_ids; dup_rows["is_train"] = 0; dup_rows["_dup_of"] = dsrc; items["_dup_of"] = -1
    items = pd.concat([items, dup_rows], ignore_index=True)
    E_cat = np.vstack([E_cat, E_cat[dsrc] + rng.normal(0, 0.05, (60, D))]); H_cat = np.vstack([H_cat, H_cat[dsrc]])
    bad = rng.choice(N_ITEMS, 90, replace=False); E_cat[bad[:60]] = 0.0; E_cat[bad[60:]] = np.nan   # failed image processing
    items["embedding_ok"] = 1; items.loc[bad, "embedding_ok"] = 0
    miss = rng.random(len(items)) < 0.015; items["colour"] = items["colour"].where(~miss, None)
    g["article_type_name"] = [TYPES[t] for t in g.article_type]
    arrays = dict(E_cat=E_cat.astype(np.float32), H_cat=H_cat.astype(np.float32), E_tr=E_tr.astype(np.float32), tr_item=tr_item, E_q_clean=E_q_clean.astype(np.float32),
                  E_q_other=E_q_other.astype(np.float32), H_q=H_q.astype(np.float32))
    return items, g, arrays


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs14"), exist_ok=True)
    it, g, ar = generate(); it.to_csv(os.path.join(here, "cs14", "items.csv.gz"), index=False); g.to_csv(os.path.join(here, "cs14", "garments.csv.gz"), index=False)
    np.savez_compressed(os.path.join(here, "cs14", "embeddings.npz"), **ar); print(len(it), "items", len(g), "garments", {k: v.shape for k, v in ar.items()})
