answers.append(render(21, "q21",
say="A GPU is one integer unit by default; time-slicing lets several pods share one GPU with no memory or fault walls, MIG cuts a supported GPU into hardware-isolated slices, and I pick by how much isolation the workload needs.",
explain="""
- **Device plugin and GPU Operator.** The NVIDIA device plugin is a DaemonSet on GPU nodes. It tells the kubelet "this node has N `nvidia.com/gpu`". Kubernetes sees only whole integers, no fractions. The GPU Operator installs the pieces for you: driver, container toolkit, device plugin, GPU feature discovery labels, DCGM metrics, MIG manager. Check current docs for versions.
- **Whole GPU.** Best for training and big models. Full memory, full speed, no neighbours.
- **Time-slicing.** You set `replicas: 4` in a config. The node then advertises 4 `nvidia.com/gpu` for one physical GPU. Pods take turns on the GPU. **No memory limit and no fault isolation.** One pod can eat all VRAM and the rest crash. Good for notebooks and small dev inference. Asking for 2 does not promise 2 different physical GPUs.
- **MIG (Multi-Instance GPU).** On supported data-centre GPUs, one card is split into hardware-isolated instances, each with its own memory and compute. Each profile gets its own resource name, such as `nvidia.com/mig-1g.10gb` (names depend on GPU and strategy: check current docs). Changing the layout needs the node drained of GPU pods. Good for small models with strict isolation, many tenants.
- **MPS.** CUDA's Multi-Process Service lets several processes share the GPU at the same time (not just turns). Some device plugin versions can enable it; support and limits vary, so check current docs.
- **Failure modes:** a time-sliced pod OOMs its neighbours; a model bigger than the MIG slice never loads; one pool mixes MIG and non-MIG nodes with no node labels, so pods land wrong; no taint on GPU nodes, so CPU pods squat there.
""",
example="""GPU has 40 GB (made-up). Time-slicing x4 means an even share of 10 GB, but nothing enforces it. Four models of 6 GB use 24 GB; with 20% headroom that is 28.8 GB, fine. If one model is 18 GB, the sum with headroom is 43.2 GB, over the pool, so the script flags OOM risk. On MIG, a 7 GB model with headroom needs 8.4 GB: a `1g.5gb` slice (5 GB) is a hard no, a `2g.10gb` slice fits.""",
code=[("yaml", ["gpu_share.yaml"]), ("python", ["vram_fit.py"])],
cmds=["python3 -I vram_fit.py", KV.format(f="gpu_share.yaml")],
notrun="**Not executed:** the device plugin, GPU Operator, time-slicing and MIG need a GPU node and a cluster. Nothing here talks to a GPU. What did run: the VRAM script (it also parses the ConfigMap's embedded YAML and reads `replicas`), and `kubernetes-validate --strict` on the ConfigMap and Pod (kubernetes-validate 1.37.0). The validator checks schema only; it cannot know whether `nvidia.com/mig-1g.10gb` exists on your nodes.",
followups="""
- **Can I get a fraction of a GPU with a plain request?** No. `nvidia.com/gpu` is an integer. Fractions come from time-slicing replicas, MIG, MPS, or newer Dynamic Resource Allocation (DRA), whose status depends on your Kubernetes version.
- **Time-slicing or MIG for multi-tenant?** MIG, because of memory and fault isolation. Time-slicing is for trusted users and dev work.
- **Why taint GPU nodes?** So only pods that tolerate `nvidia.com/gpu` land on them; otherwise cheap CPU pods use the expensive node.
""",
mistakes="""
- Calling time-slicing "isolation". It is sharing in turns; memory is shared.
- Assuming every GPU supports MIG. Only some data-centre models do; check the support matrix.
- Copying resource names from a blog. MIG names depend on the GPU model and MIG strategy.
- Forgetting headroom for activations, CUDA context and caches when sizing slices.
""")) 

