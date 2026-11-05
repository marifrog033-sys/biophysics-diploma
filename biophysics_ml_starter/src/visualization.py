from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

try:
    import umap
except ImportError:
    umap = None


def plot_cluster_sizes(labels, output_path: Path):
    values, counts = np.unique(labels, return_counts=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([str(v) for v in values], counts)
    ax.set_title("Количество научных тем в кластерах")
    ax.set_xlabel("Кластер")
    ax.set_ylabel("Количество тем")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def reduce_dimensions(embeddings):
    if umap is not None and len(embeddings) >= 4:
        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=min(15, len(embeddings) - 1),
            min_dist=0.1,
            metric="cosine",
            random_state=42,
        )
        return reducer.fit_transform(embeddings), "UMAP"

    reducer = PCA(n_components=2, random_state=42)
    return reducer.fit_transform(embeddings), "PCA"


def plot_clusters_2d(embeddings, labels, output_path: Path):
    coordinates, method = reduce_dimensions(embeddings)

    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(
        coordinates[:, 0],
        coordinates[:, 1],
        c=labels,
        cmap="tab20",
        s=12,
        alpha=0.75,
    )
    ax.set_title(f"Визуализация эмбеддингов: {method}")
    ax.set_xlabel(f"{method}-1")
    ax.set_ylabel(f"{method}-2")
    fig.colorbar(scatter, ax=ax, label="Кластер")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def plot_silhouette_scores(scores, output_path: Path):
    ks = list(scores.keys())
    values = [scores[k] for k in ks]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ks, values, marker="o")
    ax.set_title("Подбор числа кластеров")
    ax.set_xlabel("Количество кластеров (k)")
    ax.set_ylabel("Silhouette score")
    ax.set_xticks(ks)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
