"""Q21 Azure: automl.classification built offline. Nothing submitted."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml import automl, Input
print("azure-ai-ml", md.version("azure-ai-ml"))
j = automl.classification(compute="cpu-cluster", experiment_name="churn-automl",
        training_data=Input(type="mltable", path="./train_mltable"), target_column_name="churned",
        primary_metric="AUC_weighted", n_cross_validations=3, enable_model_explainability=True)
j.set_limits(timeout_minutes=60, trial_timeout_minutes=10, max_trials=20, max_concurrent_trials=2, enable_early_termination=True)
j.set_training(allowed_training_algorithms=["LightGBM", "LogisticRegression"], enable_onnx_compatible_models=True)
print("task:", j.task_type, "| metric:", j.primary_metric, "| target:", j.target_column_name)
L = j.limits
print("limits:", dict(timeout_minutes=L.timeout_minutes, trial_timeout_minutes=L.trial_timeout_minutes,
      max_trials=L.max_trials, max_concurrent_trials=L.max_concurrent_trials, early=L.enable_early_termination))
print("allowed algos:", j.training.allowed_training_algorithms, "| onnx:", j.training.enable_onnx_compatible_models)