answers.append(render(22, "q22",
say="Helm renders Go templates with values into plain YAML; I keep logic small, use `default`, `required`, `toYaml | nindent` and `with`/`if` guards, and let `values.schema.json` reject bad values before anything is rendered.",
explain="""
- **Syntax.** `{{ .Values.x }}` reads a value. A pipe passes it on: `{{ .Values.image.tag | default .Chart.AppVersion | quote }}`. `quote` makes it a YAML string (saves you from `on`, `1.10` or `0123` being read as other types).
- **Blocks.** `{{- if ... }}` / `{{- end }}` for options, `{{- with .Values.tolerations }}` to render only when set (and rebind `.`), `{{- range ... }}` to loop. Inside `with` and `range`, `.` changes. Use `$.Values` to reach the root.
- **Whitespace.** `{{-` trims spaces and newline before, `-}}` after. Lists and maps: `{{- toYaml . | nindent 8 }}` prints YAML, starts a new line and indents by 8. Wrong indent = wrong YAML, the most common template bug.
- **Helpers.** `_helpers.tpl` holds named templates (`define "model-api.labels"`). `include "name" . | nindent 4` returns a string you can pipe. `template` prints directly, so it cannot be piped.
- **Fail early.** `required "message" .Values.modelUri` stops the render with that message. `values.schema.json` (JSON Schema) is checked on install, upgrade, lint and template, so wrong types, bad enums and out-of-range numbers fail before manifests are built. Schema checks shape; `required` checks "was it really set".
- **Failure modes:** `default` treats `0`, `false` and `""` as unset, so `default true .Values.flag` can never be false; a list in an override file **replaces** the base list (maps merge); big integers from `--set` can print as floats unless you wrap them in `int`; `kubectl apply` of a template with a stray tab fails only at install time unless you lint and validate.
""",
example="""Values: `gpu.count: 1`. The guard `{{- if gt (int .Values.gpu.count) 0 }}` adds the line `nvidia.com/gpu: 1` under `limits`. With `gpu.count: 0` that line is absent, so the pod can run on CPU nodes. If someone sets `gpu.count: "two"` the schema rejects it. If `modelUri` is empty, `required` stops the render with the message.""",
code=[("yaml", ["chart/Chart.yaml", "chart/values.yaml"]),
      ("gotemplate", ["chart/templates/_helpers.tpl", "chart/templates/deployment.yaml"]),
      ("json", ["chart/values.schema.json"]),
      ("python", ["render_check.py"])],
cmds=["python3 -I render_check.py"],
notrun="**Not executed:** `helm lint`, `helm template` and `helm install` (helm is not installed here and could not be downloaded). So the Go template itself was **never rendered by Helm**. What did run: `render_check.py` is a hand-written Python **mirror** of the template logic (not Helm). It validates values against the real `values.schema.json` with the jsonschema library, produces the Deployment the template is meant to produce, and runs `kubernetes-validate --strict` on that output. It also greps the template text for the guards. Treat it as a model of the template, and run `helm lint` and `helm template` on a real machine.",
followups="""
- **Schema or `required`?** Both. Schema for types and ranges, `required` for "must be set" and for a helpful message.
- **Why is my YAML mis-indented?** Probably `nindent` count is wrong or you used `indent` without a leading newline. Run `helm template` and read the output.
- **How do I debug a template?** `helm template --debug`, `helm lint`, and `--dry-run`.
""",
mistakes="""
- Using `with` and then reading `.Values` inside it (dot has changed; use `$.Values`).
- Not quoting values that must be strings, such as image tags like `1.10`.
- Putting secrets in `values.yaml` in git.
- Writing a schema that is too strict on optional fields, so every upgrade breaks.
- Saying "I tested the template" when only a Python mirror ran.
"""))

