from __future__ import annotations

from pathlib import Path

from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from constructs import Construct

from employee_directory.config_loader import load_flask_ec2_config
from employee_directory.constructs.configurable_ec2_flask_instance import ConfigurableEc2FlaskInstance


class ComputeStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        ec2_role: iam.IRole,
        photos_bucket: s3.IBucket,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        project_root = str(Path(__file__).resolve().parents[2])
        root_cfg = load_flask_ec2_config(project_root)
        family_cfg = root_cfg.flask_ec2

        for icfg in family_cfg.instances:
            ConfigurableEc2FlaskInstance(
                self,
                f"FlaskEc2-{icfg.name}",
                family_cfg=family_cfg,
                cfg=icfg,
                ec2_role=ec2_role,
                photos_bucket=photos_bucket,
            )
