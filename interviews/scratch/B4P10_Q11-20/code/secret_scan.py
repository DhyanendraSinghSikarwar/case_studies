"""Tiny secret scanner for Dockerfiles and env files. Heuristic only: it will miss some and flag some."""
import re, sys, pathlib

AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
NAME_HINT = re.compile(r"(secret|password|passwd|token|api[_-]?key|private[_-]?key)", re.I)
ASSIGN = re.compile(r"^\s*(?:export\s+)?(?:(?:ENV|ARG)\s+)?([A-Za-z0-9_]+)\s*[= ]\s*(.+?)\s*$")
SAFE_VALUE = re.compile(r"^(\$\{?\w+\}?|<.*>|changeme|example|xxx+|)$", re.I)

def scan_text(name, text):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if AWS_KEY.search(line):
            out.append((name, n, "aws-access-key-id-shape"))
        m = ASSIGN.match(line)
        if m and NAME_HINT.search(m.group(1)):
            val = m.group(2).strip("'\"")
            if re.search(r"_(FILE|PATH|URI|URL)$", m.group(1), re.I) or val.startswith("/"):
                continue  # a pointer to a secret, not the secret
            if not SAFE_VALUE.match(val) and len(val) >= 6:
                out.append((name, n, f"hardcoded value for {m.group(1)}"))
        if re.search(r"curl[^|]*-u\s+\S+:\S+", line):
            out.append((name, n, "credentials in curl -u"))
    return out

if __name__ == "__main__":
    hits = []
    for p in sys.argv[1:]:
        hits += scan_text(p, pathlib.Path(p).read_text())
    for h in hits:
        print(f"{h[0]}:{h[1]}: {h[2]}")
    print(f"{len(hits)} finding(s)")
    sys.exit(1 if hits else 0)
