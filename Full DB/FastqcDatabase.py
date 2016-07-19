#!/usr/bin/env python3
import sys
from collections import OrderedDict

sys.path.insert(0, "..")
from Sqlite3DB import Sqlite3DB
from FastqcData import FastqcData
from os.path import join
from os import walk


# TODO: use actual db models and population with versions to manage the data


class FastqcDatabase(Sqlite3DB):
    def __init__(self, database_path, verbose=0):
        super().__init__(database_path, verbose)
        self.fastqc_records = OrderedDict()

    def load_from_dir(self, dir_path, create=False):
        created = False

        for root, directories, filenames in walk(dir_path):
            for filename in filenames:
                if filename.endswith("_fastqc.zip"):
                    path = join(root, filename)
                    data = FastqcData(path)
                    data.populate_from_file()

                    if create and not created:
                        created = True
                        print("Creating Tables")
                        self.create_db(data=data)

                    self.insert(data)

    def load_from_db(self):
        # TODO: populate fastqc_records from an already created database
        pass

    def get_all(self):
        # TODO
        return OrderedDict()

    def get_passed(self):
        # TODO
        return OrderedDict()

    def get_warned(self):
        # TODO
        return OrderedDict()

    def get_failed(self):
        # TODO
        return OrderedDict()

    def __remove_record(self, key):
        try:
            d = OrderedDict(self.fastqc_records)
            del d[key]
            self.fastqc_records = d
        except KeyError:
            print("Record {} not found in fastqc records".format(key))

    def create_db(self, data):
        for sql_val in data.create_tables_sql():
            self.execute(sql_val)

    def insert(self, fastqc_data_obj):
        """
        Insert a single fastqc_data object into the current database
        :param: str: the path to the data object to be inserted into the database
        :return:
        """
        for sql_vals in fastqc_data_obj.insertion_sql():
            self.execute(sql_vals[0], values=sql_vals[1])
            self.fastqc_records[fastqc_data_obj.fastqc_file] = fastqc_data_obj

    def delete(self, fastqc_data_obj):
        """
        Delete a single fastqc_data object into the current database
        :param: str: the path to the data object to be deleted from the database
        :return:
        """
        for sql_vals in fastqc_data_obj.deletion_sql():
            self.execute(sql_vals[0], values=sql_vals[1])
            self.__remove_record(fastqc_data_obj.fastqc_file)
