class Card:


    def __init__(self, value, suit):
        self.__value = value
        self.__suit = suit
        self.face_up = False # useful for later when you can't see everything in terminal


    def __str__(self):
        values = [None, None, '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return values[self.__value] + self.__suit