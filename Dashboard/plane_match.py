def match_plane(distance,plane_model):
    from fuzzywuzzy import fuzz
    import pandas as pd 

    #distance = 665
    #plane_model = 'Boeing 737'

    # if distance < 684:
    #     table = 'static/data/regional_tables.csv'
    if distance <1000:
        table = 'static/data/short_tables.csv'
    elif distance <3400:
        table = 'static/data/medium_tables.csv'
    else:
        table = 'static/data/long_tables.csv'

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
    matched_df=df[df['model'].str.contains(plane_model)]

    if len(matched_df)==0:
        matched_df=df[df['model'].str.contains(txt_to_find[0])]
        

    #print(matched_df)

    def get_ratio(row):
        name = plane_model
        name1 = row['model']
        return fuzz.token_set_ratio(name, name1)

    
    matched_df['Fuzz Score'] = matched_df.apply(get_ratio, axis=1)

    closest_match = matched_df[matched_df['Fuzz Score']==matched_df['Fuzz Score'].max()]

    if len(closest_match) > 1:
        closest_match = closest_match[closest_match['co2_mi']==closest_match['co2_mi'].max()]


    #closest_match = closest_match()
    #print(closest_match['model'].item())
    return([closest_match['model'].item(),closest_match['co2_mi'].item()])

def find_score(matched_plane,matched_co2):
    import pandas as pd 

    df = pd.read_csv('static/data/master_scored_ML.csv')

    plane_data = df[df['Model']==matched_plane]
    #matched_co2 = 
    fully_matched = df[df['CO2 per mi'].round(2)==round(matched_co2,2)]
    #print(plane_data,fully_matched)
    return([fully_matched['Score'].item(),fully_matched['CO2 per mi per seat'].item()])
#get_score('Airbus A320',32.296897200000004)
#match_plane(900,'Airbus A320')