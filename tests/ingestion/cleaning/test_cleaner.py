from docgraph.ingestion.cleaning.cleaner import clean
from docgraph.ingestion.cleaning.config import CleaningConfig

H = 800.0

def _item(text, page, t, b):
    return {
        "text": text,
        "prov": [{"page_no": page, "bbox": {"coord_origin": "BOTTOMLEFT",
                                            "l": 0, "r": 100, "t": t, "b": b}}],
    }

def test_clean_removes_only_repeated_edge_text():
    pages = {str(i): {"size": {"height": H}} for i in (1, 2, 3)}
    header = [_item("PN7220", p, 790, 770) for p in (1, 2, 3)]
    body = _item("Some paragraph", 1, 450, 400)
    mid_same_text = _item("PN7220", 2, 450, 430)  # same text, but mid-page
    data = {"texts": header + [body, mid_same_text], "pages": pages}

    result = clean(data, CleaningConfig())

    assert len(result.removed) == 3
    assert all(r["reason"] == "repeated_edge" for r in result.removed)
    assert body in result.kept
    assert mid_same_text in result.kept
    assert result.report["kept"] + result.report["removed"] == result.report["total"]