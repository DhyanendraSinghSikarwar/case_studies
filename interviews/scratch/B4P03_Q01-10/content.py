# Prose for Q1-Q10. Headings and Asked-at lines are copied by build.py from the part file.
C = {}

C[1] = dict(
say="A Pod runs your container, a ReplicaSet keeps N identical pods alive, a Deployment owns the ReplicaSet and handles rollouts, and a Service gives all those pods one stable address by matching their labels.",
explain="""- **Who does what.** Pod = one or more containers sharing network and storage; it is disposable and has a new IP each time. ReplicaSet = 'keep exactly 3 pods with these labels'. Deployment = owns ReplicaSets, one per version, and moves between them on a rollout or rollback. Ownership chain: Deployment owns ReplicaSet owns Pods (visible in `ownerReferences`).
- **Why not a bare Pod.** A bare pod has no controller. If it crashes past restart policy, or its node dies, nobody recreates it. A Deployment pod gets replaced, and you get rolling updates and rollback for free.
- **Delete one pod.** The ReplicaSet sees 2 of 3, creates a new pod with a new name and a new IP. The Service drops the dead pod from its endpoints and adds the new one when it is Ready, so clients keep using the same address.
- **Service = label selector, not a list of pods.** `selector: app=ml-api` picks every Ready pod with that label. ClusterIP: virtual IP reachable inside the cluster only (default). NodePort: opens the same port on every node. LoadBalancer: asks the cloud for an external load balancer (check your cloud's docs for cost and behaviour).
- **Failure modes.** Selector typo or a label missing on the pod template: the Service has zero endpoints, requests hang or are refused, and YAML validation still passes. `targetPort` pointing at the wrong port: same symptom. Readiness probe missing: traffic reaches pods that are still loading the model. Changing a Deployment's `spec.selector` after creation is rejected (immutable).""",
example="""Deployment asks for 3 replicas, labels `app=ml-api`. Pods: a, b, c. You delete b.
- Right after: 2 pods exist, desired 3, so the ReplicaSet creates d. End state: a, c, d. Count is 3 again, names differ.
- The Service selector `app=ml-api` matches the template labels `app=ml-api, version=v1` (a selector only needs to be a subset of the pod labels). Service port 80 forwards to the container port named `http` (8000).
- The scripts below check that match, run `kubernetes-validate --strict`, and replay the delete in a toy reconcile loop.""",
notexec="Not executed here: `kubectl apply`, `kubectl get pods`, `kubectl delete pod`, and `kubectl get endpoints` (no cluster, no kubectl in this sandbox). What did run: schema validation of the manifest (kubernetes-validate 1.37.0, `--strict`, which rejects unknown fields; it checks schema only, not whether the image exists or the Service finds pods), my own label/port cross-check, and the toy ReplicaSet loop (a model of the idea, not the real controller).",
follow=[("What does `kubectl delete deployment` do to the pods?","It deletes the Deployment; the garbage collector removes its ReplicaSets and pods through the owner references. The Service stays, with no endpoints."),
("Why does the Service keep working while pods change IP?","It tracks labels, not IPs. The endpoint list is rebuilt as pods become Ready or go away."),
("When would you use a StatefulSet instead?","When each replica needs a stable identity or its own disk. A stateless model API does not.")],
mistakes="""- Creating bare Pods for a service and wondering why nothing restarts them on node loss.
- Labels on the Deployment object but not on the pod template; the Service matches pod labels only.
- Assuming validation success means the Service works. Schema validation cannot see an empty endpoint list.
- Exposing every model API with `LoadBalancer`; one Ingress or gateway in front is usually cheaper and cleaner (check current docs).""",
)

