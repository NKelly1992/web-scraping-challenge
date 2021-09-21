from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Set up Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up app routes
@app.route("/")
def index():
    mars_dictionary = mongo.db.mars_dictionary.find_one()
    return render_template("index.html", mars_dictionary=mars_dictionary)

@app.route("/scrape")
def scraper():
    mars_dictionary = mongo.db.mars_dictionary
    mars_dictionary_data = scrape_mars.scrape()
    mars_dictionary.update({}, mars_dictionary_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)