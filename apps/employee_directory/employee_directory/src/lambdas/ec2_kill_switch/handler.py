import os
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2")

# Opcional: IDs que jamás quieres apagar (por si algún día los necesitas)
NEVER_STOP = set(filter(None, os.getenv("NEVER_STOP_INSTANCE_IDS", "").split(",")))


def handler(event, context):
    region = os.getenv("AWS_REGION", "us-east-1")

    paginator = ec2.get_paginator("describe_instances")
    page_iter = paginator.paginate(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    to_stop = []
    for page in page_iter:
        for res in page.get("Reservations", []):
            for inst in res.get("Instances", []):
                iid = inst["InstanceId"]
                if iid in NEVER_STOP:
                    continue
                to_stop.append(iid)

    if not to_stop:
        print(f"[{region}] No RUNNING EC2 instances found. Nothing to stop.")
        return {"stopped": [], "region": region}

    print(f"[{region}] Stopping instances: {to_stop}")

    stopped, failed = [], []
    for i in range(0, len(to_stop), 50):
        batch = to_stop[i : i + 50]
        try:
            ec2.stop_instances(InstanceIds=batch)
            stopped.extend(batch)
        except ClientError as e:
            print(f"Failed stopping batch {batch}: {e}")
            failed.extend(batch)

    return {"stopped": stopped, "failed": failed, "region": region}
