## Object structure
* Table - mostly a static record - array of seats with length 10 - table will handle all the positioning stuff, whereas game will handle other stuff
    * Seat
        * filled - bool - if not empty, there's a player id number
        * dealer - bool
        * small_blind - bool
        * big_blind - bool
        * number - int 1-10 for seat at table
        * Player -> MIGHT WANT TO THINK ABOUT JUST USING THE PLAYER ID NUMBER IN THE SEAT STRUCTURE? NOT SURE
            * unique id number, matches user id from server / account
            * cash of type int- some number of dollars, they can update from their account
            * hand of type Group_Of_Cards - cards in their hand DOES NOT INCLUDE RIVER
            * sitting_out - bool IF PLAYER SITS OUT, MAKE seat.filled FALSE
    * end_round_move_dealer method
    * get_next_player method
    * player_sit_out method
    * get_active_players method
    * ... probably some more methods to think of... I want all the game action treating table as a record
    
* Game - handles hand evaluation and money stuff I guess, none of the movement that table handles
    * every new hand / new deal / new round runs a "game."
        * player cash balance, position, etc is stored and managed by Table object, and the objects thereunder
        * game accesses various parts of this record for each player as needed

## Website structure
* two types of accounts admin and regular
    * research this, there's probably a good way to do it
    * possibly just keep some internal db of what user ids do and don't have certain permissions?
        * does this work with function decorators?

## Environment
The `env/` folder is ignored in the repository. Follow the following in poker-web-app to replicate the repository's required environment (assuming you have python 3):
```sh
pip install virtualenv
virtualenv env
source env/bin/activate
pip install flask
```

## Database
### Set up database
The poker.db file is not contained in the repository, since in production it stores account information, cash totals, etc. You wouldn't want your friends to know how much fake money is in your account on this website. To create it yourself, execute
`sqlite3 poker.db` then run the contents of init_db.sql from that prompt.

* the database does track:
    * Time and date of:
        * players joining the site
        * start and finish of games
        * start and finish of rounds
    * Which game (Texas holdem, 5 card draw, blackjack, etc) is played in a round
        * can change the game every round if you want
    * seat numbers and cards for every player every round of every game, including faceup and facedown cards, and river cards
    * change in cash balance after each round for each player
* the database does not track:
    * individual bet sizing
    * when players folded, called, raised, etc specifically
    * anything else I didn't think of
* I should be able to add functionality to track all that in a future update, but it's overkill to think about for now







## Things I've done
### July 15, 2023
* installed virtualenv in poker-web-app directory <!-- Source: https://www.youtube.com/watch?v=Z1RJmh_OqeA&ab_channel=freeCodeCamp.org -->
``` sh
pip install virtualenv
virtualenv env
source env/bin/activate
pip install flask flask-sqlalchemy
```
* Got this error:

    ```
    xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
        error: command '/usr/bin/clang' failed with exit code 1
        [end of output]
    
    note: This error originates from a subprocess, and is likely not a problem with pip.
    ERROR: Failed building wheel for greenlet
    Running setup.py clean for greenlet
    Failed to build greenlet
    ERROR: Could not build wheels for greenlet, which is required to install pyproject.toml-based projects
    ```

* Might be because I deleted XCode oops. I just couldn't stand everything opening with xcode when I want vscode sue me. We'll see if it causes any issues.

* Downloaded xcode, configured it, reran, and everything fine

### July 16, 2023

* I don't think I should commit env file since it will end up storing sensitive stuff I think?
    * is there some way I should list what people would need to download in order to run it? Because I thought the point of the env was that I didn't have to download everything locally, but could have  it attached to the project. Is there a difference between like environment variables (sensitive stuff) and the env folder?
        * LEARN MORE ABOUT ENVIRONMENT
* Session info and sources is in comments on app.py
* don't really get how sql stuff is linked, or how this database is joining the project


