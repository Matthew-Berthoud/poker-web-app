from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy  # https://www.youtube.com/watch?v=Z1RJmh_OqeA&ab_channel=freeCodeCamp.org
from sqlalchemy import text  # https://chat.openai.com/?model=text-davinci-002-render-sha
from datetime import datetime
from flask_session import Session  # https://flask-session.readthedocs.io/en/latest/
# import sqlite3  # https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
                # https://www.sqlite.org/quickstart.html
from werkzeug.security import check_password_hash, generate_password_hash
from decorators import login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker.db'
db = SQLAlchemy(app)


# Configure session to use filesystem (instead of signed cookies)
# taken from cs50 finance pset
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db = sqlite3.connect('poker.db')
# db = conn.cursor()
# conn.close()

@app.route("/")
def index():  # 
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()  # Forget any user_id

    if request.method == "POST":

        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"

        rows = db.session.execute(text("SELECT * FROM players WHERE username = :username"), {"username":  request.form.get("username")})
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/play")
def play():
    return render_template("play.html")



if __name__ == "__main__":
    app.run(debug=True)