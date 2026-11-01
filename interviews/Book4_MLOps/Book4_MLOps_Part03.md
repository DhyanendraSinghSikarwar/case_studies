# Book 4 — Part 3: Kubernetes basics for ML, Helm and autoscaling

**Topic:** running ML on Kubernetes: pods, Deployments, Services, Ingress, ConfigMaps and Secrets, requests and limits, probes, GPU scheduling and the device plugin, node selectors, taints and tolerations, Jobs and CronJobs for training, HPA, VPA, KEDA and cluster autoscaling, PVCs, namespaces and RBAC, rolling and canary updates, Helm charts, values and templating, debugging CrashLoopBackOff, OOMKilled and Pending, KServe and Kubeflow at concept level
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 15, ⭐⭐ 16, ⭐ 9)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 2 owns Docker images; Part 5 owns pipeline orchestration (Airflow, Kubeflow Pipelines detail); Part 6 owns serving frameworks (FastAPI, Triton, BentoML); Part 7 owns CI/CD design; Part 8 owns model monitoring; Parts 10 and 11 own AWS, Azure and GCP services; Part 12 owns cost and system design in depth; Book 2 owns LLM serving internals; Book 3 owns SQL; Book 6 owns product and business.

Evidence limits: the free pages found could not be opened (WebFetch failed with getaddrinfo ENOTFOUND), so every source is a search snippet only (see research_notes/Book4_Part03_sources.md). No page was found that reports exact Kubernetes questions asked by a named company at an India or global ML role; 'Asked at' tags therefore name source types (editorial guides, docs, job postings), not verified company reports. Execution limit: there is no cluster, kubectl or helm in this sandbox. Wave B can really run YAML parsing, the kubernetes-validate Python library (offline schema check, tested with Kubernetes 1.30 and 1.37 schemas) and pure-Python simulations; everything that needs a cluster or helm must be labelled 'not executed'.

---

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

### Q11 ⭐⭐⭐ 🟡 Helm basics for an ML platform: chart, release, values and templates. Explain the chart folder layout (Chart.yaml, values.yaml, templates/, _helpers.tpl), what helm install, upgrade, rollback, template and lint each do, how values are merged (chart defaults, then -f files, then --set), release revisions stored as Secrets in the namespace, and why Helm 3 has no Tiller. Write a small chart for a model server (Deployment, Service, ConfigMap) with image tag, replicas, resources and GPU as values, and a Python script that mimics value merging. helm is not installed and could not be downloaded here, so helm commands are not executed; show what to run and what to expect, hedged.
**Asked at:** Editorial Helm interview guides (KodeKloud, Hyring, TechPrep '213 Helm interview questions', ClimbTheLadder, InterviewPrep.org, OneUptime Helm rollback guide; search snippets only, not opened); guides, not verified candidate reports; DevOps and MLOps screens
**Say this first (1 line):** A Helm chart is a folder of templates plus default values; a release is one installed copy of it in a cluster, and Helm keeps every revision so you can roll back.

**Then explain:**
- **Chart layout.** `Chart.yaml` (name, chart version, appVersion), `values.yaml` (defaults), `templates/` (YAML with Go-template holes), `_helpers.tpl` (named snippets such as a shared name). `charts/` holds sub-charts.
- **The commands.** `helm lint` checks the chart. `helm template` renders YAML on your laptop, no cluster. `helm install` renders and creates a release. `helm upgrade` renders again and applies a new revision. `helm rollback N` makes a NEW revision with the content of revision N. Add `--atomic` or `--wait` so a failed upgrade is not left half done (check `helm upgrade --help`).
- **Values order, lowest to highest.** Chart `values.yaml`, then each `-f file` in the order given, then `--set`. Maps merge key by key. Scalars and lists are replaced whole. `--set` turns `true`, `null` and plain integers into non-strings, so a tag like `20260101` becomes a number (quote it in the template, or use `--set-string`).
- **Where state lives.** Helm 3 has no Tiller (the in-cluster server of Helm 2). The client talks to the API server with your kubeconfig, and each revision is saved as a Secret named like `sh.helm.release.v1.<release>.v<N>` in the release namespace (default storage driver). So RBAC on that namespace is what protects releases. Helm 4 exists; the basics here carry over, but check its release notes.
- **ML-platform failure modes.** Values drift (someone `kubectl edit`s a live Deployment and the next upgrade overwrites it). `--reuse-values` on upgrade hides new chart defaults. A bad model that still passes readiness is NOT undone by `rollback` unless the image tag was in the chart values. A rollback does not touch a database or PVC contents. Huge rendered manifests can hit the size limit of a stored release; keep big files out of templates.

**Example:** Hand-check the merge. Defaults: `replicaCount: 2`, memory limit `2Gi`, tag `1.4.1`, gpu off. `prod.yaml` sets replicas 3, gpu on, memory limit `8Gi`. Command adds `--set image.tag=1.4.2 --set replicaCount=5`. Result: replicas **5** (`--set` wins), memory limit **8Gi** (file beats default), memory request still `1Gi` (a map merges, untouched keys survive), tag **1.4.2**, and the rendered Deployment gains `nvidia.com/gpu: 1` plus a GPU toleration. With default values there are 0 lines mentioning nvidia.

**Code:**
```yaml
# ---- chart/modelserver/Chart.yaml ----
apiVersion: v2
name: modelserver
description: A small chart for one model-serving Deployment
type: application
version: 0.1.0        # version of the chart itself
appVersion: "1.4.2"   # version of the app inside (informational)

# ---- chart/modelserver/values.yaml ----
replicaCount: 2
image:
  repository: registry.example.com/ml/churn-model
  tag: "1.4.1"
service:
  port: 80
  targetPort: 8080
readiness:
  path: /ready
resources:
  requests:
    cpu: "500m"
    memory: 1Gi
  limits:
    memory: 2Gi
gpu:
  enabled: false
  count: 1
config:
  MODEL_NAME: churn
  LOG_LEVEL: info

# ---- chart/modelserver/templates/_helpers.tpl ----
{{- define "modelserver.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}

# ---- chart/modelserver/templates/configmap.yaml ----
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "modelserver.fullname" . }}
data:
  MODEL_NAME: {{ .Values.config.MODEL_NAME | quote }}
  LOG_LEVEL: {{ .Values.config.LOG_LEVEL | quote }}

# ---- chart/modelserver/templates/service.yaml ----
apiVersion: v1
kind: Service
metadata:
  name: {{ include "modelserver.fullname" . }}
spec:
  selector:
    app.kubernetes.io/name: {{ .Chart.Name }}
    app.kubernetes.io/instance: {{ .Release.Name }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}

# ---- chart/modelserver/templates/deployment.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "modelserver.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Chart.Name }}
      app.kubernetes.io/instance: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ .Chart.Name }}
        app.kubernetes.io/instance: {{ .Release.Name }}
    spec:
      containers:
        - name: server
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.targetPort }}
          envFrom:
            - configMapRef:
                name: {{ include "modelserver.fullname" . }}
          readinessProbe:
            httpGet:
              path: {{ .Values.readiness.path }}
              port: {{ .Values.service.targetPort }}
          resources:
            requests:
              cpu: {{ .Values.resources.requests.cpu | quote }}
              memory: {{ .Values.resources.requests.memory }}
            limits:
              memory: {{ .Values.resources.limits.memory }}
              {{- if .Values.gpu.enabled }}
              nvidia.com/gpu: {{ .Values.gpu.count }}
              {{- end }}
      {{- if .Values.gpu.enabled }}
      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule
      {{- end }}

# ---- prod.yaml ----
replicaCount: 3
gpu:
  enabled: true
  count: 1
resources:
  limits:
    memory: 8Gi
```

```python
# ---- helm_mimic.py ----
"""Helm mimic (teaching illustration, NOT helm): value merging + a tiny `helm template`.
Render supports ONLY what the chart uses: {{ .Values.a.b }}, {{ .Release.Name }}, {{ .Chart.Name }},
| quote, include "modelserver.fullname", and {{- if .Values.x }} ... {{- end }}.
Usage: helm_mimic.py values | helm_mimic.py CHART [-f file] [--set a.b=c] [--release name]"""
import re, sys, glob, os, copy
import yaml

import copy

def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if v is None:                       # null in an override deletes the key
            out.pop(k, None)
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)  # maps merge key by key
        else:
            out[k] = copy.deepcopy(v)       # scalars AND lists are replaced whole
    return out

def typed(s):
    """--set value typing: true/false/null/integers are converted, the rest stay strings."""
    if s.lower() == "true": return True
    if s.lower() == "false": return False
    if s.lower() == "null": return None
    if s.isdigit() and not (len(s) > 1 and s[0] == "0"): return int(s)
    return s

def parse_set(expr):
    path, _, raw = expr.partition("=")
    tree = cur = {}
    keys = path.split(".")
    for k in keys[:-1]:
        cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = typed(raw)
    return tree

def compute_values(defaults, files=(), sets=()):
    vals = defaults
    for f in files:
        vals = deep_merge(vals, f)
    for s in sets:
        vals = deep_merge(vals, parse_set(s))
    return vals


TOKEN = re.compile(r"(\s*)\{\{(-?)\s*(.*?)\s*\}\}")

def lookup(ctx, path):
    cur = ctx
    for part in path.strip(".").split("."):
        cur = cur[part]
    return cur

def scalar(v):
    if v is True: return "true"
    if v is False: return "false"
    return str(v)

def evaluate(expr, ctx):
    quote = False
    if "|" in expr:
        expr, filt = [x.strip() for x in expr.split("|", 1)]
        assert filt == "quote", filt
        quote = True
    if expr.startswith("include"):
        assert '"modelserver.fullname"' in expr
        val = f'{ctx["Release"]["Name"]}-{ctx["Chart"]["Name"]}'
    else:
        val = scalar(lookup(ctx, expr))
    return f'"{val}"' if quote else val

def render(text, ctx):
    out, pos, stack = [], 0, []          # stack of "is this branch active"
    for m in TOKEN.finditer(text):
        ws, trim, expr = m.group(1), m.group(2), m.group(3)
        active = all(stack)
        if active:
            out.append(text[pos:m.start()])
            if not trim:
                out.append(ws)           # '{{-' removes the whitespace before it
        pos = m.end()
        if expr.startswith("define") or expr == "end" and stack == []:
            continue
        if expr.startswith("if "):
            stack.append(bool(lookup(ctx, expr[3:])))
        elif expr == "end":
            stack.pop()
        elif active:
            out.append(evaluate(expr, ctx))
    if all(stack):
        out.append(text[pos:])
    return "".join(out)

def values_demo():
    defaults = yaml.safe_load(open("chart/modelserver/values.yaml"))
    prod = yaml.safe_load(open("prod.yaml"))
    v = compute_values(defaults, [prod], ["image.tag=1.4.2", "replicaCount=5"])
    print("replicaCount :", v["replicaCount"], "(default 2, prod.yaml 3, --set 5 wins)")
    print("limits       :", v["resources"]["limits"], "(prod.yaml replaced memory)")
    print("requests kept:", v["resources"]["requests"], "(maps merge, untouched keys survive)")
    print("gpu          :", v["gpu"])
    print("--set typing :", {k: parse_set(k + "=" + s)[k] for k, s in [("a", "20260101"), ("b", "true"), ("c", "1.10"), ("d", "007")]})
    print("list replace :", compute_values({"args": ["--a", "--b"]}, [{"args": ["--c"]}]))
    print("null deletes :", compute_values({"gpu": {"enabled": True}, "x": 1}, [{"x": None}]))

def main(argv):
    if argv[1] == 'values':
        return values_demo()
    chart = argv[1]
    files, sets, release = [], [], "release-name"
    i = 2
    while i < len(argv):
        if argv[i] == "-f": files.append(yaml.safe_load(open(argv[i+1]))); i += 2
        elif argv[i] == "--set": sets.append(argv[i+1]); i += 2
        elif argv[i] == "--release": release = argv[i+1]; i += 2
        else: raise SystemExit("unknown arg " + argv[i])
    meta = yaml.safe_load(open(f"{chart}/Chart.yaml"))
    defaults = yaml.safe_load(open(f"{chart}/values.yaml"))
    ctx = {"Values": compute_values(defaults, files, sets),
           "Release": {"Name": release}, "Chart": {"Name": meta["name"]}}
    docs = []
    for path in sorted(glob.glob(f"{chart}/templates/*.yaml")):
        docs.append(f"---\n# Source: {meta['name']}/templates/{os.path.basename(path)}\n"
                    + render(open(path).read(), ctx).strip() + "\n")
    print("".join(docs), end="")

if __name__ == "__main__":
    main(sys.argv)
```

```bash
# ---- helm_commands.sh ----
# NOT EXECUTED here (no helm binary, download blocked). Typical flow, check `helm help` for your version.
helm lint ./chart/modelserver                                  # static checks on chart structure and templates
helm template churn ./chart/modelserver -f prod.yaml           # render YAML locally, no cluster needed
helm install churn ./chart/modelserver -n ml -f prod.yaml --set image.tag=1.4.2
helm upgrade churn ./chart/modelserver -n ml -f prod.yaml --set image.tag=1.4.3
helm history churn -n ml                                       # one row per revision
helm rollback churn 1 -n ml                                    # creates a NEW revision with revision 1's content
helm get values churn -n ml                                    # values the release was installed with
kubectl get secret -n ml -l owner=helm                         # release records: sh.helm.release.v1.churn.v<N>
```

**Output (my run):**
**Not executed:** `helm lint`, `template`, `install`, `upgrade`, `rollback` (no helm binary; the Helm download was blocked by the sandbox proxy) and anything against a cluster. What did run: `helm_mimic.py`, a small Python stand-in that applies the value-merge rules and fills only the template holes this chart uses (it is a teaching mimic, not Helm; real Helm uses Go templates and Sprig functions, so real output can differ in whitespace and details). The rendered YAML was then checked with `kubernetes-validate --strict` (schema only, Kubernetes 1.37 schemas).

```text
$ command -v helm kubectl || echo 'helm / kubectl: not installed'
helm / kubectl: not installed

$ python3 -I helm_mimic.py values
replicaCount : 5 (default 2, prod.yaml 3, --set 5 wins)
limits       : {'memory': '8Gi'} (prod.yaml replaced memory)
requests kept: {'cpu': '500m', 'memory': '1Gi'} (maps merge, untouched keys survive)
gpu          : {'enabled': True, 'count': 1}
--set typing : {'a': 20260101, 'b': True, 'c': '1.10', 'd': '007'}
list replace : {'args': ['--c']}
null deletes : {'gpu': {'enabled': True}}

$ python3 -I helm_mimic.py chart/modelserver -f prod.yaml --set image.tag=1.4.2 --release churn > rendered.yaml; sed -n '/^kind: Deployment/,/^---/p' rendered.yaml
kind: Deployment
metadata:
  name: churn-modelserver
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: modelserver
      app.kubernetes.io/instance: churn
  template:
    metadata:
      labels:
        app.kubernetes.io/name: modelserver
        app.kubernetes.io/instance: churn
    spec:
      containers:
        - name: server
          image: "registry.example.com/ml/churn-model:1.4.2"
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: churn-modelserver
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
          resources:
            requests:
              cpu: "500m"
              memory: 1Gi
            limits:
              memory: 8Gi
              nvidia.com/gpu: 1
      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule
---

$ kubernetes-validate --strict rendered.yaml
INFO rendered.yaml passed for resource configmap/churn-modelserver against version 1.37
INFO rendered.yaml passed for resource deployment/churn-modelserver against version 1.37
INFO rendered.yaml passed for resource service/churn-modelserver against version 1.37

$ echo "lines mentioning nvidia with default values: $(python3 -I helm_mimic.py chart/modelserver | grep -c nvidia)"
lines mentioning nvidia with default values: 0

$ bash -n helm_commands.sh && echo 'bash -n: helm_commands.sh syntax OK'
bash -n: helm_commands.sh syntax OK
```

**Follow-ups:**
- **Why does `helm rollback` give a higher revision number?** Rollback is recorded as a new revision whose content equals the old one, so history stays linear.
- **How do you force a pod restart when only a ConfigMap changed?** Put a checksum of the rendered ConfigMap in a pod-template annotation; a changed hash changes the pod template and triggers a rollout.
- **Helm or Kustomize?** Helm when you need packaging and parameters for many users; Kustomize for patching plain YAML per environment. Many teams use both.

**Common mistakes:**
- Thinking `helm template` or `lint` proves the chart works on a cluster. They check rendering and structure only.
- Passing secrets with `--set`. They land in shell history and in the release Secret. Use external secret tools.
- `--reuse-values` on upgrade, then wondering why new chart defaults never show up.
- Unquoted numeric-looking image tags, so `1.10` style values or all-digit tags change type.
- Believing a rollback also restores data, a PVC or a model registry state.

### Q12 ⭐⭐⭐ 🟡 Training as a Kubernetes Job and a scheduled retrain as a CronJob. Explain Job fields (completions, parallelism, backoffLimit, activeDeadlineSeconds, ttlSecondsAfterFinished, restartPolicy OnFailure or Never) and what a Job does on pod failure and on node loss, and CronJob fields (schedule in cron syntax, concurrencyPolicy Allow, Forbid, Replace, startingDeadlineSeconds, history limits, time zone). Show a GPU training Job and a nightly retrain CronJob that mounts data from a PVC, and a script that validates the manifests and expands a cron schedule into the next five run times. Running them is not executed.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A Job runs a pod to completion with retries and a deadline; a CronJob is a Job factory on a cron schedule, and for training you set the retry, deadline, cleanup and concurrency fields on purpose.

**Then explain:**
- **Job fields.** `completions` (how many successful pods), `parallelism` (how many at once), `backoffLimit` (retries before the Job is Failed; I recall the default is 6, check docs), `activeDeadlineSeconds` (hard time cap for the whole Job, wins over retries), `ttlSecondsAfterFinished` (auto-delete the finished Job and its pods), `restartPolicy` must be `OnFailure` or `Never`, never `Always`.
- **On failure.** `Never`: the failed pod stays for `kubectl logs` and the Job creates a NEW pod. `OnFailure`: the container restarts inside the same pod. Both count towards `backoffLimit`, with growing delays between retries. A crashing GPU job with no deadline can burn GPU time for a long while.
- **On node loss.** The pod is gone or stuck; the Job controller creates a replacement pod, which starts from zero unless your code resumes from a checkpoint on a PVC or object storage. Newer clusters have a pod failure policy to treat node disruption differently from app errors (check your version).
- **CronJob fields.** `schedule` (5-field cron), `timeZone` (IANA name; without it the controller's zone is used; supported in current releases, check yours), `concurrencyPolicy` (`Allow` overlaps, `Forbid` skips if the last run is still going, `Replace` kills the old one), `startingDeadlineSeconds` (how late a run may start before it is counted as missed), `successfulJobsHistoryLimit` and `failedJobsHistoryLimit`, `suspend`.
- **Failure modes.** Overlapping nightly runs fighting for one GPU and one PVC. Missed runs after controller downtime (with many missed runs the CronJob can stop scheduling; `startingDeadlineSeconds` limits the counting window). Cron in UTC while the team thinks in IST. A finished Job never cleaned up, so hundreds of old pods pile up. `schedule` with both day-of-month and day-of-week set means OR, not AND.

**Example:** `schedule: "30 1 * * *"` with `timeZone: Asia/Kolkata` runs at 01:30 IST every day. IST is UTC+5:30, so that is 20:00 UTC the day before. Hand-check: 01:30 minus 5:30 = 20:00 previous day, and the script prints exactly that. Trace one night with `Forbid`: if last night's run is still going at 01:30, tonight's is skipped, not queued. With `backoffLimit: 1` the pod may run twice at most before the Job is Failed.

**Code:**
```yaml
# ---- train-job.yaml ----
apiVersion: batch/v1
kind: Job
metadata:
  name: churn-train-0426
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 2                 # retries before the Job is marked Failed
  activeDeadlineSeconds: 14400    # hard stop: 4 hours total, whatever the retries
  ttlSecondsAfterFinished: 86400  # delete the Job and its pods a day after it finishes
  template:
    spec:
      restartPolicy: Never        # Job pods must be OnFailure or Never, not Always
      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule
      containers:
        - name: train
          image: registry.example.com/ml/churn-train:2.3.0
          command: ["python", "train.py", "--resume-from", "/ckpt/latest.pt"]
          resources:
            requests: {cpu: "4", memory: 16Gi}
            limits: {memory: 16Gi, nvidia.com/gpu: 1}
          volumeMounts:
            - {name: data, mountPath: /data, readOnly: true}
            - {name: ckpt, mountPath: /ckpt}
      volumes:
        - name: data
          persistentVolumeClaim: {claimName: training-data, readOnly: true}
        - name: ckpt
          persistentVolumeClaim: {claimName: training-ckpt}

# ---- retrain-cron.yaml ----
apiVersion: batch/v1
kind: CronJob
metadata:
  name: churn-nightly-retrain
spec:
  schedule: "30 1 * * *"          # 01:30 every day
  timeZone: "Asia/Kolkata"        # without this the schedule uses the controller's time zone
  concurrencyPolicy: Forbid       # skip a run if last night's is still going
  startingDeadlineSeconds: 1800   # if the run could not start within 30 min of its time, skip it
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 1
      activeDeadlineSeconds: 18000
      ttlSecondsAfterFinished: 172800
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: retrain
              image: registry.example.com/ml/churn-train:2.3.0
              command: ["python", "train.py", "--data", "/data/latest"]
              resources:
                requests: {cpu: "4", memory: 16Gi}
                limits: {memory: 16Gi, nvidia.com/gpu: 1}
              volumeMounts:
                - {name: data, mountPath: /data, readOnly: true}
          volumes:
            - name: data
              persistentVolumeClaim: {claimName: training-data, readOnly: true}
```

```python
# ---- check_batch.py ----
"""Semantic checks for Job/CronJob manifests + next-N cron run times. Pure Python, no cluster."""
import sys, yaml
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

RANGES = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]   # min hour dom month dow (0 = Sunday)

def parse_field(text, lo, hi):
    out = set()
    for part in text.split(","):
        step = 1
        if "/" in part:
            part, s = part.split("/"); step = int(s)
        if part == "*": a, b = lo, hi
        elif "-" in part: a, b = map(int, part.split("-"))
        else: a = int(part); b = hi if step > 1 else a
        out.update(range(a, b + 1, step))
    assert all(lo <= v <= hi for v in out), f"out of range in {text!r}"
    return out

def next_runs(schedule, start, n=5):
    f = schedule.split()
    assert len(f) == 5, "need 5 fields"
    mins, hrs, doms, mons, dows = (parse_field(x, *r) for x, r in zip(f, RANGES))
    dom_star, dow_star = f[2] == "*", f[4] == "*"
    t = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
    runs = []
    while len(runs) < n:
        dow = (t.weekday() + 1) % 7                      # Python Monday=0 -> cron Sunday=0
        if dom_star or dow_star: day_ok = t.day in doms and dow in dows
        else: day_ok = t.day in doms or dow in dows      # both restricted: cron uses OR
        if t.minute in mins and t.hour in hrs and t.month in mons and day_ok:
            runs.append(t)
        t += timedelta(minutes=1)
    return runs

def check_pod_spec(spec, where, problems):
    if spec.get("restartPolicy") not in ("Never", "OnFailure"):
        problems.append(f"{where}: restartPolicy must be Never or OnFailure for batch pods")
    for c in spec["containers"]:
        r = c.get("resources", {})
        if "memory" not in r.get("limits", {}):
            problems.append(f"{where}: container {c['name']} has no memory limit")

def check(doc):
    problems = []
    kind, name = doc["kind"], doc["metadata"]["name"]
    job = doc["spec"]["jobTemplate"]["spec"] if kind == "CronJob" else doc["spec"]
    for f in ("backoffLimit", "activeDeadlineSeconds", "ttlSecondsAfterFinished"):
        if f not in job: problems.append(f"{kind}/{name}: {f} not set")
    check_pod_spec(job["template"]["spec"], f"{kind}/{name}", problems)
    if kind == "CronJob":
        if doc["spec"].get("concurrencyPolicy", "Allow") == "Allow":
            problems.append(f"CronJob/{name}: concurrencyPolicy Allow lets runs overlap")
        if "timeZone" not in doc["spec"]:
            problems.append(f"CronJob/{name}: no timeZone")
    return problems

if __name__ == "__main__":
    for path in sys.argv[1:]:
        for doc in yaml.safe_load_all(open(path)):
            probs = check(doc)
            print(f"{doc['kind']}/{doc['metadata']['name']}: {'OK' if not probs else probs}")
            if doc["kind"] == "CronJob":
                tz = ZoneInfo(doc["spec"].get("timeZone", "UTC"))
                now = datetime(2026, 10, 26, 22, 10, tzinfo=tz)      # fixed 'now' so output is repeatable
                print(f"  schedule {doc['spec']['schedule']!r} in {tz.key}, after {now:%Y-%m-%d %H:%M}:")
                for t in next_runs(doc["spec"]["schedule"], now):
                    print(f"    {t:%a %Y-%m-%d %H:%M %Z}  =  {t.astimezone(timezone.utc):%H:%M} UTC")
    # edge cases worth knowing
    t0 = datetime(2026, 10, 26, 0, 0, tzinfo=timezone.utc)
    print("every 15 min :", [f"{t:%H:%M}" for t in next_runs("*/15 * * * *", t0, 4)])
    print("'0 9 13 * 5' :", [f"{t:%a %m-%d}" for t in next_runs("0 9 13 * 5", t0, 4)], "(13th OR any Friday)")
```

**Output (my run):**
**Not executed:** creating the Job or CronJob and any real retry, node-loss or schedule behaviour (no cluster, no GPU). What did run: `kubernetes-validate --strict` (schema only) and `check_batch.py`, which checks the fields above and expands cron into the next five run times from a fixed 'now' of 2026-10-26 22:10 in the CronJob's zone (my own small cron parser: 5 fields, `*`, lists, ranges, steps; no `@daily` or names). The last two commands use a deliberately sloppy file: the schema validator passes it (the schema does not encode these rules, and the API server's own validation would reject `restartPolicy: Always` for a Job) while my checker lists the real problems, which shows why schema validation is not enough.

```text
$ kubernetes-validate --strict train-job.yaml retrain-cron.yaml
INFO train-job.yaml passed for resource job/churn-train-0426 against version 1.37
INFO retrain-cron.yaml passed for resource cronjob/churn-nightly-retrain against version 1.37

$ python3 -I check_batch.py train-job.yaml retrain-cron.yaml
Job/churn-train-0426: OK
CronJob/churn-nightly-retrain: OK
  schedule '30 1 * * *' in Asia/Kolkata, after 2026-10-26 22:10:
    Tue 2026-10-27 01:30 IST  =  20:00 UTC
    Wed 2026-10-28 01:30 IST  =  20:00 UTC
    Thu 2026-10-29 01:30 IST  =  20:00 UTC
    Fri 2026-10-30 01:30 IST  =  20:00 UTC
    Sat 2026-10-31 01:30 IST  =  20:00 UTC
every 15 min : ['00:15', '00:30', '00:45', '01:00']
'0 9 13 * 5' : ['Fri 10-30', 'Fri 11-06', 'Fri 11-13', 'Fri 11-20'] (13th OR any Friday)

$ python3 -I check_batch.py bad-cron.yaml | sed -n 1p
CronJob/sloppy-retrain: ['CronJob/sloppy-retrain: backoffLimit not set', 'CronJob/sloppy-retrain: activeDeadlineSeconds not set', 'CronJob/sloppy-retrain: ttlSecondsAfterFinished not set', 'CronJob/sloppy-retrain: restartPolicy must be Never or OnFailure for batch pods', 'CronJob/sloppy-retrain: container retrain has no memory limit', 'CronJob/sloppy-retrain: concurrencyPolicy Allow lets runs overlap', 'CronJob/sloppy-retrain: no timeZone']

$ kubernetes-validate --strict bad-cron.yaml
INFO bad-cron.yaml passed for resource cronjob/sloppy-retrain against version 1.37
```

**Follow-ups:**
- **Job or Deployment for training?** Job: it ends, retries and reports success. A Deployment would restart a finished process forever.
- **How do you run 8 workers of one training task?** Indexed Job or a training operator (Kubeflow, see later parts); for tightly coupled GPU jobs you also need gang scheduling so half the workers do not sit holding GPUs.
- **Why `Replace` rarely?** It kills a run that may be nearly done. `Forbid` is the safer default for training.

**Common mistakes:**
- `restartPolicy: Always` in a Job template (the API rejects it for Jobs; my checker flags it for the template).
- No `activeDeadlineSeconds`, so a hung job holds a GPU all weekend.
- No `ttlSecondsAfterFinished`, then 300 completed pods and a slow `kubectl get pods`.
- Forgetting the time zone, so the 'nightly' retrain runs at office time.
- Training that cannot resume, so a retry restarts from epoch 0.

### Q13 ⭐⭐⭐ 🟡 PersistentVolumes and PersistentVolumeClaims for ML data and model artifacts. Explain PV, PVC, StorageClass, dynamic provisioning, access modes (ReadWriteOnce, ReadOnlyMany, ReadWriteMany) and why many replicas reading one model cache need ReadOnlyMany, ReadWriteMany or an init container that downloads from object storage, reclaim policy, what happens to data when a pod dies, and why a PVC stuck Pending blocks the pod. Compare a PVC, an emptyDir cache and loading weights from S3 or a registry at start. Show the manifests and a validation script. Applying them is not executed.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A PersistentVolumeClaim is a pod's request for storage, a StorageClass says how to create it, and the access mode decides how many nodes can mount it; model replicas should not share a ReadWriteOnce claim.

**Then explain:**
- **The pieces.** PV = the real storage object. PVC = the request ('50Gi, this access mode, this class'). StorageClass = the recipe for dynamic provisioning: a PVC with a class makes the provisioner create a PV and bind it. The pod only names the PVC.
- **Access modes.** `ReadWriteOnce` (RWO): mountable read-write by ONE NODE at a time (several pods on that node can share it). `ReadOnlyMany` (ROX): many nodes read. `ReadWriteMany` (RWX): many nodes read and write. Cloud block disks are usually RWO only; RWX and ROX need a shared file backend. Which one your cluster supports is a storage-driver question, check current docs. There is also a ReadWriteOncePod mode in newer versions.
- **Lifetime.** Pod dies, PVC and data stay. Delete the PVC and the PV's `reclaimPolicy` decides: `Delete` removes the disk, `Retain` keeps it for manual cleanup. `emptyDir` dies with the pod. Zonal disks also pin the pod to one zone; `WaitForFirstConsumer` creates the disk where the pod lands.
- **A Pending PVC blocks the pod.** Typical causes: no such StorageClass, no default class, no provisioner or driver, quota exhausted, no PV matches the size or mode, or (normal!) `WaitForFirstConsumer` waiting for a pod. The pod event says 'unbound immediate PersistentVolumeClaims' or similar.
- **For many serving replicas, three options.** (1) One ROX/RWX volume holding the model: one copy, but needs shared storage and a populate step. (2) Init container downloads from object storage into `emptyDir`: simple and stateless, but every pod downloads and node disk is used N times. (3) Bake the model into the image: fastest start, big images. Pick by model size and how often it changes.

**Example:** Made-up numbers: a 20 GiB model, 4 replicas on 4 nodes. Option 2 (emptyDir): 4 downloads and 80 GiB of node disk in total, and every restart downloads again. Option 1 (one ROX volume): 1 copy, 20 GiB, no download on restart, but needs a backend that supports ROX. If instead you give all 4 replicas one RWO claim, pods on other nodes cannot mount it and stay `ContainerCreating` or Pending. The checker below flags exactly that.

**Code:**
```yaml
# ---- storage.yaml ----
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-rwo
provisioner: example.com/block-csi      # placeholder: use your cloud's CSI driver name
reclaimPolicy: Delete                   # Delete: volume dies with the PVC. Retain: keep for manual cleanup
volumeBindingMode: WaitForFirstConsumer # create the volume where the pod lands (zone-safe)
allowVolumeExpansion: true
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: training-ckpt
spec:
  accessModes: ["ReadWriteOnce"]        # one node at a time: fine for one training pod
  storageClassName: fast-rwo
  resources:
    requests:
      storage: 200Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-cache
spec:
  accessModes: ["ReadOnlyMany"]         # many nodes read; needs a backend that supports it
  storageClassName: shared-files        # not defined in this file on purpose; see the checker
  resources:
    requests:
      storage: 50Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scorer
spec:
  replicas: 4
  selector:
    matchLabels: {app: scorer}
  template:
    metadata:
      labels: {app: scorer}
    spec:
      initContainers:
        - name: fetch-weights               # pattern 3: each pod pulls from object storage at start
          image: registry.example.com/tools/fetcher:1.0
          args: ["--src", "s3://models/churn/v7/", "--dst", "/models"]
          volumeMounts:
            - {name: weights, mountPath: /models}
      containers:
        - name: server
          image: registry.example.com/ml/scorer:3.1.0
          volumeMounts:
            - {name: weights, mountPath: /models, readOnly: true}
            - {name: shared, mountPath: /shared-cache, readOnly: true}
      volumes:
        - name: weights
          emptyDir:
            sizeLimit: 10Gi                 # a node-local scratch dir, deleted with the pod
        - name: shared
          persistentVolumeClaim:
            claimName: model-cache
            readOnly: true
```

