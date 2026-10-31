import sys,re
pat=sys.argv[1]
for l in sys.stdin:
    l=l.rstrip()
    m=re.match(r'^\d{4}-\d\d-\d\dT[\d:.]+Z \[(\w+)\s*\] (.*?)\s+\[[\w.]+\].*$',l)
    msg = f"{m.group(1)}: {m.group(2)}" if m else l
    if re.search(pat,msg): print(msg[:230])
