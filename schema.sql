DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS rounds;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS hands;
DROP TABLE IF EXISTS action;


CREATE TABLE players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    pswd_hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 0.00,
    accepting_input NUMERIC DEFAULT 0
);
CREATE UNIQUE INDEX username ON players (username);

CREATE TABLE rounds (
    round_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    game_id INTEGER NOT NULL,
    date_started DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_ended DATETIME, -- can be null, round isn't over when entry created
    which_game TEXT NOT NULL, -- five card draw, texas holdem, etc.]
    shared_cards TEXT NOT NULL 
    -- Example: 4 of hearts, Jack of Spades, Ten of diamonds, Ace of clubs, no fifth card dealt == 4kJsTdNN
);

CREATE TABLE games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date_started DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_ended DATETIME -- can be null, game isn't over when entry created
);

CREATE TABLE hands (
    seat_number INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    round_id INTEGER NOT NULL,
    cards_face_down TEXT NOT NULL,
    cards_face_up TEXT NOT NULL,
    cash_change NUMERIC NOT NULL
);

CREATE TABLE action (
    player_id INTEGER NOT NULL,
    round_id INTEGER NOT NULL,
    betting_round INTEGER NOT NULL, -- round 1 is preflop, etc
    action_string TEXT NOT NULL
        -- EXAMPLE: checks, then calls someone's 20.00 raise, 
        -- then calls someone re-raised to 40.00 (20 more in)
        -- then folds to another reraise

        -- "check 0.00 call 20.00 call 20.00 fold 0.00"
        -- can use split() to decompose for data analysis
);