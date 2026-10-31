# 16 GPUs, 24h window, invented job log: (kind, gpus_held, hours_held, busy_fraction)
jobs=[("notebook",1,24,0.05),("notebook",1,24,0.08),("notebook",1,24,0.04),("notebook",2,24,0.10),
 ("notebook",1,20,0.06),("train",4,10,0.85),("train",2,8,0.70),("train",1,6,0.35),
 ("tune",1,3,0.90),("tune",1,3,0.88),("tune",1,3,0.90),("tune",1,3,0.86),("infer",1,24,0.30),("infer",1,24,0.25)]
cap=16*24
held=sum(g*h for _,g,h,_ in jobs); busy=sum(g*h*b for _,g,h,b in jobs)
print("capacity GPU-h",cap,"held",held,"held share",round(held/cap,3),"busy GPU-h",round(busy,1),"avg util of capacity",round(busy/cap,3))
# lease policy: notebooks get 4h lease unless renewed with activity; idle (<10% busy) notebooks reclaimed after 2h idle grace
LEASE=4
new_held=0; reclaim=0
for k,g,h,b in jobs:
    if k=="notebook" and b<0.10:
        keep=min(h,LEASE); reclaim+=g*(h-keep); new_held+=g*keep
    else: new_held+=g*h
print("reclaimable GPU-h",reclaim,"share of capacity",round(reclaim/cap,3))
print("held after policy",new_held,"free GPU-h now",cap-new_held)
print("busy GPU-h unchanged",round(busy,1),"util of HELD hours before",round(busy/held,3),"after",round(busy/new_held,3))
print("util of capacity unchanged:",round(busy/cap,3),"- the win is freed capacity for waiting jobs, not a higher percentage")
# if queue absorbs freed hours with jobs at 80% busy (invented)
extra=reclaim*0.8
print("if queued jobs use the freed hours at 80% busy: util of capacity",round((busy+extra)/cap,3))
assert reclaim<=held
