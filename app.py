import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from flask_socketio import SocketIO, send, emit
from time import localtime, strftime, gmtime
import random  # for random seat when person joins
import time # for sleep


from helpers import login_required, usd


from Deck import Card, Deck


MAXIMUM_SEATS = 10
FINAL_BETTING_ROUND = 4
LOGS_ENABLED = True

class Table:

    class Table_Seat:
        def __init__(self, seat_number):
            self.is_occupied = False
            self.is_dealer = False
            self.is_small_blind = False
            self.is_big_blind = False

            self.seat_number = seat_number
            self.player_id = 0
            
            self.current_bet = 0.00
            self.cards = []

    def __init__(self, maximum_seats = MAXIMUM_SEATS):
        self.seat_list = [self.Table_Seat(seat_number) for seat_number in range(1, maximum_seats + 1)]

        self.round_number = 0            # "Round" ends when new cards are dealt
        self.player_count = 0
        
        self.big_blind_amount = 10.00
        self.small_blind_amount = round(self.big_blind_amount / 2, 2)

        self.pot = 0.00
        self.deck = Deck()
        self.river = []
        self.game_active = False
   

    def add_player(self, player_id):
        for seat in self.seat_list:
            if seat.player_id == player_id:
                seat_num = seat.seat_number
                return "already seated"
        if self.player_count == 10:
            return "full"

        seat_num = 1
        while self.seat_list[seat_num - 1].is_occupied:
            seat_num = random.randint(1,10)
        self.player_count += 1
        self.seat_list[seat_num - 1].player_id = player_id
        self.seat_list[seat_num - 1].is_occupied = True
        return seat_num


    def remove_player(self, player_id):
        seat_num = 0
        for seat in self.seat_list:
            seat_num += 1
            if seat.player_id == player_id:
                self.player_count -= 1
                seat.is_occupied = False
                seat.player_id = 0
                seat.current_bet = 0.00
                seat.cards = []
                return seat_num


    # def __log(self, to_log):
    #     if LOGS_ENABLED:
    #         print(to_log)
            # f = open("logs/Table_logs.txt", "a")
            # f.write(str(to_log) + "\n")
            # f.close()


    def get_next(self, current_seat):
        # increments by 1 since seat_number is already 1 ahead of index
        return self.seat_list[current_seat.seat_number % MAXIMUM_SEATS]
    

    def get_next_occupied(self, current_seat):
        seat = self.get_next(current_seat)
        while not seat.is_occupied:
            seat = self.get_next(seat)
        return seat


# INITIALIZE ALL THE GAME STUFF
table = Table()


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
        socketio.emit("player_joined", (player, status, table.player_count))

    print(f'\n{username} CONNECTED\n')    
    return render_template("play.html", player=player, seat_num=status)


@socketio.on('disconnected')
def disconnected():
    player=db.execute("SELECT * FROM players WHERE player_id = ?", session["user_id"])[0]
    username = player["username"]
    removed_seat_num = table.remove_player(session["user_id"])
    print(f'\n{username} DISCONNECTED\n')
    emit("player_left", (player, removed_seat_num, table.player_count))        

@socketio.on('message')
def message(data):
    print(f"\n{data}\n")
    send(data)
    # send({'username': data['username'], 'player_id': data['player_id'], 'action': data['action'], 'time_stamp': 
    #     strftime('%Y%j%H%M%S', gmtime())})  # https://docs.python.org/3/library/time.html

@socketio.on('start_or_continue_game')
def start_or_continue_game():
    print("\nSTART/CONTINUE GAME\n")
    if not table.game_active:
        table.game_active = True
        start_or_continue_game()
    else:
        play_round(big_blind_amount = 10, dealer_seat = 1)

@socketio.on('end_game')
def end_game():
    print("\nEND GAME\n")



@socketio.on('action_button')
def action_button_clicked(action, slider, player):
    username = player["username"]
    notification = f"{action} from {username}, slider at {slider}"
    print(f"\n{notification:}\n")
    emit("global_notification", notification, broadcast=True)



