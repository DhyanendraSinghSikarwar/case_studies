# Q25 batch enrichment: (1) cost arithmetic with ASSUMED inputs, (2) tiny sqlite checkpointed run with poison rows, budget stop,
# prompt-version re-run and a sampled audit. The LLM is a mock; every price/size below is an assumption, not a quote.
import sqlite3, random, json, math, hashlib
ROWS = 20_000_000
A = dict(in_tok=350, out_tok=60, price_in_per_m=0.20, price_out_per_m=0.80, batch_discount=0.5)  # ASSUMED small-model prices (USD / 1M tokens)
def cost(rows, in_tok, out_tok, pin, pout, disc=1.0): return rows * (in_tok * pin + out_tok * pout) / 1e6 * disc
print("ASSUMED: 20M rows, %d in / %d out tokens, $%.2f / $%.2f per 1M tokens" % (A["in_tok"], A["out_tok"], A["price_in_per_m"], A["price_out_per_m"]))
base = cost(ROWS, A["in_tok"], A["out_tok"], A["price_in_per_m"], A["price_out_per_m"])
print(f"one pass, online pricing:  ${base:,.0f}")
print(f"one pass, batch discount {A['batch_discount']}: ${base * A['batch_discount']:,.0f}  (discount is an assumption)")
print(f"a prompt change forces a re-run of affected fields: 3 re-runs = ${3 * base * A['batch_discount']:,.0f}")
print(f"input tokens in total: {ROWS * A['in_tok'] / 1e9:.1f}B")
# --- tiny run
random.seed(5)
db = sqlite3.connect(":memory:")
db.execute("create table src(id integer primary key, text text)")
db.execute("create table out(id integer, field text, prompt_ver text, value text, primary key(id, field, prompt_ver))")
db.execute("create table dead(id integer, reason text)")
db.executemany("insert into src values(?,?)", [(i, "row %d %s" % (i, "BADJSON" if i % 97 == 0 else "ok")) for i in range(1, 1001)])
def mock_llm(text, ver):
    if "BADJSON" in text: return "{oops"
    cat = "home" if int(text.split()[1]) % 3 else "toys"
    if random.random() < 0.08: cat = "toys" if cat == "home" else "home"   # silent wrong answer, valid schema (ASSUMED 8%)
    if random.random() < 0.04: cat = "unknown_cat"                      # off-schema value (ASSUMED 4%)
    return json.dumps({"category": cat})
ALLOWED = {"home", "toys"}
def run(ver, budget_calls, state):
    done = {r[0] for r in db.execute("select id from out where field='cat' and prompt_ver=?", (ver,))}
    dead = {r[0] for r in db.execute("select id from dead")}
    for rid, text in db.execute("select id, text from src order by id").fetchall():
        if rid in done or rid in dead: continue                           # idempotent resume
        if state["calls"] >= budget_calls: state["stopped"] = True; return
        state["calls"] += 1
        try:
            v = json.loads(mock_llm(text, ver))["category"]
            assert v in ALLOWED
            db.execute("insert or ignore into out values(?,?,?,?)", (rid, "cat", ver, v))
        except Exception as e: db.execute("insert into dead values(?,?)", (rid, type(e).__name__))
    state["stopped"] = False
s = dict(calls=0); run("v1", 600, s); n1 = db.execute("select count(*) from out where prompt_ver='v1'").fetchone()[0]
print("run 1 stopped by budget:", s["stopped"], "| saved", n1, "| dead", db.execute("select count(*) from dead").fetchone()[0])
s2 = dict(calls=0); run("v1", 10**9, s2); n2 = db.execute("select count(*) from out where prompt_ver='v1'").fetchone()[0]
print("resume: new calls", s2["calls"], "(none repeated for saved rows) | saved", n2, "| dead", db.execute("select count(*) from dead").fetchone()[0])
dup = db.execute("select count(*) from (select id from out where prompt_ver='v1' group by id having count(*)>1)").fetchone()[0]
assert dup == 0
# prompt v2 re-run: only rows missing v2 are called (here all, since v2 is new); v1 rows kept for diffing
s3 = dict(calls=0); run("v2", 10**9, s3); print("prompt v2 run: calls", s3["calls"], "(rows already in the dead table are skipped, so a poison row is not retried forever)")
# sampled audit with Wilson interval; 'truth' for the toy = rule used by the mock
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - m) / d, (c + m) / d
sample = random.sample(db.execute("select id, value from out where prompt_ver='v2'").fetchall(), 100)
good = sum(1 for i, v in sample if v == ("home" if i % 3 else "toys"))
lo, hi = wilson(good, 100); print(f"audit of 100 sampled rows: {good} correct, 95% Wilson interval {lo:.2f}-{hi:.2f}")
