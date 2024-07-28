from splinter import Browser
from typing import Optional


class Site:
    b = Browser('chrome', user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

    def __init__(self, min: Optional[int] = 0, max: Optional[int] = None, distance: Optional[int] = 30) -> None:
        self.min = min
        self.max = max
        self.distance = distance
        
    def scrape(self) -> None:
        raise NotImplementedError("Subclass must implement this method!")
    
    def get_browser(self):
        return self.b
    
    # goal: depending on what parameters are given to which sites, figure out how to build the correct URL
    # goal: once URL building is working, then the scrape method will actually open the site, get and clean the data,
    # and store it somewhere