```python
# ---- check_storage.py ----
"""Cross-check PVCs, StorageClasses and the pods that use them. Offline, pure Python."""
import sys, yaml

def load(path):
    return [d for d in yaml.safe_load_all(open(path)) if d]

def main(path):
    docs = load(path)
    classes = {d["metadata"]["name"] for d in docs if d["kind"] == "StorageClass"}
    pvcs = {d["metadata"]["name"]: d for d in docs if d["kind"] == "PersistentVolumeClaim"}
    findings = []
    for name, pvc in pvcs.items():
        sc = pvc["spec"].get("storageClassName")
        if sc is None:
            findings.append(f"PVC {name}: no storageClassName -> uses the cluster default class, if one exists")
        elif sc not in classes:
            findings.append(f"PVC {name}: class {sc!r} not defined here -> stays Pending unless the cluster has it")
    for d in docs:
        if d["kind"] != "Deployment":
            continue
        replicas = d["spec"].get("replicas", 1)
        pod = d["spec"]["template"]["spec"]
        for v in pod.get("volumes", []):
            if "persistentVolumeClaim" in v:
                claim = v["persistentVolumeClaim"]["claimName"]
                if claim not in pvcs:
                    findings.append(f"Deployment {d['metadata']['name']}: claim {claim!r} does not exist -> pod Pending")
                    continue
                modes = pvcs[claim]["spec"]["accessModes"]
                if replicas > 1 and modes == ["ReadWriteOnce"]:
                    findings.append(f"Deployment {d['metadata']['name']}: {replicas} replicas share RWO claim {claim!r} -> only pods on ONE node can mount it")
                if replicas > 1 and "ReadWriteOnce" not in modes and not v["persistentVolumeClaim"].get("readOnly") and "ReadWriteMany" not in modes:
                    findings.append(f"Deployment {d['metadata']['name']}: claim {claim!r} is {modes} but mounted writable")
            if "emptyDir" in v and "sizeLimit" not in v["emptyDir"]:
                findings.append(f"emptyDir {v['name']}: no sizeLimit -> can fill the node disk")
    for sc in (d for d in docs if d["kind"] == "StorageClass"):
        print(f"StorageClass {sc['metadata']['name']}: reclaimPolicy={sc.get('reclaimPolicy', 'Delete')}, binding={sc.get('volumeBindingMode', 'Immediate')}")
    print(f"{len(findings)} finding(s)")
    for f in findings:
        print(" -", f)

main(sys.argv[1])
```

**Output (my run):**
**Not executed:** applying anything, provisioning, mounting, binding or the real Pending behaviour (no cluster, no CSI driver). What did run: `kubernetes-validate --strict` (schema only) and `check_storage.py`, my cross-checker for missing classes, missing claims, RWO shared by several replicas and unbounded emptyDir. On the good file it flags one real gap: the class `shared-files` used by `model-cache` is not defined in the file (I left it out on purpose; on a real cluster it may exist outside the file). The second run uses a deliberately broken file.

```text
$ kubernetes-validate --strict storage.yaml
INFO storage.yaml passed for resource storageclass/fast-rwo against version 1.37
INFO storage.yaml passed for resource persistentvolumeclaim/training-ckpt against version 1.37
INFO storage.yaml passed for resource persistentvolumeclaim/model-cache against version 1.37
INFO storage.yaml passed for resource deployment/scorer against version 1.37

$ python3 -I check_storage.py storage.yaml
StorageClass fast-rwo: reclaimPolicy=Delete, binding=WaitForFirstConsumer
1 finding(s)
 - PVC model-cache: class 'shared-files' not defined here -> stays Pending unless the cluster has it

$ python3 -I check_storage.py bad-storage.yaml
4 finding(s)
 - PVC shared-weights: no storageClassName -> uses the cluster default class, if one exists
 - Deployment scorer-bad: 3 replicas share RWO claim 'shared-weights' -> only pods on ONE node can mount it
 - Deployment scorer-bad: claim 'shared-weigths' does not exist -> pod Pending
 - emptyDir tmp: no sizeLimit -> can fill the node disk
```

**Follow-ups:**
- **Why can a RWO volume still work for 3 replicas sometimes?** If the scheduler puts all pods on the same node. Luck, not design.
- **Where should training checkpoints go?** A PVC or object storage, never the container filesystem, so a rescheduled job can resume.
- **Why does the PVC say Pending right after creation with WaitForFirstConsumer?** That is expected; it binds when a pod using it is scheduled.

**Common mistakes:**
- Writing to the container filesystem and calling it persistent.
- Sharing one RWO claim across replicas and blaming the scheduler.
- No `sizeLimit` on `emptyDir` and filling the node disk.
- Using `Delete` reclaim for data you cannot recreate.
- Assuming every cluster supports RWX; it depends on the storage backend.

### Q14 ⭐⭐⭐ 🟡 Ingress and exposing a model API. Explain how a Service, an Ingress resource and an ingress controller (NGINX, Traefik, cloud load balancers) fit together, host and path routing, TLS termination with a Secret, why an Ingress does nothing without a controller, timeouts and body-size limits that matter for big inference payloads, and Gateway API as the newer direction (hedge, check current docs). Give an Ingress manifest routing /v1/predict to the model Service and /docs to another, and a script that checks every Ingress backend names a real Service in the same manifest set. Not executed on a cluster.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A Service gives pods a stable in-cluster address, an Ingress is only a set of routing rules, and an ingress controller is the running proxy that reads those rules; without a controller the Ingress does nothing.

**Then explain:**
- **Three layers.** Pods behind a Service (ClusterIP). An Ingress object says 'host + path goes to Service:port'. An ingress controller (NGINX, Traefik, or a cloud load balancer controller) watches Ingress objects and configures a real proxy or cloud LB. `ingressClassName` picks which controller owns the Ingress.
- **Routing.** Host and path rules. `pathType: Prefix` matches `/docs` and `/docs/x`; `Exact` matches one path. The controller does not rewrite paths unless asked (annotation, controller-specific), so the app must really serve `/v1/predict`.
- **TLS.** `tls.secretName` points to a Secret of type `kubernetes.io/tls`. The controller terminates TLS and talks plain HTTP to the pod by default. Certificates are often issued by an add-on such as cert-manager.
- **Big inference payloads.** Proxies have a default body-size cap and read timeout, and they are small defaults for images, audio or long model calls. Annotation names are controller-specific (the ones in my file are for the community NGINX controller; check its current docs). For streaming or very long calls, also check the cloud load balancer's idle timeout.
- **Direction.** Gateway API (Gateway, HTTPRoute) is the newer, more expressive model and is where new features go. I also recall the community ingress-nginx project announcing its retirement; check its current status before choosing a controller.
- **Failure modes.** No controller installed (ADDRESS stays empty). Wrong `ingressClassName`. Backend Service name or port typo gives 404/503 from the proxy. Readiness failing, so the Service has no endpoints. Path prefix mismatch.

**Example:** Request `https://ml.example.com/v1/predict` -> controller matches host `ml.example.com`, longest prefix `/v1/predict` -> Service `model-svc` port 80 -> `targetPort` 8080 on a ready pod. Request `/docs/swagger` -> prefix `/docs` -> `docs-svc` port named `http`. Hand-check in the broken file below: the Ingress names `model-svc` but the Service was renamed `model-service`, so the proxy would have no backend, and the second rule asks for port 8000 while the Service exposes 80.

**Code:**
```yaml
# ---- ingress.yaml ----
apiVersion: v1
kind: Service
metadata:
  name: model-svc
spec:
  selector: {app: scorer}
  ports:
    - {name: http, port: 80, targetPort: 8080}
---
apiVersion: v1
kind: Service
metadata:
  name: docs-svc
spec:
  selector: {app: api-docs}
  ports:
    - {name: http, port: 80, targetPort: 3000}
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-api
  annotations:
    # Controller-specific. These names are for the community NGINX ingress controller; check its current docs.
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"      # big feature payloads or small images
    nginx.ingress.kubernetes.io/proxy-read-timeout: "120"   # seconds to wait for a slow model
spec:
  ingressClassName: nginx            # which controller should act on this Ingress
  tls:
    - hosts: ["ml.example.com"]
      secretName: ml-example-com-tls # Secret of type kubernetes.io/tls (tls.crt + tls.key)
  rules:
    - host: ml.example.com
      http:
        paths:
          - path: /v1/predict
            pathType: Prefix
            backend:
              service:
                name: model-svc
                port: {number: 80}
          - path: /docs
            pathType: Prefix
            backend:
              service:
                name: docs-svc
                port: {name: http}
```

```python
# ---- check_ingress.py ----
"""Check every Ingress backend names a real Service (same manifest set) and a port it exposes."""
import sys, yaml

def main(path):
    docs = [d for d in yaml.safe_load_all(open(path)) if d]
    services = {d["metadata"]["name"]: d for d in docs if d["kind"] == "Service"}
    secrets = {d["metadata"]["name"] for d in docs if d["kind"] == "Secret"}
    problems = 0
    for ing in (d for d in docs if d["kind"] == "Ingress"):
        name = ing["metadata"]["name"]
        spec = ing["spec"]
        if "ingressClassName" not in spec:
            print(f"WARN {name}: no ingressClassName (relies on a default class, or no controller picks it up)"); problems += 1
        for t in spec.get("tls", []):
            if t["secretName"] not in secrets:
                print(f"NOTE {name}: TLS secret {t['secretName']!r} is not in this file (fine if created elsewhere)")
        for rule in spec["rules"]:
            for p in rule["http"]["paths"]:
                be = p["backend"]["service"]
                svc = services.get(be["name"])
                where = f"{rule.get('host', '*')}{p['path']}"
                if svc is None:
                    print(f"FAIL {where}: backend Service {be['name']!r} not found"); problems += 1
                    continue
                ports = svc["spec"]["ports"]
                ok = any(("number" in be["port"] and pt["port"] == be["port"]["number"]) or
                         ("name" in be["port"] and pt.get("name") == be["port"]["name"]) for pt in ports)
                if not ok:
                    print(f"FAIL {where}: Service {be['name']!r} has no port {be['port']}; it exposes {[pt['port'] for pt in ports]}"); problems += 1
                else:
                    print(f"ok   {where} -> {be['name']}:{be['port']}")
    print("problems:", problems)

main(sys.argv[1])
```

**Output (my run):**
**Not executed:** an ingress controller, TLS, real routing or timeouts (no cluster). What did run: `kubernetes-validate --strict` (schema only; a 404 backend is valid YAML) and `check_ingress.py`, my cross-checker that every backend names a Service in the same file and a port that Service exposes (by number or name). The `bad-ingress.yaml` run shows it catching a missing Service, a wrong port and a missing `ingressClassName`.

```text
$ kubernetes-validate --strict ingress.yaml
INFO ingress.yaml passed for resource service/model-svc against version 1.37
INFO ingress.yaml passed for resource service/docs-svc against version 1.37
INFO ingress.yaml passed for resource ingress/ml-api against version 1.37

$ python3 -I check_ingress.py ingress.yaml
NOTE ml-api: TLS secret 'ml-example-com-tls' is not in this file (fine if created elsewhere)
ok   ml.example.com/v1/predict -> model-svc:{'number': 80}
ok   ml.example.com/docs -> docs-svc:{'name': 'http'}
problems: 0

$ python3 -I check_ingress.py bad-ingress.yaml
WARN ml-api: no ingressClassName (relies on a default class, or no controller picks it up)
NOTE ml-api: TLS secret 'ml-example-com-tls' is not in this file (fine if created elsewhere)
FAIL ml.example.com/v1/predict: backend Service 'model-svc' not found
FAIL ml.example.com/docs: Service 'docs-svc' has no port {'number': 8000}; it exposes [80]
problems: 3
```

**Follow-ups:**
- **Ingress or LoadBalancer Service?** A LoadBalancer Service is one cloud LB per Service (L4 mostly). An Ingress shares one entry point and routes by host/path (L7).
- **Where do you do auth and rate limiting?** At the gateway or controller (annotations or policies), or in the app; keep it consistent and check what your controller supports.
- **How do you test an Ingress rule without a cluster?** Schema-validate, cross-check names and ports like above, then test on a dev cluster.

**Common mistakes:**
- Applying an Ingress and never installing a controller.
- Forgetting `ingressClassName` on clusters with several controllers.
- Using the default body-size and timeout for big inference payloads.
- Expecting the path `/v1/predict` to be stripped before it reaches the pod.
- Putting the TLS Secret in a different namespace from the Ingress.

### Q15 ⭐⭐⭐ 🔴 Interview scenario: 'GPU pods are Pending but the dashboard shows idle GPUs'. Walk through the possible causes: the GPUs are held by pods that are running but idle, fractional or MIG resources are advertised under different names, taints or selectors mismatch, the device plugin DaemonSet is not running or crashed on a node, drivers or container runtime not configured, requests set on the wrong container, quota, and fragmentation (a pod needs 4 GPUs on one node, free GPUs are spread as 2+2). Give a diagnosis checklist with the commands, and a script that finds fragmentation from a sample node inventory. All cluster commands are not executed here.
**Asked at:** Kubernetes-for-AI question bank (Cloud Soft Solutions 'Kubernetes for AI interview questions'), NerdLevelTech MLOps interview course page, KodeKloud MLOps guide, SuperOrbital/CNCF NVIDIA device plugin post, NVIDIA GPU Operator time-slicing docs (v1.11 page only), University of Bergen RAIL GPU docs; search snippets only, not opened (WebFetch failed with ENOTFOUND); guides and docs, not verified candidate reports; GPU and deep-learning MLOps roles at product companies, GCCs and AI startups
**Say this first (1 line):** Pending is almost always about eligibility, not total capacity: read the scheduler's event, then check held GPUs, resource names, taints and selectors, the device plugin, the container that holds the request, quota, and whether the free GPUs sit on different nodes.

**Then explain:**
- **Step 1: the event.** `kubectl describe pod` shows the scheduler's reason per node group ('Insufficient nvidia.com/gpu', 'untolerated taint', 'didn't match node selector'). Wording changes by version. Start there, not with dashboards.
- **Idle but held.** A GPU is 'busy' to the scheduler the moment a pod requests it, even if `nvidia-smi` shows 0 percent (a forgotten notebook). Dashboards that read utilisation show 'idle'; the scheduler counts requests.
- **Name mismatch.** Time-sliced GPUs still use `nvidia.com/gpu` (more of them); MIG slices use their own names (for example `nvidia.com/mig-1g.10gb`, names depend on mode and GPU, check the GPU Operator docs). A pod asking for `nvidia.com/gpu` never lands on a node that only advertises MIG names.
- **Plumbing.** Taint without toleration, node selector or affinity mismatch, the device plugin DaemonSet not running or crashing on a node (the node then advertises 0 GPUs), driver or container-runtime misconfigured (pod is scheduled but fails at start, a different symptom), the GPU limit written on the wrong container or an init container, a namespace ResourceQuota on `requests.nvidia.com/gpu`.
- **Fragmentation.** GPUs are whole integers on one node. A 4-GPU pod needs 4 free on ONE node; 6 free split 2+2+2 is useless. Fixes: bin-pack (scheduler scoring, dedicated pools for big jobs), run big jobs first, quota and queueing (Kueue-style, later parts), smaller jobs, or defragment by moving small pods.

**Example:** Inventory (made up): gpu-a 8 GPUs with 6 used, gpu-b 4 with 2 used, gpu-c 4 with 2 used, gpu-d plugin down (advertises none), mig-e advertises only MIG slices, cpu-f is a CPU node, train-g has 8 free GPUs but a `dedicated=training` taint. A pod wants 4 GPUs. Hand-check: free GPUs on eligible nodes are 2+2+2 = 6 in total, largest block 2, need 4 -> fragmentation, even though 'dashboard shows idle GPUs' (train-g, mig-e and a notebook holding 2).

**Code:**
```python
# ---- gpu_diag.py ----
"""Why is my GPU pod Pending? Offline model of a few scheduler filters on a made-up node inventory."""
from collections import Counter

NODES = {
  "gpu-a":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/gpu": 8}, "used": {"nvidia.com/gpu": 6}},
  "gpu-b":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/gpu": 4}, "used": {"nvidia.com/gpu": 2}},
  "gpu-c":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/gpu": 4}, "used": {"nvidia.com/gpu": 2}},
  "gpu-d":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {}, "used": {}},   # device plugin down: no GPU advertised
  "mig-e":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/mig-1g.10gb": 7}, "used": {}},
  "cpu-f":   {"labels": {"pool": "cpu"}, "taints": [],                                    "alloc": {}, "used": {}},
  "train-g": {"labels": {"pool": "gpu"}, "taints": [("dedicated=training", "NoSchedule")], "alloc": {"nvidia.com/gpu": 8}, "used": {}},
}
RUNNING = [  # who holds GPUs on gpu-a, with a made-up utilisation sample (percent, last 3 days)
  {"pod": "notebook-ravi", "node": "gpu-a", "gpus": 2, "util": 0},
  {"pod": "train-bert",    "node": "gpu-a", "gpus": 4, "util": 93},
]
POD = {"name": "train-big", "request": {"nvidia.com/gpu": 4}, "selector": {"pool": "gpu"},
       "tolerates": [("nvidia.com/gpu", "NoSchedule")]}

def reason(pod, n):
    if any(n["labels"].get(k) != v for k, v in pod["selector"].items()):
        return "node(s) didn't match Pod's node selector"
    for t in n["taints"]:
        if t not in pod["tolerates"]:
            return f"node(s) had untolerated taint {{{t[0]}}}"
    for res, need in pod["request"].items():
        if res not in n["alloc"]:
            return f"Insufficient {res} (node does not advertise it)"
        if n["alloc"][res] - n["used"].get(res, 0) < need:
            return f"Insufficient {res}"
    return None

def explain(pod, nodes=NODES):
    reasons = {name: reason(pod, n) for name, n in nodes.items()}
    fits = [k for k, v in reasons.items() if v is None]
    print(f"pod {pod['name']} wants {pod['request']}")
    for name, r in reasons.items():
        print(f"  {name:8} {r or 'FITS'}")
    if fits:
        print("  -> schedulable on", fits)
        return
    c = Counter(reasons.values())
    print(f"  event: 0/{len(nodes)} nodes are available: " + ", ".join(f"{n} {r}" for r, n in c.items()) + ".")
    # fragmentation: only nodes that pass the non-resource filters count
    res = next(iter(pod["request"]))
    eligible = {k: n for k, n in nodes.items()
                if not (reasons[k] or "").startswith(("node(s) didn't", "node(s) had"))}
    free = {k: n["alloc"].get(res, 0) - n["used"].get(res, 0) for k, n in eligible.items() if res in n["alloc"]}
    need = pod["request"][res]
    print(f"  free {res} on eligible nodes: {free}  total={sum(free.values())} largest block={max(free.values(), default=0)} need={need}")
    if sum(free.values()) >= need > max(free.values(), default=0):
        print("  -> FRAGMENTATION: enough GPUs in total, never enough on ONE node")

explain(POD)
print()
print("idle-but-held GPUs:", [(r["pod"], r["node"], r["gpus"]) for r in RUNNING if r["util"] < 5])
print()
explain({**POD, "name": "serve-small", "request": {"nvidia.com/gpu": 2}})
```

```bash
# ---- diagnose.sh ----
# NOT EXECUTED (no cluster). Run in this order; each step narrows the cause.
kubectl describe pod train-big -n ml | sed -n '/Events:/,$p'          # the scheduler's one-line reason is here
kubectl get pod train-big -n ml -o jsonpath='{.spec.containers[*].resources}'   # GPU limit on the RIGHT container?
kubectl get nodes -o custom-columns='NODE:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu'
kubectl describe node gpu-d | grep -A8 -i -E 'Taints|Allocatable|Allocated resources'
kubectl get pods -n gpu-operator -o wide                               # device plugin / driver pods Running on every GPU node?
kubectl get resourcequota -n ml                                        # quota on requests.nvidia.com/gpu used up?
kubectl get pods -A -o wide --field-selector spec.nodeName=gpu-a       # who is actually holding the GPUs
kubectl exec -n ml notebook-ravi -- nvidia-smi                         # is the held GPU doing any work?
```

**Output (my run):**
**Not executed:** every `kubectl` command in `diagnose.sh` (no cluster, no GPU); only `bash -n` (syntax check) ran. What did run: `gpu_diag.py`, an offline model of the scheduler's node selector, taint, resource-name and free-capacity filters on a made-up inventory. The 'event' line is my approximation of the scheduler's message format, not copied from a real cluster.

```text
$ python3 -I gpu_diag.py
pod train-big wants {'nvidia.com/gpu': 4}
  gpu-a    Insufficient nvidia.com/gpu
  gpu-b    Insufficient nvidia.com/gpu
  gpu-c    Insufficient nvidia.com/gpu
  gpu-d    Insufficient nvidia.com/gpu (node does not advertise it)
  mig-e    Insufficient nvidia.com/gpu (node does not advertise it)
  cpu-f    node(s) didn't match Pod's node selector
  train-g  node(s) had untolerated taint {dedicated=training}
  event: 0/7 nodes are available: 3 Insufficient nvidia.com/gpu, 2 Insufficient nvidia.com/gpu (node does not advertise it), 1 node(s) didn't match Pod's node selector, 1 node(s) had untolerated taint {dedicated=training}.
  free nvidia.com/gpu on eligible nodes: {'gpu-a': 2, 'gpu-b': 2, 'gpu-c': 2}  total=6 largest block=2 need=4
  -> FRAGMENTATION: enough GPUs in total, never enough on ONE node

idle-but-held GPUs: [('notebook-ravi', 'gpu-a', 2)]

pod serve-small wants {'nvidia.com/gpu': 2}
  gpu-a    FITS
  gpu-b    FITS
  gpu-c    FITS
  gpu-d    Insufficient nvidia.com/gpu (node does not advertise it)
  mig-e    Insufficient nvidia.com/gpu (node does not advertise it)
  cpu-f    node(s) didn't match Pod's node selector
  train-g  node(s) had untolerated taint {dedicated=training}
  -> schedulable on ['gpu-a', 'gpu-b', 'gpu-c']

$ bash -n diagnose.sh && echo 'bash -n diagnose.sh: syntax OK'
bash -n diagnose.sh: syntax OK
```

**Follow-ups:**
- **How do you stop one notebook hoarding GPUs?** Per-namespace GPU quota, idle culling for notebooks, and time-slicing or MIG for small work.
- **A 4-GPU job keeps starving behind small jobs. Options?** Dedicated node pool for large jobs, priority classes, a queue with quota (Kueue style), or gang scheduling so the job gets all or nothing.
- **Pod is scheduled but the container fails with a driver error?** That is the runtime or driver layer, not the scheduler: check the NVIDIA container toolkit and driver on that node.

**Common mistakes:**
- Trusting a utilisation dashboard instead of requested versus allocatable.
- Putting the GPU limit on a sidecar or init container.
- Forgetting the toleration for the GPU taint.
- Adding a node when the real cause is a selector or quota.
- Not noticing that requests and limits for GPUs must match and that GPUs are not shared between containers unless you set up sharing.

### Q16 ⭐⭐ 🟡 Kubernetes architecture in one pass for an ML engineer: control plane (API server, etcd, scheduler, controller manager) and node components (kubelet, container runtime, kube-proxy). Trace what happens from kubectl apply of a Deployment to a running pod (API server stores, controllers create ReplicaSet and Pods, scheduler binds, kubelet starts containers), and say what breaks if etcd or the scheduler is down. Include a small Python toy of the reconcile loop (desired versus actual replicas) and run it. No cluster is available, so the real flow is not executed.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Kubernetes is a store plus control loops: kubectl writes the desired state through the API server into etcd, controllers create the objects, the scheduler picks a node, and the kubelet on that node starts the containers.

**Then explain:**
- **Control plane.** API server (the only door: authentication, authorisation, admission, validation, then storage). etcd (the database of all objects). Scheduler (picks a node for each unbound pod). Controller manager (runs loops: Deployment, ReplicaSet, Node, Job and many more). Cloud controller if on a cloud.
- **Node.** kubelet (watches pods bound to its node, asks the container runtime to pull and start them, reports status and probe results), container runtime (containerd or similar, through CRI), kube-proxy or an equivalent (Service routing rules on the node), plus network and, for GPU, device plugin.
- **The trace for `kubectl apply` of a Deployment.** 1) API server validates and stores it in etcd. 2) Deployment controller sees it and creates a ReplicaSet. 3) ReplicaSet controller sees 0 pods, wants N, creates N Pod objects (no node yet, phase Pending). 4) Scheduler sees unbound pods, filters and scores nodes, writes the chosen node into each pod. 5) The kubelet on that node sees a pod for it, pulls the image, starts containers, runs probes. 6) Endpoints update once pods are Ready, so the Service sends traffic.
- **Everything is level-triggered.** Each controller compares desired with actual and fixes the difference; it does not matter which event was missed. That is why a deleted pod comes back.
- **What breaks.** etcd or API server down: no reads or writes, so no deploys, no scaling, no healing; already-running pods usually keep serving, because kubelets keep running what they have. Scheduler down: existing pods fine, new pods stay Pending. Controller manager down: no replacement for dead pods, no rollouts. A node (kubelet) down: its pods are marked NotReady later and rescheduled after the eviction timeouts, so recovery is not instant.

**Example:** Run the toy: apply 3 replicas -> ReplicaSet and 3 pods are created, bound to nodes and started. Delete one pod behind the API's back -> next tick the ReplicaSet controller notices 2 of 3 and creates pod 4. Scale to 5 with the scheduler down -> 2 pods stay Pending, 3 keep running; scheduler returns -> both get nodes. Make the store reject writes (etcd down) -> the scale to 6 fails and the 5 running pods are untouched. Count by hand: 3 -> 1 lost + 1 created = 3 -> scale 5 -> 5 running.

**Code:**
```python
# ---- reconcile.py ----
"""Toy control plane: a store (etcd), controllers that only talk to the store, a scheduler and a kubelet.
Teaching model of the flow, not Kubernetes code."""
import itertools

class Store:                      # stands in for API server + etcd
    def __init__(self): self.objs, self.up, self.n = {}, True, itertools.count(1)
    def put(self, key, obj):
        if not self.up: raise ConnectionError("etcd down: write rejected")
        self.objs[key] = obj
    def delete(self, key):
        if not self.up: raise ConnectionError("etcd down: write rejected")
        self.objs.pop(key, None)
    def pods(self): return {k: v for k, v in self.objs.items() if k.startswith("pod/")}

def deployment_controller(s):     # Deployment -> ReplicaSet
    d = s.objs["deploy/scorer"]
    if "rs/scorer-abc" not in s.objs:
        s.put("rs/scorer-abc", {"replicas": d["replicas"]}); print("  deployment-ctl: created ReplicaSet scorer-abc")
    elif s.objs["rs/scorer-abc"]["replicas"] != d["replicas"]:
        s.put("rs/scorer-abc", {"replicas": d["replicas"]}); print(f"  deployment-ctl: ReplicaSet now wants {d['replicas']}")

def replicaset_controller(s):     # ReplicaSet -> Pods (desired vs actual)
    want = s.objs["rs/scorer-abc"]["replicas"]
    have = s.pods()
    for _ in range(want - len(have)):
        name = f"pod/scorer-abc-{next(s.n)}"
        s.put(name, {"node": None, "phase": "Pending"}); print(f"  replicaset-ctl: have {len(have)}, want {want} -> created {name}")
        have = s.pods()
    for name in list(have)[want:]:
        s.delete(name); print(f"  replicaset-ctl: too many -> deleted {name}")

def scheduler(s, nodes=("node-1", "node-2")):   # binds Pending pods to a node
    for name, p in s.pods().items():
        if p["node"] is None:
            p["node"] = nodes[int(name.rsplit("-", 1)[1]) % len(nodes)]
            s.put(name, p); print(f"  scheduler: bound {name} -> {p['node']}")

def kubelet(s):                   # starts containers for pods bound to its node
    for name, p in s.pods().items():
        if p["node"] and p["phase"] == "Pending":
            p["phase"] = "Running"; s.put(name, p); print(f"  kubelet({p['node']}): started {name}")

def tick(s, label, sched=True):
    print(f"[{label}]")
    try:
        deployment_controller(s); replicaset_controller(s)
        if sched: scheduler(s)
        kubelet(s)
    except ConnectionError as e:
        print("  ERROR:", e)
    ph = sorted((k.split("-")[-1], v["phase"]) for k, v in s.pods().items())
    print("  state:", ph)

s = Store()
s.put("deploy/scorer", {"replicas": 3})                    # what `kubectl apply` stores
tick(s, "apply: 3 replicas")
victim = next(iter(s.pods())); s.objs.pop(victim)           # a node loses a pod behind the API's back
print(f"\n-- {victim} vanished --")
tick(s, "self-heal")
s.objs["deploy/scorer"]["replicas"] = 5
tick(s, "scale to 5, scheduler DOWN", sched=False)
tick(s, "scheduler back")
s.up = False
s.objs["deploy/scorer"]["replicas"] = 6
tick(s, "etcd DOWN, try to scale to 6")
print("running pods still serving:", sum(p["phase"] == "Running" for p in s.pods().values()))
```

**Output (my run):**
**Not executed:** the real flow (no cluster, no API server, no etcd). What did run: `reconcile.py`, a toy of my own with a dictionary as the store and four loop functions. It models the shape of the control loop, not Kubernetes code or timing; real controllers use watches, caches and delays that this toy ignores.

```text
$ python3 -I reconcile.py
[apply: 3 replicas]
  deployment-ctl: created ReplicaSet scorer-abc
  replicaset-ctl: have 0, want 3 -> created pod/scorer-abc-1
  replicaset-ctl: have 1, want 3 -> created pod/scorer-abc-2
  replicaset-ctl: have 2, want 3 -> created pod/scorer-abc-3
  scheduler: bound pod/scorer-abc-1 -> node-2
  scheduler: bound pod/scorer-abc-2 -> node-1
  scheduler: bound pod/scorer-abc-3 -> node-2
  kubelet(node-2): started pod/scorer-abc-1
  kubelet(node-1): started pod/scorer-abc-2
  kubelet(node-2): started pod/scorer-abc-3
  state: [('1', 'Running'), ('2', 'Running'), ('3', 'Running')]

-- pod/scorer-abc-1 vanished --
[self-heal]
  replicaset-ctl: have 2, want 3 -> created pod/scorer-abc-4
  scheduler: bound pod/scorer-abc-4 -> node-1
  kubelet(node-1): started pod/scorer-abc-4
  state: [('2', 'Running'), ('3', 'Running'), ('4', 'Running')]
[scale to 5, scheduler DOWN]
  deployment-ctl: ReplicaSet now wants 5
  replicaset-ctl: have 3, want 5 -> created pod/scorer-abc-5
  replicaset-ctl: have 4, want 5 -> created pod/scorer-abc-6
  state: [('2', 'Running'), ('3', 'Running'), ('4', 'Running'), ('5', 'Pending'), ('6', 'Pending')]
[scheduler back]
  scheduler: bound pod/scorer-abc-5 -> node-2
  scheduler: bound pod/scorer-abc-6 -> node-1
  kubelet(node-2): started pod/scorer-abc-5
  kubelet(node-1): started pod/scorer-abc-6
  state: [('2', 'Running'), ('3', 'Running'), ('4', 'Running'), ('5', 'Running'), ('6', 'Running')]
[etcd DOWN, try to scale to 6]
  ERROR: etcd down: write rejected
  state: [('2', 'Running'), ('3', 'Running'), ('4', 'Running'), ('5', 'Running'), ('6', 'Running')]
running pods still serving: 5
```

**Follow-ups:**
- **Where does the Service get its pod list?** The EndpointSlice controller builds endpoints from pods that match the selector and are Ready.
- **Who deletes a pod when you scale down?** The ReplicaSet controller picks pods to remove; the kubelet then stops them (with the grace period).
- **Why is a managed control plane attractive?** The provider runs and upgrades API server, etcd and scheduler; you still own node pools, add-ons and workloads.

**Common mistakes:**
- Saying the scheduler starts the containers. It only chooses a node; the kubelet starts them.
- Saying etcd down kills running pods. It stops changes and healing, not already-running containers.
- Confusing the controller manager with the scheduler.
- Treating `kubectl apply` as a command that runs something, instead of a request to store desired state.