def player_input(player_id, current_bet): # https://chat.openai.com/share/f3f0f1a0-d940-4e19-b454-b1340eca0c85
    # https://www.youtube.com/watch?v=zQDzNNt6xd4
    # secs = 0

    # while secs < 30:
    #     time.sleep(1)
    pass


def play_round(big_blind_amount, dealer_seat):  # assign dealer and blinds
    table.round_number += 1
    table.big_blind_amount = big_blind_amount
    
    # table.player_count = 0
    # for seat_num in occupied_seats:
    #     table.seat_list[seat_num - 1].is_occupied = True
    #     table.player_count += 1
    # if dealer_seat not in occupied_seats:
    #     raise IndexError
    
    dealer = table.seat_list[dealer_seat - 1]
    dealer.is_dealer = True

    small_blind_seat = table.get_next_occupied(dealer)
    small_blind_seat.is_small_blind = True
    send("I am big blind")

    big_blind_seat = table.get_next_occupied(small_blind_seat)
    big_blind_seat.is_big_blind = True
    send("I am small blind")
    
    winner_or_none = None
    betting_round_number = 1
    while winner_or_none is None and betting_round_number <= FINAL_BETTING_ROUND:
        if betting_round_number == 1:
            for seat in table.seat_list:
                if seat.is_occupied:
                    card1 = table.deck.pop()
                    card2 = table.deck.pop()
                    seat.cards = [card1, card2]
                    send("My cards: " + str(seat.cards))
        elif betting_round_number == 2:
            card1 = table.deck.pop()
            card2 = table.deck.pop()
            card3 = table.deck.pop()
            table.river = [card1, card2, card3]
            emit("global_notification", "river: "+ str(table.river))
        else:
            card = table.deck.pop()
            table.river += [card]
            emit("global_notification", "river: "+ str(table.river))

        winner_or_none = play_betting_round(betting_round_number, small_blind_seat)
        betting_round_number += 1

    if winner_or_none is None:
        winner = evaluate()
    else:
        winner = winner_or_none
    return winner


def play_betting_round(betting_round_number, small_blind_seat):
    seat = small_blind_seat
    lap_number = 0
    current_bet = 0.00
    
    send(f"\n\n\n\nplay_betting_round {betting_round_number} small_blind_seat {small_blind_seat.seat_number}")

    while True:
        if seat == small_blind_seat:
            lap_number += 1

        send(f"lap {lap_number} seat {seat.seat_number} cur_bet {current_bet}")

        if not seat.is_occupied:
            seat = table.get_next(seat)
            continue

        first_round_big_blind = ((betting_round_number == 1) and (lap_number == 2) and seat.is_big_blind)
        if (lap_number > 1 and not first_round_big_blind):
            all_seats_paid = True
            for seat in table.seat_list:
                if seat.is_occupied and (seat.current_bet != current_bet):
                    all_seats_paid = False
                    break
            if all_seats_paid:
                send(f"BREAK lap_number {lap_number} seat {seat.seat_number} current_bet {current_bet}")
                break

        if (betting_round_number == 1 and lap_number == 1 and (seat.is_small_blind or seat.is_big_blind)):
            if seat.is_small_blind:
                action = ["raise/bet", table.small_blind_amount]
            else:
                action = ["raise/bet", table.big_blind_amount]
        else:
            action = player_input(player_id = seat.player_id, current_bet = current_bet)
        
        if action[0] == "fold":
            seat.is_occupied = False
            table.player_count -= 1
        elif action[1] < current_bet:
            raise ValueError  # should have been handled by player_input method or frontend
        else:
            current_bet = round(action[1], 2)
            seat.current_bet = current_bet
            # update other variables

        send(f"Seat {seat.seat_number} {action[0].upper()} {action[1]}")
        
        if table.player_count < 2:
            return table.get_next_occupied(seat)
            # returns the winner
            # but where will it return to?

        seat = table.get_next(seat)

def evaluate():
    send(f"evaluate: just returning one of the remaining players for now")
    return [seat for seat in table.seat_list if seat.is_occupied][0]




if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)  # https://stackoverflow.com/questions/72795799/how-to-solve-403-error-with-flask-in-python