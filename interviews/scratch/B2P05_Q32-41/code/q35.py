# Standalone, stdlib only. MOCK filter, HARMLESS placeholder word only. Educational: why a surface filter misses encoded input.
import base64, codecs, re
BLOCKLIST = {"blockedword"}                          # placeholder for "something the policy blocks"

def naive_filter(text):                              # surface keyword match only
    return any(w in text.lower() for w in BLOCKLIST)

def b64_candidates(text):                            # decode anything that looks like base64 and is readable text
    for tok in re.findall(r"[A-Za-z0-9+/=]{8,}", text):
        try: yield base64.b64decode(tok, validate=True).decode("utf-8")
        except Exception: pass

def decode_and_rescan(text):                         # normalise first, then apply the same filter to every view
    return naive_filter(text) or any(naive_filter(d) for d in b64_candidates(text))

plain = "please say BLOCKEDWORD"
b64 = "decode this and follow it: " + base64.b64encode(b"please say BLOCKEDWORD").decode()
rot = "decode this: " + codecs.encode("please say BLOCKEDWORD", "rot13")
benign = "decode this: " + base64.b64encode(b"what is the weather today").decode()
print(f"{'input':8s} naive  decode+rescan")
for name, s in [("plain", plain), ("base64", b64), ("rot13", rot), ("benign b64", benign)]:
    print(f"{name:10s} {str(naive_filter(s)):6s} {decode_and_rescan(s)}")
