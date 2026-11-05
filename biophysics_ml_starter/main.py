import numpy as np

from src.config import OUTPUT_DIR, FIGURES_DIR
from src.data_loader import load_data, build_texts
from src.embeddings import create_embeddings
from src.clustering import find_best_k, save_metrics
from src.visualization import (
    plot_cluster_sizes,
    plot_clusters_2d,
    plot_silhouette_scores,
)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()
    clean_df, texts = build_texts(df)

    embeddings = create_embeddings(texts)
    np.save(OUTPUT_DIR / "embeddings.npy", embeddings)

    _, labels, scores = find_best_k(embeddings)
    clean_df["cluster"] = labels
    clean_df.to_csv(
        OUTPUT_DIR / "clustered_topics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    best_k = max(scores, key=scores.get)
    save_metrics(scores, best_k, OUTPUT_DIR / "clustering_metrics.json")

    plot_cluster_sizes(labels, FIGURES_DIR / "cluster_sizes.png")
    plot_clusters_2d(embeddings, labels, FIGURES_DIR / "clusters_2d.png")
    plot_silhouette_scores(scores, FIGURES_DIR / "silhouette_scores.png")

    print("\\nГотово. Результаты сохранены в папке outputs/.")


if __name__ == "__main__":
    main()
