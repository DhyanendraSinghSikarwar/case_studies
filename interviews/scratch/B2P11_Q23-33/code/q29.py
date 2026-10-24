# TOY: secret handling. FAKE keys only. HMAC-signed short-lived scoped tokens, rotation overlap, log scrubbing.
import hmac, hashlib, json, base64, re, time
KEYS = {"k1": b"signing-key-one-FAKE"}            # key id -> signing key; the agent never sees these
def b64(b): return base64.urlsafe_b64encode(b).decode().rstrip("=")
def unb64(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
def mint(kid, tenant, scopes, ttl, now):
    body = b64(json.dumps({"kid": kid, "tenant": tenant, "scopes": scopes, "exp": now + ttl}, sort_keys=True).encode())
    return body + "." + b64(hmac.new(KEYS[kid], body.encode(), hashlib.sha256).digest())
def check(token, need_scope, tenant, now, accepted_kids):
    try: body, sig = token.split("."); claims = json.loads(unb64(body))
    except Exception: return "deny:malformed"
    if claims["kid"] not in accepted_kids or claims["kid"] not in KEYS: return "deny:key-retired"
    if not hmac.compare_digest(sig, b64(hmac.new(KEYS[claims["kid"]], body.encode(), hashlib.sha256).digest())): return "deny:bad-signature"
    if now > claims["exp"]: return "deny:expired"
    if claims["tenant"] != tenant: return "deny:wrong-tenant"
    if need_scope not in claims["scopes"]: return "deny:scope"
    return "allow"
t0 = 1000
tok = mint("k1", "acme", ["orders:read"], 300, t0)
print("fresh, right scope:", check(tok, "orders:read", "acme", t0 + 10, {"k1"}))
print("write scope asked :", check(tok, "orders:write", "acme", t0 + 10, {"k1"}))
print("other tenant      :", check(tok, "orders:read", "globex", t0 + 10, {"k1"}))
print("after expiry      :", check(tok, "orders:read", "acme", t0 + 301, {"k1"}))
forged = tok[:-3] + ("AAA" if tok[-3:] != "AAA" else "BBB"); print("tampered signature:", check(forged, "orders:read", "acme", t0 + 10, {"k1"}))
# rotation: add k2, mint with k2, accept {k1,k2} during overlap, then retire k1
KEYS["k2"] = b"signing-key-two-FAKE"
tok2 = mint("k2", "acme", ["orders:read"], 300, t0 + 20)
print("overlap window: old token", check(tok, "orders:read", "acme", t0 + 30, {"k1", "k2"}), "| new token", check(tok2, "orders:read", "acme", t0 + 30, {"k1", "k2"}))
print("after retiring k1: old token", check(tok, "orders:read", "acme", t0 + 40, {"k2"}), "| new token", check(tok2, "orders:read", "acme", t0 + 40, {"k2"}))
# scrubber for prompts, logs and tool outputs (illustrative patterns for FAKE formats; real formats vary by provider)
PAT = [re.compile(r"\bsk-[A-Za-z0-9]{12,}\b"), re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._-]{16,}"), re.compile(r"(?i)(api[_-]?key|secret|password)\s*[:=]\s*\S+")]
def scrub(s):
    n = 0
    for p in PAT: s, c = p.subn("[REDACTED]", s); n += c
    return s, n
samples = ["calling provider with key sk-FAKE1234567890abcd ok", "Authorization: Bearer abcdef0123456789.xyz-FAKE", "config api_key=FAKEVALUE123 loaded",
           "normal log line: order 17 shipped", "token split across words: sk-FAKE 1234567890abcd"]
for s in samples: out, n = scrub(s); print(f"{n} redactions -> {out}")
