from flask import Flask, render_template,redirect
from expedia_scraper_master_windows import scrape
import json
# Create an instance of our Flask app.
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def index():
    output = scrape()

    return render_template('index.html', model=model,airline=airline,depart=depart,arrive=arrive,duration=duration,no_stops=no_stops,price=price,layover=layover,depart_apt=depart_apt,arrive_apt=arrive_apt,layover_apt=layover_apt)


# @app.route("/scrape")
# def scrape_data():
#     output = scrape()
#     # Add scrape data to mongo
#     collection.update({},output,upsert=True)
#     return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=56575, debug=True)