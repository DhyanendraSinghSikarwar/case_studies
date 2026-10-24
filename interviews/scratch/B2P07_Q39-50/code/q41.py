# Standalone, numpy only. TOY: hand-made captions, hand-made OCR strings and hand-made "image feature" vectors.
# The word->feature lexicon is a stand-in for a joint text-image encoder. It says NOTHING about real CLIP-style or ColPali-style quality.
import re, numpy as np
FEATS = ["line_down", "line_up", "pie", "bar", "red", "blue", "table", "photo"]
#  id: (caption written by a captioner (generic), OCR text (with errors), true visual features)
ITEMS = {
 "i1": ("a line chart of sales",            "Sales 2024 Q1 Q2 Q3 Q4",        {"line_down": 1, "red": 1}),
 "i2": ("a line chart of sales",            "Sales 2024 Q1 Q2 Q3 Q4",        {"line_up": 1, "blue": 1}),
 "i3": ("a pie chart of market share",      "Market sh@re Acme 61% Other 39%", {"pie": 1, "red": 1}),
 "i4": ("a bar chart of costs",             "Cost by dept. Opex 4.2 Capex 1.1", {"bar": 1, "blue": 1}),
 "i5": ("a table of prices",                "Plan Price Basic 499 Pro 999",  {"table": 1}),
 "i6": ("a photo of a warehouse",           "",                              {"photo": 1}),
 "i7": ("a pie chart of cost split",        "Cost split R&D 30% Ops 70%",    {"pie": 1, "blue": 1}),
 "i8": ("a table of sales by region",       "Region Sales South 240 North 200", {"table": 1}),
}
LEX = {"falling": {"line_down": 1}, "declining": {"line_down": 1}, "rising": {"line_up": 1}, "growing": {"line_up": 1},
       "pie": {"pie": 1}, "bar": {"bar": 1}, "red": {"red": 1}, "blue": {"blue": 1}, "table": {"table": 1}, "photo": {"photo": 1}}
vec = lambda d: np.array([d.get(f, 0.0) for f in FEATS], float)
IMG = {k: vec(v[2]) for k, v in ITEMS.items()}
words = lambda s: set(re.findall(r"[a-z0-9]+", s.lower()))
def qfeat(q):
    d = {}
    for w in words(q): d.update(LEX.get(w, {}))
    return vec(d)

# (query, set of relevant image ids)
QUERIES = [("pie chart of market share", {"i3"}),               # text-answerable (caption has it)
           ("table of prices", {"i5"}),                          # text-answerable
           ("falling sales line chart", {"i1"}),                 # needs visual detail: caption cannot tell i1 from i2
           ("rising sales line chart", {"i2"}),
           ("red pie chart", {"i3"}),                            # colour is not in captions
           ("blue pie chart", {"i7"}),
           ("Acme 61% share", {"i3"}),                           # text inside the image (OCR territory)
           ("Opex 4.2", {"i4"})]

def s_caption(q, i): return len(words(q) & words(ITEMS[i][0]))
def s_ocr(q, i): return len(words(q) & words(ITEMS[i][1]))
def s_feat(q, i):
    a, b = qfeat(q), IMG[i]; n = np.linalg.norm(a) * np.linalg.norm(b); return float(a @ b / n) if n else 0.0
def s_cap_ocr(q, i): return s_caption(q, i) + s_ocr(q, i)
def s_combo(q, i): return s_cap_ocr(q, i) + 2 * s_feat(q, i)

def hit1(score):                                      # strict top-1: the relevant image must beat every other; a tie counts as a MISS
    h = []
    for q, rel in QUERIES:
        ranked = sorted(ITEMS, key=lambda i: (-score(q, i), i)); h.append(ranked[0] in rel and score(q, ranked[0]) > score(q, ranked[1]))
    return h
print(f"{'query':28s}" + "".join(f"{n:>10s}" for n in ["caption", "cap+ocr", "feature", "combined"]))
res = {n: hit1(f) for n, f in [("caption", s_caption), ("cap+ocr", s_cap_ocr), ("feature", s_feat), ("combined", s_combo)]}
for k, (q, _) in enumerate(QUERIES): print(f"{q:28s}" + "".join(f"{('ok' if res[n][k] else 'MISS'):>10s}" for n in res))
print("top-1 hit rate:", {n: round(float(np.mean(h)), 2) for n, h in res.items()})

# OCR noise: one wrong character breaks an exact-token match
noisy = "Market sh@re Acme 61% Other 39%"
print("OCR token 'share' found in noisy OCR:", "share" in words(noisy), "| in clean text:", "share" in words("Market share Acme 61%"))
