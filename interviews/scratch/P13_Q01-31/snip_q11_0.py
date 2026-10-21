from statsmodels.stats.power import TTestIndPower
p = TTestIndPower()
for d in (0.2, 0.5):
    print(d, round(p.power(d, 50, 0.05), 3), round(p.solve_power(d, power=0.8, alpha=0.05)))
# 0.2 -> power 0.168, n needed 393 ; 0.5 -> power 0.697, n needed 64
print(round(p.power(0.5, 100, 0.05), 3), round(p.power(0.5, 50, 0.01), 3))  # 0.94 (more n), 0.453 (lower alpha)
