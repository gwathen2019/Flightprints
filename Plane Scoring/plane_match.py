from fuzzywuzzy import fuzz
import pandas as pd 

distance = 665
plane_model = 'Boeing 737'

if distance < 684:
    table = './regional_tables'
elif distance <1000:
    table = './short_tables'
elif distance <3400:
    table = './medium_tables'
else:
    table = './long_tables'

# commuter_max = 300
# regional_min = 500
# regional_max = 684
# short_max = 1000
# medium_min = 1750
# medium_max = 3400
# long_min = 4650
# long_max = 7200


df = pd.read_csv(table)

txt_to_find = plane_model.split()
matched_df=df[df['Model'].str.contains(plane_model)]

if len(matched_df)==0:
    matched_df=df[df['Model'].str.contains(txt_to_find[0])]
    

#print(matched_df)

def get_ratio(row):
    name = plane_model
    name1 = row['Model']
    return fuzz.token_set_ratio(name, name1)

matched_df['Fuzz Score'] = matched_df.apply(get_ratio, axis=1)

closest_match = matched_df[matched_df['Fuzz Score']==matched_df['Fuzz Score'].max()]

if len(closest_match) > 1:
    closest_match = closest_match[closest_match['CO2 per mi']==closest_match['CO2 per mi'].max()]


print(closest_match)