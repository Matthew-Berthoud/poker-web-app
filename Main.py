# Runs a poker game!

from Five_Card_Draw import *
from Texas_Hold_Em import *

def print_menu():
    options = ["Texas Hold 'Em", 'Five Card Draw']

    print('\n\nWelcome to Poker. Please select a valid gamemode:')
    print()

    for mode in options:
        print(f'    {mode[0]}  -  {mode}')

    print()

    while True:
        choice = input('Gamemode: ')
        for mode in options:
            if mode[0] == choice:
                return mode


def get_players():
    while True:
        players = input('Number of players (2-9): ')
        print() # for newline
        if players in '23456789':
            return players

mode = print_menu()
players = get_players()

if mode == 'Five Card Draw':
    game = Five_Card_Draw()
elif mode == "Texas Hold 'Em":
    game = Texas_Hold_Em()

game.start(int(players))
game.play()
# game.test()