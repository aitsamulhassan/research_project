"""Explainability figures. Attribution, not causal effects."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from evaluation.plots import _save
from explainability.ebm_attribution import feature_type
from preprocessing.lendingclub_preprocessor import NUMERIC_FEATURES, PRIMARY_PREDICTORS

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
    }
)


def plot_global_importance(stats: pd.DataFrame, value_col: str, title: str, path_stem: Path, xlabel: str) -> None:
    frame = stats.sort_values(value_col, ascending=True)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.barh(frame["feature"], frame[value_col], color="#1f77b4")
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    fig.tight_layout()
    _save(fig, path_stem)


def plot_beeswarm(shap_values: np.ndarray, frame: pd.DataFrame, path_stem: Path) -> None:
    order = np.argsort(-np.mean(np.abs(shap_values), axis=0))
    rng = np.random.RandomState(42)
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    y_positions = np.arange(len(order))
    for yi, feat_i in enumerate(order):
        values = shap_values[:, feat_i]
        jitter = rng.uniform(-0.18, 0.18, size=len(values))
        name = PRIMARY_PREDICTORS[feat_i]
        if name in NUMERIC_FEATURES:
            color_src = pd.to_numeric(frame[name], errors="coerce").to_numpy()
            finite = np.isfinite(color_src)
            lo, hi = np.nanpercentile(color_src[finite], [5, 95]) if finite.any() else (0, 1)
            norm = np.clip((color_src - lo) / (hi - lo + 1e-12), 0, 1)
            ax.scatter(values, np.full(len(values), yi) + jitter, c=norm, cmap="coolwarm", s=6, alpha=0.5, linewidths=0)
        else:
            ax.scatter(values, np.full(len(values), yi) + jitter, c="#4d4d4d", s=6, alpha=0.35, linewidths=0)
    ax.axvline(0, color="0.5", linewidth=1)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([PRIMARY_PREDICTORS[i] for i in order])
    ax.set_xlabel("Additive SHAP value (logit / link scale)")
    ax.set_title("SHAP summary (color = feature value for continuous fields only)")
    fig.tight_layout()
    _save(fig, path_stem)


def plot_local_bars(payload: dict, title: str, path_stem: Path, value_key: str, xlabel: str) -> None:
    feats = sorted(payload["features"], key=lambda r: abs(r[value_key]))
    names = [r["feature"] for r in feats]
    vals = [r[value_key] for r in feats]
    colors = ["#d62728" if v > 0 else "#1f77b4" for v in vals]
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ax.barh(names, vals, color=colors)
    ax.axvline(0, color="0.4", linewidth=1)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    fig.tight_layout()
    _save(fig, path_stem)


def plot_local_shap_vs_ebm(payload: dict, title: str, path_stem: Path) -> None:
    feats = payload["features"]
    names = [r["feature"] for r in feats]
    y = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.barh(y + 0.18, [r["shap"] for r in feats], height=0.35, color="#1f77b4", label="SHAP (centered)")
    ax.barh(y - 0.18, [r["ebm_term"] for r in feats], height=0.35, color="#d62728", label="EBM term (uncentered)")
    ax.axvline(0, color="0.4", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlabel("Logit / link contribution")
    ax.set_title(title)
    ax.legend(frameon=False, loc="best")
    fig.tight_layout()
    _save(fig, path_stem)


def plot_continuous_effect(shape: dict, path_stem: Path) -> None:
    edges = np.asarray(shape["names"], dtype=float)
    scores = np.asarray(shape["scores"], dtype=float)
    if len(edges) == len(scores) + 1:
        x = 0.5 * (edges[:-1] + edges[1:])
    else:
        x = edges[: len(scores)]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(x, scores, color="#1f77b4", linewidth=2)
    ax.axhline(0, color="0.5", linewidth=1)
    ax.set_xlabel(shape["feature"])
    ax.set_ylabel("EBM term (logit / link)")
    ax.set_title(f"EBM shape function: {shape['feature']}")
    fig.tight_layout()
    _save(fig, path_stem)


def plot_categorical_effect(shape: dict, path_stem: Path, max_categories: int = 20) -> None:
    names = [str(n) for n in shape["names"]]
    scores = np.asarray(shape["scores"], dtype=float)
    order = np.argsort(-np.abs(scores))
    if len(order) > max_categories:
        order = order[:max_categories]
        title = f"EBM category contributions: {shape['feature']} ({max_categories} largest |term|; not a numeric scale)"
    else:
        title = f"EBM category contributions: {shape['feature']} (not a numeric scale)"
    names = [names[i] for i in order][::-1]
    scores = scores[order][::-1]
    colors = ["#d62728" if v > 0 else "#1f77b4" for v in scores]
    fig, ax = plt.subplots(figsize=(6.8, max(3.6, 0.28 * len(names) + 1.5)))
    ax.barh(names, scores, color=colors)
    ax.axvline(0, color="0.5", linewidth=1)
    ax.set_xlabel("EBM term (logit / link)")
    ax.set_title(title)
    fig.tight_layout()
    _save(fig, path_stem)


def plot_seed_rank_heatmap(rank_frame: pd.DataFrame, path_stem: Path) -> None:
    seeds = sorted(rank_frame["seed"].unique())
    mat = np.zeros((len(PRIMARY_PREDICTORS), len(seeds)))
    for j, seed in enumerate(seeds):
        sub = rank_frame.loc[rank_frame["seed"] == seed].set_index("feature")
        for i, name in enumerate(PRIMARY_PREDICTORS):
            mat[i, j] = sub.loc[name, "rank"]
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    im = ax.imshow(mat, cmap="viridis_r", vmin=1, vmax=9, aspect="auto")
    ax.set_xticks(range(len(seeds)))
    ax.set_xticklabels([str(s) for s in seeds])
    ax.set_yticks(range(len(PRIMARY_PREDICTORS)))
    ax.set_yticklabels(PRIMARY_PREDICTORS)
    ax.set_xlabel("EBM random seed")
    ax.set_title("SHAP importance rank by seed (1 = largest mean |SHAP|)")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Rank")
    fig.tight_layout()
    _save(fig, path_stem)


def plot_effect(shape: dict, path_stem: Path) -> None:
    if feature_type(shape["feature"]) == "continuous":
        plot_continuous_effect(shape, path_stem)
    else:
        plot_categorical_effect(shape, path_stem)
