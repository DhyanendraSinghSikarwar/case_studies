dau=20e6; req_per_user=30; peak=3
avg_qps=dau*req_per_user/86400; peak_qps=avg_qps*peak
print(round(avg_qps), round(peak_qps))
cands=500; feat_bytes=200
print("MB/s of features at peak:", round(peak_qps*cands*feat_bytes/1e6))
events=5e9/ 30; row=100
print("GB/day logs:", round(1e9*row/1e9), "TB/yr:", round(1e9*row*365/1e12,1))
