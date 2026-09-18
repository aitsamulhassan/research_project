"""Stage 6 explainability: SHAP attribution vs EBM transparent-model reference.

Does not tune the frozen EBM. Does not use explanation results for model selection.
Does not claim causal effects. EBM is not treated as ground truth.
"""

from __future__ import annotations

import gc
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from calibration.platt import PlattCalibrator  # noqa: E402
from data.audit_datasets import EXPECTED_LC_FILENAME, RAW_DIR, git_commit, sha256_file  # noqa: E402
from explainability.ebm_attribution import (  # noqa: E402
    eval_terms,
    feature_type,
    global_abs_stats,
    intercept,
    shape_function,
)
from explainability.consistency import run_consistency_checks  # noqa: E402
from explainability.local_cases import local_payload, select_local_cases  # noqa: E402
from explainability.plots import (  # noqa: E402
    plot_beeswarm,
    plot_effect,
    plot_global_importance,
    plot_local_bars,
    plot_local_shap_vs_ebm,
    plot_seed_rank_heatmap,
)
from explainability.ranking import (  # noqa: E402
    comparison_table,
    kendall_ranks,
    overlap_at_k,
    sign_agreement,
    spearman_footrule,
    spearman_ranks,
)
from explainability.sampling import SAMPLE_N, SAMPLE_SEED, sample_split_frame  # noqa: E402
from explainability.shap_additive import (  # noqa: E402
    additive_shap,
    background_term_means,
    explain_frame,
    global_shap_stats,
    shap_config,
)
from explainability.stability import feature_stability, pairwise_spearman, rank_matrix  # noqa: E402
from models.common import FINAL_SEED, SEEDS, assert_predictor_frame  # noqa: E402
from models.ebm_model import ebm_config, ebm_model  # noqa: E402
from preprocessing.lendingclub_preprocessor import (  # noqa: E402
    FEATURE_POLICY_PATH,
    FORBIDDEN_COLUMNS,
    PREPROCESS_POLICY_PATH,
    PRIMARY_PREDICTORS,
    PREPROCESSOR_PATH,
    RECORDED_LC_SHA256,
    LendingClubPreprocessor,
    sha256_text_file,
)

EXPERIMENT_ID = "stage6-lc-ebm-explain-v1"
STAGE4B_ID = "stage4b-lc-granting-v1"
STAGE5_ID = "stage5-lc-ebm-calibration-v1"
FAMILY = "explainable_boosting_machine"
ASSIGNMENTS_PATH = ROOT / "results" / "tables" / "lendingclub_split_assignments.csv"
SPLIT_MANIFEST = ROOT / "audit" / "lendingclub_split_manifest.json"
STAGE4B_SELECTION = ROOT / "experiments" / "stage4b_credit_risk" / "selected_configurations.json"
STAGE5_SELECTION = ROOT / "experiments" / "stage5_calibration" / "selected_calibration.json"
EBM_SEED42 = ROOT / "results" / "calibration" / "artifacts" / "ebm_train_only_seed42.joblib"
PLATT_PATH = ROOT / "results" / "calibration" / "artifacts" / "platt_calibrator.joblib"
EXP_DIR = ROOT / "experiments" / "stage6_explainability"
OUT = ROOT / "results" / "explainability"
FIG = ROOT / "results" / "figures" / "explainability"
AUDIT = ROOT / "audit"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_splits() -> dict[str, pd.DataFrame]:
    usecols = ["id", "Default", *PRIMARY_PREDICTORS]
    raw = pd.read_csv(RAW_DIR / EXPECTED_LC_FILENAME, usecols=usecols, low_memory=False)
    assign = pd.read_csv(ASSIGNMENTS_PATH, usecols=["id", "split"])
    merged = raw.merge(assign, on="id", how="inner")
    if len(merged) != len(raw):
        raise RuntimeError("Assignments do not match raw rows.")
    if FORBIDDEN_COLUMNS.intersection(PRIMARY_PREDICTORS):
        raise RuntimeError("Frozen predictors include excluded columns.")
    out = {}
    for split in ("train", "validation", "test"):
        part = merged.loc[merged["split"] == split, ["id", "Default", *PRIMARY_PREDICTORS]].reset_index(drop=True)
        assert_predictor_frame(part.loc[:, PRIMARY_PREDICTORS])
        out[split] = part
    return out


