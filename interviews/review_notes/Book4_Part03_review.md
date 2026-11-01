# Book 4 Part 3 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40 (Kubernetes basics for ML, Helm, autoscaling). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40; star order and counts 15 / 16 / 9 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 40 |

Code was run by each agent with `python3 -I` and `kubernetes-validate --strict`; the pasted outputs come from those runs (scripts and manifests are in each agent's `code/` folder). The lead did not re-run the scripts this part, because they take file arguments and sibling manifests (same limitation as Part 2).

## What really ran
No kubectl, helm or cluster exists here (a binary download was blocked by the permission system and was not worked around). Ran for real: `kubernetes-validate --strict` 1.37.0 on core manifests; Python models of the ReplicaSet loop, QoS classes, crash-loop backoff, OOMKilled vs Evicted, scheduler events, HPA formula with tolerance and stabilisation, rolling-update arithmetic, toleration matching, StatefulSet naming, a reconcile loop, a Prometheus text parser with histogram p95 interpolation, a removed-API scanner, RBAC and quota checkers, a cluster-autoscaler toy; `jsonschema` on a values schema; `bash -n` on shell scripts.

## Findings kept in the text
- The default validator mode passed an unknown container field; `--strict` rejected it. It does not catch junk quantities such as `nvidia.com/gpu: "x"`, so the answers add their own checks.
- The validator has no schema for CRDs (KServe, Kubeflow, KEDA, VPA, Kueue, ServiceMonitor): exit code 0 proves nothing there, so those manifests were only YAML-parsed and the answers say so.
- The bundled schemas cover 1.25 to 1.37 only; 1.24 raised an IndexError.
- The Helm chart in Q11 and the template mirror in Q22 were rendered by hand-written Python stand-ins, labelled as not Helm.

## Not executed
Every kubectl and helm command, kind, KEDA, VPA, Cluster Autoscaler, ingress controller, Kubeflow, KServe, Kueue, Prometheus/DCGM, Pod Security Admission, drain, GPUs, cloud billing and IAM. Cloud workload-identity annotations (IRSA, GKE, AKS) are hedged.

## Hedged ("check current docs")
Removed-API table, CRD field names (KServe canaryTrafficPercent, KEDA, VPA), event wording, Job backoffLimit default, HPA tolerance default, device-plugin and MIG naming, DCGM metric name, ingress-nginx status (recalled, verify). Samples (pod-status JSON, scheduler events, cold-start and node-minute numbers) are hand-written and labelled as made-up.

## Evidence limits
No candidate-reported questions found; every WebFetch failed, so sources are snippet-only guides, docs snippets and job postings. See research_notes/Book4_Part03_sources.md.
