# Defines a Texas_Hold_Em game
# Makes use of rules and methods from Poker_Games parent class

from Poker_Games import *

class Texas_Hold_Em(Poker_Games):


    def play(self):
        won = False
        while not won:

            self.start_round()

            for i in range(2):
                self.deal_to_all()
                print()

            winner = self.bet(blind_round = True)
            if winner != None: # all but one folded
                self.early_win(winner)
                continue

            print()
            for i in range(3):
                self.river_card()
            print()
            
            winner = self.bet()
            if winner != None: # all but one folded
                self.early_win(winner)
                continue

            self.river_card()

            winner = self.bet()
            if winner != None: # all but one folded
                self.early_win(winner)
                continue

            self.river_card()

            winner = self.bet()
            if winner != None: # all but one folded
                self.early_win(winner)
                continue
            self.show()