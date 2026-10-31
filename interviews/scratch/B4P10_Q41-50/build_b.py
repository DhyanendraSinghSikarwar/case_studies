from build_a import *

A[47] = (r"""
**Say this first (1 line):** ABAC lets one policy say "access if the principal's tag matches the resource's tag", so a new team means new tags, not new policies; the traps are who may edit tags, tag-on-create, and services that ignore tag conditions.

**Then explain:**
- Keys: `aws:PrincipalTag/<k>` (tag on the role or user, or a session tag passed at AssumeRole), `aws:ResourceTag/<k>` (tag on the target), `aws:RequestTag/<k>` (tag in the create or tag request).
- Scaling: RBAC needs a policy per project; ABAC needs one policy plus tags. For many ML teams that is far less policy sprawl.
- Session tags: pass tags in AssumeRole (the trust policy must allow `sts:TagSession`); they can be marked transitive for role chaining (Q9).
- Trap 1: if a team can edit tags on resources (or on their own principal), they can re-tag themselves into someone else's data. Guard tag actions with explicit denies or conditions (output shows the collapse).
- Trap 2: tag-on-create. To force the right tag at creation, use `aws:RequestTag` conditions and require the tag key (`Null` check) so untagged creates fail.
- Trap 3: not every service or action supports every tag condition key. Check the service authorisation reference in current docs before relying on it.
- Missing tag: an absent tag must give no access (the condition is false), never default allow.

**Example:** team-a principal reading a team-a object: allow. team-b reading team-a data: deny. Principal with no `team` tag: deny. Training job created with `team=team-b` by a team-a principal: deny. With tag-editing allowed, team-b re-tags the object to `team-b` and then reads it: both steps allow.

**Code:** the ABAC policy and cases (`q47_abac.py`) use the extended evaluator `iam_eval_ext.py` (in code/), derived from the Wave A sketch.
@@CODE@@

**Output (my run):** pure-Python evaluator, ran for real. The extension adds policy variables like `${aws:PrincipalTag/team}`, `Null` and the negated condition operators. moto accepted session tags on `assume_role` but IAM enforcement is off by default, so no policy decision there is real. Still not modelled (also printed): multi-value tag operators, tag-key case rules, per-service tag-condition support, session-tag precedence and transitivity, tag policies. Real IAM was not executed; check current docs.
@@OUT@@

**Follow-ups:**
- *Is ABAC always better?* No. It is good for many similar teams; for a few special roles, plain role policies are easier to read and audit.
- *How do you test it?* Use the policy simulator or Access Analyzer in real AWS (not run here), plus a negative test for each guard.
- *Who owns the tags?* A small admin role, enforced by explicit deny and SCP (Q48).

**Common mistakes:** letting developers edit the tag that grants access; forgetting `sts:TagSession`; assuming all services support tag conditions; no deny for untagged; trusting a simplified evaluator as proof.
""", ["q47_abac.py"], {"python": ["q47_abac.py"]})

