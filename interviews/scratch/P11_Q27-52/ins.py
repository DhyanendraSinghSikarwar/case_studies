import re
P=r"C:/Users/11624/OneDrive - Indian School of Business/Documents/personal/bus_2_ml_case_study/interviews/Book1_DS_ML/Book1_DS_ML_Part11.md"
ans=open("answers_a.md",encoding="utf-8").read()
parts=re.split(r"^=== Q(\d+)\n",ans,flags=re.M)
d={int(parts[i]):parts[i+1].strip("\n")+"\n" for i in range(1,len(parts),2)}
assert sorted(d)==list(range(27,53))
t=open(P,encoding="utf-8").read()
for q,a in d.items():
    pat=re.compile(r"(^### Q%d [^\n]*\n\*\*Asked at:\*\*[^\n]*\n)<!-- ANSWER_PENDING -->\n"%q,re.M)
    t,n=pat.subn(lambda m:m.group(1)+a,t,count=1); assert n==1,q
open(P,"w",encoding="utf-8",newline="").write(t)
