# poker-web-app

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

## Random notes