C[2] = dict(
say="Requests are what the scheduler reserves for placement, limits are what the kubelet and kernel enforce at run time: CPU over the limit is throttled, memory over the limit is killed.",
explain="""- **Requests = scheduling.** The scheduler adds up requests of pods already on a node and places a new pod only where the sum fits. Requests do not cap usage. They also drive HPA CPU utilisation and give a minimum CPU share under contention.
- **Limits = enforcement.** CPU limit becomes a CFS quota (for example 2 CPUs = 200 ms of CPU time per 100 ms period); beyond that the container waits, so latency goes up but nothing dies. Memory cannot be 'paused': past the limit the kernel's OOM killer ends the process (exit 137, `OOMKilled`).
- **QoS classes.** Guaranteed: every container has cpu and memory, requests equal to limits. BestEffort: nothing set at all. Burstable: everything else (for example memory limit only, or request below limit). Under node memory pressure the kubelet evicts BestEffort first, then Burstable pods using more than they requested, and Guaranteed last (the exact ranking also looks at usage over request and priority; check current docs).
- **Requests too high:** pods sit Pending, nodes look 'full' while real usage is low, money wasted. **Too low:** many pods packed on one node, noisy neighbours, CPU starvation, evictions when the node runs short.
- **Failure modes for ML.** Memory limit set to the model size only: load spikes, copies and request buffers push you over, OOMKilled. Tiny CPU limit on a model server: every request is slow because of throttling, yet CPU graphs look 'fine'. Many teams set a memory limit equal to the request and avoid a tight CPU limit; that is a policy choice, so state your reason.""",
example="""Model file is 2 GB in memory. Pick memory request = limit = 3Gi (2 GB weights + about 1 GB for runtime, tensors, request buffers). CPU request 1, limit 2.
- Requests and limits differ for CPU, so QoS is **Burstable**, even though memory is equal.
- To get **Guaranteed**, make CPU request = limit = 2 (second pod in the file). Cost: you reserve 2 CPUs always.
- A pod with no `resources` is **BestEffort** and is first to go under pressure.
- 3 pods x 3Gi memory request = 9Gi must fit in node allocatable memory (less than the node's total, after OS and kubelet reserve) or one pod stays Pending.""",
notexec="Not executed: applying the manifests, `kubectl describe pod` (which prints the QoS Class line), and any eviction. What ran: kubernetes-validate 1.37.0 with `--strict` on all three objects, and my `qos.py`. The validator does not catch a junk quantity (a string such as `x` passes the schema), so `qos.py` parses quantities itself and checks request <= limit. The classifier follows the documented rule for regular containers; it ignores init containers, pod-level resources and the eviction ranking details.",
follow=[("Why is CPU throttled and memory killed?","CPU is compressible: you can give a process less time. Memory is not: you cannot take back pages in use without losing data, so the kernel kills."),
("Should I set CPU limits?","Debated. Limits can throttle bursty servers. Many platforms set requests and a memory limit but no CPU limit. Pick one, explain it, and check your cluster's policy."),
("What is LimitRange for?","Namespace defaults and min/max per container, so pods without resources do not become BestEffort by accident.")],
mistakes="""- Requests copied equal to limits everywhere 'to be safe': over-reserves nodes.
- No memory limit on a Python server with a growing cache: it takes the node down instead of itself.
- Memory in `M` vs `Mi`: `500M` is 500 million bytes, `500Mi` is 524,288,000 bytes. Quantity typos pass schema validation.
- Reading `top` CPU graphs for a throttled pod and concluding it is idle.""",
)

C[3] = dict(
say="I go get pods, then describe pod for last state, exit code and events, then logs and logs --previous, and I let the exit code and the last log line pick the cause.",
explain="""- **Order.** 1) `kubectl get pod` (restarts, status). 2) `kubectl describe pod` (Last State: Terminated, Reason, Exit Code; Events at the bottom: probe failures, pull errors, OOM). 3) `kubectl logs <pod>` for the current attempt, then `kubectl logs <pod> --previous` for the one that just died, since the current container may have no output yet. 4) Only then guess: reproduce the image locally with `docker run`.
- **Backoff.** Kubelet restarts a failing container with delays that double from about 10 s to a cap of about 5 minutes (check current docs); it resets after the container runs cleanly for a while. So a pod that crashes in a second shows long gaps between attempts, and 'Running' for a moment can be a lie.
- **Exit codes.** 1 = app error (read the log). 127/126 = command not found / not executable (entrypoint). 137 = SIGKILL (OOMKilled, or killed by liveness/eviction). 143 = SIGTERM. 0 on a Deployment pod still loops, because Deployments expect the container to keep running.
- **Usual ML causes.** Model file missing (wrong mount path, init download failed). Wrong command or args. Import error (dependency missing in image). Bad env var or missing Secret/ConfigMap (that shows as `CreateContainerConfigError`, not a crash). Liveness probe killing a container that is still loading weights. OOM while loading the model.
- **Failure modes of the debugging itself.** Reading only current logs (empty because it just restarted). Deleting the pod, which wipes the evidence of Last State. Assuming 137 always means OOM: check the Reason line.""",
example="""Table below. Then the script reads six sample pod-status records and prints the next step for each. Backoff by hand: 10, 20, 40, 80, 160, 300, 300, 300 = 1210 s of waiting over 8 restarts.

| Symptom (describe / logs) | Likely cause | Next command |
|---|---|---|
| Exit 1, `FileNotFoundError` model path | model not mounted or download failed | `kubectl describe pod` (volumes), check init container logs, `kubectl exec` on a debug pod to `ls` the path |
| Exit 137, Reason OOMKilled | memory limit too low | `kubectl top pod` (needs metrics-server), raise limit, see Q4 |
| Exit 137, Reason Error, Events: liveness probe failed | liveness kills slow loader | add startupProbe, see Q6 |
| Exit 127 / `executable file not found` | wrong command or args | compare `spec.containers[].command` with image CMD |
| Exit 1, `ModuleNotFoundError` | dependency missing in image | `docker run --rm image python -c "import torch"`, rebuild |
| `CreateContainerConfigError` | Secret/ConfigMap name or key missing | `kubectl get secret,configmap -n ns`, fix reference |""",
notexec="Not executed: every `kubectl` command here (no cluster, no kubectl). What ran: `triage.py` over sample JSON that I wrote in the shape of `kubectl get pod -o json` status fields (not captured from a real cluster), so it shows the decision logic, not real kubectl output. The backoff numbers follow the documented doubling to a 5-minute cap; confirm in current docs for your version.",
follow=[("Pod shows Running but restarts keep climbing?","The container starts, runs a bit, then dies. Use `logs --previous` and the Last State exit code. Restart count is the signal, not status."),
("Logs are empty with --previous?","The process died before writing. Check entrypoint, config errors and OOM at start; run the image locally with the same env."),
("How do you debug if the image has no shell?","`kubectl debug` with an ephemeral container (check your cluster version) or run the same image locally with an overridden entrypoint.")],
mistakes="""- Running `kubectl delete pod` first and losing Last State and the previous logs.
- Treating CrashLoopBackOff as the cause. It is the symptom; the cause is in the exit code, the logs and the events.
- Raising memory blindly for exit 137 without checking the Reason (OOMKilled versus liveness kill).
- Forgetting `-c <container>` when the pod has sidecars.""",
)

