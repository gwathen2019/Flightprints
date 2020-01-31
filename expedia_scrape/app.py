from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

#Route to render index.html template using the data from Mongo
@app.route("/")
def home():
    planet_data = mongo.db.collection.find_one()
    return render_template("index.html", mars=planet_data)

#Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()

    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
