import re, hashlib, json
raw = [
 {"prompt": "Summarise: refunds take 5 days.", "response": "Refunds take 5 days."},
 {"prompt": "summarise:  Refunds take 5 days. ", "response": "Refunds take 5 days."},   # near-dup (case/space)
 {"prompt": "Translate 'hello' to Hindi.", "response": "Namaste."},
 {"prompt": "Translate 'hello' to Hindi.", "response": ""},                              # empty response
 {"prompt": "Hi", "response": "As an AI language model, I cannot help."},                # boilerplate refusal
 {"prompt": "Write a haiku about rain.", "response": "x" * 5000},                        # too long
 {"prompt": "Extract the city as JSON: 'I live in Pune'.", "response": '{"city": "Pune"}'},
 {"prompt": "Extract the city as JSON: 'I live in Delhi'.", "response": "city is Delhi"},   # wrong format
 {"prompt": "Explain overfitting in one line.", "response": "The model memorises training noise and fails on new data."},
]
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
seen, kept, drop = set(), [], []
def why(ex):
    r = ex["response"]
    if not r.strip(): return "empty response"
    if len(r) > 2000: return "too long"
    if r.lower().startswith("as an ai language model"): return "boilerplate"
    if "JSON" in ex["prompt"]:
        try: json.loads(r)
        except ValueError: return "format check failed"
    return None
for ex in raw:
    key = hashlib.md5((norm(ex["prompt"]) + "|" + norm(ex["response"])).encode()).hexdigest()
    reason = "exact dup after normalising" if key in seen else why(ex)
    seen.add(key)
    (drop if reason else kept).append((ex, reason))
print("kept", len(kept), "of", len(raw))
for ex, r in drop: print("  dropped:", r, "|", ex["prompt"][:35])