answers.append(render(23, "q23",
say="I upgrade with `helm upgrade --install --atomic --wait --timeout`, review a `helm diff` first, keep one chart with per-environment values files, and remember rollback restores manifests only, not data or external state.",
explain="""
- **The command.** `helm upgrade --install` creates the release if missing and upgrades otherwise, so CI uses one command. `--wait` waits until pods are Ready. `--timeout` caps the wait. `--atomic` rolls back automatically if the upgrade fails (it implies waiting). `--dry-run` renders without applying; the `helm diff` plugin (install separately) shows what would change against the live release.
- **History.** Helm 3 stores each revision as a Secret in the release namespace. `helm history` lists them (default history cap is about 10; check current docs). `helm rollback NAME REV` makes a **new** revision with the old manifests.
- **What rollback does not undo.** Database or schema migrations, model files in object storage, PVC contents, a Job that already ran, anything created by hooks (hook resources are not part of the release manifest). If the new model wrote data in a new format, rollback of pods will not fix it.
- **Hooks.** Annotations such as `helm.sh/hook: pre-upgrade` run a Job before the upgrade. Useful for migrations. Pitfalls: a failed hook fails the release; the hook Job is not rolled back; leftover Jobs block re-runs unless you set `helm.sh/hook-delete-policy`; hooks must be idempotent; ordering uses `hook-weight`.
- **Per-environment values.** One chart, `-f values-dev.yaml` or `-f values-prod.yaml`. Later files win; maps merge, lists replace. Keep the same key set everywhere so no environment silently falls back to a default.
- **Failure modes:** an interrupted upgrade leaves the release in `pending-upgrade`, and the next upgrade says another operation is in progress (fix with rollback, or inspect the release Secrets; check current docs); `--atomic` with a too-short timeout rolls back a healthy but slow model load; `--wait` does not prove the model gives good predictions.
""",
example="""`values-prod.yaml` has `gpu.type: a100` but `values-dev.yaml` does not. The key check script reports `gpu.type` missing in dev. Either add it to the base `values.yaml` with a default or remove it. Otherwise the template that reads `.Values.gpu.type` renders `<nil>` or empty in dev only.""",
code=[("yaml", ["values-dev.yaml", "values-prod.yaml"]), ("bash", ["deploy.sh"]), ("python", ["check_values.py"])],
cmds=["python3 -I check_values.py values-dev.yaml values-prod.yaml", "bash -n deploy.sh && echo \"bash -n: syntax ok\"", "command -v helm || echo \"helm: not installed\""],
notrun="**Not executed:** every `helm` command (helm lint, template, diff, upgrade, history, rollback) because helm is not installed here and its download was blocked. So `deploy.sh` is shown, not run. What did run: the key-drift script on the two values files (exit code 1 on drift is the point: CI should fail), and `bash -n` (syntax check only).",
followups="""
- **`--atomic` or `--wait`?** `--atomic` includes the wait and adds auto-rollback. In CI I use `--atomic`.
- **Why `helm diff`?** To see the real change before it lands, including values that moved by accident.
- **How do I roll back a model?** Roll back the release (old image or model URI), then check data and caches yourself.
""",
mistakes="""
- Believing rollback restores the database or the model registry.
- Running migrations in a hook that is not idempotent, or not deleting finished hook Jobs.
- Different keys per environment, so prod behaves differently from what staging proved.
- A timeout shorter than model load time, causing needless rollbacks.
- Using `latest` image tags: a rollback then re-pulls the same bits.
"""))

answers.append(render(24, "q24",
say="On shutdown Kubernetes sends SIGTERM, waits up to the grace period, then SIGKILL; so the server must stop taking new work, finish in-flight requests and exit, with a PodDisruptionBudget limiting how many pods voluntary drains can take at once.",
explain="""
- **PDB.** Limits **voluntary** disruptions: `kubectl drain`, autoscaler scale-down, upgrades. `minAvailable: 2` (or `maxUnavailable`) makes the eviction API refuse to go below that. It does **not** stop node crashes, OOM kills or spot reclaim.
- **Cordon and drain.** `cordon` marks the node unschedulable. `drain` cordons and evicts pods, respecting PDBs. DaemonSet pods need `--ignore-daemonsets`; emptyDir data is lost, so `--delete-emptydir-data` is required.
- **Shutdown sequence.** Pod goes Terminating, it is removed from Service endpoints, the `preStop` hook runs, then SIGTERM goes to each container's main process. After `terminationGracePeriodSeconds` (default 30 s, counted from the start of termination, preStop included) comes SIGKILL.
- **Why traffic still arrives.** Endpoint removal spreads to kube-proxy, ingress and mesh proxies **asynchronously**, so for a moment requests still land. A short `preStop: sleep` (and failing readiness on SIGTERM) bridges the gap, then the app drains.
- **PID 1 trap.** If the app is behind `sh -c`, the shell may not forward SIGTERM. Use `exec`, or a tiny init such as tini. A process that is PID 1 in a container gets no default SIGTERM action, so without a handler it is just killed later by SIGKILL.
- **Long training pod.** A drain evicts it like any pod. Without a checkpoint it loses progress. Save a checkpoint on SIGTERM (and keep the grace period long enough), checkpoint on a schedule, and use the cluster's "do not evict" annotation for work that cannot move (names vary by autoscaler; check current docs).
- **Failure modes:** `minAvailable` equal to replicas gives zero allowed disruptions, so drains hang forever; a grace period shorter than preStop plus drain time truncates requests; one replica plus a PDB blocks node upgrades.
""",
example="""3 replicas, `minAvailable: 2`, so 1 pod may be evicted at a time. Drain node A: pod 1 gets Terminating, `sleep 10` in preStop, SIGTERM, finishes its 3 requests, exits 0. Only after it is gone and a replacement is Ready can the next eviction proceed. Grace is 60 s, which covers 10 s sleep plus drain time.""",
code=[("yaml", ["serve_pdb.yaml"]), ("python", ["graceful.py"])],
cmds=["python3 -I graceful.py", KV.format(f="serve_pdb.yaml")],
notrun="**Not executed:** drain, cordon, eviction and PDB enforcement (no cluster). What ran for real: a Python subprocess that gets a real SIGTERM, once with a handler that drains and once with default handling (killed by signal 15, shown as exit code -15 by Python). The YAML was validated with `kubernetes-validate --strict`. Note that this test runs the process as a normal child, not as PID 1 in a container.",
followups="""
- **Does a PDB protect me from a node failure?** No, only voluntary evictions.
- **How long should the grace period be?** Longer than preStop plus the slowest request you accept to finish.
- **How do I keep a rolling update from dropping traffic?** `maxUnavailable: 0`, a real readiness probe, preStop and SIGTERM draining.
""",
mistakes="""
- No SIGTERM handler, so requests die at SIGKILL.
- `minAvailable` equal to the replica count, which blocks drains.
- Setting a long grace period but not handling SIGTERM, so every rollout waits the full time.
- Readiness probe that stays green while the server is shutting down.
"""))

