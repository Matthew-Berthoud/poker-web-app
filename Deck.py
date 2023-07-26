from random import shuffle

FULL = 52

class Card:


    def __init__(self, value, suit):
        self.__value = value
        self.__suit = suit
        self.face_up = False # useful for later when you can't see everything in terminal


    def __str__(self):
        values = [None, None, '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return values[self.__value] + self.__suit
        
class Deck:


    def __init__(self, card_count = FULL):
        self.__deck = []
        for suit in "shdc":
            for value in range(2,15):
                card = Card(value, suit)
                self.__deck.append(card)
        shuffle(self.__deck)
        if card_count != FULL:
            raise ValueError
        
        
    def pop(self):
        card = self.__deck[0]
        self.__deck = self.__deck[1:]
        return card


    def __str__(self):
        string = ''
        for card in self.__deck:
            string += str(card) + " "
        return string

