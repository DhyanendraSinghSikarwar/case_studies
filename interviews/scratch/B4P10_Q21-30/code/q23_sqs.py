import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

import json
with mock_aws():
    sqs = boto3.client("sqs")
    dlq = sqs.create_queue(QueueName="jobs-dlq")["QueueUrl"]
    dlq_arn = sqs.get_queue_attributes(QueueUrl=dlq, AttributeNames=["QueueArn"])["Attributes"]["QueueArn"]
    q = sqs.create_queue(QueueName="jobs", Attributes={"VisibilityTimeout": "30",
        "RedrivePolicy": json.dumps({"deadLetterTargetArn": dlq_arn, "maxReceiveCount": "2"})})["QueueUrl"]
    print("attrs:", {k: v for k, v in sqs.get_queue_attributes(QueueUrl=q, AttributeNames=["VisibilityTimeout", "RedrivePolicy"])["Attributes"].items()})
    sqs.send_message(QueueUrl=q, MessageBody="train-job-42")
    r1 = sqs.receive_message(QueueUrl=q, MaxNumberOfMessages=1)
    print("receive 1:", [m["Body"] for m in r1.get("Messages", [])])
    r2 = sqs.receive_message(QueueUrl=q, MaxNumberOfMessages=1)
    print("receive 2 right after (invisible):", r2.get("Messages", []))
    # worker 'crashes': shorten visibility to 0 so message returns (simulates timeout expiry)
    sqs.change_message_visibility(QueueUrl=q, ReceiptHandle=r1["Messages"][0]["ReceiptHandle"], VisibilityTimeout=0)
    r3 = sqs.receive_message(QueueUrl=q, MaxNumberOfMessages=1, AttributeNames=["ApproximateReceiveCount"])
    m = r3["Messages"][0]
    print("receive 3 after timeout expiry:", m["Body"], "ReceiveCount:", m["Attributes"]["ApproximateReceiveCount"], "-> duplicate delivery")
    # idempotent handler
    done = set()
    def handle(body):
        if body in done: return "skipped (already done)"
        done.add(body); return "processed"
    print(handle(m["Body"]), "|", handle(m["Body"]))
