from flask import Flask, render_template,redirect
from expedia_scraper_master_windows import scrape
import json
# Create an instance of our Flask app.
app = Flask(__name__, template_folder = "templates")


#################################################
# Flask Routes
#################################################

@app.route('/')
def index():
    output = scrape()
    model = output['model']
    airline = output['airline']
    depart = output['depart_time']
    arrive = output['arrive_time']
    duration = output['duration']
    no_stops = output['no_stops']
    price = output['price']
    layover = output['layover']
    depart_apt = output['depart_airport']
    arrive_apt = output['arrive_airport']
    layover_apt = output['layover_airport']
    return render_template('index.html', model=model,airline=airline,depart=depart,arrive=arrive,duration=duration,no_stops=no_stops,price=price,layover=layover,depart_apt=depart_apt,arrive_apt=arrive_apt,layover_apt=layover_apt)


# @app.route("/scrape")
# def scrape_data():
#     output = scrape()
#     # Add scrape data to mongo
#     collection.update({},output,upsert=True)
#     return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=56575, debug=True)