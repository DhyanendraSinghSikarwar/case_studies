A = {}
A[31] = r"""
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
{{PY:q31_decide.py}}
{{YAML:q31_job.yaml}}
```bash
cd code && python3 -I q31_decide.py
kubernetes-validate --strict q31_job.yaml
```

**Output (my run):** the helper and the schema validation ran. Kubeflow, Argo, Airflow and any cluster are **not executed**: no cluster here. `kubernetes-validate --strict` checks the Job schema only, not scheduling or whether the image exists.
{{OUT:q31.txt}}
{{OUT:q31v.txt}}

**Follow-ups:**
- *What does the Training Operator add over a plain Job?* It creates a set of pods with the roles and environment a distributed framework expects (master, workers) and handles the job as one unit. A plain Job knows nothing about ranks. Gang scheduling needs a queue such as Kueue or Volcano on top (check current docs).
- *Is Katib worth it?* Only if you run many trials on a shared cluster. For a handful of trials, a script with Optuna in one Job is simpler.
- *Why not just use SageMaker?* If data, IAM and the team already live in that cloud and nobody wants to run a cluster, that is often right. Say so.

**Common mistakes:** installing the whole platform on day one; confusing KFP (pipelines) with the platform; forgetting the cluster needs an owner; claiming "Kubeflow is dead" or "Kubeflow is the standard" without saying which piece.
"""

A[32] = r"""
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
{{YAML:q32_kind.yaml}}
{{PY:q32_portfolio_check.py}}
```bash
# not executed (no kind, no Docker daemon here): kind create cluster --config q32_kind.yaml
python3 -I q32_portfolio_check.py
```

**Output (my run):** `kind` is **not executed**: no Docker daemon and no kind binary here. I did run the portfolio checker on a demo folder it builds in a temp directory, and parsed the kind config with PyYAML (that only proves the YAML is valid, not that kind accepts it).
{{OUT:q32.txt}}
{{OUT:q32v.txt}}

**Follow-ups:**
- *How do you show HPA working without real traffic?* Run a loop of requests from a busybox pod and watch replicas. Metrics-server must be installed in kind (check current docs).
- *Free managed cluster?* Check current terms of each cloud; treat any credit as time-limited.
- *Is a Kubernetes certificate needed?* A project with a working chart and a rollback story says more. Certificates are optional extras.

**Common mistakes:** listing "Kubernetes" with no repo; pasting a tutorial unchanged; leaving a cloud cluster running; saying "I used GPUs" when the lab was CPU-only.
"""

A[33] = r"""
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
{{YAML:q33_statefulset.yaml}}
{{PY:q33_names.py}}
```bash
python3 -I q33_names.py
kubernetes-validate --strict q33_statefulset.yaml
```

**Output (my run):** the name script and the schema validation ran. Applying the StatefulSet, PVC binding and rolling behaviour are **not executed**: no cluster. The statements about ordering and PVC retention come from the Kubernetes docs as I know them, not from a run here.
{{OUT:q33.txt}}
{{OUT:q33v.txt}}

**Follow-ups:**
- *Distributed training workers?* Stable ranks and DNS names help, but in practice most teams use the Training Operator (PyTorchJob) rather than a raw StatefulSet. It handles the wiring.
- *Can a StatefulSet use a shared volume?* Yes, with a manually created PVC and `ReadWriteMany`, but then you lose per-replica storage, which is the point.
- *Pod stuck Terminating on a dead node?* StatefulSet will not start a duplicate until the old pod is confirmed gone. That is a safety feature (at-most-one pod per identity).

**Common mistakes:** missing or mismatched `serviceName`; using a StatefulSet for a stateless API; expecting PVCs to vanish on scale-down; no readiness probe, so ordered start moves on too early.
"""

