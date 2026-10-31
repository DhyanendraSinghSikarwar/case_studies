queries = 20_000
price = 3.0                                        # illustrative, per million input tokens
stuff, rag = 100_000, 6_000
cost = lambda tok: tok * queries * price / 1e6
c_stuff, c_rag = cost(stuff), cost(rag)
print(f"stuffing: {stuff*queries/1e9:.1f} billion tokens/day -> {c_stuff:,.0f} per day")
print(f"retrieval: {rag*queries/1e6:.0f} million tokens/day -> {c_rag:,.0f} per day")
assert c_stuff == 6000 and c_rag == 360
print(f"ratio {c_stuff/c_rag:.1f}x, gap {c_stuff-c_rag:,.0f} per day = {(c_stuff-c_rag)*365:,.0f} per year")
assert round(c_stuff / c_rag, 1) == 16.7 and (c_stuff - c_rag) * 365 == 2_058_600
# If the 100k set is identical every call and cached reads cost 10% of the input rate (invented).
c_cached = cost(stuff) * 0.10
print(f"stuffing with 100% cached prefix at 10% rate: {c_cached:,.0f} per day (still above retrieval {c_rag:,.0f})")
assert c_cached == 600 and c_cached > c_rag
# Break-even: what retrieval pipeline overhead per day would erase the saving?
print(f"retrieval overhead (embedding, vector DB, reranker) would need to exceed {c_stuff-c_rag:,.0f} per day to lose")
