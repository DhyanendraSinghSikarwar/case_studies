### Q1 ⭐⭐⭐ 🟢 Pod, Deployment, ReplicaSet and Service, explained for an ML engineer. You have a model API container and need three copies behind one stable address that survive a pod crash. Explain what each object does, who owns whom (Deployment owns ReplicaSet owns Pods), why you never create bare Pods for a service, what happens when you delete one pod, and how a Service finds pods by label selector (ClusterIP, NodePort, LoadBalancer in one line each). Give a Deployment plus Service manifest and validate it with a script; applying it to a cluster is not executed here.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A Pod runs your container, a ReplicaSet keeps N identical pods alive, a Deployment owns the ReplicaSet and handles rollouts, and a Service gives all those pods one stable address by matching their labels.

**Then explain:**
- **Who does what.** Pod = one or more containers sharing network and storage; it is disposable and has a new IP each time. ReplicaSet = 'keep exactly 3 pods with these labels'. Deployment = owns ReplicaSets, one per version, and moves between them on a rollout or rollback. Ownership chain: Deployment owns ReplicaSet owns Pods (visible in `ownerReferences`).
- **Why not a bare Pod.** A bare pod has no controller. If it crashes past restart policy, or its node dies, nobody recreates it. A Deployment pod gets replaced, and you get rolling updates and rollback for free.
- **Delete one pod.** The ReplicaSet sees 2 of 3, creates a new pod with a new name and a new IP. The Service drops the dead pod from its endpoints and adds the new one when it is Ready, so clients keep using the same address.
- **Service = label selector, not a list of pods.** `selector: app=ml-api` picks every Ready pod with that label. ClusterIP: virtual IP reachable inside the cluster only (default). NodePort: opens the same port on every node. LoadBalancer: asks the cloud for an external load balancer (check your cloud's docs for cost and behaviour).
- **Failure modes.** Selector typo or a label missing on the pod template: the Service has zero endpoints, requests hang or are refused, and YAML validation still passes. `targetPort` pointing at the wrong port: same symptom. Readiness probe missing: traffic reaches pods that are still loading the model. Changing a Deployment's `spec.selector` after creation is rejected (immutable).

**Example:** Deployment asks for 3 replicas, labels `app=ml-api`. Pods: a, b, c. You delete b.
- Right after: 2 pods exist, desired 3, so the ReplicaSet creates d. End state: a, c, d. Count is 3 again, names differ.
- The Service selector `app=ml-api` matches the template labels `app=ml-api, version=v1` (a selector only needs to be a subset of the pod labels). Service port 80 forwards to the container port named `http` (8000).
- The scripts below check that match, run `kubernetes-validate --strict`, and replay the delete in a toy reconcile loop.

**Code:**
```yaml
# ---- ml-api.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api
  labels:
    app: ml-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-api
  template:
    metadata:
      labels:
        app: ml-api
        version: v1
    spec:
      containers:
        - name: api
          image: registry.example.com/ml/sentiment-api:1.0.0
          ports:
            - name: http
              containerPort: 8000
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            requests:
              cpu: "500m"
              memory: 1Gi
            limits:
              memory: 1Gi
---
apiVersion: v1
kind: Service
metadata:
  name: ml-api
spec:
  type: ClusterIP
  selector:
    app: ml-api
  ports:
    - name: http
      port: 80
      targetPort: http
```
```python
# ---- check_manifest.py ----
"""Cross-checks that schema validation cannot do: labels, selectors, ports."""
import sys, yaml

docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if d]
dep = next(d for d in docs if d["kind"] == "Deployment")
svc = next(d for d in docs if d["kind"] == "Service")

tmpl_labels = dep["spec"]["template"]["metadata"]["labels"]
dep_sel = dep["spec"]["selector"]["matchLabels"]
svc_sel = svc["spec"]["selector"]
ports = {p["name"]: p["containerPort"] for c in dep["spec"]["template"]["spec"]["containers"]
         for p in c.get("ports", [])}

def subset(sel, labels):
    return all(labels.get(k) == v for k, v in sel.items())

problems = []
if not subset(dep_sel, tmpl_labels):
    problems.append("Deployment selector does not match its own pod template labels")
if not subset(svc_sel, tmpl_labels):
    problems.append("Service selector matches no pod: it would have zero endpoints")
for sp in svc["spec"]["ports"]:
    tp = sp["targetPort"]
    if isinstance(tp, str) and tp not in ports:
        problems.append(f"Service targetPort name {tp!r} is not a named containerPort")

print("replicas:", dep["spec"]["replicas"])
print("service reaches pods with labels:", svc_sel, "->", "OK" if subset(svc_sel, tmpl_labels) else "NO MATCH")
print("targetPort", svc["spec"]["ports"][0]["targetPort"], "resolves to container port",
      ports.get(svc["spec"]["ports"][0]["targetPort"]))
print("problems:", problems or "none")
sys.exit(1 if problems else 0)

# ---- owner_sim.py ----
"""Toy ReplicaSet reconcile loop: 'desired 3 pods' is restored after a delete."""
import itertools

ids = itertools.count(1)

class ReplicaSet:
    def __init__(self, name, replicas):
        self.name, self.replicas, self.pods = name, replicas, []
    def reconcile(self):
        while len(self.pods) < self.replicas:           # too few: create
            self.pods.append(f"{self.name}-{next(ids):02d}")
        while len(self.pods) > self.replicas:           # too many: delete
            self.pods.pop()

rs = ReplicaSet("ml-api-7d9f", 3)      # Deployment owns this ReplicaSet
rs.reconcile()
print("start      :", rs.pods)
rs.pods.remove(rs.pods[1])             # kubectl delete pod <one>
print("after kill :", rs.pods, "(2 pods, 1 missing)")
rs.reconcile()                         # controller notices the gap
print("reconciled :", rs.pods, "(new name, same count)")

bare = ["bare-pod"]                    # a bare Pod has no controller
bare.remove("bare-pod")
print("bare pod after delete:", bare, "(nobody recreates it)")
```
```bash
# these ran (from the code/ folder of this answer):
kubernetes-validate --strict ml-api.yaml
python3 -I check_manifest.py ml-api.yaml
python3 -I owner_sim.py

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl apply -f ml-api.yaml
# kubectl get deploy,rs,pods,svc,endpoints -l app=ml-api
# kubectl delete pod <one-pod-name>   # then watch the ReplicaSet make a new one
```

**Output (my run):**
```text
$ kubernetes-validate --strict ml-api.yaml
INFO ml-api.yaml passed for resource deployment/ml-api against version 1.37
INFO ml-api.yaml passed for resource service/ml-api against version 1.37

$ python3 -I check_manifest.py ml-api.yaml
replicas: 3
service reaches pods with labels: {'app': 'ml-api'} -> OK
targetPort http resolves to container port 8000
problems: none

$ python3 -I owner_sim.py
start      : ['ml-api-7d9f-01', 'ml-api-7d9f-02', 'ml-api-7d9f-03']
after kill : ['ml-api-7d9f-01', 'ml-api-7d9f-03'] (2 pods, 1 missing)
reconciled : ['ml-api-7d9f-01', 'ml-api-7d9f-03', 'ml-api-7d9f-04'] (new name, same count)
bare pod after delete: [] (nobody recreates it)
```
Not executed here: `kubectl apply`, `kubectl get pods`, `kubectl delete pod`, and `kubectl get endpoints` (no cluster, no kubectl in this sandbox). What did run: schema validation of the manifest (kubernetes-validate 1.37.0, `--strict`, which rejects unknown fields; it checks schema only, not whether the image exists or the Service finds pods), my own label/port cross-check, and the toy ReplicaSet loop (a model of the idea, not the real controller).

**Follow-ups:**
- **What does `kubectl delete deployment` do to the pods?** It deletes the Deployment; the garbage collector removes its ReplicaSets and pods through the owner references. The Service stays, with no endpoints.
- **Why does the Service keep working while pods change IP?** It tracks labels, not IPs. The endpoint list is rebuilt as pods become Ready or go away.
- **When would you use a StatefulSet instead?** When each replica needs a stable identity or its own disk. A stateless model API does not.

**Common mistakes:**
- Creating bare Pods for a service and wondering why nothing restarts them on node loss.
- Labels on the Deployment object but not on the pod template; the Service matches pod labels only.
- Assuming validation success means the Service works. Schema validation cannot see an empty endpoint list.
- Exposing every model API with `LoadBalancer`; one Ingress or gateway in front is usually cheaper and cleaner (check current docs).

---

### Q2 ⭐⭐⭐ 🟢 Resource requests and limits for an ML inference pod. Explain what requests mean to the scheduler and what limits mean to the kubelet and the Linux kernel, why CPU is throttled but memory is killed, the three QoS classes (Guaranteed, Burstable, BestEffort) and which pods are evicted first, and what happens when requests are too high (pods stay Pending, money wasted) or too low (noisy neighbours, eviction). Pick numbers for a 2 GB model server, show the manifest, and write a small script that classifies QoS from a pod spec. No cluster is available, so applying it is not executed.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Requests are what the scheduler reserves for placement, limits are what the kubelet and kernel enforce at run time: CPU over the limit is throttled, memory over the limit is killed.

**Then explain:**
- **Requests = scheduling.** The scheduler adds up requests of pods already on a node and places a new pod only where the sum fits. Requests do not cap usage. They also drive HPA CPU utilisation and give a minimum CPU share under contention.
- **Limits = enforcement.** CPU limit becomes a CFS quota (for example 2 CPUs = 200 ms of CPU time per 100 ms period); beyond that the container waits, so latency goes up but nothing dies. Memory cannot be 'paused': past the limit the kernel's OOM killer ends the process (exit 137, `OOMKilled`).
- **QoS classes.** Guaranteed: every container has cpu and memory, requests equal to limits. BestEffort: nothing set at all. Burstable: everything else (for example memory limit only, or request below limit). Under node memory pressure the kubelet evicts BestEffort first, then Burstable pods using more than they requested, and Guaranteed last (the exact ranking also looks at usage over request and priority; check current docs).
- **Requests too high:** pods sit Pending, nodes look 'full' while real usage is low, money wasted. **Too low:** many pods packed on one node, noisy neighbours, CPU starvation, evictions when the node runs short.
- **Failure modes for ML.** Memory limit set to the model size only: load spikes, copies and request buffers push you over, OOMKilled. Tiny CPU limit on a model server: every request is slow because of throttling, yet CPU graphs look 'fine'. Many teams set a memory limit equal to the request and avoid a tight CPU limit; that is a policy choice, so state your reason.

**Example:** Model file is 2 GB in memory. Pick memory request = limit = 3Gi (2 GB weights + about 1 GB for runtime, tensors, request buffers). CPU request 1, limit 2.
- Requests and limits differ for CPU, so QoS is **Burstable**, even though memory is equal.
- To get **Guaranteed**, make CPU request = limit = 2 (second pod in the file). Cost: you reserve 2 CPUs always.
- A pod with no `resources` is **BestEffort** and is first to go under pressure.
- 3 pods x 3Gi memory request = 9Gi must fit in node allocatable memory (less than the node's total, after OS and kubelet reserve) or one pod stays Pending.

**Code:**
```yaml
# ---- model-server.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: model-server
  template:
    metadata:
      labels:
        app: model-server
    spec:
      containers:
        - name: server
          image: registry.example.com/ml/model-server:2.1.0
          resources:
            requests:
              cpu: "1"
              memory: 3Gi
            limits:
              cpu: "2"
              memory: 3Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: model-server-guaranteed
spec:
  containers:
    - name: server
      image: registry.example.com/ml/model-server:2.1.0
      resources:
        requests:
          cpu: "2"
          memory: 3Gi
        limits:
          cpu: "2"
          memory: 3Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: batch-helper-besteffort
spec:
  containers:
    - name: helper
      image: registry.example.com/ml/helper:1.0.0
```
```python
# ---- qos.py ----
"""Classify QoS from a pod spec and sanity-check resource quantities."""
import re, sys, yaml

UNITS = {"Ki": 2**10, "Mi": 2**20, "Gi": 2**30, "Ti": 2**40,
         "k": 10**3, "M": 10**6, "G": 10**9, "T": 10**12, "m": 1e-3, "": 1}

def qty(s):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(Ki|Mi|Gi|Ti|k|M|G|T|m|)", str(s))
    if not m:
        raise ValueError(f"bad quantity {s!r}")
    return float(m.group(1)) * UNITS[m.group(2)]

def qos(pod_spec):
    ctrs = pod_spec["containers"] + pod_spec.get("initContainers", [])
    any_set, all_guaranteed = False, True
    for c in pod_spec["containers"]:
        r = c.get("resources", {})
        req, lim = r.get("requests", {}), r.get("limits", {})
        req = {**lim, **req}                       # requests default to limits
        if req or lim:
            any_set = True
        for res in ("cpu", "memory"):
            if res not in lim or res not in req or qty(req[res]) != qty(lim[res]):
                all_guaranteed = False
    if not any_set:
        return "BestEffort"
    return "Guaranteed" if all_guaranteed else "Burstable"

def check_quantities(pod_spec):
    out = []
    for c in pod_spec["containers"]:
        r = c.get("resources", {})
        for res, v in {**r.get("requests", {}), **r.get("limits", {})}.items():
            qty(v)                                  # raises on junk such as "x"
        for res, v in r.get("requests", {}).items():
            lim = r.get("limits", {}).get(res)
            if lim is not None and qty(v) > qty(lim):
                out.append(f"{c['name']}: {res} request {v} > limit {lim}")
    return out

EVICTION_ORDER = {"BestEffort": 0, "Burstable": 1, "Guaranteed": 2}   # lower = evicted earlier (roughly)

if __name__ == "__main__":
    rows = []
    for d in yaml.safe_load_all(open(sys.argv[1])):
        spec = d["spec"]["template"]["spec"] if d["kind"] == "Deployment" else d["spec"]
        rows.append((d["metadata"]["name"], qos(spec), check_quantities(spec)))
    for name, q, issues in sorted(rows, key=lambda r: EVICTION_ORDER[r[1]]):
        print(f"{name:26s} {q:11s} issues={issues or 'none'}")
    # mixed case: memory limit only, no cpu -> Burstable
    print("memory-only limit  ->", qos({"containers": [{"name": "a", "resources": {"limits": {"memory": "1Gi"}}}]}))
    print("limits only (cpu+mem)->", qos({"containers": [{"name": "a", "resources": {"limits": {"cpu": "1", "memory": "1Gi"}}}]}))
    try:
        qty("x")
    except ValueError as e:
        print("junk quantity caught:", e)
```
```bash
# these ran (from the code/ folder of this answer):
kubernetes-validate --strict model-server.yaml
python3 -I qos.py model-server.yaml

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl apply -f model-server.yaml
# kubectl describe pod model-server-guaranteed | grep 'QoS Class'
```

**Output (my run):**
```text
$ kubernetes-validate --strict model-server.yaml
INFO model-server.yaml passed for resource deployment/model-server against version 1.37
INFO model-server.yaml passed for resource pod/model-server-guaranteed against version 1.37
INFO model-server.yaml passed for resource pod/batch-helper-besteffort against version 1.37

$ python3 -I qos.py model-server.yaml
batch-helper-besteffort    BestEffort  issues=none
model-server               Burstable   issues=none
model-server-guaranteed    Guaranteed  issues=none
memory-only limit  -> Burstable
limits only (cpu+mem)-> Guaranteed
junk quantity caught: bad quantity 'x'
```
Not executed: applying the manifests, `kubectl describe pod` (which prints the QoS Class line), and any eviction. What ran: kubernetes-validate 1.37.0 with `--strict` on all three objects, and my `qos.py`. The validator does not catch a junk quantity (a string such as `x` passes the schema), so `qos.py` parses quantities itself and checks request <= limit. The classifier follows the documented rule for regular containers; it ignores init containers, pod-level resources and the eviction ranking details.

**Follow-ups:**
- **Why is CPU throttled and memory killed?** CPU is compressible: you can give a process less time. Memory is not: you cannot take back pages in use without losing data, so the kernel kills.
- **Should I set CPU limits?** Debated. Limits can throttle bursty servers. Many platforms set requests and a memory limit but no CPU limit. Pick one, explain it, and check your cluster's policy.
- **What is LimitRange for?** Namespace defaults and min/max per container, so pods without resources do not become BestEffort by accident.

**Common mistakes:**
- Requests copied equal to limits everywhere 'to be safe': over-reserves nodes.
- No memory limit on a Python server with a growing cache: it takes the node down instead of itself.
- Memory in `M` vs `Mi`: `500M` is 500 million bytes, `500Mi` is 524,288,000 bytes. Quantity typos pass schema validation.
- Reading `top` CPU graphs for a throttled pod and concluding it is idle.

---

### Q3 ⭐⭐⭐ 🟡 A pod is in CrashLoopBackOff. Walk through the exact debugging order you would follow in an interview: kubectl get pod, describe (last state, exit code, events), logs and logs --previous, what the backoff delay does (up to about five minutes), and the usual causes for an ML container (missing model file, wrong entrypoint, import error, bad env var or Secret, failing liveness probe, OOM). Give a decision table from symptom to likely cause to next command, and a Python script that reads sample kubectl describe or pod-status JSON and suggests the next step. The commands themselves are not executed here (no cluster).
**Asked at:** Kubernetes troubleshooting write-ups (techinterview.org 'What Kubernetes interviewers actually ask once you are past pods', OneUptime CrashLoopBackOff and OOMKilled guide 2026, vervecopilot, devopsboys; search snippets only, not opened); scenario-style 'here is what kubectl get pods prints, what next' rounds; editorial, not verified candidate reports; DevOps, SRE and MLOps loops
**Say this first (1 line):** I go get pods, then describe pod for last state, exit code and events, then logs and logs --previous, and I let the exit code and the last log line pick the cause.

**Then explain:**
- **Order.** 1) `kubectl get pod` (restarts, status). 2) `kubectl describe pod` (Last State: Terminated, Reason, Exit Code; Events at the bottom: probe failures, pull errors, OOM). 3) `kubectl logs <pod>` for the current attempt, then `kubectl logs <pod> --previous` for the one that just died, since the current container may have no output yet. 4) Only then guess: reproduce the image locally with `docker run`.
- **Backoff.** Kubelet restarts a failing container with delays that double from about 10 s to a cap of about 5 minutes (check current docs); it resets after the container runs cleanly for a while. So a pod that crashes in a second shows long gaps between attempts, and 'Running' for a moment can be a lie.
- **Exit codes.** 1 = app error (read the log). 127/126 = command not found / not executable (entrypoint). 137 = SIGKILL (OOMKilled, or killed by liveness/eviction). 143 = SIGTERM. 0 on a Deployment pod still loops, because Deployments expect the container to keep running.
- **Usual ML causes.** Model file missing (wrong mount path, init download failed). Wrong command or args. Import error (dependency missing in image). Bad env var or missing Secret/ConfigMap (that shows as `CreateContainerConfigError`, not a crash). Liveness probe killing a container that is still loading weights. OOM while loading the model.
- **Failure modes of the debugging itself.** Reading only current logs (empty because it just restarted). Deleting the pod, which wipes the evidence of Last State. Assuming 137 always means OOM: check the Reason line.

