import re
from collections import defaultdict

from docgraph.ingestion.cleaning.config import CleaningConfig
from docgraph.ingestion.cleaning.geometry import is_in_edge_band


def normalize_for_matching(text: str) -> str:
    if not text:
        return ""
    # With + we check if there is more that one digit ignore the digit from possition 1 onwards. This remove number of digits from fingerprint
    fingerprint = re.sub(r'\d+', "#", text)
    return " ".join(fingerprint.lower().split())

def edge_text_pages(text_list: list, page_dict: dict, edge_band_ratio: float = 0.10) -> dict:
    edge_map = defaultdict(set)

    for item in text_list:
        txt = item.get("text", "").strip()
        if not txt:
            continue

        if is_in_edge_band(item, page_dict, edge_band_ratio):
            norm_text = normalize_for_matching(txt)
            provs = item.get("prov", [])
            if provs:
                p_no = provs[0].get("page_no")
                if p_no is not None:
                    edge_map[norm_text].add(p_no)

    return dict(edge_map)

def find_furniture_texts(edge_map: dict, total_pages: int, config: CleaningConfig) -> set:
    threshold = config.page_threshold(total_pages)
    furniture = {
        norm_text for norm_text, pages in edge_map.items() if len(pages) >= threshold
    }
    return furniture