"""
SYNTHETIC DATA GENERATOR - CASE STUDY 13 (Flipkart-style Hinglish search query translation)
==========================================================================================
THIS DATA IS SYNTHETIC. Flipkart's query logs and tagged sets are confidential and not public.

Documented context (arXiv 2208.03713, Kulkarni, Chennabasavaraj, Garera; Flipkart): about 21% of queries are Hinglish
(Hindi words typed in Latin script); no parallel data; spelling errors and brand misspellings; "articulation gap"
queries ("juta bina dori wala" for "shoe without lace"); pseudo-labels from third-party translation APIs, then a small
human-tagged set; test sets stratified Head / Torso / Tail.

Simulation (calibrated only to the 21% Hinglish share; everything else is assumed):
  * An intent (item, colour, audience, feature, price cap, adjective, brand) is drawn from long-tailed distributions.
  * It is rendered either in English, or in Hinglish: Hindi word order, Hindi words typed with random spelling
    variants, English words mixed in, occasional English-order Hinglish, and rare "articulation gap" phrases.
  * A noisy "third-party translation API" column (word-for-word, canonical spellings only, no reordering) gives the
    pseudo-labels. A small human-tagged set has the true English query and per-word language tags.
  * A small English product catalogue lets us measure search success before and after translation.
Hidden truth columns start with "_".

Outputs (written by the notebook): query_log.csv.gz, human_tagged.csv.gz, catalogue.csv.gz
"""
import random
import numpy as np
import pandas as pd

SEED = 42
N_QUERIES = 150_000
P_HI_MODE = 0.274          # chosen so that about 21% of queries contain at least one Hindi word

# ----- lexicon -------------------------------------------------------------------------------------------
# (English gold word, [Hindi spellings (canonical) with the first used most], group)
ITEMS = [("shoes", ["joote", "juta"], "wear"), ("mobile", [], "tech"), ("clothes", ["kapde"], "wear"), ("shirt", [], "wear"),
         ("watch", ["ghadi"], "wear"), ("slippers", ["chappal"], "wear"), ("bag", ["thaila"], "wear"), ("headphones", [], "tech"),
         ("charger", [], "tech"), ("cover", [], "tech"), ("jeans", [], "wear"), ("kurta", [], "wear"), ("tshirt", [], "wear"),
         ("saree", [], "wear"), ("laptop", [], "tech"), ("bottle", [], "home"), ("sunglasses", ["chashma"], "wear"),
         ("cap", ["topi"], "wear"), ("cooker", [], "home"), ("mixer", [], "home"), ("rice", ["chawal"], "food"),
         ("tea", ["chai"], "food"), ("oil", ["tel"], "food"), ("flour", ["atta"], "food"), ("chair", ["kursi"], "home"),
         ("table", ["mez"], "home"), ("bedsheet", ["chadar"], "home"), ("pillow", ["takiya"], "home"), ("fan", ["pankha"], "home"),
         ("mirror", ["sheesha"], "home"), ("toy", ["khilona"], "other"), ("book", ["kitab"], "other"), ("pen", ["kalam"], "other"),
         ("mattress", ["gadda"], "home"), ("curtains", ["parda"], "home"), ("utensils", ["bartan"], "home"), ("bucket", ["baalti"], "home"),
         ("lentils", ["dal"], "food"), ("sugar", ["cheeni"], "food"), ("milk", ["doodh"], "food"), ("salt", ["namak"], "food"),
         ("wardrobe", ["almari"], "home"), ("doll", ["gudiya"], "other"), ("wok", ["kadhai"], "home"), ("griddle", ["tawa"], "home"),
         ("scissors", ["kainchi"], "home"), ("lock", ["taala"], "home"), ("key", ["chaabi"], "home"), ("rope", ["rassi"], "home")]
COLOURS = [("black", ["kala"]), ("red", ["lal"]), ("blue", ["neela"]), ("white", ["safed"]), ("green", ["hara"]), ("yellow", ["peela"]),
           ("pink", ["gulabi"]), ("brown", ["bhoora"]), ("orange", ["narangi"])]