### July 17, 2023
* Having tons of trouble with sql. I want to avoid using the cs50 library, which abstracts the connecting of the SQL database. I thought it would be similar to just use sqlite3, but it got weird and I didn't know what was happening
* I'm using SQAlchemy now, which is weird cause it abstracts queries into python code, but if I just use `db.session.execute(text())` it will be more like real SQL? I guess?
* There are already some differences in syntax to sqlite3, but hopefully not many

* NEVER MIND ALL OF THAT: I AM USING THE CS50 LIBRARY I DON'T UNDERSTAND ALL THIS DATABASE STUFF
    * Basically stealing the first 20ish lines of code from app.py for the finance project. Also using lots of the login/logout stuff. Why redo what works/I'm used to?
    * Learn the details of databases and servers and stuff later, right now I have a poker app to build
* I'm moving on to the actual poker logic stuff, but if I ever want to limit sessions, so people can't log into the same account from two different places at the same time can use this type stuff: https://stackoverflow.com/questions/31281470/how-to-limit-one-session-from-any-browser-for-a-username-in-flask

* Did betting logic I think
* Tomorrow: 
    * UNIT TESTS for play_betting_round as well as basic tests of Table and Seat classes, make sure things work how I want
    * Then add in pot, individual chip stacks, 
* Note that play_betting_round cycles through every seat, occupied or not, folded or not, and then decides to maybe break with that super long if statement.
    * it is okay to start at small blind every time cause it's emptiness / the weirdness of the first round will we accounted for in the huge if statement.


### July 18, 2023
I thought Tables would have good methods for unit tests, but I don't know how to simulate player input and interaction with other functions / objects

### July 19, 2023
* Today's plan is to 
    * test the stuff I've done even more
        * make necessary changes, commit
    * move on to planning structurally how things interact
        * where does bet inputting happen?
        * where does hand evaluation happen?
        * how does this all sync up?
    * figure out what more I need out of the table class and FINISH IT
        * commit
* thoughts on how to do hand eval:
    * get 7 card hand of every player. For each one:
        * make all possible 5 card hands
        * evaluate (this is the hardest part)
        * give strongest one
    * evaluate between the players (can be the same method as when we got the best hand for each player)
    * return winner(s)
* probably put current bet in the player class

### July 26, 2023
* The code below gives a string that looks like this `2023207000419` representing the year, day of year, hour, minutes, seconds so that when casted to an int I can use comparison operators.
    ```py
    strftime('%Y%j%H%M%S', localtime()
    ```
* Decided against adding room functionality at this time, there will only be the one room for now. Can use tutorial for flask socketio to add them later.
* Finished the video, can refer to the first 40 minutes as I make all these requests work, and broadcast certain things to certain people

#### HERE'S HOW I'M USING SOCKETIO:
* players clicking play button (implicitly joining the only (for now) room) will send a custom event to the server with a their player_id or username
    * same with players leaving the page (there has to be a javascript event for this)
* players clicking action buttons will send a json event to server, with player_id/username, what number the bet slider is at, which button they clicked, and maybe the time they clicked it if necessary for making sure it's their turn
    * if it's their turn (which we probably don't need to know the time to determine, on second thought), the server will process the user input and send back json to update the board
        * **this part may be hard to get right**

## AT SOME POINT I NEED TO ADD AN ALL-IN LIMIT TYPE THING TO THE METHODS IN THE TABLE CLASS, OR SIDE POTS WILL HAPPEN AND BE HANDLED IMPROPERLY

## Sources

* [Multiplayer flask game reddit post](https://www.reddit.com/r/flask/comments/if7po9/how_my_friend_and_i_built_a_multiplayer_game/?onetap_auto=true)
    * [Tutorial for flask socketio](https://www.youtube.com/watch?v=zQDzNNt6xd4)
        * For each player action:
            * send json object with user_id as key, and a dictionary as value, where the dictionary has all the info that has been changed
            * Can do something like this both directions
        * join room / leave room
            * leave room auto folds, makes you out of the round, join room puts you in a seat when the next round starts
            * maybe I'll be able to have multiple rooms! 