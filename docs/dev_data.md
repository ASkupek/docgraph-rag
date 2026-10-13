# docgraph/ingestion/cleaning
## config.py
Class is used to set the values that are important during document cleaning. We have 3 parameters:
* edge_band_ration: definition in % how big the header or footer are
* min_pages: Absolute minimum page occurrences required to classify as furniture
* min_fraction: Percentage-based threshold (e.g., 30% of total pages)

page_treshold: it gives answer on how many pages the element need to repeat that we count it as a repeted element:
Calculate the minimum number of pages based on the fraction and the minimum pages constraint.
total_pages * self.min_fraction => for example: 200 pages and fraction 0.30 means that the element need to be present on at least 60 pages.
math.ceil roudn up
self.min_pages -> ensure that the min number of pages is respected. This is important, since some things can repeat intentionally and on small documents same would be threated as repeted element which is not true

# geometry.py
It contains one function called is_in_edge_band. This function is responsible to check if element is somewhere in the top or bottom x%. If yes will return True else False

# furniture.py
We have three functions:
* normalize_for_matching: we change things like 29/209 to ##/### so basically convert to fingerprint to remove duplicates.
* edge_text_pages: function is goigh through all items in text_list and check if there are in the edge, if yes, it will add it to dictionary and function will return the edge_map so the pages and elements that are repeating
* find_furniture_texts: filters the edge map and return a set of normalized text fingerprints that appear on at least as many pages as required threshold.

# cleaner.py
First it generate a report from above functions. Then it is again goigh through all elements and check if it is repeating or if it is on the edge. If yes it will add it into remove list, otherwise will keep it.
It will also generate a report out of it, so we will exactly know why it was removed.

uv run ruff check and uv run pytest all pass.


## NOTE: We are still running cleaning only on text. For images, tables etc. will be added later

# scripts
## clean_document.py
It is calling all functions from docgraph/ingestion/cleaning and store the results