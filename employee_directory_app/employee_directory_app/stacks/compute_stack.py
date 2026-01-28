import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3 as s3

from aws_cdk import Stack
from constructs import Construct


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

        vpc = ec2.Vpc.from_lookup(
            self,
            "DefaultVpc",
            is_default=True
        )

        sg = ec2.SecurityGroup(
            self,
            "EmployeeWebSg",
            vpc=vpc,
            description="Allow HTTP",
            allow_all_outbound=True,
        )

        # DEBUG: abierto a todo el mundo. Luego restringe a tu IP /32.
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "HTTP from anywhere"
        )

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash -ex",

            # Amazon Linux 2023 usa dnf
            "dnf -y update",
            "dnf -y install wget unzip python3-pip",

            # App
            "cd /home/ec2-user",
            "wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/DEV-AWS-MO-GCNv2/FlaskApp.zip",
            "unzip -o FlaskApp.zip",
            "cd FlaskApp",

            # Mejora reproducibilidad y reduce sorpresas
            "python3 -m pip install -U pip",
            "python3 -m pip install -r requirements.txt",

            # (opcional) util debug
            "dnf -y install stress",
            "python3 -c \"import flask; print('Flask version:', flask.__version__)\"",

            # Env vars
            f"echo 'PHOTOS_BUCKET={photos_bucket.bucket_name}' >> /etc/environment",
            "echo 'AWS_DEFAULT_REGION=us-east-1' >> /etc/environment",
            "echo 'DYNAMO_MODE=on' >> /etc/environment",

            # systemd service
            "cat > /etc/systemd/system/employee-flask.service << 'EOF'\n"
            "[Unit]\n"
            "Description=Employee Flask App\n"
            "After=network.target\n\n"
            "[Service]\n"
            "Type=simple\n"
            "WorkingDirectory=/home/ec2-user/FlaskApp\n"
            "EnvironmentFile=/etc/environment\n"
            "\n"
            "# Flask app: módulo 'application' (application.py) y busca 'app' por defecto.\n"
            "# Si tu objeto Flask NO se llama 'app', cambia a: --app application:<tu_variable>\n"
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

        instance = ec2.Instance(
            self,
            "EmployeeWebInstance",
            vpc=vpc,
            security_group=sg,
            instance_type=ec2.InstanceType("t3.micro"),
            # ✅ Cambiado a Amazon Linux 2023 para evitar OpenSSL viejo de AL2
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            role=ec2_role,
            user_data=user_data,
        )

        # Si luego quieres ver la IP en outputs:
        # from aws_cdk import CfnOutput
        # CfnOutput(self, "PublicIp", value=instance.instance_public_ip)
