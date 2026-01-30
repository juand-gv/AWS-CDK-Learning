from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class BucketConfig(BaseModel):
    id: str
    bucket_name: Optional[str] = None  # None => CDK auto-name

    removal_policy: Literal["destroy", "retain"] = "destroy"
    auto_delete_objects: bool = True

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("bucket id cannot be empty")
        return v


class S3Config(BaseModel):
    buckets: List[BucketConfig] = Field(default_factory=list)
