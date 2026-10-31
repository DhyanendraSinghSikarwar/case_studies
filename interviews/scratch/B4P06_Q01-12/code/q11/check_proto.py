# usage: python -m grpc_tools.protoc -I. --python_out=OUT infer.proto ; python -I check_proto.py OUT
import sys; sys.path.insert(0, sys.argv[1])
import numpy as np, infer_pb2
x = np.zeros((1, 3, 224, 224), np.float32)
m = infer_pb2.InferRequest(model_name="resnet", model_version="3", shape=list(x.shape), datatype="FP32", raw_data=x.tobytes())
b = m.SerializeToString()
print("serialized InferRequest bytes:", len(b), "= raw", len(x.tobytes()), "+ overhead", len(b) - len(x.tobytes()))
print("round trip shape:", list(infer_pb2.InferRequest.FromString(b).shape))
