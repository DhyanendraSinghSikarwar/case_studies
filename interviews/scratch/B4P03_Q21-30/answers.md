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
