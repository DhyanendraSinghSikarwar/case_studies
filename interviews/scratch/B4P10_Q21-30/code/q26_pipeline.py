import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

import json
def check(defn):
    errs = []
    if "Version" not in defn: errs.append("no Version")
    names = [s["Name"] for s in defn.get("Steps", [])]
    if len(names) != len(set(names)): errs.append("duplicate step names")
    pnames = {p["Name"] for p in defn.get("Parameters", [])}
    text = json.dumps(defn)
    import re
    for ref in re.findall(r'"Get": "Parameters\.([A-Za-z0-9_]+)"', text):
        if ref not in pnames: errs.append("unknown parameter " + ref)
    for s in defn.get("Steps", []):
        for k in ("Name", "Type", "Arguments"):
            if k not in s and s.get("Type") != "Condition": errs.append(f"{s.get('Name')}: missing {k}")
        for dep in s.get("DependsOn", []):
            if dep not in names: errs.append(f"{s['Name']}: DependsOn unknown {dep}")
        if s.get("Type") == "Condition":
            for br in ("IfSteps", "ElseSteps"):
                for sub in s.get("Arguments", {}).get(br, []):
                    if sub["Name"] not in names + [x["Name"] for x in s["Arguments"].get(br, [])]: errs.append("bad branch step")
    return errs
good = {"Version": "2020-12-01", "Parameters": [{"Name": "InputData", "Type": "String", "DefaultValue": "s3://ml/in"}],
 "Steps": [
  {"Name": "Prep", "Type": "Processing", "Arguments": {"ProcessingInputs": [{"S3Uri": {"Get": "Parameters.InputData"}}]}},
  {"Name": "Train", "Type": "Training", "DependsOn": ["Prep"], "Arguments": {"AlgorithmSpecification": {}}, "CacheConfig": {"Enabled": True, "ExpireAfter": "P30D"}},
  {"Name": "AucCheck", "Type": "Condition", "Arguments": {"Conditions": [{"Type": "GreaterThanOrEqualTo"}], "IfSteps": [{"Name": "Register", "Type": "RegisterModel", "Arguments": {}}], "ElseSteps": []}}]}
bad = json.loads(json.dumps(good)); bad["Steps"][1]["DependsOn"] = ["Nope"]; bad["Parameters"] = []
print("good errors:", check(good)); print("bad errors:", check(bad))
with mock_aws():
    sm = boto3.client("sagemaker")
    sm.create_pipeline(PipelineName="train-pipe", PipelineDefinition=json.dumps(good), RoleArn="arn:aws:iam::123456789012:role/sm")
    ex = sm.start_pipeline_execution(PipelineName="train-pipe")["PipelineExecutionArn"]
    print("execution status (API shape only):", sm.describe_pipeline_execution(PipelineExecutionArn=ex)["PipelineExecutionStatus"])
    try:
        print("steps listed:", len(sm.list_pipeline_execution_steps(PipelineExecutionArn=ex)["PipelineExecutionSteps"]))
    except Exception as e:
        print("list_pipeline_execution_steps:", type(e).__name__, str(e)[:70])
    print("moto reports a status but no step ran: no processing, no training, no condition evaluated")