ADJ = {"wear": [("cheap", "sasta"), ("light", "halka"), ("strong", "mazboot"), ("long", "lamba"), ("big", "bada"), ("small", "chota")],
       "home": [("cheap", "sasta"), ("big", "bada"), ("small", "chota"), ("strong", "mazboot"), ("thick", "mota")],
       "tech": [("cheap", "sasta"), ("strong", "mazboot"), ("light", "halka")], "food": [("cheap", "sasta"), ("big", "bada")],
       "other": [("cheap", "sasta"), ("big", "bada"), ("small", "chota")]}
AUD = [("women", "mahila", "ladies"), ("men", "mard", "gents"), ("kids", "bachchon", "kids"), ("girls", "ladkiyon", "girls"), ("boys", "ladkon", "boys")]
FEAT = [("laces", "dori"), ("pockets", "jeb"), ("lid", "dhakkan"), ("handle", "hatthe"), ("wheels", "pahiye")]
BRANDS = ["nike", "adidas", "puma", "samsung", "boat", "redmi", "philips", "prestige", "bata", "levis", "realme", "sony", "hp", "milton", "wildcraft"]
PRICES = [199, 299, 399, 499, 599, 799, 999, 1499, 1999, 2999]
# articulation-gap phrases: (English gold, Hindi-typed variants, which tokens are English)
GAPS = [("washing machine", ["kapde dhone wali machine", "kapde dhone ki machine"]), ("earphones", ["kaan mein lagane wala", "kaan mein lagane wale speaker"]),
        ("hair dryer", ["baal sukhane wala", "baal sukhane ki machine"]), ("water heater", ["pani garam karne wala", "pani garam karne ki rod"]),
        ("iron", ["kapde press karne wala", "kapde press karne ki machine"]), ("pressure cooker", ["dal pakane ka bartan", "jaldi pakane wala bartan"]),
        ("trimmer", ["dadhi banane wali machine", "dadhi kaatne wali machine"]), ("mosquito racket", ["machhar maarne wala", "machhar maarne ka bat"]),
        ("power bank", ["mobile charge karne wala dabba", "phone charge karne ka dabba"]), ("laptop bag", ["laptop rakhne ka thaila", "laptop rakhne wala bag"])]
ENG_WORDS = {"machine", "speaker", "press", "rod", "bat", "mobile", "charge", "phone", "laptop", "bag"}
FUNC = {"ke": "", "liye": "for", "bina": "without", "saath": "with", "wala": "", "wali": "", "wale": "", "neeche": "under", "se": "", "kam": "under", "tak": "under", "aur": "and"}

# canonical Hindi -> English (what a "third-party API" knows)
CANON = {}
for en, his, g in ITEMS:
    for h in his: CANON[h] = en
for en, his in COLOURS:
    for h in his: CANON[h] = en
for g, lst in ADJ.items():
    for en, h in lst: CANON[h] = en
for en, h, _ in AUD: CANON[h] = en
for en, h in FEAT: CANON[h] = en
CANON.update({k: v for k, v in FUNC.items()})
ALL_ENGLISH_ITEMS = [i[0] for i in ITEMS] + [g[0] for g in GAPS]

RULES = [("aa", "a"), ("a", "aa"), ("ee", "i"), ("i", "ee"), ("oo", "u"), ("u", "oo"), ("sh", "s"), ("s", "sh"), ("v", "w"), ("w", "v"),
         ("ch", "chh"), ("chh", "ch"), ("th", "t"), ("t", "th"), ("dh", "d"), ("ai", "ay"), ("au", "ow"), ("o", "oo"), ("e", "a"), ("k", "c")]


def variant(tok, rnd, p=0.6):
    """Random transliteration variant of a Hindi word typed in Latin script."""
    if rnd.random() > p or len(tok) < 3: return tok
    s = tok
    for _ in range(rnd.choice([1, 1, 1, 2])):
        ap = [r for r in RULES if r[0] in s]
        if not ap: break
        a, b = rnd.choice(ap); idx = [i for i in range(len(s)) if s.startswith(a, i)]; i = rnd.choice(idx); s = s[:i] + b + s[i + len(a):]
    r = rnd.random()
    if r < 0.12 and s[-1] in "aei": s = s[:-1]
    elif r < 0.17 and len(s) > 4: i = rnd.randrange(1, len(s) - 1); s = s[:i] + s[i + 1:]
    elif r < 0.21: i = rnd.randrange(1, len(s)); s = s[:i] + s[i - 1] + s[i:]
    return s


