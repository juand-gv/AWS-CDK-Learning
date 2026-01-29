from aws_cdk import Stack, RemovalPolicy
from constructs import Construct
import aws_cdk.aws_s3 as s3


class DataStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.photos_bucket = s3.Bucket(
            self,
            "PhotosBucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )
