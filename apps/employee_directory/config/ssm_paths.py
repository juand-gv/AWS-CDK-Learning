from __future__ import annotations

import re
from aws_cdk import Stack


def app_prefix(scope) -> str:
    account = Stack.of(scope).account
    if not account or account == "unknown-account":
        raise ValueError(
            "AWS account is unresolved. Make sure you are passing env=Environment(account=..., region=...) "
            "or deploying with CDK_DEFAULT_ACCOUNT set."
        )
    return f"/employee-directory/{account}"


def safe_id(value: str) -> str:
    """
    Convert user-provided strings (yaml ids, names) into safe CDK construct IDs.

    Rules:
    - allow only [A-Za-z0-9_]
    - collapse multiple underscores
    - never start with a digit
    """
    v = (value or "").strip()
    v = re.sub(r"[^A-Za-z0-9_]", "_", v)
    v = re.sub(r"_+", "_", v)

    if not v:
        v = "id"

    if v[0].isdigit():
        v = f"id_{v}"

    return v