### Q17 ⭐⭐ 🟡 Namespaces, RBAC and quotas for an ML platform shared by several teams. Explain Namespace, Role, ClusterRole, RoleBinding, ClusterRoleBinding, ServiceAccount, and how a training pod gets only the permissions it needs (read a Secret, nothing else). Add a ResourceQuota (including a GPU quota on requests.nvidia.com/gpu) and a LimitRange per team namespace, and mention the escalate and bind verbs as the guard against self-promotion. Give manifests, a script that checks a Role against a list of 'allowed verbs on resources' requests, and what kubectl auth can-i would show (not executed).
**Asked at:** Multi-tenancy and RBAC guides (adhdecode multi-tenancy interview page, Dataford resource quota question, OneUptime multi-tenancy and RBAC posts, Uffizzi quota article; search snippets only, not opened); editorial question banks, not verified candidate reports; platform, SRE and MLOps loops at GCCs and product companies
**Say this first (1 line):** Give each team a namespace, bind small Roles to ServiceAccounts, and cap what a namespace can consume with a ResourceQuota and sane defaults with a LimitRange; RBAC only adds permissions, it never subtracts.

**Then explain:**
- **Objects.** Namespace = a scope for names and policy. Role = permissions inside one namespace. ClusterRole = cluster-wide permissions or reusable ones. RoleBinding grants a Role (or ClusterRole) to users, groups or ServiceAccounts in one namespace. ClusterRoleBinding does it cluster-wide. ServiceAccount = identity for a pod.
- **Least privilege for a training pod.** Make a ServiceAccount, a Role with `get` on `secrets` limited by `resourceNames` to one Secret, and a RoleBinding. Better still: if the pod only needs the secret's value, mount it as an env var or volume in the pod spec; the kubelet delivers it and the pod needs no API permission at all. Set `automountServiceAccountToken: false` where the pod never calls the API.
- **Watch the verbs.** `list` and `watch` on secrets expose every secret value in the namespace. `resourceNames` cannot restrict `list` the way people expect (check the docs for the fieldSelector exception). Wildcards are a smell.
- **Escalate and bind.** To stop self-promotion, creating a Role or binding that grants permissions you do not have is refused unless you hold the special `escalate` (for roles) or `bind` (for bindings) verb. Give those only to platform admins, and when you must give `bind`, scope it with `resourceNames` to specific roles as in the manifest.
- **Quota and defaults.** ResourceQuota caps totals per namespace: CPU and memory requests, pod count, and extended resources with the `requests.` prefix, such as `requests.nvidia.com/gpu`. A pod that would push the namespace over is rejected at admission. LimitRange gives default requests and limits and max values per container, and is needed because a quota on CPU or memory requires every pod to state them.
- **Limits of this.** Namespaces are soft isolation: add NetworkPolicy, Pod Security settings and node pools for hard separation. A quota guards total GPUs per team; it does not prevent fragmentation or queue waiting.

**Example:** Quota: 4 GPUs for team-a. Jobs ask for 2, 1, 1, 1 GPUs. Running total 2, 3, 4, then the fourth job would need 5 > 4, so it is rejected (the toy prints 'exceeded quota requests.nvidia.com/gpu'). RBAC: `trainer` can `get` Secret `train-creds`, but not `db-admin`, not `list` secrets, not `update`, not `get` pods. Expected `kubectl auth can-i` answers (not executed): `get secrets/train-creds` yes, `list secrets` no.

**Code:**
```yaml
# ---- team-a.yaml ----
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: trainer
  namespace: team-a
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: read-train-creds
  namespace: team-a
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["train-creds"]      # exactly one Secret
    verbs: ["get"]                      # and only get
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: trainer-reads-creds
  namespace: team-a
subjects:
  - kind: ServiceAccount
    name: trainer
    namespace: team-a
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: read-train-creds
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "40"
    requests.memory: 200Gi
    requests.nvidia.com/gpu: "4"        # quota names the extended resource with the requests. prefix
    pods: "30"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-defaults
  namespace: team-a
spec:
  limits:
    - type: Container
      default: {cpu: "1", memory: 2Gi}          # limit used when a container sets none
      defaultRequest: {cpu: 250m, memory: 512Mi}
      max: {memory: 64Gi}
---
# The guard against self-promotion: this role may create RoleBindings but may only bind the 'edit' ClusterRole.
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: team-binder
  namespace: team-a
rules:
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["rolebindings"]
    verbs: ["create"]
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["clusterroles"]
    resourceNames: ["edit"]
    verbs: ["bind"]                      # without 'bind' (or already holding the perms), binding a stronger role is refused
```

```python
# ---- rbac_check.py ----
"""Tiny `kubectl auth can-i` model for namespaced Roles + a quota admission toy. Offline."""
import yaml, sys

docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if d]
roles = {d["metadata"]["name"]: d for d in docs if d["kind"] == "Role"}
bindings = [d for d in docs if d["kind"] == "RoleBinding"]

def allowed(sa, verb, resource, name=None, group=""):
    for b in bindings:
        if not any(s["kind"] == "ServiceAccount" and s["name"] == sa for s in b["subjects"]):
            continue
        for r in roles[b["roleRef"]["name"]]["rules"]:
            if group not in r["apiGroups"] and "*" not in r["apiGroups"]: continue
            if resource not in r["resources"] and "*" not in r["resources"]: continue
            if verb not in r["verbs"] and "*" not in r["verbs"]: continue
            if "resourceNames" in r and name not in r["resourceNames"]: continue
            return True
    return False

CHECKS = [  # (verb, resource, name, expected)
    ("get",    "secrets", "train-creds", True),
    ("get",    "secrets", "db-admin",    False),   # another Secret
    ("list",   "secrets", None,          False),   # list would expose every Secret
    ("update", "secrets", "train-creds", False),
    ("get",    "pods",    None,          False),
]
bad = 0
print("kubectl auth can-i --as=system:serviceaccount:team-a:trainer ...   (modelled, not the real command)")
for verb, res, name, expect in CHECKS:
    got = allowed("trainer", verb, res, name)
    bad += got != expect
    print(f"  {verb:6} {res + ('/' + name if name else ''):22} -> {'yes' if got else 'no':3} (expected {'yes' if expect else 'no'}){'' if got == expect else '  <-- MISMATCH'}")

print("risky-verb scan:")
for role in roles.values():
    for r in role["rules"]:
        flags = [v for v in r["verbs"] if v in ("*", "escalate", "bind", "impersonate")]
        if "*" in r["resources"]: flags.append("resources:*")
        if "secrets" in r["resources"] and ({"list", "watch"} & set(r["verbs"])): flags.append("list/watch secrets")
        if flags: print(f"  {role['metadata']['name']}: {flags} on {r['resources']} resourceNames={r.get('resourceNames')}")

# --- ResourceQuota admission toy: a pod is rejected if it would push 'used' over 'hard' ---
quota = next(d for d in docs if d["kind"] == "ResourceQuota")["spec"]["hard"]
used = {k: 0 for k in quota}
def admit(pod_name, gpus, cpu):
    want = {"requests.nvidia.com/gpu": gpus, "requests.cpu": cpu, "pods": 1}
    for k, v in want.items():
        if used[k] + v > float(quota[k]):
            print(f"  {pod_name}: REJECTED, exceeded quota {k}: used {used[k]}, requested {v}, limited {quota[k]}")
            return
    for k, v in want.items(): used[k] += v
    print(f"  {pod_name}: admitted, gpu used {used['requests.nvidia.com/gpu']}/{quota['requests.nvidia.com/gpu']}")
print("quota toy (GPU hard limit 4):")
for i, g in enumerate([2, 1, 1, 1], 1): admit(f"train-{i}", g, 4)
print("mismatches:", bad)
```

**Output (my run):**
**Not executed:** `kubectl auth can-i`, `kubectl apply`, real admission or quota enforcement (no cluster). What did run: `kubernetes-validate --strict` (schema only; it cannot tell a safe Role from a dangerous one) and `rbac_check.py`, my small model of `auth can-i` for namespaced Roles (API group, resource, verb, resourceNames) plus a risky-verb scan and a toy quota check. It models the rule shape, not the full RBAC engine.

```text
$ kubernetes-validate --strict team-a.yaml
INFO team-a.yaml passed for resource namespace/team-a against version 1.37
INFO team-a.yaml passed for resource serviceaccount/trainer against version 1.37
INFO team-a.yaml passed for resource role/read-train-creds against version 1.37
INFO team-a.yaml passed for resource rolebinding/trainer-reads-creds against version 1.37
INFO team-a.yaml passed for resource resourcequota/team-a-quota against version 1.37
INFO team-a.yaml passed for resource limitrange/team-a-defaults against version 1.37
INFO team-a.yaml passed for resource role/team-binder against version 1.37

$ python3 -I rbac_check.py team-a.yaml
kubectl auth can-i --as=system:serviceaccount:team-a:trainer ...   (modelled, not the real command)
  get    secrets/train-creds    -> yes (expected yes)
  get    secrets/db-admin       -> no  (expected no)
  list   secrets                -> no  (expected no)
  update secrets/train-creds    -> no  (expected no)
  get    pods                   -> no  (expected no)
risky-verb scan:
  team-binder: ['bind'] on ['clusterroles'] resourceNames=['edit']
quota toy (GPU hard limit 4):
  train-1: admitted, gpu used 2/4
  train-2: admitted, gpu used 3/4
  train-3: admitted, gpu used 4/4
  train-4: REJECTED, exceeded quota requests.nvidia.com/gpu: used 4, requested 1, limited 4
mismatches: 0
```

**Follow-ups:**
- **Role or ClusterRole plus RoleBinding?** A ClusterRole bound with a RoleBinding is limited to that namespace; this is how you reuse one definition for every team.
- **How do you audit who can do what?** `kubectl auth can-i --list --as=...`, plus reviewing bindings; on managed clusters also the provider's IAM mapping (check current docs).
- **Quota exceeded: how does the user see it?** The create call fails with a 'forbidden: exceeded quota' error naming the resource.

**Common mistakes:**
- Binding `cluster-admin` to a CI ServiceAccount 'for now'.
- `get, list, watch` on secrets when one `get` was enough.
- A CPU/memory quota with no LimitRange, then pods without requests are rejected and nobody knows why.
- Using the `default` ServiceAccount for everything.
- Thinking namespaces alone stop cross-team network traffic or node sharing.

### Q18 ⭐⭐ 🟡 Vertical Pod Autoscaler (VPA) versus HPA versus Cluster Autoscaler. Explain what each scales (pod size, pod count, node count), the recommender, updater and admission controller of VPA, why VPA in Auto mode restarts pods and why VPA and HPA on the same CPU or memory metric conflict, using VPA in recommendation-only mode to right-size ML pods, and how Cluster Autoscaler reacts to Pending pods and removes underused nodes. Give a comparison table, a VPA manifest in Off mode, and a script that turns a list of observed memory samples into a request recommendation (percentile plus headroom). Live components are not executed.
**Asked at:** Autoscaling write-ups (techinterview.org 'System Design Interview: Kubernetes Autoscaling (HPA, VPA, KEDA, Cluster Autoscaler)', AWS EKS ML inference autoscaling HPA and KEDA guide, CloudNativeNow KEDA articles, dev.to VPA/HPA/KEDA patterns; search snippets only, not opened); editorial and vendor docs, not verified candidate reports; senior MLOps and platform loops
**Say this first (1 line):** HPA changes how many pods, VPA changes how big each pod is, and Cluster Autoscaler changes how many nodes; they work at different layers and you combine them carefully.

**Then explain:**
| Tool | What it scales | Trigger | Cost of acting |
|---|---|---|---|
| HPA | pod count | metric vs target (CPU, memory, custom, external) | new pods, cold start |
| VPA | pod CPU and memory requests (and limits) | observed usage history | pod restart in Auto/Recreate modes (newer versions may support in-place resize, check docs) |
| Cluster Autoscaler | node count | Pending pods that fit a new node; underused nodes | minutes for a node, more for GPU |

- **VPA parts.** The recommender reads usage (metrics server, optionally Prometheus history) and computes targets with bounds. The updater evicts pods whose requests are far from the target. The admission controller sets requests on new pods. `updateMode: "Off"` gives recommendations only, in the VPA object's status.
- **Why Auto mode is risky for ML.** It restarts pods to apply new sizes, so a model server reloads its weights and drops warm cache, and a restart storm hits you when usage shifts. Prefer `Off` and apply the numbers through your deploy pipeline, or use `Initial` (sets size only at pod creation).
- **VPA plus HPA conflict.** If both act on CPU or memory they chase each other: HPA adds pods because per-pod CPU is high while VPA raises the CPU request, which lowers the ratio. Use HPA on a custom metric (requests per second, queue length, latency) and VPA for resources, or VPA in recommendation mode only.
- **Cluster Autoscaler.** Sees Pending pods that cannot fit, simulates adding a node from a node group, and scales up. It removes nodes that stay underused when their pods can be moved. It works from pod REQUESTS, so wrong requests mean wrong node counts.
- **Right-sizing ML pods.** Memory is the dangerous resource: too low gives OOMKilled (exit 137); too high wastes expensive nodes. Request = limit for memory is a safe habit; CPU limits are debated. Base memory on peaks, not averages.

**Example:** Seven days of memory samples (MiB) for a scorer pod; the mean is about 1018 MiB but day 5 peaked at 1620 MiB during a big batch. A request at the mean would OOM on day 5. Peak-based recommendation: p90 of daily peaks (1620 here, because with 7 peaks p90 is the max) times 1.15 headroom = 1863, rounded up to 64 MiB steps = 1920 MiB. Check: 1620 x 1.15 = 1863; 1863 / 64 = 29.1, so 30 steps = 1920.

**Code:**
```yaml
# ---- vpa.yaml ----
apiVersion: autoscaling.k8s.io/v1      # VPA is an add-on with its own CRD; install it separately
kind: VerticalPodAutoscaler
metadata:
  name: scorer-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: scorer
  updatePolicy:
    updateMode: "Off"                  # recommend only: never evict or resize pods
  resourcePolicy:
    containerPolicies:
      - containerName: server
        controlledResources: ["cpu", "memory"]
        minAllowed: {memory: 512Mi}
        maxAllowed: {memory: 16Gi}
```

```python
# ---- rightsize.py ----
"""Turn observed memory samples into a request recommendation: daily peak -> percentile -> headroom -> round up.
A simplified model of what a recommender does, not the VPA algorithm itself."""
import math, statistics

MIB = 1
def percentile(xs, p):
    xs = sorted(xs); k = math.ceil(p / 100 * len(xs)) - 1
    return xs[max(k, 0)]

# 7 days of memory samples (MiB) for one scorer pod; day 5 had a big batch request
days = {
  "d1": [900, 950, 1010, 980, 1040], "d2": [910, 960, 1000, 1020, 990],
  "d3": [930, 970, 1050, 1000, 1030], "d4": [900, 940, 1020, 1060, 1010],
  "d5": [920, 980, 1500, 1620, 1100], "d6": [915, 955, 1005, 1035, 995],
  "d7": [925, 965, 1015, 1045, 1000],
}
all_samples = [s for v in days.values() for s in v]
peaks = [max(v) for v in days.values()]
avg = statistics.mean(all_samples)
p90_peak = percentile(peaks, 90)
rec = math.ceil(p90_peak * 1.15 / 64) * 64      # 15% headroom, rounded up to 64 MiB steps
print(f"mean of all samples : {avg:7.1f} MiB   <- the tempting, wrong number")
print(f"daily peaks         : {peaks}")
print(f"p90 of daily peaks  : {p90_peak} MiB   (only 7 peaks, so p90 is the max; with more days a rare spike drops out)")
print(f"recommended request : {rec} MiB (p90 peak + 15% headroom, rounded up to 64)")
print(f"max ever seen       : {max(all_samples)} MiB -> a request/limit at the mean would OOM on day 5: {math.floor(avg) < max(all_samples)}")
print(f"limit = request is the safe habit for memory: limit {rec} MiB")

# The VPA CRD is not in the bundled Kubernetes schemas, so check the few fields that matter by hand.
import yaml
vpa = yaml.safe_load(open("vpa.yaml"))
mode = vpa["spec"]["updatePolicy"]["updateMode"]
print(f"vpa.yaml parses; updateMode={mode!r}; valid mode: {mode in ('Off', 'Initial', 'Recreate', 'Auto')}; recommend-only: {mode == 'Off'}")
```

**Output (my run):**
**Not executed:** VPA, HPA and Cluster Autoscaler themselves (add-ons and a cluster are needed). What did run: `kubernetes-validate` (it only warns that it has no schema for the VPA kind, because VPA is a CRD outside the core API, so the manifest is NOT schema-validated) and `rightsize.py`, which parses the manifest, checks `updateMode` by hand and computes a recommendation from made-up samples. The real VPA recommender uses decaying histograms, its own percentiles and safety margins (check its docs); my script is a simplified illustration.

```text
$ kubernetes-validate --strict vpa.yaml; echo "exit code: $?"
WARN vpa.yaml Couldn't find schema for kind VerticalPodAutoscaler with api version autoscaling.k8s.io/v1 for kubernetes version 1.37
exit code: 0

$ python3 -I rightsize.py
mean of all samples :  1018.4 MiB   <- the tempting, wrong number
daily peaks         : [1040, 1020, 1050, 1060, 1620, 1035, 1045]
p90 of daily peaks  : 1620 MiB   (only 7 peaks, so p90 is the max; with more days a rare spike drops out)
recommended request : 1920 MiB (p90 peak + 15% headroom, rounded up to 64)
max ever seen       : 1620 MiB -> a request/limit at the mean would OOM on day 5: True
limit = request is the safe habit for memory: limit 1920 MiB
vpa.yaml parses; updateMode='Off'; valid mode: True; recommend-only: True
```

**Follow-ups:**
- **Pod was OOMKilled, what does VPA do?** It records the event and raises the memory recommendation; you still need a sane limit and a fix if memory leaks.
- **Which metric for HPA on an inference service?** Requests per second per pod or queue/latency signals beat CPU, especially for GPU-bound models (CPU stays low while the GPU is saturated).
- **Can you scale to zero with HPA?** Not in the standard setup; that is KEDA territory (next question group).

**Common mistakes:**
- HPA and VPA both on CPU for the same Deployment.
- VPA Auto on a model server with a slow warm-up.
- Sizing memory from averages.
- Expecting Cluster Autoscaler to react to high CPU usage; it reacts to Pending pods and requests.
- Setting requests far above real use 'to be safe', then paying for empty nodes.

### Q19 ⭐⭐ 🔴 KEDA for ML inference and batch workers. Explain how KEDA reads an external signal (Kafka lag, SQS depth, Redis list length, Prometheus query) and drives an HPA, why it can scale to zero and an ordinary HPA cannot, activation threshold versus scaling threshold, the cost of a cold start when a GPU pod must load a model (tens of seconds to minutes, hedged), and when to keep minReplicaCount at 1. Give a ScaledObject manifest for a queue-driven batch scorer and a Python simulation of replica count against queue length with a messages-per-pod target; KEDA itself is not executed.
**Asked at:** Autoscaling write-ups (techinterview.org 'System Design Interview: Kubernetes Autoscaling (HPA, VPA, KEDA, Cluster Autoscaler)', AWS EKS ML inference autoscaling HPA and KEDA guide, CloudNativeNow KEDA articles, dev.to VPA/HPA/KEDA patterns; search snippets only, not opened); editorial and vendor docs, not verified candidate reports; senior MLOps and platform loops
**Say this first (1 line):** KEDA watches an external signal such as queue depth, drives an HPA for you, and can take a workload to zero and back, which a plain HPA cannot do.

**Then explain:**
- **How it works.** You create a `ScaledObject` pointing at a Deployment, with triggers. KEDA's operator polls the signal (`pollingInterval`), creates and manages an HPA for 1 to N replicas using an external metric, and itself handles the 0 to 1 and 1 to 0 steps. Triggers exist for Kafka, SQS, Redis lists, Prometheus queries and many more (check the current scaler list).
- **Two thresholds.** The scaling target (for example `queueLength: 50` messages per pod) decides how many replicas: roughly `ceil(messages / target)`. The activation threshold decides whether to leave zero at all (for SQS `activationQueueLength`, default 0, so any message wakes it). `cooldownPeriod` is the wait with no activity before going to zero.
- **Why plain HPA cannot do zero.** HPA needs running pods to compute per-pod metrics and normally has a minimum of 1 (scale-to-zero exists only behind a feature gate in some versions, check docs). KEDA's activation step handles the empty case.
- **Cold-start cost for ML.** A GPU pod from zero needs: a node (maybe a scale-up of minutes), image pull, driver and plugin readiness, then model load. That can be tens of seconds to several minutes (hedged, depends on image and model size). For batch scoring that is fine. For latency-sensitive APIs keep `minReplicaCount: 1` (or more) and scale on latency or RPS.
- **Failure modes.** Kafka: replicas above the partition count do nothing. Queue consumers killed mid-message on scale-down: the message reappears after the visibility timeout, so make processing idempotent and give a graceful shutdown. Credentials in the trigger need a TriggerAuthentication. A flapping signal causes thrash: tune cooldown and the HPA scale-down behaviour. KEDA being down means no scaling from zero.

**Example:** Made-up inputs: target 50 messages per pod, each ready pod finishes 40 messages per tick (30 s), a new pod needs 4 ticks (2 min) to be ready, max 10. Messages arrive: 100 per tick for 4 ticks, then 400 per tick for 3 ticks. At the first tick with 100 messages the desired count is ceil(100/50) = 2; queue 400 gives 8; queue 720 gives 16, capped at 10. With `minReplicaCount: 0` the first message waits 120 s (the cold start); with 1 warm pod it is processed at once. After the burst, replicas stay up through the scale-down window and the cooldown before dropping to zero (the table shows 10 pods from tick 6, 8 pods at tick 20 and zero at tick 21).

**Code:**
```yaml
# ---- scaledobject.yaml ----
apiVersion: keda.sh/v1alpha1           # KEDA is an add-on with its own CRDs; field names: check current KEDA docs
kind: ScaledObject
metadata:
  name: batch-scorer
spec:
  scaleTargetRef:
    name: batch-scorer                 # a Deployment in the same namespace
  pollingInterval: 30                  # seconds between checks of the queue
  cooldownPeriod: 300                  # seconds of 'inactive' before going to minReplicaCount (when that is 0)
  minReplicaCount: 0                   # 0 = scale to zero; use 1 if the cold start is too slow
  maxReplicaCount: 10
  triggers:
    - type: aws-sqs-queue
      authenticationRef:
        name: sqs-auth                 # a TriggerAuthentication (not shown): keeps credentials out of this file
      metadata:
        queueURL: https://sqs.ap-south-1.amazonaws.com/123456789012/scoring-jobs   # placeholder
        awsRegion: ap-south-1
        queueLength: "50"              # target messages per pod: replicas ~ ceil(messages / 50)
        activationQueueLength: "0"     # scale 0 -> 1 only when messages > 0
```

```python
# ---- keda_sim.py ----
"""Queue length -> replicas, KEDA/HPA style. Made-up numbers; a model of the rules, not KEDA code.
One tick = 30 s (pollingInterval)."""
import math

TARGET = 50          # messages per pod (queueLength)
RATE = 40            # messages one READY pod finishes per tick
COLD = 4             # ticks (= 120 s) for a new pod to become ready: made-up, GPU/model load can be longer
MAXR, COOLDOWN, STAB = 10, 10, 10   # max replicas; ticks before scale to zero; HPA scale-down window in ticks
ARRIVALS = [0, 0] + [100] * 4 + [400] * 3 + [0] * 20          # messages arriving per tick

def run(min_replicas, verbose):
    queue, pods, window, last_active = 0, [], [], -99      # pods = list of tick when each becomes ready
    first_done, idle_pod_ticks, prev = None, 0, None
    if min_replicas: pods = [-1] * min_replicas              # warm pods already ready
    if verbose: print(f"{'tick':>4} {'arrive':>6} {'queue':>5} {'desired':>7} {'pods':>4} {'ready':>5} {'done':>5}")
    for t, arr in enumerate(ARRIVALS):
        queue += arr
        if queue > 0 or arr > 0: last_active = t
        desired = math.ceil(queue / TARGET)                  # HPA rule for an AverageValue target
        window = (window + [desired])[-STAB:]
        want = min(MAXR, max(window))                        # up: immediate. down: highest of the last STAB ticks
        floor = 1 if (t - last_active) < COOLDOWN else 0     # stay at 1 until cooldown passes
        want = max(want, floor, min_replicas)
        while len(pods) < want: pods.append(t + COLD)        # new pod: ready COLD ticks later
        while len(pods) > want: pods.pop()                   # remove the newest first
        ready = sum(1 for r in pods if r <= t)
        done = min(queue, ready * RATE); queue -= done
        if done and first_done is None: first_done = t
        if queue == 0 and arr == 0: idle_pod_ticks += len(pods)
        if verbose and (t <= 12 or len(pods) != prev):     # print early ticks and every change in pod count
            print(f"{t:>4} {arr:>6} {queue:>5} {desired:>7} {len(pods):>4} {ready:>5} {done:>5}")
        prev = len(pods)
    return first_done, idle_pod_ticks

print("=== minReplicaCount 0 ===")
f0, idle0 = run(0, True)
f1, idle1 = run(1, False)
print()
print(f"first message processed at tick: min=0 -> {f0} ({(f0 - 2) * 30} s after the first message at tick 2);  min=1 -> {f1} ({(f1 - 2) * 30} s)")
print(f"pod-ticks spent with an empty queue: min=0 -> {idle0};  min=1 -> {idle1}")
```

**Output (my run):**
**Not executed:** KEDA, HPA, SQS and any real scaling (no cluster). The ScaledObject is also not schema-validated by `kubernetes-validate`, since it is a KEDA CRD; I only parsed it with PyYAML and printed key fields. Field and scaler names are from memory of KEDA's docs (hedge: check the current KEDA docs for your version). The simulation uses made-up numbers and simplified rules (a 10-tick scale-down window and 10-tick cooldown, i.e. 5 minutes each, as an assumption; check real defaults).

```text
$ python3 -I keda_sim.py
=== minReplicaCount 0 ===
tick arrive queue desired pods ready  done
   0      0     0       0    0     0     0
   1      0     0       0    0     0     0
   2    100   100       2    2     0     0
   3    100   200       4    4     0     0
   4    100   300       6    6     0     0
   5    100   400       8    8     0     0
   6    400   720      16   10     2    80
   7    400   960      23   10     4   160
   8    400  1120      28   10     6   240
   9      0   800      23   10     8   320
  10      0   400      16   10    10   400
  11      0     0       8   10    10   400
  12      0     0       0   10    10     0
  20      0     0       0    8     8     0
  21      0     0       0    0     0     0

first message processed at tick: min=0 -> 6 (120 s after the first message at tick 2);  min=1 -> 2 (0 s)
pod-ticks spent with an empty queue: min=0 -> 98;  min=1 -> 108

$ python3 -I -c "import yaml; d=yaml.safe_load(open('scaledobject.yaml')); s=d['spec']; print(d['kind'], 'min', s['minReplicaCount'], 'max', s['maxReplicaCount'], 'trigger', s['triggers'][0]['type'], 'target', s['triggers'][0]['metadata']['queueLength'])"
ScaledObject min 0 max 10 trigger aws-sqs-queue target 50
```

**Follow-ups:**
- **ScaledObject or ScaledJob?** ScaledObject scales a long-running Deployment. ScaledJob creates a Job per batch of work, which suits long, non-restartable tasks.
- **How do you avoid losing in-flight work on scale-down?** Handle SIGTERM, finish or requeue the message, set `terminationGracePeriodSeconds`, and make processing idempotent.
- **Can KEDA scale on GPU utilisation?** Through a Prometheus trigger on a GPU metric, if you export one; for queue-based work the queue is usually the better signal.

**Common mistakes:**
- Scaling an API to zero and then being surprised by a slow first request.
- Kafka max replicas above the number of partitions.
- Confusing the activation threshold with the scaling target.
- Using CPU for a GPU-bound consumer and never scaling up.
- Putting cloud credentials in the ScaledObject instead of a TriggerAuthentication or workload identity.

### Q20 ⭐⭐ 🔴 Cluster autoscaling for GPU nodes without paying for idle GPUs. Explain how a node pool or node group with min and max size, taints and labels works with Cluster Autoscaler or Karpenter-style provisioning, why a Pending GPU pod triggers a scale-up, scale-down delay and what blocks scale-down (pods without controllers, local storage, PodDisruptionBudgets, long-running training), spot or preemptible GPU nodes and checkpointing, and how long a GPU node takes to become useful (instance start, driver, image pull). Give a sizing example with made-up round numbers and a script that simulates scale-up and scale-down decisions. Cloud behaviour is not executed; check current docs.
**Asked at:** Autoscaling write-ups (techinterview.org 'System Design Interview: Kubernetes Autoscaling (HPA, VPA, KEDA, Cluster Autoscaler)', AWS EKS ML inference autoscaling HPA and KEDA guide, CloudNativeNow KEDA articles, dev.to VPA/HPA/KEDA patterns; search snippets only, not opened); editorial and vendor docs, not verified candidate reports; senior MLOps and platform loops
**Say this first (1 line):** A Pending GPU pod makes the autoscaler add a node from a labelled, tainted GPU pool, and scale-down removes only nodes that look underused for a while and have nothing that blocks eviction; the real cost fight is idle nodes and slow starts.

**Then explain:**
- **Node pool.** A group of identical nodes with min and max size, labels, taints and a GPU type, managed by the cloud. Cluster Autoscaler works per node group. Karpenter-style provisioners instead pick instance types dynamically from the Pending pods' needs (names and fields differ by version, check current docs). Taint the GPU pool so CPU pods stay away; GPU pods tolerate it and select the pool.
- **Scale-up.** The autoscaler sees a Pending pod, simulates 'would it fit on a new node of group X', and requests a node. It only helps if the pod would actually fit there (right taints, selector, size) and the pool is below max. If the pod needs 4 GPUs and nodes have 2, a new node does not help.
- **Time to useful.** Instance start, then driver and device plugin, then image pull (GPU images are big), then model load. In the toy I use 3 + 2 + 5 = 10 minutes as a made-up total. Plan for slow first minutes; warm pools or pre-pulled images shorten it (check your cloud).
- **Scale-down.** A node is a candidate when requested use is under a threshold and its pods can be moved, and it stays that way for a delay (a default of about ten minutes is common, check docs). Blockers: pods with no controller (bare pods), pods with local storage unless marked safe to evict, PodDisruptionBudgets that allow no disruption, a `safe-to-evict: "false"` annotation, system pods, and long training jobs you must not kill.
- **Spot or preemptible GPUs.** Cheaper but can vanish with short notice. Use them for work that checkpoints and resumes (see the Job in Q12), keep serving on stable capacity or mix pools, and handle the interruption signal.
- **Failure modes.** Pool at max leaves pods Pending forever. A forgotten notebook (bare pod) keeps a whole GPU node alive. Wrong requests make the autoscaler think nodes are full or empty. Scale-up works but model load makes the first requests time out.

**Example:** Made-up round numbers: 4 GPUs per node, pool 0 to 3 nodes. At t=0 a 4-GPU training pod and two 2-GPU serving pods are Pending. Hand-pack: 4 -> node 1; 2 + 2 -> node 2. So 2 nodes, ready at t=10. At t=40 a 1-GPU notebook (bare pod) needs a third node (ready at t=50). Training ends at t=60: node 1 is empty, marked unneeded, removed at t=70. At t=80 serving is removed: node 2 empty, removed at t=90. Node 3 holds only the bare notebook at 25 percent use and stays, because it cannot be evicted. Billed node-minutes 241 versus 360 for 3 static nodes over 120 minutes (nodes are billed from creation, not from ready).

**Code:**
```yaml
# ---- gpu-workloads.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scorer
spec:
  replicas: 2
  selector:
    matchLabels: {app: scorer}
  template:
    metadata:
      labels: {app: scorer}
    spec:
      nodeSelector:
        pool: gpu-pool                   # label that every node of the GPU pool carries
      tolerations:
        - {key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}
      containers:
        - name: server
          image: registry.example.com/ml/scorer:3.1.0
          resources:
            requests: {cpu: "2", memory: 8Gi}
            limits: {memory: 8Gi, nvidia.com/gpu: 1}
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: scorer-pdb
spec:
  minAvailable: 1                        # a scale-down drain may never take the last scorer
  selector:
    matchLabels: {app: scorer}
---
apiVersion: batch/v1
kind: Job
metadata:
  name: train-long
spec:
  backoffLimit: 3
  template:
    metadata:
      annotations:
        # Tells Cluster Autoscaler not to evict this pod to empty a node. Karpenter has its own do-not-disrupt style
        # annotation; names differ by project and version, check current docs.
        cluster-autoscaler.kubernetes.io/safe-to-evict: "false"
    spec:
      restartPolicy: OnFailure
      nodeSelector:
        pool: gpu-pool
      tolerations:
        - {key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}
      containers:
        - name: train
          image: registry.example.com/ml/train:2.3.0
          command: ["python", "train.py", "--resume-from", "/ckpt/latest.pt"]   # checkpoints make spot loss survivable
          resources:
            requests: {cpu: "8", memory: 32Gi}
            limits: {memory: 32Gi, nvidia.com/gpu: 4}
```

