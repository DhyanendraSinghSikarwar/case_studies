def spans(tags):
    out=set(); start=None; typ=None
    for i,t in enumerate(tags+["O"]):
        if t=="O" or t.startswith("B-") or (t.startswith("I-") and t[2:]!=typ):
            if start is not None: out.add((start,i,typ)); start=None; typ=None
            if t!="O": start,typ=i,t[2:]
    return out
gold=["B-PER","I-PER","O","B-ORG","O","B-LOC"]
pred=["B-PER","O","O","B-ORG","O","B-LOC"]
g,p=spans(gold),spans(pred); tp=len(g&p)
pr,rc=tp/len(p),tp/len(g); print(g,p,"P",pr,"R",rc,"F1",round(2*pr*rc/(pr+rc),2))
