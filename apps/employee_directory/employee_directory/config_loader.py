from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, TypeVar

import yaml

from employee_directory.models.lambda_config import LambdasConfig
from employee_directory.models.compute_flask_config import RootFlaskEc2Config
from employee_directory.models.iam_config import IamConfig

T = TypeVar("T")


def _load_yaml(project_root: str, rel_path: str) -> tuple[Path, dict[str, Any], Path]:
    root = Path(project_root)
    path = root / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    if not isinstance(raw, dict):
        raise ValueError(f"Config must be a YAML mapping (dict). Got: {type(raw).__name__} in {path}")

    return root, raw, path


def _load_config(
    project_root: str,
    rel_path: str,
    validator: Callable[[dict[str, Any]], T],
    post_validate: Callable[[T, Path], None] | None = None,
) -> T:
    root, raw, _path = _load_yaml(project_root, rel_path)
    cfg = validator(raw)
    if post_validate:
        post_validate(cfg, root)
    return cfg


# -------------------------
# Lambdas
# -------------------------
def load_lambdas_config(project_root: str, rel_path: str = "config/lambdas.yaml") -> LambdasConfig:
    def _post(cfg: LambdasConfig, root: Path) -> None:
        # ✅ valida assets
        for logical_id, lcfg in cfg.lambdas.items():
            entry_path = root / lcfg.entry
            if not entry_path.exists():
                raise FileNotFoundError(
                    f"Lambda '{logical_id}' entry not found: {entry_path} "
                    f"(from entry='{lcfg.entry}')"
                )

    return _load_config(
        project_root=project_root,
        rel_path=rel_path,
        validator=LambdasConfig.model_validate,
        post_validate=_post,
    )


# -------------------------
# Compute (Flask EC2)
# -------------------------
def load_flask_ec2_config(project_root: str, rel_path: str = "config/compute_flask.yaml") -> RootFlaskEc2Config:
    return _load_config(
        project_root=project_root,
        rel_path=rel_path,
        validator=RootFlaskEc2Config.model_validate,
    )


# -------------------------
# IAM
# -------------------------
def load_iam_config(project_root: str, rel_path: str = "config/iam.yaml") -> IamConfig:
    return _load_config(
        project_root=project_root,
        rel_path=rel_path,
        validator=IamConfig.model_validate,
    )
