from Card import *
from random import shuffle

FULL = 52

class Deck:

    def __init__(self, card_count = FULL):
        self.__deck = []
        self.__shuffle()
        if card_count < FULL:
            self.__deck = self.__deck[FULL - card_count:]
        elif card_count > FULL:
            raise ValueError

        # Every time a new deck object is created,
        # it is automatically populated and shuffled.

    def __shuffle(self):
        for suit in ['spades', 'hearts', 'diamonds', 'clubs']:
            for value in range(2,15):
                card = Card(value, suit)
                self.__deck.append(card)
        shuffle(self.__deck)
        
    def pop(self):
        card = self.__deck[0]
        self.__deck = self.__deck[1:]
        return card

    def __str__(self):
        string = ''
        for card in self.__deck:
            string += str(card) + ' '
        return string

# TESTING

# d1 = Deck()
# d2 = Deck(10)
# try:
#     d3 = Deck(60)
# except ValueError:
#     print('Failed Successfully')

# print(d1)
# c1 = d1.pop()
# print(c1)
# print(d1)

# print(d2)
# c2 = d2.pop()
# print(c2)
# print(d2)