```python
# ---- ca_sim.py ----
"""Scale-up / scale-down decisions of a GPU node pool, one tick = 1 minute. Made-up round numbers.
A model of the usual Cluster Autoscaler rules, NOT its code. Real defaults and flags: check current docs."""
import math

GPUS_PER_NODE, POOL_MAX, POOL_MIN = 4, 3, 0
READY_AFTER = 3 + 2 + 5        # minutes: instance start + driver/device plugin + image pull (made up)
UNNEEDED_FOR, UTIL_BELOW = 10, 0.5   # node must look removable for 10 min; 'low use' = under 50% of GPUs

nodes, pods, n_counter, node_minutes, warned = {}, {}, 0, 0, set()

def add_pod(name, gpus, kind, **flags):
    pods[name] = dict(gpus=gpus, kind=kind, node=None, **flags)

EVENTS = {
    0:  lambda: [add_pod("train-A", 4, "job", no_evict=True), add_pod("serve-B", 2, "deploy"), add_pod("serve-C", 2, "deploy")],
    40: lambda: add_pod("notebook-E", 1, "bare"),
    60: lambda: pods.pop("train-A"),                      # training finished
    80: lambda: [pods.pop("serve-B"), pods.pop("serve-C")],
}

def used(n): return sum(p["gpus"] for p in pods.values() if p["node"] == n)

def blockers(n):
    out = []
    for name, p in pods.items():
        if p["node"] != n: continue
        if p["kind"] == "bare": out.append(f"{name}: no controller (cannot be recreated elsewhere)")
        if p.get("no_evict"): out.append(f"{name}: safe-to-evict=false")
    return out

for t in range(121):
    if t in EVENTS: EVENTS[t]()
    # 1. place pending pods on READY nodes with room (first fit)
    for name, p in pods.items():
        if p["node"] is None:
            for n, nd in nodes.items():
                if nd["ready_at"] <= t and GPUS_PER_NODE - used(n) >= p["gpus"]:
                    p["node"] = n; print(f"t={t:3} {name} placed on {n}"); break
    # 2. scale up: pending pods that fit on no ready OR starting node need new nodes (first-fit decreasing)
    pending = sorted((p["gpus"], nm) for nm, p in pods.items() if p["node"] is None)[::-1]
    free = [GPUS_PER_NODE - used(n) for n, nd in nodes.items()]       # ready or starting, current free
    for g, nm in pending:
        for i, f in enumerate(free):
            if f >= g: free[i] -= g; break
        else:
            if len(nodes) < POOL_MAX:
                n_counter += 1; n = f"gpu-node-{n_counter}"
                nodes[n] = dict(ready_at=t + READY_AFTER, unneeded=None)
                free.append(GPUS_PER_NODE - g)
                print(f"t={t:3} scale UP: {nm} ({g} GPU) is Pending and fits no node -> {n}, ready at t={t + READY_AFTER}")
            else:
                print(f"t={t:3} {nm} stays Pending: pool at max {POOL_MAX}")
    # 3. scale down
    for n, nd in list(nodes.items()):
        if nd["ready_at"] > t: continue
        util = used(n) / GPUS_PER_NODE
        if util >= UTIL_BELOW or len(nodes) <= POOL_MIN:
            nd["unneeded"] = None; continue
        b = blockers(n)
        if b:
            key = (n, tuple(b))
            if key not in warned: warned.add(key); print(f"t={t:3} {n} util {util:.0%} but NOT removable: {b}")
            nd["unneeded"] = None; continue
        if nd["unneeded"] is None:
            nd["unneeded"] = t; print(f"t={t:3} {n} util {util:.0%}, marked unneeded")
        elif t - nd["unneeded"] >= UNNEEDED_FOR:
            print(f"t={t:3} scale DOWN: removing {n} (unneeded for {t - nd['unneeded']} min)")
            for p in pods.values():
                if p["node"] == n: p["node"] = None       # would be evicted and rescheduled (none here)
            del nodes[n]
    node_minutes += len(nodes)

print(f"\nnodes at t=120: {sorted(nodes)}   billed node-minutes: {node_minutes}   (3 static nodes for 120 min = {3 * 120})")
print(f"still held by a bare pod: {[n for n in nodes if any(p['kind'] == 'bare' and p['node'] == n for p in pods.values())]}")
```

```bash
# ---- ca_flags.sh ----
# NOT EXECUTED. Example Cluster Autoscaler container args (self-managed install). Flag names exist in the
# upstream project but defaults and cloud-specific flags change; check the current FAQ for your version.
CA_ARGS=(
  --nodes=0:3:gpu-pool   # min:max:node-group-name  (0 = pool may be empty)
  --scale-down-unneeded-time=10m   # how long a node must look removable before it is deleted
  --scale-down-utilization-threshold=0.5   # below this share of requests, a node is a removal candidate
  --balance-similar-node-groups=false
  --skip-nodes-with-local-storage=true   # nodes with emptyDir/hostPath pods are skipped unless the pod is marked safe
  --skip-nodes-with-system-pods=true
)
```

**Output (my run):**
**Not executed:** any cloud node group, Cluster Autoscaler, Karpenter, GPU node or real timing (no cluster, no cloud). Flag names in `ca_flags.sh` are only syntax-checked with `bash -n`; defaults and flags change by version and cloud, check the current docs. What did run: `kubernetes-validate --strict` on the manifests (schema only) and `ca_sim.py`, my own simulation of scale-up, scale-down and blockers with the made-up numbers above. It models the rules, not the real autoscaler code.

```text
$ kubernetes-validate --strict gpu-workloads.yaml
INFO gpu-workloads.yaml passed for resource deployment/scorer against version 1.37
INFO gpu-workloads.yaml passed for resource poddisruptionbudget/scorer-pdb against version 1.37
INFO gpu-workloads.yaml passed for resource job/train-long against version 1.37

$ python3 -I ca_sim.py
t=  0 scale UP: train-A (4 GPU) is Pending and fits no node -> gpu-node-1, ready at t=10
t=  0 scale UP: serve-C (2 GPU) is Pending and fits no node -> gpu-node-2, ready at t=10
t= 10 train-A placed on gpu-node-1
t= 10 serve-B placed on gpu-node-2
t= 10 serve-C placed on gpu-node-2
t= 40 scale UP: notebook-E (1 GPU) is Pending and fits no node -> gpu-node-3, ready at t=50
t= 50 notebook-E placed on gpu-node-3
t= 50 gpu-node-3 util 25% but NOT removable: ['notebook-E: no controller (cannot be recreated elsewhere)']
t= 60 gpu-node-1 util 0%, marked unneeded
t= 70 scale DOWN: removing gpu-node-1 (unneeded for 10 min)
t= 80 gpu-node-2 util 0%, marked unneeded
t= 90 scale DOWN: removing gpu-node-2 (unneeded for 10 min)

nodes at t=120: ['gpu-node-3']   billed node-minutes: 241   (3 static nodes for 120 min = 360)
still held by a bare pod: ['gpu-node-3']

$ bash -n ca_flags.sh && echo 'bash -n ca_flags.sh: syntax OK'
bash -n ca_flags.sh: syntax OK
```

**Follow-ups:**
- **How do you keep one GPU node warm for latency?** Keep a minimum of 1 in the pool for serving (or a low-priority placeholder pod that gets preempted), accept the cost of that one node.
- **Cluster Autoscaler or Karpenter?** Autoscaler is group-based and common; Karpenter-style tools choose instance types per pod demand. Pick by cloud support and your control needs; check current docs.
- **How do you stop training pods being evicted?** Annotate against eviction and use a PDB for serving, but also checkpoint, because nodes can still fail or be preempted.

**Common mistakes:**
- Letting bare pods and notebooks run on the GPU pool.
- No taint on the GPU pool, so CPU pods land there and keep it alive.
- Counting only GPU price and ignoring 10 or more minutes of startup.
- Pool max too low, so Pending never clears.
- Using spot GPUs for jobs that cannot resume.

### Q21 ⭐⭐ 🔴 GPU sharing on Kubernetes: whole GPU, time-slicing, MIG and MPS. Explain what the NVIDIA device plugin and GPU Operator do, how time-slicing advertises several replicas of one GPU with no memory or fault isolation, how MIG partitions supported data-centre GPUs into hardware-isolated instances exposed under their own resource names, and when each fits (small inference models, notebooks, noisy neighbours, strict isolation). Show a device plugin time-slicing ConfigMap-style snippet, a pod requesting a MIG resource (names hedged), and a script that works out VRAM per replica and flags a model that would not fit. No GPU here; nothing is executed.
**Asked at:** Kubernetes-for-AI question bank (Cloud Soft Solutions 'Kubernetes for AI interview questions'), NerdLevelTech MLOps interview course page, KodeKloud MLOps guide, SuperOrbital/CNCF NVIDIA device plugin post, NVIDIA GPU Operator time-slicing docs (v1.11 page only), University of Bergen RAIL GPU docs; search snippets only, not opened (WebFetch failed with ENOTFOUND); guides and docs, not verified candidate reports; GPU and deep-learning MLOps roles at product companies, GCCs and AI startups
**Say this first (1 line):** A GPU is one integer unit by default; time-slicing lets several pods share one GPU with no memory or fault walls, MIG cuts a supported GPU into hardware-isolated slices, and I pick by how much isolation the workload needs.

**Then explain:**
- **Device plugin and GPU Operator.** The NVIDIA device plugin is a DaemonSet on GPU nodes. It tells the kubelet "this node has N `nvidia.com/gpu`". Kubernetes sees only whole integers, no fractions. The GPU Operator installs the pieces for you: driver, container toolkit, device plugin, GPU feature discovery labels, DCGM metrics, MIG manager. Check current docs for versions.
- **Whole GPU.** Best for training and big models. Full memory, full speed, no neighbours.
- **Time-slicing.** You set `replicas: 4` in a config. The node then advertises 4 `nvidia.com/gpu` for one physical GPU. Pods take turns on the GPU. **No memory limit and no fault isolation.** One pod can eat all VRAM and the rest crash. Good for notebooks and small dev inference. Asking for 2 does not promise 2 different physical GPUs.
- **MIG (Multi-Instance GPU).** On supported data-centre GPUs, one card is split into hardware-isolated instances, each with its own memory and compute. Each profile gets its own resource name, such as `nvidia.com/mig-1g.10gb` (names depend on GPU and strategy: check current docs). Changing the layout needs the node drained of GPU pods. Good for small models with strict isolation, many tenants.
- **MPS.** CUDA's Multi-Process Service lets several processes share the GPU at the same time (not just turns). Some device plugin versions can enable it; support and limits vary, so check current docs.
- **Failure modes:** a time-sliced pod OOMs its neighbours; a model bigger than the MIG slice never loads; one pool mixes MIG and non-MIG nodes with no node labels, so pods land wrong; no taint on GPU nodes, so CPU pods squat there.

**Example:** GPU has 40 GB (made-up). Time-slicing x4 means an even share of 10 GB, but nothing enforces it. Four models of 6 GB use 24 GB; with 20% headroom that is 28.8 GB, fine. If one model is 18 GB, the sum with headroom is 43.2 GB, over the pool, so the script flags OOM risk. On MIG, a 7 GB model with headroom needs 8.4 GB: a `1g.5gb` slice (5 GB) is a hard no, a `2g.10gb` slice fits.

**Code:**
```yaml
# ---- gpu_share.yaml ----
# Time-slicing config for the NVIDIA device plugin (ConfigMap-style).
# Field names follow the GPU Operator time-slicing docs; check current docs for your version.
apiVersion: v1
kind: ConfigMap
metadata:
  name: time-slicing-config
  namespace: gpu-operator
data:
  any: |-
    version: v1
    flags:
      migStrategy: none
    sharing:
      timeSlicing:
        resources:
          - name: nvidia.com/gpu
            replicas: 4
---
# Pod asking for ONE MIG slice. Resource name depends on GPU model and MIG strategy (mixed).
apiVersion: v1
kind: Pod
metadata:
  name: small-model
  labels:
    app: small-model
spec:
  tolerations:
    - key: nvidia.com/gpu
      operator: Exists
      effect: NoSchedule
  containers:
    - name: server
      image: registry.example.com/small-model:1.0
      resources:
        limits:
          nvidia.com/mig-1g.10gb: 1
```

```python
# ---- vram_fit.py ----
"""VRAM per replica for time-slicing and MIG, plus fit flags. All sizes are made-up round numbers."""
import yaml
cm = next(d for d in yaml.safe_load_all(open("gpu_share.yaml")) if d["kind"] == "ConfigMap")
REPLICAS = yaml.safe_load(cm["data"]["any"])["sharing"]["timeSlicing"]["resources"][0]["replicas"]
print("replicas parsed from the ConfigMap:", REPLICAS)
GPU_GB = 40                                              # assumed whole-GPU memory
MIG_GB = {"1g.5gb": 5, "2g.10gb": 10, "3g.20gb": 20}     # assumed profile sizes
HEADROOM = 1.2                                           # activations, CUDA context, KV cache

def time_slicing(replicas, models_gb):
    share = GPU_GB / replicas
    total = sum(m * HEADROOM for m in models_gb)
    flags = [f"model {m} GB is above the even share {share:g} GB" for m in models_gb if m > share]
    if total > GPU_GB:
        flags.append(f"sum with headroom {total:g} GB > {GPU_GB} GB pool: OOM risk")
    if len(models_gb) > replicas:
        flags.append("more pods than advertised replicas: extra pods stay Pending")
    return flags or ["ok on paper (still no isolation: one pod can eat the pool)"]

def mig(profile, model_gb):
    need = model_gb * HEADROOM
    cap = MIG_GB[profile]
    return "fits" if need <= cap else f"DOES NOT FIT ({need:g} GB needed > {cap} GB, hard cap)"

print(f"time-slicing x{REPLICAS}, models 6,6,6,6 GB:", time_slicing(REPLICAS, [6, 6, 6, 6]))
print(f"time-slicing x{REPLICAS}, models 6,6,6,18 GB:", time_slicing(REPLICAS, [6, 6, 6, 18]))
print("time-slicing x2, models 6,6,6 GB:", time_slicing(2, [6, 6, 6]))
for p in MIG_GB:
    print(f"MIG {p} for a 7 GB model:", mig(p, 7))
```

**Output (my run):**
**Not executed:** the device plugin, GPU Operator, time-slicing and MIG need a GPU node and a cluster. Nothing here talks to a GPU. What did run: the VRAM script (it also parses the ConfigMap's embedded YAML and reads `replicas`), and `kubernetes-validate --strict` on the ConfigMap and Pod (kubernetes-validate 1.37.0). The validator checks schema only; it cannot know whether `nvidia.com/mig-1g.10gb` exists on your nodes.

```text
$ python3 -I vram_fit.py
replicas parsed from the ConfigMap: 4
time-slicing x4, models 6,6,6,6 GB: ['ok on paper (still no isolation: one pod can eat the pool)']
time-slicing x4, models 6,6,6,18 GB: ['model 18 GB is above the even share 10 GB', 'sum with headroom 43.2 GB > 40 GB pool: OOM risk']
time-slicing x2, models 6,6,6 GB: ['more pods than advertised replicas: extra pods stay Pending']
MIG 1g.5gb for a 7 GB model: DOES NOT FIT (8.4 GB needed > 5 GB, hard cap)
MIG 2g.10gb for a 7 GB model: fits
MIG 3g.20gb for a 7 GB model: fits

$ kubernetes-validate --strict gpu_share.yaml; echo "exit code: $?"
INFO gpu_share.yaml passed for resource configmap/time-slicing-config against version 1.37
INFO gpu_share.yaml passed for resource pod/small-model against version 1.37
exit code: 0
```

**Follow-ups:**
- **Can I get a fraction of a GPU with a plain request?** No. `nvidia.com/gpu` is an integer. Fractions come from time-slicing replicas, MIG, MPS, or newer Dynamic Resource Allocation (DRA), whose status depends on your Kubernetes version.
- **Time-slicing or MIG for multi-tenant?** MIG, because of memory and fault isolation. Time-slicing is for trusted users and dev work.
- **Why taint GPU nodes?** So only pods that tolerate `nvidia.com/gpu` land on them; otherwise cheap CPU pods use the expensive node.

**Common mistakes:**
- Calling time-slicing "isolation". It is sharing in turns; memory is shared.
- Assuming every GPU supports MIG. Only some data-centre models do; check the support matrix.
- Copying resource names from a blog. MIG names depend on the GPU model and MIG strategy.
- Forgetting headroom for activations, CUDA context and caches when sizing slices.

### Q22 ⭐⭐ 🟡 Helm values, templating functions and helpers in practice. Explain the template syntax {{ .Values.x }}, default, quote, toYaml, nindent, include and named templates in _helpers.tpl, if and range blocks, whitespace control with {{- and -}}, required for mandatory values, and how values.schema.json rejects bad values early. Write a Deployment template that renders optional GPU limits and tolerations only when set, and a values.schema.json. Validate the schema with the jsonschema Python library and the YAML with a script; helm template itself is not executed because helm is unavailable.
**Asked at:** Editorial Helm interview guides (KodeKloud, Hyring, TechPrep '213 Helm interview questions', ClimbTheLadder, InterviewPrep.org, OneUptime Helm rollback guide; search snippets only, not opened); guides, not verified candidate reports; DevOps and MLOps screens
**Say this first (1 line):** Helm renders Go templates with values into plain YAML; I keep logic small, use `default`, `required`, `toYaml | nindent` and `with`/`if` guards, and let `values.schema.json` reject bad values before anything is rendered.

**Then explain:**
- **Syntax.** `{{ .Values.x }}` reads a value. A pipe passes it on: `{{ .Values.image.tag | default .Chart.AppVersion | quote }}`. `quote` makes it a YAML string (saves you from `on`, `1.10` or `0123` being read as other types).
- **Blocks.** `{{- if ... }}` / `{{- end }}` for options, `{{- with .Values.tolerations }}` to render only when set (and rebind `.`), `{{- range ... }}` to loop. Inside `with` and `range`, `.` changes. Use `$.Values` to reach the root.
- **Whitespace.** `{{-` trims spaces and newline before, `-}}` after. Lists and maps: `{{- toYaml . | nindent 8 }}` prints YAML, starts a new line and indents by 8. Wrong indent = wrong YAML, the most common template bug.
- **Helpers.** `_helpers.tpl` holds named templates (`define "model-api.labels"`). `include "name" . | nindent 4` returns a string you can pipe. `template` prints directly, so it cannot be piped.
- **Fail early.** `required "message" .Values.modelUri` stops the render with that message. `values.schema.json` (JSON Schema) is checked on install, upgrade, lint and template, so wrong types, bad enums and out-of-range numbers fail before manifests are built. Schema checks shape; `required` checks "was it really set".
- **Failure modes:** `default` treats `0`, `false` and `""` as unset, so `default true .Values.flag` can never be false; a list in an override file **replaces** the base list (maps merge); big integers from `--set` can print as floats unless you wrap them in `int`; `kubectl apply` of a template with a stray tab fails only at install time unless you lint and validate.

**Example:** Values: `gpu.count: 1`. The guard `{{- if gt (int .Values.gpu.count) 0 }}` adds the line `nvidia.com/gpu: 1` under `limits`. With `gpu.count: 0` that line is absent, so the pod can run on CPU nodes. If someone sets `gpu.count: "two"` the schema rejects it. If `modelUri` is empty, `required` stops the render with the message.

**Code:**
```yaml
# ---- chart/Chart.yaml ----
apiVersion: v2
name: model-api
version: 0.1.0
appVersion: "1.4.2"

# ---- chart/values.yaml ----
replicaCount: 2
image:
  repository: registry.example.com/model-api
  tag: ""            # empty -> falls back to .Chart.AppVersion
  pullPolicy: IfNotPresent
service:
  port: 8080
gpu:
  count: 0           # 0 = CPU only, no GPU limit rendered
resources:
  requests: {cpu: 500m, memory: 1Gi}
  limits: {memory: 2Gi}
tolerations: []
modelUri: ""         # required: chart refuses to render without it
```

```gotemplate
{{/* ---- chart/templates/_helpers.tpl ---- */}}
{{- define "model-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "model-api.labels" -}}
app.kubernetes.io/name: {{ include "model-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/* ---- chart/templates/deployment.yaml ---- */}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "model-api.name" . }}
  labels:
    {{- include "model-api.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "model-api.name" . }}
  template:
    metadata:
      labels:
        {{- include "model-api.labels" . | nindent 8 }}
    spec:
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
        - name: server
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          env:
            - name: MODEL_URI
              value: {{ required "modelUri is required (--set modelUri=s3://...)" .Values.modelUri | quote }}
          ports:
            - containerPort: {{ .Values.service.port }}
          resources:
            requests:
              {{- toYaml .Values.resources.requests | nindent 14 }}
            limits:
              {{- toYaml .Values.resources.limits | nindent 14 }}
              {{- if gt (int .Values.gpu.count) 0 }}
              nvidia.com/gpu: {{ .Values.gpu.count }}
              {{- end }}
```

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["image", "service"],
  "properties": {
    "replicaCount": {"type": "integer", "minimum": 1},
    "image": {
      "type": "object",
      "required": ["repository"],
      "properties": {
        "repository": {"type": "string", "minLength": 1},
        "tag": {"type": "string"},
        "pullPolicy": {"enum": ["Always", "IfNotPresent", "Never"]}
      }
    },
    "service": {
      "type": "object",
      "properties": {"port": {"type": "integer", "minimum": 1, "maximum": 65535}}
    },
    "gpu": {
      "type": "object",
      "properties": {"count": {"type": "integer", "minimum": 0, "maximum": 8}}
    },
    "tolerations": {"type": "array"},
    "modelUri": {"type": "string"}
  }
}
```

```python
# ---- render_check.py ----
"""NOT helm. A hand-written Python mirror of chart/templates/deployment.yaml logic, used to
(1) check values against values.schema.json, (2) dump the YAML the template should produce,
(3) check the template text still contains the guards we rely on."""
import json, sys, yaml, jsonschema, copy, tempfile, subprocess, os
TMP = tempfile.mkdtemp()

CHART = "chart"
schema = json.load(open(f"{CHART}/values.schema.json"))
defaults = yaml.safe_load(open(f"{CHART}/values.yaml"))

def merge(a, b):
    out = copy.deepcopy(a)
    for k, v in b.items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out

