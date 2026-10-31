import hashlib, hmac, json, re

SALT = b"demo-only-secret-load-from-a-secret-manager"       # never hard-code in real code
ALLOW = {"customer_id", "model_version", "score", "decision", "amount_band", "city_tier", "note", "ts"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")   # Indian mobile style, rough

def pseudo(value):
    return hmac.new(SALT, str(value).encode(), hashlib.sha256).hexdigest()[:16]

def redact(text):
    return PHONE.sub("[PHONE]", EMAIL.sub("[EMAIL]", text))

def safe_record(rec):
    out = {}
    for k, v in rec.items():
        if k not in ALLOW:
            continue                                    # allow-list: unknown fields are dropped, not logged
        if k == "customer_id":
            out["customer_pseudo_id"] = pseudo(v)
        elif isinstance(v, str):
            out[k] = redact(v)
        else:
            out[k] = v
    return out

records = [
    {"customer_id": "C1001", "model_version": "v7", "score": 0.82, "decision": "review", "amount_band": "50-100k",
     "city_tier": 2, "ts": "2026-10-26T10:00:00Z", "email": "asha@example.com", "pan": "ABCDE1234F",
     "note": "caller asha.k@example.com asked on 98765 43210"},
    {"customer_id": "C1001", "model_version": "v7", "score": 0.31, "decision": "approve", "amount_band": "10-50k",
     "city_tier": 2, "ts": "2026-10-26T10:05:00Z", "full_name": "Asha K", "note": "alt +91-9123456789"},
    {"customer_id": "C2002", "model_version": "v7", "score": 0.55, "decision": "review", "amount_band": "10-50k",
     "city_tier": 3, "ts": "2026-10-26T10:07:00Z", "note": "no pii here"},
]
for r in records:
    print(json.dumps(safe_record(r), sort_keys=True))
same = safe_record(records[0])["customer_pseudo_id"] == safe_record(records[1])["customer_pseudo_id"]
print("same customer -> same pseudo id (joins still work):", same)
# the limit: a small id space can be brute-forced by anyone who has the salt
ids = [f"C{n}" for n in range(1000, 1100)]
target = safe_record(records[0])["customer_pseudo_id"]
print("brute force with salt recovers id:", [i for i in ids if pseudo(i) == target])
