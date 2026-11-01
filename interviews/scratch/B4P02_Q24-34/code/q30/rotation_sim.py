"""Tiny model of the json-file driver rotation (max-size, max-file). Not Docker's code."""
import os, tempfile

d = tempfile.mkdtemp(); base = os.path.join(d, "c-json.log")
MAX_SIZE, MAX_FILE = 1000, 3                     # bytes, files
def write(line):
    if os.path.exists(base) and os.path.getsize(base) + len(line) > MAX_SIZE:
        for i in range(MAX_FILE - 1, 0, -1):     # .2 dropped, .1 -> .2, current -> .1
            src = base if i == 1 else f"{base}.{i-1}"
            if os.path.exists(src): os.replace(src, f"{base}.{i}")
    with open(base, "a") as f: f.write(line)
for n in range(200): write(f"step {n:04d} loss=0.123456 acc=0.9876\n")
total = sum(os.path.getsize(os.path.join(d, x)) for x in os.listdir(d))
print("files:", sorted(os.listdir(d)))
print("bytes written: ~", 200 * len("step 0000 loss=0.123456 acc=0.9876\n"), " bytes kept on disk:", total, " (cap = %d)" % (MAX_SIZE * MAX_FILE))
