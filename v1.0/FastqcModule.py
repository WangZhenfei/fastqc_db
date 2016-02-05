#!/usr/bin/env python
import sqlite3


class FastqcModule:
    def __init__(self, name, result, raw_data):
        self.name = name
        self.result = result
        self.raw_data = raw_data
        self.__table_name = self.name.replace(" ", "_")

    def __conform__(self, protocol):
        """
        Conforms this object for usage with data storage / transfer
        protocols, including sqlite3. Makes a structure for each file:
        (module_name:result;data;) in sqlite3.
        :param protocol:
        :return:
        """
        if protocol is sqlite3.PrepareProtocol:
            return " ({name}:{result};{data};) ".format(
                name=self.name,
                result=self.result,
                data=self.raw_data)

    def get_conf(self, protocol):
        """
        Return the conformation for the given protocol
        :param protocol:
        :return:
        """
        return self.__conform__(protocol)

    def __repr__(self):
        """
        print string representation of module object
        :return:
        """
        return " ({name}:{result};{data};) ".format(
            name=self.name,
            result=self.result,
            data=self.raw_data)
