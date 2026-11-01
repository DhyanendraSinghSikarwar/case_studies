"""Q21 Vertex: AutoMLTabularTrainingJob constructed offline with anonymous credentials. run() NOT called."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.auth.credentials import AnonymousCredentials
import google.cloud.aiplatform as aip
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
aip.init(project="demo-proj", location="asia-south1", credentials=AnonymousCredentials())
job = aip.AutoMLTabularTrainingJob(display_name="churn-automl", optimization_prediction_type="classification",
        optimization_objective="maximize-au-roc")
print(type(job).__name__, "| objective:", job._optimization_objective, "| type:", job._optimization_prediction_type)
print("run() signature has budget arg:", "budget_milli_node_hours" in job.run.__code__.co_varnames)
