import json
from docgraph.ingestion.cleaning.config import CleaningConfig
from docgraph.ingestion.cleaning.cleaner import clean
from collections import Counter

from docgraph.ingestion.cleaning.furniture import normalize_for_matching

if __name__ == "__main__":

    config = CleaningConfig(
        edge_band_ratio=0.10,
        min_pages=3,
        min_fraction=0.30,
    )

    json_path = "data/parsed/PN7220.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = clean(data, config)

    # **data basically take all data from the original json and replace the "texts" field with the cleaned texts.
    cleaned = {**data, "texts": result.kept}

    with open("data/parsed/PN7220_cleaned.json", "w", encoding="utf-8", ) as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=4)

    with open("data/parsed/PN7220_removed.json", "w", encoding="utf-8", ) as f:
        json.dump(result.removed, f, ensure_ascii=False, indent=4)

    with open("data/parsed/PN7220_report.json", "w", encoding="utf-8", ) as f:
        json.dump(result.report, f, ensure_ascii=False, indent=4)