def typo(tok, rnd, p=0.04):
    if len(tok) < 5 or rnd.random() > p: return tok
    i = rnd.randrange(1, len(tok) - 1)
    return tok[:i] + tok[i + 1:] if rnd.random() < 0.5 else tok[:i] + tok[i + 1] + tok[i] + tok[i + 2:]


def _zipf(n, s, rnd_unused=None):
    w = 1.0 / (np.arange(n) + 1.5) ** s; return (w / w.sum()).tolist()


TEMPLATES = ["item", "col_item", "item_adj", "aud_item", "aud_col_item", "without", "with", "price", "brand_item", "item_and", "gap", "adj_col_item"]
TW = [0.27, 0.15, 0.07, 0.12, 0.04, 0.04, 0.04, 0.08, 0.10, 0.03, 0.03, 0.03]


def make_intent(rnd, wi, wc, wa, wf, wp, wb):
    t = rnd.choices(TEMPLATES, TW)[0]; it = {"template": t}
    if t == "gap":
        g = rnd.randrange(len(GAPS)); it.update(item=GAPS[g][0], gap=g, group="home"); return it
    k = rnd.choices(range(len(ITEMS)), wi)[0]; en, his, grp = ITEMS[k]; it.update(item=en, k=k, group=grp)
    if t in ("col_item", "aud_col_item", "adj_col_item"): it["col"] = rnd.choices(range(len(COLOURS)), wc)[0]
    if t in ("aud_item", "aud_col_item"): it["aud"] = rnd.choices(range(len(AUD)), wa)[0]
    if t in ("item_adj", "adj_col_item"): it["adj"] = rnd.randrange(len(ADJ[grp]))
    if t in ("without", "with"): it["feat"] = rnd.choices(range(len(FEAT)), wf)[0]
    if t == "price": it["price"] = rnd.choices(PRICES, wp)[0]
    if t == "brand_item": it["brand"] = rnd.choices(BRANDS, wb)[0]
    if t == "item_and":
        j = rnd.choices(range(len(ITEMS)), wi)[0]
        if j == k: j = (j + 1) % len(ITEMS)
        it["item2"] = ITEMS[j][0]; it["k2"] = j
    if t in ("aud_item", "aud_col_item") and grp not in ("wear",): it["template"] = "item" if t == "aud_item" else "col_item"; it.pop("aud")
    if "col" in it and grp in ("food", "other"): it["template"] = {"col_item": "item", "aud_col_item": "aud_item", "adj_col_item": "item_adj"}[it["template"]]; it.pop("col");
    if it["template"] == "item_adj" and "adj" not in it: it["adj"] = rnd.randrange(len(ADJ[grp]))
    if it["template"] == "aud_item" and "aud" not in it: it["aud"] = rnd.choices(range(len(AUD)), wa)[0]
    return it


def gold_english(it):
    t = it["template"]; item = it["item"]; grp = it["group"]
    col = COLOURS[it["col"]][0] if "col" in it else None; aud = AUD[it["aud"]][0] if "aud" in it else None
    adj = ADJ[grp][it["adj"]][0] if "adj" in it else None
    if t == "gap": return item
    if t == "item": return item
    if t == "col_item": return f"{col} {item}"
    if t == "item_adj": return f"{adj} {item}"
    if t == "aud_item": return f"{item} for {aud}"
    if t == "aud_col_item": return f"{col} {item} for {aud}"
    if t == "without": return f"{item} without {FEAT[it['feat']][0]}"
    if t == "with": return f"{item} with {FEAT[it['feat']][0]}"
    if t == "price": return f"{item} under {it['price']}"
    if t == "brand_item": return f"{it['brand']} {item}"
    if t == "item_and": return f"{item} and {it['item2']}"
    if t == "adj_col_item": return f"{adj} {col} {item}"


def _hi_pick(his, rnd):
    if not his: return None
    return his[0] if len(his) == 1 or rnd.random() < 0.6 else his[1]


