from __future__ import annotations

from pathlib import Path

from aws_cdk import Stack
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from config.config_loader import load_iam_config
from employee_directory.constructs.configurable_iam_role import ConfigurableIamRole

from config.ssm_paths import app_prefix, safe_id


class IamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        project_root = str(Path(__file__).resolve().parents[2])

        cfg = load_iam_config(project_root=project_root)

        self.roles = {}

        for role_cfg in cfg.roles:
            sid = safe_id(role_cfg.id)

            role_construct = ConfigurableIamRole(
                self,
                f"IamRole-{sid}",
                config=role_cfg,
            )
            self.roles[role_cfg.id] = role_construct.role

        # Backward compat
        self.ec2_role = self.roles.get("employee_web_ec2_role")
        if self.ec2_role is None:
            available = ", ".join(self.roles.keys()) or "<none>"
            raise ValueError(
                "IAM role with id 'employee_web_ec2_role' was not found in iam.yaml. "
                f"Available role ids: {available}"
            )

        prefix = app_prefix(self)

        ssm.StringParameter(
            self,
            "SSM_Ec2RoleArn",
            parameter_name=f"{prefix}/iam/ec2_role_arn",
            string_value=self.ec2_role.role_arn,
        )

        ssm.StringParameter(
            self,
            "SSM_Ec2RoleName",
            parameter_name=f"{prefix}/iam/ec2_role_name",
            string_value=self.ec2_role.role_name,
        )
