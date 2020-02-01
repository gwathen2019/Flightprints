def scrape():
    from splinter import Browser
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import requests

    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    date = '03/27/2020'
    start = 'BNA'
    end = 'JFK'
    # Get news data
    url_expedia = 'https://www.expedia.com/Flights-Search?flight-type=on&starDate='+date+'&mode=search&trip=oneway&leg1=from:'+start+',to:'+end+',departure:'+date+'TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y'

    browser.get(url_expedia)
   
    # WORKS
    # dropdown_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li[1]/div[1]/div[2]/span[1]/a/span[4]')[0]
    # browser.execute_script("arguments[0].click();", dropdown_element)
    # list_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li[1]/div[1]/div[3]/div[2]/div/section/div/div[1]/ul/li[5]')[0]
    # model = list_element.text                   
    # print(model)
    model = []

    for i in range(1,6):
        dropdown_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[2]/span[1]/a/span[4]')[0]
        browser.execute_script("arguments[0].click();", dropdown_element)
        list_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[3]/div[2]/div/section/div/div[1]/ul/li[5]')[0]
        model.append(list_element.text)      
        print(i)          
        print(model)

    for i in range(0,len(model)):
        item = model[i].split(" |")
        model[i] = item[0]
    
    print(model)

    # for image in images:
    #     #print(image['href'])
    #     browser.visit('https://astrogeology.usgs.gov'+str(image['href']))
        
    #     # HTML object
    #     html = browser.html
    #     # Parse HTML with Beautiful Soup
    #     soup = BeautifulSoup(html, 'html.parser')
        
    #     image_url = soup.find('div',class_='downloads').ul.li.a['href']
    #     image_title = soup.find('h2',class_='title').text
    #     hemisphere_image_urls_dict['title']=image_title
    #     hemisphere_image_urls_dict['img_url']=image_url
        
    #     hemisphere_image_urls.append(hemisphere_image_urls_dict)
    #     hemisphere_image_urls_dict = {}

    # results_dict={}
    # results_dict['news_title']=news_title
    # results_dict['news_p']=news_p
    # results_dict['featured_image_url']=featured_image_url
    # results_dict['mars_weather']=mars_weather
    # results_dict['html_table']=html_table
    # results_dict['hemisphere_image_urls']=hemisphere_image_urls
    # browser.quit()
    # return(results_dict)


import os 
import sys

scrape()