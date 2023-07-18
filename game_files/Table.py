from Seat import *

class Table:

    def __init__(self, maximum_seats = 10):
        self.seat_list = [Seat(seat_number) for seat_number in range(1, maximum_seats + 1)]

        self.round_number = 1            # "Round" ends when new cards are dealt
        self.betting_round_number = 1    # round 1 is preflop, etc
        self.current_bet = 0.00
        self.player_count = 0
        

    def find_small_blind(self):
        for seat in self.seat_list:
            if seat.is_small_blind:
                return seat
        raise IndexError


    def play_betting_round(self):
        self.betting_round_number += 1
        starting_seat = find_small_blind()
        seat = starting_seat
        lap_number = 1

        while True:
            if seat = starting_seat:
                lap_number += 1

            if (self.betting_round_number == 1 and lap_number == 1 \
                and (seat.is_small_blind or seat.is_big_blind)) \
            or not seat.is_occupied \
            or (lap_number > 1 and self.current_bet == seat.current_bet \
                and not (self.betting_round_number == 1 and lap_number == 2 and seat.is_big_blind)):
                
                seat = self.seat_list[seat.seat_number % 10]  # this advances by 1 since seat_number is 1 ahead of index
                continue

            action = player_input(player=seat.player_id)
            if action == "fold":
                self.player_count -= 1
            else:
                self.current_bet = seat.current_bet

            if self.player_count < 2:
                return seat  # returns the winner, but how will I handle this return and where will it go?
            seat = self.seat_list[seat.seat_number % 10]  # this advances by 1 since seat_number is 1 ahead of index



    def play_round(self):
        self.round_number += 1
        for seat in self.seat_list:
            if seat.is_occupied:
                self.player_count += 1

        # deal two to all
        play_betting_round()
        if self.player_count < 2:
            return 
        # 3 river cards
        play_betting_round()
        # 1 river card
        play_betting_round()
        # 1 river card
        play_betting_round()


    def player_input(self):
        # store it in who's up
        
       
        



    def player_input(self):