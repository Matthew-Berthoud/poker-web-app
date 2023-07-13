# Defines procedures to be used across various poker game child classess

from Player import *
from Deck import *
from Hand_Evaluator import *

LITTLE_BLIND = 5
BIG_BLIND = 10


class Poker_Games:
    

    def __init__(self):
        self.river = []
        self.dealer = None
        self.deck = Deck()
        self.checker = Hand_Evaluator()
        self.pot = 0
        # self.current_bet = 0


    # TODO
        # helper method for next player that returns next player who isn't out,
        # and returns some indicator that everyone folded and you win if that next player is the current player
        
        # reorganize where the logic is for betting... maybe make first round betting 
        #(with little and big blinds) its own method?

        # whiteboard all necessary checks and exit conditions


    def bet(self, blind_round = False):
        if blind_round: # unless it's the first round
            min_bet = BIG_BLIND
            better = self.dealer.next.next.next
        else:
            min_bet = 0
            better = self.dealer.next
            self.reset_bets() # make all player.betted == 0

        can_stop = False  # becomes true once we make it around once
        while True:
            if better.next == better:
                return better  # everyone folded, you win

            if (blind_round and better == self.dealer.next.next) or (not blind_round and better == self.dealer):
                can_stop = True

            if better.out:
                better = better.next
                continue
                
            # print river
            if self.river != []:
                print('\nRiver: [', end = ' ')
                for card in self.river:
                    print(card, end = ' ')
                print(']')

            bet = better.make_bet(min_bet)
            min_bet = max(bet, min_bet)
            self.pot += bet

            if better.next == better: # everyone else folded
                return better

            if can_stop: # we've done a full lap
                # check whether next better (WHO HASN'T FOLDED) has bet the minimum
                check_next = better.next
                while check_next.out:
                    check_next = check_next.next
                if check_next.betted == min_bet:
                    break    

            better = better.next
            
            
    def reset_bets(self):
        cur = self.dealer.next
        while True:
            cur.betted = 0
            cur = cur.next
            if cur == self.dealer:
                return


    # def bet(self):
    #     player = self.dealer.next
    #     can_stop = False
    #     prev = 0
    #     while True:
    #         if player.num == prev: # one player left, winner!
    #             return player

    #         if player == self.dealer:
    #             can_stop = True
            
    #         if can_stop and self.current_bet == player.betted: # no further money owed
    #             break

    #         if player.out:
    #             player = player.next
    #             continue

    #         print('\n'+ str(player))
    #         if self.river != []:
    #             print('River: [', end = ' ')
    #             for card in self.river:
    #                 print(card, end = ' ')
    #             print(']')

    #         valid_bet = False
    #         while not valid_bet:
    #             print(f"{player.name}'s current bet: {player.betted}.")
    #             bet = input(f"{player.name}, enter bet amount or f to fold: ")
    #             if bet == 'f':
    #                 player.out = True
    #                 print(f'{player.name} folded.\n')
    #                 valid_bet = True
    #             elif not bet.isnumeric() or int(bet) < 0:
    #                 print(f'Invalid entry.')
    #             elif int(bet) + player.betted < self.current_bet:
    #                 print(f'Current bet is {self.current_bet}.')
    #             elif int(bet) >= player.money:
    #                 print(f"{player.name}'s balance is {player.money}.")
    #                 all_in = 'a'
    #                 while all_in not in 'yn':
    #                     all_in = input(f'Want to go all in? ')
    #                     if all_in == 'y':
    #                         bet = player.money
    #                         valid_bet = True
    #             else:
    #                 valid_bet = True  # all invalid entries filtered out

    #         if not player.out:
    #             self.pot += int(bet)
    #             self.current_bet += int(bet)
    #             player.reduce_balance(int(bet) - player.betted)
    #             player.betted = int(bet)
    #             prev = player.num
    #         print(player)
    #         print('Turn over.\n')
    #         player = player.next

    #     self.current_bet = 0 # reset for next time
            

    def start_round(self):
        # full deck
        self.deck = Deck() # new one, shuffled and ready!
        self.pot = 0

        # initialize dealer
        prev = self.dealer
        self.dealer = prev.next
        print(f'{self.dealer.name} is dealer.\n')

        # little and big blind to kick off each round
        little = self.dealer.next
        big = little.next

        print(f'{little.name} is little blind.')
        little.money -= LITTLE_BLIND
        little.betted = LITTLE_BLIND

        print(f'{big.name} is big blind.\n')
        big.money -= BIG_BLIND
        big.betted = BIG_BLIND

        self.pot += LITTLE_BLIND + BIG_BLIND


    def river_card(self, face_up = True): # one card for all players to see and use
        card = self.deck.pop()
        self.river.append(card)
        print(f'Adding {str(card)} to river.')


    def deal_to_all(self, face_up = False): # deal one card to everyone
        player = self.dealer.next
        while True:
            if not player.out:
                self.deal_card(player)
            player = player.next
            if player == self.dealer.next: # finished the circle
                break


    def deal_card(self, player, face_up = False,): # card to ONE player, still can be face up for like blackjack
        card = self.deck.pop()
        player.hand.append(card)
        print(f'Dealing {str(card)} to {player.name}.')


    def early_win(self, winner):
        print(f'{winner.name} wins {self.pot}, since everyone else folded.')
        winner.win_hand(self.pot)


    def show(self): # everyone shows cards, someone wins
        hands = {}

        player = self.dealer.next  # start left of dealer, by convention
        while True:
            if player.out:
                player = player.next
                continue

            hands[player.num] = player.hand

            if player == self.dealer:
                break

        self.checker.check(hands, self.river)


    def start(self, players):
        temp = []
        for i in range(1, 1 + players):
            player = Player(i)
            temp.append(player)
      
        self.dealer = temp[0]
        cur = self.dealer

        # Careful, i is not player number here, it's player's temp index (player number - 1)
        for i in range(1, players): # I don't think there's a way to only do this loop once
            cur.next = temp[i]
            cur = cur.next

        temp[-1].next = self.dealer


    def test(self):

        # make sure players form a circular linked list

        # cycles = 0
        # cur = self.dealer
        # while cycles <= 3:
        #     print(cur.name)
        #     cur = cur.next
        #     if cur is self.dealer:
        #         cycles += 1

        pass