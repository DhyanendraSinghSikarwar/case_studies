# Triton Python backend skeleton. Runs inside Triton only (triton_python_backend_utils is provided by the server).
import json
import numpy as np
import triton_python_backend_utils as pb_utils

class TritonPythonModel:
    def initialize(self, args):                       # once per model instance: load vocab, rules, tokenizer
        self.config = json.loads(args["model_config"])

    def execute(self, requests):                      # a LIST of requests (the server may batch them)
        responses = []
        for request in requests:
            raw = pb_utils.get_input_tensor_by_name(request, "RAW").as_numpy()   # shape [batch, 1], bytes
            feats = np.array([[float(v) for v in row[0].decode().split(",")] for row in raw], dtype=np.float32)
            out = pb_utils.Tensor("FEATURES", feats)
            responses.append(pb_utils.InferenceResponse(output_tensors=[out]))
        return responses                              # one response per request, same order

    def finalize(self):                               # on unload: release files, sockets
        pass
