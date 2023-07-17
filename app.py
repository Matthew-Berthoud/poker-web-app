from flask import Flask, render_template
from datetime import datetime
from flask_session import Session  # https://flask-session.readthedocs.io/en/latest/
import sqlite3  # https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
                # https://www.sqlite.org/quickstart.html
app = Flask(__name__)


app.config["SESSION_TYPE"] = "filesystem"  # Decided against SQLAlchemy: https://chat.openai.com/share/6466ccc7-c160-402c-a2fe-2777cb1812f3
    # Sessions last 31 days by default in Flask
Session(app)

db = sqlite3.connect('poker.db').cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/play")
def play():
    return render_template("play.html")


if __name__ == "__main__":
    app.run(debug=True)