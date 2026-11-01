rates0 = [0.40, 0.55, 0.70, 0.80]
names = ["visit>signup", "signup>KYC", "KYC>approval", "approval>disbursal"]
def run(visits, rates):
    c = [visits]
    for r in rates: c.append(c[-1] * r)
    return c
base = run(1_000_000, rates0)
print("last month counts:", [round(x) for x in base])
overall = 1
for r in rates0: overall *= r
print(f"overall visit>disbursal {overall:.2%}")
assert round(overall, 4) == 0.1232 and round(base[-1]) == 123_200
scen = {
 "A: traffic -10%, all rates same":      run(900_000, rates0),
 "B: KYC>approval 70% -> 63%":           run(1_000_000, [0.40, 0.55, 0.63, 0.80]),
 "C: cheap traffic +25%, signup 28.8%":  run(1_250_000, [0.288, 0.55, 0.70, 0.80]),
}
for k, c in scen.items():
    r = [c[i + 1] / c[i] for i in range(4)]
    print(k)
    print("   counts:", [round(x) for x in c], f"disbursal {c[-1] / base[-1] - 1:+.1%}")
    print("   rates :", [f"{x:.1%}" for x in r])
    assert round(c[-1]) == 110_880
