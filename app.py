# Import Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create/Bind Routes
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()

   # format -> .update(query_parameter, data, options)
   # {} -> Add and empty JSON Object
   # upsert=True -> create a new document if one doesn't 
   #                already exist, and new data will always be saved
   mars.update({}, mars_data, upsert=True)

   # '/' -> navigate our page back to '/' where we can see the updated content
   return redirect('/', code=302)   

# Instruct Flask to run
if __name__ == "__main__":
   app.run()