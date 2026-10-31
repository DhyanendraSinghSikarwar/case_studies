# Prompt arithmetic: bits to bytes
kbps, seconds = 400, 3
kbit = kbps * seconds
kB = kbit / 8
assert kbit == 1200 and kB == 150
print("kilobits in 3 s:", kbit, "| ceiling payload (kB):", kB)

# That ceiling ignores latency, handshakes and slow phases; show how fast it shrinks
for overhead_s in (0.0, 0.5, 1.0):
    avail = seconds - overhead_s
    print(f"with {overhead_s} s of fixed overhead -> payload ceiling {kbps * avail / 8:.0f} kB")
assert kbps * (3 - 1.0) / 8 == 100
# If the typical session gets only half the nominal rate (assumed), the ceiling halves
assert kB / 2 == 75

# Illustrative payload budget for a home screen (kB), compared with the ceiling at 1 s overhead and half rate
budget = {"layout + app shell (cached after first load)": 0, "feed ids and scores for 20 items": 1.0,
          "20 item cards, text only, compressed": 14.0, "20 thumbnails at 3 kB each": 60.0}
uncached = sum(budget.values())
print("illustrative uncached payload kB:", uncached, "| fits 75 kB ceiling:", uncached <= 75)
assert uncached == 75.0

# Image shrink options (assumed starting sizes): 20 images of 30 kB each
imgs, start = 20, 30
raw = imgs * start
print("uncompressed-size images kB:", raw, "| at 10 kB each:", imgs * 10, "| only 6 above-the-fold images at 10 kB:", 6 * 10)
assert raw == 600 and raw / 150 == 4.0
assert imgs * 10 == 200 > 150 and 6 * 10 == 60 < 75
# Time to download 75 kB at 400 and at 200 kbps
for r in (400, 200):
    print(f"75 kB at {r} kbps takes {75 * 8 / r:.2f} s")
assert 75 * 8 / 400 == 1.5 and 75 * 8 / 200 == 3.0
assert 10 * 8 / 400 == 0.2
print("each extra 10 kB costs seconds at 400 kbps:", 10 * 8 / 400)
