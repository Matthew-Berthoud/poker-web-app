# Defines a playing card class

class Card:

    def __init__(self, value, suit):
        self.__value = value
        self.__suit = suit
        self.face_up = False # useful for later when you can't see everything in terminal

    def change_value(self, new_value):  # Useful for low Aces in straights and straight flushes
        self.__value = new_value

    def face_up(self):
        self.face_up = True

    # Can't think of a use case for face_down method

    # def face_down(self):
    #     self.face_down = False

    def __str__(self):
        values = [None, None, '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = {'spades': '♠️', 'hearts': '♥️', 'diamonds': '♦️', 'clubs': '♣️'}
        return values[self.__value] + suits[self.__suit]

    # overloaded operators defined by value, not suit

    def __eq__(self, other): 
        return self.__value == other.__value

    def __ne__(self, other):
        return self.__value != other.__value

    def __gt__(self, other):
        return self.__value > other.__value

    def __lt__(self, other):
        return self.__value < other.__value

    def __ge__(self, other):
        return self.__value >= other.__value

    def __le__(self, other):
        return self.__value <= other.__value


# TESTING

# for suit in ['spades', 'hearts', 'diamonds', 'clubs']:
#     for value in range(2,15):
#         card = Card(value, suit)
#         print(card)

# ace = Card(14, 'hearts')
# ace2 = Card(14, 'diamonds')
# two = Card(2, 'spades')

# print(ace == two, 'False')
# print(ace == ace2, ' True')

# print(ace != two, ' True')
# print(ace != ace2, 'False')

# print(ace > two, ' True')
# print(ace > ace2, 'False')

# print(ace < two, 'False')
# print(ace < ace2, 'False')

# print(ace >= two, ' True')
# print(ace >= ace2, ' True')

# print(ace <= two, 'False')
# print(ace <= ace2, ' True')