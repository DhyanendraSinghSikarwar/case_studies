import base64, json
import numpy as np
rng = np.random.default_rng(0)
img = rng.random((1, 3, 224, 224), dtype=np.float32)            # normalised pixels in [0, 1)
n = img.size
raw = img.tobytes()
json_nested = json.dumps({"inputs": [{"name": "x", "shape": list(img.shape), "datatype": "FP32",
                                       "data": img.reshape(-1).tolist()}]})   # KServe v2 REST style (shape of the idea)
json_b64 = json.dumps({"shape": list(img.shape), "datatype": "FP32", "b64": base64.b64encode(raw).decode()})
print(f"elements: {n}")
print(f"packed float32 buffer (what a protobuf bytes field carries): {len(raw):>9,} bytes  ({len(raw)/n:.1f} B/element)")
print(f"JSON list of floats (python repr, float64 text)           : {len(json_nested):>9,} bytes  ({len(json_nested)/n:.1f} B/element)")
print(f"JSON with base64 of the float32 buffer                    : {len(json_b64):>9,} bytes  ({len(json_b64)/n:.1f} B/element)")
print(f"ratio JSON-list / packed: {len(json_nested)/len(raw):.2f}x ; base64 / packed: {len(json_b64)/len(raw):.2f}x")
small = np.float32([0.5, 0.25]).tobytes(); print("2 floats packed:", len(small), "bytes -> JSON '[0.5, 0.25]':", len(json.dumps([0.5, 0.25])), "bytes")
print("sample of the JSON body:", json_nested[:110], "...")
