loss=2_000_000; years=3
vendor_cost=[300_000]*3
inh_cost=[500_000,150_000,150_000]
vendor_prev=0.70; inh_prev=0.76
v_ben=vendor_prev*loss; i_ben=inh_prev*loss
assert v_ben==1_400_000 and i_ben==1_520_000
v_net=sum(v_ben-c for c in vendor_cost)
i_net=sum(i_ben-c for c in inh_cost)
print("vendor 3-yr net:",v_net)
print("in-house 3-yr net:",i_net)
print("difference (in-house minus vendor):",i_net-v_net)
assert v_net==3_300_000 and i_net==3_760_000 and i_net-v_net==460_000

# in-house prevention rate at which it only ties vendor
tie=(v_net+sum(inh_cost))/(loss*years)
print(f"break-even in-house prevention rate: {tie:.4f}")
assert abs(tie-0.683333)<1e-5 and tie<vendor_prev

print("\nOptimism checks (illustrative)")
# a) year-1 delay: in-house model live for only 6 months of year 1
i_delay=i_net-0.5*i_ben
print("  in-house net if year 1 is half-live:",i_delay, "diff:",i_delay-v_net)
assert i_delay==3_000_000 and i_delay-v_net==-300_000
# b) prevention falls to 70% (same as vendor)
i_70=sum(0.70*loss-c for c in inh_cost)
print("  in-house net at 70% prevention:",i_70,"diff:",i_70-v_net)
assert abs(i_70-3_400_000)<1e-6 and abs(i_70-v_net-100_000)<1e-6
# c) a 1 percentage point prevention change is worth this over 3 years
print("  value of 1 prevention point over 3 years:",0.01*loss*years)
assert 0.01*loss*years==60_000
# d) maintenance cost doubles after year 1
i_m=sum(i_ben-c for c in [500_000,300_000,300_000])
print("  in-house net if run cost is 300k/yr after year 1:",i_m,"diff:",i_m-v_net)
assert i_m==3_460_000
print("  lead as share of vendor net:",round(460_000/v_net,3),"; points of prevention to erase lead:",round(460_000/60_000,2))
assert round(460_000/v_net,2)==0.14 and round(460_000/60_000,1)==7.7
