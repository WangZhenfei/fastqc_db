#!/usr/bin/env python
from Sqlite3DB import Sqlite3DB


class FastqcDatabases(Sqlite3DB):
    def insert(self, fastqc_data):
        """
        Insert a single fastqc_data file into the current database
        :param: str: the path to the data file to be inserted into the database
        :return:
        """
        pass

    def delete(self, fastqc_data):
        """
        Delete a single fastqc_data file into the current database
        :param: str: the path to the data file to be deleted from the database
        :return:
        """
        pass

    def insert_multiple(self, fastqc_data_files):
        """
        Insert multiple fastqc_data files in the current database
        :param: fastqc_data_files: list: list of paths to these files
        :return:
        """
        pass

    def delete_multiple(self, fastqc_data_files):
        """
        Delete multiple fastqc files in the current database
        :param: fastqc_data_files: list: list of paths to these files
        :return:
        """
        pass

    def update(self, fastqc_data):
        """
        Update a single fastqc_data file in the current database
        :param: str: the path to the data file to be updated in the database
        :return:
        """
        pass

    def update_multiple(self, fastqc_data_files):
        """
        update multiple fastqc files in the current database
        :param: str: list: list of paths to these files
        :return:
        """
        pass
