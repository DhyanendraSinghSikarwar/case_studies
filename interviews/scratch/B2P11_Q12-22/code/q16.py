# TOY budget governor with soft/hard limits, reservation, showback and a denial-of-wallet simulation. Money is in synthetic cents.
class Governor:
    def __init__(self, monthly_cents, soft=0.8, per_request_cap=50):
        self.limit, self.soft, self.cap, self.spent, self.alerts, self.showback = monthly_cents, soft, per_request_cap, 0, [], {}
    def request(self, est_cents, feature):
        est = min(est_cents, self.cap)                       # cap what one request may reserve (max_tokens)
        if self.spent + est > self.limit: return "HARD_BLOCK"
        self.spent += est
        self.showback[feature] = self.showback.get(feature, 0) + est
        if self.spent >= self.soft * self.limit and not self.alerts: self.alerts.append(f"soft alert at spent={self.spent}")
        return "ok"
# normal tenant vs a tenant hit by a scripted flood (synthetic traffic)
normal, flooded = Governor(1000), Governor(1000)
for i in range(200): normal.request(3, "chat")
res = {"ok": 0, "HARD_BLOCK": 0}
for i in range(2000): res[flooded.request(40, "chat")] += 1
print("normal :", normal.spent, "cents spent, alerts:", normal.alerts)
print("flooded:", flooded.spent, "cents spent, outcomes:", res, "alerts:", flooded.alerts)
uncapped_cost = 2000 * 40
print("without a hard cap the flood would cost", uncapped_cost, "cents vs", flooded.spent, "with it (limit 1000)")
# one tenant's cap does not touch another
print("other tenant unaffected:", normal.request(3, "chat"))
# estimate-then-reconcile: reserve max, refund the unused part
class Reserving(Governor):
    def finish(self, reserved, actual): self.spent -= max(0, reserved - actual)
g = Reserving(100); g.request(30, "agent"); g.finish(30, 12)
print("after reconcile spent =", g.spent, "(reserved 30, actual 12)")
# showback table
print("showback:", flooded.showback, normal.showback)
