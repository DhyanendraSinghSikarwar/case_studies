"""Scan a Dockerfile for ARG/ENV names that look like secrets, and secret-looking literal values."""
import re, sys
SUSPECT = re.compile(r"(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY|CREDENTIAL|AWS_SECRET)", re.I)
VALUE = re.compile(r"(sk-[A-Za-z0-9-]{6,}|AKIA[0-9A-Z]{8,}|ghp_[A-Za-z0-9]{10,})")
found = 0
for path in sys.argv[1:]:
    for n, line in enumerate(open(path), 1):
        s = line.strip()
        if re.match(r"(ARG|ENV)\s", s, re.I):
            name = re.split(r"[\s=]", s.split(None, 1)[1])[0]
            if SUSPECT.search(name):
                print(f"{path}:{n}: suspicious {s.split()[0]} name '{name}' (visible in docker history / inspect)"); found += 1
        if VALUE.search(s):
            print(f"{path}:{n}: secret-looking literal value"); found += 1
        if re.search(r"\brm\b.*(netrc|token|\.env|credentials)", s, re.I):
            print(f"{path}:{n}: rm of a secret does not remove it from the earlier layer"); found += 1
print(f"{found} finding(s)")
sys.exit(1 if found else 0)
