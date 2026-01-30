#!/usr/bin/env python3
import os

import aws_cdk as cdk

from employee_directory.stacks.iam_stack import IamStack
from employee_directory.stacks.compute_stack import ComputeStack
from employee_directory.stacks.s3_stack import S3Stack
from employee_directory.stacks.lambda_stack import LambdaStack

app = cdk.App()

env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
)

iam_stack = IamStack(app, "IamStack", env=env)
s3_stack = S3Stack(app, "S3Stack", env=env)
compute_stack = ComputeStack(app,"ComputeStack", env=env)
lambda_stack = LambdaStack(app, "LambdaStack", env=env)

compute_stack.add_dependency(iam_stack)
compute_stack.add_dependency(s3_stack)

app.synth()