def describe_shape(shape: dict) -> str:
    scores = np.asarray(shape["scores"], dtype=float)
    if shape["type"] == "continuous":
        edges = np.asarray(shape["names"], dtype=float)
        if len(edges) == len(scores) + 1:
            x = 0.5 * (edges[:-1] + edges[1:])
        else:
            x = edges[: len(scores)]
        if len(x) < 3:
            return "Too few bins to describe a pattern."
        corr = float(np.corrcoef(x, scores)[0, 1])
        if corr <= -0.8:
            return f"Fitted term tends to decrease as {shape['feature']} increases (bin-level Pearson={corr:.2f}); not a causal claim."
        if corr >= 0.8:
            return f"Fitted term tends to increase as {shape['feature']} increases (bin-level Pearson={corr:.2f}); not a causal claim."
        return f"Fitted term is not approximately monotone in {shape['feature']} (bin-level Pearson={corr:.2f})."
    names = [str(n) for n in shape["names"]]
    order = np.argsort(scores)
    low = names[int(order[0])]
    high = names[int(order[-1])]
    return (
        f"Category-specific terms on the logit scale; {shape['feature']} is not a numeric magnitude. "
        f"Largest negative fitted term: {low}. Largest positive fitted term: {high}."
    )


def get_or_train_ebm(seed: int, x_train: pd.DataFrame, y_train: np.ndarray) -> object:
    path = OUT / "artifacts" / f"ebm_train_only_seed{seed}.joblib"
    if seed == FINAL_SEED and EBM_SEED42.exists():
        model = joblib.load(EBM_SEED42)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            joblib.dump(model, path)
        return model
    if path.exists():
        return joblib.load(path)
    print(f"Fitting TRAIN-only EBM seed {seed} for attribution stability", flush=True)
    model = ebm_model(seed)
    model.fit(x_train, y_train)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return model


def run_pytest() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, text.strip()


