#!/usr/bin/env python
from __future__ import print_function

import os
import sqlite3
import stat
import sys
import unittest

from Sqlite3DB import Sqlite3DB


class TestSqlite3DB(unittest.TestCase):
    def setUp(self):
        self.database = "test.db"
        self.db = Sqlite3DB(database_path=self.database, verbose=1)
        sys.stdout.write("\nLeaving setUp...\n")

    def tearDown(self):
        try:
            os.chmod(self.database, stat.S_IWRITE)
            os.remove(self.database)
        except OSError as err:
            sys.stderr.write("Could not chmod/rm test db: {}\n".format(err))
        finally:
            sys.stdout.write("Leaving tearDown...\n")

    def test_execute_1(self):
        sql1 = "CREATE TABLE test_table_name (id INTEGER PRIMARY KEY \
                AUTOINCREMENT, txt TEXT);"
        self.db.execute(sql1)

    def test_execute_2(self):
        sql1 = "CREATE TABLE test_table_name (id INTEGER PRIMARY KEY \
            AUTOINCREMENT, txt TEXT);"
        sql2 = "ravioli ravioli, give me the formuoli"

        with self.assertRaises(sqlite3.OperationalError):
            self.db.execute(sql1)
            self.db.execute(sql2)

    def test_execute_3(self):
        sql1 = "CREATE TABLE test_table_name (id INTEGER PRIMARY KEY \
            AUTOINCREMENT, txt TEXT);"
        sql3 = "INSERT INTO test_table_name (txt) VALUES ('test')"
        self.db.execute(sql1)
        self.db.execute(sql3)

    def test_execute_4(self):
        sql1 = "CREATE TABLE test_table_name (id INTEGER PRIMARY KEY \
            AUTOINCREMENT, txt TEXT);"
        sql4 = "INSERT INTO test_table_name (txt) VALUES (?);"
        values1 = "mom's spaghetti"
        values2 = "just spaghetti, this time"
        values3 = "maybe a little bokkadabeppo too"
        self.db.execute(sql1)
        self.db.execute(sql4, values1)
        self.db.execute(sql4, values2)
        self.db.execute(sql4, values3)

    def test_execute_5(self):
        sql1 = "CREATE TABLE test_table_name (id INTEGER PRIMARY KEY \
            AUTOINCREMENT, txt TEXT);"
        sql4 = "INSERT INTO test_table_name (txt) VALUES (?)"
        values1 = ["red", "orange", "yellow", "green", "blue",
                   "indigo", "violet"]
        self.db.execute(sql1)
        self.db.execute(sql4, values1)

    def test_execute_6(self):
        sql1 = "CREATE TABLE test_table_name (id INTEGER PRIMARY KEY \
            AUTOINCREMENT, txt TEXT);"
        sql4 = "INSERT INTO test_table_name (txt) VALUES (?)"
        sql6 = "SELECT * FROM test_table_name;"
        values1 = "mom's spaghetti"
        values2 = ["red", "orange", "yellow", "green", "blue",
                   "indigo", "violet"]
        self.db.execute(sql1)
        self.db.execute(sql4, values1)
        self.db.execute(sql4, values2)
        self.db.execute(sql6)

    def test_execute_7(self):
        sql1 = "CREATE TABLE test_table_name (id INTEGER PRIMARY KEY \
            AUTOINCREMENT, txt TEXT);"
        sql4 = "INSERT INTO test_table_name (txt) VALUES (?)"
        sql6 = "SELECT * FROM test_table_name;"
        values2 = ["red", "orange", "yellow", "green", "blue",
                   "indigo", "violet"]
        self.db.execute(sql1)
        self.db.execute(sql4, values2)

        with self.assertRaises(ValueError):
            self.db.execute(sql6, select="kittykat")

        with self.assertRaises(AssertionError):
            query_results = self.db.execute(sql6, select=None)
            assert (query_results is not None)

        query_results = self.db.execute(sql6, select="ALL")
        assert (len(query_results) == 7)
        print(query_results)
        query_results = self.db.execute(sql6, select="ONE")
        print(query_results)
        assert (len(query_results) == 2)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSqlite3DB)
    unittest.TextTestRunner(verbosity=3).run(suite)
