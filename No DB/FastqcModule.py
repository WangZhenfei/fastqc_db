#!/usr/bin/env python3


class FastqcModule:
    def __init__(self):
        self.name = ""
        self.table_name = ""
        self.result = ""
        self.raw_data = ""
        self.graph_blob = ""

    def populate(self, lines, graph_blob=""):
        header = lines[0].split()
        self.name = "_".join(header[:-1]).replace(">>", "")
        self.table_name = self.name.replace(" ", "_").lower()
        self.result = header[-1]
        self.raw_data = '\n'.join(lines[1:])
        self.graph_blob = graph_blob

    def get_graph(self):
        return self.graph_blob.decode('utf-8')
