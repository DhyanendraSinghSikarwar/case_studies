answers.append(render(26, "q26",
say="Every pod gets its own IP on a flat network, a Service gives a stable virtual IP and DNS name that kube-proxy turns into a pod IP, and NetworkPolicy is how I stop other namespaces from reaching the model API, if the CNI enforces it.",
explain="""
- **Flat network.** Each pod has an IP and can reach any other pod IP without NAT. The CNI plugin builds that. Pod IPs change when pods restart, so you never hard-code them.
- **Service.** A ClusterIP is a virtual IP. kube-proxy (iptables, IPVS, or an eBPF replacement in some CNIs) turns it into one of the Ready pod IPs listed in EndpointSlices. Only Ready pods are listed.
- **DNS.** CoreDNS names a Service `model-api.ml-serving.svc.cluster.local`. In the same namespace `model-api` is enough; across namespaces use `model-api.ml-serving`. A **headless** Service (`clusterIP: None`) returns the pod IPs directly; StatefulSets use it for per-pod names.
- **NetworkPolicy.** Allow-lists only. Once any policy selects a pod for Ingress, that pod accepts only what some policy allows. Default-deny is `podSelector: {}` with no rules. Then add an allow rule for the gateway.
- **CNI support.** Policies are enforced by the CNI. Some CNIs (Calico, Cilium and others) enforce them; a basic one may accept the YAML and silently do nothing. Check your CNI.
- **Failure modes:** `namespaceSelector` and `podSelector` in the **same** `from` item are AND; as two separate items they are OR (a classic leak); default-deny **egress** also blocks DNS unless you allow port 53 to kube-system; the gateway namespace needs the `kubernetes.io/metadata.name` label (set automatically on current versions); probes and node traffic handling differs by CNI.
""",
example="""Policies: default-deny plus "allow envoy pods from namespace `gateway` to port 8080". Results from the script: envoy to 8080 is allowed; envoy to 9000 is denied (port); a notebook in `research` is denied (namespace); a non-envoy pod in `gateway` is denied (pod label). A namespace with no policy stays fully open, which is why default-deny is applied per namespace.""",
code=[("yaml", ["netpol.yaml"]), ("python", ["policy_eval.py"])],
cmds=["python3 -I policy_eval.py", KV.format(f="netpol.yaml")],
notrun="**Not executed:** real enforcement (needs a cluster and a CNI that supports NetworkPolicy), DNS and kube-proxy. What ran: my simplified ingress-only evaluator (ignores egress, ipBlock, named ports) and `kubernetes-validate --strict` on all four objects.",
followups="""
- **Why can't pod A reach pod B after default-deny?** No allow rule matches; add one for the right source and port.
- **ClusterIP versus headless?** ClusterIP load-balances behind one virtual IP; headless exposes each pod IP in DNS.
- **How do I test a policy?** From a debug pod in the source namespace run curl and check the result; on a real cluster only (not executed here).
""",
mistakes="""
- Assuming NetworkPolicy works on any cluster.
- Mixing up AND and OR in `from` lists.
- Applying default-deny egress and then wondering why DNS lookups fail.
- Expecting a policy in one namespace to protect other namespaces.
"""))