def render(it, hi_mode, rnd):
    """Return list of (token, lang) with lang in {'h','e'}."""
    t = it["template"]; grp = it["group"]
    E = lambda w: [(x, "e") for x in w.split()]
    if t == "gap":
        if not hi_mode: return E(it["item"])
        ph = rnd.choice(GAPS[it["gap"]][1]); return [(variant(w, rnd) if w not in ENG_WORDS else w, "e" if w in ENG_WORDS else "h") for w in ph.split()]
    if not hi_mode:
        return [(typo(w, rnd), "e") for w, _l in E(gold_english(it))]
    en_order = rnd.random() < 0.15; P = 0.85
    def item_tok(en, his):
        h = _hi_pick(his, rnd)
        return [(variant(h, rnd), "h")] if (h and rnd.random() < P) else [(typo(en, rnd), "e")]
    en_, his_, _g = ITEMS[it["k"]]; IT = item_tok(en_, his_)
    def col_tok():
        en, his = COLOURS[it["col"]]; return [(variant(his[0], rnd), "h")] if rnd.random() < P else [(en, "e")]
    def adj_tok():
        en, h = ADJ[grp][it["adj"]]; return [(variant(h, rnd), "h")] if rnd.random() < P else [(en, "e")]
    def aud_tok():
        en, h, alt = AUD[it["aud"]]; return [(variant(h, rnd), "h")] if rnd.random() < P else [(alt, "e")]
    def feat_tok():
        en, h = FEAT[it["feat"]]; return [(variant(h, rnd), "h")] if rnd.random() < P else [(en, "e")]
    F = lambda w: [(variant(w, rnd, 0.5), "h")]
    if t == "item": return IT
    if t == "col_item": return col_tok() + IT
    if t == "adj_col_item": return adj_tok() + col_tok() + IT
    if t == "item_adj": return (adj_tok() + IT) if en_order else (IT + adj_tok())
    if t == "aud_item": return (IT + [("for", "e")] + aud_tok()) if en_order else (aud_tok() + F("ke") + F("liye") + IT)
    if t == "aud_col_item": return (col_tok() + IT + [("for", "e")] + aud_tok()) if en_order else (aud_tok() + F("ke") + F("liye") + col_tok() + IT)
    if t == "without": return (IT + [("without", "e")] + feat_tok()) if en_order else (IT + F("bina") + feat_tok() + F(rnd.choice(["wala", "wala", "wali", "wale"])))
    if t == "with":
        if en_order: return IT + [("with", "e")] + feat_tok()
        return (feat_tok() + F(rnd.choice(["wala", "wali", "wale"])) + IT) if rnd.random() < 0.6 else (IT + feat_tok() + F("ke") + F("saath"))
    if t == "price":
        n = [(str(it["price"]), "e")]
        if en_order: return IT + [("under", "e")] + n
        r = rnd.random(); return (n + F("ke") + F("neeche") + IT) if r < 0.4 else ((IT + n + F("se") + F("kam")) if r < 0.75 else (IT + n + F("tak")))
    if t == "brand_item": return [(it["brand"], "e")] + IT
    if t == "item_and":
        en2, his2, _ = ITEMS[it["k2"]]; return IT + (F("aur") if not en_order else [("and", "e")]) + item_tok(en2, his2)
    raise ValueError(t)


def api_translate(tokens, rnd):
    """Noisy third-party API: word for word, canonical spellings only, no reordering, 6% random mistranslations."""
    out = []
    vocab = list(set(CANON.values()))
    for w in tokens:
        if w in CANON:
            e = CANON[w]
            if rnd.random() < 0.06 and e: e = rnd.choice(vocab)
            if e: out.append(e)
        else:
            out.append(w)
    return " ".join(out)


def build_catalogue(rnd, per_item=200):
    rows = []; pid = 0
    for en in ALL_ENGLISH_ITEMS:
        grp = next((g for e, _h, g in ITEMS if e == en), "home")
        for _ in range(per_item):
            col = rnd.choice(COLOURS)[0] if grp in ("wear", "home", "tech") and rnd.random() < 0.65 else None
            aud = rnd.choice(AUD)[0] if grp == "wear" and rnd.random() < 0.8 else None
            feat = rnd.choice(FEAT)[0] if grp in ("wear", "home") and rnd.random() < 0.3 else None
            brand = rnd.choice(BRANDS); price = int(round(np.exp(np.log(900) + rnd.gauss(0, 0.9))))
            extra = rnd.choice(["", "", "stylish", "premium", "pack of 2", "new", "combo"])
            title = " ".join(x for x in [brand, col, en, ("for " + aud) if aud else None, ("with " + feat) if feat else None, extra] if x)
            rows.append((pid, title, en, col or "", aud or "", feat or "", brand, price)); pid += 1
    return pd.DataFrame(rows, columns=["product_id", "title", "item", "colour", "audience", "feature", "brand", "price_inr"])


