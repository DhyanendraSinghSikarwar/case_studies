"""Q26 Vertex: ExplanationParameters proto (sampled Shapley) built offline; nothing sent."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.cloud.aiplatform_v1.types import ExplanationParameters, SampledShapleyAttribution
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
p = ExplanationParameters(sampled_shapley_attribution=SampledShapleyAttribution(path_count=10), top_k=3)
print(ExplanationParameters.to_json(p, indent=None))
