# import libraries
from flask import Flask, render_template
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
col = db.scrapes

# create instance of Flask app
app = Flask(__name__)

# create route that renders index.html template
@app.route("/scrape")
def scrape_route():
    import scrape_mars
    post = scrape_mars.scrape()
    return db.col.insert_one(post)

@app.route("/")
def echo():
    most_recent_scrape = db.col.find_one(sort=[('scrape_time', pymongo.DESCENDING)])
    return render_template('index.html', scrape = most_recent_scrape)


if __name__ == "__main__":
    app.run(debug=True)
