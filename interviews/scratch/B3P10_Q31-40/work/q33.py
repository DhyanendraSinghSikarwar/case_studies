# Hard text cleaning and Unicode in SQLite versus pandas.
import sqlite3
import unicodedata
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE names(id INTEGER PRIMARY KEY, name TEXT)")
rows = [
    (1, "Asha Rao"),            # NBSP between words
    (2, "\tBen "),                   # tab and a space around
    (3, "Chi\ntra"),                 # newline inside
    (4, "Dev​"),                # zero-width space at the end
    (5, "Renée"),               # composed e-acute
    (6, "Renée"),              # decomposed e + combining acute
    (7, "Straße"),              # German sharp s
    (8, "İstanbul"),            # Turkish capital dotted I
    (9, "Zoe \U0001F600"),           # emoji
    (10, "a\x00b"),                  # embedded NUL
]
con.executemany("INSERT INTO names VALUES (?,?)", rows)

q = """SELECT id, length(name) AS len, octet_length(name) AS bytes, length(trim(name)) AS len_trim,
              hex(name) AS hex_name
       FROM names ORDER BY id"""
sql_df = pd.read_sql(q, con)
print(sql_df.to_string(index=False))

# 1) TRIM versus the characters it does not know
print("trim keeps NBSP/tab?",
      con.execute("SELECT length(trim(?)), length(trim(?))", (" x ", "\tx\t")).fetchone(), "(3 and 3 = nothing stripped)")
print("trim with explicit set:",
      con.execute("SELECT length(trim(?, char(160, 9, 10, 32)))", (" \tx \n",)).fetchone()[0])

# 2) case folding is ASCII-only
print("upper/lower:", con.execute("SELECT upper('straße é'), lower('ÀB İ'), 'é' = 'É' COLLATE NOCASE, 'e' = 'E' COLLATE NOCASE").fetchone())

# 3) composed and decomposed are different strings
print("composed = decomposed:", con.execute("SELECT (SELECT name FROM names WHERE id=5) = (SELECT name FROM names WHERE id=6)").fetchone()[0],
      "| lengths:", con.execute("SELECT length(name) FROM names WHERE id IN (5,6) ORDER BY id").fetchall())

# 4) find invisible characters: unicode() of the first char, and a scan with a recursive CTE
scan = """
WITH RECURSIVE ch(id, pos, cp) AS (
  SELECT id, 1, unicode(substr(name,1,1)) FROM names WHERE id IN (1,2,3,4,6)
  UNION ALL
  SELECT n.id, ch.pos+1, unicode(substr(n.name, ch.pos+1, 1))
  FROM ch JOIN names n ON n.id = ch.id WHERE ch.pos < length(n.name)
)
SELECT id, pos, cp FROM ch WHERE cp IN (160, 9, 10, 8203, 769) ORDER BY id, pos"""
print("suspect code points (id, position, code point):", con.execute(scan).fetchall())

# 5) clean with REPLACE and CHAR
clean = """SELECT id, trim(replace(replace(replace(replace(name, char(160), ' '), char(9), ' '), char(10), ' '), char(8203), '')) AS cleaned
           FROM names WHERE id IN (1,2,3,4) ORDER BY id"""
sql_clean = pd.read_sql(clean, con)
print(sql_clean.to_string(index=False))

# 6) pandas
s = pd.Series([r[1] for r in rows], index=[r[0] for r in rows], name="name")
print("pandas dtype:", s.dtype)
print("strip removes NBSP:", repr(" x  ".join([""])) and pd.Series([" x ", "\tx\t"]).str.strip().tolist())
same = (s.str.len().values == sql_df["len"].values)
print("pandas len equals SQL length on rows:", [int(i) for i in sql_df["id"][same]], "| differs on:", [int(i) for i in sql_df["id"][~same]])
assert list(sql_df["id"][~same]) == [10]
nfc = s.str.normalize("NFC")
print("NFC makes 5 == 6:", nfc[5] == nfc[6], "| raw:", s[5] == s[6])
print("casefold('Straße') =", pd.Series(["Straße"]).str.casefold()[0], "| upper('ß') =", pd.Series(["ß"]).str.upper()[0],
      "| lower('İ') length =", len(pd.Series(["İ"]).str.lower()[0]))
# NUL: SQL length stops at the NUL, Python len does not
print("NUL row: SQL length =", sql_df.loc[9, "len"], "| Python len =", len("a\x00b"), "| octet_length =", sql_df.loc[9, "bytes"])

p_clean = (s[[1, 2, 3, 4]].str.replace("​", "", regex=False)
            .str.replace(r"\s+", " ", regex=True).str.strip())    # \s matches NBSP, tab, newline in Python regex
print(p_clean.tolist())
assert sql_clean["cleaned"].tolist() == p_clean.tolist() == ["Asha Rao", "Ben", "Chi tra", "Dev"]

# Python title() surprise for names (pandas str.title)
print("str.title:", pd.Series(["o'neil", "mcdonald", "ASHA rao"]).str.title().tolist())
print("composed != decomposed in SQL, equal after unicodedata NFC:",
      unicodedata.normalize("NFC", rows[4][1]) == unicodedata.normalize("NFC", rows[5][1]))
con.close()
print("asserts passed")
