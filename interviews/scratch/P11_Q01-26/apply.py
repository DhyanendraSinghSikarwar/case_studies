import re,glob,io
base="scratch/P11_Q01-26/"
txt="".join(open(base+f,encoding="utf-8").read()+"\n" for f in ["a1.md","a2.md","a3.md","a4.md"])
txt=txt.replace("and about 20-30% of COD orders in some categories; goal","and RTO rates on COD can be high in some categories; goal").replace("returns are a major cost in fashion (often 20-40%)","returns are a major cost in fashion (return rates can be very high)")
ans={int(m.group(1)):m.group(2).strip("\n") for m in re.finditer(r"@@Q(\d+)\n(.*?)(?=\n@@Q|\Z)",txt,re.S)}
assert sorted(ans)==list(range(1,27)),sorted(ans)
p="Book1_DS_ML/Book1_DS_ML_Part11.md"
s=open(p,encoding="utf-8",newline="").read()
nl="\r\n" if "\r\n" in s else "\n"
for n,a in ans.items():
    pat=re.compile(r"(### Q%d [^\n]*\n\*\*Asked at:\*\*[^\n]*?\r?\n)<!-- ANSWER_PENDING -->"%n)
    assert len(pat.findall(s))==1,n
    s=pat.sub(lambda m:m.group(1)+a.replace("\n",nl),s)
open(p,"w",encoding="utf-8",newline="").write(s)
