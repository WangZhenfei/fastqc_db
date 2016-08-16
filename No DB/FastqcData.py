#!/usr/bin/env python3
from base64 import b64encode
from os.path import basename
from os.path import splitext
from zipfile import ZipFile

from FastqcModule import FastqcModule


class FastqcData:
    MODULE_GRAPH = {
        'adapter_content': 'adapter_content.png',
        'per_base_n_content': 'per_base_n_content.png',
        'per_sequence_gc_content': 'per_sequence_gc_content.png',
        'sequence_length_distribution': 'sequence_length_distribution.png',
        'sequence_duplication_levels': 'duplication_levels.png',
        'per_base_sequence_quality': 'per_base_quality.png',
        'per_sequence_quality_scores': 'per_sequence_quality.png',
        'kmer_content': 'kmer_profiles.png',
        'per_base_sequence_content': 'per_base_sequence_content.png',
        'per_tile_sequence_quality': 'per_tile_quality.png'
    }  # Dictionary of parsed module names and their graph names

    def __init__(self, fastqc_zip):
        self.fastqc_zip = fastqc_zip

    def parse_modules(cls, fastqc_data_zip=""):
        """
        Return a list of FastqcModule objects that have been populated with
        Module information from the passed lines of a read fastqc_data file
        :param fastqc_data_zip: str: The fastqc zip file
        :return: list<FastqcModule>
        """
        if fastqc_data_zip == "":
            fastqc_data_zip = self.fastqc_zip

        modules = []

        def grouped(iterable, n):
            return zip(*[iter(iterable)] * n)

        with ZipFile(fastqc_data_zip, 'r') as zipfile:
            base = splitext(basename(fastqc_data_zip))[
                0]  # contains same name directory

            module_lines = zipfile.open(
                "{}/fastqc_data.txt".format(base)
            ).readlines()

            _module_lines = list(module_lines)
            module_lines = [line.decode('utf-8') for line in _module_lines]

            idxs = [i for i, x in enumerate(module_lines) if x.startswith(">>")]
            for index_pair in grouped(sorted(idxs), 2):
                # Subset the fastqc data txt file by the module boundaries
                # as delimited by '>>' characters at the beginning of lines.
                # Then, send that information to the module information and
                # use it to create a module object.
                subset_module_lines = module_lines[index_pair[0]:index_pair[1]]
                module = FastqcModule()
                module.populate(subset_module_lines)
                modules += [module]

            # IF this module is known to have a graph, get it and add it
            for module in modules:
                if module.table_name in cls.MODULE_GRAPH.keys():
                    try:
                        module.graph_blob = b64encode(zipfile.open(
                            "{}/Images/{}".format(base,
                                                  cls.MODULE_GRAPH[
                                                      module.table_name
                                                  ])
                        ).read())
                    except KeyError:
                        print("No {} graph found".format(module.table_name))

        return (modules)