def render(overrides):
    v = merge(defaults, overrides)
    errs = sorted(jsonschema.Draft7Validator(schema).iter_errors(v), key=lambda e: list(e.path))
    if errs:
        return None, [f"schema: {'.'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errs]
    if not v["modelUri"]:                                   # mirrors: required "..." .Values.modelUri
        return None, ["required: modelUri is required (--set modelUri=s3://...)"]
    limits = dict(v["resources"]["limits"])
    if int(v["gpu"]["count"]) > 0:                          # mirrors: if gt (int .Values.gpu.count) 0
        limits["nvidia.com/gpu"] = v["gpu"]["count"]
    spec = {"containers": [{"name": "server",
        "image": f'{v["image"]["repository"]}:{v["image"]["tag"] or "1.4.2"}',   # default .Chart.AppVersion
        "imagePullPolicy": v["image"]["pullPolicy"],
        "env": [{"name": "MODEL_URI", "value": v["modelUri"]}],
        "ports": [{"containerPort": v["service"]["port"]}],
        "resources": {"requests": v["resources"]["requests"], "limits": limits}}]}
    if v["tolerations"]:                                    # mirrors: with .Values.tolerations
        spec["tolerations"] = v["tolerations"]
    labels = {"app.kubernetes.io/name": "model-api", "app.kubernetes.io/instance": "rel"}
    return {"apiVersion": "apps/v1", "kind": "Deployment",
            "metadata": {"name": "model-api", "labels": labels},
            "spec": {"replicas": v["replicaCount"],
                     "selector": {"matchLabels": {"app.kubernetes.io/name": "model-api"}},
                     "template": {"metadata": {"labels": labels}, "spec": spec}}}, []

cases = {
  "cpu-only": {"modelUri": "s3://bucket/m1"},
  "gpu+toleration": {"modelUri": "s3://bucket/m1", "gpu": {"count": 1},
        "tolerations": [{"key": "nvidia.com/gpu", "operator": "Exists", "effect": "NoSchedule"}]},
  "missing modelUri": {},
  "bad pullPolicy + replicas 0": {"modelUri": "x", "image": {"pullPolicy": "Sometimes"}, "replicaCount": 0},
  "gpu count as string": {"modelUri": "x", "gpu": {"count": "two"}},
}
for name, ov in cases.items():
    doc, errs = render(ov)
    print(f"=== {name}")
    if errs:
        print("REJECTED:"); [print("  -", e) for e in errs]
    else:
        path = os.path.join(TMP, name.split("+")[0] + ".yaml")
        yaml.safe_dump(doc, open(path, "w"), sort_keys=False)
        r = subprocess.run(["kubernetes-validate", "--strict", path], capture_output=True, text=True)
        print("kubernetes-validate --strict rc =", r.returncode, "|", r.stdout.strip().split(" against")[-1])
        lim = doc["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]
        print("OK limits:", lim, "| tolerations:", "tolerations" in doc["spec"]["template"]["spec"])

tpl = open(f"{CHART}/templates/deployment.yaml").read()
for needle in ["required ", "toYaml", "nindent", "with .Values.tolerations", "gt (int .Values.gpu.count) 0", "include "]:
    print(f"template contains {needle!r}:", needle in tpl)
```

**Output (my run):**
**Not executed:** `helm lint`, `helm template` and `helm install` (helm is not installed here and could not be downloaded). So the Go template itself was **never rendered by Helm**. What did run: `render_check.py` is a hand-written Python **mirror** of the template logic (not Helm). It validates values against the real `values.schema.json` with the jsonschema library, produces the Deployment the template is meant to produce, and runs `kubernetes-validate --strict` on that output. It also greps the template text for the guards. Treat it as a model of the template, and run `helm lint` and `helm template` on a real machine.

```text
$ python3 -I render_check.py
=== cpu-only
kubernetes-validate --strict rc = 0 |  version 1.37
OK limits: {'memory': '2Gi'} | tolerations: False
=== gpu+toleration
kubernetes-validate --strict rc = 0 |  version 1.37
OK limits: {'memory': '2Gi', 'nvidia.com/gpu': 1} | tolerations: True
=== missing modelUri
REJECTED:
  - required: modelUri is required (--set modelUri=s3://...)
=== bad pullPolicy + replicas 0
REJECTED:
  - schema: image.pullPolicy: 'Sometimes' is not one of ['Always', 'IfNotPresent', 'Never']
  - schema: replicaCount: 0 is less than the minimum of 1
=== gpu count as string
REJECTED:
  - schema: gpu.count: 'two' is not of type 'integer'
template contains 'required ': True
template contains 'toYaml': True
template contains 'nindent': True
template contains 'with .Values.tolerations': True
template contains 'gt (int .Values.gpu.count) 0': True
template contains 'include ': True
```

**Follow-ups:**
- **Schema or `required`?** Both. Schema for types and ranges, `required` for "must be set" and for a helpful message.
- **Why is my YAML mis-indented?** Probably `nindent` count is wrong or you used `indent` without a leading newline. Run `helm template` and read the output.
- **How do I debug a template?** `helm template --debug`, `helm lint`, and `--dry-run`.

**Common mistakes:**
- Using `with` and then reading `.Values` inside it (dot has changed; use `$.Values`).
- Not quoting values that must be strings, such as image tags like `1.10`.
- Putting secrets in `values.yaml` in git.
- Writing a schema that is too strict on optional fields, so every upgrade breaks.
- Saying "I tested the template" when only a Python mirror ran.

### Q23 ⭐⭐ 🟡 Helm upgrade safety and release management: helm upgrade --install, --atomic, --wait, --timeout, --dry-run, helm diff as a plugin, helm history and rollback, hooks (pre-install, pre-upgrade Jobs for database or model migrations) and their pitfalls, and keeping one chart with per-environment values files (values-dev.yaml, values-prod.yaml). Explain what rollback does and does not undo (it restores manifests, not data or external state), and a failed hook leaving a release in a bad state. Give a CI-style command sequence and a script that checks values files share the same keys. Helm is not executed here.
**Asked at:** Editorial Helm interview guides (KodeKloud, Hyring, TechPrep '213 Helm interview questions', ClimbTheLadder, InterviewPrep.org, OneUptime Helm rollback guide; search snippets only, not opened); guides, not verified candidate reports; DevOps and MLOps screens
**Say this first (1 line):** I upgrade with `helm upgrade --install --atomic --wait --timeout`, review a `helm diff` first, keep one chart with per-environment values files, and remember rollback restores manifests only, not data or external state.

**Then explain:**
- **The command.** `helm upgrade --install` creates the release if missing and upgrades otherwise, so CI uses one command. `--wait` waits until pods are Ready. `--timeout` caps the wait. `--atomic` rolls back automatically if the upgrade fails (it implies waiting). `--dry-run` renders without applying; the `helm diff` plugin (install separately) shows what would change against the live release.
- **History.** Helm 3 stores each revision as a Secret in the release namespace. `helm history` lists them (default history cap is about 10; check current docs). `helm rollback NAME REV` makes a **new** revision with the old manifests.
- **What rollback does not undo.** Database or schema migrations, model files in object storage, PVC contents, a Job that already ran, anything created by hooks (hook resources are not part of the release manifest). If the new model wrote data in a new format, rollback of pods will not fix it.
- **Hooks.** Annotations such as `helm.sh/hook: pre-upgrade` run a Job before the upgrade. Useful for migrations. Pitfalls: a failed hook fails the release; the hook Job is not rolled back; leftover Jobs block re-runs unless you set `helm.sh/hook-delete-policy`; hooks must be idempotent; ordering uses `hook-weight`.
- **Per-environment values.** One chart, `-f values-dev.yaml` or `-f values-prod.yaml`. Later files win; maps merge, lists replace. Keep the same key set everywhere so no environment silently falls back to a default.
- **Failure modes:** an interrupted upgrade leaves the release in `pending-upgrade`, and the next upgrade says another operation is in progress (fix with rollback, or inspect the release Secrets; check current docs); `--atomic` with a too-short timeout rolls back a healthy but slow model load; `--wait` does not prove the model gives good predictions.

**Example:** `values-prod.yaml` has `gpu.type: a100` but `values-dev.yaml` does not. The key check script reports `gpu.type` missing in dev. Either add it to the base `values.yaml` with a default or remove it. Otherwise the template that reads `.Values.gpu.type` renders `<nil>` or empty in dev only.

**Code:**
```yaml
# ---- values-dev.yaml ----
replicaCount: 1
image:
  tag: "dev"
resources:
  requests: {cpu: 250m, memory: 512Mi}
  limits: {memory: 1Gi}
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 2
gpu:
  count: 0
modelUri: s3://models-dev/fraud/3

# ---- values-prod.yaml ----
replicaCount: 3
image:
  tag: "1.4.2"
resources:
  requests: {cpu: "2", memory: 4Gi}
  limits: {memory: 6Gi}
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 12
gpu:
  count: 1
  type: a100          # key exists only in prod: drift
modelUri: s3://models-prod/fraud/3
```

```bash
# ---- deploy.sh ----
#!/usr/bin/env bash
# CI-style release sequence. NOT executed in this sandbox (no helm, no cluster).
set -euo pipefail
ENV="${1:?usage: deploy.sh dev|prod}"
RELEASE=model-api
NS="ml-${ENV}"

helm lint ./chart -f "values-${ENV}.yaml"                         # chart + schema errors
helm template "$RELEASE" ./chart -f "values-${ENV}.yaml" > rendered.yaml
kubernetes-validate --strict rendered.yaml                           # offline schema check (pip install kubernetes-validate)
helm diff upgrade "$RELEASE" ./chart -n "$NS" -f "values-${ENV}.yaml"   # needs the helm-diff plugin
helm upgrade --install "$RELEASE" ./chart -n "$NS" --create-namespace \
  -f "values-${ENV}.yaml" --atomic --wait --timeout 10m           # --atomic rolls back on failure
helm history "$RELEASE" -n "$NS" --max 5
# Manual escape hatch if a bad release got through:
#   helm rollback "$RELEASE" <REVISION> -n "$NS" --wait
```

```python
# ---- check_values.py ----
"""Compare values-*.yaml files: same key paths, flag drift. Values may differ; keys should not."""
import sys, yaml

def paths(d, prefix=""):
    out = set()
    for k, v in d.items():
        p = f"{prefix}{k}"
        if isinstance(v, dict) and v:
            out |= paths(v, p + ".")
        else:
            out.add(p)
    return out

files = sys.argv[1:]
keys = {f: paths(yaml.safe_load(open(f))) for f in files}
union = set().union(*keys.values())
bad = False
for f in files:
    missing = sorted(union - keys[f])
    print(f"{f}: {len(keys[f])} keys; missing: {missing or 'none'}")
    bad |= bool(missing)
print("RESULT:", "DRIFT (fix or add to the base values.yaml)" if bad else "same key set")
sys.exit(1 if bad else 0)
```

**Output (my run):**
**Not executed:** every `helm` command (helm lint, template, diff, upgrade, history, rollback) because helm is not installed here and its download was blocked. So `deploy.sh` is shown, not run. What did run: the key-drift script on the two values files (exit code 1 on drift is the point: CI should fail), and `bash -n` (syntax check only).

```text
$ python3 -I check_values.py values-dev.yaml values-prod.yaml
values-dev.yaml: 10 keys; missing: ['gpu.type']
values-prod.yaml: 11 keys; missing: none
RESULT: DRIFT (fix or add to the base values.yaml)

$ bash -n deploy.sh && echo "bash -n: syntax ok"
bash -n: syntax ok

$ command -v helm || echo "helm: not installed"
helm: not installed
```

**Follow-ups:**
- **`--atomic` or `--wait`?** `--atomic` includes the wait and adds auto-rollback. In CI I use `--atomic`.
- **Why `helm diff`?** To see the real change before it lands, including values that moved by accident.
- **How do I roll back a model?** Roll back the release (old image or model URI), then check data and caches yourself.

**Common mistakes:**
- Believing rollback restores the database or the model registry.
- Running migrations in a hook that is not idempotent, or not deleting finished hook Jobs.
- Different keys per environment, so prod behaves differently from what staging proved.
- A timeout shorter than model load time, causing needless rollbacks.
- Using `latest` image tags: a rollback then re-pulls the same bits.

### Q24 ⭐⭐ 🟡 Pod disruption, node drains and graceful shutdown for model servers. Explain PodDisruptionBudget, kubectl drain and cordon, terminationGracePeriodSeconds, the SIGTERM then SIGKILL sequence, a preStop hook, finishing in-flight requests, and why a pod can still receive traffic briefly after termination starts. Show a Deployment snippet with a PDB, a Python signal-handling test that drains work on SIGTERM (run it for real), and what happens to a long training pod during a node drain. The cluster behaviour is not executed.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** On shutdown Kubernetes sends SIGTERM, waits up to the grace period, then SIGKILL; so the server must stop taking new work, finish in-flight requests and exit, with a PodDisruptionBudget limiting how many pods voluntary drains can take at once.

**Then explain:**
- **PDB.** Limits **voluntary** disruptions: `kubectl drain`, autoscaler scale-down, upgrades. `minAvailable: 2` (or `maxUnavailable`) makes the eviction API refuse to go below that. It does **not** stop node crashes, OOM kills or spot reclaim.
- **Cordon and drain.** `cordon` marks the node unschedulable. `drain` cordons and evicts pods, respecting PDBs. DaemonSet pods need `--ignore-daemonsets`; emptyDir data is lost, so `--delete-emptydir-data` is required.
- **Shutdown sequence.** Pod goes Terminating, it is removed from Service endpoints, the `preStop` hook runs, then SIGTERM goes to each container's main process. After `terminationGracePeriodSeconds` (default 30 s, counted from the start of termination, preStop included) comes SIGKILL.
- **Why traffic still arrives.** Endpoint removal spreads to kube-proxy, ingress and mesh proxies **asynchronously**, so for a moment requests still land. A short `preStop: sleep` (and failing readiness on SIGTERM) bridges the gap, then the app drains.
- **PID 1 trap.** If the app is behind `sh -c`, the shell may not forward SIGTERM. Use `exec`, or a tiny init such as tini. A process that is PID 1 in a container gets no default SIGTERM action, so without a handler it is just killed later by SIGKILL.
- **Long training pod.** A drain evicts it like any pod. Without a checkpoint it loses progress. Save a checkpoint on SIGTERM (and keep the grace period long enough), checkpoint on a schedule, and use the cluster's "do not evict" annotation for work that cannot move (names vary by autoscaler; check current docs).
- **Failure modes:** `minAvailable` equal to replicas gives zero allowed disruptions, so drains hang forever; a grace period shorter than preStop plus drain time truncates requests; one replica plus a PDB blocks node upgrades.

**Example:** 3 replicas, `minAvailable: 2`, so 1 pod may be evicted at a time. Drain node A: pod 1 gets Terminating, `sleep 10` in preStop, SIGTERM, finishes its 3 requests, exits 0. Only after it is gone and a replacement is Ready can the next eviction proceed. Grace is 60 s, which covers 10 s sleep plus drain time.

**Code:**
```yaml
# ---- serve_pdb.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-api
spec:
  replicas: 3
  selector:
    matchLabels: {app: model-api}
  strategy:
    type: RollingUpdate
    rollingUpdate: {maxUnavailable: 0, maxSurge: 1}
  template:
    metadata:
      labels: {app: model-api}
    spec:
      terminationGracePeriodSeconds: 60      # must exceed preStop sleep + drain time
      containers:
        - name: server
          image: registry.example.com/model-api:1.4.2
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet: {path: /ready, port: 8080}
            periodSeconds: 5
          lifecycle:
            preStop:
              exec:
                command: ["sleep", "10"]     # give endpoints/proxies time to stop sending traffic
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: model-api
spec:
  minAvailable: 2                            # voluntary evictions (drain) keep at least 2 pods
  selector:
    matchLabels: {app: model-api}
```

```python
# ---- graceful.py ----
"""Real SIGTERM test: a worker that drains in-flight work vs one that ignores SIGTERM handling."""
import os, signal, subprocess, sys, tempfile, textwrap, time

WORKER = textwrap.dedent('''
    import signal, sys, time
    handle = sys.argv[1] == "graceful"
    stopping = False
    def on_term(signum, frame):
        global stopping
        stopping = True                      # stop taking new work, finish what we have
    if handle:
        signal.signal(signal.SIGTERM, on_term)
    inflight = ["req-1", "req-2", "req-3"]   # pretend these are in-flight requests (0.2 s each)
    print("ready", flush=True)
    done = []
    while True:
        if stopping and not inflight:
            break
        if inflight:
            time.sleep(0.2); done.append(inflight.pop(0))
            print("finished", done[-1], flush=True)
        else:
            time.sleep(0.05)                 # idle loop, waiting for new work
    print("drained", len(done), "requests; exiting 0", flush=True)
    sys.exit(0)
''')

def trial(mode):
    path = os.path.join(tempfile.mkdtemp(), "worker.py")
    open(path, "w").write(WORKER)
    p = subprocess.Popen([sys.executable, "-I", path, mode], stdout=subprocess.PIPE, text=True)
    assert p.stdout.readline().strip() == "ready"
    time.sleep(0.1)                          # first request is in progress
    p.send_signal(signal.SIGTERM)            # what the kubelet sends first
    out, _ = p.communicate(timeout=10)
    return p.returncode, out.strip().splitlines()

for mode in ("graceful", "ignore-handler"):
    rc, lines = trial(mode)
    print(f"--- {mode}: exit code {rc}")
    for l in lines: print("   ", l)
```

**Output (my run):**
**Not executed:** drain, cordon, eviction and PDB enforcement (no cluster). What ran for real: a Python subprocess that gets a real SIGTERM, once with a handler that drains and once with default handling (killed by signal 15, shown as exit code -15 by Python). The YAML was validated with `kubernetes-validate --strict`. Note that this test runs the process as a normal child, not as PID 1 in a container.

```text
$ python3 -I graceful.py
--- graceful: exit code 0
    finished req-1
    finished req-2
    finished req-3
    drained 3 requests; exiting 0
--- ignore-handler: exit code -15

$ kubernetes-validate --strict serve_pdb.yaml; echo "exit code: $?"
INFO serve_pdb.yaml passed for resource deployment/model-api against version 1.37
INFO serve_pdb.yaml passed for resource poddisruptionbudget/model-api against version 1.37
exit code: 0
```

**Follow-ups:**
- **Does a PDB protect me from a node failure?** No, only voluntary evictions.
- **How long should the grace period be?** Longer than preStop plus the slowest request you accept to finish.
- **How do I keep a rolling update from dropping traffic?** `maxUnavailable: 0`, a real readiness probe, preStop and SIGTERM draining.

**Common mistakes:**
- No SIGTERM handler, so requests die at SIGKILL.
- `minAvailable` equal to the replica count, which blocks drains.
- Setting a long grace period but not handling SIGTERM, so every rollout waits the full time.
- Readiness probe that stays green while the server is shutting down.

### Q25 ⭐⭐ 🟡 Pod anti-affinity, topology spread and priority classes for a latency-sensitive inference service. Explain node affinity versus pod affinity and anti-affinity, required versus preferred rules, topologySpreadConstraints across zones, PriorityClass and preemption so serving can evict batch jobs, and the failure mode where hard anti-affinity leaves pods Pending when there are fewer nodes than replicas. Give manifests for a 3-replica spread over zones, and a script that checks if a spread can be satisfied for a given node-to-zone map. Not executed on a cluster.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** For a latency-sensitive service I spread replicas across zones with topology spread, prefer one pod per node with soft anti-affinity, and give serving a higher PriorityClass than batch, while watching that hard rules can leave pods Pending.

**Then explain:**
- **Node affinity** picks nodes by node labels (GPU type, zone). **Pod affinity** pulls pods together (near a cache). **Pod anti-affinity** pushes pods apart (spread replicas).
- **Required or preferred.** `requiredDuringScheduling...` is a hard rule: no match, pod stays Pending. `preferredDuringScheduling...` is a weighted wish. "IgnoredDuringExecution" means it is checked only at scheduling time.
- **topologySpreadConstraints.** `maxSkew: 1` over `topology.kubernetes.io/zone` keeps zone counts within 1 of each other. `DoNotSchedule` is hard, `ScheduleAnyway` is soft. Skew = pods in this zone minus pods in the emptiest eligible zone.
- **PriorityClass.** Higher number wins. When a high-priority pod cannot fit, the scheduler may **preempt** (evict) lower-priority pods. Give batch `preemptionPolicy: Never` so batch never kicks others out. Evicted batch pods must tolerate restarts (checkpoints).
- **Failure modes:** hard anti-affinity with replicas greater than nodes leaves pods Pending; with a rolling update `maxSurge: 1` the extra pod also needs a free node, so rollouts stall; a hard zone spread with one zone lacking capacity leaves pods Pending even when other zones have room; preemption can kill a long training run.

**Example:** 3 nodes in zones a, b, c and 3 replicas: one per zone, nothing Pending (scenario A). 2 nodes and 3 replicas with HARD one-per-node anti-affinity: 1 pod Pending (C). 3 nodes, 3 replicas, hard anti-affinity, rolling update with one surge pod makes 4 pods: 1 Pending until an old pod terminates (D). That is why I use soft anti-affinity plus topology spread for the day-to-day rule.

**Code:**
```yaml
# ---- spread.yaml ----
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: serving-high
value: 100000
globalDefault: false
preemptionPolicy: PreemptLowerPriority
description: "Online inference. May evict batch pods when the cluster is full."
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: batch-low
value: 1000
globalDefault: false
preemptionPolicy: Never
description: "Batch scoring and training. Never preempts others."
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ranker
spec:
  replicas: 3
  selector:
    matchLabels: {app: ranker}
  template:
    metadata:
      labels: {app: ranker}
    spec:
      priorityClassName: serving-high
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule      # hard: pod stays Pending rather than break the spread
          labelSelector:
            matchLabels: {app: ranker}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:   # soft: try one pod per node
            - weight: 100
              podAffinityTerm:
                topologyKey: kubernetes.io/hostname
                labelSelector:
                  matchLabels: {app: ranker}
      containers:
        - name: server
          image: registry.example.com/ranker:2.0
          resources:
            requests: {cpu: "1", memory: 2Gi}
            limits: {memory: 2Gi}
```

```python
# ---- spread_check.py ----
"""Can N replicas be placed given a node->zone map? Simplified scheduler model:
 - topology spread over zones (maxSkew, DoNotSchedule): after placing, count(zone) - min(count over all zones) <= maxSkew
 - optional HARD pod anti-affinity per node: at most one pod per node
 - each node has a slot limit (max pods of this app). Pods are placed one by one."""
def place(nodes, replicas, max_skew=1, hard_anti_affinity=False, slots=2):
    zones = sorted(set(nodes.values()))
    per_node = {n: 0 for n in nodes}
    per_zone = {z: 0 for z in zones}
    placed, pending = [], 0
    for i in range(replicas):
        ok = []
        for n, z in nodes.items():
            if hard_anti_affinity and per_node[n] >= 1: continue
            if per_node[n] >= slots: continue
            new = dict(per_zone); new[z] += 1
            if new[z] - min(new.values()) > max_skew: continue
            ok.append((per_zone[z], per_node[n], n))
        if not ok:
            pending += 1; continue
        _, _, n = min(ok)                       # prefer emptier zone, then emptier node
        per_node[n] += 1; per_zone[nodes[n]] += 1; placed.append(n)
    return placed, per_zone, pending

def show(title, nodes, replicas, **kw):
    placed, per_zone, pending = place(nodes, replicas, **kw)
    print(f"{title}\n  placed on {placed}\n  per zone {per_zone}  Pending pods: {pending}")

three_zones = {"n1": "a", "n2": "b", "n3": "c"}
show("A) 3 nodes in 3 zones, 3 replicas, skew 1", three_zones, 3)
show("B) 3 replicas, 2 nodes in same zone a, one node in b (zone c has NO nodes)", {"n1": "a", "n2": "a", "n3": "b"}, 3)
show("C) 3 replicas, HARD anti-affinity, only 2 nodes", {"n1": "a", "n2": "b"}, 3, hard_anti_affinity=True)
show("D) rolling update: 4 pods (3 + 1 surge), HARD anti-affinity, 3 nodes", three_zones, 4, hard_anti_affinity=True)
show("E) 4 replicas, 3 nodes in zone a, 1 node in zone b, 1 slot per node, skew 1, DoNotSchedule", {"n1": "a", "n2": "a", "n3": "a", "n4": "b"}, 4, slots=1)
```

**Output (my run):**
**Not executed:** scheduling, preemption and anything on a cluster. What ran: a pure-Python placement model (my simplification: one pod at a time, skew check, optional one-pod-per-node rule, per-node slot limit; the real scheduler also scores nodes and handles many more cases) and `kubernetes-validate --strict` on the manifests.

```text
$ python3 -I spread_check.py
A) 3 nodes in 3 zones, 3 replicas, skew 1
  placed on ['n1', 'n2', 'n3']
  per zone {'a': 1, 'b': 1, 'c': 1}  Pending pods: 0
B) 3 replicas, 2 nodes in same zone a, one node in b (zone c has NO nodes)
  placed on ['n1', 'n3', 'n2']
  per zone {'a': 2, 'b': 1}  Pending pods: 0
C) 3 replicas, HARD anti-affinity, only 2 nodes
  placed on ['n1', 'n2']
  per zone {'a': 1, 'b': 1}  Pending pods: 1
D) rolling update: 4 pods (3 + 1 surge), HARD anti-affinity, 3 nodes
  placed on ['n1', 'n2', 'n3']
  per zone {'a': 1, 'b': 1, 'c': 1}  Pending pods: 1
E) 4 replicas, 3 nodes in zone a, 1 node in zone b, 1 slot per node, skew 1, DoNotSchedule
  placed on ['n1', 'n4', 'n2']
  per zone {'a': 2, 'b': 1}  Pending pods: 1

$ kubernetes-validate --strict spread.yaml; echo "exit code: $?"
INFO spread.yaml passed for resource priorityclass/serving-high against version 1.37
INFO spread.yaml passed for resource priorityclass/batch-low against version 1.37
INFO spread.yaml passed for resource deployment/ranker against version 1.37
exit code: 0
```

**Follow-ups:**
- **Spread or anti-affinity?** Topology spread is the modern, more flexible tool; anti-affinity is simple "not with my own kind".
- **What if I have fewer nodes than replicas?** Use `ScheduleAnyway` or preferred rules, or add nodes.
- **Can preemption bite me?** Yes. Pods of lower priority get SIGTERM and rescheduled; make batch resumable.

**Common mistakes:**
- Hard anti-affinity per node with `replicas` above the node count.
- Forgetting that a zone with no nodes is ignored, so the spread can look fine and still sit in two zones.
- A PriorityClass with `globalDefault: true` on a high value, so everything outranks everything.
- Label selectors in the constraint that do not match the pod's own labels (spread does nothing).

### Q26 ⭐⭐ 🟡 Kubernetes networking basics an ML engineer is asked: pod IPs and the flat network, how Service ClusterIP and kube-proxy route to endpoints, DNS names of the form service.namespace.svc.cluster.local, headless Services, and NetworkPolicy to stop other namespaces reaching the model API. Give a default-deny NetworkPolicy plus an allow rule from the gateway namespace, say what a CNI must support for policies to take effect, and write a script that evaluates a simplified policy list against sample traffic. No cluster, so policy enforcement is not executed.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Every pod gets its own IP on a flat network, a Service gives a stable virtual IP and DNS name that kube-proxy turns into a pod IP, and NetworkPolicy is how I stop other namespaces from reaching the model API, if the CNI enforces it.

**Then explain:**
- **Flat network.** Each pod has an IP and can reach any other pod IP without NAT. The CNI plugin builds that. Pod IPs change when pods restart, so you never hard-code them.
- **Service.** A ClusterIP is a virtual IP. kube-proxy (iptables, IPVS, or an eBPF replacement in some CNIs) turns it into one of the Ready pod IPs listed in EndpointSlices. Only Ready pods are listed.
- **DNS.** CoreDNS names a Service `model-api.ml-serving.svc.cluster.local`. In the same namespace `model-api` is enough; across namespaces use `model-api.ml-serving`. A **headless** Service (`clusterIP: None`) returns the pod IPs directly; StatefulSets use it for per-pod names.
- **NetworkPolicy.** Allow-lists only. Once any policy selects a pod for Ingress, that pod accepts only what some policy allows. Default-deny is `podSelector: {}` with no rules. Then add an allow rule for the gateway.
- **CNI support.** Policies are enforced by the CNI. Some CNIs (Calico, Cilium and others) enforce them; a basic one may accept the YAML and silently do nothing. Check your CNI.
- **Failure modes:** `namespaceSelector` and `podSelector` in the **same** `from` item are AND; as two separate items they are OR (a classic leak); default-deny **egress** also blocks DNS unless you allow port 53 to kube-system; the gateway namespace needs the `kubernetes.io/metadata.name` label (set automatically on current versions); probes and node traffic handling differs by CNI.

**Example:** Policies: default-deny plus "allow envoy pods from namespace `gateway` to port 8080". Results from the script: envoy to 8080 is allowed; envoy to 9000 is denied (port); a notebook in `research` is denied (namespace); a non-envoy pod in `gateway` is denied (pod label). A namespace with no policy stays fully open, which is why default-deny is applied per namespace.

**Code:**
```yaml
# ---- netpol.yaml ----
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: ml-serving
spec:
  podSelector: {}              # every pod in the namespace
  policyTypes: ["Ingress"]     # no ingress rules listed = nothing allowed in
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-gateway-to-model-api
  namespace: ml-serving
spec:
  podSelector:
    matchLabels: {app: model-api}
  policyTypes: ["Ingress"]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: gateway
          podSelector:                     # same list item = AND: gateway namespace AND these pods
            matchLabels: {app: envoy}
      ports:
        - protocol: TCP
          port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: model-api
  namespace: ml-serving
spec:
  selector: {app: model-api}
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: model-api-headless
  namespace: ml-serving
spec:
  clusterIP: None              # headless: DNS returns pod IPs, no virtual IP
  selector: {app: model-api}
  ports:
    - port: 8080
```

```python
# ---- policy_eval.py ----
"""Simplified NetworkPolicy evaluator for INGRESS. Model: a pod is 'isolated' if any policy selects it;
isolated pods accept only traffic allowed by the union of rules of the policies that select them.
Ignores egress, ipBlock, named ports, endPort. A teaching model, not a CNI."""
import yaml

docs = [d for d in yaml.safe_load_all(open("netpol.yaml")) if d["kind"] == "NetworkPolicy"]
ns_labels = {"gateway": {"kubernetes.io/metadata.name": "gateway"},
             "ml-serving": {"kubernetes.io/metadata.name": "ml-serving"},
             "research": {"kubernetes.io/metadata.name": "research"}}

def match(sel, labels):
    return all(labels.get(k) == v for k, v in (sel or {}).get("matchLabels", {}).items())

def allowed(src, dst, port, policies):
    selecting = [p for p in policies if p["metadata"]["namespace"] == dst["ns"]
                 and match(p["spec"]["podSelector"], dst["labels"])
                 and "Ingress" in p["spec"].get("policyTypes", [])]
    if not selecting:
        return True, "no policy selects the destination: open"
    for p in selecting:
        for rule in p["spec"].get("ingress", []):
            ports_ok = not rule.get("ports") or any(r["port"] == port for r in rule["ports"])
            for peer in rule.get("from", []):
                ns_ok = "namespaceSelector" not in peer or match(peer["namespaceSelector"], ns_labels[src["ns"]])
                pod_ok = "podSelector" not in peer or match(peer["podSelector"], src["labels"])
                if "podSelector" in peer and "namespaceSelector" not in peer and src["ns"] != dst["ns"]:
                    pod_ok = False                      # bare podSelector means same namespace only
                if ns_ok and pod_ok and ports_ok:
                    return True, f"allowed by {p['metadata']['name']}"
    return False, "isolated and no rule matches: dropped"

dst = {"ns": "ml-serving", "labels": {"app": "model-api"}}
tests = [
  ("envoy in gateway -> model-api:8080", {"ns": "gateway", "labels": {"app": "envoy"}}, dst, 8080),
  ("envoy in gateway -> model-api:9000", {"ns": "gateway", "labels": {"app": "envoy"}}, dst, 9000),
  ("notebook in research -> model-api:8080", {"ns": "research", "labels": {"app": "notebook"}}, dst, 8080),
  ("other pod in gateway -> model-api:8080", {"ns": "gateway", "labels": {"app": "debug"}}, dst, 8080),
  ("anyone -> pod in a namespace with no policy", {"ns": "research", "labels": {}}, {"ns": "research", "labels": {"app": "x"}}, 80),
]
for name, s, d, port in tests:
    ok, why = allowed(s, d, port, docs)
    print(f"{'ALLOW' if ok else 'DENY ':5} {name:45} ({why})")
```

**Output (my run):**
**Not executed:** real enforcement (needs a cluster and a CNI that supports NetworkPolicy), DNS and kube-proxy. What ran: my simplified ingress-only evaluator (ignores egress, ipBlock, named ports) and `kubernetes-validate --strict` on all four objects.

```text
$ python3 -I policy_eval.py
ALLOW envoy in gateway -> model-api:8080            (allowed by allow-gateway-to-model-api)
DENY  envoy in gateway -> model-api:9000            (isolated and no rule matches: dropped)
DENY  notebook in research -> model-api:8080        (isolated and no rule matches: dropped)
DENY  other pod in gateway -> model-api:8080        (isolated and no rule matches: dropped)
ALLOW anyone -> pod in a namespace with no policy   (no policy selects the destination: open)

$ kubernetes-validate --strict netpol.yaml; echo "exit code: $?"
INFO netpol.yaml passed for resource networkpolicy/default-deny-ingress against version 1.37
INFO netpol.yaml passed for resource networkpolicy/allow-gateway-to-model-api against version 1.37
INFO netpol.yaml passed for resource service/model-api against version 1.37
INFO netpol.yaml passed for resource service/model-api-headless against version 1.37
exit code: 0
```

**Follow-ups:**
- **Why can't pod A reach pod B after default-deny?** No allow rule matches; add one for the right source and port.
- **ClusterIP versus headless?** ClusterIP load-balances behind one virtual IP; headless exposes each pod IP in DNS.
- **How do I test a policy?** From a debug pod in the source namespace run curl and check the result; on a real cluster only (not executed here).

**Common mistakes:**
- Assuming NetworkPolicy works on any cluster.
- Mixing up AND and OR in `from` lists.
- Applying default-deny egress and then wondering why DNS lookups fail.
- Expecting a policy in one namespace to protect other namespaces.

### Q27 ⭐⭐ 🟡 Debugging a Service that returns nothing: pods are Running but the endpoint times out. Give the ordered checks: label selector matches pod labels, kubectl get endpoints is empty because pods are not Ready, targetPort versus containerPort versus the port the app binds, app listening on 127.0.0.1 instead of 0.0.0.0, readiness probe failing, NetworkPolicy, Ingress path rewrite and wrong backend port. Provide a script that cross-checks a Service selector and ports against a Deployment manifest and reports the mismatch, with a deliberately broken sample. kubectl is not executed.
**Asked at:** Kubernetes troubleshooting write-ups (techinterview.org 'What Kubernetes interviewers actually ask once you are past pods', OneUptime CrashLoopBackOff and OOMKilled guide 2026, vervecopilot, devopsboys; search snippets only, not opened); scenario-style 'here is what kubectl get pods prints, what next' rounds; editorial, not verified candidate reports; DevOps, SRE and MLOps loops
**Say this first (1 line):** I walk the path from the outside in: do the pods match the Service selector, are they Ready so endpoints are not empty, do the ports line up, is the app bound to 0.0.0.0, then NetworkPolicy and Ingress, and I bypass the Service with a port-forward to split the problem.

**Then explain:**
- **1. Labels.** `kubectl get pods --show-labels` against `svc.spec.selector`. A typo (`modelapi` vs `model-api`) gives empty endpoints and no error.
- **2. Endpoints.** Empty EndpointSlices means no **Ready** pod matches. Running is not Ready: the readiness probe decides.
- **3. Ports.** Service `port` is what clients call; `targetPort` must be the port the app listens on; `containerPort` is documentation but good to keep equal. A readiness probe on the wrong port keeps pods NotReady forever.
- **4. Bind address.** An app on `127.0.0.1` answers inside the pod (so `exec curl localhost` works) and nothing from outside. Bind `0.0.0.0`.
- **5. Split the problem.** `port-forward` to the pod works but the Service does not: Service or policy problem. Pod answers on port-forward but not from another pod: bind address or NetworkPolicy.
- **6. Then Ingress and policy.** Ingress path rewrite (the app sees `/v1/predict` but gets `/`), wrong backend port, TLS. NetworkPolicy default-deny with no allow.
- **Failure modes:** looking at logs first when the app is fine; trusting "Running"; forgetting that a rolling update can leave old and new labels mixed.

**Example:** The broken sample has four bugs at once: Service selects `app=model-api` but pods are `app=modelapi`; `targetPort` 8000 but the app listens on 8080; readiness probe on 9090; app started with `--host 127.0.0.1`. The script reports all four. The fixed file reports none.

**Code:**
```yaml
# ---- broken.yaml ----
apiVersion: v1
kind: Service
metadata:
  name: model-api
spec:
  selector: {app: model-api}          # BUG 1: pods are labelled app=modelapi
  ports:
    - port: 80
      targetPort: 8000                # BUG 2: container listens on 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-api
spec:
  replicas: 2
  selector:
    matchLabels: {app: modelapi}
  template:
    metadata:
      labels: {app: modelapi}
    spec:
      containers:
        - name: server
          image: registry.example.com/model-api:1.4.2
          args: ["serve", "--host", "127.0.0.1", "--port", "8080"]   # BUG 3: loopback only
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet: {path: /ready, port: 9090}                      # BUG 4: nothing listens on 9090
```

```python
# ---- svc_check.py ----
"""Cross-check a Service against the Deployment(s) in the same file. Static checks only."""
import sys, yaml

def check(path):
    docs = list(yaml.safe_load_all(open(path)))
    svcs = [d for d in docs if d["kind"] == "Service"]
    deps = [d for d in docs if d["kind"] == "Deployment"]
    problems = []
    for s in svcs:
        sel = s["spec"].get("selector", {})
        matches = [d for d in deps if all(d["spec"]["template"]["metadata"]["labels"].get(k) == v for k, v in sel.items())]
        if not matches:
            problems.append(f"Service {s['metadata']['name']}: selector {sel} matches no pod template -> endpoints will be empty")
            matches = [d for d in deps if d["metadata"]["name"] == s["metadata"]["name"]]   # keep checking the same-named Deployment
        for d in matches:
            c = d["spec"]["template"]["spec"]["containers"][0]
            cports = {p["containerPort"] for p in c.get("ports", [])}
            for sp in s["spec"]["ports"]:
                tp = sp.get("targetPort", sp["port"])
                if tp not in cports:
                    problems.append(f"Service port {sp['port']} -> targetPort {tp}, but container declares {sorted(cports)}")
            rp = c.get("readinessProbe", {}).get("httpGet", {}).get("port")
            if rp is not None and rp not in cports:
                problems.append(f"readinessProbe port {rp} is not a declared containerPort {sorted(cports)}: pods may never become Ready")
            args = c.get("args", []) + c.get("command", [])
            for i, a in enumerate(args):
                if a in ("127.0.0.1", "localhost") or (a.startswith("--host=") and a.split("=")[1] in ("127.0.0.1", "localhost")):
                    problems.append(f"app binds {a}: only reachable inside the pod, use 0.0.0.0")
    # selector vs Deployment's own matchLabels must match template labels
    for d in deps:
        ml = d["spec"]["selector"]["matchLabels"]; tl = d["spec"]["template"]["metadata"]["labels"]
        if any(tl.get(k) != v for k, v in ml.items()):
            problems.append(f"Deployment {d['metadata']['name']}: selector.matchLabels does not match template labels")
    return problems

for f in sys.argv[1:]:
    probs = check(f)
    print(f"== {f}: {len(probs)} problem(s)")
    for p in probs: print("  -", p)
```

```bash
# ---- debug.sh ----
#!/usr/bin/env bash
# Ordered checks for "Service returns nothing". NOT executed here (no kubectl, no cluster).
NS=ml-serving; SVC=model-api
kubectl -n $NS get pods -l app=$SVC -o wide --show-labels      # 1 are pods Ready (1/1)? do labels match?
kubectl -n $NS get svc $SVC -o jsonpath='{.spec.selector}{"\n"}{.spec.ports}{"\n"}'   # 2 selector + ports
kubectl -n $NS get endpointslices -l kubernetes.io/service-name=$SVC   # 3 empty = no Ready pod matches
kubectl -n $NS describe pod -l app=$SVC | grep -A5 -i readiness      # 4 probe path/port, failures
kubectl -n $NS exec deploy/$SVC -- sh -c 'ss -ltn || netstat -ltn'  # 5 which address:port is bound
kubectl -n $NS port-forward deploy/$SVC 8080:8080                  # 6 bypass Service: does the app answer?
kubectl -n $NS run dbg --rm -it --image=curlimages/curl --restart=Never -- curl -sv http://$SVC.$NS.svc.cluster.local/healthz   # 7 via Service DNS
kubectl -n $NS get networkpolicy                                   # 8 anything isolating the pod?
kubectl -n $NS get ingress -o yaml                                 # 9 backend service name, port, path rewrite
```

**Output (my run):**
**Not executed:** every `kubectl` command in `debug.sh` (no kubectl, no cluster). What ran: the static cross-check script on `broken.yaml` and `fixed.yaml` (`fixed.yaml` is the same file with the four bugs corrected; it is not pasted), `kubernetes-validate --strict` (note both files pass: the schema cannot see these logic bugs, which is exactly why the cross-check exists), and `bash -n` on the script. Static checks catch config mismatches only; they cannot see a bad bind address set inside the image or a policy on the cluster.

```text
$ python3 -I svc_check.py broken.yaml fixed.yaml
== broken.yaml: 4 problem(s)
  - Service model-api: selector {'app': 'model-api'} matches no pod template -> endpoints will be empty
  - Service port 80 -> targetPort 8000, but container declares [8080]
  - readinessProbe port 9090 is not a declared containerPort [8080]: pods may never become Ready
  - app binds 127.0.0.1: only reachable inside the pod, use 0.0.0.0
== fixed.yaml: 0 problem(s)

$ kubernetes-validate --strict broken.yaml; echo "exit code: $?"
INFO broken.yaml passed for resource service/model-api against version 1.37
INFO broken.yaml passed for resource deployment/model-api against version 1.37
exit code: 0

