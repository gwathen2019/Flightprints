from flask import Flask, render_template,redirect,request
from expedia_scraper_master_windows import scrape
import json
import pymongo
import datetime
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
    if info.count() > 0:       
        return render_template('index.html',info=info[0])
    else:
        return render_template('index.html')


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

        output = scrape(origin,destination,date)

        # Add scrape data to mongo
        collection.update({},output,upsert=True)

        # Generate just a boring response
        #return 'The origin is %s' % (origin) 
        return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=56575, debug=True)