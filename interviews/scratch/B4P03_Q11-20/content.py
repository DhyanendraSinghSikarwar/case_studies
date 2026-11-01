# ---------------- Q11 ----------------
answers.append(render(11, "q11",
say="A Helm chart is a folder of templates plus default values; a release is one installed copy of it in a cluster, and Helm keeps every revision so you can roll back.",
explain="""- **Chart layout.** `Chart.yaml` (name, chart version, appVersion), `values.yaml` (defaults), `templates/` (YAML with Go-template holes), `_helpers.tpl` (named snippets such as a shared name). `charts/` holds sub-charts.
- **The commands.** `helm lint` checks the chart. `helm template` renders YAML on your laptop, no cluster. `helm install` renders and creates a release. `helm upgrade` renders again and applies a new revision. `helm rollback N` makes a NEW revision with the content of revision N. Add `--atomic` or `--wait` so a failed upgrade is not left half done (check `helm upgrade --help`).
- **Values order, lowest to highest.** Chart `values.yaml`, then each `-f file` in the order given, then `--set`. Maps merge key by key. Scalars and lists are replaced whole. `--set` turns `true`, `null` and plain integers into non-strings, so a tag like `20260101` becomes a number (quote it in the template, or use `--set-string`).
- **Where state lives.** Helm 3 has no Tiller (the in-cluster server of Helm 2). The client talks to the API server with your kubeconfig, and each revision is saved as a Secret named like `sh.helm.release.v1.<release>.v<N>` in the release namespace (default storage driver). So RBAC on that namespace is what protects releases. Helm 4 exists; the basics here carry over, but check its release notes.
- **ML-platform failure modes.** Values drift (someone `kubectl edit`s a live Deployment and the next upgrade overwrites it). `--reuse-values` on upgrade hides new chart defaults. A bad model that still passes readiness is NOT undone by `rollback` unless the image tag was in the chart values. A rollback does not touch a database or PVC contents. Huge rendered manifests can hit the size limit of a stored release; keep big files out of templates.""",
example="""Hand-check the merge. Defaults: `replicaCount: 2`, memory limit `2Gi`, tag `1.4.1`, gpu off. `prod.yaml` sets replicas 3, gpu on, memory limit `8Gi`. Command adds `--set image.tag=1.4.2 --set replicaCount=5`. Result: replicas **5** (`--set` wins), memory limit **8Gi** (file beats default), memory request still `1Gi` (a map merges, untouched keys survive), tag **1.4.2**, and the rendered Deployment gains `nvidia.com/gpu: 1` plus a GPU toleration. With default values there are 0 lines mentioning nvidia.""",
code=[("yaml", ["chart/modelserver/Chart.yaml", "chart/modelserver/values.yaml", "chart/modelserver/templates/_helpers.tpl",
                "chart/modelserver/templates/configmap.yaml", "chart/modelserver/templates/service.yaml",
                "chart/modelserver/templates/deployment.yaml", "prod.yaml"]),
      ("python", ["helm_mimic.py"]),
      ("bash", ["helm_commands.sh"])],
cmds=["command -v helm kubectl || echo 'helm / kubectl: not installed'",
      "python3 -I helm_mimic.py values",
      "python3 -I helm_mimic.py chart/modelserver -f prod.yaml --set image.tag=1.4.2 --release churn > rendered.yaml; sed -n '/^kind: Deployment/,/^---/p' rendered.yaml",
      "kubernetes-validate --strict rendered.yaml",
      "echo \"lines mentioning nvidia with default values: $(python3 -I helm_mimic.py chart/modelserver | grep -c nvidia)\"",
      "bash -n helm_commands.sh && echo 'bash -n: helm_commands.sh syntax OK'"],
notrun="**Not executed:** `helm lint`, `template`, `install`, `upgrade`, `rollback` (no helm binary; the Helm download was blocked by the sandbox proxy) and anything against a cluster. What did run: `helm_mimic.py`, a small Python stand-in that applies the value-merge rules and fills only the template holes this chart uses (it is a teaching mimic, not Helm; real Helm uses Go templates and Sprig functions, so real output can differ in whitespace and details). The rendered YAML was then checked with `kubernetes-validate --strict` (schema only, Kubernetes 1.37 schemas).",
followups="""- **Why does `helm rollback` give a higher revision number?** Rollback is recorded as a new revision whose content equals the old one, so history stays linear.
- **How do you force a pod restart when only a ConfigMap changed?** Put a checksum of the rendered ConfigMap in a pod-template annotation; a changed hash changes the pod template and triggers a rollout.
- **Helm or Kustomize?** Helm when you need packaging and parameters for many users; Kustomize for patching plain YAML per environment. Many teams use both.""",
mistakes="""- Thinking `helm template` or `lint` proves the chart works on a cluster. They check rendering and structure only.
- Passing secrets with `--set`. They land in shell history and in the release Secret. Use external secret tools.
- `--reuse-values` on upgrade, then wondering why new chart defaults never show up.
- Unquoted numeric-looking image tags, so `1.10` style values or all-digit tags change type.
- Believing a rollback also restores data, a PVC or a model registry state."""))

