#Importing packages
#from selenium import webbrowser
import pandas as pd
import requests
import splinter
from splinter import Browser

executable_path = {'executable_path': '/usr/local/bin/chromebrowser'}
browser = Browser('chrome', **executable_path, headless=False)

date = '03/27/2020'
start = 'BNA'
end = 'JFK'
# Get news data
url_expedia = 'https://www.expedia.com/Flights-Search?flight-type=on&starDate='+date+'&mode=search&trip=oneway&leg1=from:'+start+',to:'+end+',departure:'+date+'TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y'

browser.get(url_expedia)

userid_element = browser.find_elements_by_xpath('//*[@id="section-offer-leg0-details"]/div/div[1]/ul/li[5]')
#/html/body/div[2]/div[8]/section/div/div[10]/ul
#//*[@id="section-offer-leg0-details"]/div/div[1]/ul/li[5]/text()
userid = userid_element.text
print(userid)

# flights = pd.DataFrame(columns = ['Date','Airline','Depart_time', 'Arr_time', 'No_stops', 'Depart_apt', 'Arr_apt', 'Price']) 

# ids = browser.find_elements_by_xpath('/html/body/div[2]/div[8]/section/div/div[10]/ul')[0]
# flight_ids = []
# for i in ids:
#     flight_ids.append(i.get_attribute('id'))

# for x in flight_ids:
#     #Extract dates from for each user on a page
#     user_date = browser.find_elements_by_xpath('//*[@id="' + x +'"]/div/div[2]/div[2]/span[1]/a/time')[0]
#     date = user_date.get_attribute('title')

#     #Extract user ids from each user on a page
#     userid_element = browser.find_elements_by_xpath('//*[@id="' + x +'"]/div/div[2]/div[1]/span[1]/a[2]')[0]
#     userid = userid_element.text

#     #Extract Message for each user on a page
#     user_message = browser.find_elements_by_xpath('//*[@id="' + x +'"]/div/div[3]/div/div[1]')[0]
#     comment = user_message.text
                                   
#     #Adding date, userid and comment for each user in a dataframe    
#     comments.loc[len(comments)] = [date,userid,comment]