$ bash -n debug.sh && echo "bash -n: syntax ok"
bash -n: syntax ok

$ command -v kubectl || echo "kubectl: not installed"
kubectl: not installed
```

**Follow-ups:**
- **Endpoints empty but pods Running?** Selector mismatch or readiness failing.
- **Works with port-forward, fails via Service?** Service ports, selector or NetworkPolicy.
- **Works from inside the cluster, fails via Ingress?** Ingress backend, path rewrite, host or TLS.

**Common mistakes:**
- Reading logs for 30 minutes before comparing labels.
- Confusing `port`, `targetPort` and `containerPort`.
- Binding the dev server to `localhost` (the default in many frameworks).
- Debugging through the Ingress when the Service itself is broken.

### Q28 ⭐⭐ 🟡 Sharing a big model across many pods: init containers, sidecars, emptyDir and image volumes. Compare baking weights into the image, an init container that downloads from object storage into an emptyDir, a node-local cache via hostPath or a DaemonSet pre-puller, a ReadOnlyMany or ReadWriteMany PVC, and streaming weights directly at start; cover startup time, node disk pressure, image pull time, and consistency of versions across replicas. Give an init-container manifest and a script that estimates cold-start time for each option from assumed sizes and bandwidths (state the assumptions as made-up numbers). Not executed on a cluster.
**Asked at:** Probe and model-loading write-ups (llm-d readiness probes docs, OneUptime startup probes article, DZone 'Kubernetes LLM readiness' experiment, AWS containers blog on fast model loading on EKS; search snippets only, not opened); docs and blogs, not interview reports; ML serving and platform roles
**Say this first (1 line):** For a big model I trade start time, node disk and version consistency: baking into the image is simple, an init container to an emptyDir is flexible, a node cache or a shared read-only volume is faster on repeat starts, and I always pin an immutable version.

**Then explain:**
- **Bake into image.** One artefact, versions match the code. But the image is huge, slow to pull on a cold node, and every model change is a new image.
- **Init container + emptyDir.** Small image; an init container fetches from object storage, verifies a checksum, and the server reads the shared `emptyDir`. Every pod re-downloads on start. `emptyDir` uses node ephemeral storage, so set `sizeLimit` and an `ephemeral-storage` request or the node hits disk pressure and evicts pods.
- **Node-local cache.** A DaemonSet pre-pulls into a `hostPath` so later pods on that node start fast. Costs: hostPath is a security and cleanup problem, cache invalidation is yours.
- **Shared volume.** ReadOnlyMany or ReadWriteMany PVC (needs a storage class that supports it; check your cloud). No per-pod download, but all pods hit one storage backend, and its throughput is shared.
- **Stream weights.** Some servers can load straight from object storage during start-up, overlapping download and load. Less disk, but start time depends on the network.
- **Newer option.** Recent Kubernetes versions added an image volume source to mount an OCI artifact as a read-only volume; it was feature-gated at first. Check current docs before relying on it.
- **Failure modes:** `latest` in the model URI so replicas created at different times load different models; startup probe too short, so the pod is killed mid-load; many pods starting at once overload the object store (thundering herd).

**Example:** Made-up numbers: 20 GB model, 4 replicas on 4 nodes, shared source cap 2 GB/s. Cold image pull of 22 GB at (0.5 GB/s each) gives 44 s, plus 20 s load: 64 s. Init container: 4 s image + 40 s download + 20 s load: 64 s. Node cache hit: 4 + 10 + 20 = 34 s. Baked image already cached on the node: just the 20 s load. The point is the ranking and what dominates, not the seconds.

**Code:**
```yaml
# ---- init_model.yaml ----
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-server
spec:
  replicas: 4
  selector:
    matchLabels: {app: llm-server}
  template:
    metadata:
      labels: {app: llm-server}
    spec:
      volumes:
        - name: model
          emptyDir:
            sizeLimit: 40Gi              # counts toward node ephemeral storage; pod is evicted if exceeded
      initContainers:
        - name: fetch-model
          image: registry.example.com/model-fetcher:1.0   # small image with an object-store CLI
          command: ["sh", "-c"]
          args:
            - >-
              fetch --src "$MODEL_URI" --dst /models/current &&
              sha256sum -c /models/current/SHA256SUMS
          env:
            - name: MODEL_URI
              value: s3://models-prod/llm/2026-10-01/   # pin an immutable version, never "latest"
          volumeMounts:
            - {name: model, mountPath: /models}
          resources:
            requests: {cpu: "1", memory: 1Gi, ephemeral-storage: 40Gi}
      containers:
        - name: server
          image: registry.example.com/llm-server:3.2
          volumeMounts:
            - {name: model, mountPath: /models, readOnly: true}
          startupProbe:
            httpGet: {path: /ready, port: 8080}
            periodSeconds: 10
            failureThreshold: 60         # up to 10 min to load weights before kubelet gives up
          readinessProbe:
            httpGet: {path: /ready, port: 8080}
```

```python
# ---- cold_start.py ----
"""Cold-start estimate per option. ALL NUMBERS ARE MADE-UP ASSUMPTIONS, not measurements."""
MODEL_GB = 20            # weights
IMAGE_GB_CODE = 2        # image without weights
NET_GBPS = 1.0           # GB/s from object store to node (assumed)
REGISTRY_GBPS = 0.5      # GB/s image pull (assumed)
DISK_GBPS = 2.0          # GB/s local disk read into GPU memory path (assumed)
PVC_GBPS = 0.8           # GB/s from shared network volume (assumed)
LOAD_S = 20              # seconds for the server to init the model once bytes are local (assumed)
REPLICAS = 4
NODES = 4                # one replica per node
SHARED_STORE_LIMIT_GBPS = 2.0   # object store / PVC aggregate cap (assumed)

def share(per_pod_gbps, pods):   # many pods hitting one source split its aggregate cap
    return min(per_pod_gbps, SHARED_STORE_LIMIT_GBPS / pods)

options = {
 "A baked into image (cold node)":       (MODEL_GB + IMAGE_GB_CODE) / share(REGISTRY_GBPS, NODES) + LOAD_S,
 "A baked into image (image cached)":    LOAD_S,
 "B init container -> emptyDir":         IMAGE_GB_CODE / REGISTRY_GBPS + MODEL_GB / share(NET_GBPS, REPLICAS) + LOAD_S,
 "C node cache (DaemonSet pre-pull), hit": IMAGE_GB_CODE / REGISTRY_GBPS + MODEL_GB / DISK_GBPS + LOAD_S,
 "D RWX/ROX PVC mounted":                IMAGE_GB_CODE / REGISTRY_GBPS + MODEL_GB / share(PVC_GBPS, REPLICAS) + LOAD_S,
 "E stream weights at start":            IMAGE_GB_CODE / REGISTRY_GBPS + max(MODEL_GB / share(NET_GBPS, REPLICAS), LOAD_S),
}
print(f"assumptions: model {MODEL_GB} GB, {REPLICAS} replicas on {NODES} nodes, shared source cap {SHARED_STORE_LIMIT_GBPS} GB/s")
for k, v in options.items():
    print(f"{k:42} ~{v:6.0f} s")
disk_extra = {"A baked into image (cold node)": MODEL_GB, "B init container -> emptyDir": MODEL_GB,
              "C node cache (DaemonSet pre-pull), hit": MODEL_GB, "D RWX/ROX PVC mounted": 0, "E stream weights at start": 0}
print("\nextra node disk per node (GB):", disk_extra)
```

**Output (my run):**
**Not executed:** the pods, the download and any real timings. All sizes and bandwidths in `cold_start.py` are made-up assumptions, so the seconds are arithmetic, not measurements. What ran: the estimator and `kubernetes-validate --strict` on the Deployment.

```text
$ python3 -I cold_start.py
assumptions: model 20 GB, 4 replicas on 4 nodes, shared source cap 2.0 GB/s
A baked into image (cold node)             ~    64 s
A baked into image (image cached)          ~    20 s
B init container -> emptyDir               ~    64 s
C node cache (DaemonSet pre-pull), hit     ~    34 s
D RWX/ROX PVC mounted                      ~    64 s
E stream weights at start                  ~    44 s

extra node disk per node (GB): {'A baked into image (cold node)': 20, 'B init container -> emptyDir': 20, 'C node cache (DaemonSet pre-pull), hit': 20, 'D RWX/ROX PVC mounted': 0, 'E stream weights at start': 0}

$ kubernetes-validate --strict init_model.yaml; echo "exit code: $?"
INFO init_model.yaml passed for resource deployment/llm-server against version 1.37
exit code: 0
```

**Follow-ups:**
- **Which is best?** There is none. Image for small models; shared volume or cache for many replicas; init container as a simple default.
- **How do I keep replicas on the same version?** Pin an immutable path or digest in the manifest; roll out through the Deployment.
- **What about autoscaling?** New replicas pay the cold-start cost, so slow start means slow scale-up; keep a warm minimum.

**Common mistakes:**
- No `sizeLimit` or ephemeral-storage request on the emptyDir.
- No checksum check after the download.
- `latest` as the model version.
- Startup probe budget shorter than the real load time.

### Q29 ⭐⭐ 🔴 KServe at concept level for an interviewer. Explain the InferenceService resource (predictor, optional transformer and explainer), why it sits on Knative or raw deployment mode, model storage via storageUri, scale-to-zero and concurrency-based autoscaling, canaryTrafficPercent for gradual rollout and rollback, and what KServe gives you over a hand-written Deployment plus Service plus HPA (and what it costs: Knative and Istio complexity, hedge by version). Show an InferenceService manifest for a sklearn or Triton model and a script that validates its required fields and computes the traffic split. KServe is not installed; nothing is executed. Check current docs for the schema.
**Asked at:** KServe and Kubeflow references (OneUptime canary model rollouts with KServe, Canonical 'what is KFServing', Arena docs for KServe, KServe v0.5.0 release notes, AMD AIM Engine autoscaling docs, Kubeflow Training Operator job-scheduling docs, Cast.ai Kueue article; search snippets only, not opened); docs and vendor blogs, not interview reports; MLOps roles on Kubeflow or KServe stacks
**Say this first (1 line):** KServe turns "serve this model" into one InferenceService resource: it creates the serving pods, pulls the model from storageUri, wires autoscaling and canary traffic, so you do not hand-write the Deployment, Service and HPA, at the price of extra moving parts.

**Then explain:**
- **InferenceService.** Has a **predictor** (the model server), and optionally a **transformer** (pre and post processing) and **explainer**. The predictor names a `modelFormat` (sklearn, a Triton model, and so on) and a `storageUri`. A runtime is chosen for that format, and a storage initializer fetches the model into the pod.
- **Modes.** In Serverless mode it sits on **Knative** (scale-to-zero, concurrency-based autoscaling, revisions) and usually a service mesh or gateway. In raw deployment mode it makes plain Deployments with an HPA: simpler, but no scale-to-zero (HPA cannot go to zero). Which features work in which mode depends on the version; check current docs.
- **Canary.** `canaryTrafficPercent: 10` sends 10% to the newest revision and 90% to the last good one. Raise it step by step, then remove the field to promote. Setting it to 0 sends all traffic to the previous revision, which is how you back off (check current docs for exact behaviour).
- **What you gain over Deployment + Service + HPA:** one resource per model, standard model download, revisions and traffic splitting, scale-to-zero, a common inference protocol, a pluggable runtime list.
- **What it costs:** Knative and often Istio or another gateway to run and upgrade, CRDs, extra debugging layers, version coupling. For one or two models a plain Deployment may be easier.
- **Failure modes:** scale-to-zero plus a slow model load makes the first request slow or time out; `storageUri` pointing at a path without credentials fails in the storage initializer (check the init container logs); canary without a previous good revision has nothing to split to; the field names changed between versions.

**Example:** Rollout of fraud model v4 with `canaryTrafficPercent: 10`: traffic is 10% new, 90% previous. Metrics look fine, move to 50, then remove the field: 100% latest. If errors rise at 10%, set it to 0: all traffic goes back to the previous revision without redeploying the old model (the old revision is still there).

**Code:**
```yaml
# ---- isvc.yaml ----
# KServe InferenceService, v1beta1 schema as commonly shown in KServe docs.
# CHECK CURRENT DOCS: field names and defaults vary by KServe version and deployment mode.
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: fraud-sklearn
  namespace: ml-serving
  annotations:
    serving.kserve.io/deploymentMode: Serverless     # Knative-backed; RawDeployment = plain Deployment + HPA
spec:
  predictor:
    minReplicas: 1                 # 0 allows scale-to-zero in Serverless mode
    maxReplicas: 5
    scaleMetric: concurrency       # Knative-style: in-flight requests per pod
    scaleTarget: 10
    canaryTrafficPercent: 10       # 10% to the newest revision, 90% to the previous good one
    model:
      modelFormat:
        name: sklearn
      storageUri: s3://models-prod/fraud/4/    # new version being rolled out
      resources:
        requests: {cpu: "1", memory: 2Gi}
        limits: {memory: 2Gi}
```

```python
# ---- isvc_check.py ----
"""Validate required InferenceService fields (our own short list, not the real CRD schema)
and compute the canary traffic split. Run on the manifest and on deliberately broken variants."""
import copy, yaml

def get(d, path):
    for p in path.split("."):
        if not isinstance(d, dict) or p not in d: return None
        d = d[p]
    return d

REQUIRED = ["apiVersion", "kind", "metadata.name", "spec.predictor.model.modelFormat.name", "spec.predictor.model.storageUri"]

def check(doc):
    errs = [f"missing {p}" for p in REQUIRED if get(doc, p) is None]
    if doc.get("kind") != "InferenceService": errs.append("kind is not InferenceService")
    pred = get(doc, "spec.predictor") or {}
    c = pred.get("canaryTrafficPercent")
    if c is not None and not (0 <= c <= 100): errs.append(f"canaryTrafficPercent {c} not in 0..100")
    lo = pred.get("minReplicas", 1)
    hi = pred.get("maxReplicas", lo)
    if hi < lo: errs.append(f"maxReplicas {hi} < minReplicas {lo}")
    uri = get(doc, "spec.predictor.model.storageUri") or ""
    if uri and uri.rstrip("/").endswith("latest"): errs.append("storageUri uses 'latest': not reproducible")
    return errs

def split(doc):
    c = get(doc, "spec.predictor.canaryTrafficPercent")
    if c is None: return {"latest revision": 100}
    if not 0 <= c <= 100: return "invalid"
    return {"latest revision (new)": c, "previous rolled-out revision": 100 - c}

good = yaml.safe_load(open("isvc.yaml"))
print("good manifest errors:", check(good) or "none", "| traffic:", split(good))

def variant(name, edit):
    d = copy.deepcopy(good); edit(d); print(f"{name}: {check(d) or 'none'} | traffic: {split(d)}")

variant("no storageUri", lambda d: d["spec"]["predictor"]["model"].pop("storageUri"))
variant("canary 150", lambda d: d["spec"]["predictor"].update(canaryTrafficPercent=150))
variant("canary 0 (new revision gets nothing)", lambda d: d["spec"]["predictor"].update(canaryTrafficPercent=0))
variant("promote: remove canaryTrafficPercent", lambda d: d["spec"]["predictor"].pop("canaryTrafficPercent"))
variant("max < min", lambda d: d["spec"]["predictor"].update(minReplicas=3, maxReplicas=2))
variant("latest model", lambda d: d["spec"]["predictor"]["model"].update(storageUri="s3://m/fraud/latest"))
```

**Output (my run):**
**Not executed:** KServe, Knative and Istio are not installed, so nothing was created and no traffic was split. The manifest follows commonly documented v1beta1 fields; **check current docs for the schema** of your KServe version. What ran: my own required-field checker (a short list I wrote, not the real CRD schema) and the traffic arithmetic. `kubernetes-validate --strict` printed only a **warning**: it has no schema for the InferenceService CRD, so exit code 0 here proves nothing about this manifest.

```text
$ python3 -I isvc_check.py
good manifest errors: none | traffic: {'latest revision (new)': 10, 'previous rolled-out revision': 90}
no storageUri: ['missing spec.predictor.model.storageUri'] | traffic: {'latest revision (new)': 10, 'previous rolled-out revision': 90}
canary 150: ['canaryTrafficPercent 150 not in 0..100'] | traffic: invalid
canary 0 (new revision gets nothing): none | traffic: {'latest revision (new)': 0, 'previous rolled-out revision': 100}
promote: remove canaryTrafficPercent: none | traffic: {'latest revision': 100}
max < min: ['maxReplicas 2 < minReplicas 3'] | traffic: {'latest revision (new)': 10, 'previous rolled-out revision': 90}
latest model: ["storageUri uses 'latest': not reproducible"] | traffic: {'latest revision (new)': 10, 'previous rolled-out revision': 90}

$ kubernetes-validate --strict isvc.yaml; echo "exit code: $?"
WARN isvc.yaml Couldn't find schema for kind InferenceService with api version serving.kserve.io/v1beta1 for kubernetes version 1.37
exit code: 0
```

**Follow-ups:**
- **Why not just a Deployment?** One model, one team: a Deployment is fine. Many models, canaries, scale-to-zero: KServe pays off.
- **Can it scale to zero on GPU?** It can, but the cold start (load weights, GPU init) can take tens of seconds or more, so many keep one warm replica.
- **Where do models come from?** `storageUri` (object store, PVC and others); the init step downloads them.

**Common mistakes:**
- Treating the validator's exit 0 as success for a CRD it has no schema for.
- Copying a manifest from a blog written for another KServe version.
- Scale-to-zero on a latency-critical model with a slow load.
- No pinned model version in `storageUri`.

### Q30 ⭐⭐ 🔴 Distributed training on Kubernetes at concept level: the Kubeflow Training Operator PyTorchJob (master and worker replicas), why all pods must start together (gang scheduling) or the job deadlocks holding GPUs, how Kueue queues jobs against quota, Volcano as an alternative batch scheduler, restart policy and checkpointing for node loss, and the NCCL and shared-memory (/dev/shm) pitfalls. Give a PyTorchJob manifest sketch, a Kueue ClusterQueue and LocalQueue sketch (field names hedged, check current docs) and a script that checks whether a job's total GPU ask fits a queue quota. Nothing is executed here.
**Asked at:** KServe and Kubeflow references (OneUptime canary model rollouts with KServe, Canonical 'what is KFServing', Arena docs for KServe, KServe v0.5.0 release notes, AMD AIM Engine autoscaling docs, Kubeflow Training Operator job-scheduling docs, Cast.ai Kueue article; search snippets only, not opened); docs and vendor blogs, not interview reports; MLOps roles on Kubeflow or KServe stacks
**Say this first (1 line):** Distributed training on Kubernetes needs all pods of a job to start together, so I use a PyTorchJob for the pods, a queue such as Kueue to admit the whole job against quota, checkpointing for restarts, and I watch /dev/shm and NCCL settings.

**Then explain:**
- **PyTorchJob.** A custom resource from the Kubeflow Training Operator: a Master and N Workers. The operator creates the pods and injects the distributed env (master address, world size, rank). A job for 8 GPUs at 2 GPUs per pod is 4 pods.
- **Gang scheduling.** Pods are scheduled one at a time by default. Two big jobs can each grab half the GPUs and both wait forever for the rest: a deadlock holding GPUs. Gang scheduling (all or nothing) avoids it. Options: Kueue (admits a job only when its whole ask fits quota), Volcano, or scheduler plugins.
- **Kueue.** You define a ResourceFlavor, a **ClusterQueue** with quota (for example 8 GPUs), and a namespaced **LocalQueue**. A job labelled with the queue name stays suspended until quota is free. Quota is bookkeeping, not capacity: a job can be admitted and its pods still be Pending if the nodes are missing.
- **Node loss and restarts.** Use a restart policy suited to the job, write checkpoints to a PVC or object storage, and resume with auto-detect on start. Without that, one lost node restarts from step 0.
- **Pitfalls.** `/dev/shm` is tiny by default, so PyTorch dataloader workers crash; mount a memory `emptyDir` there. NCCL needs pods to reach each other, the right network interface and (for fast links) RDMA setup; use `NCCL_DEBUG` to diagnose. Mixed GPU types in one job make the slowest set the speed.
- **Failure modes:** partial start deadlock; quota says yes but no nodes; a worker is evicted by preemption or spot reclaim and the whole job restarts; checkpoints written to local disk vanish with the node.

**Example:** Job: 1 Master + 3 Workers, 2 GPUs each = 8 GPUs. Queue quota 8. Empty queue: admit. 2 GPUs already used: the script says wait, short by 2 (it stays queued rather than starting 3 pods and blocking). Gang demo: 4 free GPUs, two jobs each needing 4. Without gang, each gets one pod and both wait forever (deadlock). With gang, job A runs and B waits.

**Code:**
```yaml
# ---- train.yaml ----
# SKETCHES. Kubeflow Training Operator and Kueue are CRDs; field names change by version. Check current docs.
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: a100-nodes
spec:
  nodeLabels:
    gpu-type: a100
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: team-ml
spec:
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
      flavors:
        - name: a100-nodes
          resources:
            - {name: cpu, nominalQuota: "64"}
            - {name: memory, nominalQuota: 512Gi}
            - {name: nvidia.com/gpu, nominalQuota: "8"}
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: team-ml-queue
  namespace: ml-train
spec:
  clusterQueue: team-ml
---
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: bert-finetune
  namespace: ml-train
  labels:
    kueue.x-k8s.io/queue-name: team-ml-queue      # Kueue holds the job until the whole ask fits quota
spec:
  runPolicy:
    backoffLimit: 3
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: registry.example.com/trainer:5.1
              args: ["--ckpt-dir=/ckpt", "--resume=auto"]      # restart resumes from the last checkpoint
              env:
                - {name: NCCL_DEBUG, value: WARN}
              resources:
                requests: {cpu: "8", memory: 64Gi}
                limits: {nvidia.com/gpu: 2}
              volumeMounts:
                - {name: shm, mountPath: /dev/shm}             # default /dev/shm is tiny; dataloaders crash
                - {name: ckpt, mountPath: /ckpt}
          volumes:
            - name: shm
              emptyDir: {medium: Memory, sizeLimit: 16Gi}
            - name: ckpt
              persistentVolumeClaim: {claimName: bert-ckpt}
    Worker:
      replicas: 3
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: registry.example.com/trainer:5.1
              args: ["--ckpt-dir=/ckpt", "--resume=auto"]
              resources:
                requests: {cpu: "8", memory: 64Gi}
                limits: {nvidia.com/gpu: 2}
              volumeMounts:
                - {name: shm, mountPath: /dev/shm}
                - {name: ckpt, mountPath: /ckpt}
          volumes:
            - name: shm
              emptyDir: {medium: Memory, sizeLimit: 16Gi}
            - name: ckpt
              persistentVolumeClaim: {claimName: bert-ckpt}
```

```python
# ---- quota_fit.py ----
"""(1) Does a PyTorchJob's total GPU ask fit a ClusterQueue quota? (2) Why gang scheduling matters."""
import yaml

docs = {d["kind"]: d for d in yaml.safe_load_all(open("train.yaml"))}

def job_gpu_ask(job):
    total = 0
    for name, spec in job["spec"]["pytorchReplicaSpecs"].items():
        per_pod = int(spec["template"]["spec"]["containers"][0]["resources"]["limits"].get("nvidia.com/gpu", 0))
        total += spec["replicas"] * per_pod
        print(f"  {name}: {spec['replicas']} pod(s) x {per_pod} GPU")
    return total

def quota(cq, resource="nvidia.com/gpu"):
    for g in cq["spec"]["resourceGroups"]:
        for f in g["flavors"]:
            for r in f["resources"]:
                if r["name"] == resource: return int(r["nominalQuota"])

ask = job_gpu_ask(docs["PyTorchJob"])
q = quota(docs["ClusterQueue"])
for used in (0, 2, 4):
    free = q - used
    print(f"queue quota {q}, already used {used}, job asks {ask}: " + ("ADMIT" if ask <= free else f"WAIT in queue (short by {ask - free})"))

print("\n--- gang vs no gang: 4 free GPUs, two jobs each need 4 (2 pods x 2 GPUs). Each pod takes 2.")
def run(gang):
    free, jobs = 4, {"A": 2, "B": 2}            # pods still needed per job
    held = {"A": 0, "B": 0}
    if gang:
        for j in jobs:                          # admit a job only if ALL its pods fit
            if jobs[j] * 2 <= free:
                free -= jobs[j] * 2; held[j] = jobs[j]; jobs[j] = 0
    else:
        while free >= 2 and any(jobs.values()):
            for j in jobs:                      # pods trickle in one at a time, alternating
                if jobs[j] and free >= 2:
                    free -= 2; held[j] += 1; jobs[j] -= 1
    running = [j for j in held if held[j] == 2]
    stuck = [j for j in held if 0 < held[j] < 2]
    print(f"gang={gang}: held pods {held}, free GPUs {free}, running {running or 'none'}, stuck-holding {stuck or 'none'}")
run(False); run(True)
```

**Output (my run):**
**Not executed:** Kubeflow Training Operator, Kueue, Volcano, GPUs, NCCL and any training. The YAML is a **sketch**: CRD field names and API versions change between releases; check current docs. What ran: the quota-fit script and a toy gang-versus-no-gang model (my simplification). `kubernetes-validate --strict` only printed warnings: it has no schemas for these CRDs, so exit code 0 proves nothing about them.

```text
$ python3 -I quota_fit.py
  Master: 1 pod(s) x 2 GPU
  Worker: 3 pod(s) x 2 GPU
queue quota 8, already used 0, job asks 8: ADMIT
queue quota 8, already used 2, job asks 8: WAIT in queue (short by 2)
queue quota 8, already used 4, job asks 8: WAIT in queue (short by 4)

--- gang vs no gang: 4 free GPUs, two jobs each need 4 (2 pods x 2 GPUs). Each pod takes 2.
gang=False: held pods {'A': 1, 'B': 1}, free GPUs 0, running none, stuck-holding ['A', 'B']
gang=True: held pods {'A': 2, 'B': 0}, free GPUs 0, running ['A'], stuck-holding none

$ kubernetes-validate --strict train.yaml; echo "exit code: $?"
WARN train.yaml Couldn't find schema for kind ResourceFlavor with api version kueue.x-k8s.io/v1beta1 for kubernetes version 1.37
WARN train.yaml Couldn't find schema for kind ClusterQueue with api version kueue.x-k8s.io/v1beta1 for kubernetes version 1.37
WARN train.yaml Couldn't find schema for kind LocalQueue with api version kueue.x-k8s.io/v1beta1 for kubernetes version 1.37
WARN train.yaml Couldn't find schema for kind PyTorchJob with api version kubeflow.org/v1 for kubernetes version 1.37
exit code: 0
```

**Follow-ups:**
- **Why not plain Jobs?** Plain Jobs have no gang start and no rank setup; the operator handles both for PyTorch.
- **Kueue or Volcano?** Both queue and gang-schedule. Kueue works with the default scheduler; Volcano brings its own. Pick by what your platform already runs.
- **Spot nodes?** Fine if you checkpoint often and accept restarts.

**Common mistakes:**
- Default `/dev/shm` size.
- Checkpoints on local disk.
- Assuming queue quota guarantees free nodes.
- Treating a validator warning on CRDs as a pass.

### Q31 ⭐⭐ 🟡 Kubeflow at concept level: what the pieces are (Pipelines, Notebooks, Training Operator, Katib for hyperparameter search, KServe), how they differ from using plain Jobs plus Argo or Airflow, the cost of running the full platform (many components, Istio, multi-user auth), and the honest 2026 view that many teams adopt individual pieces rather than the whole stack. Give a one-page decision table for 'when Kubeflow, when managed services such as SageMaker or Vertex, when plain Kubernetes Jobs'. Part 5 owns pipeline detail. No source here reports a company's exact question; nothing is executed.
**Asked at:** KServe and Kubeflow references (OneUptime canary model rollouts with KServe, Canonical 'what is KFServing', Arena docs for KServe, KServe v0.5.0 release notes, AMD AIM Engine autoscaling docs, Kubeflow Training Operator job-scheduling docs, Cast.ai Kueue article; search snippets only, not opened); docs and vendor blogs, not interview reports; MLOps roles on Kubeflow or KServe stacks
**Say this first (1 line):** Kubeflow is a toolbox for ML on Kubernetes (pipelines, notebooks, training operators, hyperparameter search, serving), and in 2026 most teams adopt one or two pieces, not the whole platform, because the full stack is heavy to run.

**Then explain:**
- The pieces, in one line each:
  - **Pipelines (KFP):** define a workflow of steps, run each step as a pod, track runs. Part 5 owns the detail.
  - **Notebooks:** per-user Jupyter pods in their own namespace.
  - **Training Operator:** custom resources such as PyTorchJob and TFJob. It creates the worker pods and wires the ranks and addresses for distributed training.
  - **Katib:** hyperparameter search. It launches many trials as Jobs and reads the metric from each.
  - **KServe:** an `InferenceService` resource for model serving (autoscaling, canary, scale-to-zero via Knative in some modes; check current docs).
- Versus plain Jobs plus Argo or Airflow: a Job runs one container to completion. Argo or Airflow adds the DAG. Kubeflow adds ML-specific resources on top (distributed-training wiring, trial loops, a model-serving CRD). If you only need "run this script on a schedule", Kubeflow adds nothing you need.
- The cost of the full platform: many components, a service mesh dependency in the usual install (Istio, check current docs), multi-user auth and profiles, a lot of CRDs to upgrade, and one team that must own all of it. Upgrades across components are the pain.
- Honest 2026 view: teams cherry-pick. KServe alone for serving, Training Operator alone for distributed jobs, KFP or Argo alone for pipelines. This is my reading of the field, not a survey.
- Failure modes: installing the whole platform for a 5-person team; version skew between components and the Kubernetes version; a broken auth layer locking everyone out of notebooks; nobody owning upgrades.

**Example:** A 40-person data science group on a company cluster with a platform team wants notebooks, GPU training and serving behind one login. Kubeflow pieces fit. A 4-person team on AWS with no platform engineer: use the managed service (SageMaker or Vertex), because the cluster itself becomes their second job. A team with one nightly retraining script: a CronJob and a Job template. The script below encodes this reasoning as four toy rules, and the manifest is the "plain Job" option.

**Decision table (one page):**

| Situation | Kubeflow (pieces) | Managed (SageMaker / Vertex / Azure ML) | Plain Jobs + Argo/Airflow |
|---|---|---|---|
| Team size / platform staff | 20+ users, a platform team exists | small team, no cluster owner | any size, some Kubernetes skill |
| Need | notebooks + distributed training + HPO + serving on one cluster | fastest path, pay for convenience | batch training and DAGs only |
| Ops burden | high (many components) | low (vendor runs it) | medium |
| Lock-in | low (open source, you run it) | higher (APIs, IAM, data location) | low |
| Cost shape | cluster + people | per-use service fees (check current docs) | cluster only |
| Pick when | you must stay on your own cluster and want ML-native resources | you want to ship in weeks | the job is "run a container, in order, on a schedule" |

**Code:** the decision helper is a teaching aid, not a product. Run with `python3 -I`.
```python
"""Q31: toy decision helper. Rules are a teaching aid, not a product. Runs offline."""
import pathlib, subprocess, sys

def decide(team):
    why = []
    if not team["has_k8s_platform_team"]:
        why.append("no one to run a cluster")
        if team["wants_managed"]:
            return "managed service (SageMaker / Vertex / Azure ML)", why
    if team["pipelines_only"] and team["has_k8s_platform_team"]:
        why.append("only pipelines needed: take Argo / Airflow / KFP alone, not the platform")
        return "plain Jobs + Argo or Airflow (or KFP alone)", why
    if team["multi_user_notebooks"] and team["hp_search"] and team["has_k8s_platform_team"] and team["data_scientists"] >= 20:
        why.append("many users, notebooks, search and serving on one cluster")
        return "Kubeflow pieces (Notebooks + Training Operator + Katib + KServe)", why
    why.append("small scope, simple batch training")
    return "plain Kubernetes Jobs (+ a scheduler)", why

cases = {
 "A: 4 DS, no platform team, on AWS":   dict(has_k8s_platform_team=False, wants_managed=True, pipelines_only=False, multi_user_notebooks=False, hp_search=False, data_scientists=4),
 "B: 8 DS, platform team, DAGs only":    dict(has_k8s_platform_team=True, wants_managed=False, pipelines_only=True, multi_user_notebooks=False, hp_search=False, data_scientists=8),
 "C: 40 DS, platform team, notebooks":   dict(has_k8s_platform_team=True, wants_managed=False, pipelines_only=False, multi_user_notebooks=True, hp_search=True, data_scientists=40),
 "D: 6 DS, platform team, nightly job":  dict(has_k8s_platform_team=True, wants_managed=False, pipelines_only=False, multi_user_notebooks=False, hp_search=False, data_scientists=6),
}
for name, t in cases.items():
    pick, why = decide(t)
    print(f"{name}\n   -> {pick}\n   because: {'; '.join(why)}")

