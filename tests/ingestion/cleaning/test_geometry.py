from docgraph.ingestion.cleaning.geometry import is_in_edge_band


def test_edge_band_top():
    page_dict = {"1": {"size": {"height": 800.0}}}

    item = {
        "prov": [{"page_no": 1, "bbox": {"coord_origin": "BOTTOMLEFT", "t": 730, "b": 780}}]
    }
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is True

def test_edge_band_bottom():
    page_dict = {"1": {"size": {"height": 800.0}}}

    item = {
        "prov": [{"page_no": 1, "bbox": {"coord_origin": "BOTTOMLEFT", "t": 20, "b": 60}}]
    }
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is True

def test_edge_band_middle():
    page_dict = {"1": {"size": {"height": 800.0}}}

    item = {
        "prov": [{"page_no": 1, "bbox": {"coord_origin": "BOTTOMLEFT", "t": 300, "b": 500}}]
    }
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is False

def test_edge_band_missing_bbox():
    page_dict = {"1": {"size": {"height": 800.0}}}

    item = {"prov": [{"page_no": 1}]}
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is False

def test_geometry_bottomleft_real_docling_coordinates():
    """
    Test real Docling coordinates with BOTTOMLEFT origin.
    In BOTTOMLEFT system, 't' (top) is greater than 'b' (bottom) because Y grows upwards.
    Example header from page height 841.889: t=778.43, b=755.16. 
    Since it's near the top (within 10% edge band), it should be detected as in the edge band.
    """
    page_dict = {"1": {"size": {"height": 841.889}}}
    item = {
        "prov": [{
            "page_no": 1, 
            "bbox": {
                "coord_origin": "BOTTOMLEFT", 
                "l": 65.5, 
                "t": 778.43, 
                "r": 152.188, 
                "b": 755.16
            }
        }]
    }
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is True

def test_geometry_crossing_boundary():
    """
    Test that an element spanning across the edge band boundary into the middle 
    of the page is correctly rejected (not considered edge furniture).
    """
    page_dict = {"1": {"size": {"height": 841.889}}}
    item = {
        "prov": [{
            "page_no": 1, 
            "bbox": {
                "coord_origin": "BOTTOMLEFT", 
                "l": 0, 
                "t": 750.0,  # inside top band
                "r": 100, 
                "b": 400.0   # extends deep into the middle of the page
            }
        }]
    }
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is False

def test_geometry_missing_page():
    """
    Test that if a page number referenced by an element is missing from 
    the page dictionary, the function safely returns False instead of raising an error.
    """
    page_dict = {}
    item = {
        "prov": [{
            "page_no": 99, 
            "bbox": {
                "coord_origin": "BOTTOMLEFT", 
                "l": 0, 
                "t": 750.0, 
                "r": 100, 
                "b": 780.0
            }
        }]
    }
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is False

def test_geometry_bottomleft_real_footer():
    """
    Test real Docling coordinates for a footer at the bottom of the page 
    using standard A4 height (841.889 points).
    """
    page_dict = {"4": {"size": {"height": 841.889}}}
    item = {
        "prov": [{
            "page_no": 4, 
            "bbox": {
                "coord_origin": "BOTTOMLEFT", 
                "l": 100.0, 
                "t": 45.0, 
                "r": 200.0, 
                "b": 30.0
            }
        }]
    }
    # Center = 37.5. Bottom band for 10% on 841.889 is <= 84.1889. True.
    assert is_in_edge_band(item, page_dict, edge_band_ratio=0.10) is True