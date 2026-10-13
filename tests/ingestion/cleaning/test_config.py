import pytest

from docgraph.ingestion.cleaning.config import CleaningConfig


def test_default_config_values():
    config = CleaningConfig()
    assert config.min_pages == 3
    assert config.min_fraction == 0.30

@pytest.mark.parametrize("total_pages,expected_threshold", [
    (209, 63),  # 30% of 209 = 62.7 -> ceil = 63
    (21, 7),    # 30% of 21 = 6.3 -> ceil = 7
    (5, 3),     # Lower bound (min_pages = 3)
    (1, 3),     # Lower bound (min_pages = 3)
])
def test_page_threshold(total_pages, expected_threshold):
    config = CleaningConfig(min_pages=3, min_fraction=0.30)
    assert config.page_threshold(total_pages) == expected_threshold