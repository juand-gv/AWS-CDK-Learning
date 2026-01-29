from __future__ import annotations

import os
from pathlib import Path

from aws_cdk import Stack
from constructs import Construct

from employee_directory.config_loader import load_lambdas_config
from employee_directory.constructs.configurable_lambda import ConfigurableLambda


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        project_root = str(Path(__file__).resolve().parents[2])
        cfg = load_lambdas_config(project_root)

        for logical_id, lambda_cfg in cfg.lambdas.items():
            ConfigurableLambda(
                self,
                f"Lambda_{logical_id}",
                cfg=lambda_cfg,
            )
