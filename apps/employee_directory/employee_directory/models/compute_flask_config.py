from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class FlaskEc2Config(BaseModel):
    vpc_is_default: bool = True

    allow_http_from: str
    http_port: int = Field(default=80, ge=1, le=65535)

    instance_type: str = "t3.micro"
    associate_public_ip: bool = True

    app_zip_url: str
    install_debug_tools: bool = True

    aws_default_region: str = "us-east-1"
    dynamo_mode: str = "on"


class RootFlaskEc2Config(BaseModel):
    flask_ec2: FlaskEc2Config
