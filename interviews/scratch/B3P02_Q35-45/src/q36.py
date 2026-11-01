# Q36: attach the latest quote at or before each trade: SQL correlated MAX vs pandas merge_asof
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE trades(trade_id INTEGER PRIMARY KEY, ticker TEXT, trade_time TEXT, qty INTEGER);
CREATE TABLE quotes(ticker TEXT, quote_time TEXT, bid REAL);
INSERT INTO trades VALUES
 (1,'A','2026-01-05 09:00:05',100),
 (2,'A','2026-01-05 09:00:10', 50),
 (3,'B','2026-01-05 09:00:07', 20),
 (4,'A','2026-01-05 09:00:01', 10),
 (5,'B','2026-01-05 09:01:30', 30);
INSERT INTO quotes VALUES
 ('A','2026-01-05 09:00:02',10.0),
 ('A','2026-01-05 09:00:10',10.5),
 ('A','2026-01-05 09:00:12',11.0),
 ('B','2026-01-05 09:00:03',20.0),
 ('B','2026-01-05 09:00:08',21.0);
"""
SQL_MAIN = """
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
"""
# tolerance of 30 seconds: the quote must also be no older than 30 s
SQL_TOL = """
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time >= datetime(t.trade_time, '-30 seconds')
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
"""
# strictly earlier (allow_exact_matches=False)
SQL_STRICT = SQL_MAIN.replace("<= t.trade_time", "< t.trade_time")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
trades = pd.read_sql_query("SELECT * FROM trades", con, parse_dates=["trade_time"])
quotes = pd.read_sql_query("SELECT * FROM quotes", con, parse_dates=["quote_time"])

def sql_df(q):
    d = pd.read_sql_query(q, con, parse_dates=["trade_time", "quote_time"])
    return d.sort_values("trade_id").reset_index(drop=True)

def asof(**kw):
    out = pd.merge_asof(trades.sort_values("trade_time"), quotes.sort_values("quote_time"),
                        left_on="trade_time", right_on="quote_time", by="ticker", **kw)
    return out[["trade_id", "ticker", "trade_time", "qty", "quote_time", "bid"]].sort_values("trade_id").reset_index(drop=True)

p_main = asof()                                           # direction='backward', exact matches allowed
p_tol = asof(tolerance=pd.Timedelta("30s"))
p_strict = asof(allow_exact_matches=False)
for name, s, p in [("main", SQL_MAIN, p_main), ("tolerance 30s", SQL_TOL, p_tol), ("strictly earlier", SQL_STRICT, p_strict)]:
    d = sql_df(s)
    pd.testing.assert_frame_equal(d, p, check_dtype=False)
    print(f"--- {name}: SQL == merge_asof (sorted by trade_id)")
    print(d[["trade_id", "ticker", "trade_time", "quote_time", "bid"]].to_string(index=False))

# SQLite has no ASOF JOIN
try:
    con.execute("SELECT * FROM trades t ASOF JOIN quotes q ON q.ticker = t.ticker AND q.quote_time <= t.trade_time")
except sqlite3.Error as e:
    print("\nASOF JOIN in SQLite ->", type(e).__name__ + ":", e)

# direction='nearest' and 'forward' exist only in pandas; the SQL needs another subquery
print("\ndirection='forward', bids:", asof(direction="forward")["bid"].tolist())
print("direction='nearest', bids:", asof(direction="nearest")["bid"].tolist())

# merge_asof refuses unsorted input
try:
    pd.merge_asof(trades.sort_values("trade_id", ascending=False), quotes.sort_values("quote_time"),
                  left_on="trade_time", right_on="quote_time", by="ticker")
except ValueError as e:
    print("\nunsorted left ->", type(e).__name__ + ":", e)

# two quotes with the same timestamp: SQL returns two rows for the trade, merge_asof exactly one
con.execute("INSERT INTO quotes VALUES ('A','2026-01-05 09:00:12',11.2)")
con.execute("INSERT INTO trades VALUES (6,'A','2026-01-05 09:00:20',5)")
d = pd.read_sql_query(SQL_MAIN, con)
print("\nwith a duplicate quote timestamp, SQL rows for trade 6:", d[d["trade_id"] == 6]["bid"].tolist())
t2 = pd.read_sql_query("SELECT * FROM trades", con, parse_dates=["trade_time"])
q2 = pd.read_sql_query("SELECT * FROM quotes", con, parse_dates=["quote_time"])
a = pd.merge_asof(t2.sort_values("trade_time"), q2.sort_values("quote_time"),
                  left_on="trade_time", right_on="quote_time", by="ticker")
print("merge_asof rows for trade 6:", a[a["trade_id"] == 6]["bid"].tolist())
con.close()
