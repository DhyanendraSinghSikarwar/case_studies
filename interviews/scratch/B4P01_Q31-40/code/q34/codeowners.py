"""Tiny CODEOWNERS matcher. Rule: the LAST matching line wins. Supports the common patterns only:
'*', '/dir/' (anchored dir), 'dir/' (any depth), '*.ext', '/file'. Not full gitignore syntax."""
import fnmatch, sys

CODEOWNERS = """\
# default owner
*                       @acme/ml-platform
/models/                @acme/data-science
/src/features/          @acme/data-science @acme/ml-platform
/deploy/                @acme/ml-platform
*.ipynb                 @acme/data-science
/deploy/secrets.example @acme/security
"""

def parse(text):
    rules = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            pat, *owners = line.split()
            rules.append((pat, owners))
    return rules

def matches(pat, path):
    anchored = pat.startswith("/")
    p = pat.lstrip("/")
    if p.endswith("/"):                       # directory pattern
        return path.startswith(p) if anchored else (path.startswith(p) or ("/" + p) in ("/" + path))
    if anchored:
        return fnmatch.fnmatch(path, p)
    return fnmatch.fnmatch(path, p) or fnmatch.fnmatch(path.rsplit("/", 1)[-1], p)

def owners_of(path, rules):
    found = []
    for pat, owners in rules:                 # keep the last hit
        if matches(pat, path):
            found = owners
    return found

if __name__ == "__main__":
    rules = parse(CODEOWNERS)
    for path in ["models/churn/model.py", "deploy/k8s/serve.yaml", "deploy/secrets.example",
                 "src/features/scale.py", "notebooks/eda.ipynb", "README.md"]:
        print(f"{path:28} -> {' '.join(owners_of(path, rules))}")
