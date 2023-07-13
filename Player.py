from Deck import *

class Player:
    
    def __init__(self, player_number, starting_balance = 100):
        self.money = 100  # gets updated by winning and losing
        self.hand = []    # gets updated by dealing
        self.num = player_number
        self.betted = 0
        self.name = 'Player ' + str(self.num)
        # Lots of flags for various behavior:
        self.out = False
        self.lost = False
        self.next = None  # assign to left player

    def make_bet(self, min_bet):
        print(self)
        print(f"{self.name}'s current bet: {self.betted}.")
        print(f"Minimum bet: {min_bet}.")
        fold = input(f'Fold? (y or n): ')
        if fold == 'y':
            self.out = True
            print()
            return 0
        bet = int(input(f"{self.name}, enter bet amount: "))

        self.money -= bet
        print(f'{self.name} bets {bet}.')
        self.betted += bet
        if self.betted != bet:
            print(f'Total bet is {self.betted}\n')
        return bet

    def win_hand(self, pot):
        self.money += pot

    def get_card(self, card):
        self.hand.append(card)


    def __str__(self):
        string = f'Player: {self.name}\n'
        string += f'    Balance: {self.money}\n'
        hand = '[ '
        for card in self.hand:
            hand += str(card) + ' '
        hand = hand + ']'
        string += f'    Hand: {hand}\n'
        return string

# TESTING

# pot = 0
# p = Player(1)
# print(p)
# p.reduce_balance(30)
# pot += 30
# print(p)

# p.get_card(Card(13,'hearts'))
# p.get_card(Card(7,'spades'))
# print(p)