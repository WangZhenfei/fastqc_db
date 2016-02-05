#!/usr/bin/env python
import sqlite3
import sys


class FastqcData:
    @staticmethod
    def Summarize(fastqc_data_objects):
        # Not exactly sure what to do here, maybe pass off to a
        # well developed summary program or something
        pass

    @staticmethod
    def Create_Tables_SQL():
        pass

    @staticmethod
    def DROP_Tables_SQL():
        pass

    def __init__(self, fastqc_file="fastqc_data.txt", version="0.10.1"):
        self.fastqc_file = fastqc_file
        self.version = version
        self.__modules = {}

    def get_module(self, name):
        try:
            assert (name in self.__modules.keys())
            return self.__modules[name]
        except AssertionError as e:
            sys.stderr.write("The key '{}' was not found.\n".format(e))
            raise e

    def set_module(self, name, value):
        try:
            assert (name in self.__modules.keys())
            self.__modules[name] = value
        except AssertionError as e:
            sys.stderr.write("The key '{}' was not found.\n".format(e))
            raise e

    def read_fastqc_file(self):
        """
        Using the fastqc_data.txt file, create and populate module information
        for this Fastqc_Data.txt object
        :return:
        """
        with open(self.fastqc_file, "r+") as fastqc_file:
            pass  # Population script here

    def insertion_sql(self):
        pass

    def deletion_sql(self):
        pass

    def __conform__(self, protocol):
        """
        Conforms this object for use with data storage / transfer protocols,
        including sqlite3. Makes a structure for each file:
        fastqc_filename:(module_name:result;data;)(module_name:result;data;)...
        in sqlite3.
        :param protocol:
        :return:
        """
        if protocol is sqlite3.PrepareProtocol:
            module_conformation = ''.join(
                [x.get_conf() for x in self.__modules.itervalues()])
            return """{fastqc_filename}:{module_stats}""".format(
                fastqc_filename=self.fastqc_file,
                module_stats=module_conformation)
