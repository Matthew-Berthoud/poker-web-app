import unittest
from Table import Table
LOGS_ENABLED = True

class Table_Tester(unittest.TestCase):
    def setUp(self):
        self.__table = Table()  

    def __log(self, to_log):
        if LOGS_ENABLED:
            f = open("logs/Table_logs.txt", "a")
            f.write(str(to_log) + "\n")
            f.close()

    def test_start_round(self):
        self.__log("========== UNIT TEST CALLED: test_start_round ==========")
        occupied_seats = [1, 2, 4, 5, 8, 9]
        for i in occupied_seats:
            self.__table.seat_list[i-1].occupied = True
        

if __name__ == '__main__':
    unittest.main()