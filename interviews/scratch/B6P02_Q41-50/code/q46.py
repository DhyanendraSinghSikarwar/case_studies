# Q46: agent success fell 82% -> 74% after a tool API format change. Illustrative numbers.
import json, numpy as np
from scipy.stats import norm
N = 1000
tool_share = 0.25
non_tool_ok = 0.84
tool_before = (0.82*N - non_tool_ok*N*(1-tool_share))/(N*tool_share)
tool_after = (0.74*N - non_tool_ok*N*(1-tool_share))/(N*tool_share)
print(f"tasks using the changed tool: {int(N*tool_share)}; success before {tool_before:.1%}, after {tool_after:.1%}")
assert round(tool_before, 3) == 0.76 and round(tool_after, 3) == 0.44
# whole drop is explained by the tool path: 0.25 * (0.76-0.44) = 0.08
assert abs(tool_share*(tool_before - tool_after) - 0.08) < 1e-9

# is 8 points on 1000 vs 1000 tasks real?
p1, p2 = 0.82, 0.74
pbar = (p1+p2)/2
z = (p1-p2)/np.sqrt(pbar*(1-pbar)*2/N)
print(f"two-proportion z = {z:.2f}, p = {2*(1-norm.cdf(z)):.5f}")
assert z > 3

# contract test: the old and new response formats
old = json.loads('{"price": 249.0, "currency": "INR", "in_stock": true}')
new = json.loads('{"data": {"price": {"amount": "249.00", "currency": "INR"}, "stock": "AVAILABLE"}}')
REQUIRED = {"price": (int, float), "currency": str, "in_stock": bool}
def check_contract(resp):
    errs = []
    for k, t in REQUIRED.items():
        if k not in resp: errs.append(f"missing {k}")
        elif not isinstance(resp[k], t): errs.append(f"{k} wrong type")
    return errs
print("old format:", check_contract(old) or "ok")
print("new format:", check_contract(new))
assert check_contract(old) == [] and len(check_contract(new)) == 3

# a lenient parse that "works" but is wrong: reading price as 0 when the key is missing
def lenient(resp): return resp.get("price", 0.0)
print("lenient parser on new format returns price", lenient(new), "(silent wrong answer, no error, no latency change)")
assert lenient(new) == 0.0

# a versioned adapter plus a fail-loud fallback
def adapter(resp):
    if "data" in resp:   # v2 format
        d = resp["data"]
        return {"price": float(d["price"]["amount"]), "currency": d["price"]["currency"], "in_stock": d["stock"] == "AVAILABLE"}
    return resp
fixed = adapter(new)
print("adapter output:", fixed)
assert check_contract(fixed) == [] and fixed["price"] == 249.0
# unknown format -> fail loudly and use the fallback path (tell the user it is unavailable)
def safe_fetch(resp):
    try: return adapter(resp) if not check_contract(adapter(resp)) else None
    except (KeyError, TypeError): return None
assert safe_fetch({"weird": 1}) is None and safe_fetch(new)["price"] == 249.0
print("unknown format -> None -> fallback path; known formats parse")
