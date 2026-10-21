f='../../Book1_DS_ML/Book1_DS_ML_Part13.md'
t=open(f,encoding='utf-8').read()
reps=[
("The t-test is dominated by outliers (p = 0.31); Mann-Whitney sees the systematic shift in ranks (p = 0.069). Different questions, different answers; decide based on the metric you care about.",
 "The Welch t-test gives p = 0.048 because outliers inflate the variance; Mann-Whitney sees the systematic shift in ranks (p = 0.0074). Different questions, different answers; decide based on the metric you care about."),
("**Example:** Revenue per user is right-skewed (n = 80, mean 29.6). Bootstrap CI for the mean is [23.6, 36.4], matching the analytic SE (3.29 vs 3.36).",
 "**Example:** Revenue per user is right-skewed (n = 80, mean 33.4). Bootstrap CI for the mean is [25.4, 42.9], and the bootstrap SE matches the analytic SE (4.47 vs 4.52)."),
("**Example:** n = 5, true variance 4. Average of divide-by-n estimates is 3.19 (about 4 x 4/5 = 3.2); divide-by-(n-1) averages 3.99. Yet MSE is lower for the biased one (5.8 vs 8.0).",
 "**Example:** n = 5, true variance 4. Average of divide-by-n estimates is 3.19 (about 4 x 4/5 = 3.2); divide-by-(n-1) averages 3.99. Yet MSE is lower for the biased one (5.8 vs 8.0)."),
("# 3.189 3.987  -> bias of ddof=0","# 3.192 3.99  -> bias of ddof=0"),
("# MSE 5.795 vs 8.028","# MSE 5.774 vs 8.002"),
("# 0.5 0.0831 0.0833","# 0.5 0.0836 0.0833"),
("Simulation gives 9.99 vs 10.01 overall.","Simulation gives 10.03 for the extra wait after already waiting 10 min, vs 10.01 overall."),
("Paired p = 0.0003; wrongly using independent gives p = 0.39.","Paired p = 0.000007; wrongly using independent gives p = 0.34."),
("Welch rejects 5.05% as it should.","Welch rejects 4.9% as it should."),
("# pooled 0.001 vs Welch 0.0505","# pooled 0.001 vs Welch 0.049"),
("ANOVA F = 8.18, p = 0.0006; Tukey shows only A vs C differ.","ANOVA F = 7.57, p = 0.0009; Tukey shows only A vs C differ (A vs B p = 0.07, B vs C p = 0.23)."),
]
for a,b in reps:
    assert t.count(a)==1,(a[:50],t.count(a))
    t=t.replace(a,b)
open(f,'w',encoding='utf-8').write(t)
