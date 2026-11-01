"""Q22 Vertex HyperparameterTuningJob built offline (anonymous creds). run() NOT called."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.auth.credentials import AnonymousCredentials
import google.cloud.aiplatform as aip
from google.cloud.aiplatform import hyperparameter_tuning as hpt
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
aip.init(project="demo-proj", location="asia-south1", staging_bucket="gs://demo-stage-bkt", credentials=AnonymousCredentials())
cj = aip.CustomJob(display_name="trial-template", worker_pool_specs=[{"machine_spec": {"machine_type": "n1-standard-4"},
        "replica_count": 1, "container_spec": {"image_uri": "asia-south1-docker.pkg.dev/demo-proj/repo/train:1"}}])
h = aip.HyperparameterTuningJob(display_name="hpt", custom_job=cj, metric_spec={"auc": "maximize"},
        parameter_spec={"lr": hpt.DoubleParameterSpec(min=0.001, max=0.1, scale="log"),
                        "depth": hpt.DiscreteParameterSpec(values=[3, 4, 6], scale=None)},
        max_trial_count=20, parallel_trial_count=4, search_algorithm=None)
spec = h._gca_resource.trial_job_spec
print(type(h).__name__, "| max_trials", h._gca_resource.max_trial_count, "| parallel", h._gca_resource.parallel_trial_count)
print("metrics:", [(m.metric_id, m.goal.name) for m in h._gca_resource.study_spec.metrics])
print("params:", [(p.parameter_id, p.scale_type.name) for p in h._gca_resource.study_spec.parameters])
print("algorithm (unset = service default):", h._gca_resource.study_spec.algorithm.name)
