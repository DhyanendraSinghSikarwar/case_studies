import re, sys
P = r"C:\Users\11624\OneDrive - Indian School of Business\Documents\personal\bus_2_ml_case_study\interviews\Book1_DS_ML\Book1_DS_ML_Part06.md"
ans = {}
for f in sys.argv[1:]:
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r"^@@Q(\d+)\n(.*?)(?=^@@Q|\Z)", txt, re.S | re.M):
        ans[int(m.group(1))] = m.group(2).strip("\n")
s = open(P, encoding="utf-8").read()  # universal newlines -> \n
for n, a in ans.items():
    pat = re.compile(r"(^### Q%d ⭐[^\n]*\n\*\*Asked at:\*\*[^\n]*\n)<!-- ANSWER_PENDING -->" % n, re.M)
    assert len(pat.findall(s)) == 1, n
    s = pat.sub(lambda m: m.group(1) + a, s, count=1)
nl = chr(13) + chr(10)
open(P, "w", encoding="utf-8", newline=nl).write(s)
print("applied", sorted(ans))
