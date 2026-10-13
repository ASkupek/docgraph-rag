def is_in_edge_band(item: dict, page_dict: dict, edge_band_ratio: float = 0.10) -> bool:
    # In prov we find the page number and bounding box.
    provs = item.get("prov", [])
    
    if not provs:
        return False

    # We only consider the first provenance entry.
    prov = provs[0]

    # Get page number and bounding box
    page_no = prov.get("page_no")
    bbox = prov.get("bbox")

    if page_no is None or not bbox:
        return False

    # Conver page number to string for dictionary lookup
    page_no_str = str(page_no)
    
    if page_no_str not in page_dict:
        return False

    # We check in the page dictionary for the page height.
    page_info = page_dict[page_no_str]
    page_height = page_info.get("size", {}).get("height")

    if page_height is None:
        return False

    # We extract the coordinate origin and top/bottom coordinates
    coord_origin = bbox.get("coord_origin")
    t = bbox.get("t")
    b = bbox.get("b")

    if t is None or b is None:
        return False
    # Calculate the center y-coordinate of the bounding box and the height of the edge band.
    center_y = (t + b) / 2.0
    band_height = page_height * edge_band_ratio
    if coord_origin == "TOPLEFT":
        # In TOPLEFT, 0 is at the top, height is at the bottom.
        # Top band: [0, band_height]
        # Bottom band: [height - band_height, height]
        in_top = 0 <= center_y <= band_height
        in_bottom = (page_height - band_height) <= center_y <= page_height
        return in_top or in_bottom
    
    else:  # BOTTOMLEFT (Docling standard)
        # In BOTTOMLEFT, 0 is at the bottom, height is at the top.
        # Top band: [height - band_height, height]
        # Bottom band: [0, band_height]
        in_top = (page_height - band_height) <= center_y <= page_height
        in_bottom = 0 <= center_y <= band_height
        return in_top or in_bottom