# ---------------- Q12 ----------------
answers.append(render(12, "q12",
say="A Job runs a pod to completion with retries and a deadline; a CronJob is a Job factory on a cron schedule, and for training you set the retry, deadline, cleanup and concurrency fields on purpose.",
explain="""- **Job fields.** `completions` (how many successful pods), `parallelism` (how many at once), `backoffLimit` (retries before the Job is Failed; I recall the default is 6, check docs), `activeDeadlineSeconds` (hard time cap for the whole Job, wins over retries), `ttlSecondsAfterFinished` (auto-delete the finished Job and its pods), `restartPolicy` must be `OnFailure` or `Never`, never `Always`.
- **On failure.** `Never`: the failed pod stays for `kubectl logs` and the Job creates a NEW pod. `OnFailure`: the container restarts inside the same pod. Both count towards `backoffLimit`, with growing delays between retries. A crashing GPU job with no deadline can burn GPU time for a long while.
- **On node loss.** The pod is gone or stuck; the Job controller creates a replacement pod, which starts from zero unless your code resumes from a checkpoint on a PVC or object storage. Newer clusters have a pod failure policy to treat node disruption differently from app errors (check your version).
- **CronJob fields.** `schedule` (5-field cron), `timeZone` (IANA name; without it the controller's zone is used; supported in current releases, check yours), `concurrencyPolicy` (`Allow` overlaps, `Forbid` skips if the last run is still going, `Replace` kills the old one), `startingDeadlineSeconds` (how late a run may start before it is counted as missed), `successfulJobsHistoryLimit` and `failedJobsHistoryLimit`, `suspend`.
- **Failure modes.** Overlapping nightly runs fighting for one GPU and one PVC. Missed runs after controller downtime (with many missed runs the CronJob can stop scheduling; `startingDeadlineSeconds` limits the counting window). Cron in UTC while the team thinks in IST. A finished Job never cleaned up, so hundreds of old pods pile up. `schedule` with both day-of-month and day-of-week set means OR, not AND.""",
example="""`schedule: "30 1 * * *"` with `timeZone: Asia/Kolkata` runs at 01:30 IST every day. IST is UTC+5:30, so that is 20:00 UTC the day before. Hand-check: 01:30 minus 5:30 = 20:00 previous day, and the script prints exactly that. Trace one night with `Forbid`: if last night's run is still going at 01:30, tonight's is skipped, not queued. With `backoffLimit: 1` the pod may run twice at most before the Job is Failed.""",
code=[("yaml", ["train-job.yaml", "retrain-cron.yaml"]), ("python", ["check_batch.py"])],
cmds=["kubernetes-validate --strict train-job.yaml retrain-cron.yaml",
      "python3 -I check_batch.py train-job.yaml retrain-cron.yaml",
      "python3 -I check_batch.py bad-cron.yaml | sed -n 1p",
      "kubernetes-validate --strict bad-cron.yaml"],
notrun="**Not executed:** creating the Job or CronJob and any real retry, node-loss or schedule behaviour (no cluster, no GPU). What did run: `kubernetes-validate --strict` (schema only) and `check_batch.py`, which checks the fields above and expands cron into the next five run times from a fixed 'now' of 2026-10-26 22:10 in the CronJob's zone (my own small cron parser: 5 fields, `*`, lists, ranges, steps; no `@daily` or names). The last two commands use a deliberately sloppy file: the schema validator passes it (the schema does not encode these rules, and the API server's own validation would reject `restartPolicy: Always` for a Job) while my checker lists the real problems, which shows why schema validation is not enough.",
followups="""- **Job or Deployment for training?** Job: it ends, retries and reports success. A Deployment would restart a finished process forever.
- **How do you run 8 workers of one training task?** Indexed Job or a training operator (Kubeflow, see later parts); for tightly coupled GPU jobs you also need gang scheduling so half the workers do not sit holding GPUs.
- **Why `Replace` rarely?** It kills a run that may be nearly done. `Forbid` is the safer default for training.""",
mistakes="""- `restartPolicy: Always` in a Job template (the API rejects it for Jobs; my checker flags it for the template).
- No `activeDeadlineSeconds`, so a hung job holds a GPU all weekend.
- No `ttlSecondsAfterFinished`, then 300 completed pods and a slow `kubectl get pods`.
- Forgetting the time zone, so the 'nightly' retrain runs at office time.
- Training that cannot resume, so a retry restarts from epoch 0."""))

