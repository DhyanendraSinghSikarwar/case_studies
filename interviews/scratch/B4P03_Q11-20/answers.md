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
