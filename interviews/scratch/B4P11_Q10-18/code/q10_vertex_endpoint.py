"""Q10: Vertex endpoint + batch prediction as proto objects, offline. No network, no aiplatform.init."""
import warnings; warnings.filterwarnings("ignore")
import google.cloud.aiplatform as ai
from google.cloud.aiplatform_v1.types import (DeployedModel, DedicatedResources, MachineSpec, Endpoint,
    BatchPredictionJob, BatchDedicatedResources, GcsSource, GcsDestination, BigQuerySource, BigQueryDestination)

print("google-cloud-aiplatform", ai.__version__)
MODEL = "projects/demo-proj/locations/asia-south1/models/111"

def dm(id_, version, min_r, max_r):
    return DeployedModel(
        id=id_, model=MODEL, model_version_id=version, display_name=f"churn-v{version}",
        dedicated_resources=DedicatedResources(
            machine_spec=MachineSpec(machine_type="n1-standard-4"),
            min_replica_count=min_r, max_replica_count=max_r))

ep = Endpoint(
    display_name="churn-ep",
    deployed_models=[dm("a", "1", 1, 3), dm("b", "2", 1, 3)],
    traffic_split={"a": 90, "b": 10},        # keys are deployed-model ids
    dedicated_endpoint_enabled=True)         # dedicated endpoint flag; check current docs
print(Endpoint.to_json(ep, indent=None, including_default_value_fields=False))

def check_split(split, deployed_ids):
    """Traffic must name only deployed models and sum to 100 (check current docs)."""
    unknown = set(split) - set(deployed_ids)
    if unknown:
        return f"BAD unknown deployed model id(s): {sorted(unknown)}"
    if sum(split.values()) != 100:
        return f"BAD sum is {sum(split.values())}, need 100"
    return "ok"

ids = [d.id for d in ep.deployed_models]
for s in [{"a": 90, "b": 10}, {"a": 90, "b": 20}, {"a": 50, "c": 50}]:
    print(s, "->", check_split(s, ids))

res = BatchDedicatedResources(machine_spec=MachineSpec(machine_type="n1-standard-4"),
                              starting_replica_count=2, max_replica_count=4)
gcs_job = BatchPredictionJob(
    display_name="nightly-gcs", model=MODEL,
    input_config=BatchPredictionJob.InputConfig(instances_format="jsonl",
        gcs_source=GcsSource(uris=["gs://demo-bkt/in/part-*.jsonl"])),
    output_config=BatchPredictionJob.OutputConfig(predictions_format="jsonl",
        gcs_destination=GcsDestination(output_uri_prefix="gs://demo-bkt/out/")),
    dedicated_resources=res)
bq_job = BatchPredictionJob(
    display_name="nightly-bq", model=MODEL,
    input_config=BatchPredictionJob.InputConfig(instances_format="bigquery",
        bigquery_source=BigQuerySource(input_uri="bq://demo-proj.sales.to_score")),
    output_config=BatchPredictionJob.OutputConfig(predictions_format="bigquery",
        bigquery_destination=BigQueryDestination(output_uri="bq://demo-proj.sales_out")),
    dedicated_resources=res)
for j in (gcs_job, bq_job):
    print(j.display_name, "| in:", BatchPredictionJob.InputConfig.to_dict(j.input_config),
          "| out:", BatchPredictionJob.OutputConfig.to_dict(j.output_config))
print("replicas:", res.starting_replica_count, "->", res.max_replica_count)

# ai.Endpoint("projects/.../endpoints/1") fetches the resource in its constructor, so it is NOT called here.
print("SDK classes present:", ai.Endpoint.__name__, ai.BatchPredictionJob.__name__, ai.Model.__name__,
      "| Model.deploy and Model.batch_predict exist:", hasattr(ai.Model, "deploy"), hasattr(ai.Model, "batch_predict"))