A[34] = r"""
**Say this first (1 line):** A DaemonSet runs one pod on every (matching) node for node-level jobs like the GPU device plugin or log shippers, and an operator is a custom resource plus a controller that keeps reconciling actual state to the desired state in that resource.

**Then explain:**
- **DaemonSet:** one pod per node, new node means new pod automatically. Typical ML uses: NVIDIA device plugin, DCGM exporter, node-exporter, log shipper. Use `nodeSelector` (or node affinity) to restrict it to GPU nodes, and a **toleration** because GPU nodes are usually tainted.
- **Operator pattern:** you define a CRD (say `ModelServer`), users create objects of that kind, and a controller watches them. The loop: read desired state, read actual state, make the smallest change, repeat. It is level-based, so it is safe to run again and recovers from missed events.
- **ML examples:** GPU Operator (installs driver, device plugin, monitoring pieces), Training Operator (PyTorchJob), KServe (InferenceService). Names and details: check current docs.
- **Failure modes:** a DaemonSet without the toleration silently skips GPU nodes; a DaemonSet with no resource requests starves workloads; a controller that is not idempotent creates duplicates; a buggy operator can delete everything (it has cluster permissions); CRD version upgrades breaking stored objects.

**Example:** nodes: 2 CPU, 3 GPU (labelled `node-pool=gpu`, tainted). The DaemonSet below produces 3 pods, not 5. Remove the toleration and it produces 0. In the toy loop: the CR says 3 replicas, one pod is killed, the next tick recreates it; edit the CR to 2 and the extra pod goes; change the image and pods are replaced.

**Code:** a DaemonSet manifest and a toy reconcile loop. The loop is a simulation: the "cluster" is a dict, there is no watch, no API server and no finalizers.
{{YAML:q34_daemonset.yaml}}
{{PY:q34_reconcile.py}}
```bash
python3 -I q34_reconcile.py
kubernetes-validate --strict q34_daemonset.yaml
```

**Output (my run):** the reconcile loop ran for real (as a Python simulation), and the DaemonSet passed schema validation. Real operators, the device plugin and DaemonSet scheduling are **not executed**: no cluster, no GPU.
{{OUT:q34.txt}}
{{OUT:q34v.txt}}

**Follow-ups:**
- *Why level-based, not edge-based?* Events can be missed or repeated. Comparing full desired and actual state each time converges either way.
- *DaemonSet vs Deployment with one replica per node?* DaemonSet follows node count automatically and tolerates node-specific needs.
- *How is a CRD different from a ConfigMap?* A CRD adds a typed API object with validation and a controller acting on it. A ConfigMap is just data.

**Common mistakes:** forgetting tolerations; thinking an operator is magic and not a program with permissions; running a DaemonSet with host access without thinking about security (see Q35); writing a controller that is not idempotent.
"""

A[35] = r"""
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
{{YAML:q35_hardened.yaml,q35_bad.yaml}}
{{PY:q35_score.py}}
```bash
python3 -I q35_score.py q35_hardened.yaml q35_bad.yaml
kubernetes-validate --strict q35_hardened.yaml q35_bad.yaml
```

**Output (my run):** scorer and schema validation ran. Both pods are schema-valid (the validator does not judge security). Pod Security Admission, seccomp, GPU access and the read-only filesystem behaviour are **not executed**: no cluster.
{{OUT:q35.txt}}
{{OUT:q35v.txt}}

**Follow-ups:**
- *Is `restricted` enough?* It covers the pod spec. Add NetworkPolicy, RBAC least privilege, image scanning and signing. Not a full security story.
- *Can I use PSS for a namespace with GPU operator pods?* The operator namespace usually needs a looser level (privileged) since it installs drivers; keep tenant namespaces at restricted. Check the operator docs.
- *Why disable the service account token?* A stolen token is API access. If the model server never calls the API, remove it.

**Common mistakes:** `privileged: true` "to make the GPU work"; running as root because the Dockerfile did; forgetting `/dev/shm` then blaming Kubernetes for DataLoader crashes; enforcing `restricted` cluster-wide on day one with no warn period.
"""

A[36] = r"""
**Say this first (1 line):** Most GPU waste is idle time, so measure idle GPU-hours first, then right-size, put training on spot nodes with checkpoints, scale idle endpoints to zero (accepting cold starts), and use quotas and TTLs so nothing is forgotten.

**Then explain:**
- **Right-sizing:** VPA in recommendation mode shows what a pod really used versus what it asked for. Use it as advice, not as automatic restarts for latency-sensitive pods. GPU memory and utilisation need GPU metrics, not VPA.
- **Spot or preemptible nodes for training:** cheaper but can vanish with short notice. It works only if the job **checkpoints** and can resume. Keep serving on on-demand nodes.
- **Scale-to-zero for idle endpoints:** HPA alone cannot go to zero (its minimum is 1 by default); KEDA or a serverless layer like Knative/KServe can (check current docs). The price is a **cold start**: node start if needed, image pull, weights load into GPU memory. Keep one warm replica if latency matters.
- **Structure:** separate CPU and GPU node pools (taint the GPU pool); ResourceQuota per team; `ttlSecondsAfterFinished` on Jobs; clean up orphaned PVCs and load balancers (they bill while idle). Part 12 owns cost design in depth.
- **Failure modes:** spot reclaim with no checkpoint loses hours; scale-to-zero on an endpoint with a strict latency target; a "temporary" notebook holding a GPU for weeks; deleted workloads leaving PVCs and load balancers.

**Example (made-up round numbers, unit is GPU-hours not money):** 2 GPU replicas always on: 2 x 24 = 48 GPU-h per day. Traffic only 6 hours a day. Scale to zero outside traffic: 2 x 6 = 12 GPU-h, plus 2 cold starts of 3 minutes each on 2 GPUs = 0.2, so 12.2 GPU-h. Saving 35.8 GPU-h (about 75 percent), paid for with a 3-minute wait for the first request after idle. A middle road: keep 1 warm replica, which costs 1 x 24 + 1 x 6 = 30 GPU-h and no cold start for the first user.

**Code:** a script that computes idle GPU-hours from an hourly log (one row = one GPU for one hour, util below 10 percent counts as idle; the threshold is a policy choice) and the arithmetic above.
{{PY:q36_idle.py}}
```bash
python3 -I q36_idle.py
```

**Output (my run):** ran with a made-up 15-row log (CSV in `code/q36_util_log.csv`). Hand check: infer-a has 6 rows, util 2, 1, 0, 60, 70, 5, so 4 are below 10 percent. Cloud billing, VPA, KEDA and spot behaviour are **not executed**: no cluster, no cloud account.
{{OUT:q36.txt}}

**Follow-ups:**
- *How do you find orphaned PVCs?* List PVCs not mounted by any pod and older than a threshold, then review. Do not auto-delete data.
- *Spot for inference?* Possible with enough replicas and a fallback on-demand pool, but each reclaim is a cold start; judge by SLO.
- *Is low GPU utilisation always waste?* No. A latency-bound model with batch size 1 can show low utilisation yet be sized right. Look at queue time and throughput too.

**Common mistakes:** no checkpointing on spot; one huge node pool for everything; trusting average utilisation (hides bursts); quoting prices from memory.
"""

