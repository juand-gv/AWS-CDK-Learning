from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class FlaskEc2InstanceConfig(BaseModel):
    name: str

    sg_id: str
    instance_id: str

    allow_http_from: str
    http_port: int = Field(default=80, ge=1, le=65535)

    instance_type: str = "t3.micro"
    associate_public_ip: bool = True

    install_debug_tools: bool = True
    dynamo_mode: str = "on"


class FlaskEc2Config(BaseModel):
    vpc_is_default: bool = True
    instances: List[FlaskEc2InstanceConfig] = Field(default_factory=list)


class RootFlaskEc2Config(BaseModel):
    flask_ec2: FlaskEc2Config
