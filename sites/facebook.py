from .site import Site
from typing import Optional
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import time


class Facebook(Site):
    def __init__(self, min: Optional[int] = 0, max: Optional[int] = 200, distance: Optional[int] = 30) -> None:
        super().__init__(min, max, distance)
        
    def buildURL(self) -> str:
        # base url
        b_url = "https://www.facebook.com/marketplace/113468615330042/search?"
        
        # url + parameter setup
        url = f"{b_url}minPrice={self.min}&maxPrice={self.max}&query=surfboards&exact=false"
        
        return url
    
    def scrape(self) -> None:
        b = self.get_browser()
        b.visit(self.buildURL())
        
        if b.is_element_present_by_css('div[aria-label="Close"]', wait_time=100):
            # Click on the element once it's found
            b.find_by_css('div[aria-label="Close"]').first.click()
        
        # scroll to gather more html on screen
        scroll_count = 4
        for i in range(scroll_count):
            b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(rand.uniform(1.5,2.5))
            time.sleep(10)
            
        # parse the html
        html = b.html
        market_soup = soup(html, 'html.parser')
            
        # close the browser
        b.quit()

        # extract data and insert into lists
        # titles
        titles_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
        titles_list = [title.text.strip() for title in titles_div]

        # prices
        prices_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
        prices_list = [price.text.strip() for price in prices_div]
        for i, price in enumerate(prices_list):
            if price == "Free":
                prices_list[i] = "$0"

        # locations
        loc_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84")
        loc_list = [loc.text.strip() for loc in loc_div]
        loc_list = loc_list[:-2]

        # urls
        url_div = market_soup.find_all('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv")
        url_list = [url.get('href') for url in url_div]


        num = len(prices_list)
        pattern = r'[$,]'

        if num != len(titles_list) or num != len(loc_list) or num != len(url_list):
            print("prices_list length: " + str(len(prices_list)))
            print("titles_list length: " + str(len(titles_list)))
            print("loc_list length: " + str(len(loc_list)))
            print("url_list length: " + str(len(url_list)))
            
            print(prices_list)
            print("\n**************************************************************************************************************\n")
            print(titles_list)
            print("\n**************************************************************************************************************\n")
            print(loc_list)
            print("\n**************************************************************************************************************\n")
            print()

        else:
            listings = []
            for i, item in enumerate(titles_list):
                surf_dict = {}
                surf_dict["Title"] = item # can change this to just 'item' ?
                surf_dict["Price"] = int(re.sub(pattern, '', prices_list[i]))
                surf_dict["Location"] = loc_list[i]
                surf_dict["URL"] = url_list[i]
                
                listings.append(surf_dict)
                
            listings_df = pd.DataFrame(listings)
            listings_df["URL"] = 'https://www.facebook.com/' +  listings_df["URL"]
            
            sorted_df = listings_df.sort_values(by="Price", ascending=True)
            sorted_df.to_csv('surf.csv', index=False)
            
            print(listings_df)