# ---------------- Q13 ----------------
answers.append(render(13, "q13",
say="A PersistentVolumeClaim is a pod's request for storage, a StorageClass says how to create it, and the access mode decides how many nodes can mount it; model replicas should not share a ReadWriteOnce claim.",
explain="""- **The pieces.** PV = the real storage object. PVC = the request ('50Gi, this access mode, this class'). StorageClass = the recipe for dynamic provisioning: a PVC with a class makes the provisioner create a PV and bind it. The pod only names the PVC.
- **Access modes.** `ReadWriteOnce` (RWO): mountable read-write by ONE NODE at a time (several pods on that node can share it). `ReadOnlyMany` (ROX): many nodes read. `ReadWriteMany` (RWX): many nodes read and write. Cloud block disks are usually RWO only; RWX and ROX need a shared file backend. Which one your cluster supports is a storage-driver question, check current docs. There is also a ReadWriteOncePod mode in newer versions.
- **Lifetime.** Pod dies, PVC and data stay. Delete the PVC and the PV's `reclaimPolicy` decides: `Delete` removes the disk, `Retain` keeps it for manual cleanup. `emptyDir` dies with the pod. Zonal disks also pin the pod to one zone; `WaitForFirstConsumer` creates the disk where the pod lands.
- **A Pending PVC blocks the pod.** Typical causes: no such StorageClass, no default class, no provisioner or driver, quota exhausted, no PV matches the size or mode, or (normal!) `WaitForFirstConsumer` waiting for a pod. The pod event says 'unbound immediate PersistentVolumeClaims' or similar.
- **For many serving replicas, three options.** (1) One ROX/RWX volume holding the model: one copy, but needs shared storage and a populate step. (2) Init container downloads from object storage into `emptyDir`: simple and stateless, but every pod downloads and node disk is used N times. (3) Bake the model into the image: fastest start, big images. Pick by model size and how often it changes.""",
example="""Made-up numbers: a 20 GiB model, 4 replicas on 4 nodes. Option 2 (emptyDir): 4 downloads and 80 GiB of node disk in total, and every restart downloads again. Option 1 (one ROX volume): 1 copy, 20 GiB, no download on restart, but needs a backend that supports ROX. If instead you give all 4 replicas one RWO claim, pods on other nodes cannot mount it and stay `ContainerCreating` or Pending. The checker below flags exactly that.""",
code=[("yaml", ["storage.yaml"]), ("python", ["check_storage.py"])],
cmds=["kubernetes-validate --strict storage.yaml",
      "python3 -I check_storage.py storage.yaml",
      "python3 -I check_storage.py bad-storage.yaml"],
notrun="**Not executed:** applying anything, provisioning, mounting, binding or the real Pending behaviour (no cluster, no CSI driver). What did run: `kubernetes-validate --strict` (schema only) and `check_storage.py`, my cross-checker for missing classes, missing claims, RWO shared by several replicas and unbounded emptyDir. On the good file it flags one real gap: the class `shared-files` used by `model-cache` is not defined in the file (I left it out on purpose; on a real cluster it may exist outside the file). The second run uses a deliberately broken file.",
followups="""- **Why can a RWO volume still work for 3 replicas sometimes?** If the scheduler puts all pods on the same node. Luck, not design.
- **Where should training checkpoints go?** A PVC or object storage, never the container filesystem, so a rescheduled job can resume.
- **Why does the PVC say Pending right after creation with WaitForFirstConsumer?** That is expected; it binds when a pod using it is scheduled.""",
mistakes="""- Writing to the container filesystem and calling it persistent.
- Sharing one RWO claim across replicas and blaming the scheduler.
- No `sizeLimit` on `emptyDir` and filling the node disk.
- Using `Delete` reclaim for data you cannot recreate.
- Assuming every cluster supports RWX; it depends on the storage backend."""))

# ---------------- Q14 ----------------
answers.append(render(14, "q14",
say="A Service gives pods a stable in-cluster address, an Ingress is only a set of routing rules, and an ingress controller is the running proxy that reads those rules; without a controller the Ingress does nothing.",
explain="""- **Three layers.** Pods behind a Service (ClusterIP). An Ingress object says 'host + path goes to Service:port'. An ingress controller (NGINX, Traefik, or a cloud load balancer controller) watches Ingress objects and configures a real proxy or cloud LB. `ingressClassName` picks which controller owns the Ingress.
- **Routing.** Host and path rules. `pathType: Prefix` matches `/docs` and `/docs/x`; `Exact` matches one path. The controller does not rewrite paths unless asked (annotation, controller-specific), so the app must really serve `/v1/predict`.
- **TLS.** `tls.secretName` points to a Secret of type `kubernetes.io/tls`. The controller terminates TLS and talks plain HTTP to the pod by default. Certificates are often issued by an add-on such as cert-manager.
- **Big inference payloads.** Proxies have a default body-size cap and read timeout, and they are small defaults for images, audio or long model calls. Annotation names are controller-specific (the ones in my file are for the community NGINX controller; check its current docs). For streaming or very long calls, also check the cloud load balancer's idle timeout.
- **Direction.** Gateway API (Gateway, HTTPRoute) is the newer, more expressive model and is where new features go. I also recall the community ingress-nginx project announcing its retirement; check its current status before choosing a controller.
- **Failure modes.** No controller installed (ADDRESS stays empty). Wrong `ingressClassName`. Backend Service name or port typo gives 404/503 from the proxy. Readiness failing, so the Service has no endpoints. Path prefix mismatch.""",
example="""Request `https://ml.example.com/v1/predict` -> controller matches host `ml.example.com`, longest prefix `/v1/predict` -> Service `model-svc` port 80 -> `targetPort` 8080 on a ready pod. Request `/docs/swagger` -> prefix `/docs` -> `docs-svc` port named `http`. Hand-check in the broken file below: the Ingress names `model-svc` but the Service was renamed `model-service`, so the proxy would have no backend, and the second rule asks for port 8000 while the Service exposes 80.""",
code=[("yaml", ["ingress.yaml"]), ("python", ["check_ingress.py"])],
cmds=["kubernetes-validate --strict ingress.yaml",
      "python3 -I check_ingress.py ingress.yaml",
      "python3 -I check_ingress.py bad-ingress.yaml"],
notrun="**Not executed:** an ingress controller, TLS, real routing or timeouts (no cluster). What did run: `kubernetes-validate --strict` (schema only; a 404 backend is valid YAML) and `check_ingress.py`, my cross-checker that every backend names a Service in the same file and a port that Service exposes (by number or name). The `bad-ingress.yaml` run shows it catching a missing Service, a wrong port and a missing `ingressClassName`.",
followups="""- **Ingress or LoadBalancer Service?** A LoadBalancer Service is one cloud LB per Service (L4 mostly). An Ingress shares one entry point and routes by host/path (L7).
- **Where do you do auth and rate limiting?** At the gateway or controller (annotations or policies), or in the app; keep it consistent and check what your controller supports.
- **How do you test an Ingress rule without a cluster?** Schema-validate, cross-check names and ports like above, then test on a dev cluster.""",
mistakes="""- Applying an Ingress and never installing a controller.
- Forgetting `ingressClassName` on clusters with several controllers.
- Using the default body-size and timeout for big inference payloads.
- Expecting the path `/v1/predict` to be stripped before it reaches the pod.
- Putting the TLS Secret in a different namespace from the Ingress."""))

