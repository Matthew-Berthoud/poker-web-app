class Seat:

    def __init__(self, seat_number):
        self.is_occupied = False
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False

        self.seat_number = seat_number
        self.player_number = 0