answers.append(render(25, "q25",
say="For a latency-sensitive service I spread replicas across zones with topology spread, prefer one pod per node with soft anti-affinity, and give serving a higher PriorityClass than batch, while watching that hard rules can leave pods Pending.",
explain="""
- **Node affinity** picks nodes by node labels (GPU type, zone). **Pod affinity** pulls pods together (near a cache). **Pod anti-affinity** pushes pods apart (spread replicas).
- **Required or preferred.** `requiredDuringScheduling...` is a hard rule: no match, pod stays Pending. `preferredDuringScheduling...` is a weighted wish. "IgnoredDuringExecution" means it is checked only at scheduling time.
- **topologySpreadConstraints.** `maxSkew: 1` over `topology.kubernetes.io/zone` keeps zone counts within 1 of each other. `DoNotSchedule` is hard, `ScheduleAnyway` is soft. Skew = pods in this zone minus pods in the emptiest eligible zone.
- **PriorityClass.** Higher number wins. When a high-priority pod cannot fit, the scheduler may **preempt** (evict) lower-priority pods. Give batch `preemptionPolicy: Never` so batch never kicks others out. Evicted batch pods must tolerate restarts (checkpoints).
- **Failure modes:** hard anti-affinity with replicas greater than nodes leaves pods Pending; with a rolling update `maxSurge: 1` the extra pod also needs a free node, so rollouts stall; a hard zone spread with one zone lacking capacity leaves pods Pending even when other zones have room; preemption can kill a long training run.
""",
example="""3 nodes in zones a, b, c and 3 replicas: one per zone, nothing Pending (scenario A). 2 nodes and 3 replicas with HARD one-per-node anti-affinity: 1 pod Pending (C). 3 nodes, 3 replicas, hard anti-affinity, rolling update with one surge pod makes 4 pods: 1 Pending until an old pod terminates (D). That is why I use soft anti-affinity plus topology spread for the day-to-day rule.""",
code=[("yaml", ["spread.yaml"]), ("python", ["spread_check.py"])],
cmds=["python3 -I spread_check.py", KV.format(f="spread.yaml")],
notrun="**Not executed:** scheduling, preemption and anything on a cluster. What ran: a pure-Python placement model (my simplification: one pod at a time, skew check, optional one-pod-per-node rule, per-node slot limit; the real scheduler also scores nodes and handles many more cases) and `kubernetes-validate --strict` on the manifests.",
followups="""
- **Spread or anti-affinity?** Topology spread is the modern, more flexible tool; anti-affinity is simple "not with my own kind".
- **What if I have fewer nodes than replicas?** Use `ScheduleAnyway` or preferred rules, or add nodes.
- **Can preemption bite me?** Yes. Pods of lower priority get SIGTERM and rescheduled; make batch resumable.
""",
mistakes="""
- Hard anti-affinity per node with `replicas` above the node count.
- Forgetting that a zone with no nodes is ignored, so the spread can look fine and still sit in two zones.
- A PriorityClass with `globalDefault: true` on a high value, so everything outranks everything.
- Label selectors in the constraint that do not match the pod's own labels (spread does nothing).
"""))
