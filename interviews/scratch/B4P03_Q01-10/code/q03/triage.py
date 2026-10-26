"""Suggest the next step for a crashing pod from pod-status JSON (kubectl get pod -o json shape)."""
import json, sys

def backoff_schedule(n):
    d, out = 10, []
    for _ in range(n):
        out.append(d)
        d = min(d * 2, 300)          # doubles, capped at 5 minutes (check current docs)
    return out

def advise(pod):
    cs = pod["status"]["containerStatuses"][0]
    waiting = cs["state"].get("waiting", {}).get("reason", "")
    term = cs.get("lastState", {}).get("terminated", {})
    code, reason = term.get("exitCode"), term.get("reason", "")
    log, events = pod.get("log_tail", ""), " ".join(pod.get("events", []))
    if waiting == "CreateContainerConfigError":
        return "config", "Secret/ConfigMap reference is broken: kubectl describe pod, read Events, create the missing object"
    if reason == "OOMKilled":
        return "oom", "memory limit hit: compare limit with real usage (kubectl top pod), raise limit or cut memory use"
    if "liveness probe" in events.lower():
        return "probe", "liveness killed a slow-starting container: add a startupProbe or relax liveness, check readiness path"
    if code in (126, 127) or "executable file not found" in log:
        return "entrypoint", "wrong command/args or missing binary: compare image CMD/ENTRYPOINT with the manifest"
    if "FileNotFoundError" in log or "No such file" in log:
        return "model-file", "model file missing: check volume mount path, init container or download step, MODEL_URI env"
    if "ModuleNotFoundError" in log or "ImportError" in log:
        return "import", "image lacks a dependency: run the image locally, fix requirements and rebuild"
    if code == 137:
        return "killed", "SIGKILL without OOM reason: look at node events, eviction, liveness, kubectl describe node"
    return "unknown", "kubectl logs --previous and describe pod; reproduce with docker run"

if __name__ == "__main__":
    for pod in json.load(open(sys.argv[1])):
        cs = pod["status"]["containerStatuses"][0]
        term = cs.get("lastState", {}).get("terminated", {})
        kind, step = advise(pod)
        print(f"{pod['name']}: exit={term.get('exitCode')} restarts={cs['restartCount']} -> [{kind}] {step}")
    print("backoff delays (s):", backoff_schedule(8))
    print("total wait over 8 restarts (s):", sum(backoff_schedule(8)))