C[4] = dict(
say="Container OOMKilled means that one container hit its own memory limit and the kernel killed it (exit 137); Evicted means the node itself was short of memory and the kubelet chose to remove a pod.",
explain="""- **Two different events.** Cgroup OOM: the limit belongs to the container; the pod stays on the node, the container restarts (`Last State: Terminated, Reason: OOMKilled`). Node-pressure eviction: kubelet sees low node memory, picks pods (those using more than their request first), and the whole pod ends up `Failed` with `Reason: Evicted`; a controller makes a new pod elsewhere. There can also be a kernel-level OOM on the node outside the kubelet's eviction, so check node events too.
- **Tell them apart.** `kubectl describe pod`: `OOMKilled` under Last State versus pod Status `Failed`, Reason `Evicted`, message 'The node was low on resource: memory'. Fix for the first: limit or usage. Fix for the second: requests honest, node sizes, fewer BestEffort pods.
- **Why Python ML services blow their limit.** Batch size (tensors scale with it). Several gunicorn/uvicorn workers each loading their own copy of the model. pandas creating copies on merge or `astype`. Pinned (page-locked) memory. Dataloader workers and `/dev/shm` shared memory for PyTorch (the default pod shared memory is small; an `emptyDir` with `medium: Memory` counts against the memory limit). Memory that is mapped but not freed because of fragmentation.
- **Choosing a limit.** Observe the working set over a realistic period including the load phase and the biggest request; set request near a high percentile, set the limit at observed peak plus headroom, then watch for OOM. Do not size from an average.
- **Failure modes.** Raising the limit hides a leak (usage keeps climbing until the new limit). Limit larger than any node can give: pod Pending forever. Memory limit below the model size: dies at start, looks like CrashLoopBackOff.""",
example="""20 working-set samples in MiB: sixteen at 1500, then 1600, 1650, 1700, 1800.
- p95 = the 19th of 20 sorted values = 1700. Peak = 1800.
- Request = 1700 rounded up to a multiple of 64 = 1728 MiB (27 x 64).
- Limit = 1800 x 1.25 = 2250, rounded up to 2304 MiB (36 x 64).
- Worker trap: a 2048 MiB model with 4 workers that each load it is 8192 MiB; loaded once and shared it is 2048 MiB. (Sharing through fork and copy-on-write is fragile in Python because reference counting touches pages, so do not count on it; one worker per pod with more replicas is the simpler fix.)""",
notexec="Not executed: `kubectl describe pod`, `kubectl top pod` and a real OOM. What ran: `oom.py` on sample pod-status JSON I wrote (the Evicted message text follows the format Kubernetes documents, but these are not captured from a cluster), the sizing function and the worker arithmetic. The headroom factor (25 percent) and the 95th percentile are my example choices, not a standard.",
follow=[("Does a memory request protect me from OOM?","No. Only the limit triggers the container OOM kill. The request affects scheduling and eviction order."),
("Pod OOMs only at start?","Peak during model load (read file plus build tensors). Size for the load peak, or load in a streaming way, or use a bigger limit only during startup via an init step."),
("How do I stop dataloader shared-memory crashes?","Mount an `emptyDir` with `medium: Memory` at `/dev/shm` and count its size in the limit (check your runtime's behaviour).")],
mistakes="""- Reporting 'OOM' for both events. Eviction is a node decision.
- Sizing the limit from the average.
- Forgetting that tmpfs `emptyDir` and page cache-heavy file reads can count toward the container's memory.
- Setting the JVM or Python worker count from the node's CPUs instead of the pod's limit.""",
)

