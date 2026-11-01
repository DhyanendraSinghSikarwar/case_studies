import requests
URL = "https://runtime.sagemaker.ap-south-1.amazonaws.com/endpoints/churn-prod/invocations"
def score(x): return requests.post(URL, json=x, timeout=2).json()
