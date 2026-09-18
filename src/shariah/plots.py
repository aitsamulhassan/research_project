"""Architecture figures for Stage 7. Not certification diagrams."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def _box(ax, xy, text, color):
    x, y = xy
    patch = FancyBboxPatch((x, y), 0.28, 0.12, boxstyle="round,pad=0.01,rounding_size=0.02", facecolor=color, edgecolor="#222")
    ax.add_patch(patch)
    ax.text(x + 0.14, y + 0.06, text, ha="center", va="center", fontsize=8, wrap=True)


def _save(fig, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def figure_governance_flow(path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Shariah-oriented governance flow (research prototype, not certification)")
    boxes = [
        (0.02, 0.55, "Input financing\ninformation", "#d9edf7"),
        (0.32, 0.55, "Contract\nidentification", "#d9edf7"),
        (0.62, 0.72, "Layer A\nevidence completeness", "#fcf8e3"),
        (0.62, 0.38, "Layer B\nverified-rule evaluation", "#fcf8e3"),
        (0.02, 0.15, "Provenance\n(source/clause/version)", "#dff0d8"),
        (0.32, 0.15, "Governance status\nPASS/REVIEW/\nNOT_STRUCTURABLE/\nINSUFFICIENT_INFORMATION", "#dff0d8"),
        (0.68, 0.15, "Human/Shariah review\nwhen required", "#f2dede"),
    ]
    for x, y, text, color in boxes:
        _box(ax, (x, y), text, color)
    ax.annotate("", xy=(0.32, 0.61), xytext=(0.30, 0.61), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.62, 0.78), xytext=(0.60, 0.66), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.62, 0.44), xytext=(0.60, 0.58), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.46, 0.27), xytext=(0.46, 0.55), arrowprops=dict(arrowstyle="->"))
    fig.tight_layout()
    _save(fig, path_stem)


def figure_evidence_separation(path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Evidence-separation architecture (layers are not statistically fused in Stage 7)")
    _box(ax, (0.05, 0.62), "Credit-risk\nevidence", "#cce5ff")
    _box(ax, (0.36, 0.62), "Calibration\nevidence", "#cce5ff")
    _box(ax, (0.67, 0.62), "Explainability\nevidence", "#cce5ff")
    _box(ax, (0.36, 0.38), "Shariah-oriented\ngovernance evidence", "#ffe8cc")
    _box(ax, (0.36, 0.10), "Final decision policy\n(not implemented in Stage 7)", "#e2d5f1")
    ax.text(0.5, 0.30, "independent until a later decision stage", ha="center", fontsize=8)
    fig.tight_layout()
    _save(fig, path_stem)


def figure_l1_l2(path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Stage 7 v2 L1 dataset readiness and L2 per-application evaluation")
    _box(ax, (0.05, 0.62), "L1 dataset/\nintegration readiness", "#d9edf7")
    _box(ax, (0.36, 0.62), "Row-specific\nevidence extractor", "#fcf8e3")
    _box(ax, (0.67, 0.62), "L2 engine evaluate\nPER_APPLICATION", "#dff0d8")
    _box(ax, (0.05, 0.18), "LendingClub L1:\nINSUFFICIENT_SCHEMA_\nFOR_APPLICANT_\nDETERMINATION", "#f2dede")
    _box(ax, (0.36, 0.18), "Firewall drops\npurpose/title/desc\nand credit fields", "#ffe8cc")
    _box(ax, (0.67, 0.18), "Per-row hashes +\nmissing evidence;\nnot a ruling", "#e2d5f1")
    fig.tight_layout()
    _save(fig, path_stem)