answers.append(render(27, "q27",
say="I walk the path from the outside in: do the pods match the Service selector, are they Ready so endpoints are not empty, do the ports line up, is the app bound to 0.0.0.0, then NetworkPolicy and Ingress, and I bypass the Service with a port-forward to split the problem.",
explain="""
- **1. Labels.** `kubectl get pods --show-labels` against `svc.spec.selector`. A typo (`modelapi` vs `model-api`) gives empty endpoints and no error.
- **2. Endpoints.** Empty EndpointSlices means no **Ready** pod matches. Running is not Ready: the readiness probe decides.
- **3. Ports.** Service `port` is what clients call; `targetPort` must be the port the app listens on; `containerPort` is documentation but good to keep equal. A readiness probe on the wrong port keeps pods NotReady forever.
- **4. Bind address.** An app on `127.0.0.1` answers inside the pod (so `exec curl localhost` works) and nothing from outside. Bind `0.0.0.0`.
- **5. Split the problem.** `port-forward` to the pod works but the Service does not: Service or policy problem. Pod answers on port-forward but not from another pod: bind address or NetworkPolicy.
- **6. Then Ingress and policy.** Ingress path rewrite (the app sees `/v1/predict` but gets `/`), wrong backend port, TLS. NetworkPolicy default-deny with no allow.
- **Failure modes:** looking at logs first when the app is fine; trusting "Running"; forgetting that a rolling update can leave old and new labels mixed.
""",
example="""The broken sample has four bugs at once: Service selects `app=model-api` but pods are `app=modelapi`; `targetPort` 8000 but the app listens on 8080; readiness probe on 9090; app started with `--host 127.0.0.1`. The script reports all four. The fixed file reports none.""",
code=[("yaml", ["broken.yaml"]), ("python", ["svc_check.py"]), ("bash", ["debug.sh"])],
cmds=["python3 -I svc_check.py broken.yaml fixed.yaml", KV.format(f="broken.yaml"), "bash -n debug.sh && echo \"bash -n: syntax ok\"", "command -v kubectl || echo \"kubectl: not installed\""],
notrun="**Not executed:** every `kubectl` command in `debug.sh` (no kubectl, no cluster). What ran: the static cross-check script on `broken.yaml` and `fixed.yaml` (`fixed.yaml` is the same file with the four bugs corrected; it is not pasted), `kubernetes-validate --strict` (note both files pass: the schema cannot see these logic bugs, which is exactly why the cross-check exists), and `bash -n` on the script. Static checks catch config mismatches only; they cannot see a bad bind address set inside the image or a policy on the cluster.",
followups="""
- **Endpoints empty but pods Running?** Selector mismatch or readiness failing.
- **Works with port-forward, fails via Service?** Service ports, selector or NetworkPolicy.
- **Works from inside the cluster, fails via Ingress?** Ingress backend, path rewrite, host or TLS.
""",
mistakes="""
- Reading logs for 30 minutes before comparing labels.
- Confusing `port`, `targetPort` and `containerPort`.
- Binding the dev server to `localhost` (the default in many frameworks).
- Debugging through the Ingress when the Service itself is broken.
"""))

answers.append(render(28, "q28",
say="For a big model I trade start time, node disk and version consistency: baking into the image is simple, an init container to an emptyDir is flexible, a node cache or a shared read-only volume is faster on repeat starts, and I always pin an immutable version.",
explain="""
- **Bake into image.** One artefact, versions match the code. But the image is huge, slow to pull on a cold node, and every model change is a new image.
- **Init container + emptyDir.** Small image; an init container fetches from object storage, verifies a checksum, and the server reads the shared `emptyDir`. Every pod re-downloads on start. `emptyDir` uses node ephemeral storage, so set `sizeLimit` and an `ephemeral-storage` request or the node hits disk pressure and evicts pods.
- **Node-local cache.** A DaemonSet pre-pulls into a `hostPath` so later pods on that node start fast. Costs: hostPath is a security and cleanup problem, cache invalidation is yours.
- **Shared volume.** ReadOnlyMany or ReadWriteMany PVC (needs a storage class that supports it; check your cloud). No per-pod download, but all pods hit one storage backend, and its throughput is shared.
- **Stream weights.** Some servers can load straight from object storage during start-up, overlapping download and load. Less disk, but start time depends on the network.
- **Newer option.** Recent Kubernetes versions added an image volume source to mount an OCI artifact as a read-only volume; it was feature-gated at first. Check current docs before relying on it.
- **Failure modes:** `latest` in the model URI so replicas created at different times load different models; startup probe too short, so the pod is killed mid-load; many pods starting at once overload the object store (thundering herd).
""",
example="""Made-up numbers: 20 GB model, 4 replicas on 4 nodes, shared source cap 2 GB/s. Cold image pull of 22 GB at (0.5 GB/s each) gives 44 s, plus 20 s load: 64 s. Init container: 4 s image + 40 s download + 20 s load: 64 s. Node cache hit: 4 + 10 + 20 = 34 s. Baked image already cached on the node: just the 20 s load. The point is the ranking and what dominates, not the seconds.""",
code=[("yaml", ["init_model.yaml"]), ("python", ["cold_start.py"])],
cmds=["python3 -I cold_start.py", KV.format(f="init_model.yaml")],
notrun="**Not executed:** the pods, the download and any real timings. All sizes and bandwidths in `cold_start.py` are made-up assumptions, so the seconds are arithmetic, not measurements. What ran: the estimator and `kubernetes-validate --strict` on the Deployment.",
followups="""
- **Which is best?** There is none. Image for small models; shared volume or cache for many replicas; init container as a simple default.
- **How do I keep replicas on the same version?** Pin an immutable path or digest in the manifest; roll out through the Deployment.
- **What about autoscaling?** New replicas pay the cold-start cost, so slow start means slow scale-up; keep a warm minimum.
""",
mistakes="""
- No `sizeLimit` or ephemeral-storage request on the emptyDir.
- No checksum check after the download.
- `latest` as the model version.
- Startup probe budget shorter than the real load time.
"""))

