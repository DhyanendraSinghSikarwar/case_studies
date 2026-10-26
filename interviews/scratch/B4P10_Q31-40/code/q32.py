# Q32: Lambda concurrency. Part 1 moto API shape; part 2 pure-Python tick simulation (NOT Lambda's real scaling).
import os, io, zipfile
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def moto_part():
    z = io.BytesIO()
    with zipfile.ZipFile(z, "w") as f: f.writestr("app.py", "def handler(e, c): return 1")
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="lam", AssumeRolePolicyDocument="{}")["Role"]["Arn"]
    lam = boto3.client("lambda")
    lam.create_function(FunctionName="score", Runtime="python3.12", Role=role, Handler="app.handler", Code={"ZipFile": z.getvalue()})
    print("put   :", lam.put_function_concurrency(FunctionName="score", ReservedConcurrentExecutions=10)["ReservedConcurrentExecutions"])
    print("get   :", lam.get_function_concurrency(FunctionName="score")["ReservedConcurrentExecutions"])
    sqs = boto3.client("sqs"); q = sqs.create_queue(QueueName="jobs")["QueueUrl"]
    arn = sqs.get_queue_attributes(QueueUrl=q, AttributeNames=["QueueArn"])["Attributes"]["QueueArn"]
    try:
        m = lam.create_event_source_mapping(FunctionName="score", EventSourceArn=arn, BatchSize=5,
                                            ScalingConfig={"MaximumConcurrency": 5})
        print("ESM   :", {k: m.get(k) for k in ("BatchSize", "ScalingConfig", "State")})
    except Exception as e:
        print("ESM   : error", type(e).__name__, str(e)[:100])
moto_part()
print("(API shape only: nothing was invoked, nothing was throttled)\n")

# ---- simulation: 1 tick = 1 second. Jobs arrive from SQS; each takes DUR ticks and holds 1 DB connection while running.
DUR, DB_LIMIT, TICKS = 3, 10, 60
def arrivals(t): return 20 if t < 20 else 0           # burst: 20 messages/s for 20 s = 400 messages, then quiet
def run(reserved):
    queue, running, db_over, max_run = 0, [], 0, 0
    backlog_peak = 0
    for t in range(TICKS):
        queue += arrivals(t)
        running = [r - 1 for r in running if r - 1 > 0]
        take = min(queue, reserved - len(running))   # no free slot: messages simply stay queued
        queue -= take; running += [DUR] * take
        max_run = max(max_run, len(running)); db_over += max(0, len(running) - DB_LIMIT)
        backlog_peak = max(backlog_peak, queue)
    # finish draining to see how long the backlog takes
    t = TICKS
    while queue or running:
        running = [r - 1 for r in running if r - 1 > 0]
        take = min(queue, reserved - len(running)); queue -= take; running += [DUR] * take
        t += 1
    return dict(reserved=reserved, peak_concurrent=max_run, secs_over_db_limit=db_over, peak_backlog=backlog_peak, seconds_to_drain=t)
print(f"{'reserved':>8} {'peak running':>12} {'excess connection-seconds':>27} {'peak backlog':>13} {'drain time (s)':>15}")
for r in (100, 30, 10):
    d = run(r)
    print(f"{d['reserved']:>8} {d['peak_concurrent']:>12} {d['secs_over_db_limit']:>27} {d['peak_backlog']:>13} {d['seconds_to_drain']:>15}")
print("rule of thumb checked: reserved <= DB_LIMIT keeps connections at the limit; backlog waits in SQS instead of hitting the DB")
