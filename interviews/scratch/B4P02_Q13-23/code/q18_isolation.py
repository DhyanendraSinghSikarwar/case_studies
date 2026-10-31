# Q18: look at the kernel features containers are built from: namespaces, cgroups, shared kernel. Read-only; no Docker.
import os, platform, subprocess
print("kernel (shared with every container on this host):", platform.release())
print("namespaces of this process:")
for ns in sorted(os.listdir("/proc/self/ns")):
    print(f"  {ns:18} {os.readlink('/proc/self/ns/' + ns)}")
print("cgroup membership:", open("/proc/self/cgroup").read().strip() or "(none)")
for f in ("memory.max", "cpu.max", "pids.max"):
    p = "/sys/fs/cgroup/" + f
    print(f"  {f:11}", open(p).read().strip() if os.path.exists(p) else "not present here")
# a new PID namespace: the child sees itself as PID 1 (needs root or user namespaces)
r = subprocess.run(["unshare", "--pid", "--fork", "--mount-proc", "python3", "-I", "-c", "import os; print('in new pid ns, my pid =', os.getpid())"],
                   capture_output=True, text=True)
print((r.stdout or r.stderr).strip())
print("host pid of this script:", os.getpid())
