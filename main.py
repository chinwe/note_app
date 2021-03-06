from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    def __init__(self, title, body, timestamp):
        self.title = title
        self.body = body
        self.timestamp = timestamp

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/notes/create", methods=["GET", "POST"])
def create_note():
        if request.method == "GET":
            return render_template("create_note.html")
        else:
            title = request.form["title"]
            body = request.form["body"]
            timestamp = datetime.now()

            note = Note(title=title, body=body, timestamp=timestamp)

            db.session.add(note)
            db.session.commit()

            return redirect("/")

@app.route("/notes")
def show_notes():
    notes = db.session.query(Note).all()
    notes.reverse()
    return render_template("notes.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)
