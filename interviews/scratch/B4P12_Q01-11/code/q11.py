import re, math, tempfile, os
FAKE_AWS="AKIA"+"IOSFODNN7EXAMPLE"        # AWS docs example id shape, fake
FAKE_DB="postgres://app:Sup3rS3cretPw@db.internal:5432/prod"
FAKE_JWT_KEY="hs256_signing_key = 'k9Zx3vQ8rLm2PfT7uYb1NcW5eHd0JaGs'"
RULES={"aws_key_id":re.compile(r"\b(AKIA|ASIA)[A-Z0-9]{16}\b"),
 "db_url_password":re.compile(r"\b[a-z+]+://[^\s:/@]+:([^\s@/]{4,})@"),
 "jwt_like_token":re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
 "private_key_header":re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----")}
ASSIGN=re.compile(r"(?i)(secret|signing_key|api_key|token|password)\w*\s*[=:]\s*['\"]([^'\"]{12,})['\"]")
def entropy(s):
    return -sum(s.count(c)/len(s)*math.log2(s.count(c)/len(s)) for c in set(s))
def scan(text,name):
    hits=[]
    for ln,line in enumerate(text.splitlines(),1):
        for rule,rx in RULES.items():
            if rx.search(line): hits.append((name,ln,rule))
        m=ASSIGN.search(line)
        if m and entropy(m.group(2))>=3.5: hits.append((name,ln,"high_entropy_assignment"))
    return hits
tree={
 "train.py":f"import boto3\nclient = boto3.client('s3', aws_access_key_id='{FAKE_AWS}')\n",
 "config.py":f"DATABASE_URL = '{FAKE_DB}'\n",
 "auth.py":f"{FAKE_JWT_KEY}\n",
 "README.md":"Set api_key = 'your-api-key-goes-here-please' in env\n",   # false positive candidate
 "notes.txt":"token = 'aGVsbG8gd29ybGQgdGhpcyBpcyBiYXNlNjQ='\n",
}
history="""commit 1a2b (removed secret)
- hs256_signing_key = 'k9Zx3vQ8rLm2PfT7uYb1NcW5eHd0JaGs'
+ hs256_signing_key = os.environ['JWT_KEY']
commit 9f9f
+ pwd_in_code = 'p@ss' + 'word123456'
"""
d=tempfile.mkdtemp(prefix="b12q11_",dir="/tmp/claude-0/b12_q01_11")
for n,t in tree.items(): open(os.path.join(d,n),"w").write(t)
hits=[]
for n in sorted(os.listdir(d)): hits+=scan(open(os.path.join(d,n)).read(),n)
print("== working tree"); [print(h) for h in hits]
print("== history-style text"); hh=scan(history,"history.diff"); [print(h) for h in hh]
print("entropy README value",round(entropy("your-api-key-goes-here-please"),2),"; base64 greeting",round(entropy("aGVsbG8gd29ybGQgdGhpcyBpcyBiYXNlNjQ="),2))
