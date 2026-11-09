# Data

## Layout

| Path | In git? | Description |
|------|---------|-------------|
| [`raw/`](raw/) | **No** | Full raw API JSON (per-card files, `cards_raw.json`, `manifest.json`). |
| [`processed/cards_clean.csv`](processed/cards_clean.csv) | Yes | Full tidy dataset after cleaning. |
| [`sample/cards_clean_sample.csv`](sample/cards_clean_sample.csv) | Yes | Small sample for quick inspection. |
| [`data_dictionary.md`](data_dictionary.md) | Yes | Field definitions for the cleaned table. |

## Reproduce

```bash
pip install -r requirements.txt
python collect.py    # polite requests → data/raw/
python clean.py      # tidy CSV → data/processed/ and data/sample/
```

See the **Data** section in the root [README](../README.md) for source, collection date, record counts, and what is left out of the repository.
