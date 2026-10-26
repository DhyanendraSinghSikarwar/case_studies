# Q34: CTR per campaign with zero guards.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE impressions(campaign_id INTEGER, impressions INTEGER);
CREATE TABLE clicks(campaign_id INTEGER, clicks INTEGER);
INSERT INTO impressions VALUES (1,1000),(2,500),(3,0),(4,200),(5,7),(6,0);
INSERT INTO clicks VALUES (1,37),(3,0),(4,5),(5,3);
""")

sql_answer = """
SELECT i.campaign_id,
       ROUND(COALESCE(c.clicks, 0) * 1.0 / NULLIF(i.impressions, 0), 4) AS ctr
FROM impressions i
LEFT JOIN clicks c ON c.campaign_id = i.campaign_id
ORDER BY i.campaign_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\nunguarded division in SQLite, 3 / 0 and 0 / 0:", con.execute("SELECT 3*1.0/0, 0*1.0/0").fetchone())

# --- pandas
imp = pd.read_sql("SELECT * FROM impressions", con)
clk = pd.read_sql("SELECT * FROM clicks", con)
m = imp.merge(clk, on="campaign_id", how="left")
m["ctr"] = (m.clicks.fillna(0) / m.impressions.replace(0, np.nan)).round(4)
want = m[["campaign_id", "ctr"]]
# --- end pandas
print("\npandas"); print(want.to_string(index=False, na_rep="NaN"))
print("unguarded pandas division 3 / 0 and 0 / 0:",
      (pd.Series([3.0, 0.0]) / pd.Series([0.0, 0.0])).tolist())
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: NULL in SQL equals NaN in pandas for campaigns 3 and 6")
