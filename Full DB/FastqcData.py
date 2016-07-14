#!/usr/bin/env python3
import sqlite3
import sys
from os.path import basename
from zipfile import ZipFile

from FastqcModule import FastqcModule


# TODO: Should the table creation sql ever belong to this class?
# TODO: Ever worthwhile to dynamically detect and add module table names?
# TODO: Cleaner way to parse from fastqc archive?
# TODO: Specify modules top down, with default a list of all modules?
# TODO: perhaps table creation should actually be an instance method?
# TODO: Class CRUD to make SQL efficient for large numbers of instances

class FastqcData:
    MODULE_GRAPH = {
        'key': 'val',
        'key2': 'val2'
    }  # Dictionary of parsed mdoule names and their graph names
    TABLE_NAME = 'fastqc_archive'

    @staticmethod
    def parse_modules(cls, fastqc_data_zip):
        """
        Return a list of FastqcModule objects that have been populated with
        Module information from the passed lines of a read fastqc_data file
        :param fastqc_data_zip: str: The fastqc zip file
        :return: list<FastqcModule>
        """
        modules = []

        def grouped(iterable, n):
            return zip(*[iter(iterable)] * n)

        with ZipFile(fastqc_data_zip, 'r') as zip:
            base = basename(fastqc_data_zip)  # contains same name directory

            module_lines = zip.open(
                "{}/fastqc_data.txt".format(base)
            ).readlines()

            idxs = [i for i, x in enumerate(module_lines) if x.starswith(">>")]
            for index_pair in grouped(sorted(idxs), 2):
                # Subset the fastqc data txt file by the module boundaries
                # as delimited by '>>' characters at the beginning of lines.
                # Then, send that information to the module information and
                # use it to create a module object.
                subset_module_lines = module_lines[index_pair[0]:index_pair[1]]
                modules += [FastqcModule().populate(subset_module_lines)]

            # IF this module is known to have a graph, get it and add it
            for module in modules:
                if module.name in cls.MODULE_GRAPH.keys():
                    module.graph_blob = zip.open(
                        cls.MODULE_GRAPH[module.name]).read()

        return (modules)

    @staticmethod
    def drop_tables_sql(cls, names):
        """
        Generates SQL for tables with name in [names] that have id, result, and
        raw_data as columns with types INTEGER, TEXT, and TEXT
        :param names: names of the tables
        :return: list<str>: SQL for each table
        """
        tables = [("DROP TABLE {table_name} IF EXISTS;").format(cls.TABLE_NAME)]

        def table_sql(n):
            return "DROP TABLE {tab} IF EXISTS;".format(tab=n)

        return tables.extend([table_sql(name) for name in names])

    @staticmethod
    def create_tables_sql(cls, names):
        """
        Generates SQL for tables with name in [names] that have id,
        result, and raw_data as their column names, all of types INTEGER, TEXT,
        and TEXT
        :param names: names of the tables
        :return: list<str>: SQL for each table
        """
        tables = [("CREATE TABLE {table_name} (id INTEGER KEY AUTOINCREMENT,"
                   "file_name TEXT UNIQUE) IF NOT EXISTS;").format(
            cls.TABLE_NAME)]

        def table_sql(n):
            return "CREATE TABLE {tab} (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                result TEXT, raw_data TEXT) IF NOT EXISTS;".format(tab=n)

        return tables.extend([table_sql(name) for name in names])

    def __init__(self, fastqc_file="fastqc_data.txt", version="0.10.1"):
        self.fastqc_file = fastqc_file  # The Zip Archive containing results
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
        for module in FastqcModule.parse_modules(self.fastqc_file):
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
                [x.get_conf() for x in self.__modules.values()])
            return """{fastqc_filename}:{module_stats}""".format(
                fastqc_filename=self.fastqc_file,
                module_stats=module_conformation)
