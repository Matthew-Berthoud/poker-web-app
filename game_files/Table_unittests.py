import unittest
from Table import Table

class Table_Tester(unittest.TestCase):
    def setUp(self):
        self.__table = Table()
        self.__heads_up_table = Table(2)
        self.__five_table = Table(5)



if __name__ == '__main__':
    unittest.main()