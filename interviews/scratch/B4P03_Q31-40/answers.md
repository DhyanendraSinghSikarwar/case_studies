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
