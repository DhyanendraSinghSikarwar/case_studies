# TOY gateway: one call() entry point with key lookup, tenant-scoped cache, budget, retry and fallback. Providers are mocks.
import hashlib, json
class Provider:
    def __init__(self, name, fail_first=0, text="ok"):
        self.name, self.fail, self.text, self.calls = name, fail_first, text, 0
    def complete(self, model, prompt):
        self.calls += 1
        if self.calls <= self.fail: raise TimeoutError(self.name + " timeout")
        return {"text": f"{self.text}:{prompt[:12]}", "in": len(prompt.split()), "out": 5}
class Gateway:
    def __init__(self, routes, budgets, max_retries=1):
        self.routes, self.budgets, self.cache, self.log, self.max_retries = routes, budgets, {}, [], max_retries
    def key(self, tenant, model, prompt):  # tenant AND model are in the key (Part 11 Q38 bug class)
        return hashlib.sha256(json.dumps([tenant, model, prompt]).encode()).hexdigest()
    def call(self, tenant, model, prompt):
        if self.budgets.get(tenant, 0) <= 0: self.log.append((tenant, "BUDGET_BLOCK")); return None
        k = self.key(tenant, model, prompt)
        if k in self.cache: self.log.append((tenant, "CACHE_HIT")); return self.cache[k]
        for prov in self.routes[model]:                     # ordered: primary then fallback
            for attempt in range(self.max_retries + 1):
                try:
                    r = prov.complete(model, prompt)
                    self.budgets[tenant] -= r["in"] + r["out"]
                    self.cache[k] = r; self.log.append((tenant, f"OK via {prov.name} attempt {attempt}")); return r
                except TimeoutError as e:
                    self.log.append((tenant, f"FAIL {e}"))
        self.log.append((tenant, "ALL_FAILED")); return None
a, b = Provider("A", fail_first=2), Provider("B", text="fallback")
gw = Gateway({"m": [a, b]}, {"t1": 100, "t2": 6})
gw.call("t1", "m", "hello world question one")   # A fails twice (try+retry), falls to B
gw.call("t1", "m", "hello world question one")   # cache hit for t1
gw.call("t2", "m", "hello world question one")   # different tenant: NOT served t1's cached answer
gw.call("t2", "m", "another prompt entirely")    # t2 budget exhausted -> blocked
for row in gw.log: print(row)
print("provider calls: A =", a.calls, "B =", b.calls, "| cache entries:", len(gw.cache))