answers.append(render(29, "q29",
say="KServe turns \"serve this model\" into one InferenceService resource: it creates the serving pods, pulls the model from storageUri, wires autoscaling and canary traffic, so you do not hand-write the Deployment, Service and HPA, at the price of extra moving parts.",
explain="""
- **InferenceService.** Has a **predictor** (the model server), and optionally a **transformer** (pre and post processing) and **explainer**. The predictor names a `modelFormat` (sklearn, a Triton model, and so on) and a `storageUri`. A runtime is chosen for that format, and a storage initializer fetches the model into the pod.
- **Modes.** In Serverless mode it sits on **Knative** (scale-to-zero, concurrency-based autoscaling, revisions) and usually a service mesh or gateway. In raw deployment mode it makes plain Deployments with an HPA: simpler, but no scale-to-zero (HPA cannot go to zero). Which features work in which mode depends on the version; check current docs.
- **Canary.** `canaryTrafficPercent: 10` sends 10% to the newest revision and 90% to the last good one. Raise it step by step, then remove the field to promote. Setting it to 0 sends all traffic to the previous revision, which is how you back off (check current docs for exact behaviour).
- **What you gain over Deployment + Service + HPA:** one resource per model, standard model download, revisions and traffic splitting, scale-to-zero, a common inference protocol, a pluggable runtime list.
- **What it costs:** Knative and often Istio or another gateway to run and upgrade, CRDs, extra debugging layers, version coupling. For one or two models a plain Deployment may be easier.
- **Failure modes:** scale-to-zero plus a slow model load makes the first request slow or time out; `storageUri` pointing at a path without credentials fails in the storage initializer (check the init container logs); canary without a previous good revision has nothing to split to; the field names changed between versions.
""",
example="""Rollout of fraud model v4 with `canaryTrafficPercent: 10`: traffic is 10% new, 90% previous. Metrics look fine, move to 50, then remove the field: 100% latest. If errors rise at 10%, set it to 0: all traffic goes back to the previous revision without redeploying the old model (the old revision is still there).""",
code=[("yaml", ["isvc.yaml"]), ("python", ["isvc_check.py"])],
cmds=["python3 -I isvc_check.py", KV.format(f="isvc.yaml")],
notrun="**Not executed:** KServe, Knative and Istio are not installed, so nothing was created and no traffic was split. The manifest follows commonly documented v1beta1 fields; **check current docs for the schema** of your KServe version. What ran: my own required-field checker (a short list I wrote, not the real CRD schema) and the traffic arithmetic. `kubernetes-validate --strict` printed only a **warning**: it has no schema for the InferenceService CRD, so exit code 0 here proves nothing about this manifest.",
followups="""
- **Why not just a Deployment?** One model, one team: a Deployment is fine. Many models, canaries, scale-to-zero: KServe pays off.
- **Can it scale to zero on GPU?** It can, but the cold start (load weights, GPU init) can take tens of seconds or more, so many keep one warm replica.
- **Where do models come from?** `storageUri` (object store, PVC and others); the init step downloads them.
""",
mistakes="""
- Treating the validator's exit 0 as success for a CRD it has no schema for.
- Copying a manifest from a blog written for another KServe version.
- Scale-to-zero on a latency-critical model with a slow load.
- No pinned model version in `storageUri`.
"""))

