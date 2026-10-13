from dataclasses import dataclass

from docgraph.ingestion.cleaning.config import CleaningConfig
from docgraph.ingestion.cleaning.furniture import (
    edge_text_pages,
    find_furniture_texts,
    normalize_for_matching,
)
from docgraph.ingestion.cleaning.geometry import is_in_edge_band


@dataclass(frozen=True)
class CleaningResult:
    kept: list[dict]
    removed: list[dict]  # each entry: {"item": ..., "reason": ...}
    report: dict

def clean(data: dict, config: CleaningConfig) -> CleaningResult:
    REASON_REPEATED_EDGE = "repeated_edge"

    texts = data["texts"]
    page_dict = data["pages"]
    total_pages = len(page_dict)

    edge_map = edge_text_pages(texts, page_dict, config.edge_band_ratio)
    furniture = find_furniture_texts(edge_map, total_pages, config)

    kept, removed = [], []
    for item in texts:
        fingerprint = normalize_for_matching(item.get("text"))
        is_repeated = fingerprint in furniture
        on_edge = is_in_edge_band(item, page_dict, config.edge_band_ratio)

        if is_repeated and on_edge:
            removed.append({"item": item, "reason": REASON_REPEATED_EDGE})
        else:
            kept.append(item)

    assert len(kept) + len(removed) == len(texts)

    report = {
        "total": len(texts),
        "kept": len(kept),
        "removed": len(removed),
        "distinct_removed_fingerprints": len(
            {normalize_for_matching(r["item"].get("text")) for r in removed}
        ),
        "total_pages": total_pages,
        "page_threshold": config.page_threshold(total_pages),
    }
    return CleaningResult(kept=kept, removed=removed, report=report)