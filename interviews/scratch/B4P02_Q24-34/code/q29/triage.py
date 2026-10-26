import json, sys

def diagnose(c):
    s = c["State"]; code = s["ExitCode"]; err = s.get("Error", "")
    if s.get("OOMKilled"):
        return "OOM kill: raise --memory, shrink batch/workers, check for a leak (docker logs will look like it just stopped)"
    if "exec format error" in err:
        return "wrong CPU architecture: image built for arm64 run on amd64 or the reverse (see Q26)"
    if "no such file or directory" in err:
        return "entrypoint path missing, OR script has CRLF line endings so the shebang interpreter is not found, OR wrong WORKDIR"
    if code == 127: return "command not found: binary or script not in PATH/image"
    if code == 126: return "found but not executable: missing chmod +x, or a directory, or noexec mount"
    if code == 139: return "segfault (SIGSEGV): bad native lib, CUDA/driver mismatch"
    if code == 143: return "stopped by SIGTERM (normal for docker stop); only a problem if nobody asked it to stop"
    if code == 137: return "SIGKILL without OOMKilled: docker kill, stop grace period expired, or host OOM killer (check dmesg)"
    if code == 1:   return "app error: read `docker logs` for the traceback (import error, bad config, missing file)"
    return "unknown: read docker logs and docker events"

data = json.load(open(sys.argv[1]))
print(f"{'container':10} {'status':11} {'exit':>4} {'restarts':>8}  diagnosis")
for c in data:
    print(f"{c['Name']:10} {c['State']['Status']:11} {c['State']['ExitCode']:>4} {c['RestartCount']:>8}  {diagnose(c)}")
