# TOY handoff-template validator: required fields for a delegation, checked on a good and a vague handoff.
import re
REQUIRED = ["objective", "output_format", "tools", "boundaries"]
VAGUE = re.compile(r"\b(research|look into|find out about|investigate)\b", re.I)
def validate(h):
    errs = [f"missing {f}" for f in REQUIRED if not str(h.get(f, "")).strip()]
    obj = str(h.get("objective", ""))
    if obj and len(obj.split()) < 8: errs.append("objective too short to be specific (<8 words)")
    if obj and VAGUE.search(obj) and not re.search(r"\d", obj): errs.append("objective is vague: no scope, count or date range")
    if h.get("boundaries") and not re.search(r"\b(not|only|exclude|stop|at most|do not)\b", h["boundaries"], re.I):
        errs.append("boundaries state no limit or exclusion")
    return errs

good = {"objective": "List the 2023 and 2024 annual revenue of each of the three largest listed Indian IT services firms",
        "output_format": "JSON list of {company, year, revenue_inr_crore, source_url}",
        "tools": "web_search for filings; use the pdf reader only on investor-relations pages",
        "boundaries": "Only these three firms; do not cover subsidiaries; stop after 10 searches; the sibling agent handles headcount"}
vague = {"objective": "research IT companies", "output_format": "", "tools": "", "boundaries": ""}
partial = dict(good, boundaries="be careful")
for name, h in (("good", good), ("vague", vague), ("partial", partial)):
    e = validate(h); print(f"{name:8}", "OK" if not e else e)
assert validate(good) == [] and len(validate(vague)) >= 4 and validate(partial) == ["boundaries state no limit or exclusion"]
# duplicate-work check: two sub-agents whose objectives overlap heavily could be flagged before launch (word overlap is a crude proxy)
def overlap(a, b):
    wa, wb = set(re.findall(r"\w+", a.lower())), set(re.findall(r"\w+", b.lower())); return len(wa & wb) / len(wa | wb)
print("word overlap of two vague objectives =", round(overlap("research IT companies", "research IT firms"), 2), "(crude proxy; flag high overlap for review)")
assert overlap("research IT companies", "research IT firms") > 0.4
print("tests passed")
