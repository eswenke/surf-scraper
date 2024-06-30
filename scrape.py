from splinter import Browser
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
# import matplotlib.pyplot as plt ...  NEED TO DO SOME DOWNLOAD/UPDATING OR SOMETHING
import time
import random as rand

# set up splinter
b = Browser('chrome', user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# base url
b_url = "https://www.facebook.com/marketplace/113468615330042/search?"

# parameters
minPrice = 0
maxPrice = 200

# params = f"minPrice={}&maxPrice={}&query=surfboards&exact=false"