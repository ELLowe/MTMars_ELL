from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.mars_data.find_one()
    # Return template and data
    return render_template("index.html", mission=destination_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable

    news_results = scrape_mars.scrape_news_info()

    featured_results = scrape_mars.scrape_featured_image()

    weather_results = scrape_mars.scrape_weather_info()

    facts_results = scrape_mars.scrape_mars_facts()

    images_results = scrape_mars.scrape_full_res_images()

    results = {
        'news':news_results,
        'featured_image': featured_results,
        'weather':weather_results,
        'facts': facts_results,
        'hemispheres': images_results
    }

    # Update the Mongo database using update and upsert=True

    mongo.db.mars_data.update({},results,upsert=True)
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
