import re
f='../../Book1_DS_ML/Book1_DS_ML_Part13.md'
t=open(f,encoding='utf-8').read()
reps=[
("print(rejection_rate(0.0))   # ~0.052 -> Type I rate (alpha)\npw = rejection_rate(0.5)     # ~0.71  -> power; beta = 1 - pw ~ 0.29\nprint(pw, 1 - pw)",
 "print(rejection_rate(0.0))   # 0.049 -> Type I rate (alpha)\npw = rejection_rate(0.5)     # power; beta = 1 - pw\nprint(pw, 1 - pw)             # 0.7035 0.2965"),
("print(round(sd, 2), round(se, 2), round(stats.sem(x), 2))  # 16.64 0.83 0.83","print(round(sd, 2), round(se, 2), round(stats.sem(x), 2))  # 14.95 0.75 0.75"),
("**Example:** Exponential data has skew 2.0. Means of n = 2 samples are still skewed (1.48); n = 30 gives 0.37; n = 500 gives 0.06, and the SD of the mean tracks 1/sqrt(n).",
 "**Example:** Exponential data has skew 2.0. Means of n = 2 samples are still skewed (1.43); n = 30 gives 0.36; n = 500 gives 0.11, and the SD of the mean tracks 1/sqrt(n)."),
("print(\"pop skew\", round(stats.skew(pop), 2))                     # 2.0","print(\"pop skew\", round(stats.skew(pop), 2))                     # 2.01"),
("# 2 1.48 0.704 0.707 | 30 0.37 0.18 0.183 | 500 0.06 0.045 0.045","# n, skew of mean, SD of mean, 1/sqrt(n):  2 1.43 0.707 0.707 | 30 0.36 0.185 0.183 | 500 0.11 0.045 0.045"),
("print(hits / 10000)    # 0.9464 -> about 95% of intervals cover the truth","print(hits / 10000)    # 0.95 -> about 95% of intervals cover the truth"),
("Output from my run: 0.0195, 0.0098, 0.9902.","Output from my run: 0.0205, 0.0103, 0.9897."),
("**Example:** Height (cm) vs weight (kg): covariance 47.7, correlation 0.71. Change height to metres: covariance 0.477, correlation still 0.71.",
 "**Example:** Height (cm) vs weight (kg): covariance 51.7, correlation 0.74. Change height to metres: covariance 0.517, correlation still 0.74."),
("# 47.7  0.707","# 51.72  0.736"),("# 0.477 0.707","# 0.517 0.736"),
("print(stats.shapiro(x).pvalue.round(3))                          # 0.697 -> consistent with normal","print(stats.shapiro(x).pvalue.round(3))                          # 0.757 -> consistent with normal"),
("print(stats.probplot(x, dist='norm')[1][2].round(4))             # Q-Q straightness r = 0.998","print(stats.probplot(x, dist='norm')[1][2].round(4))             # Q-Q straightness r = 0.9981"),
("**Example:** Average basket value of 20 customers is 52 vs. claimed 50, s = 10. t = 0.50, p = 0.62, no evidence of difference.",
 "**Example:** 20 baskets sampled, claimed average Rs 50, sample SD about 10, sample mean very close to 50. t = 0.09, p = 0.93: no evidence the claim is wrong."),
("print(round(t, 3), round(2 * stats.t.sf(abs(t), 19), 4))   # 0.499 0.6238","print(round(t, 3), round(2 * stats.t.sf(abs(t), 19), 4))   # 0.086 0.9322"),
("p = 4e-8, but d = 0.017 and the CI is [0.22, 0.47] rupees.","p = 9e-10, but d = 0.019 and the CI is [0.26, 0.51] rupees."),
("**Example:** Avg order value Rs 100.0 vs Rs 100.35 with 200,000 users per arm:","**Example:** Avg order value Rs 100.0 vs Rs 100.39 with 200,000 users per arm:"),
("# 4.4e-08  0.017  0.346  [0.222 0.47]","# 8.5e-10  0.019  0.387  [0.264 0.511]"),
]
for a,b in reps:
    assert t.count(a)==1,(a[:50],t.count(a))
    t=t.replace(a,b)
open(f,'w',encoding='utf-8').write(t)
