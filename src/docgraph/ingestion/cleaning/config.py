import math
from dataclasses import dataclass


@dataclass
class CleaningConfig:
    edge_band_ratio: float = 0.10
    min_pages: int = 3
    min_fraction: float = 0.30

    def page_threshold(self, total_pages: int) -> int:
        # Calculate the minimum number of pages based on the fraction and the minimum pages constraint.
        # total_pages * self.min_fraction => for example: 200 pages and fraction 0.30 means that the element need to be present on at least 60 pages.
        # math.ceil roudn up
        # self.min_pages -> ensure that the min number of pages is respected
        return max(self.min_pages, math.ceil(self.min_fraction * total_pages))
    