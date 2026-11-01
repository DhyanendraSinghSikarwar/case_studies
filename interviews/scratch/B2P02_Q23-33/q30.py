def ngrams(t, n):
    w = t.lower().split(); return {" ".join(w[i:i+n]) for i in range(len(w)-n+1)}
bench = "what is the capital of france and which river flows through its capital city paris"
docs = {"leak": "quiz dump: what is the capital of france and which river flows through its capital city paris answer seine",
        "para": "name the capital of france and the river that runs through paris",
        "clean": "gradient descent updates parameters in the direction of the negative gradient of the loss"}
for n in (13, 5):
    b = ngrams(bench, n)
    for name, d in docs.items():
        print(f"n={n} {name}: overlap {len(b & ngrams(d, n))}/{len(b)}")
