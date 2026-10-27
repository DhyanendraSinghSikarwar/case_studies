# abstract cost units, invented usage
bill = {"compute":1000,"storage":300,"shared_cluster":400,"registry":50,"feature_store":150,"untagged":100}
direct = {  # tagged direct cost per team
 "fraud":{"compute":380,"storage":90},
 "reco":{"compute":330,"storage":120},
 "forecast":{"compute":120,"storage":50},
 "credit":{"compute":110,"storage":30},
}
usage = {"fraud":40,"reco":35,"forecast":15,"credit":10}   # share of cluster-hours
fs_use = {"fraud":50,"reco":30,"forecast":10,"credit":10}
pool_cluster=bill["shared_cluster"]; pool_reg=bill["registry"]; pool_fs=bill["feature_store"]
tagged_direct=sum(sum(v.values()) for v in direct.values())
untagged=bill["compute"]+bill["storage"]-tagged_direct+bill["untagged"]
print("tagged direct",tagged_direct,"untagged residue",untagged)
out={}
for t in direct:
    d=sum(direct[t].values())
    c=pool_cluster*usage[t]/sum(usage.values())
    r=pool_reg/len(direct)                      # fixed even split
    f=pool_fs*fs_use[t]/sum(fs_use.values())
    # untagged residue spread in proportion to direct cost
    u=untagged*d/tagged_direct
    out[t]=d+c+r+f+u
    print(f"{t:9} direct {d:5} cluster {c:6.1f} registry {r:5.1f} fs {f:6.1f} untagged {u:6.1f} total {out[t]:7.1f}")
total=sum(bill.values())
print("sum",round(sum(out.values()),6),"bill",total)
assert abs(sum(out.values())-total)<1e-9
