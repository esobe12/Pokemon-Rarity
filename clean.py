#!/usr/bin/env python3
"""
Clean raw TCGdex card JSON into a tidy rectangular dataset.

Reads data/raw/cards_raw.json (from collect.py) and writes:
  - data/processed/cards_clean.csv  (full tidy table)
  - data/sample/cards_clean_sample.csv  (small sample for the repo)
  - prints a short cleaning summary to stdout
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data" / "raw" / "cards_raw.json"
PROCESSED_DIR = ROOT / "data" / "processed"
SAMPLE_DIR = ROOT / "data" / "sample"
SAMPLE_N = 25
REFERENCE_DATE = date(2026, 11, 9)  # collection week reference for "age"


def extract_market_price_usd(card: dict) -> tuple[float | None, str | None]:
    """Prefer TCGPlayer marketPrice from variants_detailed; fall back to top-level pricing."""
    variants = card.get("variants_detailed") or []
    best_price: float | None = None
    best_variant: str | None = None

    for variant in variants:
        pricing = (variant.get("pricing") or {}).get("tcgplayer") or {}
        variant_type = variant.get("type") or "unknown"
        # pricing may nest by finish: normal / holofoil / reverse-holofoil / etc.
        candidates: list[tuple[str, float]] = []
        if isinstance(pricing.get("marketPrice"), (int, float)):
            candidates.append((variant_type, float(pricing["marketPrice"])))
        for finish, payload in pricing.items():
            if isinstance(payload, dict) and isinstance(payload.get("marketPrice"), (int, float)):
                label = f"{variant_type}:{finish}"
                candidates.append((label, float(payload["marketPrice"])))
        for label, price in candidates:
            if best_price is None or price > best_price:
                best_price = price
                best_variant = label

    if best_price is not None:
        return best_price, best_variant

    # Top-level pricing (TCGPlayer) used by some cards
    top = card.get("pricing") or {}
    tcg = top.get("tcgplayer") if isinstance(top, dict) else None
    if isinstance(tcg, dict):
        for finish, payload in tcg.items():
            if isinstance(payload, dict) and isinstance(payload.get("marketPrice"), (int, float)):
                price = float(payload["marketPrice"])
                if best_price is None or price > best_price:
                    best_price = price
                    best_variant = f"top:{finish}"
    return best_price, best_variant


def parse_release_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def tidy_rows(cards: list[dict]) -> pd.DataFrame:
    rows: list[dict] = []
    for card in cards:
        release = parse_release_date(card.get("_set_releaseDate"))
        price, variant = extract_market_price_usd(card)
        age_years = None
        if release is not None:
            age_years = round((REFERENCE_DATE - release).days / 365.25, 2)

        rows.append(
            {
                "card_id": card.get("id"),
                "card_name": card.get("name"),
                "set_id": card.get("_set_id") or (card.get("set") or {}).get("id"),
                "set_name": card.get("_set_name") or (card.get("set") or {}).get("name"),
                "release_date": release.isoformat() if release else None,
                "age_years": age_years,
                "rarity": card.get("rarity"),
                "category": card.get("category"),
                "local_id": card.get("localId"),
                "variant_price_source": variant,
                "market_price_usd": price,
                "collected_at_utc": card.get("_collected_at"),
                "source_url": card.get("_source_url"),
            }
        )

    df = pd.DataFrame(rows)

    before = len(df)
    # Require identity fields, rarity, age, and a usable price.
    df = df.dropna(subset=["card_id", "card_name", "set_id", "rarity", "release_date", "market_price_usd"])
    df = df[df["market_price_usd"] > 0]
    df = df.drop_duplicates(subset=["card_id", "variant_price_source"])
    after = len(df)

    print(f"Cleaning summary")
    print(f"  rows in:  {before}")
    print(f"  rows out: {after} (dropped {before - after} missing price/age/rarity or non-positive price)")
    print(f"  sets:     {df['set_id'].nunique()}")
    print(f"  rarities: {sorted(df['rarity'].dropna().unique())}")
    print(f"  price USD min/median/max: "
          f"{df['market_price_usd'].min():.2f} / "
          f"{df['market_price_usd'].median():.2f} / "
          f"{df['market_price_usd'].max():.2f}")
    return df.sort_values(["release_date", "set_id", "card_id"]).reset_index(drop=True)


def main() -> None:
    if not RAW_PATH.exists():
        raise SystemExit(f"Missing {RAW_PATH}. Run collect.py first.")

    cards = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    df = tidy_rows(cards)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    full_path = PROCESSED_DIR / "cards_clean.csv"
    sample_path = SAMPLE_DIR / "cards_clean_sample.csv"
    df.to_csv(full_path, index=False)

    sample = df.sample(n=min(SAMPLE_N, len(df)), random_state=4617).sort_values(
        ["release_date", "card_id"]
    )
    sample.to_csv(sample_path, index=False)

    meta = {
        "cleaned_at_utc": datetime.now(timezone.utc).isoformat(),
        "n_rows_clean": int(len(df)),
        "n_rows_sample": int(len(sample)),
        "reference_date_for_age": REFERENCE_DATE.isoformat(),
        "full_csv": str(full_path.relative_to(ROOT)),
        "sample_csv": str(sample_path.relative_to(ROOT)),
    }
    (PROCESSED_DIR / "clean_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {full_path}")
    print(f"Wrote {sample_path}")
    print(sample.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
