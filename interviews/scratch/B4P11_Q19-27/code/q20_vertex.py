"""Q20 Vertex side: ModelMonitoringObjectiveConfig proto built offline (v1beta1 types); nothing sent."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.cloud.aiplatform_v1.types import (ModelDeploymentMonitoringObjectiveConfig, ModelMonitoringObjectiveConfig,
    ModelMonitoringAlertConfig, SamplingStrategy, ThresholdConfig)
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
obj = ModelMonitoringObjectiveConfig(
    training_dataset=ModelMonitoringObjectiveConfig.TrainingDataset(
        bigquery_source={"input_uri": "bq://my-proj.ds.train"}, target_field="label"),
    training_prediction_skew_detection_config=ModelMonitoringObjectiveConfig.TrainingPredictionSkewDetectionConfig(
        skew_thresholds={"age": ThresholdConfig(value=0.3)}),
    prediction_drift_detection_config=ModelMonitoringObjectiveConfig.PredictionDriftDetectionConfig(
        drift_thresholds={"age": ThresholdConfig(value=0.3)}))
dep = ModelDeploymentMonitoringObjectiveConfig(deployed_model_id="1234", objective_config=obj)
sampling = SamplingStrategy(random_sample_config=SamplingStrategy.RandomSampleConfig(sample_rate=0.2))
alert = ModelMonitoringAlertConfig(email_alert_config=ModelMonitoringAlertConfig.EmailAlertConfig(user_emails=["mlops@example.com"]))
print("sample_rate", sampling.random_sample_config.sample_rate, "| emails", list(alert.email_alert_config.user_emails))
print("skew thresholds:", {k: v.value for k, v in obj.training_prediction_skew_detection_config.skew_thresholds.items()})
print("types:", type(dep).__name__, type(obj).__name__)
