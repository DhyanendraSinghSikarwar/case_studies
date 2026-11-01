import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

import json
def check(d):
    errs = []; st = d.get("States", {})
    if "StartAt" not in d: errs.append("no StartAt")
    elif d["StartAt"] not in st: errs.append("StartAt unknown: " + d["StartAt"])
    terminal = 0
    for n, s in st.items():
        t = s.get("Type"); nxt = []
        if t in ("Succeed", "Fail"): terminal += 1
        elif t == "Choice":
            nxt = [c["Next"] for c in s.get("Choices", [])] + ([s["Default"]] if "Default" in s else [])
        else:
            if s.get("End"): terminal += 1
            elif "Next" in s: nxt = [s["Next"]]
            else: errs.append(n + ": no Next or End")
        for c in s.get("Catch", []): nxt.append(c["Next"])
        for x in nxt:
            if x not in st: errs.append(f"{n}: Next '{x}' not found")
    if terminal == 0: errs.append("no terminal state")
    return errs
retry = [{"ErrorEquals": ["ThrottlingException", "SageMaker.AmazonSageMakerException"], "IntervalSeconds": 10, "BackoffRate": 2.0, "MaxAttempts": 4}]
flow = {"StartAt": "Train", "States": {
 "Train": {"Type": "Task", "Resource": "arn:aws:states:::sagemaker:createTrainingJob.sync", "Parameters": {"TrainingJobName.$": "$$.Execution.Name"}, "Retry": retry, "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "Failed"}], "Next": "Evaluate"},
 "Evaluate": {"Type": "Task", "Resource": "arn:aws:states:::lambda:invoke", "Next": "Gate"},
 "Gate": {"Type": "Choice", "Choices": [{"Variable": "$.Payload.auc", "NumericGreaterThanEquals": 0.9, "Next": "Deploy"}], "Default": "Failed"},
 "Deploy": {"Type": "Task", "Resource": "arn:aws:states:::sagemaker:createEndpoint", "End": True},
 "Failed": {"Type": "Fail", "Error": "QualityGate", "Cause": "auc below bar or training failed"}}}
print("good:", check(flow))
broken = json.loads(json.dumps(flow)); broken["States"]["Gate"]["Default"] = "Nowhere"; del broken["States"]["Deploy"]["End"]
print("broken:", check(broken))
with mock_aws():
    sf = boto3.client("stepfunctions")
    arn = sf.create_state_machine(name="train-eval-deploy", definition=json.dumps(flow), roleArn="arn:aws:iam::123456789012:role/sfn")["stateMachineArn"]
    print("created:", sf.describe_state_machine(stateMachineArn=arn)["status"])
    print("type:", sf.describe_state_machine(stateMachineArn=arn)["type"])
    ex = sf.start_execution(stateMachineArn=arn, input="{}")["executionArn"]
    print("started; status reported by moto (no real state engine for these task ARNs):", sf.describe_execution(executionArn=ex)["status"])
