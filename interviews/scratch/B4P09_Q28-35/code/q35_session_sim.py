"""Q35: validate the feature-view spec, then simulate session features with sliding expiry (pure Python; Redis-like TTL emulated)."""
import sys, re, yaml

spec = yaml.safe_load(open(sys.argv[1]))
FRESH = {"batch_daily", "near_real_time_5m", "streaming", "per_request"}
errs = []
for fv in spec["feature_views"]:
    if fv["freshness"] not in FRESH: errs.append(f"{fv['name']}: bad freshness")
    if fv["store"] and not re.fullmatch(r"\d+[mhd]", fv.get("ttl", "")): errs.append(f"{fv['name']}: stored view needs ttl like 30m")
    if not fv["store"] and "ttl" in fv: errs.append(f"{fv['name']}: per-request view has no ttl")
    if "cold_start" not in fv and fv["entity"] != "request_id" and fv["freshness"] != "streaming":
        errs.append(f"{fv['name']}: no cold start rule")
print("spec errors:", errs or "none", "| views:", [v["name"] for v in spec["feature_views"]])

UNIT = {"m": 60, "h": 3600, "d": 86400}
n, u = re.fullmatch(r"(\d+)([mhd])", next(v["ttl"] for v in spec["feature_views"] if v["name"] == "session_stream")).groups()
TTL = int(n) * UNIT[u]
print("session ttl seconds:", TTL)

class SessionStore:
    """Online store emulation: value + last_write time; read after TTL returns None (like an expired key). Sliding expiry."""
    def __init__(self): self.d = {}
    def update(self, sid, now, item, clicked):
        cur = self.get(sid, now) or {"last_5_items": [], "clicks_in_session": 0, "session_start_ts": now}
        cur["last_5_items"] = (cur["last_5_items"] + [item])[-5:]
        cur["clicks_in_session"] += int(clicked)
        self.d[sid] = (now, cur)                       # refresh expiry on every write
    def get(self, sid, now):
        if sid not in self.d: return None
        t, v = self.d[sid]
        return v if now - t < TTL else None

POP_DEFAULT = {"last_5_items": [], "clicks_in_session": 0, "session_start_ts": None}   # cold-start fallback

# (time_s, session, item, clicked)
log = [(0, "s1", "i1", 0), (60, "s1", "i2", 1), (200, "s1", "i3", 1),
       (400, "s2", "i9", 0),
       (200 + 1799, "s1", "i4", 0),                    # 1799 s after last s1 write: still alive
       (200 + 1799 + 1800, "s1", "i5", 1)]             # exactly 1800 s after the previous write: expired -> new session
st = SessionStore()
training_rows = []
print("\n  time sess item  served_features(before this impression)")
for now, sid, item, clicked in sorted(log):
    served = st.get(sid, now) or POP_DEFAULT
    print(f"{now:6d} {sid:4s} {item:4s}  {served}")
    training_rows.append({"ts": now, "session": sid, "item": item, "label": clicked, "feat_clicks": served["clicks_in_session"]})
    st.update(sid, now, item, clicked)                  # the event updates state AFTER the feature was served

print("\nlogged training rows (features are the ones served, so no leakage from the click itself):")
for r in training_rows: print(" ", r)
