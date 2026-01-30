from __future__ import annotations

from aws_cdk import RemovalPolicy
from aws_cdk import aws_s3 as s3
from constructs import Construct

from employee_directory.models.s3_config import BucketConfig


class ConfigurableS3Bucket(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, cfg: BucketConfig) -> None:
        super().__init__(scope, construct_id)

        removal = RemovalPolicy.DESTROY if cfg.removal_policy == "destroy" else RemovalPolicy.RETAIN

        self.bucket = s3.Bucket(
            self,
            "Bucket",
            bucket_name=cfg.bucket_name,  # None => generated
            removal_policy=removal,
            auto_delete_objects=(cfg.auto_delete_objects and removal == RemovalPolicy.DESTROY),
        )
