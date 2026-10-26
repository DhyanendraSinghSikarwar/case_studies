import sys, time, numpy as np, onnxruntime as ort
so = ort.SessionOptions(); so.intra_op_num_threads = 1
s = ort.InferenceSession(sys.argv[1], so, providers=["CPUExecutionProvider"])
x = np.random.default_rng(0).standard_normal((32, 512)).astype(np.float32)
def best(f, n=20):
    f(); ts = []
    for _ in range(n):
        t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
    return min(ts) * 1000
one = best(lambda: [s.run(None, {"x": x[i:i+1]}) for i in range(32)])
bat = best(lambda: s.run(None, {"x": x}))
print(f"32 rows as 32 calls of batch 1: {one:6.1f} ms | one call of batch 32: {bat:6.1f} ms | ratio {one/bat:.1f}x (this sandbox only)")