C[5] = dict(
say="Pending means the scheduler could not place the pod, so I read the FailedScheduling event in describe pod: it says how many nodes failed for each reason, and I fix the biggest reason.",
explain="""- **Order I check.** 1) Event text (`kubectl describe pod`, Events). 2) Resources: Insufficient cpu, memory or `nvidia.com/gpu`. 3) Taints without tolerations. 4) nodeSelector or affinity that matches no node. 5) PVC unbound (StorageClass, zone). 6) Pod-count cap ('Too many pods'). 7) Quota: if a ResourceQuota blocks you, the **pod is never created**: look at the ReplicaSet events (`FailedCreate ... exceeded quota`), not at a Pending pod.
- **Reading the message.** `0/5 nodes are available: 3 Insufficient nvidia.com/gpu, 2 node(s) had untolerated taint ...`. The 0/5 says no node passed. The numbers after it sum to the node count: each node is listed once under the first filter it failed. Wording varies by Kubernetes version, so read, do not pattern-match blindly.
- **Eligibility, not capacity.** Often the cluster has room but your pod is not allowed on those nodes (taints, selector, zone of the PVC). Adding nodes does not fix that.
- **Image problems are not Pending.** A pod that was scheduled and cannot pull its image shows `ErrImagePull` / `ImagePullBackOff` (status Pending phase but the node is chosen). Check events for 'Successfully assigned' to separate the two.
- **Failure modes.** Cluster autoscaler adds nothing because the pod can never fit any node shape (request bigger than the largest node, or GPU label wrong). A GPU pod Pending forever because the GPU nodes are tainted and the pod has no toleration.""",
example="""Message: `0/5 nodes are available: 3 Insufficient nvidia.com/gpu, 2 node(s) had untolerated taint {nvidia.com/gpu: present}.`
- 3 + 2 = 5 nodes. Three nodes have GPUs but all in use; two nodes are tainted and the pod does not tolerate. Next step: free or add GPUs, and check whether your toleration key matches the taint (Q8).
- Second example in the file: `4 node(s) didn't match Pod's node affinity/selector` means a label problem; no amount of capacity helps.""",
notexec="Not executed: `kubectl get pod`, `describe pod`, `get events`, `get pvc`, and any scheduling. What ran: `pending.py` on five message strings I wrote in the format the scheduler documents (not captured from a cluster). Message wording changes between Kubernetes versions, so this parser is a teaching sketch; a production tool should use structured events.",
follow=[("Pod is Pending but the node has free CPU?","Look for taints, selectors, unbound PVC, or pod anti-affinity. Free CPU is irrelevant if the pod is not eligible."),
("How does cluster autoscaler react to Pending pods?","It scales up only for pods that could fit on a new node of a configured group. Pods blocked by selectors that no group satisfies stay Pending (check your autoscaler's docs)."),
("What if the PVC is bound to a zone with no GPU nodes?","The pod is Pending with a volume node-affinity conflict. Use a StorageClass with delayed binding or put the pool in that zone.")],
mistakes="""- Calling ImagePullBackOff 'Pending'.
- Adding nodes for a taint or label problem.
- Looking for a pod when a quota rejection means none was created.
- Quoting a single event string as if wording were stable across versions.""",
)

C[6] = dict(
say="Liveness asks 'is the process stuck, restart it', readiness asks 'can it serve right now, send traffic or not', and a startup probe holds the other two off until the slow model load is done.",
explain="""- **What a failure does.** Liveness fails: kubelet restarts the container. Readiness fails: the pod is removed from Service endpoints, nothing restarts. Startup fails past its budget: container is restarted; while startup has not succeeded, liveness and readiness do not run.
- **Liveness must be cheap and local.** Check that the process answers (`/healthz`). If liveness also checks 'model loaded', then during a 90 s load it fails, gets killed at about the third miss, restarts, loads again, fails again: a restart loop that never serves.
- **Readiness checks usefulness.** `/ready` returns 200 only when weights are in memory and, if you can afford it, a tiny dummy prediction works. Before that, 503, so no traffic. A shallow readiness (just 'port open') sends traffic to a pod that will fail requests. Do not make readiness depend on a downstream database you share: one outage then removes every pod and widens the incident.
- **Size the startup probe.** Budget = `failureThreshold x periodSeconds` (plus initial delay). It must beat the worst-case load, not the average: loads slow down when many pods pull weights together or the disk is cold. Rule I use: worst case x 1.5.
- **Failure modes.** Startup budget too small: restart loop. Probe `timeoutSeconds` shorter than a GC pause or a busy worker: false restarts. Probing an endpoint that runs inference on the same thread: probes queue behind real traffic.""",
example="""Worst-case load 90 s, probe period 5 s, safety x1.5 = 135 s, so failureThreshold >= 27. The YAML uses 36 (budget 180 s).
- Timeline of the bad design (liveness checks the model, first probe at 10 s, period 10 s, 3 failures): restarts at t = 30, 60, 90, 120... the model needs 90 s but gets only 30 s per life, so it never gets healthy. The script reproduces these times.
- Good design: startup (budget 180 s) holds liveness off; `/healthz` is always 200; `/ready` flips from 503 to 200 once loading ends.""",
notexec="Not executed: kubelet probe behaviour, restarts and endpoint removal (no cluster). What ran: kubernetes-validate 1.37.0 `--strict` on the Deployment; the budget arithmetic; the restart timeline (a simulation of my reading of the probe rules); and a real local HTTP server with a loading flag, polled with urllib (1 s load stands in for 90 s). The server is a stdlib sketch, not a production server.",
follow=[("Do I still need a readiness probe if I have a startup probe?","Yes. Startup only guards boot. Readiness keeps working all life long, for example when a worker is overloaded or the model reloads."),
("Why not a long `initialDelaySeconds`?","It is a fixed guess: slow loads still fail, fast loads wait for nothing. Startup probes poll and finish as soon as the app is up."),
("What about graceful shutdown?","Separate topic (SIGTERM, preStop, terminationGracePeriodSeconds): readiness should go false first so the pod drains.")],
mistakes="""- One `/health` endpoint used for liveness and readiness.
- Liveness that calls the model or the database.
- Startup budget sized for the average load time.
- Probe port or path typo: every pod restarts. Schema validation cannot catch it.""",
)

