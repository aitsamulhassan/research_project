"""
Build publication figures from frozen stored artifacts only.
Presentation polish only: no model loading, metric recalculation, or TEST rescoring.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

COL_W = 3.5
FULL_W = 7.16

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "axes.linewidth": 0.6,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
    }
)


def _box(ax, xy, w, h, text, fc="#e8eef5", ec="#1a1a1a", fontsize=8, weight="normal"):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        linewidth=0.8,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        wrap=True,
    )
    return patch


def _arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=10,
            lw=0.9,
            color="#222222",
            shrinkA=1,
            shrinkB=1,
        )
    )


def fig1_architecture() -> None:
    """Evidence-separated research prototype (vertical flow; no fraud/deployment claims)."""
    fig, ax = plt.subplots(figsize=(FULL_W, 4.35))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.2)
    ax.axis("off")

    ax.text(
        5.0,
        10.05,
        "Evidence-separated research prototype (not a production or certification system)",
        ha="center",
        va="top",
        fontsize=8.5,
        style="italic",
        color="#333333",
    )

    # Main scoring column (center-left)
    _box(ax, (3.15, 8.55), 3.7, 0.95, "LendingClub inputs\n(frozen predictors)", fc="#f5f5f5", fontsize=8)
    _box(ax, (3.15, 7.25), 3.7, 0.95, "M-5 TRAIN-only EBM", fc="#d9e6f5", fontsize=8.5, weight="bold")
    _box(ax, (3.15, 5.95), 3.7, 0.95, "Validation-only Platt calibration", fc="#d9e6f5", fontsize=8)
    _box(ax, (3.15, 4.65), 3.7, 0.95, r"Frozen $p_{\mathrm{selected}}$", fc="#d9e6f5", fontsize=8.5)
    _box(
        ax,
        (3.15, 3.35),
        3.7,
        0.95,
        "Credit bands  " + r"$t_{\mathrm{low}},\,t_{\mathrm{high}}$",
        fc="#fff2cc",
        fontsize=8,
    )
    _box(ax, (3.15, 1.85), 3.7, 1.05, "G0 decision fusion map\n(credit band × L2 status)", fc="#ffe0c2", fontsize=8, weight="bold")

    for y0, y1 in [(8.55, 8.2), (7.25, 6.9), (5.95, 5.6), (4.65, 4.3), (3.35, 2.9)]:
        _arrow(ax, (5.0, y0), (5.0, y1))

    # Outcomes
    _box(ax, (1.0, 0.35), 2.0, 0.7, "APPROVE", fc="#d9ead3", fontsize=8)
    _box(ax, (4.0, 0.35), 2.0, 0.7, "HUMAN_REVIEW", fc="#fff2cc", fontsize=7.5)
    _box(ax, (7.0, 0.35), 2.0, 0.7, "REJECT", fc="#f4cccc", fontsize=8)
    _arrow(ax, (4.0, 1.85), (2.0, 1.05))
    _arrow(ax, (5.0, 1.85), (5.0, 1.05))
    _arrow(ax, (6.0, 1.85), (8.0, 1.05))

    # Explanation side path (right)
    _box(
        ax,
        (7.35, 6.85),
        2.4,
        1.35,
        "Additive explanations\n(logit scale)\nnot an approval criterion\nTreeSHAP not used",
        fc="#e8f0e8",
        fontsize=7,
    )
    _arrow(ax, (6.85, 7.7), (7.35, 7.5))

    # Shariah side path (left)
    _box(
        ax,
        (0.25, 3.55),
        2.55,
        1.55,
        "Shariah-oriented\nL1/L2 evidence\n→ L2 status\n(governance support;\nnot certification)",
        fc="#f3e8f0",
        fontsize=7,
    )
    _arrow(ax, (2.8, 4.2), (3.15, 4.1))
    _arrow(ax, (1.5, 3.55), (3.15, 2.4))

    fig.savefig(OUT / "fig1_architecture.pdf")
    fig.savefig(OUT / "fig1_architecture.png")
    plt.close(fig)


def fig2_model_roc_auc() -> None:
    stage4b = json.loads((ROOT / "results/metrics/stage4b_test_metrics.json").read_text(encoding="utf-8"))
    stage5 = json.loads(
        (ROOT / "results/calibration/metrics/stage5_test_metrics.json").read_text(encoding="utf-8")
    )
    m4b = {}
    for row in stage4b:
        if row.get("seed") == 42 and row.get("split") == "test":
            m4b[row["family"]] = row["roc_auc"]
    m5_platt = next(r["roc_auc"] for r in stage5 if r["method"] == "platt")
    assert abs(m4b["explainable_boosting_machine"] - 0.6799408767429772) < 1e-15
    assert abs(m5_platt - 0.6776693941139847) < 1e-15

    labels = [
        "logistic\nregression",
        "random\nforest",
        "XGBoost\n(LC only)",
        "EBM\n(M-4B)",
        "EBM raw/Platt\n(M-5)",
    ]
    values = [
        m4b["logistic_regression"],
        m4b["random_forest"],
        m4b["xgboost"],
        m4b["explainable_boosting_machine"],
        m5_platt,
    ]
    contexts = ["M-4B"] * 4 + ["M-5"]
    colors = ["#5b7c99", "#5b7c99", "#5b7c99", "#2f4b7c", "#a65d3f"]

    fig, ax = plt.subplots(figsize=(FULL_W * 0.98, 2.85))
    x = range(len(labels))
    bars = ax.bar(x, values, color=colors, edgecolor="black", linewidth=0.45, width=0.7)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("TEST ROC-AUC")
    ax.set_ylim(0.645, 0.705)
    ax.yaxis.grid(True, linestyle=":", linewidth=0.4, color="#bbbbbb")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar, v, ctx in zip(bars, values, contexts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.0015,
            f"{v:.4f}\n({ctx})",
            ha="center",
            va="bottom",
            fontsize=7,
        )
    fig.savefig(OUT / "fig2_model_test_roc_auc.pdf")
    fig.savefig(OUT / "fig2_model_test_roc_auc.png")
    plt.close(fig)


def fig3_decision_policy() -> None:
    pol = json.loads((ROOT / "results/decision/v2/frozen_policy.json").read_text(encoding="utf-8"))
    t_low = float(pol["t_low"])
    t_high = float(pol["t_high"])
    t_star = float(pol["monolithic_t"])
    assert t_low == 0.06 and t_high == 0.69 and t_star == 0.16

    fig, axes = plt.subplots(2, 1, figsize=(FULL_W * 0.98, 2.75), sharex=True)
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.add_patch(Rectangle((0, 0.28), t_low, 0.44, facecolor="#d9ead3", edgecolor="black", lw=0.55))
    ax.add_patch(Rectangle((t_low, 0.28), t_high - t_low, 0.44, facecolor="#fff2cc", edgecolor="black", lw=0.55))
    ax.add_patch(Rectangle((t_high, 0.28), 1 - t_high, 0.44, facecolor="#f4cccc", edgecolor="black", lw=0.55))
    ax.text(t_low / 2, 0.5, "APPROVE\n(LOW)", ha="center", va="center", fontsize=8)
    ax.text((t_low + t_high) / 2, 0.5, "HUMAN_REVIEW\n(MEDIUM)", ha="center", va="center", fontsize=8)
    ax.text((t_high + 1) / 2, 0.5, "REJECT\n(HIGH)", ha="center", va="center", fontsize=8)
    for t, lab in [(t_low, r"$t_{\mathrm{low}}=0.06$"), (t_high, r"$t_{\mathrm{high}}=0.69$")]:
        ax.axvline(t, color="black", lw=0.85)
        ax.text(t, 0.86, lab, ha="center", va="bottom", fontsize=8)
    ax.set_yticks([])
    ax.set_title(r"(a) Credit-only bands (A0) on frozen $p_{\mathrm{selected}}$", loc="left", fontsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)

    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.add_patch(Rectangle((0, 0.28), t_star, 0.44, facecolor="#d9ead3", edgecolor="black", lw=0.55))
    ax.add_patch(Rectangle((t_star, 0.28), 1 - t_star, 0.44, facecolor="#f4cccc", edgecolor="black", lw=0.55))
    ax.text(t_star / 2, 0.5, "APPROVE", ha="center", va="center", fontsize=8)
    ax.text((t_star + 1) / 2, 0.5, "REJECT", ha="center", va="center", fontsize=8)
    ax.axvline(t_star, color="black", lw=0.85)
    ax.text(t_star, 0.86, r"$t^{*}=0.16$", ha="center", va="bottom", fontsize=8)
    ax.set_xlabel(r"Frozen calibrated probability $p_{\mathrm{selected}}$")
    ax.set_yticks([])
    ax.set_title("(b) Monolithic single threshold (A3/A4); no HUMAN_REVIEW band", loc="left", fontsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)

    fig.tight_layout(rect=[0, 0.0, 1, 1])
    fig.savefig(OUT / "fig3_decision_policy_thresholds.pdf")
    fig.savefig(OUT / "fig3_decision_policy_thresholds.png")
    plt.close(fig)


def fig4_global_attribution() -> None:
    df = pd.read_csv(ROOT / "results/explainability/tables/table1_global_attribution.csv")
    df = df.sort_values("shap_rank")
    assert abs(df.loc[df["feature"] == "fico_n", "shap_mean_abs"].iloc[0] - 0.3072104502059198) < 1e-15

    fig, ax = plt.subplots(figsize=(COL_W + 0.55, 3.25))
    y = range(len(df) - 1, -1, -1)
    ax.barh(list(y), df["shap_mean_abs"].to_numpy(), color="#2f4b7c", edgecolor="black", linewidth=0.4, height=0.72)
    ax.set_yticks(list(y))
    ax.set_yticklabels([rf"\texttt{{{f}}}" if False else f for f in df["feature"]])
    ax.set_xlabel(r"Mean $|\phi_i|$ (logit scale; $n=5000$ TEST sample)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.grid(True, linestyle=":", linewidth=0.4, color="#bbbbbb")
    ax.set_axisbelow(True)
    for yi, v in zip(y, df["shap_mean_abs"]):
        ax.text(v + 0.004, yi, f"{v:.3f}", va="center", fontsize=7)
    ax.set_xlim(0, 0.37)
    fig.savefig(OUT / "fig4_global_attribution.pdf")
    fig.savefig(OUT / "fig4_global_attribution.png")
    plt.close(fig)


def fig5_calibration_risk_ranges() -> None:
    df = pd.read_csv(ROOT / "results/calibration/tables/stage5_risk_ranges.csv")
    raw = df[df["method"] == "raw"]
    platt = df[df["method"] == "platt"]

    fig, ax = plt.subplots(figsize=(COL_W + 0.35, 3.05))
    ax.plot([0, 0.6], [0, 0.6], color="#888888", lw=0.85, ls="--", label="Ideal")
    ax.scatter(
        raw["mean_predicted"],
        raw["observed_rate"],
        s=42,
        c="#5b7c99",
        edgecolors="black",
        linewidths=0.4,
        zorder=3,
        label="raw",
    )
    ax.scatter(
        platt["mean_predicted"],
        platt["observed_rate"],
        s=42,
        c="#a65d3f",
        marker="s",
        edgecolors="black",
        linewidths=0.4,
        zorder=3,
        label="Platt (selected)",
    )
    for _, row in platt.iterrows():
        ax.annotate(
            row["range_label"],
            (row["mean_predicted"], row["observed_rate"]),
            textcoords="offset points",
            xytext=(5, 4),
            fontsize=6.5,
        )
    ax.set_xlabel("Mean predicted probability (stored risk range)")
    ax.set_ylabel("Observed default rate")
    ax.set_xlim(0, 0.60)
    ax.set_ylim(0, 0.60)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(frameon=False, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.savefig(OUT / "fig5_calibration_risk_ranges.pdf")
    fig.savefig(OUT / "fig5_calibration_risk_ranges.png")
    plt.close(fig)


if __name__ == "__main__":
    fig1_architecture()
    fig2_model_roc_auc()
    fig3_decision_policy()
    fig4_global_attribution()
    fig5_calibration_risk_ranges()
    print("Wrote figures to", OUT)
