#!/usr/bin/env python3
from collections import OrderedDict
from copy import deepcopy
from os import walk
from os.path import join

from FastqcData import FastqcData


class FastqcDatabase():
    def __init__(self, directory="fastqc"):
        self.directory = directory
        self.fastqc_records = OrderedDict()

    def load_from_dir(self, dir_path=None):
        if not dir_path:
            dir_path = self.directory

        for root, directories, filenames in walk(dir_path):
            for filename in filenames:
                if filename.endswith("_fastqc.zip"):
                    path = join(root, filename)
                    data = FastqcData(path)
                    for module in data.parse_modules(path):
                        data.modules[module.table_name] = module
                    self.fastqc_records[data.fastqc_zip] = data

    def get_all(self):
        return self.fastqc_records

    def get_only(self, result):
        copy_dict = deepcopy(self.fastqc_records)

        for key, val in copy_dict.items():
            for modkey, module in deepcopy(val.modules).items():
                if module.result != result:
                    del (val.modules[modkey])

        return copy_dict

    def get(self, result):
        if result == 'all':
            return self.get_all()

        records = OrderedDict()

        for key, val in self.fastqc_records.items():
            has_result = False
            for module in val.modules.values():
                if module.result == result:
                    has_result = True
                    break

            if not has_result:
                records[key] = val

        return records
