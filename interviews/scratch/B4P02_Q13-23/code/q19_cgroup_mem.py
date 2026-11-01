# Q19: read cgroup memory limit/usage (v2 or v1), /dev/shm size, and show why a SIGKILL exit looks like 137.
import os, subprocess, signal, sys

def rd(p):
    try: return open(p).read().strip()
    except OSError: return None

def mem():
    v2 = rd("/sys/fs/cgroup/memory.max")
    if v2 is not None:
        return "cgroup v2", v2, rd("/sys/fs/cgroup/memory.current"), (rd("/sys/fs/cgroup/memory.events") or "").replace("\n", "; ")
    v1 = rd("/sys/fs/cgroup/memory/memory.limit_in_bytes")
    if v1 is not None:
        return "cgroup v1", v1, rd("/sys/fs/cgroup/memory/memory.usage_in_bytes"), None
    return None

m = mem()
if not m: print("no cgroup memory files visible")
else:
    ver, lim, cur, ev = m
    unlimited = lim == "max" or (lim.isdigit() and int(lim) > 1 << 60)
    print(f"{ver}: limit={'UNLIMITED' if unlimited else str(int(lim)//2**20) + ' MiB'}, current={int(cur)//2**20 if cur else '?'} MiB, events={ev}")
st = os.statvfs("/dev/shm"); print(f"/dev/shm size: {st.f_blocks * st.f_frsize // 2**20} MiB (Docker default for a container is 64 MiB)")
print("host-visible RAM from /proc/meminfo (what many libs wrongly trust):", int(open('/proc/meminfo').readline().split()[1])//1024, "MiB")

# exit 137 = 128 + 9: the process was killed by SIGKILL (the OOM killer sends it, so does docker kill)
p = subprocess.Popen([sys.executable, "-I", "-c", "import time; time.sleep(30)"]); p.send_signal(signal.SIGKILL); p.wait()
print("python returncode:", p.returncode, "-> shell/docker would report", 128 + abs(p.returncode))
