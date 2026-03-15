"""
We'll be using matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
from Bio import Phylo

def plot_tree(tree, title="Phylogenetic Tree", type="rooted"):
    """This renders the Biopython tree object into a matplotlib figure."""
    fig, ax = plt.subplots(figsize=(10, 6))

    if type == "unrooted":
        Phylo.draw(tree, axes=ax, do_show=False, branch_labels=lambda c: round(c.branch_length, 3) if c.branch_length else "")
    else:
        Phylo.draw(tree, axes=ax, do_show=False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.set_title(title, fontsize=16, pad=20)
    ax.set_ylabel("")
    ax.set_xlabel("Genetic Distance")

    plt.tight_layout()
    return fig

def plot_distance_matrix(distance_matrix):
    """Renders a Biopython DistanceMatrix as heatmap."""
    names = distance_matrix.names
    n = len(names)

    full_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1):
            val = distance_matrix[i, j]
            full_matrix[i, j] = val
            full_matrix[j, i] = val # Symmetrical square

    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.imshow(full_matrix, cmap="YlGnBu", aspect='auto')
    cbar = fig.colorbar(cax)
    cbar.set_label('Genetic Distance', rotation=270, labelpad=15)

    # Labeling with sequence names
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_yticklabels(names)

    for i in range(n):
        for j in range(n):
            text = ax.text(j, i, f"{full_matrix[i, j]:.2f}",
            ha="center", va="center", color="black" if full_matrix[i, j] < (full_matrix.max()/2) else "white")
    ax.set_title("Pairwise Distance Matrix", fontsize=16, pad=20)
    fig.tight_layout()
    return fig
            