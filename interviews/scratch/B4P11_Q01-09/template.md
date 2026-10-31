@@HEAD 1@@
**Say this first (1 line):** The ideas map almost one to one across Azure ML, Vertex AI and SageMaker, but the containers differ: Azure has a workspace that owns assets, Vertex has a project plus region and resources hang off it, and the names for compute, data and environments do not line up cleanly.

**Then explain:**
- Start from the lifecycle, not the product names: data, environment, train, tune, register, deploy, monitor. Every cloud has a managed piece for each step. Say the table, then say where it bends.
- Where it is not one to one: (1) Azure ML has a workspace object that owns data, models, environments and endpoints; Vertex has no workspace, the project and region are the boundary; (2) Azure has standing compute objects (cluster, instance), Vertex training takes a machine spec per job; (3) Azure has datastores and data assets, Vertex mostly takes Cloud Storage or BigQuery paths; (4) an Azure environment is a versioned asset, Vertex and SageMaker use a container image.
- Names that sound alike but are not the same: "Pipelines" on Vertex is a KFP spec; on Azure ML it is a pipeline job of components in Azure's own YAML. "Model Monitoring" differs in what it watches and how you configure it.
- Failure mode: answering with a marketing table and no caveats. Interviewers then ask "so what breaks if I move from one to the other?" and the honest answer is the SDK objects, registry metadata and IAM, not the model file.
- SageMaker is by concept only here. Part 10 owns its depth. Cells marked "check current docs" in the table may have changed; product names move often.

**Example:** "Train, then deploy". Azure: command job on a compute cluster, model asset registered, managed online endpoint with a deployment. Vertex: CustomJob with a machine spec, Model uploaded to Model Registry, Endpoint with a deployed model. SageMaker: TrainingJob, model package, real-time endpoint.

**Code:** the table is YAML inside Python. It is loaded and asserted: every concept has a non-empty entry for all three clouds, and a broken copy is rejected. The mapping content is my own summary from general knowledge, not checked against live docs.
@@CODE q01.py python@@

**Output (my run):** (azure-ai-ml venv, Python 3.13; pyyaml only; no cloud call.)
@@OUT q01.py az@@
Real services, quotas, Regions and product names were not executed; check current docs for the cells marked so.

**Follow-ups:**
1. *Which cell is least stable?* Feature store and monitoring: product designs and names have changed on more than one cloud, check current docs.
2. *Is a registry the same everywhere?* Same job, different fields: Azure has versions and tags, Vertex has versions and aliases, SageMaker has model package groups.
3. *Why show YAML?* A table you can load and assert stays complete when someone edits it.

**Common mistakes:**
- Saying "Vertex is the same as SageMaker" with no caveats.
- Forgetting that a project plus region is the Vertex boundary.
- Quoting price or quota numbers from memory.

@@HEAD 2@@
**Say this first (1 line):** An Azure ML workspace is the top-level place that owns your ML assets and points at a storage account, Key Vault, container registry and Application Insights; Vertex has no such object, a Google Cloud project plus a region is the boundary.

**Then explain:**
- Hierarchy: subscription, then resource group, then workspace. The workspace holds data assets, environments, models, components, endpoints and compute. RBAC and network settings can be applied at the workspace.
- Companion resources: a storage account (default datastore and job artifacts), Key Vault (secrets), container registry (built environment images), Application Insights (logs and telemetry). Whether they are created for you or you bring your own depends on how you create the workspace; check current docs.
- Vertex difference: a Google Cloud project holds resources with a regional location (jobs, models, endpoints). You pick the region at `aiplatform.init`. There is no workspace to create; you enable the API in the project.
- What an MLClient needs: a credential, subscription id, resource group and workspace name. Without a credential it fails at once; with `DefaultAzureCredential` it still fails when it has nothing to log in with.
- Failure modes: assuming creating the entity creates Azure resources (it does not), forgetting the workspace region is a data-residency choice, public access left on, and mixing up which resource group holds the companion resources.

**Example:** Dev and prod are two workspaces (or two subscriptions). Model assets move between them via a shared registry or a rebuild from the same code. On Vertex you would normally use two projects instead.

**Code:** the entity below is built offline. It has no network call. A fake all-zero subscription id is used.
@@CODE q02.py python@@

**Output (my run):** (azure-ai-ml 1.35.2; stdout shown; stderr carried only SDK warnings and the long credential error text, which I cut to its first line.)
@@OUT q02.py az@@
Not executed: creating a workspace, the companion resources, RBAC, any `MLClient` call to a real workspace.

