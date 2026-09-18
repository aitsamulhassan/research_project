"""Load the versioned Stage 8 decision-policy configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
YAML_PATH = ROOT / "configs" / "stage8_decision_policy.yaml"
JSON_PATH = ROOT / "configs" / "stage8_decision_policy.json"


def load_policy_config(path: Path | None = None) -> dict[str, Any]:
    target = path or YAML_PATH
    if target.suffix.lower() == ".json":
        return json.loads(target.read_text(encoding="utf-8"))
    try:
        import yaml
    except ImportError:
        if JSON_PATH.exists():
            return json.loads(JSON_PATH.read_text(encoding="utf-8"))
        raise ImportError("PyYAML is required to load configs/stage8_decision_policy.yaml") from None
    payload = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Decision-policy configuration must be a mapping.")
    required = (
        "model_reference",
        "calibrator_reference",
        "cost_scenarios",
        "threshold_grid",
        "review_policy",
        "governance_policy",
        "audit_schema_version",
        "random_seed",
        "policy_version",
    )
    missing = [k for k in required if k not in payload]
    if missing:
        raise ValueError(f"Decision-policy configuration missing keys: {missing}")
    return payload
