# Project Proposal: Pokémon Card Rarity, Age, and Market Value

**Edgar Soberon**  
**Course:** INFO 4617  
**Repository:** [https://github.com/esobe12/Pokemon-Rarity](https://github.com/esobe12/Pokemon-Rarity)

*Source: revised from the submitted proposal PDF (`Pokemon Research.pdf`).*

## Research question

**To what extent are Pokémon card rarity and age associated with their current market value?**

I will explore whether cards from older sets have higher prices and whether rarity explains price differences compared with cards in newer sets. Some cards graded in pristine condition have valued at over $1 million in both older and newer sets. This question matters to collectors, buyers, sellers, and anyone interested in how collectible markets assign value. The analysis is empirical and falsifiable. I expect rare cards to have higher market prices than common cards, but I do not expect age alone to account for value. I would be surprised if age were the strongest predictor of market value on its own, rather than age combined with rarity.

## Data sources and methods

### Sources

- **Primary (planned):** [Scrydex Pokémon TCG API](https://scrydex.com) — [API reference](https://scrydex.com/docs/pokemon/api-reference). Endpoint for English cards: `https://api.scrydex.com/pokemon/v1/en/cards`. Scrydex provides card IDs, names, rarity, release dates, language, and prices when requested. Access requires an API key.
- **Alternate / possible primary:** [pokewallet.io](https://pokewallet.io/api-docs) (free tier). Connected to TCGPlayer for real-time prices; over 50k cards on file, plus sealed-product prices. Useful for follow-up questions as well.

### Methods

- Use Python `requests` to call the API, parse JSON, and use **pandas** to flatten nested expansion and variant data into a table (access/platform restrictions; JSON structure and parsing; request–response workflows and pagination).
- Check response codes, handle errors, and page through results in batches of at most **100**.
- Compare median prices by rarity and release period; make boxplots and scatterplots of age versus price.
- Target sample: approximately **300–500 cards** across expansion packs from **1999 through 2026**, with a mix of rarity categories.
- Analysis will be a **one-time price snapshot**, not a claim about historical market paths.
- Compare raw/ungraded and graded conditions where the API permits; exclude records missing price or age.

### Record fields

I will use: card id, card name, set id/name, rarity, variant, market price, and timestamp.

## Ethics and feasibility

- Prefer an official API (Scrydex or pokewallet.io) rather than scraping market pages.
- **Scrydex:** paid membership (~$29/month), API key, ~5k credits; access to TCG data and RAW prices; up to 100 cards per request.
- **pokewallet.io:** free plan with signup for an API key; rate limits ~100 requests/hour and ~1k/day; access to ~50k Pokémon cards, rarity, and prices. May use this as the primary source for cost reasons.
- Focus is on **cards**, not individuals. If seller-related fields appear, exploration will stay limited to card attributes and not personal seller information.

## AI use disclosure

I did not use ChatGPT for this proposal. I may use it later to troubleshoot code as the research begins; any such use will be annotated (where and how).

## Repository deliverables (portfolio)

| Path | Role |
|------|------|
| [`README.md`](README.md) | Project overview and section placeholders |
| [`analysis.ipynb`](analysis.ipynb) | Data collection and analysis notebook |
| [`report.md`](report.md) | Written report (or link to a final PDF) |
| [`data/`](data/) | Datasets and data documentation |
| [`Pokemon_Research.pdf`](Pokemon_Research.pdf) | Original proposal PDF |