C[7] = dict(
say="ConfigMaps hold non-secret settings, Secrets hold credentials, both reach the pod as env vars or mounted files, and base64 in a Secret is only encoding, so you protect Secrets with RBAC, encryption at rest and an external secret manager.",
explain="""- **What goes where.** ConfigMap: model URI, thresholds, log level, feature flags. Secret: API keys, registry credentials, database passwords, tokens. If a leak would hurt, it is a Secret.
- **Env var vs file.** Env vars are read once at container start; changing the ConfigMap does **not** restart pods and running pods keep the old values. Mounted ConfigMap files are refreshed by the kubelet after a delay (not for `subPath` mounts, and your app must re-read the file). Env is simple; files suit big or changing configs.
- **Rolling on change.** Put a hash of the config in a pod-template annotation (`checksum/config`). Config changes, hash changes, template changes, Deployment rolls. Helm charts do this with a `sha256sum` template function; or run `kubectl rollout restart` (not executed here).
- **Secrets are base64, not encrypted.** Anyone who can `get` the Secret can decode it (the script shows it). Real protection: RBAC that limits who can read Secrets (including list and watch, and the ability to create pods that mount them), encryption at rest in etcd (a cluster setting; check your platform), and external managers (a cloud secrets service or Vault, synced by a CSI driver or operator; check current docs). Never commit Secret YAML with real values to git.
- **Failure modes.** Missing key or object: pod stuck in `CreateContainerConfigError`. Secret in an env var can leak through crash dumps, logs of `env`, or child processes. A ConfigMap above about 1 MiB is rejected: do not store models in it.""",
example="""ConfigMap `THRESHOLD: "0.62"`. The Deployment reads it with `envFrom`.
- Edit it to "0.70": running pods still use 0.62 (env is fixed at start).
- The hash of the config data changes (00131ed2432d8c33 becomes 8be2d7a7357668d7 in the output), the annotation changes with it, so the pod template changes and a rollout starts. Same data in a different key order gives the same hash because the script sorts keys.
- The dummy token `bm90LWEtcmVhbC10b2tlbg==` decodes to `not-a-real-token`: one line of Python, no key needed.""",
notexec="Not executed: applying, `kubectl rollout restart`, kubelet file refresh, etcd encryption, external secret managers. What ran: kubernetes-validate 1.37.0 `--strict` on the manifest and on the regenerated manifest with the new annotation, base64 decoding, and the hash demo. The value in the Secret is a dummy.",
follow=[("Is `stringData` safer than `data`?","No. It is a write convenience; the stored result is the same base64."),
("How do you rotate a secret without downtime?","Update the Secret and roll pods with the same hash trick or an external-secret operator, keeping old and new credentials valid during the overlap."),
("ConfigMap vs baking config into the image?","ConfigMap lets one image run in dev and prod with different settings; baked config means a rebuild per change. Keep secrets out of images either way.")],
mistakes="""- Saying 'Secrets are encrypted'.
- Expecting pods to pick up a changed env ConfigMap.
- Putting real keys in a values file or manifest in git.
- Granting wide `get secrets` rights to CI service accounts.
- Using `subPath` and expecting live updates.""",
)

