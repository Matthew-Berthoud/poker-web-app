from flask import Flask, render_template#, session
# from flask_session import Session 
    # Session info for Sql Alchemy: https://flask-session.readthedocs.io/en/latest/interfaces.html#sqlalchemysessioninterface


app = Flask(__name__)
# app.config["SESSION_TYPE"] = "sqlalchemy"
#     # Session configuration info: https://flask-session.readthedocs.io/en/latest/config.html
#     # Sessions last 31 days by default in Flask, no config needed on that. Source: https://tedboy.github.io/flask/generated/generated/flask.Flask.permanent_session_lifetime.html#:~:text=permanent_session_lifetime,-Flask.&text=A%20timedelta%20which%20is%20used,survive%20for%20roughly%20one%20month.
# Session(app)


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