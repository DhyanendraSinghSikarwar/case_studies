import json, numpy as np, tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException
URL = "localhost:8221"
c = httpclient.InferenceServerClient(url=URL)
x = np.array([[6.7, 3.0, 5.2, 2.3], [5.1, 3.5, 1.4, 0.2]], dtype=np.float32)
inp = httpclient.InferInput("X", list(x.shape), "FP32")
inp.set_data_from_numpy(x, binary_data=False)                 # JSON data; binary_data=True is the fast path on real Triton
print("input tensor JSON the client builds:", json.dumps(inp._get_tensor()))   # _get_tensor is a private helper, for display only
print("live:", c.is_server_live(), " ready:", c.is_server_ready(), " model ready:", c.is_model_ready("iris_onnx"))
print("metadata inputs:", c.get_model_metadata("iris_onnx")["inputs"])
r = c.infer("iris_onnx", [inp], outputs=[httpclient.InferRequestedOutput("label", binary_data=False),
                                          httpclient.InferRequestedOutput("probabilities", binary_data=False)])
print("label:", r.as_numpy("label"), " probabilities shape:", r.as_numpy("probabilities").shape)
bad = httpclient.InferInput("X", [1, 3], "FP32"); bad.set_data_from_numpy(np.zeros((1, 3), np.float32), binary_data=False)
try: c.infer("iris_onnx", [bad])
except InferenceServerException as e: print("wrong shape ->", e)
