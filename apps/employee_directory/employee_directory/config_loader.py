from __future__ import annotations

from pathlib import Path
import yaml

from employee_directory.models.lambda_config import LambdasConfig
from employee_directory.models.compute_flask_config import RootFlaskEc2Config


def load_lambdas_config(project_root: str, rel_path: str = "config/lambdas.yaml") -> LambdasConfig:
    root = Path(project_root)
    path = root / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    cfg = LambdasConfig.model_validate(raw)

    # ✅ valida assets
    for logical_id, lcfg in cfg.lambdas.items():
        entry_path = root / lcfg.entry
        if not entry_path.exists():
            raise FileNotFoundError(
                f"Lambda '{logical_id}' entry not found: {entry_path} "
                f"(from entry='{lcfg.entry}')"
            )

    return cfg

def load_flask_ec2_config(project_root: str, rel_path: str = "config/compute_flask.yaml") -> RootFlaskEc2Config:
    root = Path(project_root)
    path = root / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    return RootFlaskEc2Config.model_validate(raw)
