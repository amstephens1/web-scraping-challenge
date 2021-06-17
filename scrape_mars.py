from bs4 import BeautifulSoup 
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import pandas as pd
import pymongo

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dict= {}

    url = 'https://redplanetscience.com/#'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    img_html = browser.html
    image_soup = BeautifulSoup(img_html, 'html.parser')
    relative_image_path = image_soup.find_all('img')[1]["src"]
    featured_image_url = jpl_url + relative_image_path

    fact_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(fact_url)
    mars_df = tables[1]
    mars_df.columns = ["Profile", "Value"]
    mars_df.set_index('Profile', inplace=True)
    html_table = mars_df.to_html()
    html_table.replace('\n', '')

    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    four_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    hemisphere_item = four_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []
    for mars in hemisphere_item:
        hemisphere = mars.find('div', class_='description')
        title = hemisphere.h3.text
        
        hemisphere_section = hemisphere.a['href']
        browser.visit(hemispheres_url + hemisphere_section)
        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        
        image_dict = {}
        image_dict['title'] = title
        image_dict['pic_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)

    mars_dict={
        "news_title": news_title,
        "news_p": news_p,
        "featured__image_url": featured_image_url,
        "mars_facts": str(html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    browser.quit()
    return mars_dict
