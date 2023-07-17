from flask import Flask, render_template
from datetime import datetime
from flask_session import Session  # https://flask-session.readthedocs.io/en/latest/
import sqlite3  # https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
                # https://www.sqlite.org/quickstart.html
app = Flask(__name__)


app.config["SESSION_TYPE"] = "filesystem"  # Decided against SQLAlchemy: https://chat.openai.com/share/6466ccc7-c160-402c-a2fe-2777cb1812f3
    # Sessions last 31 days by default in Flask
Session(app)

# db = sqlite3.connect("sqlite:///poker.db")

# Example code about Alchemy DB
# Source: https://www.youtube.com/watch?v=Z1RJmh_OqeA
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#     # 4 slashes is absolute path, 3 is relative path, we just want db to live with project somewhere
# db = SQLAlchemy(app)
    
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id





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