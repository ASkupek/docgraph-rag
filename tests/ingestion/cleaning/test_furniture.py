from docgraph.ingestion.cleaning.config import CleaningConfig
from docgraph.ingestion.cleaning.furniture import (
    edge_text_pages,
    find_furniture_texts,
    normalize_for_matching,
)


def test_edge_text_pages_logic():
    """Test mapping of edge text to unique page sets using prov[0]."""
    # Mock page dictionary with a standard height
    page_dict = {
        "1": {"size": {"height": 800.0}},
        "2": {"size": {"height": 800.0}},
        "3": {"size": {"height": 800.0}},
    }
    
    texts_list = [
        # Page 1: Item in the top edge band (y: 750 to 780, assuming BOTTOMLEFT or top-relative depending on geometry logic)
        {
            "text": "Page Header",
            "prov": [{"page_no": 1, "bbox": {"coord_origin": "BOTTOMLEFT", "l": 0, "t": 750, "r": 100, "b": 780}}]
        },
        # Page 2: Same item appearing twice on the same page (should be deduplicated into a set)
        {
            "text": "Page Header",
            "prov": [{"page_no": 2, "bbox": {"coord_origin": "BOTTOMLEFT", "l": 0, "t": 740, "r": 100, "b": 770}}]
        },
        {
            "text": "Page Header",
            "prov": [{"page_no": 2, "bbox": {"coord_origin": "BOTTOMLEFT", "l": 0, "t": 740, "r": 100, "b": 770}}]
        },
        # Page 3: Same item on a third page
        {
            "text": "Page Header",
            "prov": [{"page_no": 3, "bbox": {"coord_origin": "BOTTOMLEFT", "l": 0, "t": 745, "r": 100, "b": 775}}]
        },
        # Middle text (should be ignored by edge band check if ratio is small, or test with a valid edge band ratio)
        {
            "text": "Regular Body Text",
            "prov": [{"page_no": 1, "bbox": {"coord_origin": "BOTTOMLEFT", "l": 0, "t": 400, "r": 100, "b": 420}}]
        }
    ]

    # Run edge test pages with an edge band ratio that captures top items
    result = edge_text_pages(texts_list, page_dict, edge_band_ratio=0.15)
    
    # Assertions
    assert "page header" in result
    assert result["page header"] == {1, 2, 3}
    assert "regular body text" not in result


def test_find_furniture_texts():
    """Test threshold filtering to distinguish furniture from regular text."""
    # Simulate a document of 10 pages
    total_pages = 10
    config = CleaningConfig(min_pages=3, min_fraction=0.30)
    # Threshold for 10 pages: max(3, ceil(0.30 * 10)) = max(3, 3) = 3 pages.

    edge_text_pages = {
        "page # of #": {1, 2, 3},       # Present on 3 pages -> meets threshold -> Furniture
        "rare warning footer": {1, 2},   # Present on 2 pages -> below threshold -> Not furniture
    }

    furniture = find_furniture_texts(edge_text_pages, total_pages, config)

    assert "page # of #" in furniture
    assert "rare warning footer" not in furniture

def test_normalization_fingerprints():
    # 1. 19 / 209 -> # / # and NXP Semiconductors -> nxp semiconductors
    assert normalize_for_matching("19 / 209") == "# / #"
    assert normalize_for_matching("NXP Semiconductors") == "nxp semiconductors"

def test_normalization_empty_and_none():
    assert normalize_for_matching("") == ""
    assert normalize_for_matching(None) == ""

def test_normalization_same_fingerprint():
    # 4 / 209 and 19 / 209 data should add same fingerprint
    assert normalize_for_matching("4 / 209") == normalize_for_matching("19 / 209")

def test_normalization_voltage():
    # Voltage 2.4 V becomes #.# v
    assert normalize_for_matching("2.4 V") == "#.# v"