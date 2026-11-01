# Illustrative bridge from 4.2M (finance) to 3.6M (product), millions.
fin, prod = 4.2, 3.6
gap = fin - prod
print(f"gap {gap:.1f}M = {gap/fin:.1%} of finance, {gap/prod:.1%} of product")
assert round(gap, 1) == 0.6 and round(gap / fin, 3) == 0.143 and round(gap / prod, 3) == 0.167
# Invented bridge: finance = any login in 30 days incl. bots; product = >=1 meaningful action, bots excluded.
bridge = [("bots and automated traffic", 0.25), ("login only, no meaningful action", 0.30), ("test and internal accounts", 0.05)]
run = fin
for name, v in bridge:
    run = round(run - v, 2)
    print(f"{name:36} -{v:.2f}  -> {run:.2f}")
assert run == prod and round(sum(v for _, v in bridge), 2) == round(gap, 2)
# Which number for which job (illustrative rule)
print("billing/seats -> finance definition; engagement -> product definition; both labelled with names")
# Cost of ambiguity: if growth is 5% on each series the absolute change differs
print("5% growth:", round(fin * 0.05, 2), "vs", round(prod * 0.05, 2), "million users")
assert round(fin * .05, 2) == 0.21 and round(prod * .05, 2) == 0.18
