# Set F Q1: requirements table and TPS (invented inputs)
daily = 20_000_000
avg = daily / 86_400
peak = avg * 6
req = [
 ("daily transactions", daily),
 ("average TPS", round(avg, 1)),
 ("peak/avg ratio", 6),
 ("peak TPS", round(peak, 1)),
 ("p99 model-hop budget ms", 60),
 ("fraud rate", "0.1% (assumed)"),
]
for k, v in req: print(f"{k:28} {v}")
assert round(avg) == 231 and round(peak) == 1389
print("note: Q5 uses 700 TPS peak; that is the book's later figure, not this arithmetic")