**Follow-ups:**
1. *Where do the companion resources show up?* After creation, in the same resource group unless you supplied your own; check current docs.
2. *Is a workspace a security boundary?* It is a scope for RBAC and network rules, not a magic wall; Part 12 owns design.
3. *Hub and project workspaces?* Newer workspace kinds exist; check current docs. I only built the default kind.

**Common mistakes:**
- "I created the Workspace object so the workspace exists."
- Putting dev and prod in one workspace and relying on naming.
- Forgetting that `MLClient(credential=None)` is a ValueError, not an auth error.

@@HEAD 3@@
**Say this first (1 line):** On Vertex you enable the API in a project, choose a region once with `aiplatform.init(project, location, staging_bucket)`, authenticate with Application Default Credentials, and remember every job, model and endpoint is a regional resource.

**Then explain:**
- Setup: enable the Vertex AI API in the project, make a Cloud Storage bucket in the same region for staging, call `init`. The client then talks to a regional host (`<region>-aiplatform.googleapis.com`).
- Regional means: a model uploaded in one region cannot be deployed to an endpoint in another. Data in a bucket should sit in the same region (check current docs for exceptions and cost).
- Credentials: ADC looks at an env var for a key file, then the user's `gcloud` login, then the attached service account on Google compute. No credentials: the SDK raises a credentials error.
- What I measured offline: with no `init` the PipelineJob raised a project error; after `init` without credentials it raised `DefaultCredentialsError`; with `AnonymousCredentials` the PipelineJob and CustomJob objects built. Building an object proves nothing about access.
- In CI: use Workload Identity Federation (the CI platform's OIDC token trades for a short-lived credential for a service account), not a downloaded key file. Part 7 owns CI design; Q25 shows the workflow.
- Failure modes: bucket and job in different regions, staging bucket missing, a key file committed to the repo, the job service account lacking bucket access.

**Example:** Project `fake-project`, region `asia-south1`, bucket `gs://fake-bucket-name`. A job created in `asia-south1` with a staging bucket in another region fails or costs extra to cross, check current docs. Which regions have which accelerators: check current docs.

**Code:** the script compiles a tiny pipeline, then tries four situations. Anonymous credentials are used only to show object construction; `submit()` is deliberately not called.
@@CODE q03.py python@@

**Output (my run):** (google-cloud-aiplatform 1.165.1, kfp 2.17.3; `NO_GCE_CHECK=True` set so no metadata server probe.)
@@OUT q03.py gcp@@
Line 7 is a statement, not a result of this run. The earlier Wave A research run recorded that a real unauthenticated `submit()` returned HTTP 400 and then 401; I did not repeat any call to a Google endpoint. Real project setup, ADC with a real account and Workload Identity Federation: not executed.

**Follow-ups:**
1. *Why is `staging_bucket` needed?* The SDK uploads job artifacts there (code, specs, outputs) unless you give other paths.
2. *Can I use a key file?* It works but it is a long-lived secret. Prefer federation or an attached service account.
3. *Why did step 3 fail differently from step 1?* Step 1 had no project; step 3 had a project but no credentials.

**Common mistakes:**
- Treating "object built" as "job allowed".
- Using a bucket in a different region.
- Committing a service-account JSON.

@@HEAD 4@@
**Say this first (1 line):** A command job is code plus a command line plus inputs, outputs, an environment and a compute target; the YAML and the SDK `command()` produce the same job object, and offline validation catches shape errors, not missing environments or missing data.

**Then explain:**
- YAML fields: `code` (folder uploaded as a snapshot), `command` with `${{inputs.x}}` and `${{outputs.y}}` placeholders, `inputs` (a datastore path or a literal), `outputs`, `environment`, `compute`, `experiment_name`.
- Two ways in: `az ml job create -f job.yml` (CLI v2, not executed) or `ml_client.jobs.create_or_update(job)` (SDK v2, not executed). Both send the same job to the service.
- What happens on submit (from docs, not run): the code folder is uploaded, the environment image is resolved or built, a node is allocated on the compute, the command runs, inputs are mounted or downloaded, outputs and logs are saved to the workspace storage.
- What offline validation does: the schema check says "Unknown field" for a misspelt key. It did not catch a command that refers to `${{inputs.learning_rate}}` when no such input exists, so that error appears only at run time.
- Failure modes: environment name that does not exist, compute name typo, datastore path wrong, identity without access, command refers to an input you never defined.

**Example:** A churn job with an `lr` of 0.1 reading a folder on the default datastore. The YAML job and the SDK job came out equal as dictionaries (after removing the absolute code path and the environment).

**Code:** the Python builds the YAML in a temp dir, loads it, validates, builds the SDK equivalent, compares, and breaks it two ways. The CLI line is shown for reference only.
@@CODE q04.py python@@
```bash
# not executed: needs az CLI with the ml extension and a login
az ml job create -f job.yml --workspace-name mlw-dev-cin --resource-group rg-ml-dev
```

**Output (my run):** (azure-ai-ml 1.35.2; stderr had "experimental class" warnings, not shown; error text shortened by the script.)
@@OUT q04.py az@@
Not executed: the `az` CLI (not installed here), submit, compute, the datastore read, the environment build.

**Follow-ups:**
1. *Why does `$schema` matter?* Editors use it for autocompletion. This run did not fetch the URL; validation used the SDK's own schemas.
2. *Are the dicts always equal?* Not across versions; SDK object kwargs drift, check current docs.
3. *Where do I see output?* In the job's run page and the workspace storage; not run here.

**Common mistakes:**
- Treating `_validate()` passing as "the job will run".
- Relying on a private method `_validate()` in production; it is shown only as the offline check here and may change.
- Hard-coding a storage key in `command`.

@@HEAD 5@@
**Say this first (1 line):** Use a compute instance for a person at a notebook, a compute cluster that scales to zero for the nightly GPU job, serverless when you do not want to manage a cluster, and attached Kubernetes when platform rules require it; always check the Region quota first.

**Then explain:**
- Compute instance: one VM per user, interactive, should have idle shutdown on. Compute cluster (AmlCompute): `min_instances`, `max_instances`, idle time before scale-down; multi-node training and queued jobs. Serverless: you give instance type and count on the job, no cluster object. Attached Kubernetes: your own cluster, your own ops.
- Nightly 4-hour GPU job: cluster with `min_instances=0` and a sensible `max_instances`. Notebook user: a compute instance with idle shutdown and a schedule. Quota is per VM family per Region; check current docs.
- Cost of min 0: the first job waits for node allocation and image pull. How long depends on the VM family, region capacity and image size, so I would measure it, not quote a number. For a nightly job the wait does not matter. For many short jobs per hour it does; then keep warm nodes (min above 0) and accept idle time.
- Failure modes: quota too low for the GPU family so jobs sit queued, `max_instances` too high with no quota guard, instance left running over a weekend, scale-to-zero cluster used for latency-sensitive work.

**Example:** Nightly 4-hour job at 02:00 on a 2-node cluster with 5 minutes idle time: nodes spin up at job start and release after the idle window. A `Standard_NC6s_v3`-style size is used only as an example name; whether it exists in your Region: check current docs.

**Code:** two entities built offline, assertions on scale-to-zero, and a toy selection rule. The rule is my own simplification, not Microsoft guidance.
@@CODE q05.py python@@

**Output (my run):** (azure-ai-ml 1.35.2.)
@@OUT q05.py az@@
Not executed: creating compute, quota, GPU availability, node start-up time. No prices.

**Follow-ups:**
1. *Why did the entity accept min greater than max?* Offline objects do no cross-field checks; the service (or your own CI check) must.
2. *Where does cost depth live?* Part 12.
3. *Serverless vs cluster?* Serverless saves cluster admin; a cluster gives you a fixed pool and shared quota control. Check current docs for what serverless supports.

**Common mistakes:**
- `min_instances` above 0 "just in case", leaving GPUs idle.
- No idle shutdown on instances.
- Assuming the same VM size exists in every Region.

@@HEAD 6@@
**Say this first (1 line):** An Azure ML pipeline is a pipeline job whose steps are components; you wire step outputs to step inputs with `${{parent...}}` bindings in YAML or with the `dsl.pipeline` decorator, and offline validation checks structure while only a real submit checks compute, environments and data.

**Then explain:**
- Component: a reusable command with typed inputs and outputs and an environment, versioned. Pipeline job: `jobs:` of steps, each pointing at a component, with `settings.default_compute`.
- Wiring: `${{parent.inputs.raw_data}}` feeds a pipeline input into a step; `${{parent.jobs.prep_step.outputs.clean}}` feeds one step's output to the next; a step output is promoted to a pipeline output with `${{parent.outputs.final_model}}`.
- Caching and reuse: a deterministic component with the same inputs and code can reuse an earlier result instead of running again. Check current docs for the exact reuse conditions; `is_deterministic` is the component-side switch.
- Default compute: a step with no `compute` uses `settings.default_compute`.
- What my offline run showed: the structural check caught a missing component file. It did not catch a misspelt step output name (`cleen`), so that kind of error only appears on submit or in review. I would write a small test that resolves every binding.
- Failure modes: step reuse hiding a data change (data path same, content new), wrong binding name, forgot a type on a Python SDK step, compute name not existing.

**Example:** `prep_step` makes `clean`; `train_step` takes `clean` and `lr` and returns `model`, promoted to `final_model`.

**Code:** components and pipeline YAML written to a temp dir, loaded, validated, rebuilt with `dsl.pipeline`, then two bad variants.
@@CODE q06.py python@@

**Output (my run):** (azure-ai-ml 1.35.2; load of a pipeline with a misspelt output binding returned a passing validation; error text shortened.)
@@OUT q06.py az@@
Not executed: submit, caching behaviour, step scheduling, compute and environment existence. Part 5 owns orchestration concepts.

**Follow-ups:**
1. *Can the YAML and SDK pipelines differ?* They gave the same shape here (step names differ because the SDK names steps from variable names).
2. *Why a component, not a script?* Typed interface, versioning and reuse across pipelines.
3. *How do I catch binding typos?* A unit test that parses the YAML and checks each `${{parent.jobs.X.outputs.Y}}` against the component's declared outputs.

**Common mistakes:**
- Assuming validation means the pipeline will run.
- Turning on reuse for a non-deterministic step (timestamps, random seeds, "latest" data).
- Forgetting default compute and hitting a compute error on submit.

@@HEAD 7@@
**Say this first (1 line):** A managed online endpoint is a stable URL and auth setup; deployments (blue, green) sit behind it and traffic percentages move between them, with the rule that the map must sum to 0 or 100 and only name deployments that already exist.

**Then explain:**
- Endpoint versus deployment: the endpoint holds name, auth mode and traffic; a deployment holds model, environment or scoring script, VM size and instance count.
- Scoring script versus MLflow no-code: with a custom model you give `score.py` with `init()` and `run()` plus an environment; for an MLflow model the service can build scoring for you, so no script and no environment on the deployment. Check current docs for supported flavors.
- Auth modes: `key`, `aml_token`, and Microsoft Entra token (I would check current docs for the exact option names in the SDK version you use). The endpoint has an identity (system- or user-assigned) that the container uses to read things like Key Vault; that is separate from the caller's identity.
- Rollout: create green with 0 traffic, test it (a deployment can be called directly with a header, check current docs), then shift 10 percent, then 100, then delete blue. Part 6 owns rollout mechanics.
- Failure modes: setting traffic before the deployment exists, traffic that sums to 95, deleting blue before green is healthy, quota too low for two deployments side by side, scoring script that loads the model in `run()` instead of `init()`.

**Example:** blue 100. Create green at 0. Set `{"blue": 90, "green": 10}`. Check metrics. Set `{"green": 100}`. The function below accepts that and rejects 90 plus 5.

**Code:** objects built offline and a traffic-map validator that I wrote. The service applies its own checks; this one is for CI.
@@CODE q07.py python@@

**Output (my run):** (azure-ai-ml 1.35.2.)
@@OUT q07.py az@@
Not executed: creating the endpoint or deployments, auth, scoring, traffic shifting, mirrored traffic (third-party sources mention it; the exact syntax was not confirmed; check current docs).

**Follow-ups:**
1. *What needs to be real for a rollout?* Quota for both deployments, a model asset, environment image, identity roles, and a monitoring check before shifting.
2. *Can I skip a canary?* You can, but then a bad model takes all traffic at once.
3. *Batch has traffic split?* No; you switch the default deployment instead (Q17).

**Common mistakes:**
- Setting `traffic` before creating the deployment.
- Giving the endpoint identity broad roles.
- Believing the SDK entity validates the traffic rule offline (it did not here).

@@HEAD 8@@
**Say this first (1 line):** A Vertex CustomJob is a list of worker pools, each with a machine spec, replica count and a container (prebuilt or your own), run under a service account, writing to a staging bucket; the `AIP_*` environment variables tell the container where to put the model.

**Then explain:**
- `worker_pool_specs`: pool 0 is the chief (replica count 1); more pools are workers, parameter servers or evaluators for distributed training. Each pool has `machine_spec` (machine type, accelerator type and count), `replica_count`, and `container_spec` (image, args, env) or a Python package spec.
- Prebuilt versus custom container: prebuilt for common frameworks, custom for your own dependencies (image in Artifact Registry). Whether a given framework version is available: check current docs.
- Identity and network: pass a `service_account` for the job; without one it runs as a default service account that may have more rights than you want. `network` attaches the job to a VPC through peering, or use Private Service Connect (see Q24).
- Environment variables: Vertex sets variables like `AIP_MODEL_DIR` (where to save the model), `AIP_CHECKPOINT_DIR` and `AIP_TENSORBOARD_LOG_DIR` when you set a base output directory. My script reads `AIP_MODEL_DIR` with a local fallback, so it also runs on a laptop. Names are from the docs as I remember them; check current docs.
- Azure comparison in two sentences: an Azure command job points at a named compute and an environment asset, and the data is a mounted input. A Vertex CustomJob carries its machine spec and container inline, and the data is whatever path your code reads with the job's service account.
- Failure modes: bucket in another region, job service account missing bucket access, GPU quota or accelerator not in the region, image not pullable by the service agent, timeouts.

**Example:** One T4 on an `n1-standard-8`, one replica, image in Artifact Registry in `asia-south1`, 4-hour timeout, service account `trainer@...`.

**Code:** both the SDK `CustomJob` and the raw proto are built with `AnonymousCredentials`; nothing is sent.
@@CODE q08.py python@@

**Output (my run):** (google-cloud-aiplatform 1.165.1.)
@@OUT q08.py gcp@@
Not executed: `run()`/`submit()`, image pull, GPU allocation, service-account or VPC checks, writing to a real bucket.

**Follow-ups:**
1. *Why is the service account empty on the SDK object?* It is passed at run or submit time in this SDK; check current docs for your version.
2. *Chief and workers?* Pool 0 chief, later pools for workers, per Vertex docs.
3. *Where is the model saved?* Under the output directory you set, read through `AIP_MODEL_DIR`.

**Common mistakes:**
- Running as the default service account with broad rights.
- Hard-coding output paths instead of reading `AIP_MODEL_DIR`.
- Assuming an offline object means a valid image or quota.

@@HEAD 9@@
**Say this first (1 line):** Vertex Pipelines runs a compiled KFP v2 spec: you compile to JSON or YAML, create a PipelineJob with a GCS pipeline root and parameter values, and the service runs each task as a container under a service account, records artifacts and lineage in ML Metadata, and skips cached steps.

**Then explain:**
- What the compile gives you: `pipelineInfo` (name), `root.dag.tasks` (the steps and their dependencies), `components` and `deploymentSpec.executors` (the containers), `defaultPipelineRoot` and `root.inputDefinitions` (the parameters).
- What `submit` does (docs, not run here): uploads or reads the spec, uses the pipeline root in Cloud Storage for artifacts, runs each task under the pipeline service account you pass, records executions and artifacts in ML Metadata so you can trace lineage, and reuses a cached step when the inputs and component match and caching is on.
- Testing logic without the service: `kfp.local` with `SubprocessRunner` runs one component as a subprocess on your machine. It tests the Python logic, not GCS, IAM or container images.
- Failure modes: service account without bucket access, pipeline root bucket in another region, cache hiding a data change, unpinned `packages_to_install` at run time, forgetting that a lightweight component's imports must be inside the function.
- Part 5 owns KFP concepts; this answer is the Vertex service layer.

**Example:** `prep` then `train`. The compiled root lists both tasks and `train` has `dependentTasks: [prep]`.

**Code:** compile, inspect, build the PipelineJob with anonymous credentials (no submit), and run the local runner on one component. The runner's own log lines are hidden and counted.
@@CODE q09.py python@@

**Output (my run):** (kfp 2.17.3, google-cloud-aiplatform 1.165.1.)
@@OUT q09.py gcp@@
Not executed: `submit()`, any use of GCS, service-account checks, caching, ML Metadata lineage. The local runner used the default Python of the venv; the component had no extra packages.

**Follow-ups:**
1. *JSON or YAML?* Both compile; Vertex accepts the compiled spec; check current docs for which formats your SDK version prefers.
2. *Does local run test caching?* No, caching is a service feature.
3. *Which service account?* The one you pass at submit; give it only the bucket, registry and API roles the steps need.

**Common mistakes:**
- Believing `PipelineJob(...)` built offline means the pipeline is valid in the service.
- Using one wide service account for every pipeline.
- Caching steps that read mutable "latest" data.
