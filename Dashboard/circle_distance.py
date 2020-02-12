def distance_finder(stops):
    import pandas as pd 

    #stops = ['JFK','BOS','BNA']

    # GCMap URL
    url1 = 'http://www.gcmap.com/dist?P='
    url2 = '&DU=nm&DM=&SG=&SU=nmph'


    if len(stops) < 3:    
        start = stops[0]
        end = stops[1]

        route = start + '-' + end

        url = url1 + route + url2

        tables = pd.read_html(url)

        dist_txt = tables[1]['Distance'][0]
        dist = dist_txt.split()
        dist_list = [dist[0]]
        #print(dist_list)
        distance = int(dist_list[0].replace(',',''))
    else:
        for i in range(0,len(stops)):
            if i == 0:
                route = stops[i]
            else:
                route = route + "-" + stops[i]

        url = url1 + route + url2

        tables = pd.read_html(url)

        dist_list = []
        for i in range(1,len(stops)):
            dist_txt = str(tables[1]['Distance'][i])
            dist = dist_txt.split()
            dist_list.append(int(dist[0].replace(',','')))
        #print(dist_list)
        distance = sum(dist_list)


    return(distance)
   
