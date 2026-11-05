# База данных `topic_analytics` — Описание

**СУБД:** PostgreSQL 15.6  
**Проекты:** ScienceTrending, ResearchAreaFiltrator, Horizon, Semantics  
**Драйвер:** psycopg2 2.9.12 (все запросы — raw SQL, ORM не используется)  
**Подключение:** `postgresql://myuser:mypassword@localhost:5432/topic_analytics`

---

## Выгруженные таблицы

| Таблица | Строк | Колонок | Описание |
|---------|-------|---------|----------|
| `raw_topic_data` | 753 024 | 8 | Сырые показатели заметности тем по годам |
| `citational_data` | 94 128 | 5 | Цитатные показатели Scopus/SciVal (2023–2025) |
| `clustering` | 36 000 | 4 | Результаты кластеризации тем |

**Уникальные темы:** 94 128 (`topic_id`)

---

## Детальное описание таблиц

### 1. `raw_topic_data`

**Назначение:** Исходные данные о заметности научных тем по годам.

| Поле | Тип | Описание |
|------|------|----------|
| `topic_id` | INTEGER | ID темы (часть PK) |
| `topic_title` | TEXT | Название темы |
| `cluster_id` | INTEGER | ID кластера |
| `cluster_title` | TEXT | Название кластера |
| `year` | INTEGER | Год (часть PK) |
| `topic_prominence` | FLOAT | Заметность темы |
| `cluster_prominence` | FLOAT | Заметность кластера |
| `biomedicine` | BOOLEAN | Принадлежность к биомедицине |

**Индексы:** `idx_raw_topic_year` on `year`  
**Первичный ключ:** `(topic_id, year)`

---

### 2. `citational_data`

**Назначение:** Реальные цитатные показатели из Scopus/SciVal за период 2023–2025.

| Поле | Тип | Описание |
|------|------|----------|
| `topic_id` | INTEGER | ID темы (часть PK) |
| `topic_title` | TEXT | Название темы |
| `year` | TEXT | Период: `"2023-2025"` (часть PK) |
| `scholarly_output` | DOUBLE PRECISION | Количество публикаций |
| `fwci` | DOUBLE PRECISION | Field-Weighted Citation Impact |

**Первичный ключ:** `(topic_id, year)`

**Интерпретация FWCI:**
- `FWCI = 1.0` — цитируемость на уровне мирового среднего
- `FWCI > 1.0` — выше мирового среднего
- `FWCI < 1.0` — ниже мирового среднего
- Диапазон в БД: 0.0 – 22.6

---

### 3. `clustering`

**Назначение:** Результаты кластеризации научных тем на двух уровнях детализации.

| Поле | Тип | Описание |
|------|------|----------|
| `topic_id` | INTEGER | ID темы (PK) |
| `topic_title` | TEXT | Название темы |
| `cluster_200` | INTEGER | Номер кластера (уровень 200) |
| `cluster_50` | INTEGER | Номер кластера (уровень 50) |

**Первичный ключ:** `topic_id`

**Уровни кластеризации:**

| Уровень | Кол-во кластеров | Диапазон значений | Назначение |
|---------|------------------|-------------------|------------|
| `cluster_50` | 50 | 0–49 | Крупные исследовательские районы |
| `cluster_200` | 200 | 0–199 | Детальные подгруппы |

**Пример:**
| topic_id | topic_title | cluster_200 | cluster_50 |
|----------|-------------|-------------|------------|
| 0 | Innovative Deep Learning Techniques for Object Detection | 123 | 30 |
| 6 | Antimicrobial and Anticancer Applications of Nanoparticles | 189 | 46 |
| 8 | Microplastics as Environmental Pollutants and Risks | 111 | 27 |

**Иерархия:** Каждая тема одновременно принадлежит к кластеру уровня 50 и подкластеру уровня 200.

---

## Выгруженные файлы

| Файл | Строк | Колонок | Размер |
|------|-------|---------|--------|
| `raw_topic_data.csv` | 753 024 | 8 | 94 МБ |
| `citational_data.csv` | 94 128 | 5 | 7,1 МБ |
| `clustering.csv` | 36 000 | 4 | 2,2 МБ |

---

## Технические детали

- **Нет ORM** — все запросы через `psycopg2` с raw SQL
- **Нет миграций** — схема управляется через `init_db.sql` (DROP + CREATE)
- **Нет `.env` файлов** — credentials в `config.json`
- **Повторяющаяся структура** — одинаковая логика в `Archive/Horizon/`, `Archive/Horizon_beta/`, `ScienceTrending/`
