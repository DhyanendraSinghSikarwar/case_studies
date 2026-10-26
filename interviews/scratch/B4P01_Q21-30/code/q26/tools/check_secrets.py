import re, sys
# deliberately small; real teams use a maintained scanner (detect-secrets, gitleaks, ...). Check current docs.
PATTERNS = [r"AKIA[0-9A-Z]{16}", r"(?i)(api[_-]?key|secret|password|token)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
            r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"]
bad = 0
for f in sys.argv[1:]:
    try: text = open(f, errors="ignore").read()
    except OSError: continue
    for i, line in enumerate(text.splitlines(), 1):
        if any(re.search(p, line) for p in PATTERNS):
            print(f"{f}:{i}: looks like a secret"); bad = 1
sys.exit(bad)