here = pathlib.Path(__file__).resolve().parent
r = subprocess.run([sys.executable, "-I", "-m", "kubernetes_validate", "--strict", str(here / "q31_job.yaml")], capture_output=True, text=True)
print("\nkubernetes-validate --strict q31_job.yaml (exit", r.returncode, ")\n" + (r.stdout + r.stderr).strip())
```
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: train-churn-001
  labels: {app: churn-train}
spec:
  backoffLimit: 2
  ttlSecondsAfterFinished: 3600
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: train
        image: registry.example.com/churn-train:1.4.2
        command: ["python", "train.py", "--epochs", "5"]
        resources:
          requests: {cpu: "2", memory: 4Gi}
          limits: {memory: 4Gi}
```
```bash
cd code && python3 -I q31_decide.py
kubernetes-validate --strict q31_job.yaml
```

**Output (my run):** the helper and the schema validation ran. Kubeflow, Argo, Airflow and any cluster are **not executed**: no cluster here. `kubernetes-validate --strict` checks the Job schema only, not scheduling or whether the image exists.
```text
A: 4 DS, no platform team, on AWS
   -> managed service (SageMaker / Vertex / Azure ML)
   because: no one to run a cluster
B: 8 DS, platform team, DAGs only
   -> plain Jobs + Argo or Airflow (or KFP alone)
   because: only pipelines needed: take Argo / Airflow / KFP alone, not the platform
C: 40 DS, platform team, notebooks
   -> Kubeflow pieces (Notebooks + Training Operator + Katib + KServe)
   because: many users, notebooks, search and serving on one cluster
D: 6 DS, platform team, nightly job
   -> plain Kubernetes Jobs (+ a scheduler)
   because: small scope, simple batch training

kubernetes-validate --strict q31_job.yaml (exit 0 )
INFO /home/user/case_studies/interviews/scratch/B4P03_Q31-40/code/q31_job.yaml passed for resource job/train-churn-001 against version 1.37
```
```text
INFO q31_job.yaml passed for resource job/train-churn-001 against version 1.37
```

**Follow-ups:**
- *What does the Training Operator add over a plain Job?* It creates a set of pods with the roles and environment a distributed framework expects (master, workers) and handles the job as one unit. A plain Job knows nothing about ranks. Gang scheduling needs a queue such as Kueue or Volcano on top (check current docs).
- *Is Katib worth it?* Only if you run many trials on a shared cluster. For a handful of trials, a script with Optuna in one Job is simpler.
- *Why not just use SageMaker?* If data, IAM and the team already live in that cloud and nobody wants to run a cluster, that is often right. Say so.

**Common mistakes:** installing the whole platform on day one; confusing KFP (pipelines) with the platform; forgetting the cluster needs an owner; claiming "Kubeflow is dead" or "Kubeflow is the standard" without saying which piece.

---

### Q32 ⭐ 🟡 Kubernetes in India MLOps hiring: what do postings ask and how do you prepare without a cluster budget? Summarise the skills lists in Bengaluru-style MLOps postings (Kubernetes, Helm, GPU workloads, autoscaling), then give a practical lab plan using kind, minikube or k3d on a laptop, the free tiers and credits of managed clusters (check current terms), and what a Kubernetes-for-ML portfolio project should show (Helm chart, HPA, probes, a canary). Include a table of skills to labs. State clearly that postings are not interview reports. No cluster is available here; nothing is executed.
**Asked at:** Bengaluru and India MLOps job postings that list Kubernetes, Helm and GPU/CUDA workloads (weekday.works, builtinbengaluru, GrabJobs listings seen while researching Part 2; snippets only) plus editorial Kubernetes guides; postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
**Say this first (1 line):** Postings ask for Kubernetes, Docker, Helm, CI/CD, cloud and sometimes GPU work, and you can build all of that on a laptop with kind or k3d, so show a small model service with a Helm chart, an HPA, probes and a canary, not a big cluster bill.

**Then explain:**
- **What postings ask (pattern, not a report):** the skills lists I saw while researching list Kubernetes, Helm, Docker, autoscaling, and for some roles GPU/CUDA workloads. These are skills lists in postings. They are **not** interview reports, and I have not verified what any company actually asks.
- **Lab tools:** `kind` (Kubernetes in Docker containers), `minikube`, `k3d` (k3s in Docker). All need a container runtime on your laptop. Pick one and learn it well.
- **Managed free tiers and credits:** some clouds offer trial credits or a free control plane tier. Terms change, so check current docs before relying on any of it, and set a budget alert. Delete the cluster after every session.
- **No real GPU?** Practise the Kubernetes side only: node labels, taints, tolerations and `nodeSelector` on a fake "gpu-sim" node, resource requests, and a pod that stays Pending because no node matches. You cannot practise the device plugin or CUDA without a GPU, so say that plainly.
- **Failure modes:** a portfolio that is only a YAML dump; a chart that nobody can install because values are missing; cluster left running overnight on a managed trial; claiming GPU experience from a CPU lab.

**Example (skills to labs):**

| Skill in postings | Lab on a laptop | Proof in the repo |
|---|---|---|
| Deployments, Services | model API in kind, port-forward | `k8s/deploy.yaml`, README with curl |
| Probes | readiness plus startup probe on a slow-loading model | probe config and a note on why |
| Helm | chart with `values.yaml` and a values override | `chart/` folder |
| Autoscaling | HPA on CPU, load with a loop | `hpa.yaml`, screenshot of replicas rising |
| Rollouts | second Deployment as canary with a weight split | canary doc |
| GPU scheduling | fake GPU node label and taint; Pending demo | notes, labelled "simulated" |
| Debugging | break the image tag, read events | a short troubleshooting log |

**Code:** a kind config with one labelled "gpu-sim" worker, and a script that checks a project folder against the portfolio list. The check is a crude text match, not a real review.
```yaml
# kind config: 1 control plane + 2 workers; label one worker "gpu-sim" to practise nodeSelector/taints (no real GPU)
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
  labels:
    node-pool: gpu-sim
```
```python
"""Q32: checks a portfolio project folder for the things a K8s-for-ML repo should show. Runs on a temp demo repo."""
import pathlib, tempfile, yaml

def check(root):
    root = pathlib.Path(root)
    docs = []
    for p in list(root.rglob("*.yaml")) + list(root.rglob("*.yml")):
        if "templates" in p.parts:   # Helm templates hold {{ }} and are not plain YAML
            docs.append(("tmpl", p.read_text()))
            continue
        try:
            for d in yaml.safe_load_all(p.read_text()):
                if isinstance(d, dict): docs.append(("yaml", d))
        except yaml.YAMLError:
            pass
    text = " ".join(str(d) for _, d in docs)
    return {
      "Chart.yaml (Helm chart)": (root / "chart" / "Chart.yaml").exists(),
      "values.yaml":              (root / "chart" / "values.yaml").exists(),
      "HPA":                      "HorizontalPodAutoscaler" in text,
      "readiness probe":          "readinessProbe" in text,
      "startup probe":            "startupProbe" in text,
      "canary (2nd Deployment or weight)": "canary" in text.lower(),
      "resource requests/limits": "requests" in text and "limits" in text,
      "README with run steps":    (root / "README.md").exists(),
    }

with tempfile.TemporaryDirectory() as t:
    r = pathlib.Path(t)
    (r / "chart" / "templates").mkdir(parents=True)
    (r / "chart" / "Chart.yaml").write_text("apiVersion: v2\nname: model-api\nversion: 0.1.0\n")
    (r / "chart" / "values.yaml").write_text("replicas: 2\n")
    (r / "chart" / "templates" / "deploy.yaml").write_text("kind: Deployment\n# {{ .Values.replicas }} readinessProbe canary\n")
    (r / "k8s").mkdir()
    (r / "k8s" / "hpa.yaml").write_text("apiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nmetadata: {name: model-api}\n")
    (r / "k8s" / "deploy.yaml").write_text(
        "apiVersion: apps/v1\nkind: Deployment\nmetadata: {name: model-api}\nspec:\n  template:\n    spec:\n      containers:\n"
        "      - name: api\n        readinessProbe: {httpGet: {path: /ready, port: 8000}}\n"
        "        resources: {requests: {cpu: 100m}, limits: {memory: 256Mi}}\n")
    for k, v in check(r).items():
        print(f"{'PASS' if v else 'MISSING':8}{k}")
```
```bash
# not executed (no kind, no Docker daemon here): kind create cluster --config q32_kind.yaml
python3 -I q32_portfolio_check.py
```

**Output (my run):** `kind` is **not executed**: no Docker daemon and no kind binary here. I did run the portfolio checker on a demo folder it builds in a temp directory, and parsed the kind config with PyYAML (that only proves the YAML is valid, not that kind accepts it).
```text
PASS    Chart.yaml (Helm chart)
PASS    values.yaml
PASS    HPA
PASS    readiness probe
MISSING startup probe
PASS    canary (2nd Deployment or weight)
PASS    resource requests/limits
MISSING README with run steps
```
```text
{'kind': 'Cluster', 'apiVersion': 'kind.x-k8s.io/v1alpha4', 'nodes': [{'role': 'control-plane'}, {'role': 'worker'}, {'role': 'worker', 'labels': {'node-pool': 'gpu-sim'}}]}
```

**Follow-ups:**
- *How do you show HPA working without real traffic?* Run a loop of requests from a busybox pod and watch replicas. Metrics-server must be installed in kind (check current docs).
- *Free managed cluster?* Check current terms of each cloud; treat any credit as time-limited.
- *Is a Kubernetes certificate needed?* A project with a working chart and a rollback story says more. Certificates are optional extras.

**Common mistakes:** listing "Kubernetes" with no repo; pasting a tutorial unchanged; leaving a cloud cluster running; saying "I used GPUs" when the lab was CPU-only.

---

### Q33 ⭐ 🔴 StatefulSet versus Deployment, and when ML needs a StatefulSet: stable network identity, ordered startup, volumeClaimTemplates for per-replica storage (vector DBs, feature stores, distributed training workers with stable ranks). Explain headless Services, why StatefulSet pods are slower to roll, and why a stateless model server should stay a Deployment. Give a StatefulSet manifest with a volumeClaimTemplate and a script that lists the pod names and PVC names it will create for a given replica count. Not executed on a cluster.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A StatefulSet gives each pod a stable name, stable storage and ordered start, so use it for things that remember who they are (vector DBs, feature store nodes, ranked training workers) and keep stateless model servers as Deployments.

**Then explain:**
- **Stable identity:** pods are `name-0`, `name-1`, ... and keep those names across restarts. A **headless Service** (`clusterIP: None`) gives each pod its own DNS name, `name-0.svc.ns.svc.cluster.local`, so peers can find a specific member.
- **Ordered startup:** with the default `OrderedReady` policy, pod 1 starts only after pod 0 is Ready, and scale-down goes in reverse. `podManagementPolicy: Parallel` removes the ordering when you do not need it.
- **volumeClaimTemplates:** each replica gets its own PVC (`data-vecdb-0`, `data-vecdb-1`, ...). If pod 1 is rescheduled, it reattaches to `data-vecdb-1`. PVCs are kept on scale-down by default (there is a retention policy setting; check current docs), so scaling down does not free the disks.
- **Why they roll slowly:** rolling update goes one pod at a time, in reverse ordinal order, and waits for Ready each time. A slow readiness probe is paid once per replica. With `ReadWriteOnce` volumes, a pod moving to another node must wait for the disk to detach and attach.
- **Why not for a stateless model server:** it does not need identity or per-pod disks, and ordered, one-at-a-time rolling just makes deploys slow. A Deployment can surge and replace pods in parallel, and an HPA scales it freely.
- **Failure modes:** a pod stuck Pending because its zone-bound PVC cannot attach on the free node; a broken pod 0 blocking pods 1 and 2 from ever starting; deleting a StatefulSet and forgetting the PVCs (cost, and stale data on re-create).

**Example:** `replicas: 3`, StatefulSet `vecdb`, template named `data`. Pods: `vecdb-0`, `vecdb-1`, `vecdb-2`. PVCs: `data-vecdb-0`, `data-vecdb-1`, `data-vecdb-2` (rule: template name, dash, pod name). Scale to 5 adds `vecdb-3` and `vecdb-4` with new PVCs. Scale back to 3 deletes the pods but leaves `data-vecdb-3` and `data-vecdb-4` behind.

**Code:** manifest (headless Service plus StatefulSet) and a script that prints the names for a given replica count.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: vecdb
spec:
  clusterIP: None            # headless: DNS returns pod IPs, gives each pod a stable name
  selector: {app: vecdb}
  ports:
  - {name: grpc, port: 6334}
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vecdb
spec:
  serviceName: vecdb         # must match the headless Service
  replicas: 3
  podManagementPolicy: OrderedReady
  selector:
    matchLabels: {app: vecdb}
  updateStrategy:
    type: RollingUpdate
  template:
    metadata:
      labels: {app: vecdb}
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: db
        image: registry.example.com/vector-db:2.3.1
        ports:
        - {containerPort: 6334, name: grpc}
        readinessProbe:
          tcpSocket: {port: 6334}
        resources:
          requests: {cpu: "1", memory: 4Gi}
          limits: {memory: 4Gi}
        volumeMounts:
        - {name: data, mountPath: /var/lib/vecdb}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests: {storage: 50Gi}
```
```python
"""Q33: list the pod names, PVC names and DNS names a StatefulSet will create. Reads the manifest, no cluster."""
import pathlib, sys, yaml

def plan(sts, ns="default"):
    name = sts["metadata"]["name"]; n = sts["spec"]["replicas"]; svc = sts["spec"]["serviceName"]
    vcts = [v["metadata"]["name"] for v in sts["spec"].get("volumeClaimTemplates", [])]
    rows = []
    for i in range(n):
        pod = f"{name}-{i}"
        rows.append((pod, [f"{v}-{pod}" for v in vcts], f"{pod}.{svc}.{ns}.svc.cluster.local"))
    return rows

path = pathlib.Path(__file__).resolve().parent / "q33_statefulset.yaml"
sts = next(d for d in yaml.safe_load_all(path.read_text()) if d["kind"] == "StatefulSet")
for replicas in (sts["spec"]["replicas"], 5):
    sts["spec"]["replicas"] = replicas
    print(f"replicas={replicas}")
    for pod, pvcs, dns in plan(sts):
        print(f"  {pod:8} pvc={','.join(pvcs):14} dns={dns}")
print("start order: 0 -> 1 -> 2 (OrderedReady); stop order: reverse. PVCs are NOT deleted on scale-down by default.")
```
```bash
python3 -I q33_names.py
kubernetes-validate --strict q33_statefulset.yaml
```

**Output (my run):** the name script and the schema validation ran. Applying the StatefulSet, PVC binding and rolling behaviour are **not executed**: no cluster. The statements about ordering and PVC retention come from the Kubernetes docs as I know them, not from a run here.
```text
replicas=3
  vecdb-0  pvc=data-vecdb-0   dns=vecdb-0.vecdb.default.svc.cluster.local
  vecdb-1  pvc=data-vecdb-1   dns=vecdb-1.vecdb.default.svc.cluster.local
  vecdb-2  pvc=data-vecdb-2   dns=vecdb-2.vecdb.default.svc.cluster.local
replicas=5
  vecdb-0  pvc=data-vecdb-0   dns=vecdb-0.vecdb.default.svc.cluster.local
  vecdb-1  pvc=data-vecdb-1   dns=vecdb-1.vecdb.default.svc.cluster.local
  vecdb-2  pvc=data-vecdb-2   dns=vecdb-2.vecdb.default.svc.cluster.local
  vecdb-3  pvc=data-vecdb-3   dns=vecdb-3.vecdb.default.svc.cluster.local
  vecdb-4  pvc=data-vecdb-4   dns=vecdb-4.vecdb.default.svc.cluster.local
start order: 0 -> 1 -> 2 (OrderedReady); stop order: reverse. PVCs are NOT deleted on scale-down by default.
```
```text
INFO q33_statefulset.yaml passed for resource service/vecdb against version 1.37
INFO q33_statefulset.yaml passed for resource statefulset/vecdb against version 1.37
```

**Follow-ups:**
- *Distributed training workers?* Stable ranks and DNS names help, but in practice most teams use the Training Operator (PyTorchJob) rather than a raw StatefulSet. It handles the wiring.
- *Can a StatefulSet use a shared volume?* Yes, with a manually created PVC and `ReadWriteMany`, but then you lose per-replica storage, which is the point.
- *Pod stuck Terminating on a dead node?* StatefulSet will not start a duplicate until the old pod is confirmed gone. That is a safety feature (at-most-one pod per identity).

**Common mistakes:** missing or mismatched `serviceName`; using a StatefulSet for a stateless API; expecting PVCs to vanish on scale-down; no readiness probe, so ordered start moves on too early.

---

### Q34 ⭐ 🔴 DaemonSets and operators in an ML cluster. Explain what a DaemonSet is (one pod per node: the NVIDIA device plugin, log shippers, node exporters), nodeSelector on a DaemonSet to target GPU nodes only, and the operator pattern (custom resource plus controller: GPU Operator, Training Operator, KServe) as the way platforms extend Kubernetes. Give a DaemonSet manifest and a toy reconcile loop in Python that treats a custom resource as desired state and runs for real. Real operators are not executed.
**Asked at:** Kubernetes-for-AI question bank (Cloud Soft Solutions 'Kubernetes for AI interview questions'), NerdLevelTech MLOps interview course page, KodeKloud MLOps guide, SuperOrbital/CNCF NVIDIA device plugin post, NVIDIA GPU Operator time-slicing docs (v1.11 page only), University of Bergen RAIL GPU docs; search snippets only, not opened (WebFetch failed with ENOTFOUND); guides and docs, not verified candidate reports; GPU and deep-learning MLOps roles at product companies, GCCs and AI startups
**Say this first (1 line):** A DaemonSet runs one pod on every (matching) node for node-level jobs like the GPU device plugin or log shippers, and an operator is a custom resource plus a controller that keeps reconciling actual state to the desired state in that resource.

**Then explain:**
- **DaemonSet:** one pod per node, new node means new pod automatically. Typical ML uses: NVIDIA device plugin, DCGM exporter, node-exporter, log shipper. Use `nodeSelector` (or node affinity) to restrict it to GPU nodes, and a **toleration** because GPU nodes are usually tainted.
- **Operator pattern:** you define a CRD (say `ModelServer`), users create objects of that kind, and a controller watches them. The loop: read desired state, read actual state, make the smallest change, repeat. It is level-based, so it is safe to run again and recovers from missed events.
- **ML examples:** GPU Operator (installs driver, device plugin, monitoring pieces), Training Operator (PyTorchJob), KServe (InferenceService). Names and details: check current docs.
- **Failure modes:** a DaemonSet without the toleration silently skips GPU nodes; a DaemonSet with no resource requests starves workloads; a controller that is not idempotent creates duplicates; a buggy operator can delete everything (it has cluster permissions); CRD version upgrades breaking stored objects.

**Example:** nodes: 2 CPU, 3 GPU (labelled `node-pool=gpu`, tainted). The DaemonSet below produces 3 pods, not 5. Remove the toleration and it produces 0. In the toy loop: the CR says 3 replicas, one pod is killed, the next tick recreates it; edit the CR to 2 and the extra pod goes; change the image and pods are replaced.

**Code:** a DaemonSet manifest and a toy reconcile loop. The loop is a simulation: the "cluster" is a dict, there is no watch, no API server and no finalizers.
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: gpu-node-agent
  namespace: kube-system
spec:
  selector:
    matchLabels: {app: gpu-node-agent}
  updateStrategy:
    type: RollingUpdate
    rollingUpdate: {maxUnavailable: 1}
  template:
    metadata:
      labels: {app: gpu-node-agent}
    spec:
      nodeSelector:
        node-pool: gpu          # only nodes with this label get a pod
      tolerations:
      - {key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}   # GPU nodes are tainted
      priorityClassName: system-node-critical
      containers:
      - name: agent
        image: registry.example.com/gpu-node-agent:0.3.0
        resources:
          requests: {cpu: 50m, memory: 64Mi}
          limits: {memory: 128Mi}
```
```python
"""Q34: toy operator. A 'ModelServer' custom resource is desired state; reconcile() drives actual state to it.
Pure Python, runs for real. The 'cluster' is a dict; failures are injected to show self-healing."""
import copy

desired = {"ModelServer/churn": {"replicas": 3, "image": "churn:1.0"}}   # the custom resources (spec)
actual = {}                                                              # pods that exist: name -> image

def reconcile(cr_name, spec):
    """Level-based: look at the whole picture, do the minimum to converge, safe to run again."""
    base = cr_name.split("/")[1]
    want = {f"{base}-{i}": spec["image"] for i in range(spec["replicas"])}
    actions = []
    for pod in sorted(set(actual) - set(want)):
        del actual[pod]; actions.append(f"delete {pod}")
    for pod, img in want.items():
        if pod not in actual:
            actual[pod] = img; actions.append(f"create {pod} ({img})")
        elif actual[pod] != img:
            actual[pod] = img; actions.append(f"replace {pod} -> {img}")
    return actions

def tick(label):
    acts = []
    for cr, spec in desired.items():
        acts += reconcile(cr, spec)
    print(f"[{label}] actions={acts or 'none (converged)'} actual={dict(sorted(actual.items()))}")

tick("t0 first run")
tick("t1 nothing changed")
del actual["churn-1"]                                   # a pod dies
tick("t2 pod churn-1 killed")
desired["ModelServer/churn"]["replicas"] = 2            # user edits the CR: scale down
tick("t3 replicas 3->2")
desired["ModelServer/churn"]["image"] = "churn:1.1"     # user edits the CR: new image
tick("t4 image 1.0->1.1")
tick("t5 idempotent re-run")
del desired["ModelServer/churn"]                        # CR deleted (a real operator uses finalizers; here: cleanup by hand)
actual.clear()
tick("t6 CR deleted, cleaned up")
```
```bash
python3 -I q34_reconcile.py
kubernetes-validate --strict q34_daemonset.yaml
```

**Output (my run):** the reconcile loop ran for real (as a Python simulation), and the DaemonSet passed schema validation. Real operators, the device plugin and DaemonSet scheduling are **not executed**: no cluster, no GPU.
```text
[t0 first run] actions=['create churn-0 (churn:1.0)', 'create churn-1 (churn:1.0)', 'create churn-2 (churn:1.0)'] actual={'churn-0': 'churn:1.0', 'churn-1': 'churn:1.0', 'churn-2': 'churn:1.0'}
[t1 nothing changed] actions=none (converged) actual={'churn-0': 'churn:1.0', 'churn-1': 'churn:1.0', 'churn-2': 'churn:1.0'}
[t2 pod churn-1 killed] actions=['create churn-1 (churn:1.0)'] actual={'churn-0': 'churn:1.0', 'churn-1': 'churn:1.0', 'churn-2': 'churn:1.0'}
[t3 replicas 3->2] actions=['delete churn-2'] actual={'churn-0': 'churn:1.0', 'churn-1': 'churn:1.0'}
[t4 image 1.0->1.1] actions=['replace churn-0 -> churn:1.1', 'replace churn-1 -> churn:1.1'] actual={'churn-0': 'churn:1.1', 'churn-1': 'churn:1.1'}
[t5 idempotent re-run] actions=none (converged) actual={'churn-0': 'churn:1.1', 'churn-1': 'churn:1.1'}
[t6 CR deleted, cleaned up] actions=none (converged) actual={}
```
```text
INFO q34_daemonset.yaml passed for resource daemonset/gpu-node-agent against version 1.37
```

**Follow-ups:**
- *Why level-based, not edge-based?* Events can be missed or repeated. Comparing full desired and actual state each time converges either way.
- *DaemonSet vs Deployment with one replica per node?* DaemonSet follows node count automatically and tolerates node-specific needs.
- *How is a CRD different from a ConfigMap?* A CRD adds a typed API object with validation and a controller acting on it. A ConfigMap is just data.

**Common mistakes:** forgetting tolerations; thinking an operator is magic and not a program with permissions; running a DaemonSet with host access without thinking about security (see Q35); writing a controller that is not idempotent.

---

### Q35 ⭐ 🔴 Security hardening for ML pods: run as non-root, readOnlyRootFilesystem, drop capabilities, no privileged GPU hacks, seccomp, Pod Security Standards (privileged, baseline, restricted) enforced per namespace, image pull secrets, private registry, and not mounting service account tokens when not needed. Give a hardened pod spec, explain what breaks for ML (writable cache directories, /dev/shm, GPU access), and write a script that scores a manifest against a short checklist. Enforcement on a cluster is not executed.
**Asked at:** Multi-tenancy and RBAC guides (adhdecode multi-tenancy interview page, Dataford resource quota question, OneUptime multi-tenancy and RBAC posts, Uffizzi quota article; search snippets only, not opened); editorial question banks, not verified candidate reports; platform, SRE and MLOps loops at GCCs and product companies
**Say this first (1 line):** Run as non-root with a read-only root filesystem, drop all capabilities, use the runtime-default seccomp profile, never use privileged mode for GPUs, enforce Pod Security Standards per namespace, and give ML pods writable emptyDir paths for caches and `/dev/shm`.

**Then explain:**
- **The hardening list:** `runAsNonRoot`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`, `seccompProfile: RuntimeDefault`, no `hostNetwork` or `privileged`, `automountServiceAccountToken: false` when the pod never calls the API, images pinned by tag or digest from a private registry with `imagePullSecrets`.
- **Pod Security Standards:** three levels: privileged (anything), baseline (blocks the known-dangerous), restricted (current hardening best practice). Enforced per namespace with Pod Security Admission labels (`pod-security.kubernetes.io/enforce: restricted`). Use `warn` and `audit` modes first to see what would break.
- **What breaks for ML:**
  - Read-only root: libraries want to write caches (`HF_HOME`, `~/.cache`, `/tmp`, compiled kernels). Point env vars at an `emptyDir` mount.
  - `/dev/shm`: PyTorch DataLoader workers use shared memory; the default is small. Mount an in-memory `emptyDir` at `/dev/shm`.
  - GPU access: you request `nvidia.com/gpu` in limits and the device plugin and runtime inject the device. You do **not** need `privileged: true`. If an image insists on root, fix the image (numeric `USER`, writable dirs).
  - Volumes written by a different uid: use `fsGroup`.
- **Failure modes:** pod fails with `Read-only file system` at first model download; `runAsNonRoot` with an image whose `USER` is a name, not a number, gets "cannot verify non-root"; restricted namespace rejects a GPU sidecar that needs host paths; a scoring script that says green while the namespace label is missing.

**Example:** the sloppy pod below has `privileged: true`, `hostNetwork`, `:latest` and no seccomp, and scores 0 of 10. The hardened pod scores 10 of 10 and still gets a GPU, a cache dir and a bigger `/dev/shm`.

**Code:** the hardened pod, a deliberately bad pod, and the checklist scorer. The scorer is my short checklist, not the official Pod Security check.
```yaml
# ===== q35_hardened.yaml =====
apiVersion: v1
kind: Pod
metadata:
  name: infer-hardened
  labels: {app: infer}
spec:
  automountServiceAccountToken: false
  serviceAccountName: infer-sa
  imagePullSecrets:
  - name: regcred
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
    seccompProfile: {type: RuntimeDefault}
  containers:
  - name: server
    image: registry.example.com/infer@sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities: {drop: ["ALL"]}
    env:
    - {name: HF_HOME, value: /cache/hf}
    - {name: TMPDIR, value: /tmp}
    resources:
      requests: {cpu: "2", memory: 8Gi}
      limits: {memory: 8Gi, nvidia.com/gpu: 1}
    volumeMounts:
    - {name: tmp, mountPath: /tmp}
    - {name: cache, mountPath: /cache}
    - {name: shm, mountPath: /dev/shm}
  volumes:
  - {name: tmp, emptyDir: {}}
  - {name: cache, emptyDir: {sizeLimit: 10Gi}}
  - {name: shm, emptyDir: {medium: Memory, sizeLimit: 2Gi}}
# ===== q35_bad.yaml =====
apiVersion: v1
kind: Pod
metadata: {name: infer-sloppy}
spec:
  hostNetwork: true
  containers:
  - name: server
    image: registry.example.com/infer:latest
    securityContext:
      privileged: true
    resources:
      limits: {nvidia.com/gpu: 1}
```
```python
"""Q35: score a Pod manifest against a short hardening checklist (Pod Security 'restricted' flavoured). Not a full PSS check."""
import pathlib, sys, yaml

def score(pod):
    spec = pod["spec"]; psc = spec.get("securityContext", {}); out = []
    def add(name, ok, why=""): out.append((name, bool(ok), why))
    add("automountServiceAccountToken false", spec.get("automountServiceAccountToken") is False, "token mounted by default")
    add("no hostNetwork/hostPID/hostIPC", not any(spec.get(k) for k in ("hostNetwork", "hostPID", "hostIPC")))
    add("pod seccomp RuntimeDefault", psc.get("seccompProfile", {}).get("type") in ("RuntimeDefault", "Localhost"))
    for c in spec["containers"]:
        sc = c.get("securityContext", {}); n = c["name"]
        add(f"{n}: runAsNonRoot", psc.get("runAsNonRoot") or sc.get("runAsNonRoot"))
        add(f"{n}: not privileged", not sc.get("privileged"))
        add(f"{n}: allowPrivilegeEscalation false", sc.get("allowPrivilegeEscalation") is False)
        add(f"{n}: readOnlyRootFilesystem", sc.get("readOnlyRootFilesystem") is True)
        add(f"{n}: drop ALL capabilities", "ALL" in sc.get("capabilities", {}).get("drop", []))
        img = c["image"]
        add(f"{n}: image pinned (digest or non-latest tag)", "@sha256:" in img or (":" in img.split("/")[-1] and not img.endswith(":latest")))
        add(f"{n}: memory limit set", "memory" in c.get("resources", {}).get("limits", {}))
    return out

for f in sys.argv[1:]:
    pod = yaml.safe_load(pathlib.Path(f).read_text())
    res = score(pod); ok = sum(r[1] for r in res)
    print(f"== {pathlib.Path(f).name}: {ok}/{len(res)}")
    for name, good, why in res:
        if not good: print(f"   FAIL {name} {('(' + why + ')') if why else ''}")
```
```bash
python3 -I q35_score.py q35_hardened.yaml q35_bad.yaml
kubernetes-validate --strict q35_hardened.yaml q35_bad.yaml
```

**Output (my run):** scorer and schema validation ran. Both pods are schema-valid (the validator does not judge security). Pod Security Admission, seccomp, GPU access and the read-only filesystem behaviour are **not executed**: no cluster.
```text
== q35_hardened.yaml: 10/10
== q35_bad.yaml: 0/10
   FAIL automountServiceAccountToken false (token mounted by default)
   FAIL no hostNetwork/hostPID/hostIPC 
   FAIL pod seccomp RuntimeDefault 
   FAIL server: runAsNonRoot 
   FAIL server: not privileged 
   FAIL server: allowPrivilegeEscalation false 
   FAIL server: readOnlyRootFilesystem 
   FAIL server: drop ALL capabilities 
   FAIL server: image pinned (digest or non-latest tag) 
   FAIL server: memory limit set 
