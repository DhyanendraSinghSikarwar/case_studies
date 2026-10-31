# Q19: counting substrings, words and vowels with LENGTH/REPLACE, versus pandas str.count
import re
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE logs(id INTEGER PRIMARY KEY, raw_line TEXT);
INSERT INTO logs VALUES
 (1,'error error warn'),(2,'ok'),(3,NULL),(4,'Error,error'),(5,''),(6,'a  b   c'),(7,'  disk  full  ');
CREATE TABLE names(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO names VALUES (1,'Anil'),(2,'RAHUL'),(3,'Rhythm'),(4,'Aeiou'),(5,NULL);
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)

# <<sql_main
SQL_COUNTS = """
SELECT id,
       (LENGTH(raw_line) - LENGTH(REPLACE(raw_line, 'error', ''))) / LENGTH('error')                 AS err_case_sensitive,
       (LENGTH(raw_line) - LENGTH(REPLACE(LOWER(raw_line), LOWER('error'), ''))) / LENGTH('error')   AS err_any_case,
       LENGTH(TRIM(raw_line)) - LENGTH(REPLACE(TRIM(raw_line), ' ', '')) + 1                         AS words_naive,
       CASE WHEN TRIM(raw_line) = '' THEN 0
            ELSE LENGTH(TRIM(REPLACE(REPLACE(REPLACE(raw_line, '  ', ' '), '  ', ' '), '  ', ' ')))
               - LENGTH(REPLACE(TRIM(REPLACE(REPLACE(REPLACE(raw_line, '  ', ' '), '  ', ' '), '  ', ' ')), ' ', '')) + 1
       END                                                                                           AS words_fixed
FROM logs ORDER BY id
"""
# >>
# <<sql_vowels
SQL_VOWELS = """
SELECT id, name,
       LENGTH(name) - LENGTH(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(LOWER(name), 'a', ''), 'e', ''), 'i', ''), 'o', ''), 'u', '')) AS vowels
FROM names ORDER BY id
"""
# >>
sql = pd.read_sql_query(SQL_COUNTS, con)
vow = pd.read_sql_query(SQL_VOWELS, con)
print("\nSQL counts (NULL line gives NULL; the empty line gives words_naive = 1):")
print(sql.to_string(index=False))
print("\nSQL vowels:"); print(vow.to_string(index=False))

# <<pd
logs = pd.read_sql_query("SELECT * FROM logs ORDER BY id", con)
names = pd.read_sql_query("SELECT * FROM names ORDER BY id", con)
line = logs["raw_line"]
p = pd.DataFrame({
    "id": logs["id"],
    "err_case_sensitive": line.str.count("error"),
    "err_any_case": line.str.count("error", flags=re.IGNORECASE),
    "words": line.str.split().str.len(),
})
p_vowels = names["name"].str.count("[aeiouAEIOU]")
# >>
print("\npandas str.count / split:"); print(p.to_string(index=False))

# comparisons (ordered by id; SQL NULL equals pandas NaN)
pd.testing.assert_series_equal(p["err_case_sensitive"], sql["err_case_sensitive"].astype(float), check_names=False)
pd.testing.assert_series_equal(p["err_any_case"], sql["err_any_case"].astype(float), check_names=False)
pd.testing.assert_series_equal(p["words"], sql["words_fixed"].astype(float), check_names=False)
pd.testing.assert_series_equal(p_vowels, vow["vowels"].astype(float), check_names=False)
assert sql["words_naive"].tolist()[:2] == [3, 1] and sql.loc[4, "words_naive"] == 1 and sql.loc[5, "words_naive"] == 6 and sql.loc[6, "words_naive"] == 3
print("asserts passed (SQL and pandas equal, ordered by id; the naive word count is not asserted equal because it is wrong)")

# overlap
print("\noverlap: does 'aaa' contain 'aa' once or twice?")
sql_overlap = con.execute("SELECT (LENGTH('aaa') - LENGTH(REPLACE('aaa', 'aa', ''))) / LENGTH('aa'), REPLACE('aaa', 'aa', '')").fetchone()
a = pd.Series(["aaa"])
print("  SQL LENGTH/REPLACE:", sql_overlap[0], "(REPLACE leaves", repr(sql_overlap[1]) + ")")
print("  pandas str.count('aa')            :", a.str.count("aa")[0])
print("  pandas str.count('(?=aa)') lookahead:", a.str.count("(?=aa)")[0])
print("  Python 'aaa'.count('aa')          :", "aaa".count("aa"))
assert sql_overlap[0] == a.str.count("aa")[0] == "aaa".count("aa") == 1 and a.str.count("(?=aa)")[0] == 2

# regex versus literal
b = pd.Series(["a.b.c"])
print("\nstr.count is always a regex: '.' ->", b.str.count(".")[0], "| r'\\.' ->", b.str.count(r"\.")[0],
      "| re.escape('.') ->", b.str.count(re.escape("."))[0], "| SQL on 'a.b.c':",
      con.execute("SELECT LENGTH('a.b.c') - LENGTH(REPLACE('a.b.c', '.', ''))").fetchone()[0])
# the empty pattern: REPLACE(s, '', '') returns s unchanged, and dividing by LENGTH('') = 0 gives NULL in SQLite
print("\nempty pattern: REPLACE('abc', '', '') ->", repr(con.execute("SELECT REPLACE('abc', '', '')").fetchone()[0]),
      "| 3 / LENGTH('') ->", con.execute("SELECT 3 / LENGTH('')").fetchone()[0], "(division by zero is NULL in SQLite)")
# a substring is not a word
print("substring is not a word: 'terrors' counts", con.execute("SELECT (LENGTH('terrors') - LENGTH(REPLACE('terrors', 'error', ''))) / 5").fetchone()[0], "occurrence of 'error'")

# LIKE case-insensitivity and PRAGMA case_sensitive_like
print("\n'Error' LIKE '%error%':", con.execute("SELECT 'Error' LIKE '%error%'").fetchone()[0], "| REPLACE is case-sensitive:",
      con.execute("SELECT REPLACE('Error', 'error', '')").fetchone()[0])
con.execute("PRAGMA case_sensitive_like = 1")
print("after PRAGMA case_sensitive_like = 1: 'Error' LIKE '%error%' ->", con.execute("SELECT 'Error' LIKE '%error%'").fetchone()[0])
con.execute("PRAGMA case_sensitive_like = 0")