A[37] = r"""
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
{{YAML:q37_sa.yaml}}
{{PY:q37_check.py}}
```bash
python3 -I q37_check.py
kubernetes-validate --strict q37_sa.yaml
```

**Output (my run):** the annotation check and schema validation ran. Annotations are free-form strings to the schema, so passing proves only that the YAML is a valid ServiceAccount. Whether a cloud accepts them is **not executed**: no cloud account, no cluster.
{{OUT:q37.txt}}
{{OUT:q37v.txt}}

**Follow-ups:**
- *Why not put cloud keys in a Secret?* They are long-lived, easy to leak and hard to rotate. Federated short-lived tokens are safer.
- *Autopilot-style modes for GPUs?* Check current docs for GPU support and limits.
- *Multi-cloud?* Kubernetes helps with manifests, but identity, storage and load balancers still differ per cloud.

**Common mistakes:** saying "managed" means "no ops"; forgetting zonal disks; no GPU quota check; quoting instance names from memory.
"""

A[38] = r"""
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
{{YAML:q38_servicemonitor.yaml}}
{{PY:q38_parse.py}}
```bash
python3 -I q38_parse.py
```

**Output (my run):** the parser ran on a sample file (`code/q38_metrics.txt`); the numbers match the hand calculation. The ServiceMonitor was only parsed with PyYAML: it is a CRD, so `kubernetes-validate` has no schema for it, and Prometheus, PromQL, DCGM and `kubectl top` are **not executed**: no cluster.
{{OUT:q38.txt,q38v.txt}}

**Follow-ups:**
- *Why not alert on CPU?* For an ML service CPU may be low while the GPU or queue is the bottleneck. Alert on user symptoms plus saturation.
- *Why histograms, not averages?* Averages hide the tail, and histograms from many pods can be summed before taking a quantile.
- *Where do events go?* Ship them to your log store if you need history.

**Common mistakes:** ServiceMonitor selecting Pods not Services; unnamed Service port; alerting on everything; no model-quality signal at all.
"""

A[39] = r"""
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
{{YAML:q39_quota.yaml}}
{{PY:q39_check.py}}
```bash
python3 -I q39_check.py
kubernetes-validate --strict q39_quota.yaml
```

**Output (my run):** script and schema validation ran. Kueue, KServe, KEDA, quota enforcement and notebook culling are **not executed**: this is a design question and there is no cluster.
{{OUT:q39.txt}}
{{OUT:q39v.txt}}

**Follow-ups:**
- *Time-slicing or MIG to share a GPU?* Time-slicing has no memory or fault isolation; MIG (on supported GPUs) gives hardware isolation. Use for small inference and notebooks; check current docs.
- *How do you stop hoarding?* Quotas, idle culling, a max runtime on GPU notebooks, and a usage report per team.
- *Why a queue, not just quota?* Quota says no; a queue says wait, and lets idle capacity be used.

**Common mistakes:** quota larger than the cluster; no preemption story; GPUs held by idle notebooks; forgetting fragmentation.
"""

A[40] = r"""
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
{{YAML:q40_manifests/old_hpa_cronjob.yaml}}
{{PY:q40_scan.py}}
```bash
python3 -I q40_scan.py
kubernetes-validate --strict q40_manifests/ok_deploy.yaml
# not executed (no cluster, no kubectl): kubectl drain NODE --ignore-daemonsets --delete-emptydir-data
```

**Output (my run):** the scan and the multi-version validation ran (kubernetes-validate 1.37.0). The upgrade, drain, GPU driver and device plugin checks are **not executed**: no cluster, no kubectl, no GPU.
{{OUT:q40.txt}}
{{OUT:q40v.txt}}

**Follow-ups:**
- *`kubectl convert`?* It is a separate plugin that rewrites old manifests to a newer apiVersion; check current docs. Not available here.
- *Helm releases with removed APIs?* The release stored in the cluster can reference removed kinds; a Helm plugin or manual edit is needed (check current docs). Better to fix before upgrading.
- *How do you reduce risk?* Staging cluster first, canary node pool, backups, and a rollback plan for node images.

**Common mistakes:** testing only the raw YAML and not the rendered chart; skipping a minor; draining GPU nodes with no checkpointing; assuming the GPU driver is unchanged in the new image.
"""
