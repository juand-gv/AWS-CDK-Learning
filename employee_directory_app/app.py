#!/usr/bin/env python3
import os

import aws_cdk as cdk

from employee_directory_app.stacks.iam_stack import IamStack
from employee_directory_app.stacks.compute_stack import ComputeStack


app = cdk.App()

env = cdk.Environment(
    account=app.node.try_get_context("account"),
    region=app.node.try_get_context("region"),
)

iam_stack = IamStack(app, "IamStack", env=env)
ComputeStack(app, "ComputeStack", ec2_role=iam_stack.ec2_role, env=env)

app.synth()
