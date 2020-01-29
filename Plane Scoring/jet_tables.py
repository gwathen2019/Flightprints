# import requests
# from bs4 import BeautifulSoup as bs

# website_url = requests.get('https://en.wikipedia.org/wiki/Fuel_economy_in_aircraft').text


# soup = bs(website_url,'lxml')
# #print(soup.prettify())

# My_table = soup.find('table',{'class':'wikitable sortable'})
# print(My_table)


import pandas as pd 

# Wikipedia URL
url = 'https://en.wikipedia.org/wiki/Fuel_economy_in_aircraft'

tables = pd.read_html(url)

# Create tables from scrape and give columns names
commuter_tables_df = tables[0]
regional_tables_df = tables[1]
short_tables_df = tables[2]
medium_tables_df = tables[3]
long_tables_df = tables[4]

commuter_tables_df.columns = ['Model','First flight','Seats','Fuel burn','Fuel per seat']
regional_tables_df.columns = ['Model','First flight','Seats','Sector','Fuel burn','Fuel per seat']
short_tables_df.columns = ['Model','First flight','Seats','Fuel burn','Fuel per seat']
medium_tables_df.columns = ['Model','First flight','Seats','Sector','Fuel burn','Fuel per seat']
long_tables_df.columns = ['Model','First flight','Seats','Sector','Fuel burn','Fuel per seat']

tables = [commuter_tables_df,regional_tables_df,short_tables_df,medium_tables_df,long_tables_df]

commuter_max = 300
regional_min = 500
regional_max = 684
short_max = 1000
medium_min = 1750
medium_max = 3400
long_min = 4650
long_max = 7200

ranges = [commuter_max,regional_max,short_max,medium_max,long_max]

# Carbon output calculation
def carbon_calc(gpm):
    # Using the density of dodecane (2,839.06 g / gal), we can calculate our average fuel economy
    # Weighted average capacity and fuel efficiency in grams of dodecane per mile:
    fuel_economy = gpm * 2839.06
    # Given that 1 gram of dodecane produces 3.1 grams of carbon dioxide, we can calculate how much 
    # carbon dioxide an average plane produces to fly one mile in the air:
    co2 = fuel_economy * 3.096 * (1/453.59)
    # In lbs/mi
    return(co2)


# Calculate CO2 per mile and per seat for each table
for i in range(0,len(tables)):
    co2_per_mi_per_seat = []
    co2_per_mi = []
    for j in range(0,len(tables[i]['Fuel per seat'])):    
        txt = tables[i]['Fuel per seat'][j]
        x = txt.split()
        y=x[3].split('(')
        mpg = y[1]
        gpm = 1/float(mpg)
        co2_seat = carbon_calc(gpm)
        co2 = co2_seat * tables[i]['Seats'][j]
        co2_per_mi_per_seat.append(co2_seat)
        co2_per_mi.append(co2)

    tables[i]["CO2 per mi per seat"] = co2_per_mi_per_seat
    tables[i]["CO2 per mi"] = co2_per_mi


# Dataframes to CSVs
commuter_tables_df.to_csv('commuter_tables.csv',index=False)
regional_tables_df.to_csv('regional_tables.csv',index=False)
short_tables_df.to_csv('short_tables.csv',index=False)
medium_tables_df.to_csv('medium_tables.csv',index=False)
long_tables_df.to_csv('long_tables.csv',index=False)

print(len(commuter_tables_df)+len(regional_tables_df)+len(short_tables_df)+len(medium_tables_df)+len(long_tables_df))

# for i in range(0,len(tables)):
#     print('Min:')
#     print(tables[i]["CO2 per mi per seat"].min())
#     print('Max:')
#     print(tables[i]["CO2 per mi per seat"].max())

# Range is 0.18042959328441344 to 0.5412887798532404
# .036 increments?


# Master CSV with added column for max range
for i in range(0,len(tables)):
    tables[i]['Max Range'] = ranges[i]
    if i == 0:
        master_df = tables[i]
    else:
        master_df = master_df.append(tables[i])
        print('appending')

master_df.to_csv('master.csv',index=False)
