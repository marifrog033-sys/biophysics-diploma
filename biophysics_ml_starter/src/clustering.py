import json
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from src.config import MIN_CLUSTERS, MAX_CLUSTERS, RANDOM_STATE


def find_best_k(embeddings):
    n_samples = len(embeddings)
    if n_samples < 3:
        raise ValueError("Для кластеризации и оценки silhouette нужно минимум 3 объекта.")

    upper_k = min(MAX_CLUSTERS, n_samples - 1)
    scores = {}

    for k in range(MIN_CLUSTERS, upper_k + 1):
        model = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init="auto",
        )
        labels = model.fit_predict(embeddings)

        # Silhouette score требует минимум два непустых кластера.
        if len(set(labels)) > 1:
            score = silhouette_score(
                embeddings,
                labels,
                sample_size=min(5000, n_samples),
                random_state=RANDOM_STATE,
            )
            scores[k] = float(score)
            print(f"k={k}: silhouette={score:.4f}")

    if not scores:
        raise RuntimeError("Не удалось подобрать число кластеров.")

    best_k = max(scores, key=scores.get)
    best_model = KMeans(
        n_clusters=best_k,
        random_state=RANDOM_STATE,
        n_init="auto",
    )
    best_labels = best_model.fit_predict(embeddings)

    return best_model, best_labels, scores


def save_metrics(scores, best_k, output_path: Path):
    payload = {
        "selected_k": int(best_k),
        "silhouette_scores": {str(k): v for k, v in scores.items()},
        "best_silhouette": float(scores[best_k]),
    }
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
