# Q41: 3-year relative TCO, invented units; sensitivity to team size.
def tco(kind, team, models, years=3):
    p = dict(
     build  =dict(upfront=6*team,  run_infra=10+0.05*models, license=0,  eng_per_year=lambda t: t*1.0, oncall=4),
     managed=dict(upfront=2*team,  run_infra=16+0.30*models, license=0,  eng_per_year=lambda t: t*0.5, oncall=1.5),
     buy    =dict(upfront=1.5*team,run_infra=12+0.10*models, license=14+0.30*models, eng_per_year=lambda t: t*0.4, oncall=1.5))[kind]
    per_year = p["run_infra"] + p["license"] + p["eng_per_year"](team) + p["oncall"]
    return p["upfront"] + years * per_year
for models in [20, 100, 400]:
    print(f"--- {models} models in production")
    print(f"{'team':>5s}{'build':>8s}{'managed':>9s}{'buy':>7s}  cheapest")
    for team in [4, 8, 16]:
        r = {k: tco(k, team, models) for k in ("build", "managed", "buy")}
        print(f"{team:>5d}{r['build']:8.1f}{r['managed']:9.1f}{r['buy']:7.1f}  {min(r, key=r.get)}")
# lock-in: exit cost as a share of year-3 run cost
print("exit-cost units: build 0, managed 12, buy 18  (invented; re-platforming effort)")
print("criterion that flips: if compliance forbids the managed service region, managed drops out")
