import re,glob
rm={2:[13,14,10,41],14:[10],10:[50,56],5:[13],3:[32],4:[30],8:[55],1:[36],9:[38],11:[21]}
rows=[];log=[]
for p in range(1,15):
    f=f"Book1_DS_ML/Book1_DS_ML_Part{p:02d}.md"
    t=open(f,encoding='utf-8').read()
    parts=re.split(r'(?m)^(?=### Q\d+ )',t)
    head,blocks=parts[0],parts[1:]
    out=[];n=0
    for b in blocks:
        q=int(re.match(r'### Q(\d+) ',b).group(1))
        if q in rm.get(p,[]):
            log.append((p,q,b.split('\n')[0][:110])); continue
        n+=1
        b=re.sub(r'^### Q\d+ ',f'### Q{n} ',b,count=1)
        out.append(b)
        title=re.sub(r'^### Q\d+ (?:⭐+ )?(?:[🟢🟡🔴] )?','',b.split('\n')[0])
        rows.append(f"| B1P{p:02d}-Q{n} | {p} | {title} |")
    head=re.sub(r'(\*\*Actual:\*\*\s*)\d+',lambda m:m.group(1)+str(n),head,count=1)
    if rm.get(p): head=head.rstrip('\n')+f"\n\n> Dedupe pass: removed {len(rm[p])} cross-part duplicate(s); renumbered Q1–Q{n}. (Star counts in header lines above may be stale.)\n\n---\n\n"
    open(f,'w',encoding='utf-8').write(head+''.join(out))
idx=open('question_index.md',encoding='utf-8').read().split('| Q-ID | Part | Canonical question |')[0]
open('question_index.md','w',encoding='utf-8').write(idx+'| Q-ID | Part | Canonical question |\n|---|---|---|\n'+'\n'.join(rows)+'\n')
for l in log: print(l)
print(len(rows))