# ---------------- Q15 ----------------
answers.append(render(15, "q15",
say="Pending is almost always about eligibility, not total capacity: read the scheduler's event, then check held GPUs, resource names, taints and selectors, the device plugin, the container that holds the request, quota, and whether the free GPUs sit on different nodes.",
explain="""- **Step 1: the event.** `kubectl describe pod` shows the scheduler's reason per node group ('Insufficient nvidia.com/gpu', 'untolerated taint', 'didn't match node selector'). Wording changes by version. Start there, not with dashboards.
- **Idle but held.** A GPU is 'busy' to the scheduler the moment a pod requests it, even if `nvidia-smi` shows 0 percent (a forgotten notebook). Dashboards that read utilisation show 'idle'; the scheduler counts requests.
- **Name mismatch.** Time-sliced GPUs still use `nvidia.com/gpu` (more of them); MIG slices use their own names (for example `nvidia.com/mig-1g.10gb`, names depend on mode and GPU, check the GPU Operator docs). A pod asking for `nvidia.com/gpu` never lands on a node that only advertises MIG names.
- **Plumbing.** Taint without toleration, node selector or affinity mismatch, the device plugin DaemonSet not running or crashing on a node (the node then advertises 0 GPUs), driver or container-runtime misconfigured (pod is scheduled but fails at start, a different symptom), the GPU limit written on the wrong container or an init container, a namespace ResourceQuota on `requests.nvidia.com/gpu`.
- **Fragmentation.** GPUs are whole integers on one node. A 4-GPU pod needs 4 free on ONE node; 6 free split 2+2+2 is useless. Fixes: bin-pack (scheduler scoring, dedicated pools for big jobs), run big jobs first, quota and queueing (Kueue-style, later parts), smaller jobs, or defragment by moving small pods.""",
example="""Inventory (made up): gpu-a 8 GPUs with 6 used, gpu-b 4 with 2 used, gpu-c 4 with 2 used, gpu-d plugin down (advertises none), mig-e advertises only MIG slices, cpu-f is a CPU node, train-g has 8 free GPUs but a `dedicated=training` taint. A pod wants 4 GPUs. Hand-check: free GPUs on eligible nodes are 2+2+2 = 6 in total, largest block 2, need 4 -> fragmentation, even though 'dashboard shows idle GPUs' (train-g, mig-e and a notebook holding 2).""",
code=[("python", ["gpu_diag.py"]), ("bash", ["diagnose.sh"])],
cmds=["python3 -I gpu_diag.py", "bash -n diagnose.sh && echo 'bash -n diagnose.sh: syntax OK'"],
notrun="**Not executed:** every `kubectl` command in `diagnose.sh` (no cluster, no GPU); only `bash -n` (syntax check) ran. What did run: `gpu_diag.py`, an offline model of the scheduler's node selector, taint, resource-name and free-capacity filters on a made-up inventory. The 'event' line is my approximation of the scheduler's message format, not copied from a real cluster.",
followups="""- **How do you stop one notebook hoarding GPUs?** Per-namespace GPU quota, idle culling for notebooks, and time-slicing or MIG for small work.
- **A 4-GPU job keeps starving behind small jobs. Options?** Dedicated node pool for large jobs, priority classes, a queue with quota (Kueue style), or gang scheduling so the job gets all or nothing.
- **Pod is scheduled but the container fails with a driver error?** That is the runtime or driver layer, not the scheduler: check the NVIDIA container toolkit and driver on that node.""",
mistakes="""- Trusting a utilisation dashboard instead of requested versus allocatable.
- Putting the GPU limit on a sidecar or init container.
- Forgetting the toleration for the GPU taint.
- Adding a node when the real cause is a selector or quota.
- Not noticing that requests and limits for GPUs must match and that GPUs are not shared between containers unless you set up sharing."""))

