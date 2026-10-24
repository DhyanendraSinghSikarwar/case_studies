# Standalone, standard library only. TOY: an invented company and made-up numbers; no PDF parsing, no LLM (a keyword lookup stands in for retrieval).
import re
table = {"company": "ToyCo Ltd", "caption": "Consolidated statement of profit and loss", "unit": "Rs crore", "page": 41,
         "columns": ["FY2024", "FY2025"],
         "rows": [("Revenue from operations", [1200.0, 1380.0]), ("Operating expenses", [900.0, 1010.0]), ("Net profit", [150.0, 190.0])]}

def row_sentences(t):                                   # one self-contained sentence per (row, period): keeps unit, period, source
    out = []
    for name, vals in t["rows"]:
        for col, v in zip(t["columns"], vals):
            out.append({"text": f"{t['company']}, {t['caption']}, {col}: {name} was {v:,.1f} {t['unit']}.",
                        "meta": {"company": t["company"], "period": col, "page": t["page"], "unit": t["unit"], "value": v, "row": name}})
    return out
chunks = row_sentences(table)
print(chunks[0]["text"]); print(chunks[0]["meta"])

def retrieve(q, chunks):                                 # TOY keyword-overlap retrieval (a real system: hybrid BM25 + dense, filtered by company and period)
    qw = set(re.findall(r"\w+", q.lower()))
    return max(chunks, key=lambda c: len(qw & set(re.findall(r"\w+", c["text"].lower()))))
def lookup(row, period):
    return retrieve(f"{row} {period}", [c for c in chunks if c["meta"]["period"] == period])["meta"]
def growth_pct(row):                                     # arithmetic done in CODE, not by the language model
    a, b = lookup(row, "FY2024")["value"], lookup(row, "FY2025")["value"]; return round((b - a) / a * 100, 1)

golden = [("Net profit in FY2025 (Rs crore)?", 190.0, lambda: lookup("Net profit", "FY2025")["value"]),
          ("Revenue growth FY2024 to FY2025 (%)?", 15.0, lambda: growth_pct("Revenue from operations")),
          ("Operating expenses FY2024 (Rs crore)?", 900.0, lambda: lookup("Operating expenses", "FY2024")["value"]),
          ("Net profit margin FY2025 (%)?", 13.8, lambda: round(lookup("Net profit", "FY2025")["value"] / lookup("Revenue from operations", "FY2025")["value"] * 100, 1))]
def exact(pred, gold, tol=0.0): return abs(pred - gold) <= tol
ok = 0
for q, gold, fn in golden:
    pred = fn(); hit = exact(pred, gold); ok += hit; print(f"{q:42s} gold={gold:7.1f} pred={pred:7.1f} {'OK' if hit else 'MISS'}")
print(f"numeric exact match: {ok}/{len(golden)}")
print("unit trap: the same revenue in Rs million is", table['rows'][0][1][1] * 10, "(1 crore = 10 million): a wrong unit looks like a wrong answer")
