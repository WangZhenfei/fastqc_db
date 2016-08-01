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
                    data.populate_from_file()
                    self.fastqc_records[data.fastqc_file] = data

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
