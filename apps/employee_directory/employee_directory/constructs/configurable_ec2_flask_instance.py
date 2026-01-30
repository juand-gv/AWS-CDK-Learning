from __future__ import annotations

from aws_cdk import Aws
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from constructs import Construct

from employee_directory.models.compute_flask_config import FlaskEc2Config


_APP_ZIP_URL = (
    "https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/DEV-AWS-MO-GCNv2/FlaskApp.zip"
)

class ConfigurableEc2FlaskInstance(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        cfg: FlaskEc2Config,
        ec2_role: iam.IRole,
        photos_bucket: s3.IBucket,
    ) -> None:
        super().__init__(scope, construct_id)

        vpc = ec2.Vpc.from_lookup(
            self,
            "DefaultVpc",
            is_default=cfg.vpc_is_default,
        )

        sg = ec2.SecurityGroup(
            self,
            "EmployeeWebSg",
            vpc=vpc,
            description="Allow HTTP",
            allow_all_outbound=True,
        )

        sg.add_ingress_rule(
            ec2.Peer.ipv4(cfg.allow_http_from),
            ec2.Port.tcp(cfg.http_port),
            "HTTP allowed (config-driven)",
        )

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash -ex",

            # Amazon Linux 2023 usa dnf
            "dnf -y update",
            "dnf -y install wget unzip python3-pip",

            # App
            "cd /home/ec2-user",
            f"wget {cfg.app_zip_url}",
            f"wget {_APP_ZIP_URL}",
            "unzip -o FlaskApp.zip",
            "cd FlaskApp",

            # pip
            "python3 -m pip install -U pip",
            "python3 -m pip install -r requirements.txt",
        )

        if cfg.install_debug_tools:
            user_data.add_commands(
                "dnf -y install stress",
                "python3 -c \"import flask; print('Flask version:', flask.__version__)\"",
            )

        # Env vars
        user_data.add_commands(
            f"echo 'PHOTOS_BUCKET={photos_bucket.bucket_name}' >> /etc/environment",
            f"echo 'AWS_DEFAULT_REGION={cfg.aws_default_region}' >> /etc/environment",
            f"echo 'AWS_DEFAULT_REGION={Aws.REGION}' >> /etc/environment",
            f"echo 'DYNAMO_MODE={cfg.dynamo_mode}' >> /etc/environment",
        )

        # systemd service
        user_data.add_commands(
            "cat > /etc/systemd/system/employee-flask.service << 'EOF'\n"
            "[Unit]\n"
            "Description=Employee Flask App\n"
            "After=network.target\n\n"
            "[Service]\n"
            "Type=simple\n"
            "WorkingDirectory=/home/ec2-user/FlaskApp\n"
            "EnvironmentFile=/etc/environment\n"
            "\n"
            "ExecStart=/usr/bin/python3 -m flask --app application run --host=0.0.0.0 --port=80\n"
            "Restart=always\n"
            "RestartSec=3\n\n"
            "[Install]\n"
            "WantedBy=multi-user.target\n"
            "EOF",
            "systemctl daemon-reload",
            "systemctl enable employee-flask",
            "systemctl restart employee-flask",
            "systemctl --no-pager -l status employee-flask || true",
        )

        self.instance = ec2.Instance(
            self,
            "EmployeeWebInstance",
            vpc=vpc,
            security_group=sg,
            instance_type=ec2.InstanceType(cfg.instance_type),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            role=ec2_role,
            user_data=user_data,
            associate_public_ip_address=cfg.associate_public_ip,
        )
