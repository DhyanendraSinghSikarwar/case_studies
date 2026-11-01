import os
import numpy as np, onnxruntime as ort, bentoml

@bentoml.service(traffic={"timeout": 30})
class Iris:
    def __init__(self) -> None:                    # runs once per worker at startup
        self.sess = ort.InferenceSession(os.environ.get("MODEL_PATH", "iris.onnx"), providers=["CPUExecutionProvider"])

    @bentoml.api
    def predict(self, features: list[float]) -> int:
        x = np.array([features], dtype=np.float32)
        return int(self.sess.run(["label"], {"X": x})[0][0])
