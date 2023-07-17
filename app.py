# import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
# from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///poker.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        return redirect("/play")
    else:
        return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM players WHERE username = ?", username)
        p1 = request.form.get("password")
        p2 = request.form.get("confirmation")
        if not username:
            return "must provide username"
        elif len(rows) > 0:
            return "username already exists"
        elif not p1:
            return "must provide password"
        elif p1 != p2:
            return "passwords do not match"
        db.execute("INSERT INTO players (username, pswd_hash) VALUES(?, ?)", username, generate_password_hash(p1))
        session["user_id"] = db.execute("SELECT * FROM players WHERE username = ?", username)[0]["player_id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        rows = db.execute("SELECT * FROM players WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["pswd_hash"], request.form.get("password")):
            return "invalid username and/or password"
        # Remember which user has logged in
        session["user_id"] = rows[0]["player_id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/play")
@login_required
def play():
    return render_template("play.html")


if __name__ == "__main__":
    app.run(debug=True)