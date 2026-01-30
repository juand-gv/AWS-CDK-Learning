from __future__ import annotations

from pathlib import Path

from aws_cdk import Stack
from constructs import Construct

from employee_directory.config_loader import load_iam_config
from employee_directory.constructs.configurable_iam_role import ConfigurableIamRole


class IamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        project_root = str(Path(__file__).resolve().parents[2])

        cfg = load_iam_config(project_root=project_root)

        self.roles = {}

        for role_cfg in cfg.roles:
            role_construct = ConfigurableIamRole(
                self,
                f"IamRole-{role_cfg.id}",
                config=role_cfg,
            )
            self.roles[role_cfg.id] = role_construct.role

        # Backward compat
        self.ec2_role = self.roles.get("employee_web_ec2_role")
