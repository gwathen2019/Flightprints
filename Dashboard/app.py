from flask import Flask, render_template,redirect,request
from expedia_scraper_master_windows import scrape
from circle_distance import distance_finder
from plane_match import match_plane, find_score
import json
import pymongo
import datetime
from time import sleep

# Create an instance of our Flask app.
app = Flask(__name__, template_folder = "templates")

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.flights_db
collection = db.flights
#Drops collection if available to remove duplicates
db.flights.drop()

#################################################
# Flask Routes
#################################################

@app.route('/',methods=['GET', 'POST'])
def index():
    info = db.flights.find()
    print(info.count())
    if info.count() == 0:  
        return render_template('index.html')
    else:
        return render_template('index.html',info=info[0], score=info[2])
        #return render_template('index.html',info=info)


@app.route("/scrape",methods=['GET', 'POST'])
def scrape_data():
    if request.method == 'POST':   
        # Then get the data from the form
        tag = request.form
        #origin, destination, date = tag_lookup(tag)
        print(tag)
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%y')
        #try:
            #output = scrape(origin,destination,date)
        info = db.flights.find()
        while info.count() == 0:
            try:
                output = scrape(origin,destination,date)                
                collection.update({},output,upsert=True)
                info = db.flights.find()
            except:
                pass
        info = db.flights.find()
        while info.count() < 2:
            try:
                print(info.count())
                print("running circle dist")
                circle_distance()
                print("running score")
                get_score()
                info = db.flights.find()
            except:
                pass
            #output = scrape()
            # while output is None:
            #     print('passing')
            #     sleep(5)
            #     pass
            # Add scrape data to mongo
            #collection.update({},output,upsert=True)
            # circle_distance()
            # get_score()
        #except:
         #   pass
        # Generate just a boring response
        #return 'The origin is %s' % (origin) 
        return redirect("/")
    else:
        try:
            output = scrape('BNA','BOS','03/01/2020')
            collection.update({},output,upsert=True)
            circle_distance()
            get_score()
        except:
            pass
        return redirect("/")

@app.route("/distance",methods=['GET', 'POST'])
def circle_distance():
    print("in circle dist")
    info = db.flights.find()[0]
    routes = []
    #print(info['depart_airport'])
    for i in range(0,len(info['depart_airport'])):
        if info['layover_airport'][i] == 'none':
            stops = [info['depart_airport'][i],info['arrive_airport'][i]]
        else:
            stops = [info['depart_airport'][i],info['layover_airport'][i],info['arrive_airport'][i]]
        #print(stops)
        routes.append(stops)
    distance = {}
    distances = []
    for i in range(0,len(routes)):
        #print('in for loop')
        output = distance_finder(routes[i])
        #print(output)
        distances.append(output)
    distance['flight_distance'] = distances
    print(distances)
    collection.insert(distance)
    return redirect("/")

@app.route("/score",methods=['GET', 'POST'])
def get_score():
    dist_info = db.flights.find()[1]
    flight_info = db.flights.find()[0]
    scores = []
    cos = []
    offsets = []
    paid_offsets = []
    results_dict = {}
    #info = db.flights.find()[1]
    for i in range(0,len(flight_info['model'])):
        try:
        
            dist = dist_info['flight_distance'][i]
            name = flight_info['model'][i]
            model_match = match_plane(dist,name)
            model = model_match[0]
            co2_mi = model_match[1]

            score_co = find_score(model,co2_mi)
            score = round(score_co[0],2)
            scores.append(score)
            co2_mi_seat = score_co[1]
            cos.append(co2_mi_seat)
            offset = round((dist*co2_mi_seat),2)
            offsets.append(offset)
            paid_offset = round((dist*co2_mi_seat)/1000,2)
            paid_offsets.append(paid_offset)

        except(ValueError):
            dist = dist_info['flight_distance'][i]
            model = flight_info['model'][i]
            co2_mi_seat = 0.220206117258477
            cos.append(co2_mi_seat)
            score = round(8.322955080213202,2)
            scores.append(score)
            offset = round((dist*co2_mi_seat),2)
            offsets.append(offset)
            paid_offset = round((dist*co2_mi_seat)/1000,2)
            paid_offsets.append(paid_offset)
            pass
    results_dict['score'] = scores
    results_dict['co2_mi_seat']=cos
    results_dict['offset'] = offsets
    results_dict['paid_offset'] = paid_offsets
    collection.insert(results_dict)    
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=56575, debug=True)