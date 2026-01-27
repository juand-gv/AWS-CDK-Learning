#!/usr/bin/env python3
import os

import aws_cdk as cdk

from employee_directory_app.stacks.iam_stack import IamStack
from employee_directory_app.stacks.compute_stack import ComputeStack


app = cdk.App()

env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
)

iam_stack = IamStack(app, "IamStack", env=env)
ComputeStack(app, "ComputeStack", ec2_role=iam_stack.ec2_role, env=env)

app.synth()
