#!/usr/bin/env python3
import sys

sys.path.insert(0, "..")
from Sqlite3DB import Sqlite3DB


class FastqcDatabases(Sqlite3DB):
    def __init__(self, database_name, verbose=0):
        self.database_name = database_name

    def insert(self, fastqc_data_obj):
        """
        Insert a single fastqc_data object into the current database
        :param: str: the path to the data object to be inserted into the database
        :return:
        """
        pass

    def delete(self, fastqc_data_obj):
        """
        Delete a single fastqc_data object into the current database
        :param: str: the path to the data object to be deleted from the database
        :return:
        """
        pass

    def insert_multiple(self, fastqc_data_objects):
        """
        Insert multiple fastqc_data objects in the current database
        :param: fastqc_data_objects: list: list of paths to these objects
        :return:
        """
        pass

    def delete_multiple(self, fastqc_data_objects):
        """
        Delete multiple fastqc objects in the current database
        :param: fastqc_data_objects: list: list of paths to these objects
        :return:
        """
        pass

    def update(self, fastqc_data_obj):
        """
        Update a single fastqc_data object in the current database
        :param: str: the path to the data object to be updated in the database
        :return:
        """
        pass

    def update_multiple(self, fastqc_data_objects):
        """
        update multiple fastqc objects in the current database
        :param: str: list: list of paths to these objects
        :return:
        """
        pass
