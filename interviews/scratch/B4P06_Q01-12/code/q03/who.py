import collections, httpx
c = collections.Counter()
for _ in range(40):
    with httpx.Client() as cl:                       # new connection each time
        c[cl.post("http://127.0.0.1:8103/predict", json=[6.7, 3.0, 5.2, 2.3]).json()["pid"]] += 1
print("distinct worker pids:", len(c), "| answers per pid:", sorted(c.values(), reverse=True))
