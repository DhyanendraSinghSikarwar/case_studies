from collections import Counter
import math
ref="the cat is on the mat".split()
good="there is a cat on the mat".split()
bad="the the the the the the".split()
def p1(c,r):
    cc,rc=Counter(c),Counter(r); return sum(min(v,rc[w]) for w,v in cc.items())/len(c)
print("clipped unigram precision:",round(p1(good,ref),2),round(p1(bad,ref),2),"(naive for bad:",1.0 if all(w in ref for w in bad) else 0,")")
def rouge1(c,r):
    cc,rc=Counter(c),Counter(r); o=sum(min(v,rc[w]) for w,v in cc.items())
    p,rec=o/len(c),o/len(r); return round(p,2),round(rec,2),round(2*p*rec/(p+rec),2)
print("ROUGE-1 P,R,F1:",rouge1(good,ref))
print("BP for 3-word candidate vs 6-word ref:",round(math.exp(1-6/3),2))
