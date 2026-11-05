"""Схожесть названий тем с «биофизика» через allenai/specter (запускать локально, нужен доступ к HuggingFace).
pip install torch transformers pandas openpyxl scikit-learn
Вход: filtered_2024_2025.csv (или любая таблица с topic_id, topic_title); biophysics_topics.xlsx (лист «Валидация порога» для подбора порога).
Выход: specter_scores.csv (topic_id, cosine, score_0_100) и печать точности по порогам."""
import numpy as np, pandas as pd, torch
from transformers import AutoTokenizer, AutoModel

tok = AutoTokenizer.from_pretrained("allenai/specter"); model = AutoModel.from_pretrained("allenai/specter").eval()
ANCHORS = ["Biophysics", "Molecular biophysics of proteins and nucleic acids", "Ion channels and membrane biophysics",
           "Single-molecule force spectroscopy", "Biological membranes and lipid bilayers", "Mechanotransduction and cell mechanics",
           "Protein folding and molecular dynamics of biomolecules", "Bioelectricity and electrophysiology",
           "Biological effects of radiation and electromagnetic fields", "Biomedical optics and laser-tissue interaction"]

@torch.no_grad()
def embed(texts, bs=128):
    out = []
    for i in range(0, len(texts), bs):
        b = tok(texts[i:i+bs], padding=True, truncation=True, max_length=64, return_tensors="pt")
        out.append(model(**b).last_hidden_state[:, 0, :].numpy())
    e = np.vstack(out); return e / np.linalg.norm(e, axis=1, keepdims=True)

raw = pd.read_csv("filtered_2024_2025.csv", usecols=["topic_id", "topic_title"]).drop_duplicates("topic_id")  # ~94 тыс. названий, куски по bs
E, A = embed(raw.topic_title.tolist()), embed(ANCHORS)
cos = (E @ A.T).max(1)
# шкала 0-100: 0 = медиана всех тем, 100 = максимум среди самих якорей
lo, hi = np.median(cos), np.max(cos)
raw["cosine"] = cos; raw["score_0_100"] = np.clip(100 * (cos - lo) / (hi - lo), 0, 100).round(1)
raw.to_csv("specter_scores.csv", index=False)

# подбор порога по размеченной выборке (метки B / b / N в листе «Валидация порога»)
lab = pd.read_excel("biophysics_topics.xlsx", sheet_name="Валидация порога", header=3).dropna(subset=["topic_id"])
lab = lab[lab["Метка (Claude)"].isin(["B", "b", "N"])].merge(raw[["topic_id", "score_0_100"]], on="topic_id")
lab["pos"] = lab["Метка (Claude)"].isin(["B"])
for t in range(40, 100, 10):
    s = lab[lab.score_0_100 >= t]
    print(f"порог {t}: тем в выборке {len(s)}, точность {s.pos.mean():.0%}" if len(s) else f"порог {t}: пусто")
