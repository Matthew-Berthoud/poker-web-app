from Seat import *

class Table:

    def __init__(self, maximum_seats = 10):
        self.seat_list = [Seat(seat_number) for seat_number in range(1, maximum_seats + 1)]
