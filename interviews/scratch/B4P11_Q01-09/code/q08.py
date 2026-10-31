import os, warnings, json
os.environ["NO_GCE_CHECK"] = "True"
warnings.filterwarnings("ignore")
import google.cloud.aiplatform as aip
from google.auth.credentials import AnonymousCredentials
from google.cloud.aiplatform_v1.types import CustomJobSpec, WorkerPoolSpec, MachineSpec, ContainerSpec, Scheduling
print("google-cloud-aiplatform", aip.__version__)
aip.init(project="fake-project", location="asia-south1", staging_bucket="gs://fake-bucket-name", credentials=AnonymousCredentials())

pools = [
  {"machine_spec": {"machine_type": "n1-standard-8", "accelerator_type": "NVIDIA_TESLA_T4", "accelerator_count": 1},
   "replica_count": 1,
   "container_spec": {"image_uri": "asia-south1-docker.pkg.dev/fake-project/ml/train:1.0",
                      "args": ["--epochs", "3"], "env": [{"name": "MODEL_NAME", "value": "churn"}]}},
]
cj = aip.CustomJob(display_name="churn-train", worker_pool_specs=pools,
                   staging_bucket="gs://fake-bucket-name/jobs", base_output_dir="gs://fake-bucket-name/out/run1")
print("CustomJob built:", type(cj).__name__, "| resource name before submit:", getattr(cj._gca_resource, "name", "") or "(empty)")
spec = cj._gca_resource.job_spec
print("service_account on spec (empty unless passed to run/submit):", repr(spec.service_account))
print("base_output_dir:", spec.base_output_directory.output_uri_prefix)

# the underlying proto, built by hand with a service account and a peered network
proto = CustomJobSpec(
    worker_pool_specs=[WorkerPoolSpec(machine_spec=MachineSpec(machine_type="n1-standard-8",
        accelerator_type="NVIDIA_TESLA_T4", accelerator_count=1), replica_count=1,
        container_spec=ContainerSpec(image_uri="asia-south1-docker.pkg.dev/fake-project/ml/train:1.0", args=["--epochs", "3"]))],
    service_account="trainer@fake-project.iam.gserviceaccount.com",
    network="projects/123456789/global/networks/vpc-ml",
    scheduling=Scheduling(timeout={"seconds": 14400}),
)
def prune(x):
    if isinstance(x, dict):
        return {k: prune(v) for k, v in x.items() if v not in ("", [], 0, False, None, {}) or k == "replicaCount"}
    if isinstance(x, list):
        return [prune(i) for i in x]
    return x
print(json.dumps(prune(json.loads(CustomJobSpec.to_json(proto))), indent=1))
print("(empty and zero-valued fields pruned for reading; acceleratorType 5 is the enum number)")

# how a training script should read them, with a local fallback so it also runs on a laptop
model_dir = os.environ.get("AIP_MODEL_DIR", "./model_out")
print("script would write the model to:", model_dir)
