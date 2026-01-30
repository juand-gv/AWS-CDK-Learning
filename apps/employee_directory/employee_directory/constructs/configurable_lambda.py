from __future__ import annotations

from aws_cdk import Duration
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from constructs import Construct

from typing import Optional

from employee_directory.models.lambda_config import LambdaFunctionConfig


_RUNTIME_MAP = {
    "python3.12": _lambda.Runtime.PYTHON_3_12,
    "python3.11": _lambda.Runtime.PYTHON_3_11,
    "python3.10": _lambda.Runtime.PYTHON_3_10,
}


class ConfigurableLambda(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, cfg: LambdaFunctionConfig) -> None:
        super().__init__(scope, construct_id)

        fn = _lambda.Function(
            self,
            "Function",
            function_name=cfg.function_name,
            runtime=_RUNTIME_MAP[cfg.runtime],
            handler=cfg.handler,
            code=_lambda.Code.from_asset(cfg.entry),
            timeout=Duration.seconds(cfg.timeout),
            memory_size=cfg.memory,
            environment=cfg.environment,
        )

        # IAM permissions (mínimas y declarativas)
        if cfg.permissions.actions:
            fn.add_to_role_policy(
                iam.PolicyStatement(
                    actions=cfg.permissions.actions,
                    resources=cfg.permissions.resources or ["*"],
                )
            )

        # Optional: Scheduler
        self.rule: Optional[events.Rule] = None
        if cfg.schedule_expression:
            self.rule = events.Rule(
                self,
                "ScheduleRule",
                schedule=events.Schedule.expression(cfg.schedule_expression),
            )
            self.rule.add_target(targets.LambdaFunction(fn))

        self.function = fn
