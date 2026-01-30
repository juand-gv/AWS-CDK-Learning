from __future__ import annotations

from pathlib import Path

from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from config.config_loader import load_flask_ec2_config
from employee_directory.constructs.configurable_ec2_flask_instance import ConfigurableEc2FlaskInstance

from config.ssm_paths import app_prefix, safe_id


class ComputeStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        project_root = str(Path(__file__).resolve().parents[2])
        root_cfg = load_flask_ec2_config(project_root)
        family_cfg = root_cfg.flask_ec2

        prefix = app_prefix(self)

        role_arn = ssm.StringParameter.value_for_string_parameter(
            self, f"{prefix}/iam/ec2_role_arn"
        )

        ec2_role = iam.Role.from_role_arn(self, "ImportedEc2Role", role_arn, mutable=False)

        bucket_name = ssm.StringParameter.value_for_string_parameter(
            self, f"{prefix}/s3/buckets/photos/bucket_name"
        )

        photos_bucket = s3.Bucket.from_bucket_name(self, "ImportedPhotosBucket", bucket_name)

        for icfg in family_cfg.instances:
            sid = safe_id(icfg.name)

            inst = ConfigurableEc2FlaskInstance(
                self,
                f"FlaskEc2_{sid}",
                family_cfg=family_cfg,
                cfg=icfg,
                ec2_role=ec2_role,
                photos_bucket=photos_bucket,
            )

            instance = inst.instance
            sg = inst.security_group


            base = f"{prefix}/compute/ec2/{icfg.name}"

            ssm.StringParameter(
                self,
                f"SSM_{sid}_InstanceId",
                parameter_name=f"{base}/instance_id",
                string_value=instance.instance_id,
            )

            ssm.StringParameter(
                self,
                f"SSM_{sid}_InstanceArn",
                parameter_name=f"{base}/instance_arn",
                string_value=instance.instance_arn,
            )

            ssm.StringParameter(
                self,
                f"SSM_{sid}_SecurityGroupId",
                parameter_name=f"{base}/security_group_id",
                string_value=sg.security_group_id,
            )



