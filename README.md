# Pokémon Card Rarity, Age, and Market Value

**Edgar Soberon** · INFO 4617 Final Project

**Research question:** To what extent are Pokémon card rarity and age associated with their current market value? I explore whether cards from older sets have higher prices and whether rarity explains price differences compared with cards in newer sets. Using a PokéWallet API snapshot of English cards with TCGPlayer market prices, I clean the data into a tidy table and compare median prices by rarity and release era, plus the age–price relationship. I expect rarer cards to sell for more than common cards, but I do not expect age alone to be the strongest predictor.

## Repository contents

| Path | Purpose |
|------|---------|
| [`proposal.md`](proposal.md) | Research proposal |
| [`analysis.ipynb`](analysis.ipynb) | Analysis notebook (PokéWallet collect → clean → results; outputs saved) |
| [`figures/rarity_age_vs_price.png`](figures/rarity_age_vs_price.png) | Main figure for this week |
| [`data/`](data/) | Raw snapshot, cleaned table, sample, dictionary |
| [`report.md`](report.md) | Written report draft |
| [`requirements.txt`](requirements.txt) | Python dependencies |
| [`collect.py`](collect.py) / [`clean.py`](clean.py) | Earlier TCGdex collect/clean scripts (still reproducible) |

## Data

**Primary source (analysis week):** [PokéWallet API](https://pokewallet.io/api-docs) (`https://api.pokewallet.io`). Auth via `X-API-Key` from local env var `PokeEDU_KEY`. Requests use User-Agent `WebDataScience/1.0 (edgar.soberonmunoz@colorado.edu)` with pauses between calls.

**Collected:** 2026-11-16 (UTC), one-time snapshot.

**How many records:**
- **569** raw card records in [`data/raw_pokewallet/`](data/raw_pokewallet/) (`cards_raw.json`, per-set search JSON, `sets.json`, `manifest.json`).
- **568** cleaned rows in [`data/processed/cards_clean_pokewallet.csv`](data/processed/cards_clean_pokewallet.csv) after requiring rarity, release date, and a positive TCGPlayer `market_price` (sealed products excluded).
- **25**-row sample: [`data/sample/cards_clean_pokewallet_sample.csv`](data/sample/cards_clean_pokewallet_sample.csv).
- Field definitions: [`data/data_dictionary.md`](data/data_dictionary.md).

**What is in / out of the repo:**
- **In repo:** PokéWallet raw JSON + cleaned/sample CSVs + figure + notebook with outputs. No seller/personal information—only card catalog and market-price fields. API keys are **not** committed (`.env` is gitignored).
- **Also in repo (earlier week):** TCGdex snapshot under [`data/raw/`](data/raw/) and [`data/processed/cards_clean.csv`](data/processed/cards_clean.csv).

## Methods

1. **Collect:** `GET /sets`, keep English sets (`language == "eng"`), then page `GET /search?q=<set_code>` for chosen expansions (docs: search returns TCGPlayer prices; `/sets/:setCode` listings have empty `prices`). Polite pauses + rate-limit handling.
2. **Clean:** flatten nested `tcgplayer.prices`, take a positive `market_price`, derive `age_years` from set `release_date`, drop incomplete rows, bucket rarities (`Common`, `Uncommon`, `Rare`, `Ultra+`, `Secret/Special`) and eras.
3. **Analyze:** counts; **median USD price by rarity bucket** and **by release era**; Spearman correlation of age vs price (and vs log10 price); save a two-panel figure.

Reproduce:

```bash
cp .env.example .env   # set PokeEDU_KEY=pk_live_...
pip install -r requirements.txt
jupyter notebook analysis.ipynb   # Restart → Run All
```

## Findings

Preliminary results from the 2026-11-16 PokéWallet snapshot (**n = 568** cards with prices):

| Rarity bucket | n | Median market price (USD) |
|---------------|---|---------------------------|
| Common | 194 | 0.94 |
| Uncommon | 171 | 1.49 |
| Ultra+ | 23 | 4.08 |
| Secret/Special | 14 | 15.18 |
| Rare | 166 | 27.70 |

- **Rarity:** Medians rise from Common/Uncommon into higher-rarity groups. In this snapshot the **Rare** bucket (including many vintage holo rares) has the highest median, above Secret/Special and Ultra+—so rarity matters, but label buckets are uneven and vintage holos dominate the “Rare” group.
- **Age:** All cleaned rows fall in the **20+ years** era (ages ≈ 26.7–27.9 years), so this run does **not** yet compare old vs new sets cleanly. Spearman correlation of age vs price is ≈ **0.00** within this narrow age band.
- **Interpretation:** Part of the research question is answered on **rarity** (higher-rarity groups tend to price above commons/uncommons). The **age** comparison is inconclusive until later sets with correct, varied release dates are included (some PokéWallet set dates look unreliable—for example names like “SM Base Set” / “XY Base Set” arrived with 1999 dates).

**Figure:** [`figures/rarity_age_vs_price.png`](figures/rarity_age_vs_price.png)  
**Caption:** Median TCGPlayer market price differs sharply by rarity bucket, while age vs price is weak/noisy in this vintage-heavy snapshot—consistent with rarity mattering more than age alone so far.

## How to reproduce

```bash
pip install -r requirements.txt
# Optional earlier TCGdex path:
python collect.py && python clean.py
# PokéWallet analysis path:
jupyter notebook analysis.ipynb
```