**Example:** Table below. Then the script reads six sample pod-status records and prints the next step for each. Backoff by hand: 10, 20, 40, 80, 160, 300, 300, 300 = 1210 s of waiting over 8 restarts.

| Symptom (describe / logs) | Likely cause | Next command |
|---|---|---|
| Exit 1, `FileNotFoundError` model path | model not mounted or download failed | `kubectl describe pod` (volumes), check init container logs, `kubectl exec` on a debug pod to `ls` the path |
| Exit 137, Reason OOMKilled | memory limit too low | `kubectl top pod` (needs metrics-server), raise limit, see Q4 |
| Exit 137, Reason Error, Events: liveness probe failed | liveness kills slow loader | add startupProbe, see Q6 |
| Exit 127 / `executable file not found` | wrong command or args | compare `spec.containers[].command` with image CMD |
| Exit 1, `ModuleNotFoundError` | dependency missing in image | `docker run --rm image python -c "import torch"`, rebuild |
| `CreateContainerConfigError` | Secret/ConfigMap name or key missing | `kubectl get secret,configmap -n ns`, fix reference |

**Code:**
```text
[
 {"name": "ml-api-a1", "status": {"containerStatuses": [{"name": "api", "restartCount": 7,
   "state": {"waiting": {"reason": "CrashLoopBackOff"}},
   "lastState": {"terminated": {"exitCode": 1, "reason": "Error"}}}]},
  "log_tail": "FileNotFoundError: [Errno 2] No such file or directory: '/models/model.pkl'"},
 {"name": "ml-api-b2", "status": {"containerStatuses": [{"name": "api", "restartCount": 5,
   "state": {"waiting": {"reason": "CrashLoopBackOff"}},
   "lastState": {"terminated": {"exitCode": 137, "reason": "OOMKilled"}}}]},
  "log_tail": ""},
 {"name": "ml-api-c3", "status": {"containerStatuses": [{"name": "api", "restartCount": 9,
   "state": {"waiting": {"reason": "CrashLoopBackOff"}},
   "lastState": {"terminated": {"exitCode": 137, "reason": "Error"}}}]},
  "log_tail": "INFO loading weights ...", "events": ["Warning Unhealthy Liveness probe failed: HTTP probe failed with statuscode: 503", "Normal Killing Container api failed liveness probe, will be restarted"]},
 {"name": "ml-api-d4", "status": {"containerStatuses": [{"name": "api", "restartCount": 4,
   "state": {"waiting": {"reason": "CrashLoopBackOff"}},
   "lastState": {"terminated": {"exitCode": 127, "reason": "ContainerCannotRun"}}}]},
  "log_tail": "exec: \"serve\": executable file not found in $PATH"},
 {"name": "ml-api-e5", "status": {"containerStatuses": [{"name": "api", "restartCount": 6,
   "state": {"waiting": {"reason": "CrashLoopBackOff"}},
   "lastState": {"terminated": {"exitCode": 1, "reason": "Error"}}}]},
  "log_tail": "ModuleNotFoundError: No module named 'torch'"},
 {"name": "ml-api-f6", "status": {"containerStatuses": [{"name": "api", "restartCount": 3,
   "state": {"waiting": {"reason": "CreateContainerConfigError"}}}]},
  "log_tail": "", "events": ["Warning Failed Error: secret \"api-keys\" not found"]}
]
```
```python
# ---- triage.py ----
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
```
```bash
# these ran (from the code/ folder of this answer):
python3 -I triage.py pods_crash.json

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl get pod ml-api-a1
# kubectl describe pod ml-api-a1
# kubectl logs ml-api-a1
# kubectl logs ml-api-a1 --previous
```

