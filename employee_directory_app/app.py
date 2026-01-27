#!/usr/bin/env python3
import os

import aws_cdk as cdk

from employee_directory_app.stacks.iam_stack import IamStack
from employee_directory_app.stacks.compute_stack import ComputeStack
from employee_directory_app.stacks.data_stack import DataStack

app = cdk.App()

env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
)

iam_stack = IamStack(app, "IamStack", env=env)
data_stack = DataStack(app, "DataStack", env=env)
compute_stack = ComputeStack(
    app,
    "ComputeStack",
    ec2_role=iam_stack.ec2_role,
    photos_bucket=data_stack.photos_bucket,
    env=env
)

compute_stack.add_dependency(iam_stack)
compute_stack.add_dependency(data_stack)

app.synth()
