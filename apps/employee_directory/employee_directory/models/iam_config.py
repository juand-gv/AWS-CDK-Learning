from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class AssumedByConfig(BaseModel):
    # The one needed so far is service. Possibility to add "account", "federated", etc
    service: str


class PolicyStatementConfig(BaseModel):
    effect: Literal["Allow", "Deny"] = "Allow"
    actions: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=lambda: ["*"])


class InlinePolicyConfig(BaseModel):
    name: str
    statements: List[PolicyStatementConfig] = Field(default_factory=list)


class RoleConfig(BaseModel):
    id: str
    role_name: str
    assumed_by: AssumedByConfig

    managed_policies: List[str] = Field(default_factory=list)
    inline_policies: List[InlinePolicyConfig] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("role id cannot be empty")
        return v

    @field_validator("role_name")
    @classmethod
    def validate_role_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("role_name cannot be empty")
        return v


class IamConfig(BaseModel):
    roles: List[RoleConfig] = Field(default_factory=list)