**Output (my run):**
```text
$ python3 -I triage.py pods_crash.json
ml-api-a1: exit=1 restarts=7 -> [model-file] model file missing: check volume mount path, init container or download step, MODEL_URI env
ml-api-b2: exit=137 restarts=5 -> [oom] memory limit hit: compare limit with real usage (kubectl top pod), raise limit or cut memory use
ml-api-c3: exit=137 restarts=9 -> [probe] liveness killed a slow-starting container: add a startupProbe or relax liveness, check readiness path
ml-api-d4: exit=127 restarts=4 -> [entrypoint] wrong command/args or missing binary: compare image CMD/ENTRYPOINT with the manifest
ml-api-e5: exit=1 restarts=6 -> [import] image lacks a dependency: run the image locally, fix requirements and rebuild
ml-api-f6: exit=None restarts=3 -> [config] Secret/ConfigMap reference is broken: kubectl describe pod, read Events, create the missing object
backoff delays (s): [10, 20, 40, 80, 160, 300, 300, 300]
total wait over 8 restarts (s): 1210
```
Not executed: every `kubectl` command here (no cluster, no kubectl). What ran: `triage.py` over sample JSON that I wrote in the shape of `kubectl get pod -o json` status fields (not captured from a real cluster), so it shows the decision logic, not real kubectl output. The backoff numbers follow the documented doubling to a 5-minute cap; confirm in current docs for your version.

**Follow-ups:**
- **Pod shows Running but restarts keep climbing?** The container starts, runs a bit, then dies. Use `logs --previous` and the Last State exit code. Restart count is the signal, not status.
- **Logs are empty with --previous?** The process died before writing. Check entrypoint, config errors and OOM at start; run the image locally with the same env.
- **How do you debug if the image has no shell?** `kubectl debug` with an ephemeral container (check your cluster version) or run the same image locally with an overridden entrypoint.

**Common mistakes:**
- Running `kubectl delete pod` first and losing Last State and the previous logs.
- Treating CrashLoopBackOff as the cause. It is the symptom; the cause is in the exit code, the logs and the events.
- Raising memory blindly for exit 137 without checking the Reason (OOMKilled versus liveness kill).
- Forgetting `-c <container>` when the pod has sidecars.

---

### Q4 ⭐⭐⭐ 🟡 A pod was OOMKilled (exit code 137). Explain the difference between a container hitting its memory limit (cgroup OOM kill of that container) and the node running out of memory (kubelet eviction), how to tell them apart from describe output (Reason: OOMKilled versus Evicted), why a Python ML service can exceed its limit (batch size, model copies per worker, pandas copies, pinned memory, shared memory in dataloaders), and how you would choose a new limit from observed usage. Include a script that parses a sample pod status and a memory-sizing calculation worked by hand. Live kubectl and metrics are not executed.
**Asked at:** Kubernetes troubleshooting write-ups (techinterview.org 'What Kubernetes interviewers actually ask once you are past pods', OneUptime CrashLoopBackOff and OOMKilled guide 2026, vervecopilot, devopsboys; search snippets only, not opened); scenario-style 'here is what kubectl get pods prints, what next' rounds; editorial, not verified candidate reports; DevOps, SRE and MLOps loops
**Say this first (1 line):** Container OOMKilled means that one container hit its own memory limit and the kernel killed it (exit 137); Evicted means the node itself was short of memory and the kubelet chose to remove a pod.

**Then explain:**
- **Two different events.** Cgroup OOM: the limit belongs to the container; the pod stays on the node, the container restarts (`Last State: Terminated, Reason: OOMKilled`). Node-pressure eviction: kubelet sees low node memory, picks pods (those using more than their request first), and the whole pod ends up `Failed` with `Reason: Evicted`; a controller makes a new pod elsewhere. There can also be a kernel-level OOM on the node outside the kubelet's eviction, so check node events too.
- **Tell them apart.** `kubectl describe pod`: `OOMKilled` under Last State versus pod Status `Failed`, Reason `Evicted`, message 'The node was low on resource: memory'. Fix for the first: limit or usage. Fix for the second: requests honest, node sizes, fewer BestEffort pods.
- **Why Python ML services blow their limit.** Batch size (tensors scale with it). Several gunicorn/uvicorn workers each loading their own copy of the model. pandas creating copies on merge or `astype`. Pinned (page-locked) memory. Dataloader workers and `/dev/shm` shared memory for PyTorch (the default pod shared memory is small; an `emptyDir` with `medium: Memory` counts against the memory limit). Memory that is mapped but not freed because of fragmentation.
- **Choosing a limit.** Observe the working set over a realistic period including the load phase and the biggest request; set request near a high percentile, set the limit at observed peak plus headroom, then watch for OOM. Do not size from an average.
- **Failure modes.** Raising the limit hides a leak (usage keeps climbing until the new limit). Limit larger than any node can give: pod Pending forever. Memory limit below the model size: dies at start, looks like CrashLoopBackOff.

**Example:** 20 working-set samples in MiB: sixteen at 1500, then 1600, 1650, 1700, 1800.
- p95 = the 19th of 20 sorted values = 1700. Peak = 1800.
- Request = 1700 rounded up to a multiple of 64 = 1728 MiB (27 x 64).
- Limit = 1800 x 1.25 = 2250, rounded up to 2304 MiB (36 x 64).
- Worker trap: a 2048 MiB model with 4 workers that each load it is 8192 MiB; loaded once and shared it is 2048 MiB. (Sharing through fork and copy-on-write is fragile in Python because reference counting touches pages, so do not count on it; one worker per pod with more replicas is the simpler fix.)

**Code:**
```text
[
 {"name": "scorer-1", "status": {"phase": "Running", "containerStatuses": [{"name": "app", "restartCount": 3,
   "lastState": {"terminated": {"exitCode": 137, "reason": "OOMKilled"}}}]}},
 {"name": "scorer-2", "status": {"phase": "Failed", "reason": "Evicted",
   "message": "The node was low on resource: memory. Container app was using 1900Mi, request is 512Mi, has larger consumption of memory than requested.",
   "containerStatuses": []}},
 {"name": "scorer-3", "status": {"phase": "Running", "containerStatuses": [{"name": "app", "restartCount": 0, "lastState": {}}]}}
]
```
```python
# ---- oom.py ----
"""Tell cgroup OOM kill from node-pressure eviction, and size a memory limit."""
import json, math, sys

def classify(pod):
    st = pod["status"]
    if st.get("reason") == "Evicted":
        return "node-eviction", "node ran low on memory; this pod was chosen. Check requests vs usage and node size."
    for cs in st.get("containerStatuses", []):
        t = cs.get("lastState", {}).get("terminated", {})
        if t.get("reason") == "OOMKilled":
            return "container-oom", "this container hit ITS OWN memory limit (exit 137). Raise limit or cut usage."
    return "healthy", "no memory kill seen"

def size_memory(samples_mib, headroom=0.25, req_pctl=0.95):
    s = sorted(samples_mib)
    p = s[min(len(s) - 1, math.ceil(req_pctl * len(s)) - 1)]
    peak = s[-1]
    request = math.ceil(p / 64) * 64                 # round up to 64 MiB
    limit = math.ceil(peak * (1 + headroom) / 64) * 64
    return {"p95": p, "peak": peak, "request": request, "limit": limit}

def python_footprint(model_mib, workers, preload_shared=False):
    # naive model: each worker loads its own copy unless weights are shared (copy-on-write, fragile in Python)
    return model_mib if preload_shared else model_mib * workers

if __name__ == "__main__":
    for pod in json.load(open(sys.argv[1])):
        k, why = classify(pod)
        print(f"{pod['name']}: {k:14s} {why}")
    # hand-checkable: 20 samples of working set in MiB
    samples = [1500] * 16 + [1600, 1650, 1700, 1800]
    print("sizing:", size_memory(samples))
    print("2048 MiB model x 4 workers  =", python_footprint(2048, 4), "MiB")
    print("2048 MiB model, shared once =", python_footprint(2048, 4, True), "MiB")
```
```bash
# these ran (from the code/ folder of this answer):
python3 -I oom.py pods_mem.json

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl describe pod scorer-1 | grep -A6 'Last State'
# kubectl top pod scorer-1 --containers
```

**Output (my run):**
```text
$ python3 -I oom.py pods_mem.json
scorer-1: container-oom  this container hit ITS OWN memory limit (exit 137). Raise limit or cut usage.
scorer-2: node-eviction  node ran low on memory; this pod was chosen. Check requests vs usage and node size.
scorer-3: healthy        no memory kill seen
sizing: {'p95': 1700, 'peak': 1800, 'request': 1728, 'limit': 2304}
2048 MiB model x 4 workers  = 8192 MiB
2048 MiB model, shared once = 2048 MiB
```
Not executed: `kubectl describe pod`, `kubectl top pod` and a real OOM. What ran: `oom.py` on sample pod-status JSON I wrote (the Evicted message text follows the format Kubernetes documents, but these are not captured from a cluster), the sizing function and the worker arithmetic. The headroom factor (25 percent) and the 95th percentile are my example choices, not a standard.