C[8] = dict(
say="The device plugin advertises GPUs as the extended resource nvidia.com/gpu, you ask for whole GPUs under limits, the GPU nodes are tainted so ordinary pods stay off, and your pod carries a toleration plus a nodeSelector to land there.",
explain="""- **Device plugin.** A DaemonSet (often installed by the NVIDIA GPU Operator) runs on GPU nodes and tells the kubelet how many `nvidia.com/gpu` the node has. The scheduler then treats that like any other countable resource. Versions and install methods change: check current NVIDIA docs.
- **Limits, whole numbers.** Extended resources cannot be overcommitted: you write them under `limits` (a request, if set, must equal the limit; if only limit is set, request defaults to it). Only integers: `0.5` is invalid. Sharing one GPU needs time-slicing (no memory or fault isolation between pods) or MIG (hardware partitions with their own resource names such as `nvidia.com/mig-1g.10gb`), both configured by the platform.
- **Taints keep the pool clean.** A taint such as `nvidia.com/gpu=present:NoSchedule` stops web pods and cron jobs from occupying expensive nodes. Many managed Kubernetes offerings add this taint to GPU pools by themselves (check yours).
- **Steering.** Toleration says 'I am allowed there'. It does not attract the pod. A nodeSelector or node affinity says 'I want nodes with this label'. For GPU pods you want both, plus the GPU resource request, which itself already limits placement to nodes that advertise GPUs.
- **Failure modes.** Toleration key typo: pod Pending with 'untolerated taint'. Label missing: Pending with 'didn't match node selector'. GPU requested but driver or plugin pod not running: node shows 0 GPUs, Pending 'Insufficient nvidia.com/gpu'. A tolerating CPU-only pod can still land on a GPU node, because a toleration does not require a GPU.""",
example="""Node `gpu-node-1` has taint `nvidia.com/gpu=present:NoSchedule` and label `pool=gpu`.
- Pod has toleration `key nvidia.com/gpu, operator Exists, effect NoSchedule`: tolerated. With `Exists` the value is ignored.
- `spot-gpu-2` also carries a `spot=true:NoSchedule` taint: **every** NoSchedule taint must be tolerated, so this pod is blocked by `spot`.
- `PreferNoSchedule` is a soft hint, so it does not block.
- The script also rejects `0.5` GPUs and a GPU only in requests.""",
code_note="Node taint and label commands (not executed): `kubectl taint nodes gpu-node-1 nvidia.com/gpu=present:NoSchedule` and `kubectl label nodes gpu-node-1 pool=gpu`.",
notexec="Not executed: tainting nodes, the device plugin, any GPU scheduling (no GPU and no cluster here). What ran: kubernetes-validate 1.37.0 `--strict` on the Deployment (note: it accepts `nvidia.com/gpu: 1` because extended resource names are free text), and `tolerates.py`, which implements the documented toleration rules for NoSchedule/NoExecute and my GPU-field checks. It ignores `tolerationSeconds`.",
follow=[("Can two pods share one GPU?","Not with the default plugin. Use time-slicing (no isolation) or MIG on supported GPUs, set up by the platform team; check current NVIDIA docs."),
("Why does my CPU-only pod run on a GPU node?","It tolerates the taint (or the pool has none). Taints repel; they do not reserve. Add node affinity away from GPU nodes for those pods."),
("How do you scale GPU nodes to zero?","Cluster autoscaler or Karpenter-style tools on a GPU pool; cold start includes node boot, driver and image pull (check provider docs).")],
mistakes="""- Putting `nvidia.com/gpu` only under requests, or asking for a fraction.
- Toleration without a nodeSelector or GPU request: pod may land on a CPU node (if untainted) or not at all.
- Forgetting that a taint on the node with `effect: NoExecute` also evicts running pods.
- Assuming the cloud adds the taint, then discovering web pods eating GPU nodes.""",
)

