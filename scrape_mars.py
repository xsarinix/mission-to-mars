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

    # Create splinter browser instance
    executable_path = {'executable_path':'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    # Scrape NASA images page for featured image
    nasa_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_images_url)
    browser.find_by_css('.button').first.click()
    time.sleep(3)
    browser.find_by_css('.button').last.click()
    partial_link = browser.find_by_css('.download_tiff').last.value.split(" ")[2]
    browser.click_link_by_partial_href(partial_link)
    featured_image_url = browser.url
    # Update dictionary
    scrape_dict["featured_image"] = featured_image_url

    # Use Splinter to scrape USGS for hemisphere images and urls
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    link_objects = browser.find_by_css('h3')
    hemisphere_list = []
    {hemisphere_list.append(link.value.replace(" Enhanced","")) for link in link_objects}
    url_list = []
    for hemisphere in hemisphere_list:
        browser.click_link_by_partial_text(hemisphere)
        image_object = browser.find_by_css('img.wide-image')
        img_url = image_object['src']
        url_list.append(img_url)
        browser.back()
    browser.quit()
    hemisphere_image_urls = []
    for hemisphere, url in zip(hemisphere_list, url_list):
        hemisphere_dict = {"title": hemisphere, "url": url}
        hemisphere_image_urls.append(hemisphere_dict)
    hemisphere_image_urls
    # Update dictionary
    scrape_dict["hemisphere_images"] = hemisphere_image_urls
    
    # Scrape weather conditions from Mars Weather Twitter
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    twitter_html = requests.get(twitter_url).text
    twitter_soup = bs(twitter_html, 'lxml')
    tweets = twitter_soup.find_all('div', class_ = "content")
    weather_only_tweets = []
    for tweet in tweets:
        username = tweet.find('span', class_ = "username u-dir u-textTruncate")
        pic_link = tweet.find('a', class_="twitter-timeline-link u-hidden")
        if username.text == "@MarsWxReport":
            tweet_content = tweet.find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
            # Eliminate non-weather tweets
            report_test = tweet_content.split(" ")
            if report_test[0] == "Sol":
                if pic_link is not None:
                    weather_only_tweets.append(tweet_content.replace(pic_link.text, ""))
                else:
                    weather_only_tweets.append(tweet_content)
    mars_weather = weather_only_tweets[0]
    # Update dictionary
    scrape_dict["mars_weather"] = mars_weather
    
    # Scrape facts table
    facts_url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[0]
    facts_df=facts_df.set_index(0)
    facts_html = facts_df.to_html(classes="table table-format", border=0, header = False, index_names=False).replace("\n", "")
    # Update dictionary
    scrape_dict["mars_facts"] = facts_html
    
    return scrape_dict


    
