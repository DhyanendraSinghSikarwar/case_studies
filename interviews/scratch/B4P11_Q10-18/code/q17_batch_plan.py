"""Azure ML BatchEndpoint/BatchDeployment built offline + a nightly invoke plan with hand-checkable arithmetic."""
import math, warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml.entities import BatchEndpoint, ModelBatchDeployment, ModelBatchDeploymentSettings, BatchRetrySettings, Data
from azure.ai.ml.constants import BatchDeploymentOutputAction
print("azure-ai-ml", m.__version__)

ep = BatchEndpoint(name="churn-batch", description="nightly scoring")
dep = ModelBatchDeployment(
    name="v1", endpoint_name="churn-batch", model="azureml:churn:7", compute="cpu-cluster",
    settings=ModelBatchDeploymentSettings(
        mini_batch_size=1, instance_count=4, max_concurrency_per_instance=2,
        output_action=BatchDeploymentOutputAction.APPEND_ROW, output_file_name="predictions.csv",
        retry_settings=BatchRetrySettings(max_retries=3, timeout=300), error_threshold=-1, logging_level="info"))
s = dep.settings
print("endpoint:", ep.name, "| deployment:", dep.name, "->", dep.endpoint_name)
print("settings:", dict(mini_batch_size=s.mini_batch_size, instance_count=s.instance_count,
      max_concurrency=s.max_concurrency_per_instance, output_action=s.output_action,
      retries=s.retry_settings.max_retries, timeout_s=s.retry_settings.timeout))
# NOTE: for an MLflow model the scoring script is not needed (no-code); for a custom model you add code + scoring_script.

ROWS = 2_000_000
# Plan. Assumption (check current docs): mini_batch_size counts FILES for file-based input, so 1 means one file per mini-batch.
# The input is 200 part-files of 10,000 rows each.
FILE_ROWS, FILES_PER_MB = 10_000, s.mini_batch_size
files = math.ceil(ROWS / FILE_ROWS)
mini_batches = math.ceil(files / FILES_PER_MB)
workers = s.instance_count * s.max_concurrency_per_instance
waves = math.ceil(mini_batches / workers)
print(f"files={files} mini_batches={mini_batches} parallel_workers={workers} waves={waves}")
plan = [
 "1. ensure input data asset (uri_folder of part files) is registered/versioned: churn-input:<date>",
 "2. az ml batch-endpoint invoke --name churn-batch --deployment-name v1 --input azureml:churn-input:<date>   (returns a job)",
 "3. poll the returned job until Completed (or Failed/Canceled); alert on Failed",
 "4. read predictions.csv from the job's output location; row count must equal 2,000,000 (APPEND_ROW)",
 "5. publish only after the count check; keep the job name in the run log",
 "6. rollback = set default deployment back (no traffic split on batch)",
]
print("\n".join(plan))
