from .site import Site
from typing import Optional
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import time

# OFFERUP CHANGES CLASS NAMES basically each time you open up and search for anything
# utilize their api and try to reverse it like with insomia / postman (CHECK NOTES)
# maybe utilize regex? try the api though, that seems to be the logical and more interesting next step

class OfferUp(Site):
    def __init__(self, min: Optional[int] = 0, max: Optional[int] = None, distance: Optional[int] = 30) -> None:
        super().__init__(min, max, distance)
        
    def buildURL(self) -> str:
        # base url
        b_url = "https://offerup.com/search?cid=7&v2_category_id=7&q=surfboards&source=autocomplete&"
        
        # url + parameter setup
        # has min, max, distance, delivery params
        url = f"{b_url}PRICE_MIN={self.min}&PRICE_MAX={self.max}&SORT=price&DISTANCE=30&DELIVERY_FLAGS=p"
        print(url)
        
        return url
    
    def scrape(self) -> None:
        b = self.get_browser()
        b.visit(self.buildURL())
    
        # scroll to gather more html on screen
        scroll_count = 1
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
        titles_div = market_soup.find_all('span', class_="MuiTypography-root {} MuiTypography-subtitle1 MuiTypography-colorTextPrimary MuiTypography-noWrap MuiTypography-alignLeft")
        titles_list = [title.text.strip() for title in titles_div]
        
        # MuiTypography-root jss467 MuiTypography-subtitle1 MuiTypography-colorTextPrimary MuiTypography-noWrap MuiTypography-alignLeft
    
        # prices
        prices_div = market_soup.find_all('span', class_="MuiTypography-root {} MuiTypography-body1 MuiTypography-colorTextPrimary MuiTypography-noWrap MuiTypography-alignLeft")
        prices_list = [price.text.strip() for price in prices_div]
        for i, price in enumerate(prices_list):
            if price == "Free":
                prices_list[i] = "$0"

        # locations
        loc_div = market_soup.find_all('span', class_="MuiTypography-root MuiTypography-body2 MuiTypography-colorTextSecondary MuiTypography-noWrap MuiTypography-alignLeft")
        loc_list = [loc.text.strip() for loc in loc_div]
        loc_list = loc_list[:-2]

        # urls
        url_div = market_soup.find_all('a', class_="{}")
        url_list = [url.get('href') for url in url_div]


        num = len(prices_list)
        pattern = r'[$,]'
        
        if num != len(titles_list) or num != len(loc_list) or num != len(url_list):
            print("prices_list length: " + str(len(prices_list)))
            print("titles_list length: " + str(len(titles_list)))
            print("loc_list length: " + str(len(loc_list)))
            print("url_list length: " + str(len(url_list)))
            print()
            
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
                surf_dict["Title"] = item 
                surf_dict["Price"] = int(re.sub(pattern, '', prices_list[i]))
                surf_dict["Location"] = loc_list[i]
                surf_dict["URL"] = url_list[i]
                
                listings.append(surf_dict)
                
            listings_df = pd.DataFrame(listings)
            # listings_df["URL"] = 'https://www.facebook.com/' +  listings_df["URL"]
            
            sorted_df = listings_df.sort_values(by="Price", ascending=True)
            sorted_df.to_csv('surf.csv', index=False)
            
            print(listings_df)