#!/usr/bin/env python3
import sys
from base64 import b64encode
from collections import OrderedDict
from os.path import basename
from os.path import splitext
from zipfile import ZipFile

from FastqcModule import FastqcModule


# TODO: Add Update and Select operations

class FastqcData:
    MODULE_GRAPH = {
        'adapter_content': 'adapter_content.png',
        'per_base_n_content': 'per_base_n_content.png',
        'per_sequence_gc_content': 'per_sequence_gc_content.png',
        'sequence_length_distribution': 'sequence_length_distribution.png',
        'sequence_duplication_levels': 'duplication_levels.png',
        'per_base_sequence_quality': 'per_base_quality.png',
        'per_sequence_quality_scores': 'per_sequence_quality.png',
        'kmer_content': 'kmer_profiles.png',
        'per_base_sequence_content': 'per_base_sequence_content.png',
        'per_tile_sequence_quality': 'per_tile_quality.png'
    }  # Dictionary of parsed module names and their graph names

    TABLE_NAME = 'fastqc_archive'

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

        with ZipFile(fastqc_data_zip, 'r') as zipfile:
            base = splitext(basename(fastqc_data_zip))[
                0]  # contains same name directory

            module_lines = zipfile.open(
                "{}/fastqc_data.txt".format(base)
            ).readlines()

            _module_lines = list(module_lines)
            module_lines = [line.decode('utf-8') for line in _module_lines]

            idxs = [i for i, x in enumerate(module_lines) if x.startswith(">>")]
            for index_pair in grouped(sorted(idxs), 2):
                # Subset the fastqc data txt file by the module boundaries
                # as delimited by '>>' characters at the beginning of lines.
                # Then, send that information to the module information and
                # use it to create a module object.
                subset_module_lines = module_lines[index_pair[0]:index_pair[1]]
                module = FastqcModule()
                module.populate(subset_module_lines)
                modules += [module]

            # IF this module is known to have a graph, get it and add it
            for module in modules:
                if module.table_name in cls.MODULE_GRAPH.keys():
                    try:
                        module.graph_blob = b64encode(zipfile.open(
                            "{}/Images/{}".format(base,
                                                  cls.MODULE_GRAPH[
                                                      module.table_name
                                                  ])
                        ).read())
                    except KeyError:
                        print("No {} graph found".format(module.table_name))

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

    def create_tables_sql(self):
        """
        Generates SQL for tables with name in [names] that have id,
        result, and raw_data as their column names, all of types INTEGER, TEXT,
        and TEXT
        :param names: names of the tables
        :return: list<str>: SQL for each table
        """
        tables = [("CREATE TABLE IF NOT EXISTS {table_name} "
                   "(id INTEGER PRIMARY KEY, file_name TEXT UNIQUE, "
                   "version TEXT);").format(table_name=self.TABLE_NAME)]

        def table_sql(n):
            return ("CREATE TABLE IF NOT EXISTS {tab} (id INTEGER PRIMARY KEY, "
                    "result TEXT, raw_data TEXT, graph BLOB);").format(tab=n)

        tables.extend([table_sql(name) for name in self.module_names()])
        return tables

    def __init__(self, fastqc_file="data_fastqc.zip", version="0.11.5"):
        self.fastqc_file = fastqc_file  # The Zip Archive containing results
        self.version = version
        self.modules = OrderedDict()

    def module_names(self):
        return [x.table_name for x in self.modules.values()]

    def get_module(self, name):
        try:
            return self.modules[name]
        except KeyError as e:
            print("FastqcData object has no key {}".format(e), file=sys.stderr)
            raise e

    def set_module(self, name, value):
        try:
            assert (type(value) is FastqcModule)
            self.modules[name] = value
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
        for module in self.parse_modules(self.fastqc_file):
            self.modules[module.name] = module

    def insertion_sql(self):
        """
        Generate a single SQL statement with wildcard notation and a list of
        values in tuples that can be inserted via SQLite3's python interface
        The stored tuples can be inserted directly using the sqlite3 module
        :return: list<tuple(str, tuple(str,str))>: insertion sql for this file
        """
        sql_statements = []
        for module in self.modules.values():
            sql_statements += [module.insertion_sql()]

        return sql_statements


    def deletion_sql(self):
        """
        Generate a single SQL statement with wildcard notation and a list of
        values in tuples that can be deleted via SQLite3's python interface
        :return: list<str>: deletion sql for this file
        """
        sql_statements = []
        for module in self.modules:
            sql_statements += [module.deletion_sql()]

        return sql_statements