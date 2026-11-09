#!/usr/bin/env python3
"""
Collect a one-time snapshot of Pokémon TCG card metadata and market prices
from the public TCGdex API for INFO 4617 (Edgar Soberon).

Polite collection:
  - Identifies the requester in the User-Agent
  - Pauses between requests
  - Checks HTTP status codes and stops clearly on repeated failures

Raw responses are written under data/raw/ (not committed).
"""

from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "https://api.tcgdex.net/v2/en"
USER_AGENT = (
    "EdgarSoberon-INFO4617/1.0 "
    "(edso9941@colorado.edu; University of Colorado Boulder educational research)"
)
REQUEST_PAUSE_SECONDS = 0.6
MAX_RETRIES = 3
TARGET_CARDS = 400
CARDS_PER_SET = 40
RANDOM_SEED = 4617

# Stratified main expansions across eras (1999–2020s). Promo/misc sets omitted.
SAMPLE_SETS = [
    "base1",  # Base Set (1999)
    "base5",  # Team Rocket
    "ex1",  # Ruby & Sapphire (2003)
    "dp1",  # Diamond & Pearl
    "bw1",  # Black & White
    "xy1",  # XY (2014)
    "sm1",  # Sun & Moon (2017)
    "swsh1",  # Sword & Shield (2020)
    "swsh3",  # Darkness Ablaze
    "sv01",  # Scarlet & Violet (2023)
    "sv03",  # Obsidian Flames
    "sv04",  # Paradox Rift
]

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
)


def polite_get(url: str) -> dict | list:
    """GET JSON with retries, status checks, and a pause after each attempt."""
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        time.sleep(REQUEST_PAUSE_SECONDS)
        try:
            response = SESSION.get(url, timeout=60)
            if response.status_code == 429:
                wait = REQUEST_PAUSE_SECONDS * (2**attempt)
                print(f"  rate limited; sleeping {wait:.1f}s")
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.json()
        except Exception as exc:  # noqa: BLE001 - surface and retry network/HTTP errors
            last_error = exc
            print(f"  attempt {attempt}/{MAX_RETRIES} failed for {url}: {exc}")
    raise RuntimeError(f"Failed to fetch {url}") from last_error


def save_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def sample_card_ids(cards: list[dict], n: int, rng: random.Random) -> list[str]:
    ids = [c["id"] for c in cards if c.get("id")]
    if len(ids) <= n:
        return ids
    return rng.sample(ids, n)


def main() -> None:
    collected_at = datetime.now(timezone.utc).isoformat()
    rng = random.Random(RANDOM_SEED)
    print(f"Collection started at {collected_at}")
    print(f"User-Agent: {USER_AGENT}")
    print(f"Pause between requests: {REQUEST_PAUSE_SECONDS}s")

    set_summaries: list[dict] = []
    card_payloads: list[dict] = []

    for set_id in SAMPLE_SETS:
        if len(card_payloads) >= TARGET_CARDS:
            break

        print(f"Fetching set {set_id}…")
        set_url = f"{BASE_URL}/sets/{set_id}"
        set_data = polite_get(set_url)
        assert isinstance(set_data, dict)
        save_json(RAW_DIR / "sets" / f"{set_id}.json", set_data)
        set_summaries.append(
            {
                "id": set_data.get("id"),
                "name": set_data.get("name"),
                "releaseDate": set_data.get("releaseDate"),
                "cardCount": set_data.get("cardCount"),
            }
        )

        remaining = TARGET_CARDS - len(card_payloads)
        take = min(CARDS_PER_SET, remaining)
        chosen_ids = sample_card_ids(set_data.get("cards") or [], take, rng)
        print(f"  sampling {len(chosen_ids)} cards from {set_data.get('name')}")

        for card_id in chosen_ids:
            card_url = f"{BASE_URL}/cards/{card_id}"
            card = polite_get(card_url)
            assert isinstance(card, dict)
            # Attach collection metadata without mutating API schema meaning.
            card["_collected_at"] = collected_at
            card["_source_url"] = card_url
            card["_set_releaseDate"] = set_data.get("releaseDate")
            card["_set_name"] = set_data.get("name")
            card["_set_id"] = set_data.get("id")
            save_json(RAW_DIR / "cards" / f"{card_id}.json", card)
            card_payloads.append(card)
            print(f"  saved {card_id} ({len(card_payloads)}/{TARGET_CARDS})")

    manifest = {
        "source": "TCGdex API",
        "base_url": BASE_URL,
        "docs": "https://tcgdex.dev/",
        "collector": "Edgar Soberon <edso9941@colorado.edu>",
        "user_agent": USER_AGENT,
        "collected_at_utc": collected_at,
        "request_pause_seconds": REQUEST_PAUSE_SECONDS,
        "sample_sets": SAMPLE_SETS,
        "n_sets_fetched": len(set_summaries),
        "n_cards_fetched": len(card_payloads),
        "sets": set_summaries,
        "card_ids": [c.get("id") for c in card_payloads],
    }
    save_json(RAW_DIR / "manifest.json", manifest)
    save_json(RAW_DIR / "cards_raw.json", card_payloads)

    print(
        f"Done. Wrote {len(card_payloads)} raw cards and manifest to {RAW_DIR}/ "
        "(keep this directory local; see README Data section)."
    )


if __name__ == "__main__":
    main()
