# Pokémon Card Rarity, Age, and Market Value

**Edgar Soberon** · INFO 4617 Final Project

**Research question:** To what extent are Pokémon card rarity and age associated with their current market value? I will explore whether cards from older sets have higher prices and whether rarity explains price differences compared with cards in newer sets. Using a public Pokémon TCG API snapshot, I collect English cards across expansions from 1999 through recent Scarlet & Violet sets, clean them into a tidy table with rarity, age, and USD market price, and (in later weeks) compare prices by rarity and release period with boxplots, scatterplots, and simple models. I expect rarer cards to sell for more than common cards, but I do not expect age alone to be the strongest predictor—value is more likely to reflect rarity and age together than age by itself.

## Repository contents

| Path | Purpose |
|------|---------|
| [`proposal.md`](proposal.md) | Research proposal |
| [`collect.py`](collect.py) | Polite API collection → `data/raw/` |
| [`clean.py`](clean.py) | Cleaning step → tidy CSV + sample |
| [`analysis.ipynb`](analysis.ipynb) | Analysis notebook |
| [`report.md`](report.md) | Written report draft |
| [`data/`](data/) | Sample data, dictionary, processed table |
| [`requirements.txt`](requirements.txt) | Python dependencies |

## Data

**Source:** [TCGdex API](https://api.tcgdex.net/v2/en) ([docs](https://tcgdex.dev/)), English cards. Market prices come from TCGPlayer fields exposed by TCGdex. The proposal also considered Scrydex and pokewallet.io (both need API keys); TCGdex is used here because it is publicly readable without a key, supports polite scripted collection, and still provides rarity, set release dates, and USD market prices for the research question.

**Collected:** 2026-11-09 (UTC), one-time snapshot via `collect.py` (User-Agent identifies Edgar Soberon / INFO 4617; ~0.6s pause between requests).

**How many records:**
- **400** raw card JSON records downloaded across **10** main expansions (Base Set through Scarlet & Violet), stratified by era.
- **394** rows retained after cleaning in [`data/processed/cards_clean.csv`](data/processed/cards_clean.csv) (dropped 6 with missing rarity, release date, or usable market price).
- **25**-row sample in [`data/sample/cards_clean_sample.csv`](data/sample/cards_clean_sample.csv); field definitions in [`data/data_dictionary.md`](data/data_dictionary.md).

**What is kept out of the repo and why:**
- The full **`data/raw/`** dump (per-card JSON, combined `cards_raw.json`, set payloads, manifest) is **not** committed. It is larger than needed for review, can be regenerated with `python collect.py`, and republishing bulk API responses is unnecessary when the tidy table answers the project need. No seller/personal information is collected; only card catalog and market-price fields.

## Methods

*Placeholder for later weeks — exploratory plots and models relating rarity and age to market price.*

Cleaning already implemented in `clean.py`: flatten nested price/variant JSON, derive `age_years` from set release date, drop incomplete rows, write tidy CSV.

## Findings

*Placeholder — results will be summarized here after the analysis is complete.*

## How to reproduce

```bash
pip install -r requirements.txt
python collect.py   # writes data/raw/ (local only)
python clean.py     # writes data/processed/ and data/sample/
jupyter notebook analysis.ipynb
```
