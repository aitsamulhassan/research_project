# Audit schema (Stage 8)

Schema version: `1.0`  
Policy version: `stage8-v1`  
Machine copy: `audit/stage8_audit_schema.json`

## Purpose

An audit record lets another researcher reconstruct **why** the system produced an action, without exposing raw applicant identifiers.

## Required fields

| Field | Role |
| --- | --- |
| `audit_schema_version` | Schema identifier |
| `decision_id` | SHA-256 of the canonical logic payload (hex) |
| `event_timestamp` | When the record object was written. **Not** a logic input |
| `dataset_id` | Dataset name |
| `dataset_hash` | SHA-256 of the frozen raw file |
| `record_reference_hash` | `sha256("lc-row|{id}")[:16]` |
| `model_name` | `explainable_boosting_machine` |
| `model_version` | Stage 4B experiment id and seed |
| `preprocessor_version` | Stage 4A preprocessor script version |
| `calibrator_name` | `platt` |
| `calibrator_version` | Stage 5 experiment id |
| `raw_probability` | Frozen EBM raw score |
| `calibrated_probability` | Frozen Platt output |
| `credit_risk_band` | `LOW` / `MEDIUM` / `HIGH` |
| `top_explanation_features` | Frozen Stage 6 global \|SHAP\| names (evidence, not a gate) |
| `shariah_evidence_completeness` | Layer A label |
| `shariah_governance_status` | Stage 7 overall status |
| `triggered_rule_ids` | Applicable Stage 7 rule ids |
| `rule_source_ids` | Source ids of those rules |
| `policy_version` | `stage8-v1` |
| `cost_scenario` | Assumed FN:FP label |
| `threshold_configuration` | `t_low`, `t_high`, policy type |
| `final_decision` | `APPROVE` / `HUMAN_REVIEW` / `REJECT` |
| `review_required` | Boolean |

## Timestamp policy

`event_timestamp` is attached after the logic payload is hashed. Changing the timestamp must not change `decision_id` or the action.

## Identifier policy

Published records must not contain `id`, `addr_state`, `zip_code`, `title`, `desc`, `issue_d`, or other raw applicant fields. `record_reference_hash` is the public reference.

## Reproducibility

For the same inputs and configuration, the logic payload is deterministic. Two runs may differ in `event_timestamp` only.

## Synthetic illustrations

Any example that is not a hashed LendingClub row must be labeled synthetic. Synthetic illustrations are not empirical LendingClub counts.
