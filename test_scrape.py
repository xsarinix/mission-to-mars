import pymongo
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import numpy as np
import time
import datetime

def scrape():
    scrape_dict = {}

    # Update dictionary with scrape time
    scrape_dict["scrape_time"] = str(datetime.datetime.now())

    # Get most current news story from NASA's mars site
    nasa_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    nasa_html = requests.get(nasa_news_url).text
    nasa_soup = bs(nasa_html, 'lxml')
    # Get first title
    title_results = nasa_soup.find_all('div', class_="content_title")
    title_list = []
    for result in title_results:
        try:
            title = result.find('a').text.strip()
            if title:
                title_list.append(title)
        except Exception as e:
            return e
    news_title = title_list[0]
    # Get first paragraph
    p_results = nasa_soup.find_all('div', class_="rollover_description_inner")
    p_list = []
    for p in p_results:
        try:
            par = p.text.strip()
            if par:
                p_list.append(par)
        except Exception as e:
            return e
    news_p = p_list[0]
    # Update dictionary
    scrape_dict["mars_news_title"] = news_title
    scrape_dict["mars_news_p"] = news_p

    return scrape_dict


    