A[48] = (r"""
**Say this first (1 line):** An SCP is a permission ceiling for accounts in the organisation: it never grants anything, it only removes; I would use a few deny guardrails (Regions, leaving the org, CloudTrail, tags or encryption on create) with a tight break-glass exception, and remember the management account is not affected.

**Then explain:**
- An action is allowed only if every SCP level on the path allows it (and an identity or resource policy also allows it). An explicit deny in any SCP wins.
- The management account is not restricted by SCPs, so keep workloads out of it.
- Region guardrail: deny everything outside approved Regions, with `NotAction` for global services (IAM, Organizations, and so on) so you do not break them. The right list of global-service actions changes; check current docs.
- Org and audit guardrails: deny `organizations:LeaveOrganization` and the CloudTrail stop, delete, update and event-selector actions.
- Create-time rules: deny a create call when a required tag is absent (`Null` on `aws:RequestTag/<k>`). Encryption-on-create rules depend on condition keys that exist per action; check current docs.
- Break-glass: exempt one role with `ArnNotLike aws:PrincipalArn`; protect that role with MFA, alarms and a rarely used trust path.
- Failure modes: a broad deny that blocks your own pipeline or service-linked roles, no testing in a sandbox OU first, and size and nesting limits (check current docs).

**Example:** Everything below uses an AdministratorAccess-like identity policy. Training in ap-south-1: allowed. In us-east-1: denied. Same as BreakGlass: allowed. `iam:ListRoles` in us-east-1: allowed (global service exempt). Stopping CloudTrail: denied, except for BreakGlass. Leaving the org: denied unless the caller is the management account.

**Code:** the SCP document (JSON) and the script that validates it, creates it in moto and runs the cases.
@@CODE@@

**Output (my run):** structure validation and evaluator runs are real. moto Organizations accepted and listed the policy and attached it to the root, but a mock does not enforce SCPs, so enforcement is not executed. The evaluator is simplified: no OU hierarchy, no service-linked-role exemption, and it treats condition keys as always available. Verify guardrails in a sandbox organisation first.
@@OUT@@

**Follow-ups:**
- *Why does the identity policy matter if an SCP allows?* SCP allow is not a grant. Someone still needs an identity or resource policy.
- *Can an SCP block the root user of a member account?* Generally yes for member accounts (check current docs for exceptions).
- *SCP versus permissions boundary?* SCP caps whole accounts; a boundary caps one role or user (Q30).

**Common mistakes:** thinking an SCP grants access; attaching a deny to the root with no break-glass; no `NotAction` for global services; putting workloads in the management account; shipping untested.
""", ["q48_scp.py"], {"python": ["q48_scp.py"], "json": ["scp_ml_org.json"]})

A[49] = (r"""
**Say this first (1 line):** Three accounts (dev, prod, shared services) with data zones in S3, images in ECR, training and registry in dev, a controlled promoter role that is the only writer into prod, deployment into private-subnet endpoints, one role per stage, KMS per environment, an org CloudTrail and alarms.

**Then explain:**
- Flow (whiteboard): ingest to `raw`, curate to Parquet, snapshot a dataset version, train in dev (SageMaker, VPC-attached, execution role), register in the Model Registry with an approval, a promoter role copies the approved artifact into the prod model bucket, a deployer creates the endpoint in prod with its own execution role, Model Monitor and CloudWatch alarms watch it.
- Accounts: dev for experiments, prod for serving and production data, shared for ECR, CI and logging. Why: blast radius and clear audit lines, which matters for regulated lending and payments data (follow your regulator's guidance; check current rules).
- Roles per stage: data engineering, training, promoter, endpoint execution, deployer. Each role gets the least privilege (Q8), and `iam:PassRole` is limited to named roles (Q4).
- Cross-account: both sides must allow (Q40). The prod bucket policy also denies writes from anyone but the promoter, as a second line.
- Network: private subnets, S3 gateway endpoint and interface endpoints for ECR, Logs and STS (Q16, Q39).
- Encryption and audit: KMS key per environment with key policies, org trail to a log-archive bucket, alarms for denied calls and key-policy changes, SCP guardrails (Q48).
- Failure modes: training role allowed on prod "to save time"; one KMS key for all; no approval gate; manual console deploys; no rollback artifact. System-design depth is Part 12.

**Example:** Hand-check: the dev training role has no allow on the prod bucket and the bucket policy denies any writer other than the promoter, so a PUT to `acme-ml-prod-models/approved/credit_v7.tar.gz` by the training role is denied twice. The promoter, which has an identity allow in shared and a bucket allow in prod, is allowed.

**Code:** the role and permission matrix (YAML) and the checker (`q49_check.py`) with the extended evaluator.
@@CODE@@

**Output (my run):** pyyaml parsing, the matrix lint and the evaluator cases ran for real. The evaluator is simplified and uses fake account ids; it ignores SCPs, KMS, VPC endpoint policies and Block Public Access here. The architecture itself (accounts, endpoints, SageMaker, CloudTrail) was not executed.
@@OUT@@

**Follow-ups:**
- *Why a separate promoter role?* One narrow identity can write to prod, so the policy is easy to audit and alarm on.
- *Where is the human approval?* In the registry approval status and a protected CI environment (Parts 4 and 7).
- *What about rollback?* Keep the previous approved artifact and endpoint config; redeploy it (Part 6).

**Common mistakes:** sharing one account; broad `iam:PassRole`; writing to prod from dev roles; no network endpoints so jobs hang (Q39); an architecture with no monitoring and no audit trail.
""", ["q49_check.py"], {"python": ["q49_check.py"], "yaml": ["q49_matrix.yaml"]})