def generate(seed=SEED, n=N_QUERIES):
    rnd = random.Random(seed)
    wi, wc, wa, wf, wp, wb = _zipf(len(ITEMS), 1.0), _zipf(len(COLOURS), 0.9), _zipf(len(AUD), 0.8), _zipf(len(FEAT), 0.8), _zipf(len(PRICES), 0.8), _zipf(len(BRANDS), 0.9)
    rows = []
    for q in range(n):
        it = make_intent(rnd, wi, wc, wa, wf, wp, wb); hi_mode = rnd.random() < P_HI_MODE
        toks = render(it, hi_mode, rnd); raw = " ".join(w for w, _ in toks); langs = " ".join(l for _, l in toks); gold = gold_english(it)
        if it["template"] == "item_and": gold_items = f"{it['item']}|{it['item2']}"
        else: gold_items = it["item"]
        rows.append((q, rnd.randrange(90), rnd.choices(["android", "ios", "web"], [0.72, 0.1, 0.18])[0], raw,
                     api_translate(raw.split(), rnd), gold, langs, it["template"], gold_items,
                     COLOURS[it["col"]][0] if "col" in it else "", AUD[it["aud"]][0] if "aud" in it else "", int("h" in langs.split()), int(it["template"] == "gap" and "h" in langs.split())))
    log = pd.DataFrame(rows, columns=["query_id", "day", "device", "raw_query", "api_translation", "_gold_en", "_tok_lang", "_template", "_items", "_colour", "_audience", "_is_hinglish", "_is_gap"])
    # strata by traffic share of Hinglish raw strings
    h = log[log._is_hinglish == 1]; vc = h.raw_query.value_counts(); cum = vc.cumsum() / vc.sum()
    stratum = pd.Series(np.where(cum <= 1 / 3, "head", np.where(cum <= 2 / 3, "torso", "tail")), index=vc.index)
    log["_stratum"] = np.where(log._is_hinglish == 1, log.raw_query.map(stratum), "")
    # human-tagged set: test (1,000 Hinglish per stratum + 3,000 English) and train pool (uniform draw)
    r2 = np.random.default_rng(seed + 1); test_ids = []
    for s in ("head", "torso", "tail"): test_ids += r2.choice(log.query_id[log._stratum == s].values, 1000, replace=False).tolist()
    test_ids += r2.choice(log.query_id[log._is_hinglish == 0].values, 3000, replace=False).tolist()
    rest = log[~log.query_id.isin(test_ids)]
    train_ids = r2.choice(rest.query_id[rest._is_hinglish == 1].values, 9000, replace=False).tolist() + r2.choice(rest.query_id[rest._is_hinglish == 0].values, 6000, replace=False).tolist()
    tag = log[log.query_id.isin(test_ids + train_ids)].copy(); tag["split"] = np.where(tag.query_id.isin(test_ids), "test", "train")
    tagged = tag[["query_id", "raw_query", "_gold_en", "_tok_lang", "split"]].rename(columns={"_gold_en": "human_translation", "_tok_lang": "human_token_lang"}).reset_index(drop=True)
    cat = build_catalogue(rnd)
    return log, tagged, cat


if __name__ == "__main__":
    import time
    t0 = time.time(); lg, tg, ct = generate(); print(len(lg), "queries,", round(lg._is_hinglish.mean(), 4), "Hinglish share,", len(tg), "tagged,", len(ct), "products,", round(time.time() - t0, 1), "s")
    print(lg.sample(12, random_state=1)[["raw_query", "_gold_en", "api_translation"]].to_string())
    print(lg[lg._is_hinglish == 1]._stratum.value_counts(), lg.raw_query[lg._is_hinglish == 1].nunique())