C[9] = dict(
say="HPA computes desired replicas = ceil(current replicas x current metric / target metric), clamps it between min and max, ignores small deviations, and scales down slowly with a stabilisation window.",
explain="""- **Formula.** `desired = ceil(current x currentMetric / targetMetric)`. If the ratio is within a tolerance of 1.0 (default 10 percent; check your version) nothing changes. Result is clamped to `minReplicas`..`maxReplicas`. The controller syncs about every 15 s by default (cluster setting).
- **Requests must exist.** CPU Utilization is usage divided by the container's **request**. No request, no percentage: the HPA reports unknown and does nothing. Pods with several containers: every container needs a request. Also needs metrics-server (or another metrics API provider); without it you see `<unknown>` targets.
- **Behaviour block.** `scaleUp` can be quick (no wait, double each minute in the example). `scaleDown` uses a stabilisation window: it picks the highest recommendation over the window (300 s here), so a short dip does not kill pods you will need again. `policies` cap how many pods or what percent can change per period.
- **Why CPU is a poor signal for model servers.** A GPU-bound model can be saturated at low CPU. A queue-bound or batching server has latency growing while CPU is flat. Cold starts are slow, so reacting late hurts. Better signals: requests in flight, queue length, GPU utilisation, or latency, via custom/external metrics or KEDA (see the autoscaling Qs in this part).
- **Failure modes.** Request set too low: utilisation reads 300 percent and HPA hits max. Not-ready pods and fresh pods are treated specially (pods without metrics are treated conservatively, which damps the change; check the HPA docs for details). HPA and a manually set `replicas` in the Deployment fight each other on every apply. Max replicas larger than quota or GPU capacity: new pods Pending.""",
example="""By hand: 4 pods at 90 percent, target 60 percent. Ratio 1.5, 4 x 1.5 = 6, so desired 6 (inside min 2..max 10).
- 4 pods at 63 percent: ratio 1.05, inside the 10 percent dead band, stay at 4.
- 8 pods at 150 percent: raw 20, capped at 10.
- 4 pods at 10 percent: raw 1, floor 2.
- Time series in the output: a spike to 6 cores of demand takes the pods to 10; when demand drops to 1.2 cores the recommendation is 2 at once, but replicas stay at 10 until the 5-step window forgets the high values. The simulation's step is abstract (not 15 s), and it leaves out the scaleDown `policies` limit and pod start-up time.""",
notexec="Not executed: the real HPA, metrics-server, and applying the manifest (no cluster). What ran: kubernetes-validate 1.37.0 `--strict` on the Deployment and the `autoscaling/v2` HPA, and `hpa_sim.py`, my model of the documented formula, tolerance, clamp and a simplified window. It is a teaching model; the real controller has more rules (readiness handling, multiple metrics, policies).",
follow=[("HPA vs VPA vs cluster autoscaler?","HPA changes replica count. VPA changes requests and limits (often needs pod restarts; do not run it on the same CPU/memory metric as HPA). Cluster autoscaler adds or removes nodes for Pending pods."),
("Can HPA scale to zero?","Not in the standard setup (minReplicas must be 1 or more unless a feature gate is on; check your version). KEDA is the usual route."),
("Multiple metrics?","HPA computes a desired count per metric and takes the largest.")],
mistakes="""- HPA on CPU without a CPU request.
- Letting Git or Helm keep resetting `spec.replicas`.
- Using CPU for a GPU or queue-bound model.
- Scale-down window of zero, causing flapping.
- Max replicas that the nodes or quota cannot hold.""",
)

C[10] = dict(
say="A rolling update swaps pods in steps bounded by maxSurge and maxUnavailable and only counts a new pod when it is Ready, so readiness is the gate, but a bad model that still answers 200 passes the gate and needs a canary with real metrics.",
explain="""- **The two knobs.** `maxSurge` = how many extra pods above desired may exist during the update. `maxUnavailable` = how many below desired may be unready. Percentages: surge rounds up, unavailable rounds down. They cannot both be zero. Defaults are 25 percent each (check docs for your version). Example 10 replicas: surge 3, unavailable 2, so between 8 and 13 pods.
- **Readiness gates the rollout.** The controller creates new pods, waits for Ready, then removes old ones. If new pods never become Ready, the rollout stalls with old pods still serving (after `progressDeadlineSeconds` it is marked failed but nothing is rolled back by itself).
- **Commands (not executed here).** `kubectl rollout status deploy/x`, `kubectl rollout history deploy/x`, `kubectl rollout undo deploy/x [--to-revision=N]`. Undo makes the Deployment use the previous ReplicaSet's template again.
- **The real danger.** A model that loads, answers 200, and returns bad predictions passes readiness and the rollout completes. Readiness proves liveness of serving, not quality. You catch it with a canary plus metrics (error rate, latency, prediction distribution, business proxy; see Part 8) and an easy rollback.
- **Canary options.** Plain Kubernetes: two Deployments behind one Service whose selector matches both; traffic split follows replica ratio (roughly, since connection reuse skews it, and you cannot do 1 percent without 100 pods). Ingress or service mesh: weighted routing, exact percentages (check your controller's docs). KServe: `canaryTrafficPercent` on the predictor (check current KServe docs for the schema); also header routing in meshes.
- **Failure modes.** `maxUnavailable: 0` with no spare quota: surge pods Pending, rollout stuck. GPU models: surge needs a free GPU per extra pod; with no spare GPU set `maxSurge: 0, maxUnavailable: 1` and accept reduced capacity. Large models: every new pod loads weights, so a big surge makes a slow, expensive rollout.""",
example="""Rolling, 4 replicas, maxSurge 1, maxUnavailable 0: at most 5 pods, at least 4 ready. Steps: 1 new created, once ready 1 old removed, repeat: the output shows old 4,3,3,2,2,1,1,0 and new 1,1,2,2,3,3,4,4.
- If the new pods never become Ready, old stays 4 forever: stuck, but still serving.
- Canary: 9 stable plus 1 canary pods behind one Service: about 10 percent of requests hit the canary. Scale to 8+2 for 20 percent.""",
notexec="Not executed: the rollout, rollout status/history/undo, the canary and KServe (no cluster, no KServe). What ran: kubernetes-validate 1.37.0 `--strict` on the three core objects; the arithmetic and tick model in `rollout_math.py` (my simplification of the Deployment controller); and a YAML parse (only) of the KServe file, since the validator ships core schemas and not that CRD. The KServe field names come from memory of its docs and snippets: check current docs.",
follow=[("Rollout undo, but the old model is gone from the registry?","The old ReplicaSet keeps the old image reference, so undo needs that image and model artifact to still exist. Pin immutable tags and keep artifacts."),
("Where does `minReadySeconds` help?","It makes a pod stay Ready for N seconds before counting, catching crashes right after readiness turns green."),
("Why is rollback not enough for a bad model?","Because nobody notices without metrics. You need alerts on quality proxies and a canary before 100 percent.")],
mistakes="""- Treating a finished rollout as proof the model is good.
- `maxUnavailable: 0` and `maxSurge: 0` together (rejected).
- Using `latest` tags, so undo does not return to what ran before.
- Expecting an exact traffic percent from replica counts.
- Selector on the Service containing the `track` label, which splits canary from stable and removes one.""",
)