**Follow-ups:**
- **Does a memory request protect me from OOM?** No. Only the limit triggers the container OOM kill. The request affects scheduling and eviction order.
- **Pod OOMs only at start?** Peak during model load (read file plus build tensors). Size for the load peak, or load in a streaming way, or use a bigger limit only during startup via an init step.
- **How do I stop dataloader shared-memory crashes?** Mount an `emptyDir` with `medium: Memory` at `/dev/shm` and count its size in the limit (check your runtime's behaviour).

**Common mistakes:**
- Reporting 'OOM' for both events. Eviction is a node decision.
- Sizing the limit from the average.
- Forgetting that tmpfs `emptyDir` and page cache-heavy file reads can count toward the container's memory.
- Setting the JVM or Python worker count from the node's CPUs instead of the pod's limit.

---

### Q5 ⭐⭐⭐ 🟡 A pod stays Pending. List the reasons in the order you would check them: insufficient CPU, memory or GPU on any node, node selector or affinity mismatch, taints without tolerations, unbound PersistentVolumeClaim, quota exceeded, image pull problems (that one is ImagePullBackOff, not Pending), and a scheduler event message such as '0/5 nodes are available: 3 Insufficient nvidia.com/gpu, 2 node(s) had untolerated taint'. Explain how to read that message, and write a script that parses such event strings into a summary count of reasons. The cluster commands are not executed here.
**Asked at:** Kubernetes troubleshooting write-ups (techinterview.org 'What Kubernetes interviewers actually ask once you are past pods', OneUptime CrashLoopBackOff and OOMKilled guide 2026, vervecopilot, devopsboys; search snippets only, not opened); scenario-style 'here is what kubectl get pods prints, what next' rounds; editorial, not verified candidate reports; DevOps, SRE and MLOps loops
**Say this first (1 line):** Pending means the scheduler could not place the pod, so I read the FailedScheduling event in describe pod: it says how many nodes failed for each reason, and I fix the biggest reason.

**Then explain:**
- **Order I check.** 1) Event text (`kubectl describe pod`, Events). 2) Resources: Insufficient cpu, memory or `nvidia.com/gpu`. 3) Taints without tolerations. 4) nodeSelector or affinity that matches no node. 5) PVC unbound (StorageClass, zone). 6) Pod-count cap ('Too many pods'). 7) Quota: if a ResourceQuota blocks you, the **pod is never created**: look at the ReplicaSet events (`FailedCreate ... exceeded quota`), not at a Pending pod.
- **Reading the message.** `0/5 nodes are available: 3 Insufficient nvidia.com/gpu, 2 node(s) had untolerated taint ...`. The 0/5 says no node passed. The numbers after it sum to the node count: each node is listed once under the first filter it failed. Wording varies by Kubernetes version, so read, do not pattern-match blindly.
- **Eligibility, not capacity.** Often the cluster has room but your pod is not allowed on those nodes (taints, selector, zone of the PVC). Adding nodes does not fix that.
- **Image problems are not Pending.** A pod that was scheduled and cannot pull its image shows `ErrImagePull` / `ImagePullBackOff` (status Pending phase but the node is chosen). Check events for 'Successfully assigned' to separate the two.
- **Failure modes.** Cluster autoscaler adds nothing because the pod can never fit any node shape (request bigger than the largest node, or GPU label wrong). A GPU pod Pending forever because the GPU nodes are tainted and the pod has no toleration.

**Example:** Message: `0/5 nodes are available: 3 Insufficient nvidia.com/gpu, 2 node(s) had untolerated taint {nvidia.com/gpu: present}.`
- 3 + 2 = 5 nodes. Three nodes have GPUs but all in use; two nodes are tainted and the pod does not tolerate. Next step: free or add GPUs, and check whether your toleration key matches the taint (Q8).
- Second example in the file: `4 node(s) didn't match Pod's node affinity/selector` means a label problem; no amount of capacity helps.

**Code:**
```text
# ---- events.txt ----
0/5 nodes are available: 3 Insufficient nvidia.com/gpu, 2 node(s) had untolerated taint {nvidia.com/gpu: present}. preemption: 0/5 nodes are available: 5 Preemption is not helpful for scheduling.
0/4 nodes are available: 4 node(s) didn't match Pod's node affinity/selector.
0/6 nodes are available: 2 Insufficient memory, 1 Insufficient cpu, 3 node(s) had untolerated taint {dedicated: gpu}.
0/3 nodes are available: pod has unbound immediate PersistentVolumeClaims.
0/5 nodes are available: 5 Too many pods.
```
```python
# ---- pending.py ----
"""Parse scheduler FailedScheduling messages into a count of reasons per message and overall."""
import re, sys
from collections import Counter

def split_top(s):
    """Split on commas that are not inside braces (taints look like {key: value})."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        depth += ch == "{"
        depth -= ch == "}"
        if ch == "," and depth == 0:
            parts.append(cur.strip()); cur = ""
        else:
            cur += ch
    return parts + [cur.strip()] if cur.strip() else parts

def parse(msg):
    m = re.match(r"0/(\d+) nodes are available: (.*)", msg)
    total, rest = int(m.group(1)), m.group(2)
    rest = re.split(r"\.\s+preemption:", rest)[0].rstrip(".")      # drop the preemption tail
    counts = Counter()
    for part in split_top(rest):
        pm = re.match(r"(\d+) (.*)", part)
        if pm:
            counts[pm.group(2)] += int(pm.group(1))
        else:
            counts[part] += total                                   # no count prefix: applies to all
    return total, counts

HINTS = {
    "Insufficient": "no node has that much free; reduce requests, add nodes, or wait for autoscaler",
    "untolerated taint": "add a toleration, or this pod should not run on those nodes",
    "node affinity": "fix nodeSelector / affinity labels vs kubectl get nodes --show-labels",
    "unbound": "PVC is not bound: kubectl get pvc, check StorageClass and zone",
    "Too many pods": "node pod-count cap reached: more nodes or bigger max-pods",
}
def hint(reason):
    return next((h for k, h in HINTS.items() if k in reason), "read the full event")

if __name__ == "__main__":
    grand = Counter()
    for line in open(sys.argv[1]):
        total, counts = parse(line.strip())
        grand.update(counts)
        print(f"nodes={total}  sum_of_reasons={sum(counts.values())}")
        for r, n in counts.most_common():
            print(f"   {n} x {r}  -> {hint(r)}")
    print("\noverall:")
    for r, n in grand.most_common():
        print(f"  {n:2d}  {r}")
```
```bash
# these ran (from the code/ folder of this answer):
python3 -I pending.py events.txt

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl describe pod <pod> | sed -n '/Events/,$p'
# kubectl get events --field-selector reason=FailedScheduling
# kubectl get pvc
# kubectl describe resourcequota -n <ns>
```

**Output (my run):**
```text
$ python3 -I pending.py events.txt
nodes=5  sum_of_reasons=5
   3 x Insufficient nvidia.com/gpu  -> no node has that much free; reduce requests, add nodes, or wait for autoscaler
   2 x node(s) had untolerated taint {nvidia.com/gpu: present}  -> add a toleration, or this pod should not run on those nodes
nodes=4  sum_of_reasons=4
   4 x node(s) didn't match Pod's node affinity/selector  -> fix nodeSelector / affinity labels vs kubectl get nodes --show-labels
nodes=6  sum_of_reasons=6
   3 x node(s) had untolerated taint {dedicated: gpu}  -> add a toleration, or this pod should not run on those nodes
   2 x Insufficient memory  -> no node has that much free; reduce requests, add nodes, or wait for autoscaler
   1 x Insufficient cpu  -> no node has that much free; reduce requests, add nodes, or wait for autoscaler
nodes=3  sum_of_reasons=3
   3 x pod has unbound immediate PersistentVolumeClaims  -> PVC is not bound: kubectl get pvc, check StorageClass and zone
nodes=5  sum_of_reasons=5
   5 x Too many pods  -> node pod-count cap reached: more nodes or bigger max-pods

overall:
   5  Too many pods
   4  node(s) didn't match Pod's node affinity/selector
   3  Insufficient nvidia.com/gpu
   3  node(s) had untolerated taint {dedicated: gpu}
   3  pod has unbound immediate PersistentVolumeClaims
   2  node(s) had untolerated taint {nvidia.com/gpu: present}
   2  Insufficient memory
   1  Insufficient cpu
```
Not executed: `kubectl get pod`, `describe pod`, `get events`, `get pvc`, and any scheduling. What ran: `pending.py` on five message strings I wrote in the format the scheduler documents (not captured from a cluster). Message wording changes between Kubernetes versions, so this parser is a teaching sketch; a production tool should use structured events.

