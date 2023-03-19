from flask import Flask, render_template, request
from dotenv import load_dotenv
from pymongo import MongoClient
import datetime
import os

# Flask's app factory
def create_app():
    load_dotenv()
    app = Flask(__name__)
    #MongoDB
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    # entries = []

    @app.route("/", methods=["GET", "POST"])
    def index():
        # print([e for e in app.db.entries.find({})])
        user = {
            'username': 'solfury11',
            'title': 'microblog',
            }
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            # entries.append((entry_content, formatted_date))
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template('index.html', user=user, entries=entries_with_date)

    @app.route("/about")
    def about():
        return "About"

    @app.route("/blog/")
    def blog():
        posts = [
            {
                'title': 'A bit of a chill day today!',
                'date': 'Oct 24',
                'body': 'Today I couldnt do much programming, but thats ok! Cant be too awesome every day now!',
                'author': {'name': 'John'}
            },
            {
                'title': 'Coding with Python',
                'date': 'Nov 4',
                'body': 'Today I couldnt do much programming, but thats ok! Cant be too awesome every day now!',
                'author': {'name': 'Randall'}
            }
        ]
        return render_template('blog.html', posts=posts)
    
    return app