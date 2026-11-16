# Data dictionary — cleaned Pokémon TCG tables

## PokéWallet analysis table (this week)

Files:
- [`processed/cards_clean_pokewallet.csv`](processed/cards_clean_pokewallet.csv)
- [`sample/cards_clean_pokewallet_sample.csv`](sample/cards_clean_pokewallet_sample.csv)

Each row is one English Pokémon TCG **card** (not sealed product) from the PokéWallet snapshot, after cleaning.

| Field | Type | Meaning |
|-------|------|---------|
| `card_id` | string | PokéWallet card id (`pk_…` for TCGPlayer-linked cards). |
| `card_name` | string | Card name from `card_info.name`. |
| `set_id` | string | Numeric PokéWallet set id (stable join key). |
| `set_code` | string | Short set code (e.g. `BS`, `FO`). |
| `set_name` | string | Set name. |
| `release_date` | date (`YYYY-MM-DD`) | Parsed set release date used for age. |
| `age_years` | number | Years from `release_date` to collection/reference date. |
| `rarity` | string | Printed rarity string from the API. |
| `card_number` | string | Collector number when present. |
| `variant_price_source` | string | TCGPlayer finish used for the price (e.g. Normal, Holofoil). |
| `market_price_usd` | number | TCGPlayer `market_price` (USD) at snapshot time. |
| `collected_at_utc` | string | Collection timestamp (UTC). |
| `rarity_bucket` | string | Coarse rarity group for comparisons. |
| `era` | string | Age band for release-period comparisons. |

### Cleaning rules

- Keep `product_type` cards only (exclude sealed).
- Require `card_id`, name, set, rarity, release date, and positive TCGPlayer `market_price`.
- Prefer the highest positive `market_price` across finish variants on the card.
- Age comes from set release date, not print variant.

## Earlier TCGdex table

[`processed/cards_clean.csv`](processed/cards_clean.csv) / [`sample/cards_clean_sample.csv`](sample/cards_clean_sample.csv) use TCGdex ids and fields from the prior collection week.
