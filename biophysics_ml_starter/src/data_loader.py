import pandas as pd

from src.config import DATA_PATH, TEXT_COLUMNS

TEXT_CANDIDATES = [
    "title", "topic", "name", "label", "abstract",
    "description", "text", "keywords", "Title", "Abstract",
    "Topic", "Description"
]


def load_data(path=DATA_PATH):
    if not path.exists():
        raise FileNotFoundError(
            f"Не найден файл: {path}\n"
            "Положите raw_topic_data.csv в папку data/raw."
        )

    # sep=None позволяет определить распространённый разделитель CSV.
    df = pd.read_csv(path, sep=None, engine="python")
    if df.empty:
        raise ValueError("CSV загружен, но в нём нет строк.")

    print(f"Загружено строк: {len(df):,}")
    print("Столбцы:", list(df.columns))
    return df


def build_texts(df):
    columns = TEXT_COLUMNS or [
        col for col in TEXT_CANDIDATES if col in df.columns
    ]

    if not columns:
        raise ValueError(
            "Не удалось автоматически определить текстовые столбцы.\n"
            f"Доступные столбцы: {list(df.columns)}\n"
            "Укажите нужные названия в src/config.py → TEXT_COLUMNS."
        )

    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"В TEXT_COLUMNS указаны отсутствующие столбцы: {missing}")

    text = (
        df[columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    valid_mask = text.ne("")
    clean_df = df.loc[valid_mask].copy().reset_index(drop=True)
    clean_texts = text.loc[valid_mask].tolist()

    if not clean_texts:
        raise ValueError("После очистки не осталось непустых текстов.")

    print(f"Используемые текстовые столбцы: {columns}")
    print(f"Объектов с непустым текстом: {len(clean_texts):,}")
    return clean_df, clean_texts
