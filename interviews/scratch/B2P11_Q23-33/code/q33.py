# Prompt registry: immutable versions, movable labels, promote/rollback, cached client, fallback prompt.
import hashlib, time
class Registry:
    def __init__(self): self.versions, self.labels, self.history = {}, {}, []      # name -> [texts]; (name,label)->version
    def create(self, name, text):
        vs = self.versions.setdefault(name, []); vs.append((text, hashlib.sha256(text.encode()).hexdigest())); return len(vs)   # append-only, numbered from 1
    def get_version(self, name, v):
        text, h = self.versions[name][v - 1]
        if hashlib.sha256(text.encode()).hexdigest() != h: raise ValueError("version content does not match its recorded hash")
        return text
    def set_label(self, name, label, v, who="system"):
        if not 1 <= v <= len(self.versions[name]): raise KeyError("no such version")
        self.history.append((name, label, self.labels.get((name, label)), v, who)); self.labels[(name, label)] = v
    def promote(self, name, src="staging", dst="production", who="system"): self.set_label(name, dst, self.labels[(name, src)], who)
    def rollback(self, name, label="production"):
        for n, l, prev, new, _ in reversed(self.history):
            if n == name and l == label and prev is not None and self.labels[(name, label)] == new:
                self.set_label(name, label, prev, "rollback"); return prev
        raise RuntimeError("nothing to roll back to")
    def fetch(self, name, label):
        v = self.labels[(name, label)]; return v, self.get_version(name, v)
class Client:
    def __init__(self, reg, ttl, clock, fallback): self.reg, self.ttl, self.clock, self.fallback, self.cache, self.up = reg, ttl, clock, fallback, {}, True
    def get(self, name, label):
        now = self.clock(); hit = self.cache.get((name, label))
        if hit and now - hit[0] < self.ttl: return hit[1], hit[2], "cache"
        try:
            if not self.up: raise ConnectionError("registry down")
            v, t = self.reg.fetch(name, label); self.cache[(name, label)] = (now, v, t); return v, t, "registry"
        except Exception:
            if hit: return hit[1], hit[2], "stale-cache"          # prefer last known good over the static fallback
            return 0, self.fallback, "fallback"
# ---- tests
r = Registry(); t = [0.0]; c = Client(r, ttl=60, clock=lambda: t[0], fallback="You are a helpful assistant.")
A = "Answer briefly using the context."; B = "Answer in detail and cite sources."; C2 = "Answer in French."
v1, v2 = r.create("qa", A), r.create("qa", B)
r.set_label("qa", "production", v1, "alice"); r.set_label("qa", "staging", v2, "alice")
assert r.fetch("qa", "production") == (1, A)
r.promote("qa", who="bob"); assert r.fetch("qa", "production") == (2, B)
assert r.rollback("qa") == 1 and r.fetch("qa", "production")[1] == A, "rollback must restore the exact previous text"
assert hashlib.sha256(r.fetch("qa", "production")[1].encode()).hexdigest() == hashlib.sha256(A.encode()).hexdigest()
orig = r.versions["qa"][0]; r.versions["qa"][0] = ("tampered in place", orig[1])    # simulate someone editing storage directly
try: r.get_version("qa", 1)
except ValueError as e: print("tamper detected on read:", e)
r.versions["qa"][0] = orig
v3 = r.create("qa", C2); r.set_label("qa", "production", v3); r.set_label("qa", "production", 2)
assert r.rollback("qa") == v3, "rollback goes to the previous label target, not to version-1"
print("rollback after two label moves goes back one step to version", r.fetch("qa", "production")[0])
try: r.set_label("qa", "production", 99)
except KeyError as e: print("label to missing version rejected:", e)
print("client reads:", c.get("qa", "production")[2], end=" | "); t[0] = 30; r.set_label("qa", "production", 1)
print("30s later (ttl 60, label moved):", c.get("qa", "production")[2], "-> still serves version", c.get("qa", "production")[0])
t[0] = 61; print("after ttl:", c.get("qa", "production")[2], "-> version", c.get("qa", "production")[0])
c.up = False; t[0] = 200; print("registry down, cache expired:", c.get("qa", "production")[2])
c2 = Client(r, 60, lambda: t[0], "You are a helpful assistant."); c2.up = False
print("cold client with registry down:", c2.get("qa", "production")[2], "->", c2.get("qa", "production")[1])
print("history rows:", len(r.history), "| all tests passed")