OUT = {  # which files go into Code blocks, per question: lang -> files ; cmds: list of shell commands to run (in the q dir)
1: dict(yaml=["ml-api.yaml"], python=["check_manifest.py", "owner_sim.py"],
        cmds=["kubernetes-validate --strict ml-api.yaml", "python3 -I check_manifest.py ml-api.yaml", "python3 -I owner_sim.py"],
        cluster=["kubectl apply -f ml-api.yaml", "kubectl get deploy,rs,pods,svc,endpoints -l app=ml-api", "kubectl delete pod <one-pod-name>   # then watch the ReplicaSet make a new one"]),
2: dict(yaml=["model-server.yaml"], python=["qos.py"],
        cmds=["kubernetes-validate --strict model-server.yaml", "python3 -I qos.py model-server.yaml"],
        cluster=["kubectl apply -f model-server.yaml", "kubectl describe pod model-server-guaranteed | grep 'QoS Class'"]),
3: dict(json=["pods_crash.json"], python=["triage.py"],
        cmds=["python3 -I triage.py pods_crash.json"],
        cluster=["kubectl get pod ml-api-a1", "kubectl describe pod ml-api-a1", "kubectl logs ml-api-a1", "kubectl logs ml-api-a1 --previous"]),
4: dict(json=["pods_mem.json"], python=["oom.py"],
        cmds=["python3 -I oom.py pods_mem.json"],
        cluster=["kubectl describe pod scorer-1 | grep -A6 'Last State'", "kubectl top pod scorer-1 --containers"]),
5: dict(text=["events.txt"], python=["pending.py"],
        cmds=["python3 -I pending.py events.txt"],
        cluster=["kubectl describe pod <pod> | sed -n '/Events/,$p'", "kubectl get events --field-selector reason=FailedScheduling", "kubectl get pvc", "kubectl describe resourcequota -n <ns>"]),
6: dict(yaml=["model-server.yaml"], python=["probes.py"],
        cmds=["kubernetes-validate --strict model-server.yaml", "python3 -I probes.py"],
        cluster=["kubectl apply -f model-server.yaml", "kubectl get endpoints model-server -w"]),
7: dict(yaml=["config.yaml"], python=["secret_demo.py"],
        cmds=["kubernetes-validate --strict config.yaml", "python3 -I secret_demo.py config.yaml", "kubernetes-validate --strict config.rendered.yaml"],
        cluster=["kubectl apply -f config.rendered.yaml", "kubectl rollout restart deploy/scorer"]),
8: dict(yaml=["gpu-serving.yaml"], python=["tolerates.py"],
        cmds=["kubernetes-validate --strict gpu-serving.yaml", "python3 -I tolerates.py gpu-serving.yaml"],
        cluster=["kubectl taint nodes gpu-node-1 nvidia.com/gpu=present:NoSchedule", "kubectl label nodes gpu-node-1 pool=gpu", "kubectl apply -f gpu-serving.yaml", "kubectl describe node gpu-node-1 | grep -A8 Allocatable"]),
9: dict(yaml=["hpa.yaml"], python=["hpa_sim.py"],
        cmds=["kubernetes-validate --strict hpa.yaml", "python3 -I hpa_sim.py"],
        cluster=["kubectl apply -f hpa.yaml", "kubectl get hpa infer-cpu -w", "kubectl top pods   # needs metrics-server"]),
10: dict(yaml=["rollout.yaml", "kserve-canary.yaml"], python=["rollout_math.py"],
        cmds=["kubernetes-validate --strict rollout.yaml", "python3 -I rollout_math.py kserve-canary.yaml"],
        cluster=["kubectl apply -f rollout.yaml", "kubectl rollout status deploy/churn-stable", "kubectl rollout history deploy/churn-stable", "kubectl rollout undo deploy/churn-stable"]),
}
