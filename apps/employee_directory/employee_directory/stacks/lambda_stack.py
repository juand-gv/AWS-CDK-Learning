from __future__ import annotations

from pathlib import Path

from aws_cdk import Stack
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from config.config_loader import load_lambdas_config
from employee_directory.constructs.configurable_lambda import ConfigurableLambda

from config.ssm_paths import app_prefix, safe_id


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        project_root = str(Path(__file__).resolve().parents[2])
        cfg = load_lambdas_config(project_root)

        prefix = app_prefix(self)

        for logical_id, lambda_cfg in cfg.lambdas.items():

            sid = safe_id(logical_id)

            c = ConfigurableLambda(
                self,
                f"Lambda_{sid}",
                cfg=lambda_cfg,
            )

            base = f"{prefix}/lambda/{logical_id}"

            ssm.StringParameter(
                self,
                f"SSM_{sid}FunctionArn",
                parameter_name=f"{base}/function_arn",
                string_value=c.function.function_arn,
            )

            ssm.StringParameter(
                self,
                f"SSM_{sid}FunctionName",
                parameter_name=f"{base}/function_name",
                string_value=c.function.function_name,
            )

            if c.rule is not None:
                ssm.StringParameter(
                    self,
                    f"SSM_{sid}_RuleArn",
                    parameter_name=f"{base}/rule_arn",
                    string_value=c.rule.rule_arn,
                )
