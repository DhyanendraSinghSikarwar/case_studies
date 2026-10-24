import hashlib
BLOCK = 4
def block_keys(tokens):
    keys, prev = [], ""
    for i in range(0, len(tokens) - len(tokens) % BLOCK, BLOCK):   # full blocks only
        prev = hashlib.sha1((prev + str(tokens[i:i+BLOCK])).encode()).hexdigest()[:8]  # key depends on ALL earlier tokens
        keys.append(prev)
    return keys
cache = set()
def run(name, tokens):
    ks = block_keys(tokens); hit = 0
    for k in ks:
        if k in cache: hit += 1
        else: break
    cache.update(ks)
    print(f"{name}: {len(tokens)} tokens, reused {hit*BLOCK} from cache, prefill {len(tokens)-hit*BLOCK}")
system = list(range(100, 112))                        # 12 shared tokens (system prompt + docs)
run("req1", system + [1, 2, 3])
run("req2", system + [7, 8, 9, 10, 11])               # same prefix, new question -> hit
run("req3", [999] + system + [1, 2, 3])               # one token added at the FRONT -> miss
