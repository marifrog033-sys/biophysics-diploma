import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import MODEL_NAME, BATCH_SIZE


def create_embeddings(texts):
    print(f"Загрузка модели: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)
    print("Размер матрицы эмбеддингов:", embeddings.shape)
    return embeddings
