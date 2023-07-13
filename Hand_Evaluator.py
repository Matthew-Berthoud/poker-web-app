# Defines rules by which to evaluate hands

from Card import *
from Player import *

class Hand_Evaluator:

    def __init__(self):
        pass  # not sure if I need anything in the constructor honestly
    

    def evaluate(self, hands, river = []):
        best_five = {}
        for player in list(hands.keys()):
            best_five[player] = self.get_best_five(hands[player] + river)

        return self.get_winning_hand(best_five)


    def get_best_five(self, full_hand):
        hand = []

        # TODO
            # sort hand
            # check for straights
            # check for duplicate cards
            # check for flushes
            # build hand with best hand type and highest hand factor

        return hand


    def get_winning_hand(self, five_card_hands):
        best = None
        for player in list(five_card_hands.keys()):

        # TODO
            # look through hands
                # if one is best hand, return it (trivial case)
                # if two are "tied" (like both two of a kind)
                    # use highest card and "grouping" techniques to get best

        return best
