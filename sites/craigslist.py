from .site import Site
from typing import Optional
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import time


class CraigsList(Site):
    def __init__(self, min: Optional[int] = 0, max: Optional[int] = None, distance: Optional[int] = 30) -> None:
        super().__init__(min, max, distance)
        
    def buildURL(self) -> str:
        pass
    
    def scrape(self) -> None:
        b = self.get_browser()
        b.visit(self.buildURL())
        
# https://slo.craigslist.org
# /search/sss?max_price=200&min_price=0&postal=93405&query=surfboards&search_distance=30#search=1~gallery~0~0
#
# needs a {city} parameter for {}.craiglist.org
# the last number in the link signifies how many listings are loaded (basically)
# also max, min, distance (from a given zip code) and many others