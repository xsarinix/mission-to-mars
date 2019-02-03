# import libraries
from flask import Flask, render_template, redirect
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
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    col = db.scrapes
    post = scrape_mars.scrape()
    print(post)
    db.col.insert_one(post)
    return redirect("http://127.0.0.1:5000/")

@app.route("/")
def echo():
    scrapes = list(db.col.find().sort('scrape_time', pymongo.DESCENDING))
    print("Scrapes retrieved.")
    return render_template('index.html', scrapes = scrapes)


if __name__ == "__main__":
    app.run(debug=True)
