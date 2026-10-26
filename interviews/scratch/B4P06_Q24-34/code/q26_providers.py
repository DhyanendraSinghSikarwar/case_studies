# Q26: pick an ONNX Runtime provider with a CPU fallback.
import sys, onnxruntime as ort
def pick_providers():
    avail = ort.get_available_providers()
    wanted = ["CUDAExecutionProvider", "CPUExecutionProvider"]   # order = priority
    return [p for p in wanted if p in avail]
print("onnxruntime", ort.__version__)
print("available:", ort.get_available_providers())
print("device:", ort.get_device())
chosen = pick_providers()
print("chosen:", chosen)
sess = ort.InferenceSession(sys.argv[1], providers=chosen)
print("session is using:", sess.get_providers())
try:
    s2 = ort.InferenceSession(sys.argv[1], providers=["CUDAExecutionProvider"])
    print("asked for CUDA only, session loaded anyway; it is really using:", s2.get_providers())
except Exception as e:
    print("CUDA only ->", type(e).__name__, str(e)[:160].replace("\n"," "))
