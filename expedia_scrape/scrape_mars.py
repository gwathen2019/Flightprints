from bs4 import BeautifulSoup as bs
import requests
import splinter
from splinter import Browser
import os
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'c:/users/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    #listings = {}

    #URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    #open splinter browser
    browser.visit(url)
    
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')
    
    #look for latest news titles
    result1 = soup.find_all('div', class_='content_title')
    news_title = []
    # Loop through returned results
    for result in result1:
        news_title.append(result.a.text)
    news_title[0]

    #look for latest news teaser narrative
    result2 = soup.find_all('div', class_='article_teaser_body')
    news_p = []
    # Loop through returned results
    for result in result2:
        news_p.append(result.text)
    news_p[0]

    #JPL Mars Space Featured Image

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    soup = bs(browser.html, 'html.parser')
    #find tag with featured image
    div_tag = soup.find('a', class_='button fancybox')

    #create link to access featured image
    image_link = "https://jpl.nasa.gov" + str(div_tag['data-link'])
    #image_link

    url3 = image_link
    browser.visit(url3)
    soup = bs(browser.html, 'html.parser')

    figure = soup.find_all('figure')
    figure
    image = soup.figure.a
    #image['href']

    featured_image_url = "https://jpl.nasa.gov" + str(image['href'])
    #featured_image_url

    #Mars Weather
    url4 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url4)
    soup = bs(browser.html, 'html.parser')

    mars_tweet = soup.find('div', class_="js-tweet-text-container")
    mars_weather = mars_tweet.p.text
    #mars_weather

    #Mars Facts
    url5 = 'https://space-facts.com/mars/'
    browser.visit(url5)
    soup = bs(browser.html, 'html.parser')

    tables = pd.read_html(url5)
    df = tables[0]
    df.columns = ['description', 'value']

    mars_facts_table = df.to_html()
    #mars_facts_table

    #Mars Hemisphere Images
    url6 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url6)
    soup = bs(browser.html, 'html.parser')
    cerberus_image = soup.find('img', class_="wide-image")

    cerberus_image_url = "https://astrogeology.usgs.gov" + str(cerberus_image['src'])
    #cerberus_image_url

    url7 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url7)
    soup = bs(browser.html, 'html.parser')
    schiaparelli_image = soup.find('img', class_="wide-image")

    schiaparelli_image_url = "https://astrogeology.usgs.gov" + str(schiaparelli_image['src'])
    #schiaparelli_image_url

    url8 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url8)
    soup = bs(browser.html, 'html.parser')
    syrtis_major_image = soup.find('img', class_="wide-image")

    syrtis_major_image_url = "https://astrogeology.usgs.gov" + str(syrtis_major_image['src'])
    #syrtis_major_image_url

    url9 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url9)
    soup = bs(browser.html, 'html.parser')
    valles_marineris_image = soup.find('img', class_="wide-image")

    valles_marineris_image_url = "https://astrogeology.usgs.gov" + str(valles_marineris_image['src'])
    #valles_marineris_image_url

    hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere", "img_url": cerberus_image_url},
    {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli_image_url},
    {"title": "Syrtis Major Hemisphere", "img_url": syrtis_major_image_url},
    {"title": "Valles Marineris Hemisphere", "img_url": valles_marineris_image_url}, 
    ]
    #hemisphere_image_urls

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title[0],
        "news_p": news_p[0],
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_table,
        "hemisphere_images": hemisphere_image_urls,
        "cerberus_image": cerberus_image_url,
        "schiaparelli_image": schiaparelli_image_url,
        "syrtis_major_image": syrtis_major_image_url,
        "valles_marineris_image": valles_marineris_image_url

    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data