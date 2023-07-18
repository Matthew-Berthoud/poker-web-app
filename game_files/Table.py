import random  # ONLY FOR TESTING BEFORE I IMPLEMENT player_input

MAXIMUM_SEATS = 10
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
        self.betting_round_number = 0    # round 1 is preflop, etc
        self.player_count = 0
        
        self.big_blind_amount = 10.00
        self.small_blind_amount = 5.00

    def find_small_blind(self):
        for seat in self.seat_list:
            if seat.is_small_blind:
                return seat
        raise IndexError


    def play_betting_round(self):
        self.betting_round_number += 1
        starting_seat = self.find_small_blind()
        seat = starting_seat
        lap_number = 0
        current_bet = 0.00
        
        self.__log(f"play_betting_round {self.betting_round_number} starting_seat {starting_seat.seat_number}")

        while True:
            if seat == starting_seat:
                lap_number += 1

            self.__log("WHILE LOOP")
            cb = "{:10.2f}".format(current_bet)
            self.__log(f"lap_number {lap_number} seat {seat.seat_number} current_bet {cb}")

            if not seat.is_occupied:
                seat = self.seat_list[seat.seat_number % MAXIMUM_SEATS]  # this advances by 1 since seat_number is 1 ahead of index
                continue
            
            if (lap_number > 1 and current_bet == seat.current_bet \
                and not (self.betting_round_number == 1 and lap_number == 2 and seat.is_big_blind)):
                self.__log(f"BREAKING WITH THESE VALUES:")
                self.__log(f"lap_number {lap_number} seat {seat.seat_number} current_bet {cb}")
                break

            if (self.betting_round_number == 1 and lap_number == 1 \
            and (seat.is_small_blind or seat.is_big_blind)):
                if seat.is_small_blind:
                    action = ["bet", self.small_blind_amount]
                else:
                    action = ["bet", self.big_blind_amount]
            else:
                action = self.player_input(player_id = seat.player_id, current_bet = current_bet)
            
            if action[0] == "fold":
                seat.is_occupied = False
                self.player_count -= 1
            elif action[1] < current_bet:
                raise ValueError  # should have been handled by player_input method or frontend
            else:
                current_bet = action[1]
                # update other variables

            self.__log(f"Seat {seat.seat_number} {action[0].upper()} {action[1]}")
            
            if self.player_count < 2:
                remaining = [seat.seat_number for seat in self.seat_list if seat.is_occupied]
                self.__log(f"WINNER DUE TO FOLDS: {remaining} (should only be one)")
                return remaining[0]
                # returns the winner
                # but where will it return to?

            seat = self.seat_list[seat.seat_number % MAXIMUM_SEATS]  # this advances by 1 since seat_number is 1 ahead of index


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


    def player_input(self, player_id, current_bet):
        return [random.choice(["fold", "fold", "fold", "fold", "fold", "check", "call", "bet", "raise"]), round(random.randint(current_bet,1000), 2)]
        # just for testing
    
    def start_round(self, occupied_seats = [1, 2], dealer_seat = 1):  # assign dealer and blinds
        for seat_num in occupied_seats:
            self.seat_list[seat_num - 1].is_occupied = True
        if dealer_seat not in occupied_seats:
            raise IndexError
        
            self.player_count += 1


    def __log(self, to_log):  # self.__log(f"\t = {}\n")       <-- helpful to copy and paste for printing variables
        if LOGS_ENABLED:
            f = open("logs/Table_logs.txt", "a")
            f.write(str(to_log) + "\n")
            f.close()


table = Table()

table.seat_list[5-1].is_dealer = True
table.seat_list[6-1].is_small_blind = True
table.seat_list[7-1].is_big_blind = True
for i in range(10):
    table.player_count += 1
    table.seat_list[i].is_occupied = True

table.play_betting_round()
