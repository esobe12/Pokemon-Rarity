# Data dictionary — cleaned Pokémon TCG sample

File: [`sample/cards_clean_sample.csv`](sample/cards_clean_sample.csv)  
Full tidy table (local / also committed when small): [`processed/cards_clean.csv`](processed/cards_clean.csv)

Each row is one English Pokémon TCG card from the collection snapshot, after cleaning.

| Field | Type | Meaning |
|-------|------|---------|
| `card_id` | string | TCGdex card identifier (e.g. `base1-4`). |
| `card_name` | string | Printed card name. |
| `set_id` | string | TCGdex set identifier (e.g. `swsh1`). |
| `set_name` | string | Expansion / set name. |
| `release_date` | date (ISO `YYYY-MM-DD`) | Official set release date used as the card’s age anchor. |
| `age_years` | number | Years between `release_date` and the project reference date (2026-11-09). |
| `rarity` | string | Printed rarity label from TCGdex (e.g. Common, Rare, Ultra Rare). |
| `category` | string | Card category (e.g. Pokemon, Trainer, Energy). |
| `local_id` | string | Collector number within the set. |
| `variant_price_source` | string | Which variant/finish the USD market price was taken from. |
| `market_price_usd` | number | TCGPlayer market price in USD at collection time (snapshot). |
| `collected_at_utc` | string (ISO datetime) | When this card record was downloaded. |
| `source_url` | string | TCGdex API URL for the raw card JSON. |

## Cleaning rules (summary)

- Drop rows missing `card_id`, name, set, rarity, release date, or market price.
- Drop non-positive prices.
- Prefer TCGPlayer `marketPrice` from `variants_detailed`; otherwise use top-level pricing.
- Age is derived from set release date, not from individual print variants.
