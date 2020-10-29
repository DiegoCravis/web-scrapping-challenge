from bs4 import BeautifulSoup
import requests
import pymongo
import os
from splinter import Browser
import pandas as pd

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA MARS NEWS
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_titles = soup.find_all('div', class_='content_title', limit = (2))
    news_title = news_titles[1].text
    news_p = (soup.find('div', class_='article_teaser_body')).text

    #JPL Mars Space Images - Featured Image
    url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url1)
    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')


    featured_image = soup1.find("article", class_='carousel_item')
    featured_image_url= featured_image["style"]
    featured_image_url= featured_image_url.split("'")[1]


    #Mars Weather
    url2 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    mars_weather = soup2.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

    # Mars Facts

    url3 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url3)
    df = tables[0]
    df.columns = ['Title', 'Data']
    html_table = df.to_html()

    # Mars Hemispheres
    url3 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    hemisphere_image = soup3.find_all('div', class_='item')
    title_lt = []
    img_lt = []
    hemisphere_image_urls = []
    for div in hemisphere_image:
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
        img_url = div.find('img')
        img_url = img_url ['src']
        title = div.find('h3').text
        img_lt.append(img_url)
        title_lt.append(title)
        
        
        hemisphere_image_url = {
                    'title': title,
                    'img_url': img_url
                }
        hemisphere_image_urls.append(hemisphere_image_url)

    print(hemisphere_image_urls)

data = {"news_title":news_title,"news_article":news_p,"featured_image_url":featured_image_url,"mars_weather":mars_weather,"Facts":html_table,"Hemispheres":hemisphere_image_urls}
