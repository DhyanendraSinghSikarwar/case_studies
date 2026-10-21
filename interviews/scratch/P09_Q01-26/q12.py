import numpy as np
# detections for one class sorted by confidence: (score, is_TP at IoU>=0.5); 4 ground truths
dets=[(0.95,1),(0.9,1),(0.8,0),(0.7,1),(0.6,0),(0.5,1)]
n_gt=5
tp=np.cumsum([d[1] for d in dets]); fp=np.cumsum([1-d[1] for d in dets])
prec=tp/(tp+fp); rec=tp/n_gt
print(np.round(prec,2),np.round(rec,2))
# all-point interpolated AP
mrec=np.r_[0,rec,1]; mpre=np.r_[0,prec,0]
for i in range(len(mpre)-2,-1,-1): mpre[i]=max(mpre[i],mpre[i+1])
idx=np.where(mrec[1:]!=mrec[:-1])[0]
print("AP@0.5 =",round(float(np.sum((mrec[idx+1]-mrec[idx])*mpre[idx+1])),3))