**Follow-ups:**
- **Pod is Pending but the node has free CPU?** Look for taints, selectors, unbound PVC, or pod anti-affinity. Free CPU is irrelevant if the pod is not eligible.
- **How does cluster autoscaler react to Pending pods?** It scales up only for pods that could fit on a new node of a configured group. Pods blocked by selectors that no group satisfies stay Pending (check your autoscaler's docs).
- **What if the PVC is bound to a zone with no GPU nodes?** The pod is Pending with a volume node-affinity conflict. Use a StorageClass with delayed binding or put the pool in that zone.

**Common mistakes:**
- Calling ImagePullBackOff 'Pending'.
- Adding nodes for a taint or label problem.
- Looking for a pod when a quota rejection means none was created.
- Quoting a single event string as if wording were stable across versions.

---

### Q6 ⭐⭐⭐ 🟡 Liveness, readiness and startup probes for a model server that takes 90 seconds to load weights. Explain what each probe does when it fails (restart, remove from Service endpoints, hold off the other probes), why a liveness probe that checks the model can cause a restart loop during loading, why readiness should check the model is loaded and can answer, and how to size a startup probe (failureThreshold times periodSeconds above the worst-case load time). Give the probe YAML for an HTTP /healthz and /ready pair, a small Python server sketch with a loading flag, and a script that computes the startup budget. No cluster, so probe behaviour is not executed; the Python flag logic can be run locally.
**Asked at:** Probe and model-loading write-ups (llm-d readiness probes docs, OneUptime startup probes article, DZone 'Kubernetes LLM readiness' experiment, AWS containers blog on fast model loading on EKS; search snippets only, not opened); docs and blogs, not interview reports; ML serving and platform roles
**Say this first (1 line):** Liveness asks 'is the process stuck, restart it', readiness asks 'can it serve right now, send traffic or not', and a startup probe holds the other two off until the slow model load is done.

**Then explain:**
- **What a failure does.** Liveness fails: kubelet restarts the container. Readiness fails: the pod is removed from Service endpoints, nothing restarts. Startup fails past its budget: container is restarted; while startup has not succeeded, liveness and readiness do not run.
- **Liveness must be cheap and local.** Check that the process answers (`/healthz`). If liveness also checks 'model loaded', then during a 90 s load it fails, gets killed at about the third miss, restarts, loads again, fails again: a restart loop that never serves.
- **Readiness checks usefulness.** `/ready` returns 200 only when weights are in memory and, if you can afford it, a tiny dummy prediction works. Before that, 503, so no traffic. A shallow readiness (just 'port open') sends traffic to a pod that will fail requests. Do not make readiness depend on a downstream database you share: one outage then removes every pod and widens the incident.
- **Size the startup probe.** Budget = `failureThreshold x periodSeconds` (plus initial delay). It must beat the worst-case load, not the average: loads slow down when many pods pull weights together or the disk is cold. Rule I use: worst case x 1.5.
- **Failure modes.** Startup budget too small: restart loop. Probe `timeoutSeconds` shorter than a GC pause or a busy worker: false restarts. Probing an endpoint that runs inference on the same thread: probes queue behind real traffic.

**Example:** Worst-case load 90 s, probe period 5 s, safety x1.5 = 135 s, so failureThreshold >= 27. The YAML uses 36 (budget 180 s).
- Timeline of the bad design (liveness checks the model, first probe at 10 s, period 10 s, 3 failures): restarts at t = 30, 60, 90, 120... the model needs 90 s but gets only 30 s per life, so it never gets healthy. The script reproduces these times.
- Good design: startup (budget 180 s) holds liveness off; `/healthz` is always 200; `/ready` flips from 503 to 200 once loading ends.

**Code:**
```yaml
# ---- model-server.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: model-server
  template:
    metadata:
      labels:
        app: model-server
    spec:
      terminationGracePeriodSeconds: 30
      containers:
        - name: server
          image: registry.example.com/ml/model-server:2.1.0
          ports:
            - name: http
              containerPort: 8000
          startupProbe:
            httpGet:
              path: /healthz
              port: http
            periodSeconds: 5
            failureThreshold: 36        # 36 x 5 s = 180 s budget for a 90 s load
          livenessProbe:
            httpGet:
              path: /healthz            # process-only check, never the model
              port: http
            periodSeconds: 10
            failureThreshold: 3
            timeoutSeconds: 2
          readinessProbe:
            httpGet:
              path: /ready              # 200 only when weights are loaded and a tiny predict works
              port: http
            periodSeconds: 5
            failureThreshold: 2
            timeoutSeconds: 2
```
```python
# ---- probes.py ----
"""Model server sketch with a loading flag (/healthz = process alive, /ready = model usable),
plus startup-budget arithmetic, a bad-liveness restart timeline and a real local test."""
import http.server, threading, time

STATE = {"loaded": False}

def load_model(seconds):
    time.sleep(seconds)               # stands in for reading weights from disk or object storage
    STATE["loaded"] = True

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            code = 200                                   # alive even while loading
        elif self.path == "/ready":
            code = 200 if STATE["loaded"] else 503       # not ready until weights are in memory
        else:
            code = 404
        self.send_response(code); self.end_headers(); self.wfile.write(b"ok" if code == 200 else b"no")
    def log_message(self, *a): pass

def make_server(load_seconds, port=0):
    threading.Thread(target=load_model, args=(load_seconds,), daemon=True).start()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

import urllib.request, urllib.error

def budget(period_s, failure_threshold, initial_delay=0):
    return initial_delay + period_s * failure_threshold

def min_threshold(worst_case_load_s, period_s, safety=1.5):
    need = worst_case_load_s * safety
    return int(-(-need // period_s))                # ceil

print("budget 5s x 36        =", budget(5, 36), "s")
print("min failureThreshold for worst load 90 s, period 5 s, x1.5 safety =", min_threshold(90, 5))

def liveness_loop(load_s, initial=10, period=10, threshold=3, horizon=200):
    """Liveness checks the MODEL (fails while loading). Returns restart times."""
    t0, restarts, fails, t = 0, [], 0, initial
    while t <= horizon:
        loaded = (t - t0) >= load_s
        fails = 0 if loaded else fails + 1
        if fails >= threshold:
            restarts.append(t); t0, fails, t = t, 0, t + initial   # container restarts, loads again
            continue
        t += period
    return restarts
print("bad liveness (checks model, load 90 s) restarts at t =", liveness_loop(90)[:4], "... never becomes healthy")
print("good: liveness=/healthz always 200 -> restarts: none; startupProbe holds liveness off")

def get(port, path):
    try:
        return urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=1).status
    except urllib.error.HTTPError as e:
        return e.code

srv = make_server(load_seconds=1.0)               # 1 s stands in for 90 s
port = srv.server_address[1]
print("t=0.0  /healthz", get(port, "/healthz"), " /ready", get(port, "/ready"))
time.sleep(1.3)
print("t=1.3  /healthz", get(port, "/healthz"), " /ready", get(port, "/ready"))
srv.shutdown()
```
```bash
# these ran (from the code/ folder of this answer):
kubernetes-validate --strict model-server.yaml
python3 -I probes.py

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl apply -f model-server.yaml
# kubectl get endpoints model-server -w
```

**Output (my run):**
```text
$ kubernetes-validate --strict model-server.yaml
INFO model-server.yaml passed for resource deployment/model-server against version 1.37

$ python3 -I probes.py
budget 5s x 36        = 180 s
min failureThreshold for worst load 90 s, period 5 s, x1.5 safety = 27
bad liveness (checks model, load 90 s) restarts at t = [30, 60, 90, 120] ... never becomes healthy
good: liveness=/healthz always 200 -> restarts: none; startupProbe holds liveness off
t=0.0  /healthz 200  /ready 503
t=1.3  /healthz 200  /ready 200
```
Not executed: kubelet probe behaviour, restarts and endpoint removal (no cluster). What ran: kubernetes-validate 1.37.0 `--strict` on the Deployment; the budget arithmetic; the restart timeline (a simulation of my reading of the probe rules); and a real local HTTP server with a loading flag, polled with urllib (1 s load stands in for 90 s). The server is a stdlib sketch, not a production server.

**Follow-ups:**
- **Do I still need a readiness probe if I have a startup probe?** Yes. Startup only guards boot. Readiness keeps working all life long, for example when a worker is overloaded or the model reloads.
- **Why not a long `initialDelaySeconds`?** It is a fixed guess: slow loads still fail, fast loads wait for nothing. Startup probes poll and finish as soon as the app is up.
- **What about graceful shutdown?** Separate topic (SIGTERM, preStop, terminationGracePeriodSeconds): readiness should go false first so the pod drains.

**Common mistakes:**
- One `/health` endpoint used for liveness and readiness.
- Liveness that calls the model or the database.
- Startup budget sized for the average load time.
- Probe port or path typo: every pod restarts. Schema validation cannot catch it.

---

### Q7 ⭐⭐⭐ 🟡 ConfigMaps and Secrets for an ML service. Explain what goes in each (feature thresholds, model URI, log level versus API keys, registry credentials), how they are consumed (environment variables versus mounted files), why a changed ConfigMap does not restart pods by itself (env vars are read at start; mounted files update after a delay), how Secrets are only base64 encoded by default and what that means, and options such as encryption at rest, external secret managers and RBAC. Give manifests, a script that base64 decodes a sample Secret to show it is not encryption, and a hash-annotation trick to roll pods on config change. Applying is not executed.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** ConfigMaps hold non-secret settings, Secrets hold credentials, both reach the pod as env vars or mounted files, and base64 in a Secret is only encoding, so you protect Secrets with RBAC, encryption at rest and an external secret manager.

**Then explain:**
- **What goes where.** ConfigMap: model URI, thresholds, log level, feature flags. Secret: API keys, registry credentials, database passwords, tokens. If a leak would hurt, it is a Secret.
- **Env var vs file.** Env vars are read once at container start; changing the ConfigMap does **not** restart pods and running pods keep the old values. Mounted ConfigMap files are refreshed by the kubelet after a delay (not for `subPath` mounts, and your app must re-read the file). Env is simple; files suit big or changing configs.
- **Rolling on change.** Put a hash of the config in a pod-template annotation (`checksum/config`). Config changes, hash changes, template changes, Deployment rolls. Helm charts do this with a `sha256sum` template function; or run `kubectl rollout restart` (not executed here).
- **Secrets are base64, not encrypted.** Anyone who can `get` the Secret can decode it (the script shows it). Real protection: RBAC that limits who can read Secrets (including list and watch, and the ability to create pods that mount them), encryption at rest in etcd (a cluster setting; check your platform), and external managers (a cloud secrets service or Vault, synced by a CSI driver or operator; check current docs). Never commit Secret YAML with real values to git.
- **Failure modes.** Missing key or object: pod stuck in `CreateContainerConfigError`. Secret in an env var can leak through crash dumps, logs of `env`, or child processes. A ConfigMap above about 1 MiB is rejected: do not store models in it.

**Example:** ConfigMap `THRESHOLD: "0.62"`. The Deployment reads it with `envFrom`.
- Edit it to "0.70": running pods still use 0.62 (env is fixed at start).
- The hash of the config data changes (00131ed2432d8c33 becomes 8be2d7a7357668d7 in the output), the annotation changes with it, so the pod template changes and a rollout starts. Same data in a different key order gives the same hash because the script sorts keys.
- The dummy token `bm90LWEtcmVhbC10b2tlbg==` decodes to `not-a-real-token`: one line of Python, no key needed.

**Code:**
```yaml
# ---- config.yaml ----
apiVersion: v1
kind: ConfigMap
metadata:
  name: scorer-config
data:
  MODEL_URI: "models:/churn/Production"
  LOG_LEVEL: "info"
  THRESHOLD: "0.62"
---
apiVersion: v1
kind: Secret
metadata:
  name: scorer-secrets
type: Opaque
data:
  REGISTRY_TOKEN: bm90LWEtcmVhbC10b2tlbg==      # base64 of a dummy value
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scorer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: scorer
  template:
    metadata:
      labels:
        app: scorer
      annotations:
        checksum/config: "REPLACE_WITH_HASH_OF_CONFIGMAP_DATA"   # changes -> pod template changes -> rollout
    spec:
      containers:
        - name: scorer
          image: registry.example.com/ml/scorer:1.4.0
          envFrom:
            - configMapRef:
                name: scorer-config
          env:
            - name: REGISTRY_TOKEN
              valueFrom:
                secretKeyRef:
                  name: scorer-secrets
                  key: REGISTRY_TOKEN
          volumeMounts:
            - name: config-files
              mountPath: /etc/scorer
              readOnly: true
      volumes:
        - name: config-files
          configMap:
            name: scorer-config
```
```python
# ---- secret_demo.py ----
"""(1) base64 is not encryption, (2) hash of ConfigMap data -> pod-template annotation -> rollout trigger."""
import base64, hashlib, json, sys, yaml

docs = {d["kind"]: d for d in yaml.safe_load_all(open(sys.argv[1]))}

for k, v in docs["Secret"]["data"].items():
    print(f"{k}: stored as {v!r} -> decoded {base64.b64decode(v).decode()!r}   (anyone with get-secret RBAC can do this)")

def config_hash(cm):
    return hashlib.sha256(json.dumps(cm["data"], sort_keys=True).encode()).hexdigest()[:16]

cm = docs["ConfigMap"]
h1 = config_hash(cm)
cm["data"]["THRESHOLD"] = "0.70"                  # someone edits the threshold
h2 = config_hash(cm)
print("config hash before:", h1)
print("config hash after :", h2, "->", "template changes, Deployment rolls" if h1 != h2 else "no change")
print("same data, other key order:", config_hash({"data": dict(reversed(list(cm["data"].items())))}) == h2)

dep = docs["Deployment"]
dep["spec"]["template"]["metadata"]["annotations"]["checksum/config"] = h2
print("annotation now:", dep["spec"]["template"]["metadata"]["annotations"])
yaml.safe_dump_all(docs.values(), open("config.rendered.yaml", "w"), sort_keys=False)
```
```bash
# these ran (from the code/ folder of this answer):
kubernetes-validate --strict config.yaml
python3 -I secret_demo.py config.yaml
kubernetes-validate --strict config.rendered.yaml

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl apply -f config.rendered.yaml
# kubectl rollout restart deploy/scorer
```

**Output (my run):**
```text
$ kubernetes-validate --strict config.yaml
INFO config.yaml passed for resource configmap/scorer-config against version 1.37
INFO config.yaml passed for resource secret/scorer-secrets against version 1.37
INFO config.yaml passed for resource deployment/scorer against version 1.37

$ python3 -I secret_demo.py config.yaml
REGISTRY_TOKEN: stored as 'bm90LWEtcmVhbC10b2tlbg==' -> decoded 'not-a-real-token'   (anyone with get-secret RBAC can do this)
config hash before: 00131ed2432d8c33
config hash after : 8be2d7a7357668d7 -> template changes, Deployment rolls
same data, other key order: True
annotation now: {'checksum/config': '8be2d7a7357668d7'}

$ kubernetes-validate --strict config.rendered.yaml
INFO config.rendered.yaml passed for resource configmap/scorer-config against version 1.37
INFO config.rendered.yaml passed for resource secret/scorer-secrets against version 1.37
INFO config.rendered.yaml passed for resource deployment/scorer against version 1.37
```
Not executed: applying, `kubectl rollout restart`, kubelet file refresh, etcd encryption, external secret managers. What ran: kubernetes-validate 1.37.0 `--strict` on the manifest and on the regenerated manifest with the new annotation, base64 decoding, and the hash demo. The value in the Secret is a dummy.

**Follow-ups:**
- **Is `stringData` safer than `data`?** No. It is a write convenience; the stored result is the same base64.
- **How do you rotate a secret without downtime?** Update the Secret and roll pods with the same hash trick or an external-secret operator, keeping old and new credentials valid during the overlap.
- **ConfigMap vs baking config into the image?** ConfigMap lets one image run in dev and prod with different settings; baked config means a rebuild per change. Keep secrets out of images either way.

**Common mistakes:**
- Saying 'Secrets are encrypted'.
- Expecting pods to pick up a changed env ConfigMap.
- Putting real keys in a values file or manifest in git.
- Granting wide `get secrets` rights to CI service accounts.
- Using `subPath` and expecting live updates.

---

### Q8 ⭐⭐⭐ 🟡 Scheduling an ML pod onto a GPU node: nvidia.com/gpu requests, node selectors, taints and tolerations. Explain how the NVIDIA device plugin advertises GPUs to the kubelet as the extended resource nvidia.com/gpu, why GPUs go only in limits (requests default to the limit) and cannot be fractionally requested in the default setup, why GPU nodes are usually tainted so ordinary pods do not waste them, and how a toleration plus a nodeSelector (or node affinity) steers training and serving pods. Show a Deployment spec and a node taint command, and write a script that checks whether a pod spec would tolerate a node's taints. No GPU or cluster here, so scheduling is not executed.
**Asked at:** Kubernetes-for-AI question bank (Cloud Soft Solutions 'Kubernetes for AI interview questions'), NerdLevelTech MLOps interview course page, KodeKloud MLOps guide, SuperOrbital/CNCF NVIDIA device plugin post, NVIDIA GPU Operator time-slicing docs (v1.11 page only), University of Bergen RAIL GPU docs; search snippets only, not opened (WebFetch failed with ENOTFOUND); guides and docs, not verified candidate reports; GPU and deep-learning MLOps roles at product companies, GCCs and AI startups
**Say this first (1 line):** The device plugin advertises GPUs as the extended resource nvidia.com/gpu, you ask for whole GPUs under limits, the GPU nodes are tainted so ordinary pods stay off, and your pod carries a toleration plus a nodeSelector to land there.

**Then explain:**
- **Device plugin.** A DaemonSet (often installed by the NVIDIA GPU Operator) runs on GPU nodes and tells the kubelet how many `nvidia.com/gpu` the node has. The scheduler then treats that like any other countable resource. Versions and install methods change: check current NVIDIA docs.
- **Limits, whole numbers.** Extended resources cannot be overcommitted: you write them under `limits` (a request, if set, must equal the limit; if only limit is set, request defaults to it). Only integers: `0.5` is invalid. Sharing one GPU needs time-slicing (no memory or fault isolation between pods) or MIG (hardware partitions with their own resource names such as `nvidia.com/mig-1g.10gb`), both configured by the platform.
- **Taints keep the pool clean.** A taint such as `nvidia.com/gpu=present:NoSchedule` stops web pods and cron jobs from occupying expensive nodes. Many managed Kubernetes offerings add this taint to GPU pools by themselves (check yours).
- **Steering.** Toleration says 'I am allowed there'. It does not attract the pod. A nodeSelector or node affinity says 'I want nodes with this label'. For GPU pods you want both, plus the GPU resource request, which itself already limits placement to nodes that advertise GPUs.
- **Failure modes.** Toleration key typo: pod Pending with 'untolerated taint'. Label missing: Pending with 'didn't match node selector'. GPU requested but driver or plugin pod not running: node shows 0 GPUs, Pending 'Insufficient nvidia.com/gpu'. A tolerating CPU-only pod can still land on a GPU node, because a toleration does not require a GPU.

**Example:** Node `gpu-node-1` has taint `nvidia.com/gpu=present:NoSchedule` and label `pool=gpu`.
- Pod has toleration `key nvidia.com/gpu, operator Exists, effect NoSchedule`: tolerated. With `Exists` the value is ignored.
- `spot-gpu-2` also carries a `spot=true:NoSchedule` taint: **every** NoSchedule taint must be tolerated, so this pod is blocked by `spot`.
- `PreferNoSchedule` is a soft hint, so it does not block.
- The script also rejects `0.5` GPUs and a GPU only in requests.

**Code:**
```yaml
# ---- gpu-serving.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: embed-gpu
spec:
  replicas: 1
  selector:
    matchLabels:
      app: embed-gpu
  template:
    metadata:
      labels:
        app: embed-gpu
    spec:
      nodeSelector:
        pool: gpu                      # a label YOU put on GPU nodes (cloud pools often add their own)
      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule
      containers:
        - name: server
          image: registry.example.com/ml/embed-server:3.0.0
          resources:
            requests:
              cpu: "2"
              memory: 8Gi
            limits:
              memory: 8Gi
              nvidia.com/gpu: 1         # whole GPUs only; goes in limits
```
```python
# ---- tolerates.py ----
"""Would this pod tolerate these node taints? Mirrors the Kubernetes matching rules (NoSchedule/NoExecute)."""
import sys, yaml

def tol_matches(tol, taint):
    if tol.get("effect") and tol["effect"] != taint["effect"]:
        return False
    op = tol.get("operator", "Equal")
    if op == "Exists":
        return not tol.get("key") or tol["key"] == taint["key"]     # empty key + Exists matches all
    return tol.get("key") == taint["key"] and tol.get("value", "") == taint.get("value", "")

def tolerates(pod_spec, taints):
    blocking = [t for t in taints if t["effect"] in ("NoSchedule", "NoExecute")
                and not any(tol_matches(x, t) for x in pod_spec.get("tolerations", []))]
    return not blocking, blocking

def check_gpu(pod_spec):
    errs = []
    for c in pod_spec["containers"]:
        r = c.get("resources", {})
        lim, req = r.get("limits", {}), r.get("requests", {})
        g = lim.get("nvidia.com/gpu", req.get("nvidia.com/gpu"))
        if g is None:
            continue
        if not str(g).isdigit():
            errs.append(f"{c['name']}: GPU count {g!r} must be a whole number")
        if "nvidia.com/gpu" in req and "nvidia.com/gpu" not in lim:
            errs.append(f"{c['name']}: GPU in requests without limits is rejected")
        if "nvidia.com/gpu" in req and "nvidia.com/gpu" in lim and str(req["nvidia.com/gpu"]) != str(lim["nvidia.com/gpu"]):
            errs.append(f"{c['name']}: GPU request must equal limit")
    return errs

if __name__ == "__main__":
    dep = next(yaml.safe_load_all(open(sys.argv[1])))
    spec = dep["spec"]["template"]["spec"]
    nodes = {
        "gpu-node-1":  [{"key": "nvidia.com/gpu", "value": "present", "effect": "NoSchedule"}],
        "cpu-node-1":  [],
        "spot-gpu-2":  [{"key": "nvidia.com/gpu", "value": "present", "effect": "NoSchedule"},
                        {"key": "spot", "value": "true", "effect": "NoSchedule"}],
        "pref-node-3": [{"key": "nvidia.com/gpu", "value": "present", "effect": "PreferNoSchedule"}],
    }
    for n, taints in nodes.items():
        ok, why = tolerates(spec, taints)
        print(f"{n:12s} taints={len(taints)} tolerated={ok}", "" if ok else f"blocked by {[t['key'] for t in why]}")
    print("node label match for nodeSelector pool=gpu is a separate check (labels, not taints)")
    print("GPU spec errors:", check_gpu(spec) or "none")
    bad = {"containers": [{"name": "c", "resources": {"requests": {"nvidia.com/gpu": "0.5"}}}]}
    print("fractional/request-only case:", check_gpu(bad))
```
```bash
# these ran (from the code/ folder of this answer):
kubernetes-validate --strict gpu-serving.yaml
python3 -I tolerates.py gpu-serving.yaml

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl taint nodes gpu-node-1 nvidia.com/gpu=present:NoSchedule
# kubectl label nodes gpu-node-1 pool=gpu
# kubectl apply -f gpu-serving.yaml
# kubectl describe node gpu-node-1 | grep -A8 Allocatable
# Node taint and label commands (not executed): `kubectl taint nodes gpu-node-1 nvidia.com/gpu=present:NoSchedule` and `kubectl label nodes gpu-node-1 pool=gpu`.
```

**Output (my run):**
```text
$ kubernetes-validate --strict gpu-serving.yaml
INFO gpu-serving.yaml passed for resource deployment/embed-gpu against version 1.37

$ python3 -I tolerates.py gpu-serving.yaml
gpu-node-1   taints=1 tolerated=True 
cpu-node-1   taints=0 tolerated=True 
spot-gpu-2   taints=2 tolerated=False blocked by ['spot']
pref-node-3  taints=1 tolerated=True 
node label match for nodeSelector pool=gpu is a separate check (labels, not taints)
GPU spec errors: none
fractional/request-only case: ["c: GPU count '0.5' must be a whole number", 'c: GPU in requests without limits is rejected']
```
Not executed: tainting nodes, the device plugin, any GPU scheduling (no GPU and no cluster here). What ran: kubernetes-validate 1.37.0 `--strict` on the Deployment (note: it accepts `nvidia.com/gpu: 1` because extended resource names are free text), and `tolerates.py`, which implements the documented toleration rules for NoSchedule/NoExecute and my GPU-field checks. It ignores `tolerationSeconds`.

**Follow-ups:**
- **Can two pods share one GPU?** Not with the default plugin. Use time-slicing (no isolation) or MIG on supported GPUs, set up by the platform team; check current NVIDIA docs.
- **Why does my CPU-only pod run on a GPU node?** It tolerates the taint (or the pool has none). Taints repel; they do not reserve. Add node affinity away from GPU nodes for those pods.
- **How do you scale GPU nodes to zero?** Cluster autoscaler or Karpenter-style tools on a GPU pool; cold start includes node boot, driver and image pull (check provider docs).

**Common mistakes:**
- Putting `nvidia.com/gpu` only under requests, or asking for a fraction.
- Toleration without a nodeSelector or GPU request: pod may land on a CPU node (if untainted) or not at all.
- Forgetting that a taint on the node with `effect: NoExecute` also evicts running pods.
- Assuming the cloud adds the taint, then discovering web pods eating GPU nodes.

---

### Q9 ⭐⭐⭐ 🟡 Horizontal Pod Autoscaler (HPA) for a CPU-bound inference service. Explain the scaling formula (desired = ceil(current replicas x current metric / target metric)), why requests must be set for CPU utilisation targets, the metrics-server dependency, min and max replicas, stabilisation windows and scale-down behaviour, and why CPU is a poor signal for a GPU-bound or queue-bound model. Work one example by hand (4 pods at 90 percent CPU, target 60 percent) and give an autoscaling/v2 manifest with a behavior block. Include a Python function that simulates the HPA formula with tolerance and clamping and run it; the live autoscaler is not executed.
**Asked at:** Autoscaling write-ups (techinterview.org 'System Design Interview: Kubernetes Autoscaling (HPA, VPA, KEDA, Cluster Autoscaler)', AWS EKS ML inference autoscaling HPA and KEDA guide, CloudNativeNow KEDA articles, dev.to VPA/HPA/KEDA patterns; search snippets only, not opened); editorial and vendor docs, not verified candidate reports; senior MLOps and platform loops
**Say this first (1 line):** HPA computes desired replicas = ceil(current replicas x current metric / target metric), clamps it between min and max, ignores small deviations, and scales down slowly with a stabilisation window.

**Then explain:**
- **Formula.** `desired = ceil(current x currentMetric / targetMetric)`. If the ratio is within a tolerance of 1.0 (default 10 percent; check your version) nothing changes. Result is clamped to `minReplicas`..`maxReplicas`. The controller syncs about every 15 s by default (cluster setting).
- **Requests must exist.** CPU Utilization is usage divided by the container's **request**. No request, no percentage: the HPA reports unknown and does nothing. Pods with several containers: every container needs a request. Also needs metrics-server (or another metrics API provider); without it you see `<unknown>` targets.
- **Behaviour block.** `scaleUp` can be quick (no wait, double each minute in the example). `scaleDown` uses a stabilisation window: it picks the highest recommendation over the window (300 s here), so a short dip does not kill pods you will need again. `policies` cap how many pods or what percent can change per period.
- **Why CPU is a poor signal for model servers.** A GPU-bound model can be saturated at low CPU. A queue-bound or batching server has latency growing while CPU is flat. Cold starts are slow, so reacting late hurts. Better signals: requests in flight, queue length, GPU utilisation, or latency, via custom/external metrics or KEDA (see the autoscaling Qs in this part).
- **Failure modes.** Request set too low: utilisation reads 300 percent and HPA hits max. Not-ready pods and fresh pods are treated specially (pods without metrics are treated conservatively, which damps the change; check the HPA docs for details). HPA and a manually set `replicas` in the Deployment fight each other on every apply. Max replicas larger than quota or GPU capacity: new pods Pending.

**Example:** By hand: 4 pods at 90 percent, target 60 percent. Ratio 1.5, 4 x 1.5 = 6, so desired 6 (inside min 2..max 10).
- 4 pods at 63 percent: ratio 1.05, inside the 10 percent dead band, stay at 4.
- 8 pods at 150 percent: raw 20, capped at 10.
- 4 pods at 10 percent: raw 1, floor 2.
- Time series in the output: a spike to 6 cores of demand takes the pods to 10; when demand drops to 1.2 cores the recommendation is 2 at once, but replicas stay at 10 until the 5-step window forgets the high values. The simulation's step is abstract (not 15 s), and it leaves out the scaleDown `policies` limit and pod start-up time.

**Code:**
```yaml
# ---- hpa.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: infer-cpu
spec:
  replicas: 4
  selector:
    matchLabels:
      app: infer-cpu
  template:
    metadata:
      labels:
        app: infer-cpu
    spec:
      containers:
        - name: server
          image: registry.example.com/ml/infer-cpu:1.0.0
          resources:
            requests:
              cpu: "1"                 # utilisation % is measured against THIS
              memory: 2Gi
            limits:
              memory: 2Gi
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: infer-cpu
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: infer-cpu
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Pods
          value: 1
          periodSeconds: 60
```
```python
# ---- hpa_sim.py ----
"""HPA formula with tolerance, min/max clamp and a scale-down stabilisation window."""
import math

def desired(current, metric, target, tol=0.10, lo=2, hi=10):
    ratio = metric / target
    if abs(ratio - 1.0) <= tol:                 # inside the dead band: do nothing
        d = current
    else:
        d = math.ceil(current * ratio)
    return max(lo, min(hi, d))

print("hand example: 4 pods, 90% vs 60% ->", desired(4, 90, 60))          # ceil(4*1.5)=6
print("tolerance   : 4 pods, 63% vs 60% ->", desired(4, 63, 60), "(ratio 1.05, no change)")
print("clamp high  : 8 pods, 150% vs 60% ->", desired(8, 150, 60), "(raw 20, capped at max 10)")
print("clamp low   : 4 pods, 10% vs 60% ->", desired(4, 10, 60), "(raw 1, floor at min 2)")

def run(cpu_per_pod_total, window=5, steps=14):
    """cpu_per_pod_total[t] = total CPU demand in 'cores' at step t; each pod requests 1 core; target 60%."""
    cur, recs, log = 4, [], []
    for t, demand in enumerate(cpu_per_pod_total[:steps]):
        util = 100 * demand / cur                  # average utilisation vs request
        rec = desired(cur, util, 60)
        recs.append(rec)
        # scale-up uses the newest recommendation; scale-down uses the MAX over the window
        new = rec if rec > cur else min(cur, max(recs[-window:]))
        log.append((t, round(util), rec, new))
        cur = new
    return log

demand = [3.6]*3 + [6.0]*3 + [1.2]*8          # spike, then quiet
print("t  util%  rec  replicas_after")
for t, u, r, n in run(demand):
    print(f"{t:<2d} {u:<5d}  {r:<3d}  {n}")
```
```bash
# these ran (from the code/ folder of this answer):
kubernetes-validate --strict hpa.yaml
python3 -I hpa_sim.py

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl apply -f hpa.yaml
# kubectl get hpa infer-cpu -w
# kubectl top pods   # needs metrics-server
```

**Output (my run):**
```text
$ kubernetes-validate --strict hpa.yaml
INFO hpa.yaml passed for resource deployment/infer-cpu against version 1.37
INFO hpa.yaml passed for resource horizontalpodautoscaler/infer-cpu against version 1.37

$ python3 -I hpa_sim.py
hand example: 4 pods, 90% vs 60% -> 6
tolerance   : 4 pods, 63% vs 60% -> 4 (ratio 1.05, no change)
clamp high  : 8 pods, 150% vs 60% -> 10 (raw 20, capped at max 10)
clamp low   : 4 pods, 10% vs 60% -> 2 (raw 1, floor at min 2)
t  util%  rec  replicas_after
0  90     6    6
1  60     6    6
2  60     6    6
3  100    10   10
4  60     10   10
5  60     10   10
6  12     2    10
7  12     2    10
8  12     2    10
9  12     2    10
10 12     2    2
11 60     2    2
12 60     2    2
13 60     2    2
```
Not executed: the real HPA, metrics-server, and applying the manifest (no cluster). What ran: kubernetes-validate 1.37.0 `--strict` on the Deployment and the `autoscaling/v2` HPA, and `hpa_sim.py`, my model of the documented formula, tolerance, clamp and a simplified window. It is a teaching model; the real controller has more rules (readiness handling, multiple metrics, policies).

**Follow-ups:**
- **HPA vs VPA vs cluster autoscaler?** HPA changes replica count. VPA changes requests and limits (often needs pod restarts; do not run it on the same CPU/memory metric as HPA). Cluster autoscaler adds or removes nodes for Pending pods.
- **Can HPA scale to zero?** Not in the standard setup (minReplicas must be 1 or more unless a feature gate is on; check your version). KEDA is the usual route.
- **Multiple metrics?** HPA computes a desired count per metric and takes the largest.

**Common mistakes:**
- HPA on CPU without a CPU request.
- Letting Git or Helm keep resetting `spec.replicas`.
- Using CPU for a GPU or queue-bound model.
- Scale-down window of zero, causing flapping.
- Max replicas that the nodes or quota cannot hold.

---

### Q10 ⭐⭐⭐ 🟡 Rolling updates, rollbacks and canary releases for a new model version on Kubernetes. Explain maxSurge and maxUnavailable, how readiness gates a rollout, kubectl rollout status, history and undo, why a bad model that still passes readiness is the real danger, and how to do a canary with plain Kubernetes (two Deployments behind one Service, traffic proportional to replica count) versus an ingress or service-mesh weight split or KServe canaryTrafficPercent. Give manifests and a script that computes how many pods roll at once for given maxSurge and maxUnavailable. The rollout itself is not executed here.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A rolling update swaps pods in steps bounded by maxSurge and maxUnavailable and only counts a new pod when it is Ready, so readiness is the gate, but a bad model that still answers 200 passes the gate and needs a canary with real metrics.

**Then explain:**
- **The two knobs.** `maxSurge` = how many extra pods above desired may exist during the update. `maxUnavailable` = how many below desired may be unready. Percentages: surge rounds up, unavailable rounds down. They cannot both be zero. Defaults are 25 percent each (check docs for your version). Example 10 replicas: surge 3, unavailable 2, so between 8 and 13 pods.
- **Readiness gates the rollout.** The controller creates new pods, waits for Ready, then removes old ones. If new pods never become Ready, the rollout stalls with old pods still serving (after `progressDeadlineSeconds` it is marked failed but nothing is rolled back by itself).
- **Commands (not executed here).** `kubectl rollout status deploy/x`, `kubectl rollout history deploy/x`, `kubectl rollout undo deploy/x [--to-revision=N]`. Undo makes the Deployment use the previous ReplicaSet's template again.
- **The real danger.** A model that loads, answers 200, and returns bad predictions passes readiness and the rollout completes. Readiness proves liveness of serving, not quality. You catch it with a canary plus metrics (error rate, latency, prediction distribution, business proxy; see Part 8) and an easy rollback.
- **Canary options.** Plain Kubernetes: two Deployments behind one Service whose selector matches both; traffic split follows replica ratio (roughly, since connection reuse skews it, and you cannot do 1 percent without 100 pods). Ingress or service mesh: weighted routing, exact percentages (check your controller's docs). KServe: `canaryTrafficPercent` on the predictor (check current KServe docs for the schema); also header routing in meshes.
- **Failure modes.** `maxUnavailable: 0` with no spare quota: surge pods Pending, rollout stuck. GPU models: surge needs a free GPU per extra pod; with no spare GPU set `maxSurge: 0, maxUnavailable: 1` and accept reduced capacity. Large models: every new pod loads weights, so a big surge makes a slow, expensive rollout.

**Example:** Rolling, 4 replicas, maxSurge 1, maxUnavailable 0: at most 5 pods, at least 4 ready. Steps: 1 new created, once ready 1 old removed, repeat: the output shows old 4,3,3,2,2,1,1,0 and new 1,1,2,2,3,3,4,4.
- If the new pods never become Ready, old stays 4 forever: stuck, but still serving.
- Canary: 9 stable plus 1 canary pods behind one Service: about 10 percent of requests hit the canary. Scale to 8+2 for 20 percent.

**Code:**
```yaml
# ---- rollout.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: churn
      track: stable
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: churn
        track: stable
    spec:
      containers:
        - name: api
          image: registry.example.com/ml/churn:1.0.0
          ports:
            - name: http
              containerPort: 8000
          readinessProbe:
            httpGet:
              path: /ready
              port: http
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: churn
      track: canary
  template:
    metadata:
      labels:
        app: churn
        track: canary
    spec:
      containers:
        - name: api
          image: registry.example.com/ml/churn:1.1.0
          ports:
            - name: http
              containerPort: 8000
          readinessProbe:
            httpGet:
              path: /ready
              port: http
---
apiVersion: v1
kind: Service
metadata:
  name: churn
spec:
  selector:
    app: churn                  # no 'track' key: both Deployments sit behind one Service
  ports:
    - name: http
      port: 80
      targetPort: http

# ---- kserve-canary.yaml ----
# KServe CRD: field names from memory of the docs; check current KServe docs. Not schema-validated here.
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: churn
spec:
  predictor:
    canaryTrafficPercent: 10
    model:
      modelFormat:
        name: sklearn
      storageUri: s3://example-bucket/models/churn/v2
```
```python
# ---- rollout_math.py ----
"""maxSurge / maxUnavailable arithmetic and a tick-by-tick rollout sketch."""
import math, sys, yaml

def resolve(v, replicas, round_up):
    if isinstance(v, str) and v.endswith("%"):
        x = replicas * int(v[:-1]) / 100
        return math.ceil(x) if round_up else math.floor(x)      # surge rounds up, unavailable rounds down
    return int(v)

def limits(replicas, surge="25%", unavail="25%"):
    s, u = resolve(surge, replicas, True), resolve(unavail, replicas, False)
    if s == 0 and u == 0:
        raise ValueError("both zero: rollout can never make progress (API rejects it)")
    return s, u, replicas + s, replicas - u        # surge, unavailable, max total, min available

def simulate(replicas, surge, unavail, new_is_ready=True):
    s, u, max_total, min_avail = limits(replicas, surge, unavail)
    old, new, new_ready, ticks = replicas, 0, 0, []
    for t in range(1, 40):
        new_ready = new if new_is_ready else 0
        new += max(0, min(replicas - new, max_total - (old + new)))          # create new pods up to surge
        ready_now = old + new_ready                                           # old are ready, new count when ready
        old -= max(0, min(old, ready_now - min_avail))                        # delete old while availability allows
        ticks.append((t, old, new, old + new_ready))
        if old == 0 and new == replicas:
            break
    return ticks

for r, s, u in [(10, "25%", "25%"), (4, 1, 0), (3, "25%", "25%"), (9, "25%", 0)]:
    su, un, mt, ma = limits(r, s, u)
    print(f"replicas={r} maxSurge={s} maxUnavailable={u}: surge={su} unavailable={un} max_total={mt} min_available={ma}")

print("\nrollout 4 replicas, maxSurge=1, maxUnavailable=0 (tick, old, new_created, ready)")
for row in simulate(4, 1, 0):
    print(row)
print("\nbad model whose pods never become Ready (4 replicas, surge 1, unavail 0): first ticks")
for row in simulate(4, 1, 0, new_is_ready=False)[:4]:
    print(row, "<- old pods kept, rollout stuck")
print("\ncanary split by replica count: 9 stable + 1 canary ->", 1 / (9 + 1) * 100, "% of requests (roughly, per-connection)")

docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if d]
canary = docs[0]
print("kserve file parses; canaryTrafficPercent =", canary["spec"]["predictor"]["canaryTrafficPercent"])
```
```bash
# these ran (from the code/ folder of this answer):
kubernetes-validate --strict rollout.yaml
python3 -I rollout_math.py kserve-canary.yaml

# NOT EXECUTED here (no cluster, no kubectl):
# kubectl apply -f rollout.yaml
# kubectl rollout status deploy/churn-stable
# kubectl rollout history deploy/churn-stable
# kubectl rollout undo deploy/churn-stable
```

**Output (my run):**
```text
$ kubernetes-validate --strict rollout.yaml
INFO rollout.yaml passed for resource deployment/churn-stable against version 1.37
INFO rollout.yaml passed for resource deployment/churn-canary against version 1.37
INFO rollout.yaml passed for resource service/churn against version 1.37

$ python3 -I rollout_math.py kserve-canary.yaml
replicas=10 maxSurge=25% maxUnavailable=25%: surge=3 unavailable=2 max_total=13 min_available=8
replicas=4 maxSurge=1 maxUnavailable=0: surge=1 unavailable=0 max_total=5 min_available=4
replicas=3 maxSurge=25% maxUnavailable=25%: surge=1 unavailable=0 max_total=4 min_available=3
replicas=9 maxSurge=25% maxUnavailable=0: surge=3 unavailable=0 max_total=12 min_available=9

rollout 4 replicas, maxSurge=1, maxUnavailable=0 (tick, old, new_created, ready)
(1, 4, 1, 4)
(2, 3, 1, 4)
(3, 3, 2, 4)
(4, 2, 2, 4)
(5, 2, 3, 4)
(6, 1, 3, 4)
(7, 1, 4, 4)
(8, 0, 4, 4)

bad model whose pods never become Ready (4 replicas, surge 1, unavail 0): first ticks
(1, 4, 1, 4) <- old pods kept, rollout stuck
(2, 4, 1, 4) <- old pods kept, rollout stuck
(3, 4, 1, 4) <- old pods kept, rollout stuck
(4, 4, 1, 4) <- old pods kept, rollout stuck

canary split by replica count: 9 stable + 1 canary -> 10.0 % of requests (roughly, per-connection)
kserve file parses; canaryTrafficPercent = 10
```
Not executed: the rollout, rollout status/history/undo, the canary and KServe (no cluster, no KServe). What ran: kubernetes-validate 1.37.0 `--strict` on the three core objects; the arithmetic and tick model in `rollout_math.py` (my simplification of the Deployment controller); and a YAML parse (only) of the KServe file, since the validator ships core schemas and not that CRD. The KServe field names come from memory of its docs and snippets: check current docs.

**Follow-ups:**
- **Rollout undo, but the old model is gone from the registry?** The old ReplicaSet keeps the old image reference, so undo needs that image and model artifact to still exist. Pin immutable tags and keep artifacts.
- **Where does `minReadySeconds` help?** It makes a pod stay Ready for N seconds before counting, catching crashes right after readiness turns green.
- **Why is rollback not enough for a bad model?** Because nobody notices without metrics. You need alerts on quality proxies and a canary before 100 percent.

**Common mistakes:**
- Treating a finished rollout as proof the model is good.
- `maxUnavailable: 0` and `maxSurge: 0` together (rejected).
- Using `latest` tags, so undo does not return to what ran before.
- Expecting an exact traffic percent from replica counts.
- Selector on the Service containing the `track` label, which splits canary from stable and removes one.

---
