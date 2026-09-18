"""Exact additive SHAP for first-order GAMs / EBMs with interactions=0.

TreeSHAP is not used: EBM is not a tree ensemble of the kind TreeSHAP expects.

For f(x) = intercept + sum_i g_i(x_i), interventional Shapley values are
phi_i(x) = g_i(x_i) - E_background[g_i]. This is the quantity shap.AdditiveExplainer
computes for first-order GAMs. shap 0.52 AdditiveExplainer cannot be applied
directly to mixed string categoricals (Independent masker requires numeric
arrays; encoding categories as floats broke additivity). The closed form is
therefore used, on the EBM logit/link scale.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from explainability.ebm_attribution import eval_terms, intercept
from preprocessing.lendingclub_preprocessor import PRIMARY_PREDICTORS

OUTPUT_SPACE = "ebm_decision_function_logit_link"
EXPLAINER_TYPE = "exact_additive_shap_from_ebm_terms"


def background_term_means(model, background: pd.DataFrame) -> np.ndarray:
    return eval_terms(model, background).mean(axis=0)


def additive_shap(terms: np.ndarray, background_means: np.ndarray) -> np.ndarray:
    return np.asarray(terms, dtype=float) - np.asarray(background_means, dtype=float)


def shap_base_value(intercept_value: float, background_means: np.ndarray) -> float:
    return float(intercept_value + np.asarray(background_means, dtype=float).sum())


def explain_frame(model, frame: pd.DataFrame, background: pd.DataFrame) -> dict[str, np.ndarray | float]:
    terms = eval_terms(model, frame)
    means = background_term_means(model, background)
    phi = additive_shap(terms, means)
    intercept_value = intercept(model)
    base = shap_base_value(intercept_value, means)
    return {
        "terms": terms,
        "shap_values": phi,
        "background_means": means,
        "intercept": intercept_value,
        "base_value": base,
        "decision": terms.sum(axis=1) + intercept_value,
    }


def global_shap_stats(shap_values: np.ndarray) -> pd.DataFrame:
    abs_s = np.abs(shap_values)
    rows = []
    for i, name in enumerate(PRIMARY_PREDICTORS):
        col = abs_s[:, i]
        rows.append(
            {
                "feature": name,
                "mean_abs": float(col.mean()),
                "median_abs": float(np.median(col)),
                "std_abs": float(col.std(ddof=1)),
                "p25_abs": float(np.quantile(col, 0.25)),
                "p75_abs": float(np.quantile(col, 0.75)),
                "mean_signed": float(shap_values[:, i].mean()),
            }
        )
    out = pd.DataFrame(rows)
    out["rank"] = out["mean_abs"].rank(ascending=False, method="first").astype(int)
    return out.sort_values("rank").reset_index(drop=True)


def shap_config(n_explained: int | None = None) -> dict:
    import shap

    payload = {
        "shap_library_version": shap.__version__,
        "explainer_type": EXPLAINER_TYPE,
        "shap_explainer_class_used": None,
        "tree_shap": False,
        "tree_shap_reason": "EBM is a first-order GAM of bin terms, not a TreeSHAP-compatible forest.",
        "additive_explainer_not_used_reason": (
            "shap.AdditiveExplainer is the matching algorithm, but shap's Independent masker "
            "does not accept mixed string categoricals; float-encoding categories broke additivity."
        ),
        "output_space": OUTPUT_SPACE,
        "link_function": "EBM logit/link; probability is sigmoid(decision_function)",
        "background": "TRAIN rows after Stage 4A train-only imputation; mean term values",
        "additive_identity": "phi_i(x) = g_i(x_i) - mean_TRAIN g_i",
    }
    if n_explained is not None:
        payload["n_explained_observations"] = int(n_explained)
    return payload