```
```text
INFO q35_hardened.yaml passed for resource pod/infer-hardened against version 1.37
INFO q35_bad.yaml passed for resource pod/infer-sloppy against version 1.37
```

**Follow-ups:**
- *Is `restricted` enough?* It covers the pod spec. Add NetworkPolicy, RBAC least privilege, image scanning and signing. Not a full security story.
- *Can I use PSS for a namespace with GPU operator pods?* The operator namespace usually needs a looser level (privileged) since it installs drivers; keep tenant namespaces at restricted. Check the operator docs.
- *Why disable the service account token?* A stolen token is API access. If the model server never calls the API, remove it.

**Common mistakes:** `privileged: true` "to make the GPU work"; running as root because the Dockerfile did; forgetting `/dev/shm` then blaming Kubernetes for DataLoader crashes; enforcing `restricted` cluster-wide on day one with no warn period.

---

### Q36 ⭐ 🔴 Cost control for Kubernetes ML workloads: right-sizing with VPA recommendations, spot or preemptible nodes for training with checkpointing, scale-to-zero for idle endpoints, separate node pools for CPU and GPU, quotas per team, TTL on finished Jobs, and cleaning orphaned PVCs and load balancers. Give a worked example with made-up round numbers (no real prices) comparing always-on GPU replicas versus scale-to-zero with cold starts, and a script that computes idle GPU-hours from a utilisation log. Cloud billing is not executed; Part 12 owns cost design in depth.
**Asked at:** Autoscaling write-ups (techinterview.org 'System Design Interview: Kubernetes Autoscaling (HPA, VPA, KEDA, Cluster Autoscaler)', AWS EKS ML inference autoscaling HPA and KEDA guide, CloudNativeNow KEDA articles, dev.to VPA/HPA/KEDA patterns; search snippets only, not opened); editorial and vendor docs, not verified candidate reports; senior MLOps and platform loops
**Say this first (1 line):** Most GPU waste is idle time, so measure idle GPU-hours first, then right-size, put training on spot nodes with checkpoints, scale idle endpoints to zero (accepting cold starts), and use quotas and TTLs so nothing is forgotten.

**Then explain:**
- **Right-sizing:** VPA in recommendation mode shows what a pod really used versus what it asked for. Use it as advice, not as automatic restarts for latency-sensitive pods. GPU memory and utilisation need GPU metrics, not VPA.
- **Spot or preemptible nodes for training:** cheaper but can vanish with short notice. It works only if the job **checkpoints** and can resume. Keep serving on on-demand nodes.
- **Scale-to-zero for idle endpoints:** HPA alone cannot go to zero (its minimum is 1 by default); KEDA or a serverless layer like Knative/KServe can (check current docs). The price is a **cold start**: node start if needed, image pull, weights load into GPU memory. Keep one warm replica if latency matters.
- **Structure:** separate CPU and GPU node pools (taint the GPU pool); ResourceQuota per team; `ttlSecondsAfterFinished` on Jobs; clean up orphaned PVCs and load balancers (they bill while idle). Part 12 owns cost design in depth.
- **Failure modes:** spot reclaim with no checkpoint loses hours; scale-to-zero on an endpoint with a strict latency target; a "temporary" notebook holding a GPU for weeks; deleted workloads leaving PVCs and load balancers.

**Example (made-up round numbers, unit is GPU-hours not money):** 2 GPU replicas always on: 2 x 24 = 48 GPU-h per day. Traffic only 6 hours a day. Scale to zero outside traffic: 2 x 6 = 12 GPU-h, plus 2 cold starts of 3 minutes each on 2 GPUs = 0.2, so 12.2 GPU-h. Saving 35.8 GPU-h (about 75 percent), paid for with a 3-minute wait for the first request after idle. A middle road: keep 1 warm replica, which costs 1 x 24 + 1 x 6 = 30 GPU-h and no cold start for the first user.

**Code:** a script that computes idle GPU-hours from an hourly log (one row = one GPU for one hour, util below 10 percent counts as idle; the threshold is a policy choice) and the arithmetic above.
```python
"""Q36: idle GPU-hours from an hourly utilisation log (one row = one GPU for one hour), plus the always-on vs scale-to-zero example.
All numbers are made up. Cost unit is 'GPU-hour' so no prices are needed."""
import csv, pathlib, collections

IDLE_BELOW = 10          # percent; a policy choice, state it out loud
rows = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parent / "q36_util_log.csv")))
per = collections.defaultdict(lambda: [0, 0])
for r in rows:
    p = per[r["pod"]]; p[0] += 1; p[1] += int(r["gpu_util_pct"]) < IDLE_BELOW
tot = idle = 0
print(f"{'pod':9}{'gpu-hours':>10}{'idle':>6}{'idle %':>8}")
for pod, (n, i) in sorted(per.items()):
    print(f"{pod:9}{n:>10}{i:>6}{100*i/n:>8.0f}"); tot += n; idle += i
print(f"{'TOTAL':9}{tot:>10}{idle:>6}{100*idle/tot:>8.0f}   (idle = util < {IDLE_BELOW}%)")

print("\nAlways-on vs scale-to-zero (made-up: 2 GPU replicas, traffic 6 h/day, cold start 3 min)")
gpus, busy_h, cold_min = 2, 6, 3
always = gpus * 24
s2z = gpus * busy_h + gpus * (cold_min / 60) * 2     # assume 2 cold starts/day, GPU billed while loading
print(f"always-on    : {always} GPU-h/day")
print(f"scale-to-zero: {s2z:.1f} GPU-h/day  (saves {always - s2z:.1f}, {100*(always-s2z)/always:.0f}%)")
print(f"price of it  : first request after idle waits about {cold_min} min unless one replica is kept warm")
```
```bash
python3 -I q36_idle.py
```

**Output (my run):** ran with a made-up 15-row log (CSV in `code/q36_util_log.csv`). Hand check: infer-a has 6 rows, util 2, 1, 0, 60, 70, 5, so 4 are below 10 percent. Cloud billing, VPA, KEDA and spot behaviour are **not executed**: no cluster, no cloud account.
```text
pod       gpu-hours  idle  idle %
infer-a           6     4      67
infer-b           6     4      67
train-x           3     1      33
TOTAL            15     9      60   (idle = util < 10%)

Always-on vs scale-to-zero (made-up: 2 GPU replicas, traffic 6 h/day, cold start 3 min)
always-on    : 48 GPU-h/day
scale-to-zero: 12.2 GPU-h/day  (saves 35.8, 75%)
price of it  : first request after idle waits about 3 min unless one replica is kept warm
```

**Follow-ups:**
- *How do you find orphaned PVCs?* List PVCs not mounted by any pod and older than a threshold, then review. Do not auto-delete data.
- *Spot for inference?* Possible with enough replicas and a fallback on-demand pool, but each reclaim is a cold start; judge by SLO.
- *Is low GPU utilisation always waste?* No. A latency-bound model with batch size 1 can show low utilisation yet be sized right. Look at queue time and throughput too.

**Common mistakes:** no checkpointing on spot; one huge node pool for everything; trusting average utilisation (hides bursts); quoting prices from memory.

---

### Q37 ⭐ 🔴 Managed Kubernetes for ML: EKS, AKS and GKE at the level an interviewer expects. Compare control-plane management, node pools with GPU instance types, IAM mapping to pods (IRSA, Workload Identity; names hedged, check current docs), load balancer and storage integrations, and when to pick SageMaker or Vertex instead of running your own cluster. No cloud account is available; nothing is executed. Parts 10 and 11 own cloud details, so keep this to the Kubernetes angle and give a comparison table.
**Asked at:** Editorial Kubernetes interview guides and question banks (weekday.works '45 Kubernetes Interview Questions (2026)', techinterview.org, vervecopilot troubleshooting list, WeCreateProblems, Codecademy, DataCamp; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** EKS, AKS and GKE all run the control plane for you and differ in how they handle GPU node pools, pod-to-cloud identity, load balancers and storage; I pick managed Kubernetes when I need the Kubernetes API itself, and SageMaker or Vertex when I would rather not run a cluster.

**Then explain:**
- **Control plane:** the cloud runs and upgrades the API server and etcd; you manage node pools (or let an autopilot-style mode manage them; check current docs). Upgrade cadence and support windows differ; check current docs.
- **GPU node pools:** a separate pool with GPU instance types, tainted so only GPU pods land there, with the NVIDIA driver and device plugin installed (some clouds preinstall, some need the GPU Operator or an add-on; check current docs).
- **Pod identity:** pods should get short-lived cloud credentials through the ServiceAccount, not static keys. Names: IRSA (and EKS Pod Identity) on EKS, Workload Identity on GKE, Azure Workload Identity on AKS. The manifest pattern is an annotation on the ServiceAccount (hedge the exact keys).
- **Load balancer and storage integrations:** a Service of type LoadBalancer or an Ingress provisions a cloud load balancer; PVCs map to cloud disks through a CSI driver. Disks are zonal, so a pod can be stuck if its zone has no GPU capacity.
- **When SageMaker/Vertex instead:** small team, no cluster owner, want managed training and endpoints. Parts 10 and 11 own the cloud detail.
- **Failure modes:** GPU quota not approved in the region; static keys in Secrets; nodes in one zone while the PVC is in another; surprise load balancers per Service.

**Example (comparison table, keep it at interview level):**

| Topic | EKS | AKS | GKE |
|---|---|---|---|
| Control plane | managed | managed | managed (plus Autopilot mode) |
| GPU pools | node group with GPU instance types | GPU node pool | node pool with accelerators |
| Pod identity | IRSA / Pod Identity | Workload Identity | Workload Identity |
| Load balancer | cloud LB via controller or in-tree | cloud LB | cloud LB |
| Block storage | EBS via CSI | Azure Disk via CSI | Persistent Disk via CSI |
| Pick instead | SageMaker | Azure ML | Vertex AI |

All cells are from memory and hedged. Check current docs.

**Code:** the same idea on three clouds as ServiceAccount annotations (fake ids), plus a check that each carries its key.
```yaml
# Same idea on three clouds: annotate a ServiceAccount, the cloud maps it to a cloud identity. Names hedged: check current docs.
apiVersion: v1
kind: ServiceAccount
metadata:
  name: trainer-eks
  namespace: ml
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/ml-trainer   # IRSA (EKS Pod Identity is the newer alternative)
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: trainer-gke
  namespace: ml
  annotations:
    iam.gke.io/gcp-service-account: ml-trainer@my-project.iam.gserviceaccount.com   # GKE Workload Identity
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: trainer-aks
  namespace: ml
  annotations:
    azure.workload.identity/client-id: 00000000-0000-0000-0000-000000000000   # AKS Workload Identity (pod also needs a label)
```
```python
"""Q37: each ServiceAccount carries the identity annotation its cloud expects; the manifests are placeholders (fake account ids)."""
import pathlib, yaml
EXPECT = {"trainer-eks": "eks.amazonaws.com/role-arn", "trainer-gke": "iam.gke.io/gcp-service-account", "trainer-aks": "azure.workload.identity/client-id"}
for d in yaml.safe_load_all((pathlib.Path(__file__).resolve().parent / "q37_sa.yaml").read_text()):
    name = d["metadata"]["name"]; key = EXPECT[name]
    print(f"{name:12} {key:34} {'present' if key in d['metadata'].get('annotations', {}) else 'MISSING'}")
```
```bash
python3 -I q37_check.py
kubernetes-validate --strict q37_sa.yaml
```

**Output (my run):** the annotation check and schema validation ran. Annotations are free-form strings to the schema, so passing proves only that the YAML is a valid ServiceAccount. Whether a cloud accepts them is **not executed**: no cloud account, no cluster.
```text
trainer-eks  eks.amazonaws.com/role-arn         present
trainer-gke  iam.gke.io/gcp-service-account     present
trainer-aks  azure.workload.identity/client-id  present
```
```text
INFO q37_sa.yaml passed for resource serviceaccount/trainer-eks against version 1.37
INFO q37_sa.yaml passed for resource serviceaccount/trainer-gke against version 1.37
INFO q37_sa.yaml passed for resource serviceaccount/trainer-aks against version 1.37
```

**Follow-ups:**
- *Why not put cloud keys in a Secret?* They are long-lived, easy to leak and hard to rotate. Federated short-lived tokens are safer.
- *Autopilot-style modes for GPUs?* Check current docs for GPU support and limits.
- *Multi-cloud?* Kubernetes helps with manifests, but identity, storage and load balancers still differ per cloud.

**Common mistakes:** saying "managed" means "no ops"; forgetting zonal disks; no GPU quota check; quoting instance names from memory.

---

### Q38 ⭐ 🔴 Observability for ML on Kubernetes: kubectl top and metrics-server, Prometheus scraping of the model's /metrics endpoint, GPU metrics through DCGM exporter (hedge), liveness of dashboards versus alerts, events and logs retention, and the four signals to alert on for a model service (latency, errors, saturation, and a model-quality proxy). Give a ServiceMonitor or scrape-config sketch, a Python prometheus-style metrics text parser and PromQL examples for p95 latency and GPU utilisation (hedged). Not executed on a cluster; Part 8 owns model monitoring.
**Asked at:** Autoscaling write-ups (techinterview.org 'System Design Interview: Kubernetes Autoscaling (HPA, VPA, KEDA, Cluster Autoscaler)', AWS EKS ML inference autoscaling HPA and KEDA guide, CloudNativeNow KEDA articles, dev.to VPA/HPA/KEDA patterns; search snippets only, not opened); editorial and vendor docs, not verified candidate reports; senior MLOps and platform loops
**Say this first (1 line):** Metrics-server gives quick CPU and memory (`kubectl top`), Prometheus scrapes the model's `/metrics`, a GPU exporter such as DCGM gives GPU metrics, and I alert on four signals: latency, errors, saturation and a model-quality proxy.

**Then explain:**
- **Quick look:** `kubectl top pod` needs metrics-server. It shows current usage only, no history, and is what HPA uses for CPU.
- **Prometheus:** the app exposes text at `/metrics` (counters, histograms). A ServiceMonitor (Prometheus Operator CRD) or a scrape config tells Prometheus where to pull. The ServiceMonitor selects the **Service**, and the port is matched by **name**.
- **GPU metrics:** a GPU exporter (NVIDIA DCGM exporter is the common one; check current docs for metric names) exposes utilisation, memory, temperature. Run as a DaemonSet on GPU nodes (see Q34).
- **Dashboards vs alerts:** a dashboard is for looking after something is wrong; an alert is what wakes someone. Alert on symptoms users feel, not on every metric.
- **Four signals for a model service:** latency (p95/p99), error rate, saturation (queue depth, GPU memory, CPU throttling), and a model-quality proxy (score distribution, empty or default outputs, drift flags). Part 8 owns model monitoring.
- **Events and logs:** Kubernetes events expire quickly (about an hour by default, so export them if you need them); pod logs vanish with the pod unless shipped.
- **Failure modes:** averaging latency (hides the tail); a histogram with bad bucket boundaries (p95 jumps); ServiceMonitor label not matching Prometheus' selector so nothing is scraped; alerting on GPU utilisation alone.

**Example:** one scrape of a histogram: cumulative counts 600 (<=0.05s), 850 (<=0.1), 940 (<=0.25), 985 (<=0.5), 1000 total. For p95, rank = 0.95 x 1000 = 950. That falls in the 0.25-0.5 bucket, after 940, so p95 = 0.25 + 0.25 x (950-940)/(985-940) = 0.3056 s. Error ratio: 30 errors of 1000 = 0.03.

**PromQL examples (hedged, not executed):**
```promql
# p95 latency over 5 minutes
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{route="/predict"}[5m])))
# error ratio
sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
# GPU utilisation (DCGM exporter metric name; check current docs)
avg by (pod) (DCGM_FI_DEV_GPU_UTIL)
```

**Code:** a ServiceMonitor sketch and a Python parser for the text format with a histogram quantile, as above.
```yaml
# Prometheus Operator CRD (monitoring.coreos.com/v1). Needs the operator installed: not executed. Check current docs for fields.
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: model-api
  labels: {release: prometheus}      # must match the Prometheus' serviceMonitorSelector
spec:
  selector:
    matchLabels: {app: model-api}    # selects the Service, not the Pods
  endpoints:
  - port: http                       # NAME of the Service port
    path: /metrics
    interval: 15s
```
```python
"""Q38: parse Prometheus text exposition, compute p95 from histogram buckets (same linear interpolation idea as histogram_quantile)
and an error ratio. One scrape, so these are totals since start; PromQL would use rate() over a window."""
import math, pathlib, re

LINE = re.compile(r'^([a-zA-Z_:][a-zA-Z0-9_:]*)(\{[^}]*\})?\s+(\S+)$')
def parse(text):
    out = []
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith("#"): continue
        m = LINE.match(ln.strip())
        if not m: raise ValueError(f"bad line: {ln!r}")
        labels = dict(re.findall(r'(\w+)="([^"]*)"', m.group(2) or ""))
        out.append((m.group(1), labels, float(m.group(3))))
    return out

def quantile(q, buckets):                       # buckets: [(upper_bound, cumulative_count)] sorted
    total = buckets[-1][1]; rank = q * total; prev_b, prev_c = 0.0, 0.0
    for b, c in buckets:
        if c >= rank:
            if math.isinf(b): return prev_b     # in the +Inf bucket: Prometheus returns the highest finite bound
            return prev_b + (b - prev_b) * (rank - prev_c) / (c - prev_c)
        prev_b, prev_c = b, c

s = parse((pathlib.Path(__file__).resolve().parent / "q38_metrics.txt").read_text())
bk = sorted((float("inf") if l["le"] == "+Inf" else float(l["le"]), v) for n, l, v in s if n.endswith("_bucket"))
print(f"samples parsed: {len(s)}")
print(f"p95 latency  : {quantile(0.95, bk):.4f} s")
print(f"p50 latency  : {quantile(0.50, bk):.4f} s")
req = {l["code"]: v for n, l, v in s if n == "http_requests_total"}
print(f"error ratio  : {req['500'] / sum(req.values()):.3f}")
try: parse("this is not a metric line")
except ValueError as e: print("bad input   :", e)
```
```bash
python3 -I q38_parse.py
```

**Output (my run):** the parser ran on a sample file (`code/q38_metrics.txt`); the numbers match the hand calculation. The ServiceMonitor was only parsed with PyYAML: it is a CRD, so `kubernetes-validate` has no schema for it, and Prometheus, PromQL, DCGM and `kubectl top` are **not executed**: no cluster.
```text
samples parsed: 9
p95 latency  : 0.3056 s
p50 latency  : 0.0417 s
error ratio  : 0.030
bad input   : bad line: 'this is not a metric line'
ServiceMonitor {'port': 'http', 'path': '/metrics', 'interval': '15s'}
```

**Follow-ups:**
- *Why not alert on CPU?* For an ML service CPU may be low while the GPU or queue is the bottleneck. Alert on user symptoms plus saturation.
- *Why histograms, not averages?* Averages hide the tail, and histograms from many pods can be summed before taking a quantile.
- *Where do events go?* Ship them to your log store if you need history.

**Common mistakes:** ServiceMonitor selecting Pods not Services; unnamed Service port; alerting on everything; no model-quality signal at all.

---

### Q39 ⭐ 🔴 Design question: an ML platform on Kubernetes for 30 data scientists with 16 shared GPUs. Cover namespaces and quotas per team, a Kueue-style queue or priority classes, GPU node pools with taints, notebook pods with idle culling, a training Job template, KServe or plain Deployments for serving, a shared model registry, a Helm chart per service type, HPA and KEDA rules, and cost visibility. Draw it as a table of components and owners and give a script that checks a team request against its GPU quota. Pure design; nothing is executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** One cluster, a namespace and GPU quota per team, a tainted GPU pool, a queue (Kueue-style) or priority classes for fairness, notebooks that cull when idle, Jobs for training, a Deployment or KServe for serving, and cost visibility per namespace; 16 GPUs for 30 people means sharing and queueing are the design.

**Then explain:**
- **Isolation and fairness:** namespace per team with ResourceQuota on `requests.nvidia.com/gpu`, LimitRange for defaults, RBAC to the team group. A plain quota is a hard cap: no borrowing. Borrowing idle capacity and preemption is what a queue system like Kueue adds (cohorts; check current docs). Without a queue, use PriorityClasses: serving high, training medium, notebooks low.
- **GPU pool:** taint it, so only pods that ask for GPUs land there. Notebooks default to CPU; a GPU notebook is an explicit request with a time limit.
- **Idle culling:** stop notebooks with no activity for N hours, release the GPU, keep the PVC.
- **Training:** a Job template (checkpointing, TTL, resource requests, a queue label). Serving: Deployments with HPA for simple cases, KServe if you want canary and scale-to-zero (check current docs).
- **Shared things:** model registry (one place for versions), Helm chart per service type (training, serving, notebook), HPA and KEDA rules for serving, cost visibility by namespace labels.
- **Failure modes:** one team hoards GPUs by holding idle notebooks; quotas sum above 16 and nobody can run; no preemption so a long job blocks serving; quota set on limits not requests; fragmentation (4 free GPUs spread over 4 nodes cannot run an 8-GPU job).

**Example (components and owners):**

| Component | Purpose | Owner |
|---|---|---|
| Namespaces + ResourceQuota + RBAC | isolation, GPU caps | platform team |
| GPU node pool + taint | keep CPU work off GPUs | platform team |
| Kueue (or PriorityClasses) | queue, fairness, borrowing | platform team |
| Notebook service + culler | interactive work, free idle GPUs | platform team |
| Training Job chart | repeatable training, checkpoints, TTL | ML platform + data scientists |
| Serving chart (Deployment/KServe) + HPA/KEDA | online inference | ML engineers |
| Model registry | versions, stage, lineage | ML platform |
| Cost dashboard | spend by namespace label | platform + finance |

Quota split used in the script: vision 4, nlp 5, speech 3, research 2 = 14 GPUs, leaving 2 as shared reserve. This split is an example, not a recommendation.

**Code:** a ResourceQuota and a script that checks a team's request against quota and cluster capacity. The "borrow" branch models what a Kueue-style queue could allow; a plain ResourceQuota would not.
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: team-vision
spec:
  hard:
    requests.nvidia.com/gpu: "4"
    requests.cpu: "64"
    requests.memory: 256Gi
    persistentvolumeclaims: "20"
```
```python
"""Q39: check a team's GPU request against its quota and the cluster total. Numbers are the design example: 16 GPUs, 4 teams."""
CLUSTER_GPUS = 16
QUOTA = {"team-vision": 4, "team-nlp": 5, "team-speech": 3, "team-research": 2}   # sum 14; 2 left as shared burst/reserve
USED  = {"team-vision": 3, "team-nlp": 5, "team-speech": 0, "team-research": 1}
assert sum(QUOTA.values()) <= CLUSTER_GPUS

def check(team, want, borrow_ok=False):
    if team not in QUOTA: return "DENY: unknown team"
    if want <= 0: return "DENY: request must be positive"
    free_quota = QUOTA[team] - USED[team]
    if want <= free_quota: return f"ADMIT: {want} of {free_quota} free quota GPUs"
    spare = CLUSTER_GPUS - sum(USED.values())          # idle GPUs anywhere
    if borrow_ok and want - free_quota <= spare:
        return f"ADMIT as preemptible: {free_quota} in quota + {want - free_quota} borrowed (spare={spare})"
    return f"QUEUE/DENY: wants {want}, quota free {free_quota} (hard limit {QUOTA[team]})"

for team, want, b in [("team-vision", 1, False), ("team-vision", 2, False), ("team-vision", 2, True),
                      ("team-nlp", 1, False), ("team-nlp", 1, True), ("team-ghost", 1, False), ("team-speech", 0, False)]:
    print(f"{team:14} wants {want} borrow={b!s:5} -> {check(team, want, b)}")
```
```bash
python3 -I q39_check.py
kubernetes-validate --strict q39_quota.yaml
```

**Output (my run):** script and schema validation ran. Kueue, KServe, KEDA, quota enforcement and notebook culling are **not executed**: this is a design question and there is no cluster.
```text
team-vision    wants 1 borrow=False -> ADMIT: 1 of 1 free quota GPUs
team-vision    wants 2 borrow=False -> QUEUE/DENY: wants 2, quota free 1 (hard limit 4)
team-vision    wants 2 borrow=True  -> ADMIT as preemptible: 1 in quota + 1 borrowed (spare=7)
team-nlp       wants 1 borrow=False -> QUEUE/DENY: wants 1, quota free 0 (hard limit 5)
team-nlp       wants 1 borrow=True  -> ADMIT as preemptible: 0 in quota + 1 borrowed (spare=7)
team-ghost     wants 1 borrow=False -> DENY: unknown team
team-speech    wants 0 borrow=False -> DENY: request must be positive
```
```text
INFO q39_quota.yaml passed for resource resourcequota/gpu-quota against version 1.37
```

**Follow-ups:**
- *Time-slicing or MIG to share a GPU?* Time-slicing has no memory or fault isolation; MIG (on supported GPUs) gives hardware isolation. Use for small inference and notebooks; check current docs.
- *How do you stop hoarding?* Quotas, idle culling, a max runtime on GPU notebooks, and a usage report per team.
- *Why a queue, not just quota?* Quota says no; a queue says wait, and lets idle capacity be used.

**Common mistakes:** quota larger than the cluster; no preemption story; GPUs held by idle notebooks; forgetting fragmentation.

---

### Q40 ⭐ 🔴 Cluster upgrade and version-skew questions: why Kubernetes minor versions go out of support quickly (check current docs for the window), API deprecations such as removed beta APIs, running kubectl convert or a validator against manifests before an upgrade, Helm charts pinning old apiVersions, draining nodes, and GPU driver and device plugin compatibility with the new node image. Give a script that scans manifests for a list of removed apiVersions (state which ones as examples, hedged) and validates a manifest against several versions with the kubernetes-validate library, which does run here. The upgrade itself is not executed.
**Asked at:** Expert extension (no source found for this exact question); typical of senior ML engineer and MLOps loops at product companies and GCCs
**Say this first (1 line):** Kubernetes minor versions go out of support quickly, so upgrades are routine; before each one I scan manifests and chart output for removed API versions, validate against the target version, drain nodes carefully, and confirm the GPU driver and device plugin work with the new node image.

**Then explain:**
- **Short support window:** minor releases come several times a year and each is supported for a limited time (check current docs for the window; managed clouds add their own dates). Staying behind means no patches, and skipping minors is not allowed for control planes (upgrade one minor at a time).
- **API removals:** beta APIs get removed. Examples (hedged, from my memory of the deprecation guide, check current docs): `extensions/v1beta1` Ingress (removed in 1.22), `batch/v1beta1` CronJob (1.25), `autoscaling/v2beta1` HPA (1.25), `autoscaling/v2beta2` HPA (1.26), `policy/v1beta1` PodSecurityPolicy (1.25). Apply of an old manifest then fails after the upgrade.
- **Before the upgrade:** render Helm charts to YAML and scan it; run a validator against the target version; look for old apiVersions in charts you pinned and fix or bump the chart; also check stored objects and clients (CI scripts, operators) that still call old APIs.
- **Nodes:** upgrade the control plane first, then nodes (kubelet may be at most a few minors behind; check the version skew policy). Drain a node: cordon it, evict pods respecting PodDisruptionBudgets, upgrade or replace the node, uncordon. Training pods without checkpoints lose work on drain.
- **GPU stack:** a new node image can bring a different kernel and driver. Check that the driver, container toolkit and device plugin (or GPU Operator) versions support it, test on one canary node, and keep the old image to roll back.
- **Failure modes:** a chart with an old apiVersion fails at install after the upgrade; PDB with `maxUnavailable: 0` blocks drain forever; drain kills a long training job; GPU nodes come back without `nvidia.com/gpu` capacity.

**Example:** the file below has an HPA at `autoscaling/v2beta2` and a CronJob at `batch/v1beta1`. Scan says: both removed (1.26 and 1.25 in my table). The validator agrees: the CronJob has no schema from 1.25 onward, while the HPA validates against 1.25 but not against 1.26 or 1.37. The fix is to move to `autoscaling/v2` and `batch/v1`, and re-validate.

**Code:** a removed-API scanner plus a strict multi-version validation through the `kubernetes_validate` Python API. The removal table is only examples. The bundled schemas here cover 1.25 to 1.37; 1.24 raised an `IndexError` when I tried it, so I left it out.
```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata: {name: model-api}
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: model-api}
  minReplicas: 1
  maxReplicas: 4
  metrics:
  - type: Resource
    resource: {name: cpu, target: {type: Utilization, averageUtilization: 70}}
---
apiVersion: batch/v1beta1
kind: CronJob
metadata: {name: nightly-train}
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers:
          - {name: t, image: "registry.example.com/train:1.0"}
```
```python
"""Q40: (1) scan manifests for apiVersion/kind pairs that were removed in some Kubernetes release;
(2) validate a manifest against several versions with the kubernetes-validate Python API.
The removal table holds EXAMPLES from memory of the official deprecation guide: check current docs before relying on it."""
import pathlib, sys, yaml
import kubernetes_validate

REMOVED = {   # (apiVersion, kind or '*') -> (removed in, use instead)
 ("extensions/v1beta1", "Ingress"):          ("1.22", "networking.k8s.io/v1"),
 ("networking.k8s.io/v1beta1", "Ingress"):   ("1.22", "networking.k8s.io/v1"),
 ("batch/v1beta1", "CronJob"):               ("1.25", "batch/v1"),
 ("autoscaling/v2beta1", "HorizontalPodAutoscaler"): ("1.25", "autoscaling/v2"),
 ("autoscaling/v2beta2", "HorizontalPodAutoscaler"): ("1.26", "autoscaling/v2"),
 ("policy/v1beta1", "PodDisruptionBudget"):  ("1.25", "policy/v1"),
 ("policy/v1beta1", "PodSecurityPolicy"):    ("1.25", "(no replacement object: use Pod Security Admission)"),
 ("flowcontrol.apiserver.k8s.io/v1beta2", "*"): ("1.29", "flowcontrol.apiserver.k8s.io/v1"),
}

def scan(path):
    hits = []
    for d in yaml.safe_load_all(path.read_text()):
        if not isinstance(d, dict): continue
        key = (d.get("apiVersion"), d.get("kind"))
        hit = REMOVED.get(key) or REMOVED.get((key[0], "*"))
        if hit: hits.append((d["kind"], d["metadata"]["name"], key[0], *hit))
    return hits

root = pathlib.Path(__file__).resolve().parent / "q40_manifests"
print("== removed-API scan")
found = 0
for f in sorted(root.glob("*.yaml")):
    for kind, name, api, rem, use in scan(f):
        found += 1; print(f"{f.name}: {kind}/{name} uses {api}, removed in {rem}, use {use}")
print(f"{found} problem(s)")

print("\n== kubernetes-validate (strict) per version")
for f in ("ok_deploy.yaml", "old_hpa_cronjob.yaml", "old_ingress.yaml"):
    docs = [d for d in yaml.safe_load_all((root / f).read_text())]
    for ver in ("1.25", "1.26", "1.37"):
        for d in docs:
            try:
                kubernetes_validate.validate(d, ver, strict=True)
                r = "ok"
            except kubernetes_validate.SchemaNotFoundError:
                r = "no schema in that release (API removed or unknown)"
            except kubernetes_validate.ValidationError as e:
                r = "INVALID: " + str(e).splitlines()[0][:70]
            except Exception as e:
                r = type(e).__name__
            print(f"{f:22} {d['kind']:24} v{ver:5} {r}")
```
```bash
python3 -I q40_scan.py
kubernetes-validate --strict q40_manifests/ok_deploy.yaml
# not executed (no cluster, no kubectl): kubectl drain NODE --ignore-daemonsets --delete-emptydir-data
```

**Output (my run):** the scan and the multi-version validation ran (kubernetes-validate 1.37.0). The upgrade, drain, GPU driver and device plugin checks are **not executed**: no cluster, no kubectl, no GPU.
```text
== removed-API scan
old_hpa_cronjob.yaml: HorizontalPodAutoscaler/model-api uses autoscaling/v2beta2, removed in 1.26, use autoscaling/v2
old_hpa_cronjob.yaml: CronJob/nightly-train uses batch/v1beta1, removed in 1.25, use batch/v1
old_ingress.yaml: Ingress/model-api uses extensions/v1beta1, removed in 1.22, use networking.k8s.io/v1
3 problem(s)

== kubernetes-validate (strict) per version
ok_deploy.yaml         Deployment               v1.25  ok
ok_deploy.yaml         Deployment               v1.26  ok
ok_deploy.yaml         Deployment               v1.37  ok
old_hpa_cronjob.yaml   HorizontalPodAutoscaler  v1.25  ok
old_hpa_cronjob.yaml   CronJob                  v1.25  no schema in that release (API removed or unknown)
old_hpa_cronjob.yaml   HorizontalPodAutoscaler  v1.26  no schema in that release (API removed or unknown)
old_hpa_cronjob.yaml   CronJob                  v1.26  no schema in that release (API removed or unknown)
old_hpa_cronjob.yaml   HorizontalPodAutoscaler  v1.37  no schema in that release (API removed or unknown)
old_hpa_cronjob.yaml   CronJob                  v1.37  no schema in that release (API removed or unknown)
old_ingress.yaml       Ingress                  v1.25  no schema in that release (API removed or unknown)
old_ingress.yaml       Ingress                  v1.26  no schema in that release (API removed or unknown)
old_ingress.yaml       Ingress                  v1.37  no schema in that release (API removed or unknown)
```
```text
INFO q40_manifests/ok_deploy.yaml passed for resource deployment/model-api against version 1.37
```

**Follow-ups:**
- *`kubectl convert`?* It is a separate plugin that rewrites old manifests to a newer apiVersion; check current docs. Not available here.
- *Helm releases with removed APIs?* The release stored in the cluster can reference removed kinds; a Helm plugin or manual edit is needed (check current docs). Better to fix before upgrading.
- *How do you reduce risk?* Staging cluster first, canary node pool, backups, and a rollback plan for node images.

**Common mistakes:** testing only the raw YAML and not the rendered chart; skipping a minor; draining GPU nodes with no checkpointing; assuming the GPU driver is unchanged in the new image.

---