def write_report(p: dict) -> None:
    t1 = p["table1"]
    lines = [
        "# Stage 6 Explainability Report",
        "",
        "## A. Explanation methodology",
        "",
        "The frozen Stage 4B model is an Explainable Boosting Machine with `interactions=0`. It is used here as a **transparent-model reference**, not as ground truth, not as a causal explanation, and not as an authoritative explanation.",
        "",
        "SHAP values are **model attributions** for this EBM, not causal effects and not proof that a feature causes default.",
        "",
        "TreeSHAP was not used: it is not mathematically appropriate for this EBM. `shap.AdditiveExplainer` is the matching SHAP algorithm for a first-order GAM, but shap 0.52's Independent masker does not accept mixed string categoricals, and encoding categories as floats broke additivity in a probe. Stage 6 therefore computes the closed-form additive interventional SHAP on the EBM logit/link scale:",
        "",
        "`phi_i(x) = g_i(x_i) - mean_{TRAIN} g_i`",
        "",
        "where `g_i` are native EBM term contributions from `eval_terms`. For a first-order additive model this is the Shapley value of feature i. Output space: EBM `decision_function` (logit/link). Probability is `sigmoid(decision)`. Platt calibration is a later monotone map `sigmoid(a * logit(p_raw) + b)` and is not inside the EBM.",
        "",
        f"Explanation sample: {SAMPLE_N} TEST rows, `RandomState({SAMPLE_SEED})` without replacement. Labels were not used to draw the sample or to choose local cases.",
        "",
        f"SHAP config: {json.dumps(p['shap_config'])}",
        "",
        "## B. Global attribution",
        "",
        "| Feature | SHAP mean(|value|) | SHAP rank | EBM mean(|contribution|) | EBM rank |",
        "| --- | --- | --- | --- | --- |",
    ]
    for _, r in t1.iterrows():
        lines.append(
            f"| {r['feature']} | {r['shap_mean_abs']:.6f} | {int(r['shap_rank'])} | {r['ebm_mean_abs']:.6f} | {int(r['ebm_rank'])} |"
        )
    bg_max = p.get("background_mean_max_abs", float("nan"))
    lines += [
        "",
        f"SHAP values are TRAIN-centered EBM terms (`phi_i = g_i - mean_TRAIN g_i`). Uncentered EBM magnitudes are `mean(|g_i|)` on the same explanation sample. Max `|mean_TRAIN g_i|` was {bg_max:.3e}, so the two global mean-absolute series are numerically identical at reported precision. This is a property of the fitted additive EBM, not evidence from a second model class. Ranks remain the primary comparison; raw magnitude is not treated as a second confirmatory scale.",
        "",
        "The model attributes the largest mean |SHAP| to `fico_n`, then `loan_amnt`, `dti_n`, `revenue`, and `home_ownership_n`. `addr_state` has the smallest mean |SHAP|. These are attributions of this EBM, not causes of default.",
        "",
        "## C. SHAP vs EBM comparison",
        "",
        "| Top-k | Overlap | Spearman correlation |",
        "| --- | --- | --- |",
        f"| 3 | {p['overlap3']:.3f} | {p['spearman']:.4f} |",
        f"| 5 | {p['overlap5']:.3f} | {p['spearman']:.4f} |",
        f"| 9 | {p['overlap9']:.3f} | {p['spearman']:.4f} |",
        "",
        f"Spearman rank correlation (full ranking): {p['spearman']:.4f}. Kendall tau: {p['kendall']:.4f}. Normalized Spearman footrule: {p['footrule']:.4f}.",
        "",
        f"Sign agreement between SHAP values and **centered** EBM terms (identity for this explainer): {p['sign_vs_centered']:.4f}.",
        f"Sign agreement between SHAP values and **uncentered** EBM terms: {p['sign_vs_raw_terms']:.4f}.",
        "",
        "EBM is used as a transparent-model reference for attribution comparison, not as ground truth. Perfect rank agreement is expected because additive SHAP is the centered EBM term vector. It is not independent confirmation from a second attribution method or a second predictive model.",
        "",
        "## D. Local explanations",
        "",
        "Cases were selected from the explanation sample by a frozen rule: maximum raw probability, minimum raw probability, closest to the sample median raw probability, and lowest Spearman correlation between local |SHAP| and local |EBM term| rankings. Ties broken by `row_ref`. Labels were not used.",
        "",
        "| Case | Raw probability | Calibrated probability | Top positive (SHAP) | Top negative (SHAP) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, label in (
        ("high_risk", "High raw p"),
        ("low_risk", "Low raw p"),
        ("median_risk", "Median raw p"),
        ("disagreement", "Deterministic lowest |SHAP| vs |EBM| rank correlation"),
    ):
        c = p["cases"][key]
        lines.append(
            f"| {label} | {c['p_raw']:.6f} | {c['p_calibrated']:.6f} | {', '.join(c['top_positive_shap'])} | {', '.join(c['top_negative_shap'])} |"
        )
    d_s = p.get("disagreement_spearman", p["cases"].get("disagreement", {}).get("local_rank_spearman"))
    lines += [
        "",
        f"The fourth case is selected by a frozen rule (lowest Spearman of local |SHAP| vs |EBM term| ranks; ties broken by `row_ref`), not by inspecting plots. Observed local Spearman for that case: {d_s}. Because TRAIN-mean EBM terms are numerically ~0, local SHAP rankings match local |EBM term| rankings; no substantial SHAP-vs-EBM rank disagreement exists in the sample.",
        "",
        "True labels are stored only as descriptive context in the case JSON and were not used to choose or alter explanations.",
        "",
        "## E. Seed stability",
        "",
        "| Feature | Mean SHAP importance | SD | Mean rank | Rank SD | Top-3 frequency | Top-5 frequency |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for _, r in p["stability"].iterrows():
        lines.append(
            f"| {r['feature']} | {r['mean_importance']:.6f} | {r['sd_importance']:.6f} | {r['mean_rank']:.2f} | {r['rank_sd']:.2f} | {r['top3_frequency']:.2f} | {r['top5_frequency']:.2f} |"
        )
    lines += [
        "",
        f"Pairwise Spearman between seeds (mean): {p['pairwise_spearman_mean']:.4f}. Mean pairwise top-3 overlap: {p.get('pairwise_top3_mean', float('nan')):.4f}. Mean pairwise top-5 overlap: {p.get('pairwise_top5_mean', float('nan')):.4f}. Reported as mean ± SD across the five frozen seeds. No seed was selected as best.",
        "",
        "## F. Calibration relationship",
        "",
        p["calibration_text"],
        "",
        "## G. Feature effects",
        "",
        "| Feature | Type | Observed pattern | Attribution scale |",
        "| --- | --- | --- | --- |",
    ]
    for row in p["effects"]:
        lines.append(f"| {row['feature']} | {row['type']} | {row['pattern']} | {row['scale']} |")
    lines += [
        "",
        "ZIP codes and other categoricals are identities, not numeric distances. Associations are model attributions, not causes of default.",
        "",
        "## H. Limitations",
        "",
        "- Attributions describe this EBM, not the data-generating process.",
        "- Additive SHAP equals centered EBM terms. Agreement is expected; it is not independent confirmation from a second model class.",
        "- KernelSHAP on the probability scale was not used, so probability-space SHAP rankings were not estimated separately.",
        "- The explanation sample is 5,000 TEST rows, not the full test set.",
        "- Stage 6 uses the TRAIN-only EBM that Stage 5 calibrated. Stage 4B test metrics used a TRAIN+VALIDATION refit; those two EBMs are not mixed here.",
        "- High-cardinality `zip_code` effect plots show the largest-magnitude categories only.",
        "- No Shariah, threshold, or decision-policy analysis was performed.",
        "",
        "## I. Reproducibility",
        "",
        f"- explainability_experiment_id: `{EXPERIMENT_ID}`",
        f"- dataset_hash: `{p['dataset_hash']}`",
        f"- split_manifest_hash: `{p['split_hash']}`",
        f"- preprocessing_policy_hash: `{p['prep_hash']}`",
        f"- git_commit: `{p['git_commit']}`",
        f"- libraries: {json.dumps(p['versions'])}",
        f"- sample_seed: {SAMPLE_SEED}; sample_n: {SAMPLE_N}; model seeds: {SEEDS}",
        "",
        "## J. Tests",
        "",
        p.get("test_suite_summary", "Not run."),
        "",
        "## K. Stage gate",
        "",
        f"`STAGE_6_STATUS = {p['status']}`",
        "",
        p.get("status_reason", ""),
        "",
        "Stage 7 was not started.",
        "",
    ]
    (ROOT / "docs" / "STAGE_6_EXPLAINABILITY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    for path in (OUT / "tables", OUT / "metrics", OUT / "artifacts", OUT / "sample", FIG, EXP_DIR):
        path.mkdir(parents=True, exist_ok=True)

    dataset_hash = sha256_file(RAW_DIR / EXPECTED_LC_FILENAME)
    if dataset_hash != RECORDED_LC_SHA256:
        print("HARD STOP: raw hash changed.", file=sys.stderr)
        return 2
    if json.loads(STAGE4B_SELECTION.read_text(encoding="utf-8"))["selected_family"] != FAMILY:
        print("HARD STOP: Stage 4B family is not EBM.", file=sys.stderr)
        return 2
    if json.loads(STAGE5_SELECTION.read_text(encoding="utf-8"))["selected_method"] != "platt":
        print("HARD STOP: Stage 5 method is not Platt.", file=sys.stderr)
        return 2

    splits = load_splits()
    prep = joblib.load(PREPROCESSOR_PATH)
    x_train = prep.transform_imputed_frame(splits["train"].loc[:, PRIMARY_PREDICTORS])
    y_train = splits["train"]["Default"].to_numpy()
    x_test = prep.transform_imputed_frame(splits["test"].loc[:, PRIMARY_PREDICTORS])
    x_test.index = splits["test"].index
    x_train.index = splits["train"].index

    test_full = splits["test"].copy()
    for col in PRIMARY_PREDICTORS:
        test_full[col] = x_test[col].to_numpy()
    sample = sample_split_frame(test_full, SAMPLE_N, SAMPLE_SEED)
    sample_x = sample.loc[:, PRIMARY_PREDICTORS]
    bg = x_train

    sample_out = sample[["row_ref", "sample_position", "source_iloc"]].copy()
    sample_out["split"] = "test"
    sample_out["experiment_id"] = EXPERIMENT_ID
    sample_out["sampling_seed"] = SAMPLE_SEED
    sample_out["sampling_rule"] = "deterministic_random_without_replacement_labels_not_used"
    sample_out.to_csv(OUT / "sample" / "explanation_sample_row_refs.csv", index=False)

    model42 = get_or_train_ebm(FINAL_SEED, x_train, y_train)
    intercept_before = intercept(model42)
    terms_imp_before = np.asarray(model42.term_importances(), dtype=float).copy()
    platt: PlattCalibrator = joblib.load(PLATT_PATH)
    explained = explain_frame(model42, sample_x, bg)
    shap_values = explained["shap_values"]
    terms = explained["terms"]
    p_raw = model42.predict_proba(sample_x)[:, 1]
    p_cal = platt.transform(p_raw)
    intercept_after = intercept(model42)
    if intercept_before != intercept_after or not np.allclose(terms_imp_before, model42.term_importances()):
        raise RuntimeError("Platt application modified frozen EBM parameters.")

    decision = explained["decision"]
    reconstructed = shap_values.sum(axis=1) + explained["base_value"]
    add_err = float(np.max(np.abs(reconstructed - decision)))
    print(f"Additive SHAP max reconstruction error: {add_err}", flush=True)

    shap_stats = global_shap_stats(shap_values)
    ebm_stats = global_abs_stats(terms)
    shap_stats = shap_stats.assign(experiment_id=EXPERIMENT_ID, scale="additive_shap_logit_link")
    ebm_stats = ebm_stats.assign(experiment_id=EXPERIMENT_ID, scale="uncentered_ebm_term_logit_link")
    shap_imp = shap_stats.set_index("feature").loc[list(PRIMARY_PREDICTORS), "mean_abs"].to_numpy()
    ebm_imp = ebm_stats.set_index("feature").loc[list(PRIMARY_PREDICTORS), "mean_abs"].to_numpy()
    table1 = comparison_table(shap_imp, ebm_imp)
    table1["experiment_id"] = EXPERIMENT_ID
    table1.to_csv(OUT / "tables" / "table1_global_attribution.csv", index=False)
    shap_stats.to_csv(OUT / "tables" / "shap_global_distribution.csv", index=False)
    ebm_stats.to_csv(OUT / "tables" / "ebm_global_distribution.csv", index=False)

    overlap3 = overlap_at_k(shap_imp, ebm_imp, 3)
    overlap5 = overlap_at_k(shap_imp, ebm_imp, 5)
    overlap9 = overlap_at_k(shap_imp, ebm_imp, 9)
    spearman = spearman_ranks(shap_imp, ebm_imp)
    kendall = kendall_ranks(shap_imp, ebm_imp)
    footrule = spearman_footrule(shap_imp, ebm_imp)["footrule_normalized"]
    centered_terms = terms - explained["background_means"]
    sign_c = sign_agreement(shap_values.ravel(), centered_terms.ravel())
    sign_u = sign_agreement(shap_values.ravel(), terms.ravel())
    dump_json(
        OUT / "metrics" / "shap_vs_ebm_agreement.json",
        {
            "overlap_top3": overlap3,
            "overlap_top5": overlap5,
            "overlap_top9": overlap9,
            "spearman": spearman,
            "kendall": kendall,
            "footrule_normalized": footrule,
            "sign_agreement_vs_centered_terms": sign_c,
            "sign_agreement_vs_uncentered_terms": sign_u,
            "additive_reconstruction_max_abs_error": add_err,
            "background_means": {
                name: float(explained["background_means"][i]) for i, name in enumerate(PRIMARY_PREDICTORS)
            },
            "background_mean_max_abs": float(np.max(np.abs(explained["background_means"]))),
            "experiment_id": EXPERIMENT_ID,
        },
    )
    pd.DataFrame(
        [{"top_k": k, "overlap": overlap_at_k(shap_imp, ebm_imp, k), "spearman": spearman} for k in (3, 5, 9)]
    ).assign(experiment_id=EXPERIMENT_ID).to_csv(OUT / "tables" / "table2_shap_ebm_agreement.csv", index=False)

    np.savez_compressed(
        OUT / "artifacts" / "seed42_attributions.npz",
        shap_values=shap_values,
        ebm_terms=terms,
        p_raw=p_raw,
        p_cal=p_cal,
        decision=decision,
        background_means=explained["background_means"],
        base_value=np.array([explained["base_value"]]),
        row_ref=np.asarray(sample["row_ref"]),
        source_iloc=np.asarray(sample["source_iloc"]),
    )
    dump_json(
        OUT / "artifacts" / "seed42_attributions.meta.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "model_id": "ebm_train_only_seed42",
            "model_path": str((OUT / "artifacts" / "ebm_train_only_seed42.joblib").relative_to(ROOT)).replace("\\", "/"),
            "stage5_model_path": str(EBM_SEED42.relative_to(ROOT)).replace("\\", "/"),
            "seed": FINAL_SEED,
            "n_explained": int(shap_values.shape[0]),
            "features": list(PRIMARY_PREDICTORS),
            "output_space": "ebm_decision_function_logit_link",
        },
    )

    cases_idx = select_local_cases(p_raw, shap_values, terms, sample["row_ref"].to_numpy())
    y_desc = sample["Default"].to_numpy()
    cases = {}
    for key in ("high_risk", "low_risk", "median_risk", "disagreement"):
        cases[key] = local_payload(cases_idx[key], sample, p_raw, p_cal, shap_values, terms, y_desc)
        cases[key]["experiment_id"] = EXPERIMENT_ID
    dump_json(OUT / "metrics" / "local_cases.json", {"indices": cases_idx, "cases": cases})
    pd.DataFrame(
        [
            {
                "case": key,
                "row_ref": cases[key]["row_ref"],
                "p_raw": cases[key]["p_raw"],
                "p_calibrated": cases[key]["p_calibrated"],
                "top_positive": "; ".join(cases[key]["top_positive_shap"]),
                "top_negative": "; ".join(cases[key]["top_negative_shap"]),
                "local_rank_spearman": cases[key]["local_rank_spearman"],
                "y_true_descriptive_only": cases[key]["y_true_descriptive_only"],
                "experiment_id": EXPERIMENT_ID,
            }
            for key in cases
        ]
    ).to_csv(OUT / "tables" / "table4_local_cases.csv", index=False)

    a = float(platt.coef_)
    calibration_text = (
        f"Platt is `sigmoid(a * logit(p_raw) + b)` with a={a:.6f}, b={float(platt.intercept_):.6f}. "
        "Because a>0 this is a strictly increasing map of the EBM probability and an affine map of the EBM logit "
        f"(logit(p_cal) = a * decision + b). Additive SHAP on logit(p_cal) equals a times SHAP on the raw decision, "
        "so feature rankings are identical. Platt was applied to probabilities only; EBM intercept "
        f"{intercept_before:.6f} and term_importances were unchanged. Calibration changed probability values; "
        "it did not change the EBM's internal additive attribution structure."
    )

    top_features = list(table1.sort_values("shap_rank")["feature"].head(5))
    effects = []
    for i, name in enumerate(top_features, start=1):
        shape = shape_function(model42, name)
        effects.append(
            {
                "feature": name,
                "type": feature_type(name),
                "pattern": describe_shape(shape),
                "scale": "EBM additive term on logit/link scale",
                "experiment_id": EXPERIMENT_ID,
            }
        )
        plot_effect(shape, FIG / f"figure{6 + i}_effect_{name}")
    pd.DataFrame(effects).to_csv(OUT / "tables" / "table5_top_feature_effects.csv", index=False)

    plot_global_importance(
        shap_stats,
        "mean_abs",
        "Global additive SHAP importance (mean |value|, logit scale)",
        FIG / "figure1_global_shap_importance",
        "mean |SHAP|",
    )
    plot_beeswarm(shap_values, sample_x, FIG / "figure2_shap_beeswarm")
    plot_local_bars(
        cases["high_risk"],
        "High raw-probability case (SHAP, logit scale)",
        FIG / "figure3_local_high_risk",
        "shap",
        "SHAP value (logit / link)",
    )
    plot_local_bars(
        cases["low_risk"],
        "Low raw-probability case (SHAP, logit scale)",
        FIG / "figure4_local_low_risk",
        "shap",
        "SHAP value (logit / link)",
    )
    plot_local_bars(
        cases["median_risk"],
        "Median raw-probability case (SHAP, logit scale)",
        FIG / "figure5_local_median_risk",
        "shap",
        "SHAP value (logit / link)",
    )
    plot_local_shap_vs_ebm(
        cases["disagreement"],
        "Local SHAP vs uncentered EBM terms (deterministic lowest rank-correlation case)",
        FIG / "figure6_shap_vs_ebm_disagreement",
    )

    print("Seed-stability EBMs", flush=True)
    importances = {}
    for seed in SEEDS:
        model = get_or_train_ebm(seed, x_train, y_train)
        means = background_term_means(model, bg)
        phi = additive_shap(eval_terms(model, sample_x), means)
        importances[seed] = np.mean(np.abs(phi), axis=0)
        print(f"  seed {seed} top feature {PRIMARY_PREDICTORS[int(np.argmax(importances[seed]))]}", flush=True)
        del model
        gc.collect()
    ranks = rank_matrix(importances).assign(experiment_id=EXPERIMENT_ID)
    stab = feature_stability(ranks, len(SEEDS))
    pair = pairwise_spearman(importances)
    ranks.to_csv(OUT / "tables" / "seed_ranks.csv", index=False)
    stab.assign(experiment_id=EXPERIMENT_ID).to_csv(OUT / "tables" / "table3_seed_stability.csv", index=False)
    pair.assign(experiment_id=EXPERIMENT_ID).to_csv(OUT / "tables" / "seed_pairwise.csv", index=False)
    plot_seed_rank_heatmap(ranks, FIG / "figure12_seed_rank_stability")

    cal_shap = a * shap_values
    cal_imp = np.mean(np.abs(cal_shap), axis=0)
    dump_json(
        OUT / "metrics" / "calibration_attribution.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "platt_a": a,
            "platt_b": float(platt.intercept_),
            "logit_calibrated_shap": "a * raw_logit_shap because logit(p_cal)=a*decision+b",
            "rank_spearman_raw_vs_scaled": spearman_ranks(shap_imp, cal_imp),
            "top3_overlap_raw_vs_scaled": overlap_at_k(shap_imp, cal_imp, 3),
            "top5_overlap_raw_vs_scaled": overlap_at_k(shap_imp, cal_imp, 5),
            "ebm_parameters_unchanged_by_calibration": True,
        },
    )

    consistency = run_consistency_checks(
        feature_names=list(PRIMARY_PREDICTORS),
        shap_values=shap_values,
        ebm_terms=terms,
        base_value=float(explained["base_value"]),
        decision=decision,
        background_means=explained["background_means"],
        test_n=len(splits["test"]),
        sample_n=SAMPLE_N,
        sample_seed=SAMPLE_SEED,
        source_iloc=sample["source_iloc"].to_numpy(),
        seed_feature_names=list(PRIMARY_PREDICTORS),
    )
    dump_json(OUT / "metrics" / "consistency_checks.json", {**consistency, "experiment_id": EXPERIMENT_ID})
    if not consistency["passed"]:
        raise RuntimeError(f"Explanation consistency checks failed: {consistency}")

    figure_stems = [
        "figure1_global_shap_importance",
        "figure2_shap_beeswarm",
        "figure3_local_high_risk",
        "figure4_local_low_risk",
        "figure5_local_median_risk",
        "figure6_shap_vs_ebm_disagreement",
        *[f"figure{6 + i}_effect_{name}" for i, name in enumerate(top_features, start=1)],
        "figure12_seed_rank_stability",
    ]
    dump_json(
        FIG / "figure_manifest.json",
        {
            "experiment_id": EXPERIMENT_ID,
            "stems": figure_stems,
            "formats": ["png", "pdf"],
        },
    )

    import interpret
    import matplotlib
    import shap
    import sklearn

    versions = {
        "python": sys.version.replace("\n", " "),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "interpret": interpret.__version__,
        "shap": shap.__version__,
        "matplotlib": matplotlib.__version__,
        "joblib": joblib.__version__,
    }
    shap_cfg = shap_config(SAMPLE_N)
    background_mean_max_abs = float(np.max(np.abs(explained["background_means"])))
    audit_body = {
        "explainability_experiment_id": EXPERIMENT_ID,
        "base_model_experiment_id": STAGE4B_ID,
        "calibration_experiment_id": STAGE5_ID,
        "selected_family": FAMILY,
        "selected_calibration": "platt",
        "dataset_hash": dataset_hash,
        "split_manifest_hash": sha256_text_file(SPLIT_MANIFEST),
        "feature_policy_hash": sha256_text_file(FEATURE_POLICY_PATH),
        "preprocessing_policy_hash": sha256_text_file(PREPROCESS_POLICY_PATH),
        "ebm_config": ebm_config(FINAL_SEED),
        "shap": shap_cfg,
        "sample_n": SAMPLE_N,
        "sample_seed": SAMPLE_SEED,
        "sampling_used_labels": False,
        "model_seeds": SEEDS,
        "model_ids": [f"ebm_train_only_seed{s}" for s in SEEDS],
        "platt_a": a,
        "platt_b": float(platt.intercept_),
        "ebm_parameters_unchanged_by_calibration": True,
        "background_mean_max_abs": background_mean_max_abs,
        "software_library_versions": versions,
        "execution_timestamp": utc_now(),
        "git_commit": git_commit(ROOT),
        "status": "PENDING_TESTS",
        "status_reason": "Artifacts written; test suite not yet executed.",
        "pytest_exit_code": None,
        "additive_reconstruction_max_abs_error": add_err,
        "disagreement_spearman": cases_idx["disagreement_spearman"],
        "consistency_passed": True,
    }
    dump_json(AUDIT / "stage6_explainability_run.json", audit_body)

    print("Running pytest", flush=True)
    pytest_code, pytest_text = run_pytest()
    status = "PASS" if pytest_code == 0 else "BLOCKED"
    status_reason = (
        "Explainability experiments completed with a valid additive SHAP method for EBM; tests passed."
        if status == "PASS"
        else f"pytest_exit={pytest_code}"
    )
    audit_body["status"] = status
    audit_body["status_reason"] = status_reason
    audit_body["pytest_exit_code"] = pytest_code
    dump_json(AUDIT / "stage6_explainability_run.json", audit_body)
    payload = {
        "status": status,
        "status_reason": status_reason,
        "table1": table1,
        "overlap3": overlap3,
        "overlap5": overlap5,
        "overlap9": overlap9,
        "spearman": spearman,
        "kendall": kendall,
        "footrule": footrule,
        "sign_vs_centered": sign_c,
        "sign_vs_raw_terms": sign_u,
        "cases": cases,
        "disagreement_spearman": cases_idx["disagreement_spearman"],
        "stability": stab,
        "pairwise_spearman_mean": float(pair["spearman"].mean()) if len(pair) else float("nan"),
        "pairwise_top3_mean": float(pair["top3_overlap"].mean()) if len(pair) else float("nan"),
        "pairwise_top5_mean": float(pair["top5_overlap"].mean()) if len(pair) else float("nan"),
        "calibration_text": calibration_text,
        "effects": effects,
        "shap_config": shap_cfg,
        "dataset_hash": dataset_hash,
        "split_hash": sha256_text_file(SPLIT_MANIFEST),
        "prep_hash": sha256_text_file(PREPROCESS_POLICY_PATH),
        "git_commit": git_commit(ROOT),
        "versions": versions,
        "background_mean_max_abs": background_mean_max_abs,
        "test_suite_summary": pytest_text[-4000:] if pytest_text else f"pytest exit {pytest_code}",
    }
    write_report(payload)
    print(json.dumps({"status": status, "add_err": add_err, "spearman": spearman}, indent=2), flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
