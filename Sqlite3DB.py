#!/usr/bin/env python
import os
import sqlite3
import stat
import sys
import time


class Sqlite3DB:
    def __init__(self, database_path, verbose=0):
        self.database_name = database_path
        self.__conn = None
        self.__curs = None
        self.verbose = verbose

    @staticmethod
    def __tuplify(an_element):
        if type(an_element) is not None:
            if type(an_element) is not tuple:
                return tuple([an_element])
            else:
                return an_element
        else:
            return an_element

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
                    os.chmod(self.database_name, stat.S_IWRITE)
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
            assert (selection in ["ALL", "ONE"])
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
