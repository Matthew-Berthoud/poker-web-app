import random  # ONLY FOR TESTING BEFORE I IMPLEMENT player_input
from Deck import *


MAXIMUM_SEATS = 10
FINAL_BETTING_ROUND = 4
LOGS_ENABLED = True

class Table:

    class __Table_Seat:
        def __init__(self, seat_number):
            self.is_occupied = False
            self.is_dealer = False
            self.is_small_blind = False
            self.is_big_blind = False

            self.seat_number = seat_number
            self.player_id = 0
            
            self.current_bet = 0.00

    def __init__(self, maximum_seats = MAXIMUM_SEATS):
        self.seat_list = [self.__Table_Seat(seat_number) for seat_number in range(1, maximum_seats + 1)]

        self.round_number = 0            # "Round" ends when new cards are dealt
        self.player_count = 0
        
        self.big_blind_amount = 10.00
        self.small_blind_amount = round(self.big_blind_amount / 2, 2)

        self.pot = 0.00
   

    def __log(self, to_log):
        if LOGS_ENABLED:
            f = open("logs/Table_logs.txt", "a")
            f.write(str(to_log) + "\n")
            f.close()


    def get_next(self, current_seat):
        # increments by 1 since seat_number is already 1 ahead of index
        return self.seat_list[current_seat.seat_number % MAXIMUM_SEATS]
    

    def get_next_occupied(self, current_seat):
        seat = self.get_next(current_seat)
        while not seat.is_occupied:
            seat = self.get_next(seat)
        return seat


    def player_input(self, player_id, current_bet):
        action = random.choice(["fold", "call/check", "raise/bet"])
        if action == "fold":
            amount = ""
        elif action == "call/check":
            amount = current_bet
        else:
            amount = round(random.randint(current_bet,1000), 2)
        return [action, amount]
        # just for testing
        # finish later


    def play_round(self, big_blind_amount, occupied_seats, dealer_seat):  # assign dealer and blinds
        self.round_number += 1
        
        self.big_blind_amount = big_blind_amount
        
        for seat_num in occupied_seats:
            self.seat_list[seat_num - 1].is_occupied = True
            self.player_count += 1
        if dealer_seat not in occupied_seats:
            raise IndexError
        
        dealer = self.seat_list[dealer_seat - 1]
        dealer.is_dealer = True

        small_blind_seat = self.get_next_occupied(dealer)
        small_blind_seat.is_small_blind = True

        big_blind_seat = self.get_next_occupied(small_blind_seat)
        big_blind_seat.is_big_blind = True
        
        winner_or_none = None
        betting_round_number = 1
        while winner_or_none is None and betting_round_number <= FINAL_BETTING_ROUND:
            self.deal_cards(betting_round_number)
            winner_or_none = self.play_betting_round(betting_round_number, small_blind_seat)
            betting_round_number += 1

        return winner_or_none
        # winner = determine_winner(winner_or_none)


    def deal_cards(self, betting_round_number):
        if betting_round_number == 1:
            print("dealing 2 cards")
            pass
            # cards_to_players(2)
        elif betting_round_number == 2:
            print("dealing 3 to river")
            pass
            # river_cards(3)
        else:
            print("dealing 1 to river")
            pass
            # river_cards(1)


    def play_betting_round(self, betting_round_number, small_blind_seat):
        seat = small_blind_seat
        lap_number = 0
        current_bet = 0.00
        
        self.__log(f"\n\n\n\nplay_betting_round {betting_round_number} small_blind_seat {small_blind_seat.seat_number}")

        while True:
            if seat == small_blind_seat:
                lap_number += 1

            # self.__log(f"lap {lap_number} seat {seat.seat_number} cur_bet {current_bet}")

            if not seat.is_occupied:
                seat = self.get_next(seat)
                continue

            first_round_big_blind = ((betting_round_number == 1) and (lap_number == 2) and seat.is_big_blind)
            if (lap_number > 1 and not first_round_big_blind):
                all_seats_paid = True
                for seat in self.seat_list:
                    if seat.is_occupied and (seat.current_bet != current_bet):
                        all_seats_paid = False
                        break
                if all_seats_paid:
                    self.__log(f"BREAK lap_number {lap_number} seat {seat.seat_number} current_bet {current_bet}")
                    self.__log(f"seats still in: {}")
                    break

            if (betting_round_number == 1 and lap_number == 1 and (seat.is_small_blind or seat.is_big_blind)):
                if seat.is_small_blind:
                    action = ["raise/bet", self.small_blind_amount]
                else:
                    action = ["raise/bet", self.big_blind_amount]
            else:
                action = self.player_input(player_id = seat.player_id, current_bet = current_bet)
            
            if action[0] == "fold":
                seat.is_occupied = False
                self.player_count -= 1
            elif action[1] < current_bet:
                raise ValueError  # should have been handled by player_input method or frontend
            else:
                current_bet = round(action[1], 2)
                seat.current_bet = current_bet
                # update other variables

            self.__log(f"Seat {seat.seat_number} {action[0].upper()} {action[1]}")
            
            if self.player_count < 2:
                return self.get_next_occupied(seat)
                # returns the winner
                # but where will it return to?

            seat = self.get_next(seat)



table = Table()

winner = table.play_round(big_blind_amount = 10.00, occupied_seats = [1,2,3,4,5], dealer_seat = 5)
print(winner)