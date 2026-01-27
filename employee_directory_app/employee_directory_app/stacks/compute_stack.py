import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
from aws_cdk import Stack, CfnParameter
from constructs import Construct


class ComputeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, ec2_role: iam.IRole, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        photos_bucket_param = CfnParameter(
            self,
            "PhotosBucketName",
            type="String",
            description="Name of S3 bucket for PHOTOS_BUCKET (i.e: my-photos-bucket)",
        )

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
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash -ex",
            "yum -y update",
            "yum -y install wget unzip python3-pip",
            "cd /home/ec2-user",
            "wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/DEV-AWS-MO-GCNv2/FlaskApp.zip",
            "unzip -o FlaskApp.zip",
            "cd FlaskApp",
            "pip3 install -r requirements.txt",
            "yum -y install stress",
            f"echo 'PHOTOS_BUCKET={photos_bucket_param.value_as_string}' >> /etc/environment",
            "echo 'AWS_DEFAULT_REGION=us-east-1' >> /etc/environment",
            "echo 'DYNAMO_MODE=on' >> /etc/environment",
            # systemd service to keep it alive
            "cat > /etc/systemd/system/employee-flask.service << 'EOF'\n"
            "[Unit]\n"
            "Description=Employee Flask App\n"
            "After=network.target\n\n"
            "[Service]\n"
            "Type=simple\n"
            "WorkingDirectory=/home/ec2-user/FlaskApp\n"
            "EnvironmentFile=/etc/environment\n"
            "User=root\n"
            "ExecStart=/usr/bin/python3 -m flask --app application.py run --host=0.0.0.0 --port=80\n"
            "Restart=always\n"
            "RestartSec=3\n\n"
            "[Install]\n"
            "WantedBy=multi-user.target\n"
            "EOF",
            "systemctl daemon-reload",
            "systemctl enable employee-flask",
            "systemctl start employee-flask",
        )

        instance = ec2.Instance(
            self,
            "EmployeeWebInstance",
            vpc=vpc,
            security_group=sg,
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            role=ec2_role,
            user_data=user_data,
        )

        # (Opcional) muestra el public IP en outputs si lo quieres luego
        # from aws_cdk import CfnOutput
        # CfnOutput(self, "PublicIp", value=instance.instance_public_ip)
