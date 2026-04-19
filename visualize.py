import json
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# ── find most recent batch and variance files ──────────────────────────────
def find_latest(pattern):
    files = glob.glob(pattern)
    return max(files, key=os.path.getmtime) if files else None

batch_file = find_latest("batch_*.json")
variance_file = find_latest("variance_*.json")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
COLORS = {"llama3.1:8b": "#a78bfa", "mistral": "#34d399"}
CATEGORIES = ["neutral", "distress", "identity_challenge", "aggressive"]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#0d0d0d")
for ax in axes:
    ax.set_facecolor("#1a1a1a")
    ax.tick_params(colors="#aaaaaa")
    ax.xaxis.label.set_color("#aaaaaa")
    ax.yaxis.label.set_color("#aaaaaa")
    ax.title.set_color("#ffffff")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")

# ── chart 1: batch ratings by category ────────────────────────────────────
ax1 = axes[0]
ax1.set_title("avg emotional rating by category", pad=12)

if batch_file:
    with open(batch_file, encoding="utf-8") as f:
        batch_data = json.load(f)

    models = list(COLORS.keys())
    x = np.arange(len(CATEGORIES))
    width = 0.35

    for i, model in enumerate(models):
        avgs = []
        for cat in CATEGORIES:
            cat_results = [r for r in batch_data if r.get("model") == model and r.get("category") == cat and r.get("rating") is not None]
            ratings = [r["rating"] for r in cat_results]
            avgs.append(np.mean(ratings) if ratings else 0)

        bars = ax1.bar(x + i * width - width/2, avgs, width, color=COLORS[model], alpha=0.85, label=model)
        for bar, val in zip(bars, avgs):
            if val:
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        f"{val:.1f}", ha="center", va="bottom", color="#ffffff", fontsize=9)

    ax1.set_xticks(x)
    ax1.set_xticklabels(CATEGORIES, rotation=15, ha="right", fontsize=9)
    ax1.set_ylim(0, 11)
    ax1.set_ylabel("rating (1-10)")
    ax1.legend(facecolor="#1a1a1a", labelcolor="#ffffff", edgecolor="#333333")
    ax1.axhline(y=5, color="#444444", linestyle="--", linewidth=0.8, alpha=0.7)
    ax1.text(3.6, 5.15, "midpoint", color="#666666", fontsize=8)
else:
    ax1.text(0.5, 0.5, "no batch data found\nrun batch_probe.py first",
             ha="center", va="center", color="#666666", transform=ax1.transAxes)

# ── chart 2: variance across 10 runs ──────────────────────────────────────
ax2 = axes[1]
ax2.set_title("rating variance across 10 runs (same prompt)", pad=12)

if variance_file:
    with open(variance_file, encoding="utf-8") as f:
        var_data = json.load(f)

    for entry in var_data:
        model = entry["model"]
        category = entry["category"]
        ratings = [r for r in entry["ratings"] if r is not None]
        if not ratings:
            continue

        label = f"{model}\n{category}"
        y = ratings
        x_jitter = [var_data.index(entry)] * len(y)
        x_jitter = [v + np.random.uniform(-0.1, 0.1) for v in x_jitter]

        ax2.scatter(x_jitter, y, color=COLORS.get(model, "#ffffff"), alpha=0.7, s=40, zorder=3)
        ax2.plot([var_data.index(entry)] * 2,
                [min(ratings), max(ratings)],
                color=COLORS.get(model, "#ffffff"), alpha=0.4, linewidth=1.5)
        avg = entry.get("avg")
        if avg:
            ax2.scatter([var_data.index(entry)], [avg],
                       color=COLORS.get(model, "#ffffff"), s=100, marker="_",
                       linewidths=2, zorder=4)

    labels = [f"{e['model'].split(':')[0]}\n{e['category']}" for e in var_data]
    ax2.set_xticks(range(len(var_data)))
    ax2.set_xticklabels(labels, fontsize=7, rotation=20, ha="right")
    ax2.set_ylim(0, 11)
    ax2.set_ylabel("rating (1-10)")
    ax2.axhline(y=5, color="#444444", linestyle="--", linewidth=0.8, alpha=0.7)

    patches = [mpatches.Patch(color=c, label=m) for m, c in COLORS.items()]
    ax2.legend(handles=patches, facecolor="#1a1a1a", labelcolor="#ffffff", edgecolor="#333333")
else:
    ax2.text(0.5, 0.5, "no variance data found\nrun variance_probe.py first",
             ha="center", va="center", color="#666666", transform=ax2.transAxes)

plt.suptitle("llm-therapymaxxing — emotional probe results", color="#ffffff", fontsize=13)
plt.tight_layout(rect=[0, 0, 1, 0.95])

out_path = f"results_chart_{timestamp}.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"saved to {out_path}")
plt.show()
