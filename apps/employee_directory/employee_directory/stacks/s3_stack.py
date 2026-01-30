from __future__ import annotations

from pathlib import Path

from aws_cdk import Stack
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from config.config_loader import load_s3_config
from config.ssm_paths import app_prefix, safe_id
from employee_directory.constructs.configurable_s3 import ConfigurableS3Bucket


class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        project_root = str(Path(__file__).resolve().parents[2])
        cfg = load_s3_config(project_root)

        prefix = app_prefix(self)
        self.buckets = {}

        for bcfg in cfg.buckets:
            bid = safe_id(bcfg.id)

            b = ConfigurableS3Bucket(
                self,
                f"Bucket_{bid}",
                cfg=bcfg,
            )

            self.buckets[bcfg.id] = b.bucket

            # ✅ Standard paths (new)
            base = f"{prefix}/s3/buckets/{bcfg.id}"

            ssm.StringParameter(
                self,
                f"SSM_{bid}_BucketName",
                parameter_name=f"{base}/bucket_name",
                string_value=b.bucket.bucket_name,
            )

            ssm.StringParameter(
                self,
                f"SSM_{bid}_BucketArn",
                parameter_name=f"{base}/bucket_arn",
                string_value=b.bucket.bucket_arn,
            )
