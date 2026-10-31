import math, random, heapq
peak=700; svc=0.012; threads=4; headroom=0.30; budget=0.060
per_rep=threads/svc                      # req/s at 100% busy
need=peak*(1+headroom)
reps=math.ceil(need/per_rep)             # one zone must carry the whole peak plus headroom
per_az=reps; reps_az=2*per_az
print("per-replica capacity rps",round(per_rep,1),"needed with headroom",need,"replicas per AZ",per_az,"-> deploy",reps_az)
surv=per_az
print("after losing one AZ: replicas",surv,"util at peak",round(peak/(surv*per_rep),3))
assert peak/(surv*per_rep)<1
print("naive N/2 split (2 per AZ) would give util",round(peak/(2*per_rep),3),"-> saturated")
def sim(lam,c,n=60000,seed=1):
    rnd=random.Random(seed); free=[0.0]*c; heapq.heapify(free); t=0; waits=[]
    for _ in range(n):
        t+=rnd.expovariate(lam); s=rnd.expovariate(1/svc)
        f=heapq.heappop(free); st=max(t,f); waits.append(st-t); heapq.heappush(free,st+s)
    waits.sort(); return waits[int(.99*n)]*1000, sum(waits)/n*1000
c=reps_az*threads
print("servers (threads) in sim:",c,"full cap",round(c/svc))
print("util  p99_wait_ms  mean_wait_ms   (full fleet, then one AZ lost)")
for u in (0.5,0.7,0.85,0.95,0.99):
    p,m=sim(u*c/svc,c); print(f"{u:.2f}  {p:8.2f}  {m:8.2f}")
c2=surv*threads
p,m=sim(peak,c2); print("one AZ lost at 700 rps: util",round(peak*svc/c2,2),"p99 wait ms",round(p,2),"p99 total ~",round(p+12*4.6,1),"(service p99 for exp ~4.6x mean, sandbox model)")