A[50] = (r"""
**Say this first (1 line):** Treat it as compromised now: confirm what the credential did, neutralise it, cut off any live sessions, rotate related secrets, review everything it touched, then fix the root cause with roles, secret scanning and boundaries.

**Then explain:**
- First: what kind of credential is it? An IAM role has no long-term access key. A leaked key beginning with `AKIA` belongs to an IAM user; one beginning with `ASIA` is a temporary credential from a role session. The first you deactivate and delete; the second you cannot deactivate, so you revoke older sessions (below).
- Order: (1) confirm with CloudTrail which calls that key or session made, and from where (the first look, since you must not lose evidence); (2) deactivate the key (do not delete it yet if you want it for evidence, check your process); (3) for role sessions, attach a deny with `aws:TokenIssueTime` before "now", which cuts all older sessions; new legitimate sessions still work; (4) rotate any secrets the key could read; (5) review S3, SageMaker, IAM changes and look for persistence (new users, keys, roles, trust policy edits, endpoints, cross-account grants); (6) remove the key from the repo and history, though treat it as public forever; (7) add detection.
- Afterward: use roles and short-lived credentials (Q3, Q9, Q31), secret scanning and push protection, permissions boundaries and least privilege (Q8, Q30), SCP guardrails (Q48), alarms on unusual API activity.
- Edge cases: a long-term user key has no `TokenIssueTime`, so the deny-before-time policy does not stop it; deactivation does. CloudTrail has delivery delay and may not record every data event unless enabled (check current docs).
- Security design in depth is Part 12.

**Example:** Cutoff 10:00. A session issued at 09:00 is denied; one issued at 10:30 is allowed. A long-term key (no issue time in the request) is not touched by this policy: deactivate it.

**Code:** the drill (moto server on port 8541, `aws` CLI and boto3, the evaluator and a small scanner).
@@CODE@@

**Output (my run):** the CLI and boto3 calls ran against a local moto server with fake keys; the server was stopped afterwards. moto's `get_access_key_last_used` returned `N/A`, and CloudTrail `lookup_events` failed (not implemented), so the evidence step is not executed; in real AWS you would query CloudTrail. The deny-before-time results come from the simplified evaluator, not real IAM. The AWS example key ids in the scanner are documentation placeholders, not real keys.
@@OUT@@

**Follow-ups:**
- *Is deleting the repo file enough?* No. History, forks and caches keep it. Rotate and assume it was used.
- *Revoke sessions in the console?* There is a console action that attaches this kind of deny policy; check current docs for the exact name and effect.
- *How would you detect it earlier?* Secret scanning with push protection, and alarms on unusual regions or calls (Part 8 alerting patterns).

**Common mistakes:** deleting before reading CloudTrail; forgetting temporary sessions are still valid; rotating the key but ignoring what it read; no review for persistence; blaming the developer instead of removing long-term keys.
""", ["q50_incident.py"], {"python": ["q50_incident.py"]})

parts = []
for n in range(41, 51):
    tmpl, runs, codes = A[n]
    parts.append(build(n, tmpl, runs, codes))
hdr = "# Book 4 Part 10, Q41-Q50 answers (Wave B)\n\nRuntime: Python 3.13 venv /tmp/claude-0/b10p10/v; boto3/botocore 1.43.118, moto 5.2.4 (decorator mode, plus one moto_server on port 8541 for Q50), awscli 1.46.2; fake keys only; no real AWS call. Moto does not enforce IAM by default, ignores trust policies in STS assume_role, cannot invoke Lambda without Docker, and runs no SageMaker jobs or endpoints. Real AWS behaviour, limits and prices: not executed; check current docs.\n\n"
open(f"{ROOT}/scratch/B4P10_Q41-50/answers.md", "w").write(hdr + "\n\n".join(parts) + "\n")
print("written")