# ---------------- Q16 ----------------
answers.append(render(16, "q16",
say="Kubernetes is a store plus control loops: kubectl writes the desired state through the API server into etcd, controllers create the objects, the scheduler picks a node, and the kubelet on that node starts the containers.",
explain="""- **Control plane.** API server (the only door: authentication, authorisation, admission, validation, then storage). etcd (the database of all objects). Scheduler (picks a node for each unbound pod). Controller manager (runs loops: Deployment, ReplicaSet, Node, Job and many more). Cloud controller if on a cloud.
- **Node.** kubelet (watches pods bound to its node, asks the container runtime to pull and start them, reports status and probe results), container runtime (containerd or similar, through CRI), kube-proxy or an equivalent (Service routing rules on the node), plus network and, for GPU, device plugin.
- **The trace for `kubectl apply` of a Deployment.** 1) API server validates and stores it in etcd. 2) Deployment controller sees it and creates a ReplicaSet. 3) ReplicaSet controller sees 0 pods, wants N, creates N Pod objects (no node yet, phase Pending). 4) Scheduler sees unbound pods, filters and scores nodes, writes the chosen node into each pod. 5) The kubelet on that node sees a pod for it, pulls the image, starts containers, runs probes. 6) Endpoints update once pods are Ready, so the Service sends traffic.
- **Everything is level-triggered.** Each controller compares desired with actual and fixes the difference; it does not matter which event was missed. That is why a deleted pod comes back.
- **What breaks.** etcd or API server down: no reads or writes, so no deploys, no scaling, no healing; already-running pods usually keep serving, because kubelets keep running what they have. Scheduler down: existing pods fine, new pods stay Pending. Controller manager down: no replacement for dead pods, no rollouts. A node (kubelet) down: its pods are marked NotReady later and rescheduled after the eviction timeouts, so recovery is not instant.""",
example="""Run the toy: apply 3 replicas -> ReplicaSet and 3 pods are created, bound to nodes and started. Delete one pod behind the API's back -> next tick the ReplicaSet controller notices 2 of 3 and creates pod 4. Scale to 5 with the scheduler down -> 2 pods stay Pending, 3 keep running; scheduler returns -> both get nodes. Make the store reject writes (etcd down) -> the scale to 6 fails and the 5 running pods are untouched. Count by hand: 3 -> 1 lost + 1 created = 3 -> scale 5 -> 5 running.""",
code=[("python", ["reconcile.py"])],
cmds=["python3 -I reconcile.py"],
notrun="**Not executed:** the real flow (no cluster, no API server, no etcd). What did run: `reconcile.py`, a toy of my own with a dictionary as the store and four loop functions. It models the shape of the control loop, not Kubernetes code or timing; real controllers use watches, caches and delays that this toy ignores.",
followups="""- **Where does the Service get its pod list?** The EndpointSlice controller builds endpoints from pods that match the selector and are Ready.
- **Who deletes a pod when you scale down?** The ReplicaSet controller picks pods to remove; the kubelet then stops them (with the grace period).
- **Why is a managed control plane attractive?** The provider runs and upgrades API server, etcd and scheduler; you still own node pools, add-ons and workloads.""",
mistakes="""- Saying the scheduler starts the containers. It only chooses a node; the kubelet starts them.
- Saying etcd down kills running pods. It stops changes and healing, not already-running containers.
- Confusing the controller manager with the scheduler.
- Treating `kubectl apply` as a command that runs something, instead of a request to store desired state."""))

