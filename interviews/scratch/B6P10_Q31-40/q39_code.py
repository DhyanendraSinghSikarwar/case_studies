accounts, deg, pps = 30_000_000, 12, 5000
one_hop = deg
two_hop_exact = deg * deg
within_two = one_hop + two_hop_exact
print("one-hop", one_hop, "exactly two-hop", two_hop_exact, "within two hops", within_two)
assert two_hop_exact == 144 and within_two == 156
lookups_within = pps * within_two
lookups_exact = pps * two_hop_exact
print("profile lookups/s (156 per payment)", lookups_within, "(144 per payment)", lookups_exact)
assert lookups_within == 780_000 and lookups_exact == 720_000
# adjacency-list reads to discover the two-hop set: 1 (sender) + 12 (each neighbour)
adj = pps * (1 + deg)
print("adjacency reads/s", adj)
assert adj == 65_000
# precomputed alternative: 1 vector read for the sender (and 1 for the receiver)
pre = pps * 2
print("precomputed reads/s", pre, "reduction vs 780,000:", lookups_within / pre)
assert pre == 10_000 and lookups_within / pre == 78.0
# edge storage: 30M * 12 outgoing edges, 8-byte ids (undirected counted both ways is the same count here)
edges = accounts * deg
print("edge entries", edges, "GB at 8 B each", edges * 8 / 1e9)
assert edges == 360_000_000 and edges * 8 == 2_880_000_000
# embedding table: 64 floats of 4 B per account
emb = accounts * 64 * 4
print("embedding table GB", emb / 1e9)
assert emb == 7_680_000_000
# overlap is real: with 12 neighbours of which some share neighbours, the true two-hop set is smaller
# but hub accounts (degree 100,000) explode the other way; cap fan-out
cap = 50
print("capped fan-out two hops", cap * cap, "per payment at 5,000/s:", pps * cap * cap)
assert pps * cap * cap == 12_500_000
