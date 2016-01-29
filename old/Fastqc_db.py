#!/usr/bin/env python
import sqlite3
import os
import sys
import stat
import time
import unittest


class sqlite3_db:
    def __init__(self, database_path, verbose=0):
        self.database_name = database_path
        self.__conn = None
        self.__curs = None
        self.verbose = verbose

    def __connect(self):
        attempts = 0

        while True:
            try:
                attempts += 1
                self.__conn = sqlite3.connect(self.database_name)
            except (sqlite3.Error, OSError) as connection_err:
                if self.verbose > 0:
                    sys.stderr.write("Error connecting: {}\n".format(
                        connection_err))
                    sys.stdout.write("Connection attempts: {}\n".format(
                        attempts))
                if attempts > 10:
                    raise connection_err
                try:
                    os.chmod(self.database_name, stat.I_WRITE)
                except OSError as e:
                    if self.verbose > 0:
                        sys.stderr.write("Could not chmod {}: {}\n".format(
                            self.database_name, e))
                finally:
                    time.sleep(2)
                continue
            break

        if self.verbose > 0:
            sys.stdout.write("Connected to {}\n".format(self.database_name))

    def __cursor(self):
        attempts = 0

        while True:
            try:
                attempts += 1
                self.__curs = self.__conn.cursor()
            except sqlite3.ProgrammingError as err:
                if self.verbose > 0:
                    sys.stderr.write("""sqlite3.ProgrammingError: {}
                                     Attempting to reconnect...
                                     """.format(err))
                if attempts > 3:
                    raise err

                time.sleep(1)
                self.__connect()
                continue
            break

        if self.verbose > 0:
            sys.stdout.write("Acquired {} cursor\n".format(self.database_name))

    def __tuplify(self, an_element):
        if type(an_element) is not None:
            if type(an_element) is not tuple:
                return tuple([an_element])
            else:
                return an_element
        else:
            return an_element

    def __exec_sql(self, sql, values):
        if type(values) is list:
            self.__curs.executemany(sql, [self.__tuplify(x) for x in values])
        elif values is not None:
            self.__curs.execute(sql, self.__tuplify(values))
        else:
            self.__curs.execute(sql)

    def __get_query_result(self, select):
        selection = select.strip().upper()
        try:
            assert(selection in ["ALL", "ONE"])
            if selection == "ALL":
                return self.__curs.fetchall()
            elif selection == "ONE":
                return self.__curs.fetchone()
        except AssertionError:
            raise ValueError("'select' should be 'ALL' or 'ONE'")
        except sqlite3.Error:
            sys.stderr.write("A database error has occurred.\n")

    def execute(self, sql, values=None, select=None):
        try:
            self.__connect()
            self.__cursor()
            query_results = None

            with self.__conn:
                self.__exec_sql(sql, values)
                if select:
                    query_results = self.__get_query_result(select)

            if self.verbose > 0:
                sys.stdout.write("Successfully committed to {}\n".format(
                    self.database_name))

            return query_results
        except sqlite3.IntegrityError as err:
            if self.verbose > 0:
                sys.stderr.write("Error, rollback called: {}\n".format(err))
        except (ValueError, sqlite3.ProgrammingError) as err:
            if self.verbose > 0:
                sys.stderr.write(
                    """Incorrect Parameters passed to API, Syntax Error: {}
                    """.format(err))
            raise err
        finally:
            self.__conn.close()


class test_sqlite3_db(unittest.TestCase):
    def setUp(self):
        self.database = "fastqc_test.db"
        self.db = sqlite3_db(database_path=self.database, verbose=1)
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
            query_results = self.db.execute(sql6, select="kittykat")

        with self.assertRaises(AssertionError):
            query_results = self.db.execute(sql6, select=None)
            assert(query_results is not None)

        query_results = self.db.execute(sql6, select="ALL")
        assert(len(query_results) == 7)
        query_results = self.db.execute(sql6, select="ONE")
        print query_results
        assert(len(query_results) == 2)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(test_sqlite3_db)
    unittest.TextTestRunner(verbosity=3).run(suite)
