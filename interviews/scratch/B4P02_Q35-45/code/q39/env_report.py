"""Q39: what a venv+lockfile pins, and what only the host decides. Run: python3 -I env_report.py"""
import os, platform, shutil, sys
from importlib import metadata

print("== pinned by a lockfile (python packages)")
for p in ("numpy", "pyyaml"):
    try: print(f"  {p}=={metadata.version(p)}")
    except metadata.PackageNotFoundError: print(f"  {p}: not installed")

print("== NOT pinned by a lockfile (comes from the machine)")
print("  libc:", " ".join(platform.libc_ver()))
print("  kernel:", platform.release(), "(a container shares the HOST kernel)")
print("  cpu count:", os.cpu_count(), "| arch:", platform.machine())
print("  nvidia-smi on PATH:", bool(shutil.which("nvidia-smi")), "(GPU driver is a host thing, never inside the image)")
print("  nvcc on PATH:", bool(shutil.which("nvcc")))

def choose(team_size, needs_gpu_libs, deploys_to_cluster, mixed_os_laptops):
    """Decision rule used in the answer. Returns a short recommendation."""
    if deploys_to_cluster or (needs_gpu_libs and team_size > 10):
        return "Docker image for deploy and CI; devs may still use venv/conda locally"
    if mixed_os_laptops and needs_gpu_libs:
        return "conda (or Docker dev container) so CUDA libs match; lock it"
    return "venv + lockfile (uv/pip-tools), add Docker only when you deploy"

print("== decision rule examples")
for args in [(3, False, False, False), (3, True, True, False), (3, True, False, True), (30, True, True, True)]:
    print(f"  team={args[0]:>2} gpu_libs={args[1]!s:<5} cluster={args[2]!s:<5} mixed_os={args[3]!s:<5} -> {choose(*args)}")
