import re,sys
F=r"C:\Users\11624\OneDrive - Indian School of Business\Documents\personal\bus_2_ml_case_study\interviews\Book1_DS_ML\Book1_DS_ML_Part08.md"
src=open(sys.argv[1],encoding="utf-8").read()
parts=re.split(r"^=====Q(\d+)\n",src,flags=re.M)
ans={int(parts[i]):parts[i+1].strip("\n") for i in range(1,len(parts),2)}
t=open(F,encoding="utf-8").read()
for n,a in ans.items():
    assert 1<=n<=29
    pat=re.compile(r"(^### Q%d \D[^\n]*\n\*\*Asked at:\*\*[^\n]*\n)<!-- ANSWER_PENDING -->"%n,re.M)
    assert len(pat.findall(t))==1,n
    t=pat.sub(lambda m:m.group(1)+a,t,count=1)
open(F,"w",encoding="utf-8",newline="\r\n").write(t)
print("applied",sorted(ans))
