import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from flask_socketio import SocketIO, send, emit
from time import localtime, strftime, gmtime
import random  # for random seat when person joins

from helpers import login_required, usd


from Table import Table
from Deck import Card, Deck

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret!' # necessary for socketio for some reason
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///poker.db")

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Jinja Filter
app.jinja_env.filters["usd"] = usd

# INITIALIZE ALL THE GAME STUFF
table = Table()




@app.after_request
def after_request(response):
    """Ensure responses aren't cached""" # no idea how or why, stole from cs50
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        return redirect("/play")
    else:
        account = db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])
        return render_template("index.html", player=account[0]["username"], cash=account[0]["cash"])


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


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", player=db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0])


@app.route("/settings/username", methods=["GET", "POST"])
@login_required
def change_username():
    player = db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0]
    if request.method == "POST":
        new = request.form.get("new")
        old = player["username"]
        rows = db.execute("SELECT * FROM players WHERE username = ?", new)
        if len(rows) > 0 and new != old:
            return "username already in use"
        db.execute("UPDATE players SET username = ? WHERE player_id = ?", new, session["user_id"])
        flash("Username changed")
        return redirect("/settings")
    else:
        return render_template("username.html", player=player)


@app.route("/settings/password", methods=["GET", "POST"])
@login_required
def change_password():
    player = db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0]
    if request.method == "POST":
        old = request.form.get("old")
        new = request.form.get("new")
        conf = request.form.get("confirmation")
        if not check_password_hash(player["pswd_hash"], old):
            return "old password incorrect"
        if new != conf:
            return "new passwords do not match"
        db.execute("UPDATE players SET pswd_hash = ? WHERE player_id = ?", generate_password_hash(new), session["user_id"])
        flash("Password changed")
        return redirect("/settings")
    else:
        return render_template("password.html", player=player)


@app.route("/settings/balance", methods=["GET", "POST"])
@login_required
def change_balance():
    if request.method == "POST":
        deposit = request.form.get("deposit")
        withdrawal = request.form.get("withdrawal")

        # most error checking handled by min, max, and step attributes in the template
        # check that one and only one of the fields has an entry
        if not (bool(deposit) ^ bool(withdrawal)):
            return "enter dollar amount in exactly one field"
        if bool(deposit):
            update = float(deposit)
        if bool(withdrawal):
            update = -1 * float(withdrawal)
        db.execute("UPDATE players SET cash = cash + ? WHERE player_id = ?", update, session["user_id"])
        flash("Bankroll updated")
        return redirect("/settings")
    else:
        return render_template("bankroll.html", player=db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0])
    

@app.route("/play", methods=['GET', 'POST'])
@login_required
def play():
    player = db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0]
    return render_template("play.html", player=player)

@socketio.on('connected')
def connected():
    player = db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0]
    username = player["username"]
    
    status = table.add_player(session["user_id"])
    if status == "full":
        return "table full"
    elif status in range(1,11):
        socketio.emit("player_joined", (player, status))

    print(f'\n\n{username} CONNECTED\n\n')    
    return render_template("play.html", player=player, seat_num=status)


@socketio.on('disconnected')
def disconnected():
    player=db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0]
    username = player["username"]
    table.remove_player(session["user_id"])
    
    print(f'\n\n{username} DISCONNECTED\n\n')
    send("fully_disconnected")



@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send(data)
    # send({'username': data['username'], 'player_id': data['player_id'], 'action': data['action'], 'time_stamp': 
    #     strftime('%Y%j%H%M%S', gmtime())})  # https://docs.python.org/3/library/time.html

@socketio.on('action_button')
def action_button_clicked(action, slider, player):
    username = player["username"]
    notification = f"{action} from {username}, slider at {slider}"
    print(notification)
    emit("global_notification", notification, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)