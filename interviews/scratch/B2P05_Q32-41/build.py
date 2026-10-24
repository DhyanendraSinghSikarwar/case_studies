import re,sys,os
# usage: build.py  -> rebuilds answers.md from blocks/qNN.md in order, substituting {{CODE:file}}
out=[]
for n in range(32,42):
    p=f"blocks/q{n}.md"
    if not os.path.exists(p): continue
    t=open(p).read().strip("\n")
    t=re.sub(r"\{\{CODE:(.+?)\}\}",lambda m:open("code/"+m.group(1)).read().rstrip("\n"),t)
    out.append(t)
open("answers.md","w").write("\n\n".join(out)+"\n")
