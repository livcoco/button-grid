#!/usr/bin/python3
from src.button-grid.database.qlite3Database import DatabaseInterface

import unittest

class DatabaseTest(unittest):
    def setup(self):
        pass
    def test_00_instantiate(self):
        db = Sqlite3Database()

if __name__ == '__main__':
    unittest.main()
