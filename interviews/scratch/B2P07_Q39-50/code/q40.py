# Standalone, stdlib only (sqlite3). TOY router + TOY text store; the "text-to-SQL" step is a hand-written template, not an LLM.
import re, sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, region TEXT);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, status TEXT, month TEXT);
INSERT INTO customers VALUES (1,'Asha','south'),(2,'Ravi','north'),(3,'Meera','south');
INSERT INTO orders VALUES (1,1,120,'delivered','2026-08'),(2,1,80,'refunded','2026-09'),
                          (3,2,200,'delivered','2026-09'),(4,3,50,'delivered','2026-09'),(5,3,70,'delivered','2026-09');
""")
db.commit()
SCHEMA = {"customers": ["id", "name", "region"], "orders": ["id", "customer_id", "amount", "status", "month"]}   # schema grounding
TEXTS = {"refund_policy": "Refunds are allowed within 30 days of delivery. Shipping fees are not refunded.",
         "returns_faq": "To return an item, open the app and choose Return. Pickup happens in 2 days."}

FORBIDDEN = re.compile(r"\b(insert|update|delete|drop|alter|create|attach|pragma|replace|vacuum)\b", re.I)
def guard(sql):
    s = sql.strip().rstrip(";")
    if ";" in s: return False, "multiple statements"
    if not re.match(r"(?is)^select\b", s): return False, "only SELECT is allowed"
    if FORBIDDEN.search(s): return False, "forbidden keyword"
    tables = set(re.findall(r"(?i)\b(?:from|join)\s+([a-z_]+)", s))
    if not tables <= set(SCHEMA): return False, f"table not in allowlist: {sorted(tables - set(SCHEMA))}"
    return True, s

def run_sql(sql):
    ok, s = guard(sql)
    if not ok: return {"error": s}
    conn = db
    conn.execute("PRAGMA query_only = ON")                           # second layer: the connection itself refuses writes
    try:
        cur = conn.execute(s + " LIMIT 50"); return {"cols": [d[0] for d in cur.description], "rows": cur.fetchall()}
    finally: conn.execute("PRAGMA query_only = OFF")

def route(q):                                                        # toy router: numbers/aggregates -> SQL, policy wording -> text
    ql = q.lower()
    sql_cues = re.search(r"\b(how many|total|sum|average|count|revenue|top)\b", ql)
    text_cues = re.search(r"\b(policy|allowed|can i|how do i|why)\b", ql)
    if sql_cues and text_cues: return "both"
    return "sql" if sql_cues else "text"

def text_search(q):
    w = set(re.findall(r"[a-z]+", q.lower()))
    return max(TEXTS.items(), key=lambda kv: len(w & set(re.findall(r"[a-z]+", kv[1].lower()))))

TEMPLATES = {"total revenue by region": "SELECT c.region, SUM(o.amount) AS total FROM orders o JOIN customers c ON c.id = o.customer_id "
                                       "WHERE o.status = 'delivered' GROUP BY c.region ORDER BY c.region"}
def answer(q):
    r = route(q); out = {"route": r}
    if r in ("sql", "both"): out["sql"] = run_sql(TEMPLATES.get("total revenue by region" if "revenue" in q.lower() else "", "SELECT 1 WHERE 0"))
    if r in ("text", "both"): out["text"] = text_search(q)
    return out

for q in ["total revenue by region", "what is the refund policy for shipping fees", "total refunds allowed by policy revenue"]:
    print(q, "->", answer(q))

print("--- guard tests ---")
for bad in ["DELETE FROM orders", "SELECT * FROM orders; DROP TABLE orders", "SELECT * FROM secrets",
            "UPDATE orders SET amount = 0", "SELECT * FROM orders WHERE id = 1 OR 1=1; --"]:
    print(repr(bad), "->", run_sql(bad))
assert db.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 5      # nothing was changed
db.execute("PRAGMA query_only = ON")
try: db.execute("DELETE FROM orders")
except sqlite3.OperationalError as e: print("engine-level read-only also refuses a write:", e)
db.execute("PRAGMA query_only = OFF")
# wrong-join symptom: joining orders to customers on the wrong key silently returns plausible but wrong totals
wrong = db.execute("SELECT SUM(o.amount) FROM orders o JOIN customers c ON c.id = o.id").fetchone()[0]
right = db.execute("SELECT SUM(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id").fetchone()[0]
print("wrong join total:", wrong, "| right join total:", right)
