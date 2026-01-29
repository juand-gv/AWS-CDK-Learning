from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class PermissionConfig(BaseModel):
    actions: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=lambda: ["*"])


class LambdaFunctionConfig(BaseModel):
    function_name: str
    entry: str
    handler: str = "handler.handler"
    runtime: str = "python3.12"

    memory: int = Field(default=128, ge=128, le=10240)
    timeout: int = Field(default=60, ge=1, le=900)

    schedule_expression: Optional[str] = None
    environment: Dict[str, str] = Field(default_factory=dict)
    permissions: PermissionConfig = Field(default_factory=PermissionConfig)

    @field_validator("runtime")
    @classmethod
    def validate_runtime(cls, v: str) -> str:
        allowed = {"python3.12", "python3.11", "python3.10"}
        if v not in allowed:
            raise ValueError(f"Unsupported runtime '{v}'. Allowed: {sorted(allowed)}")
        return v

    @field_validator("schedule_expression")
    @classmethod
    def validate_schedule_expression(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not (v.startswith("cron(") or v.startswith("rate(")):
            raise ValueError("schedule_expression must start with cron( or rate(")
        return v


class LambdasConfig(BaseModel):
    lambdas: Dict[str, LambdaFunctionConfig]
