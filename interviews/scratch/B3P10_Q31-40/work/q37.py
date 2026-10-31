# Palindromes and anagram groups in SQLite (no REVERSE) versus pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE words(word TEXT);
INSERT INTO words VALUES ('madam'),('Level'),('abc'),('A man a plan'),(NULL),(''),
  ('Taco cat'),('listen'),('Silent'),('tinsel'),('cab'),('bca');
""")

pal_sql = """
WITH RECURSIVE w AS (
  SELECT DISTINCT word, lower(replace(word, ' ', '')) AS norm FROM words WHERE word IS NOT NULL
), rev(word, norm, i, r) AS (
  SELECT word, norm, 0, '' FROM w
  UNION ALL
  SELECT word, norm, i + 1, substr(norm, i + 1, 1) || r      -- prepend the next character
  FROM rev WHERE i < length(norm)
)
SELECT word, norm, r AS reversed, (norm = r) AS is_palindrome
FROM rev WHERE i = length(norm) ORDER BY word"""
sql_pal = pd.read_sql(pal_sql, con)
print(sql_pal.to_string(index=False))

anag_sql = """
WITH RECURSIVE w AS (
  SELECT DISTINCT word, lower(replace(word, ' ', '')) AS norm FROM words WHERE word IS NOT NULL
), ch(word, norm, pos, c) AS (
  SELECT word, norm, 1, substr(norm, 1, 1) FROM w WHERE norm <> ''
  UNION ALL
  SELECT word, norm, pos + 1, substr(norm, pos + 1, 1) FROM ch WHERE pos < length(norm)
), sig AS (
  SELECT word, group_concat(c, '' ORDER BY c) AS signature FROM ch GROUP BY word
)
SELECT signature, COUNT(*) AS n, group_concat(word, ',' ORDER BY word) AS members
FROM sig GROUP BY signature HAVING COUNT(*) > 1 ORDER BY signature"""
sql_anag = pd.read_sql(anag_sql, con)
print(sql_anag.to_string(index=False))

# group_concat(DISTINCT x, sep) is rejected: DISTINCT works only with a single argument
try:
    con.execute("SELECT group_concat(DISTINCT word, '|') FROM words").fetchall()
except sqlite3.Error as e:
    print("group_concat(DISTINCT word, '|') ->", e)
print("group_concat(DISTINCT word) works, default separator ',':", con.execute("SELECT group_concat(DISTINCT word) FROM (SELECT word FROM words WHERE word IN ('abc','abc','cab') ORDER BY word)").fetchone()[0])
print("string_agg with ORDER BY works:", con.execute("SELECT string_agg(word, '|' ORDER BY word) FROM words WHERE word LIKE '%a%'").fetchone()[0])
print("reverse:", end=" ")
try:
    con.execute("SELECT reverse('abc')")
except sqlite3.Error as e:
    print(e)

# ---- pandas
df = pd.read_sql("SELECT word FROM words", con)
norm = df["word"].str.lower().str.replace(" ", "", regex=False)
p_pal = pd.DataFrame({"word": df["word"], "norm": norm})
p_pal = p_pal.dropna().drop_duplicates()
p_pal["reversed"] = p_pal["norm"].str[::-1]
p_pal["is_palindrome"] = (p_pal["norm"] == p_pal["reversed"]).astype(int)
p_pal = p_pal.sort_values("word").reset_index(drop=True)
pd.testing.assert_frame_equal(p_pal[["word", "norm", "reversed", "is_palindrome"]], sql_pal, check_dtype=False)  # sorted by word (binary)

nn = p_pal[p_pal["norm"] != ""].copy()
nn["signature"] = nn["norm"].map(lambda w: "".join(sorted(w)))
p_anag = (nn.groupby("signature").agg(n=("word", "size"), members=("word", lambda s: ",".join(sorted(s))))
            .query("n > 1").reset_index())
pd.testing.assert_frame_equal(p_anag, sql_anag, check_dtype=False)       # sorted by signature
print("pandas palindromes:", p_pal.loc[p_pal.is_palindrome == 1, "word"].tolist())
print("pandas anagram groups:", p_anag[["signature", "members"]].values.tolist())
con.close()
print("asserts passed")
