"""Run INSIDE the container on a GPU host. Not executable in this sandbox (no GPU, no torch)."""
import torch
print("torch", torch.__version__, "built for CUDA", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device:", torch.cuda.get_device_name(0))
    x = torch.randn(1024, 1024, device="cuda")
    print("matmul ok:", (x @ x).shape)
