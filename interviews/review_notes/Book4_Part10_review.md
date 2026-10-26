# Book 4 Part 10 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the five answer agents). Scope: 50 questions, Q1-Q50 (AWS for ML: S3, IAM, EC2, Lambda, SageMaker, ECR/ECS, VPC, KMS, CloudWatch, cost basics). Band per plan.md: Rs 30-80 LPA; no salary figures; no prices.

## Process
Five agents answered Q1-10, Q11-20, Q21-30, Q31-40, Q41-50; merged by heading: 50 of 50 merged, 0 skipped, 0 pending. No spend-limit stops. Only fake keys were used; nothing contacted real AWS. No moto servers were left running.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q50; star order and counts 20 / 20 / 10 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 50 |

The lead did not re-run the scripts (they use moto state and per-agent temp dirs); pasted outputs come from each agent's real runs (`python3 -I`, boto3 1.43.118, moto 5.2.4, awscli 1.46.2), with code in each agent's `code/` folder.

## What really ran
Everything ran against the moto mock (in-process `mock_aws` or a local `moto_server`), so every AWS result is an API-shape result, not real AWS behaviour, and each answer says so. A simplified pure-Python IAM evaluator (identity and resource policies, explicit deny, boundaries, SCPs, session policies, cross-account, with an extended copy adding NotAction, policy variables, negated and Date conditions) was run on many cases. Other pure-Python models: spot checkpoint and resume (bit-identical vs a sloppy weights-only resume), cold/warm Lambda model load, reserved-concurrency tick simulation, M-of-N alarm evaluation, security-group vs NACL, GET-count arithmetic, a secret scanner.

## Moto gaps and surprises (stated in the answers)
- Lifecycle: moto stores rules but never moves objects, accepted a 5-day Standard-IA transition real S3 should reject, dropped NewerNoncurrentVersions and the replication prefix filter on read-back.
- STS `assume_role` ignored a trust policy naming another account and an external ID; a 2 MB presigned POST passed a 1 MiB content-length-range; a presigned GET was served after expiry; KMS still decrypted after `disable_key`; IAM enforcement is off unless `set_initial_no_auth_action_count` is used (works when set); S3 bucket-policy explicit Deny is enforced.
- Not implemented or API-shape only: Lambda invoke (needs Docker; returns the Docker error text), provisioned concurrency, SageMaker training/endpoints/pipelines/monitoring schedules/labeling jobs/feature-store runtime, `list_pipeline_execution_steps`, CloudTrail `lookup_events`, placement groups, Bedrock `invoke_model` (empty body) and guardrails, SCP enforcement.
- CloudWatch alarm showed OK right after creation (real CloudWatch typically starts INSUFFICIENT_DATA).
- ABAC trap: if a team can edit its own tags, access collapses. A long-term access key with no TokenIssueTime is not affected by a deny-before-time policy (AKIA keys belong to users and are deactivated; ASIA temporary credentials are cut off with the policy).

## Not executed
Real S3, IAM, KMS, SCP and Organizations behaviour, spot interruptions, Lambda cold starts and concurrency, SageMaker jobs and endpoints, networking and VPC endpoints, cross-region replication, IMDS/web identity/IRSA/Pod Identity, EFA and placement groups, GPU capacity and quotas, Bedrock calls, Glue/Athena/Redshift queries, ECS/ECR runtime, Docker builds (no daemon). Limits, quotas and any pricing are hedged "check current docs"; no price figures anywhere.

## Hedged from memory
IMDSv2 hop limit, AWS managed keys not shareable cross-account, EKS Pod Identity mechanics, model-registry sharing options, botocore chain order details beyond the printed run. The evaluator is simplified (see each answer's list of simplifications, e.g. KMS key-policy rule, account-root principals, grants).

## Evidence limits
No candidate-reported questions found; every WebFetch failed (docs.aws.amazon.com unreachable), so sources are snippet-only; no India-specific interview reports found. Third-party endpoint figures that conflicted with AWS docs, and spot savings percentages, were left out. See research_notes/Book4_Part10_sources.md.
