import matplotlib.pyplot as plt
import numpy as np
from typing import Dict
from datastructs import AttentionProfile

# ===========================================================================
# VISUALIZATION
# ===========================================================================

def plot_summary_bars(
    profiles: Dict[str, AttentionProfile],
    title: str,
    filename: str,
):
    """Bar chart: mean attention to each paragraph, per condition."""
    fig, ax = plt.subplots(figsize=(10, 6))

    conditions = list(profiles.keys())
    para_nums = sorted({p for prof in profiles.values() for p in prof.to_para.keys()})
    colors = ['#2ecc71', '#3498db', '#e74c3c']

    x = np.arange(len(conditions))
    width = 0.25

    for i, (para_num, color) in enumerate(zip(para_nums, colors)):
        means = [profiles[c].mean_to(para_num) for c in conditions]
        ax.bar(x + i * width, means, width, label=f'Paragraph {para_num}', color=color)

    ax.set_ylabel('Mean Attention (query → paragraph)')
    ax.set_title(title)
    ax.set_xticks(x + width)
    ax.set_xticklabels(conditions, rotation=15)
    ax.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"  Saved {filename}")


def plot_layer_heatmaps(
    profiles: Dict[str, AttentionProfile],
    target_para: int,
    title_suffix: str,
    filename: str,
):
    """Per-layer, per-head heatmaps of attention to a specific paragraph."""
    conditions = list(profiles.keys())
    n = len(conditions)

    fig, axes = plt.subplots(1, n, figsize=(6 * n, 6), sharey=True)
    if n == 1:
        axes = [axes]

    for ax, cond in zip(axes, conditions):
        data = profiles[cond].to_para[target_para]
        im = ax.imshow(data, aspect='auto', cmap='hot', interpolation='nearest')
        ax.set_title(f'{cond}\n→ Paragraph {target_para}')
        ax.set_xlabel('Head')
        ax.set_ylabel('Layer')
        plt.colorbar(im, ax=ax, shrink=0.8)

    fig.suptitle(f'Attention to Paragraph {target_para} — {title_suffix}', fontsize=14)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"  Saved {filename}")


def plot_layer_curves(
    profiles: Dict[str, AttentionProfile],
    target_para: int,
    title: str,
    filename: str,
):
    """Line plot: mean attention to target paragraph at each layer, per condition."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for label, profile in profiles.items():
        layer_means = profile.per_layer_to(target_para)
        ax.plot(layer_means, label=label, linewidth=2)

    ax.set_xlabel('Layer')
    ax.set_ylabel('Mean Attention → Paragraph ' + str(target_para))
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"  Saved {filename}")


def plot_narrowed_bars(
    profiles: Dict[str, AttentionProfile],
    target_para: int,
    layer_start: int,
    layer_end: int,
    title: str,
    filename: str,
):
    """
    Bar chart of attention to a specific paragraph, averaged over only
    a narrow range of layers [layer_start, layer_end] inclusive.
    This avoids drowning the signal in null layers.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    conditions = list(profiles.keys())
    colors = ['#3498db', '#e67e22', '#2ecc71']

    means = []
    for cond in conditions:
        data = profiles[cond].to_para[target_para]
        # data shape: [n_layers, n_heads] — slice to our layer range
        layer_slice = data[layer_start:layer_end + 1, :]
        means.append(layer_slice.mean())

    x = np.arange(len(conditions))
    bars = ax.bar(x, means, color=colors[:len(conditions)], width=0.5)

    # Add value labels on bars
    for bar, val in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                f'{val:.4f}', ha='center', va='bottom', fontsize=10)

    ax.set_ylabel(f'Mean Attention → Paragraph {target_para}')
    ax.set_title(f'{title}\n(Layers {layer_start}–{layer_end} only)')
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, rotation=15)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"  Saved {filename}")


def plot_single_layer_heads(
    profiles: Dict[str, AttentionProfile],
    target_para: int,
    layer: int,
    title: str,
    filename: str,
):
    """
    Bar chart showing attention to target_para at a SINGLE layer,
    broken out by individual head. One group of bars per head,
    one bar per condition.
    """
    conditions = list(profiles.keys())
    n_heads = profiles[conditions[0]].to_para[target_para].shape[1]
    colors = ['#3498db', '#e67e22', '#2ecc71']

    fig, ax = plt.subplots(figsize=(14, 6))

    x = np.arange(n_heads)
    width = 0.25
    offsets = np.arange(len(conditions)) * width - width * (len(conditions) - 1) / 2

    for i, cond in enumerate(conditions):
        head_vals = profiles[cond].to_para[target_para][layer, :]
        ax.bar(x + offsets[i], head_vals, width, label=cond, color=colors[i])

    ax.set_xlabel('Head')
    ax.set_ylabel(f'Attention → Paragraph {target_para}')
    ax.set_title(f'{title}\nLayer {layer}, per head')
    ax.set_xticks(x)
    ax.set_xticklabels([str(h) for h in range(n_heads)])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"  Saved {filename}")


def plot_single_layer_heads_difference(
    profiles: Dict[str, AttentionProfile],
    target_para: int,
    layer: int,
    baseline_key: str,
    title: str,
    filename: str,
):
    """
    Difference plot: for each head, show (condition - baseline) attention.
    Makes it easy to see which heads are most affected by retrieval tokens.
    """
    conditions = [k for k in profiles.keys() if k != baseline_key]
    n_heads = profiles[baseline_key].to_para[target_para].shape[1]
    colors = ['#e67e22', '#2ecc71', '#e74c3c']

    fig, ax = plt.subplots(figsize=(14, 6))

    baseline_vals = profiles[baseline_key].to_para[target_para][layer, :]

    x = np.arange(n_heads)
    width = 0.35
    offsets = np.arange(len(conditions)) * width - width * (len(conditions) - 1) / 2

    for i, cond in enumerate(conditions):
        head_vals = profiles[cond].to_para[target_para][layer, :]
        diff = head_vals - baseline_vals
        ax.bar(x + offsets[i], diff, width, label=f'{cond} − {baseline_key}', color=colors[i])

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_xlabel('Head')
    ax.set_ylabel(f'Δ Attention → Paragraph {target_para}')
    ax.set_title(f'{title}\nLayer {layer}, difference from {baseline_key}')
    ax.set_xticks(x)
    ax.set_xticklabels([str(h) for h in range(n_heads)])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"  Saved {filename}")


def print_summary(profiles: Dict[str, AttentionProfile]):
    """Print a clean text summary."""
    para_nums = sorted({p for prof in profiles.values() for p in prof.to_para.keys()})

    print("\n" + "=" * 70)
    header = f"{'Condition':<25}"
    for p in para_nums:
        header += f" {'→ P' + str(p):>10}"
    print(header)
    print("-" * 70)

    for label, profile in profiles.items():
        row = f"{label:<25}"
        for p in para_nums:
            row += f" {profile.mean_to(p):>10.6f}"
        print(row)

    print("-" * 70)


