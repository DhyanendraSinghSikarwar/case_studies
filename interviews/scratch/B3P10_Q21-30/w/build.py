import re, subprocess, pathlib
W = pathlib.Path(__file__).parent
part = pathlib.Path("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part10.md").read_text().split("\n")

def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i+1].startswith("**Asked at:**")
    return part[i] + "\n" + part[i+1]

def code(q): return (W / f"{q}.py").read_text().rstrip("\n")
def out(q):
    r = subprocess.run(["python3", "-I", str(W / f"{q}.py")], capture_output=True, text=True, cwd="/tmp")
    assert r.returncode == 0 and r.stderr.strip() == "", (q, r.stderr[-500:])
    return r.stdout.rstrip("\n")
def schema(q):
    m = re.search(r'executescript\("""(.*?)"""\)', code(q), re.S)
    return m.group(1).strip("\n")

SCHEMA_OVERRIDE = {
 "q22": """CREATE TABLE items(item_id INTEGER PRIMARY KEY, price_text TEXT, qty INTEGER, code);   -- code: no declared type
-- loaded from CSV text, so every value arrives as a string:
INSERT INTO items VALUES (1,'9','3','9'),(2,'10','12','10'),(3,'100','7','100'),(4,'2.5','5','2.5');""",
 "q26": """CREATE TABLE u_unique(email TEXT UNIQUE);
CREATE TABLE u_check(age INTEGER CHECK(age >= 18));
CREATE TABLE u_pk(code TEXT PRIMARY KEY, n INTEGER);            -- not INTEGER PRIMARY KEY
CREATE TABLE u_pk_nn(code TEXT PRIMARY KEY NOT NULL, n INTEGER);
CREATE TABLE u_pk_wr(code TEXT PRIMARY KEY, n INTEGER) WITHOUT ROWID;
CREATE TABLE u_pk_int(id INTEGER PRIMARY KEY, n INTEGER);
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_active INTEGER);          -- 1, 0 or NULL
INSERT INTO users VALUES (1,1),(2,1),(3,0),(4,NULL),(5,NULL);""",
 "q25": """CREATE TABLE contacts_a(email TEXT);
CREATE TABLE contacts_b(email TEXT);
INSERT INTO contacts_a VALUES ('a@x.com'),('a@x.com'),(NULL),(NULL),('b@x.com');
INSERT INTO contacts_b VALUES ('a@x.com'),(NULL),('c@x.com'),(NULL);""",
 "q28": """CREATE TABLE scores_wide(student TEXT, math_2023 INTEGER, math_2024 INTEGER, sci_2023 INTEGER, sci_2024 INTEGER);
INSERT INTO scores_wide VALUES ('Zed',90,92,80,NULL),('Ana',70,NULL,65,66),('Mia',NULL,NULL,NULL,NULL);
-- the long table scores_long (student, subject, year, score) is built from it by the UNION ALL query below""",
 "q30": """CREATE TABLE sales(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A',10),('East','A',5),('East','B',20),('East','C',30),
 ('West','A',40),('West','B',15);                                   -- West has no C row""",
}
exec(open(W / "prose.py").read())
blocks = []
for n in range(21, 31):
    q = f"q{n}"
    P = PROSE[n]
    sch = SCHEMA_OVERRIDE.get(q, None) or schema(q)
    b = [head(n), ""]
    b.append(f"**Say this first (1 line):** {P['say']}\n")
    b.append("**Schema and sample data:**\n```sql\n" + sch + "\n```\n")
    b.append("**SQL answer:** " + P["sql"] + "\n")
    b.append("**pandas answer:** " + P["pandas"] + "\n")
    b.append("**Example:** " + P["example"] + "\n")
    b.append("**Code:** run with `python3 -I`.\n```python\n" + code(q) + "\n```\n")
    b.append("**Output (my run):**\n```text\n" + out(q) + "\n```\n")
    b.append("**Edge cases:**\n" + P["edge"] + "\n")
    b.append("**Then explain:**\n" + P["explain"] + "\n")
    b.append("**Follow-ups:**\n" + P["follow"] + "\n")
    b.append("**Common mistakes:**\n" + P["mistakes"] + "\n")
    blocks.append("\n".join(b))
(W.parent / "answers.md").write_text("\n".join(blocks) + "\n")
print("written", len(blocks))
