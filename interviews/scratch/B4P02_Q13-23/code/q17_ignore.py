# Q17: simplified .dockerignore matcher. Last matching rule wins; '!' re-includes. Prints what would be sent.
import os, re, sys

def to_regex(pat):
    pat = pat.rstrip("/")
    out, i = "", 0
    while i < len(pat):
        c = pat[i]
        if pat[i:i+3] == "**/": out += "(?:.*/)?"; i += 3
        elif pat[i:i+2] == "**": out += ".*"; i += 2
        elif c == "*": out += "[^/]*"; i += 1
        elif c == "?": out += "[^/]"; i += 1
        else: out += re.escape(c); i += 1
    return re.compile("^" + out + "(?:/.*)?$")      # a match on a directory covers everything under it

def load(path):
    rules = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"): continue
        neg = line.startswith("!"); rules.append((neg, line.lstrip("!"), to_regex(line.lstrip("!").lstrip("/"))))
    return rules

def ignored(rel, rules):
    res, why = False, None
    for neg, raw, rx in rules:
        if rx.match(rel): res, why = (not neg), raw
    return res, why

if __name__ == "__main__":
    root, ig = sys.argv[1], sys.argv[2]
    rules = load(ig); sent, skipped = [], []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), root); size = os.path.getsize(os.path.join(dp, f))
            ign, why = ignored(rel, rules)
            (skipped if ign else sent).append((rel, size, why))
    print("SENT to daemon:");   [print(f"  {r}  ({s} B)") for r, s, _ in sorted(sent)]
    print("EXCLUDED:");         [print(f"  {r}  <- {w}") for r, s, w in sorted(skipped)]
    print(f"context: {sum(s for _,s,_ in sent)} B sent, {sum(s for _,s,_ in skipped)} B kept out")
