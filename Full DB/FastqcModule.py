#!/usr/bin/env python
import sqlite3


class FastqcModule:
    def __init__(self):
        self.name = None
        self.table_name = None
        self.result = None
        self.raw_data = None
        self.graph_blob = None

    def populate(self, lines, graph_blob=""):
        header = lines[0].split()
        self.name = "_".join(header[:-1]).replace(">>", "")
        self.table_name = self.name.replace(" ", "_")
        self.result = header[-1]
        self.raw_data = lines[1:].join('\n')
        self.graph_blob = graph_blob

    def insertion_sql(self):
        return ["INSERT INTO {} VALUES (?, ?, ?);".format(self.table_name),
                (self.result, self.raw_data, self.graph_blob)]

    def deletion_sql(self):
        return [("DELETE FROM {} "
                 "WHERE result = ? AND raw_data = ? AND graph = ?;").format(
            self.table_name), (self.result, self.raw_data, self.graph_blob)]

    def __conform__(self, protocol):
        """
        Conforms this object for usage with data storage / transfer
        protocols, including sqlite3. Makes a structure for each file:
        (module_name:result;data;) in sqlite3.
        :param protocol:
        :return:
        """
        if protocol is sqlite3.PrepareProtocol:
            return " ({name}:{result};{data};{blob}) ".format(
                name=self.name,
                result=self.result,
                data=self.raw_data,
                blob=self.graph_blob
            )  # conform

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
        return " ({name}:{result};{data};{blob}) ".format(
            name=self.name,
            result=self.result,
            data=self.raw_data,
            blob=self.graph_blob
        )  # repr
