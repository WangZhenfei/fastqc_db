#!/usr/bin/env python3
import sys
from collections import OrderedDict
from copy import deepcopy
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
        pass

    def get_all(self):
        return self.fastqc_records

    def get_only(self, result):
        copy_dict = deepcopy(self.fastqc_records)

        for key, val in copy_dict.items():
            for modkey, module in deepcopy(val.modules).items():
                if module.result != result:
                    del (val.modules[modkey])

        return copy_dict

    def get_passed(self):
        passed = OrderedDict()
        for key, val in self.fastqc_records.items():
            has_fail = False
            for module in val.modules.values():
                if module.result == "fail":
                    has_fail = True

            if not has_fail:
                passed[key] = val

        return passed

    def get_warned(self):
        warn = OrderedDict()
        for key, val in self.fastqc_records.items():
            has_warn = False
            for module in val.modules.values():
                if module.result == "warn":
                    has_warn = True

            if has_warn:
                warn[key] = val

        return warn

    def get_failed(self):
        failed = OrderedDict()
        for key, val in self.fastqc_records.items():
            has_fail = False
            for module in val.modules.values():
                if module.result == "fail":
                    has_fail = True

            if has_fail:
                failed[key] = val

        return failed

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