# ---------------- Q17 ----------------
answers.append(render(17, "q17",
say="Give each team a namespace, bind small Roles to ServiceAccounts, and cap what a namespace can consume with a ResourceQuota and sane defaults with a LimitRange; RBAC only adds permissions, it never subtracts.",
explain="""- **Objects.** Namespace = a scope for names and policy. Role = permissions inside one namespace. ClusterRole = cluster-wide permissions or reusable ones. RoleBinding grants a Role (or ClusterRole) to users, groups or ServiceAccounts in one namespace. ClusterRoleBinding does it cluster-wide. ServiceAccount = identity for a pod.
- **Least privilege for a training pod.** Make a ServiceAccount, a Role with `get` on `secrets` limited by `resourceNames` to one Secret, and a RoleBinding. Better still: if the pod only needs the secret's value, mount it as an env var or volume in the pod spec; the kubelet delivers it and the pod needs no API permission at all. Set `automountServiceAccountToken: false` where the pod never calls the API.
- **Watch the verbs.** `list` and `watch` on secrets expose every secret value in the namespace. `resourceNames` cannot restrict `list` the way people expect (check the docs for the fieldSelector exception). Wildcards are a smell.
- **Escalate and bind.** To stop self-promotion, creating a Role or binding that grants permissions you do not have is refused unless you hold the special `escalate` (for roles) or `bind` (for bindings) verb. Give those only to platform admins, and when you must give `bind`, scope it with `resourceNames` to specific roles as in the manifest.
- **Quota and defaults.** ResourceQuota caps totals per namespace: CPU and memory requests, pod count, and extended resources with the `requests.` prefix, such as `requests.nvidia.com/gpu`. A pod that would push the namespace over is rejected at admission. LimitRange gives default requests and limits and max values per container, and is needed because a quota on CPU or memory requires every pod to state them.
- **Limits of this.** Namespaces are soft isolation: add NetworkPolicy, Pod Security settings and node pools for hard separation. A quota guards total GPUs per team; it does not prevent fragmentation or queue waiting.""",
example="""Quota: 4 GPUs for team-a. Jobs ask for 2, 1, 1, 1 GPUs. Running total 2, 3, 4, then the fourth job would need 5 > 4, so it is rejected (the toy prints 'exceeded quota requests.nvidia.com/gpu'). RBAC: `trainer` can `get` Secret `train-creds`, but not `db-admin`, not `list` secrets, not `update`, not `get` pods. Expected `kubectl auth can-i` answers (not executed): `get secrets/train-creds` yes, `list secrets` no.""",
code=[("yaml", ["team-a.yaml"]), ("python", ["rbac_check.py"])],
cmds=["kubernetes-validate --strict team-a.yaml", "python3 -I rbac_check.py team-a.yaml"],
notrun="**Not executed:** `kubectl auth can-i`, `kubectl apply`, real admission or quota enforcement (no cluster). What did run: `kubernetes-validate --strict` (schema only; it cannot tell a safe Role from a dangerous one) and `rbac_check.py`, my small model of `auth can-i` for namespaced Roles (API group, resource, verb, resourceNames) plus a risky-verb scan and a toy quota check. It models the rule shape, not the full RBAC engine.",
followups="""- **Role or ClusterRole plus RoleBinding?** A ClusterRole bound with a RoleBinding is limited to that namespace; this is how you reuse one definition for every team.
- **How do you audit who can do what?** `kubectl auth can-i --list --as=...`, plus reviewing bindings; on managed clusters also the provider's IAM mapping (check current docs).
- **Quota exceeded: how does the user see it?** The create call fails with a 'forbidden: exceeded quota' error naming the resource.""",
mistakes="""- Binding `cluster-admin` to a CI ServiceAccount 'for now'.
- `get, list, watch` on secrets when one `get` was enough.
- A CPU/memory quota with no LimitRange, then pods without requests are rejected and nobody knows why.
- Using the `default` ServiceAccount for everything.
- Thinking namespaces alone stop cross-team network traffic or node sharing."""))

# ---------------- Q18 ----------------
answers.append(render(18, "q18",
say="HPA changes how many pods, VPA changes how big each pod is, and Cluster Autoscaler changes how many nodes; they work at different layers and you combine them carefully.",
explain="""| Tool | What it scales | Trigger | Cost of acting |
|---|---|---|---|
| HPA | pod count | metric vs target (CPU, memory, custom, external) | new pods, cold start |
| VPA | pod CPU and memory requests (and limits) | observed usage history | pod restart in Auto/Recreate modes (newer versions may support in-place resize, check docs) |
| Cluster Autoscaler | node count | Pending pods that fit a new node; underused nodes | minutes for a node, more for GPU |

- **VPA parts.** The recommender reads usage (metrics server, optionally Prometheus history) and computes targets with bounds. The updater evicts pods whose requests are far from the target. The admission controller sets requests on new pods. `updateMode: "Off"` gives recommendations only, in the VPA object's status.
- **Why Auto mode is risky for ML.** It restarts pods to apply new sizes, so a model server reloads its weights and drops warm cache, and a restart storm hits you when usage shifts. Prefer `Off` and apply the numbers through your deploy pipeline, or use `Initial` (sets size only at pod creation).
- **VPA plus HPA conflict.** If both act on CPU or memory they chase each other: HPA adds pods because per-pod CPU is high while VPA raises the CPU request, which lowers the ratio. Use HPA on a custom metric (requests per second, queue length, latency) and VPA for resources, or VPA in recommendation mode only.
- **Cluster Autoscaler.** Sees Pending pods that cannot fit, simulates adding a node from a node group, and scales up. It removes nodes that stay underused when their pods can be moved. It works from pod REQUESTS, so wrong requests mean wrong node counts.
- **Right-sizing ML pods.** Memory is the dangerous resource: too low gives OOMKilled (exit 137); too high wastes expensive nodes. Request = limit for memory is a safe habit; CPU limits are debated. Base memory on peaks, not averages.""",
example="""Seven days of memory samples (MiB) for a scorer pod; the mean is about 1018 MiB but day 5 peaked at 1620 MiB during a big batch. A request at the mean would OOM on day 5. Peak-based recommendation: p90 of daily peaks (1620 here, because with 7 peaks p90 is the max) times 1.15 headroom = 1863, rounded up to 64 MiB steps = 1920 MiB. Check: 1620 x 1.15 = 1863; 1863 / 64 = 29.1, so 30 steps = 1920.""",
code=[("yaml", ["vpa.yaml"]), ("python", ["rightsize.py"])],
cmds=["kubernetes-validate --strict vpa.yaml; echo \"exit code: $?\"", "python3 -I rightsize.py"],
notrun="**Not executed:** VPA, HPA and Cluster Autoscaler themselves (add-ons and a cluster are needed). What did run: `kubernetes-validate` (it only warns that it has no schema for the VPA kind, because VPA is a CRD outside the core API, so the manifest is NOT schema-validated) and `rightsize.py`, which parses the manifest, checks `updateMode` by hand and computes a recommendation from made-up samples. The real VPA recommender uses decaying histograms, its own percentiles and safety margins (check its docs); my script is a simplified illustration.",
followups="""- **Pod was OOMKilled, what does VPA do?** It records the event and raises the memory recommendation; you still need a sane limit and a fix if memory leaks.
- **Which metric for HPA on an inference service?** Requests per second per pod or queue/latency signals beat CPU, especially for GPU-bound models (CPU stays low while the GPU is saturated).
- **Can you scale to zero with HPA?** Not in the standard setup; that is KEDA territory (next question group).""",
mistakes="""- HPA and VPA both on CPU for the same Deployment.
- VPA Auto on a model server with a slow warm-up.
- Sizing memory from averages.
- Expecting Cluster Autoscaler to react to high CPU usage; it reacts to Pending pods and requests.
- Setting requests far above real use 'to be safe', then paying for empty nodes."""))

