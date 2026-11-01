import yaml
TABLE = """
workspace_or_project:
  azure_ml: Workspace (inside a resource group and subscription)
  vertex_ai: Google Cloud project plus a region (no workspace object)
  sagemaker: AWS account plus Region; SageMaker Domain for Studio users
notebooks:
  azure_ml: Compute instance with Jupyter/VS Code
  vertex_ai: Workbench instances and Colab Enterprise
  sagemaker: Studio notebooks / notebook instances
compute:
  azure_ml: Compute cluster (AmlCompute), serverless compute, attached Kubernetes
  vertex_ai: Machine specs inside each job (no standing cluster object for training)
  sagemaker: Instance type and count inside each training job
data_access:
  azure_ml: Datastores and data assets (uri_file, uri_folder, mltable)
  vertex_ai: Cloud Storage paths, BigQuery tables, managed datasets
  sagemaker: S3 URIs as channels
environments:
  azure_ml: Environment asset (image plus conda or Dockerfile), versioned
  vertex_ai: Prebuilt or custom container in Artifact Registry
  sagemaker: Prebuilt or custom container in ECR
training_jobs:
  azure_ml: command job
  vertex_ai: CustomJob / CustomTrainingJob
  sagemaker: TrainingJob
pipelines:
  azure_ml: Pipeline job made of components
  vertex_ai: Vertex AI Pipelines (KFP v2 spec)
  sagemaker: SageMaker Pipelines
hyperparameter_tuning:
  azure_ml: sweep job
  vertex_ai: HyperparameterTuningJob (Vizier)
  sagemaker: Automatic Model Tuning job
automl:
  azure_ml: Automated ML jobs (automl.classification etc.)
  vertex_ai: Vertex AI AutoML training
  sagemaker: Autopilot / Canvas
model_registry:
  azure_ml: Model asset in workspace or shared registry
  vertex_ai: Model Registry (versions and aliases)
  sagemaker: Model Registry (model package groups)
realtime_inference:
  azure_ml: Managed online endpoint plus deployments
  vertex_ai: Endpoint plus deployed models
  sagemaker: Real-time endpoint
batch_inference:
  azure_ml: Batch endpoint plus batch deployments
  vertex_ai: BatchPredictionJob
  sagemaker: Batch Transform job
monitoring:
  azure_ml: Model monitoring (signals and schedules)
  vertex_ai: Model Monitoring
  sagemaker: Model Monitor
feature_store:
  azure_ml: Managed feature store (check current docs)
  vertex_ai: Vertex AI Feature Store (BigQuery based; legacy store deprecated)
  sagemaker: SageMaker Feature Store
experiment_tracking:
  azure_ml: Jobs and runs with MLflow tracking
  vertex_ai: Vertex AI Experiments (and ML Metadata)
  sagemaker: SageMaker Experiments or managed MLflow
"""
t = yaml.safe_load(TABLE)
CLOUDS = {"azure_ml", "vertex_ai", "sagemaker"}
for concept, row in t.items():
    assert set(row) == CLOUDS, (concept, set(row) ^ CLOUDS)
    assert all(isinstance(v, str) and v.strip() for v in row.values()), concept
print("concepts:", len(t), "all have", sorted(CLOUDS))
# one-to-one check: where do the three clouds NOT line up as a single named object?
NOT_ONE_TO_ONE = ["workspace_or_project", "compute", "data_access", "environments"]
for c in NOT_ONE_TO_ONE:
    print(f"{c:22} azure={t[c]['azure_ml']!r:.45}  vertex={t[c]['vertex_ai']!r:.45}")
# negative test: a missing cell must fail
broken = yaml.safe_load(TABLE); del broken["monitoring"]["vertex_ai"]
try:
    for concept, row in broken.items():
        assert set(row) == CLOUDS, (concept, sorted(CLOUDS - set(row)))
except AssertionError as e:
    print("broken table rejected:", e)
