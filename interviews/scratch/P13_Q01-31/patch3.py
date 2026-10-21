f='../../Book1_DS_ML/Book1_DS_ML_Part13.md'
t=open(f,encoding='utf-8').read()
reps=[
("the t-test still rejects about 5% of the time (0.05), so it is robust here. But Shapiro-Wilk on the same kind of data gives p ~ 1e-14.",
 "the t-test still rejects about 5% of the time (0.0465 in my run), so it is robust here. But Shapiro-Wilk on the same kind of data gives p ~ 6e-14."),
("Both with 5,000 rows: D = 0.126, p ~ 4e-35 -> alert. Check against N(0,1): D = 0.007, p = 0.95 -> same distribution.",
 "Both with 5,000 rows: D = 0.134, p ~ 9e-40 -> alert. Reference sample checked against N(0,1): D = 0.009, p = 0.76 -> consistent."),
("SD of the estimate is 1.28 with simple random sampling vs 0.28 with proportional stratification.","SD of the estimate is 1.23 with simple random sampling vs 0.29 with proportional stratification."),
("# 1.279 vs 0.279; truth 21.04","# 1.234 vs 0.289; truth 21.04"),
("Pearson 0.887, Spearman 0.997, Kendall 0.971. Add one extreme outlier and Pearson collapses to 0.58 while Spearman stays 0.97.",
 "Pearson 0.876, Spearman 0.997, Kendall 0.969. Add one extreme outlier and Pearson collapses to 0.58 while Spearman stays 0.97."),
]
for a,b in reps:
    assert t.count(a)==1,(a[:50],t.count(a))
    t=t.replace(a,b)
open(f,'w',encoding='utf-8').write(t)
