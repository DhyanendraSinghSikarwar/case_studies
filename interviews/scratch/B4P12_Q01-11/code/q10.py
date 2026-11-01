import random, statistics
def arrivals():
    t=0.0; out=[]
    for rate,dur in ((200,20),(40,100)):
        end=t+dur
        n=int(rate*dur)
        for i in range(n): out.append(t+i/rate)
        t=end
    return out
MU=80; TIMEOUT=2.0   # callers give up after 2s
def run(policy,cap=None):
    arr=arrivals(); q=[]; busy_until=0.0; waits=[]; rej=0; wasted=0; done=0; maxq=0
    # event-free fluid-ish discrete sim: process in arrival order with FIFO server, rate MU
    import heapq
    ev=[(a,'a') for a in arr]; i=0; now=0.0; q=[]; server_free=0.0
    # advance time by arrivals; serve between arrivals
    def serve_until(t):
        nonlocal server_free,done,wasted
        while q and server_free<=t:
            # pick next
            a=q.pop(0)
            start=max(server_free,a)
            if policy=="timeout_drop" and start-a>TIMEOUT:
                continue                    # dropped before work started
            waits.append(start-a)
            server_free=start+1/MU
            if start-a>TIMEOUT: wasted+=1     # caller already gone, work still done
            else: done+=1
    for a in arr:
        serve_until(a)
        if cap is not None and len(q)>=cap:
            if policy=="bounded_reject": rej+=1; continue
            if policy=="timeout_drop": q.pop(0); rej+=1      # drop oldest
        q.append(a); maxq=max(maxq,len(q))
    serve_until(1e9)
    waits.sort(); p99=waits[int(.99*len(waits))] if waits else 0
    return dict(policy=policy,total=len(arr),max_depth=maxq,p99_wait_s=round(p99,2),rejected_or_dropped=rej,useful=done,wasted_late=wasted)
for r in (run("unbounded"),run("bounded_reject",160),run("timeout_drop",160)): print(r)
print("arrivals",len(arrivals()),"= 4000 + 4000; capacity over 120 s =",MU*120)
