from .site import Site
from splinter import Browser
from typing import Optional


class OfferUp(Site):
    def __init__(self, min: Optional[int] = 0, max: Optional[int] = None, distance: Optional[int] = 30) -> None:
        super().__init__(min, max, distance)
        
    def buildURL(self) -> str:
        pass
    
    def scrape(self) -> None:
        pass
    
# https://offerup.com
# /search?cid=7&v2_category_id=7&q=surfboards&source=autocomplete&
# PRICE_MIN=0&PRICE_MAX=200&SORT=price&DISTANCE=30&DELIVERY_FLAGS=p
#
# has min, max, distance, delivery params