from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any, Iterable, Iterator

from .models import Restaurant
from .normalization import (
    normalize_cost,
    normalize_cuisines,
    normalize_location,
    normalize_name,
    normalize_rating,
)
from .schema import assert_source_schema

HF_DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
# Keep revision pin explicit. Update only with a documented data-contract change.
HF_DATASET_REVISION = "main"


def _iter_local_rows(path: Path) -> Iterator[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            for row in data:
                if isinstance(row, dict):
                    yield row
            return
        raise ValueError("JSON source must be a list of objects.")
    if suffix == ".jsonl":
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if isinstance(row, dict):
                    yield row
            return
    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield dict(row)
        return
    raise ValueError(f"Unsupported local source type: {suffix}")


def _iter_hf_rows(limit: int | None = None) -> Iterator[dict[str, Any]]:
    try:
        from datasets import load_dataset  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "datasets package is required for Hugging Face loading. "
            "Install with: py -m pip install datasets"
        ) from exc

    split = os.getenv("HF_DATASET_SPLIT", "train")
    dataset = load_dataset(
        HF_DATASET_NAME,
        split=split,
        revision=HF_DATASET_REVISION,
    )
    count = 0
    for row in dataset:
        if isinstance(row, dict):
            yield row
            count += 1
            if limit is not None and count >= limit:
                break


def _restaurant_from_row(row: dict[str, Any], mapping: dict[str, str]) -> Restaurant | None:
    name = normalize_name(row.get(mapping["name"]))
    location = normalize_location(row.get(mapping["location"]))
    cuisines = normalize_cuisines(row.get(mapping["cuisines"]))
    cost = normalize_cost(row.get(mapping["cost"]))
    rating = normalize_rating(row.get(mapping["rating"]))
    if not name or not location or not cuisines or rating is None:
        return None
    metadata = {k: v for k, v in row.items() if k not in mapping.values()}
    return Restaurant(
        name=name,
        location=location,
        cuisines=cuisines,
        cost=cost,
        rating=rating,
        metadata=metadata,
    )


def iter_restaurants(
    *,
    source: str = "hf",
    local_path: str | None = None,
    limit: int | None = None,
    dedupe: bool = True,
) -> Iterator[Restaurant]:
    if source == "hf":
        row_iter = _iter_hf_rows(limit=limit)
    elif source == "local":
        if not local_path:
            raise ValueError("local_path is required when source='local'.")
        row_iter = _iter_local_rows(Path(local_path))
    else:
        raise ValueError("source must be one of: 'hf', 'local'.")

    mapping: dict[str, str] | None = None
    emitted = 0
    seen_keys: set[tuple[str, str]] = set()

    for row in row_iter:
        if mapping is None:
            mapping = assert_source_schema(row)
        restaurant = _restaurant_from_row(row, mapping)
        if restaurant is None:
            continue
        if dedupe:
            dedupe_key = (restaurant.name.lower(), restaurant.location)
            if dedupe_key in seen_keys:
                continue
            seen_keys.add(dedupe_key)
        yield restaurant
        emitted += 1
        if limit is not None and emitted >= limit:
            break


def load_restaurants(
    *,
    source: str = "hf",
    local_path: str | None = None,
    limit: int | None = None,
    dedupe: bool = True,
) -> list[Restaurant]:
    return list(
        iter_restaurants(
            source=source,
            local_path=local_path,
            limit=limit,
            dedupe=dedupe,
        )
    )


def summarize_restaurants(restaurants: Iterable[Restaurant]) -> dict[str, Any]:
    items = list(restaurants)
    unique_locations = sorted({r.location for r in items})
    return {
        "count": len(items),
        "unique_locations": len(unique_locations),
        "sample_locations": unique_locations[:5],
        "avg_rating": round(sum(r.rating for r in items) / len(items), 3) if items else 0.0,
    }
