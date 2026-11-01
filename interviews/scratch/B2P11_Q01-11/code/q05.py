# TOY prompt registry: immutable versions, movable labels, audit log, client cache with TTL, trace stamped with name@version.
import hashlib
class Registry:
    def __init__(self): self.versions, self.labels, self.audit = {}, {}, []
    def publish(self, name, text, author):
        v = len([k for k in self.versions if k[0] == name]) + 1
        self.versions[(name, v)] = {"text": text, "sha": hashlib.sha256(text.encode()).hexdigest()[:8]}   # versions never change
        self.audit.append(f"{author} published {name}@v{v} sha={self.versions[(name, v)]['sha']}"); return v
    def move_label(self, name, label, v, author, protected_ok):
        if label == "production" and not protected_ok:
            self.audit.append(f"{author} DENIED move {name}:{label}->v{v}"); return False
        old = self.labels.get((name, label)); self.labels[(name, label)] = v
        self.audit.append(f"{author} moved {name}:{label} v{old}->v{v}"); return True
    def get(self, name, label):
        v = self.labels[(name, label)]; return v, self.versions[(name, v)]["text"]
class Client:                                  # caches the label resolution for ttl seconds
    def __init__(self, reg, ttl): self.reg, self.ttl, self.cache = reg, ttl, {}
    def prompt(self, name, label, now):
        hit = self.cache.get((name, label))
        if hit and now - hit[0] < self.ttl: return hit[1], hit[2], "cache"
        v, text = self.reg.get(name, label); self.cache[(name, label)] = (now, v, text); return v, text, "fetch"
reg = Registry()
reg.publish("qa", "Answer briefly.", "asha"); reg.publish("qa", "Answer briefly and cite sources.", "asha"); reg.publish("qa", "Answer in 3 bullets.", "ravi")
reg.move_label("qa", "production", 1, "release-bot", True)
reg.move_label("qa", "production", 3, "ravi", False)     # not allowed: only the release path may move the production label
reg.move_label("qa", "production", 2, "release-bot", True)
c = Client(reg, ttl=60)
traces = []
def serve(now):
    v, _, src = c.prompt("qa", "production", now); traces.append((now, f"qa@v{v}", src))
serve(0); serve(30)
reg.move_label("qa", "production", 1, "release-bot", True)   # ROLLBACK at t=40: no code deploy, just a label move
for t in (45, 59, 61, 90): serve(t)
print("t(s)  prompt stamped on trace  served from")
for t, p, s in traces: print(f"{t:4d}  {p:6}                   {s}")
print("audit log:"); [print("  " + a) for a in reg.audit]
