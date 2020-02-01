def scrape():
    from splinter import Browser
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import requests

    try:
        browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

        date = '03/27/2020'
        start = 'BNA'
        end = 'JFK'

        url_expedia = 'https://www.expedia.com/Flights-Search?flight-type=on&starDate='+date+'&mode=search&trip=oneway&leg1=from:'+start+',to:'+end+',departure:'+date+'TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y'

        browser.get(url_expedia)
    
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
                layover_apt.append('none')
                arrive_apt.append(item[-1].split(' ')[-1])

        results_dict={}
        results_dict['model']=model
        results_dict['airline']=airline
        results_dict['depart_time']=depart
        results_dict['arrive_time']=arrive
        results_dict['duration']=duration
        results_dict['no_stops']=no_stops
        results_dict['price']=price
        results_dict['layover']=layover
        results_dict['depart_airport']=depart_apt
        results_dict['arrive_airport']=arrive_apt
        results_dict['layover_airport']=layover_apt

        browser.quit()
        print(results_dict)
        return(results_dict)
    except(IndexError):
        pass

scrape()