# ---------------- Q19 ----------------
answers.append(render(19, "q19",
say="KEDA watches an external signal such as queue depth, drives an HPA for you, and can take a workload to zero and back, which a plain HPA cannot do.",
explain="""- **How it works.** You create a `ScaledObject` pointing at a Deployment, with triggers. KEDA's operator polls the signal (`pollingInterval`), creates and manages an HPA for 1 to N replicas using an external metric, and itself handles the 0 to 1 and 1 to 0 steps. Triggers exist for Kafka, SQS, Redis lists, Prometheus queries and many more (check the current scaler list).
- **Two thresholds.** The scaling target (for example `queueLength: 50` messages per pod) decides how many replicas: roughly `ceil(messages / target)`. The activation threshold decides whether to leave zero at all (for SQS `activationQueueLength`, default 0, so any message wakes it). `cooldownPeriod` is the wait with no activity before going to zero.
- **Why plain HPA cannot do zero.** HPA needs running pods to compute per-pod metrics and normally has a minimum of 1 (scale-to-zero exists only behind a feature gate in some versions, check docs). KEDA's activation step handles the empty case.
- **Cold-start cost for ML.** A GPU pod from zero needs: a node (maybe a scale-up of minutes), image pull, driver and plugin readiness, then model load. That can be tens of seconds to several minutes (hedged, depends on image and model size). For batch scoring that is fine. For latency-sensitive APIs keep `minReplicaCount: 1` (or more) and scale on latency or RPS.
- **Failure modes.** Kafka: replicas above the partition count do nothing. Queue consumers killed mid-message on scale-down: the message reappears after the visibility timeout, so make processing idempotent and give a graceful shutdown. Credentials in the trigger need a TriggerAuthentication. A flapping signal causes thrash: tune cooldown and the HPA scale-down behaviour. KEDA being down means no scaling from zero.""",
example="""Made-up inputs: target 50 messages per pod, each ready pod finishes 40 messages per tick (30 s), a new pod needs 4 ticks (2 min) to be ready, max 10. Messages arrive: 100 per tick for 4 ticks, then 400 per tick for 3 ticks. At the first tick with 100 messages the desired count is ceil(100/50) = 2; queue 400 gives 8; queue 720 gives 16, capped at 10. With `minReplicaCount: 0` the first message waits 120 s (the cold start); with 1 warm pod it is processed at once. After the burst, replicas stay up through the scale-down window and the cooldown before dropping to zero (the table shows 10 pods from tick 6, 8 pods at tick 20 and zero at tick 21).""",
code=[("yaml", ["scaledobject.yaml"]), ("python", ["keda_sim.py"])],
cmds=["python3 -I keda_sim.py",
      "python3 -I -c \"import yaml; d=yaml.safe_load(open('scaledobject.yaml')); s=d['spec']; print(d['kind'], 'min', s['minReplicaCount'], 'max', s['maxReplicaCount'], 'trigger', s['triggers'][0]['type'], 'target', s['triggers'][0]['metadata']['queueLength'])\""],
notrun="**Not executed:** KEDA, HPA, SQS and any real scaling (no cluster). The ScaledObject is also not schema-validated by `kubernetes-validate`, since it is a KEDA CRD; I only parsed it with PyYAML and printed key fields. Field and scaler names are from memory of KEDA's docs (hedge: check the current KEDA docs for your version). The simulation uses made-up numbers and simplified rules (a 10-tick scale-down window and 10-tick cooldown, i.e. 5 minutes each, as an assumption; check real defaults).",
followups="""- **ScaledObject or ScaledJob?** ScaledObject scales a long-running Deployment. ScaledJob creates a Job per batch of work, which suits long, non-restartable tasks.
- **How do you avoid losing in-flight work on scale-down?** Handle SIGTERM, finish or requeue the message, set `terminationGracePeriodSeconds`, and make processing idempotent.
- **Can KEDA scale on GPU utilisation?** Through a Prometheus trigger on a GPU metric, if you export one; for queue-based work the queue is usually the better signal.""",
mistakes="""- Scaling an API to zero and then being surprised by a slow first request.
- Kafka max replicas above the number of partitions.
- Confusing the activation threshold with the scaling target.
- Using CPU for a GPU-bound consumer and never scaling up.
- Putting cloud credentials in the ScaledObject instead of a TriggerAuthentication or workload identity."""))

