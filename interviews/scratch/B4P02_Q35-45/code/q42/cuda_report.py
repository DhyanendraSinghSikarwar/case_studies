"""Q42: print every version that matters; interpret what is missing. Run: python3 -I cuda_report.py"""
import re, shutil, subprocess

def sh(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout
    except Exception as e:
        return ""

def parse_smi(text):
    m = re.search(r"Driver Version:\s*([\d.]+).*?CUDA Version:\s*([\d.]+)", text)
    return m.groups() if m else None

def parse_nvcc(text):
    m = re.search(r"release\s+([\d.]+)", text)
    return m.group(1) if m else None

def ver(s): return tuple(int(x) for x in s.split("."))

def verdict(driver_max_cuda, runtime_cuda):
    """A CUDA runtime in the image works if the driver's max supported CUDA is >= it
    (simple rule; minor-version compatibility and forward-compat packages exist, check NVIDIA docs)."""
    return "ok" if ver(driver_max_cuda) >= ver(runtime_cuda) else "driver too old for this image"

print("== this machine")
smi = shutil.which("nvidia-smi")
print("nvidia-smi:", parse_smi(sh([smi])) if smi else "not found (no NVIDIA driver here)")
nvcc = shutil.which("nvcc")
print("nvcc:", parse_nvcc(sh([nvcc, "--version"])) if nvcc else "not found (no CUDA toolkit here)")
try:
    import torch
    print("torch:", torch.__version__, "| torch.version.cuda:", torch.version.cuda,
          "| is_available:", torch.cuda.is_available())
except ImportError:
    print("torch: not installed in this sandbox (so no torch.version.cuda to read)")

print("== the question from the interview, with pasted sample text (not from this machine)")
sample_smi = "| NVIDIA-SMI 550.54   Driver Version: 550.54   CUDA Version: 12.4 |"
sample_nvcc = "Cuda compilation tools, release 11.8, V11.8.89"
d, c = parse_smi(sample_smi); t = parse_nvcc(sample_nvcc)
print(f"nvidia-smi says CUDA {c} (driver {d}); nvcc says {t}")
print(f"driver supports up to {c}; toolkit {t} is what compiled code used -> {verdict(c, t)}")
print("== image/driver checks")
for drv_max, img in [("12.4", "11.8"), ("12.4", "12.4"), ("11.8", "12.4")]:
    print(f"driver max CUDA {drv_max}, image CUDA {img}: {verdict(drv_max, img)}")
