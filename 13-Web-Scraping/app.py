from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    mars_data = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scraper():


    # Run scraped functions
    mars_info = scrape_mars.scrape()

    # Store results into a dictionary
    mars_dat = {
        "news_title": mars_info["news_title"],
		"news_p": mars_info["news_p"],
		"featured_image_url": mars_info["featured_image_url"],
		"mars_weather": mars_info["mars_weather"],
		"mars_facts_html_table": mars_info["mars_facts_html_table"],
		"hemisphere_image_urls": mars_info["hemisphere_image_urls"],
    }

    # Drops collection if available to remove duplicates
    mongo.db.collection.drop()

    # Insert mars_dat into database
    mongo.db.collection.insert_one(mars_dat)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