# ---------------- Q20 ----------------
answers.append(render(20, "q20",
say="A Pending GPU pod makes the autoscaler add a node from a labelled, tainted GPU pool, and scale-down removes only nodes that look underused for a while and have nothing that blocks eviction; the real cost fight is idle nodes and slow starts.",
explain="""- **Node pool.** A group of identical nodes with min and max size, labels, taints and a GPU type, managed by the cloud. Cluster Autoscaler works per node group. Karpenter-style provisioners instead pick instance types dynamically from the Pending pods' needs (names and fields differ by version, check current docs). Taint the GPU pool so CPU pods stay away; GPU pods tolerate it and select the pool.
- **Scale-up.** The autoscaler sees a Pending pod, simulates 'would it fit on a new node of group X', and requests a node. It only helps if the pod would actually fit there (right taints, selector, size) and the pool is below max. If the pod needs 4 GPUs and nodes have 2, a new node does not help.
- **Time to useful.** Instance start, then driver and device plugin, then image pull (GPU images are big), then model load. In the toy I use 3 + 2 + 5 = 10 minutes as a made-up total. Plan for slow first minutes; warm pools or pre-pulled images shorten it (check your cloud).
- **Scale-down.** A node is a candidate when requested use is under a threshold and its pods can be moved, and it stays that way for a delay (a default of about ten minutes is common, check docs). Blockers: pods with no controller (bare pods), pods with local storage unless marked safe to evict, PodDisruptionBudgets that allow no disruption, a `safe-to-evict: "false"` annotation, system pods, and long training jobs you must not kill.
- **Spot or preemptible GPUs.** Cheaper but can vanish with short notice. Use them for work that checkpoints and resumes (see the Job in Q12), keep serving on stable capacity or mix pools, and handle the interruption signal.
- **Failure modes.** Pool at max leaves pods Pending forever. A forgotten notebook (bare pod) keeps a whole GPU node alive. Wrong requests make the autoscaler think nodes are full or empty. Scale-up works but model load makes the first requests time out.""",
example="""Made-up round numbers: 4 GPUs per node, pool 0 to 3 nodes. At t=0 a 4-GPU training pod and two 2-GPU serving pods are Pending. Hand-pack: 4 -> node 1; 2 + 2 -> node 2. So 2 nodes, ready at t=10. At t=40 a 1-GPU notebook (bare pod) needs a third node (ready at t=50). Training ends at t=60: node 1 is empty, marked unneeded, removed at t=70. At t=80 serving is removed: node 2 empty, removed at t=90. Node 3 holds only the bare notebook at 25 percent use and stays, because it cannot be evicted. Billed node-minutes 241 versus 360 for 3 static nodes over 120 minutes (nodes are billed from creation, not from ready).""",
code=[("yaml", ["gpu-workloads.yaml"]), ("python", ["ca_sim.py"]), ("bash", ["ca_flags.sh"])],
cmds=["kubernetes-validate --strict gpu-workloads.yaml", "python3 -I ca_sim.py", "bash -n ca_flags.sh && echo 'bash -n ca_flags.sh: syntax OK'"],
notrun="**Not executed:** any cloud node group, Cluster Autoscaler, Karpenter, GPU node or real timing (no cluster, no cloud). Flag names in `ca_flags.sh` are only syntax-checked with `bash -n`; defaults and flags change by version and cloud, check the current docs. What did run: `kubernetes-validate --strict` on the manifests (schema only) and `ca_sim.py`, my own simulation of scale-up, scale-down and blockers with the made-up numbers above. It models the rules, not the real autoscaler code.",
followups="""- **How do you keep one GPU node warm for latency?** Keep a minimum of 1 in the pool for serving (or a low-priority placeholder pod that gets preempted), accept the cost of that one node.
- **Cluster Autoscaler or Karpenter?** Autoscaler is group-based and common; Karpenter-style tools choose instance types per pod demand. Pick by cloud support and your control needs; check current docs.
- **How do you stop training pods being evicted?** Annotate against eviction and use a PDB for serving, but also checkpoint, because nodes can still fail or be preempted.""",
mistakes="""- Letting bare pods and notebooks run on the GPU pool.
- No taint on the GPU pool, so CPU pods land there and keep it alive.
- Counting only GPU price and ignoring 10 or more minutes of startup.
- Pool max too low, so Pending never clears.
- Using spot GPUs for jobs that cannot resume."""))