answers.append(render(30, "q30",
say="Distributed training on Kubernetes needs all pods of a job to start together, so I use a PyTorchJob for the pods, a queue such as Kueue to admit the whole job against quota, checkpointing for restarts, and I watch /dev/shm and NCCL settings.",
explain="""
- **PyTorchJob.** A custom resource from the Kubeflow Training Operator: a Master and N Workers. The operator creates the pods and injects the distributed env (master address, world size, rank). A job for 8 GPUs at 2 GPUs per pod is 4 pods.
- **Gang scheduling.** Pods are scheduled one at a time by default. Two big jobs can each grab half the GPUs and both wait forever for the rest: a deadlock holding GPUs. Gang scheduling (all or nothing) avoids it. Options: Kueue (admits a job only when its whole ask fits quota), Volcano, or scheduler plugins.
- **Kueue.** You define a ResourceFlavor, a **ClusterQueue** with quota (for example 8 GPUs), and a namespaced **LocalQueue**. A job labelled with the queue name stays suspended until quota is free. Quota is bookkeeping, not capacity: a job can be admitted and its pods still be Pending if the nodes are missing.
- **Node loss and restarts.** Use a restart policy suited to the job, write checkpoints to a PVC or object storage, and resume with auto-detect on start. Without that, one lost node restarts from step 0.
- **Pitfalls.** `/dev/shm` is tiny by default, so PyTorch dataloader workers crash; mount a memory `emptyDir` there. NCCL needs pods to reach each other, the right network interface and (for fast links) RDMA setup; use `NCCL_DEBUG` to diagnose. Mixed GPU types in one job make the slowest set the speed.
- **Failure modes:** partial start deadlock; quota says yes but no nodes; a worker is evicted by preemption or spot reclaim and the whole job restarts; checkpoints written to local disk vanish with the node.
""",
example="""Job: 1 Master + 3 Workers, 2 GPUs each = 8 GPUs. Queue quota 8. Empty queue: admit. 2 GPUs already used: the script says wait, short by 2 (it stays queued rather than starting 3 pods and blocking). Gang demo: 4 free GPUs, two jobs each needing 4. Without gang, each gets one pod and both wait forever (deadlock). With gang, job A runs and B waits.""",
code=[("yaml", ["train.yaml"]), ("python", ["quota_fit.py"])],
cmds=["python3 -I quota_fit.py", KV.format(f="train.yaml")],
notrun="**Not executed:** Kubeflow Training Operator, Kueue, Volcano, GPUs, NCCL and any training. The YAML is a **sketch**: CRD field names and API versions change between releases; check current docs. What ran: the quota-fit script and a toy gang-versus-no-gang model (my simplification). `kubernetes-validate --strict` only printed warnings: it has no schemas for these CRDs, so exit code 0 proves nothing about them.",
followups="""
- **Why not plain Jobs?** Plain Jobs have no gang start and no rank setup; the operator handles both for PyTorch.
- **Kueue or Volcano?** Both queue and gang-schedule. Kueue works with the default scheduler; Volcano brings its own. Pick by what your platform already runs.
- **Spot nodes?** Fine if you checkpoint often and accept restarts.
""",
mistakes="""
- Default `/dev/shm` size.
- Checkpoints on local disk.
- Assuming queue quota guarantees free nodes.
- Treating a validator warning on CRDs as a pass.
"""))
