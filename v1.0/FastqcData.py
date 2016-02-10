#!/usr/bin/env python
from __future__ import print_function

import sqlite3
import sys
from itertools import izip

from FastqcModule import FastqcModule


class FastqcData:
    @staticmethod
    def parse_modules(module_lines):
        """
        Return a list of FastqcModule objects that have been populated with
        Module information from the passed lines of a read fastqc_data file
        :param module_lines: list: Lines of the fastqc_data file
        :return: list<FastqcModule>
        """

        def grouped(iterable, n):
            return izip(*[iter(iterable)] * n)

        modules = []
        indices = [i for i, x in enumerate(module_lines) if x.starswith(">>")]

        for index_pair in grouped(sorted(indices), 2):
            subset_module_lines = module_lines[index_pair[0]:index_pair[1]]
            modules += [FastqcModule().populate(subset_module_lines)]
        return modules

    @staticmethod
    def drop_tables_sql(names):
        """
        Generates SQL for tables with name in [names] that have id, result, and
        raw_data as columns with types INTEGER, TEXT, and TEXT
        :param names: names of the tables
        :return: list<str>: SQL for each table
        """
        tables = [("DROP TABLE file IF EXISTS;")]

        def table_sql(n):
            return "DROP TABLE {tab} IF EXISTS;".format(tab=n)

        return tables.extend([table_sql(name) for name in names])

    @staticmethod
    def create_tables_sql(names):
        """
        Generates SQL for tables with name in [names] that have id,
        result, and raw_data as their column names, all of types INTEGER, TEXT,
        and TEXT
        :param names: names of the tables
        :return: list<str>: SQL for each table
        """
        tables = [("CREATE TABLE file (id INTEGER KEY AUTOINCREMENT,"
                   "file_name TEXT UNIQUE) IF NOT EXISTS;")]

        def table_sql(n):
            return "CREATE TABLE {tab} (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                result TEXT, raw_data TEXT) IF NOT EXISTS;".format(tab=n)

        return tables.extend([table_sql(name) for name in names])

    def __init__(self, fastqc_file="fastqc_data.txt", version="0.10.1"):
        self.fastqc_file = fastqc_file
        self.version = version
        self.__modules = {}

    def get_module(self, name):
        try:
            return self.__modules[name]
        except KeyError as e:
            print("FastqcData object has no key {}".format(e), file=sys.stderr)
            raise e

    def set_module(self, name, value):
        try:
            assert (type(value) is FastqcModule)
            self.__modules[name] = value
        except KeyError as e:
            print("FastqcData object has no key {}".format(e), file=sys.stderr)
            raise e
        except AssertionError as e:
            print("set_module(FastqcModule) type mismatch: {}".format(e),
                  file=sys.stderr)

    def populate_from_file(self):
        """
        Using the fastqc_data file, create and populate module information
        :return:
        """
        with open(self.fastqc_file, "r+") as fastqc_file:
            fastqc_content = fastqc_file.readlines()
            for module in FastqcData.parse_modules(fastqc_content):
                self.__modules[module.name] = module

    def insertion_sql(self):
        """
        Generate a single SQL statement with wildcard notation and a list of
        values in tuples that can be inserted via SQLite3's python interface
        The stored tuples can be inserted directly using the sqlite3 module
        :return: list<tuple(str, tuple(str,str))>: insertion sql for this file
        """
        sql_statements = []
        for module in self.__modules:
            sql_statements += [module.insertion_sql()]

        return sql_statements

    def update_sql(self, modules, values):
        """
        SQL to Update this item
        TODO: how to do this?
        :modules: TODO
        :values: TODO
        :return:
        """
        pass

    def select_sql(self, mode):
        """
        SQL to select this object from DB
        :param mode: TODO
        :return: TODO
        """
        pass


    def deletion_sql(self):
        """
        Generate a single SQL statement with wildcard notation and a list of
        values in tuples that can be deleted via SQLite3's python interface
        :return: list<str>: deletion sql for this file
        """
        sql_statements = []
        for module in self.__modules:
            sql_statements += [module.deletion_sql()]

        return sql_statements

    def __conform__(self, protocol):
        """
        Conforms this object for use with data storage / transfer protocols,
        including sqlite3. Makes a structure for each file:
        fastqc_filename:(module_name:result;data;)(module_name:result;data;)...
        in sqlite3.
        :param protocol: The data transfer protocol to be used
        :return: str: protocol representation of this object
        """
        if protocol is sqlite3.PrepareProtocol:
            module_conformation = ''.join(
                [x.get_conf() for x in self.__modules.itervalues()])
            return """{fastqc_filename}:{module_stats}""".format(
                fastqc_filename=self.fastqc_file,
                module_stats=module_conformation)
