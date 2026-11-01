rps=900; cand=400
calls=rps*cand
print("ranking calls/s, 400 cands:",calls)
budget={"feature lookup":15,"retrieval":25,"ranking":55,"re-ranking":15,"overhead":10}
print(budget,"sum",sum(budget.values())); assert sum(budget.values())==120
for name,n in [("two-tower prefilter to 150",150),("smaller set 200",200)]:
    print(name,"calls/s",rps*n,"cut",round(1-n/cand,3))
hit=0.30
print("cache 30% of requests (invented):",int(rps*(1-hit))*cand)
print("combined prefilter 150 + cache 30%:",int(rps*(1-hit))*150)
