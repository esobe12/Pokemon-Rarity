# Data

## Layout

| Path | In git? | Description |
|------|---------|-------------|
| [`raw_pokewallet/`](raw_pokewallet/) | Yes | PokéWallet raw JSON (sets, search pages, `cards_raw.json`, manifest). |
| [`processed/cards_clean_pokewallet.csv`](processed/cards_clean_pokewallet.csv) | Yes | Tidy PokéWallet analysis table. |
| [`sample/cards_clean_pokewallet_sample.csv`](sample/cards_clean_pokewallet_sample.csv) | Yes | 25-row sample. |
| [`raw/`](raw/) | Yes | Earlier TCGdex raw snapshot. |
| [`processed/cards_clean.csv`](processed/cards_clean.csv) | Yes | Earlier TCGdex tidy table. |
| [`data_dictionary.md`](data_dictionary.md) | Yes | Field definitions. |

## Reproduce (PokéWallet)

```bash
cp .env.example .env   # PokeEDU_KEY=pk_live_...
pip install -r requirements.txt
jupyter notebook analysis.ipynb
```

See the root [README](../README.md) Data / Methods / Findings sections for counts and interpretation.
