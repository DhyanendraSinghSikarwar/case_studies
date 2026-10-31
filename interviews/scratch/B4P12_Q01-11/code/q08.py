import random
rnd=random.Random(7)
N=400_000; fraud=0.001
y=[rnd.random()<fraud for _ in range(N)]
day=[rnd.randrange(60) for _ in range(N)]
score=[rnd.gauss(2.0 if f else 0.0,1) for f in y]
thr=sorted(score)[int(0.995*N)]          # analysts review top 0.5 percent
flag=[s>=thr for s in score]
cb=[rnd.randrange(7,46) for _ in range(N)]        # chargeback delay 7..45
fast=[rnd.randrange(1,4) for _ in range(N)]       # analyst confirms in 1..3 days (scenario 2)
nf=sum(y); tp=sum(1 for f,v in zip(flag,y) if f and v)
print("frauds",nf,"true recall at top 0.5%:",round(tp/nf,3))
cohort=[i for i in range(N) if day[i]<7 and y[i]]       # first week of the fresh model
caught=[i for i in cohort if flag[i]]
def run(name,lab_delay):
    print(name)
    for ed in (7,14,30,50):
        arrived=[i for i in cohort if day[i]+lab_delay(i)<=ed]
        a=sum(1 for i in arrived if flag[i])
        A=a/len(cohort); B=a/max(1,len(arrived))
        print(f"  eval day {ed:2}: labelled {len(arrived):2}/{len(cohort)}  recall A (caught-labelled / all eventual frauds) {A:.3f}   recall B (among labelled only) {B:.3f}")
run("scenario 1: all labels via 7-45 day process",lambda i:cb[i])
run("scenario 2: flagged frauds confirmed in 1-3 days, missed ones wait for chargeback",lambda i:fast[i] if flag[i] else cb[i])
print("cohort true recall:",round(len(caught)/len(cohort),3))
