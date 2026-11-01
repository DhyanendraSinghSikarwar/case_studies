"""Decision helper for the two classic GPU-in-container failures. Pure logic, runnable anywhere."""
def diagnose(host_driver_ok, toolkit_installed, daemon_has_nvidia_runtime,
             image_cuda, max_cuda_supported_by_driver, torch_built_for_cuda, torch_is_cpu_wheel):
    out = []
    if not host_driver_ok: out.append("Fix host: nvidia-smi fails; install the driver first.")
    if not toolkit_installed: out.append("Install NVIDIA Container Toolkit on the host.")
    elif not daemon_has_nvidia_runtime:
        out.append("could not select device driver 'gpu': run nvidia-ctk runtime configure, restart docker.")
    if torch_is_cpu_wheel: out.append("torch is a CPU wheel: is_available() is False even with a working GPU.")
    if torch_built_for_cuda and torch_built_for_cuda > max_cuda_supported_by_driver:
        out.append(f"Wheel needs CUDA {torch_built_for_cuda} but driver supports up to {max_cuda_supported_by_driver}: upgrade driver or use older wheel.")
    if image_cuda and image_cuda > max_cuda_supported_by_driver:
        out.append(f"Image CUDA {image_cuda} newer than driver ({max_cuda_supported_by_driver}): too new; use older image.")
    return out or ["No issue found by these rules; check NVIDIA_DRIVER_CAPABILITIES and run with --gpus."]

cases = {
 "A could-not-select-device-driver": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=False, image_cuda=12.4, max_cuda_supported_by_driver=12.6, torch_built_for_cuda=12.4, torch_is_cpu_wheel=False),
 "B smi ok, torch False (cpu wheel)": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=True, image_cuda=None, max_cuda_supported_by_driver=12.6, torch_built_for_cuda=None, torch_is_cpu_wheel=True),
 "C wheel newer than driver": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=True, image_cuda=None, max_cuda_supported_by_driver=11.8, torch_built_for_cuda=12.4, torch_is_cpu_wheel=False),
 "D image older than driver (fine)": dict(host_driver_ok=True, toolkit_installed=True, daemon_has_nvidia_runtime=True, image_cuda=11.8, max_cuda_supported_by_driver=12.6, torch_built_for_cuda=11.8, torch_is_cpu_wheel=False),
}
for name, kw in cases.items():
    print(name); [print("  -", m) for m in diagnose(**kw)]
