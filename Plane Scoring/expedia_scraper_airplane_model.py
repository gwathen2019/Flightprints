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
    airline = []
    depart = []
    arrive = []
    duration = []
    no_stops = []
    depart_arrival = []
    price = []
    layover = []
    depart_apt = []
    arrive_apt = []
    layover_apt = []

    for i in range(1,6):
        dropdown_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[2]/span[1]/a/span[4]')[0]
        browser.execute_script("arguments[0].click();", dropdown_element)
        model_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[3]/div[2]/div/section/div/div[1]/ul/li[5]')[0]
        model.append(model_element.text) 
        airline_id_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[1]/div[1]/div/div/div/div[1]/div[2]/span')[0]
        airline.append(airline_id_element.text)
        depart_time_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[1]/div[1]/div/div/div/div[1]/div[1]/span/span[1]')[0]
        depart.append(depart_time_element.text)
        arrive_time_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[1]/div[1]/div/div/div/div[1]/div[1]/span/span[4]')[0]
        arrive.append(arrive_time_element.text)
        duration_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[1]/div[1]/div/div/div/div[2]/div[1]/span[1]')[0]
        duration.append(duration_element.text)
        no_stops_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[1]/div[1]/div/div/div/div[2]/div[1]/span[2]')[0]
        no_stops.append(no_stops_element.text)
        depart_arrival_apt_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[1]/div[1]/div/div/div/div[2]/div[2]')[0]
        depart_arrival.append(depart_arrival_apt_element.text)
        price_element = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul/li['+str(i)+']/div[1]/div[1]/div[2]/div/div[1]/div[1]/span')[0]
        price.append(price_element.text)

    for i in range(0,len(model)):
        item = model[i].split(" |")
        model[i] = item[0]
    
    for i in range(0,len(depart_arrival)):
        item = depart_arrival[i].split("\n")
        if len(item) > 4:
            layover.append(True)
            depart_apt.append(item[1].split(' ')[0])
            layover_apt.append(item[2].split(' ')[-1])
            arrive_apt.append(item[-1].split(' ')[-1])
        else:
            layover.append(False)
            depart_apt.append(item[1].split(' ')[0])
            arrive_apt.append(item[-1].split(' ')[-1])
            
        print(layover)

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
    browser.quit()
    # return(results_dict)

scrape()