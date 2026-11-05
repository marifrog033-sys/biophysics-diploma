from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "raw_topic_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Оставить пустым для автоматического поиска типичных названий.
# Если автоопределение не сработает, вписать точные названия столбцов CSV.
TEXT_COLUMNS = []

# SPECTER — предобученная модель эмбеддингов научных текстов.
MODEL_NAME = "sentence-transformers/allenai-specter"

RANDOM_STATE = 42
MIN_CLUSTERS = 2
MAX_CLUSTERS = 10
BATCH_SIZE = 16
