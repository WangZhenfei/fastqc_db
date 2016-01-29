#!/usr/bin/env python
from status import Status


class Sequence():
    def __init__(self):
        self.filename = None
        self.filetype = None
        self.encoding = None
        self.total_seqs = None
        self.filtered_seqs = None
        self.sequence_length = None
        self.GC_Content_Percent = None
        self.stats = Status()

    def __getInformation(self, lines):
        # Read the fastqc file and gather the information into attributes of
        # this class. For use in population of database or in working with the
        # results in other ways
        for line in lines:
            if line.startswith("Filename"):
                self.filename = " ".join(line.split()[1:])
            elif line.startswith("File type"):
                self.filetype = " ".join(line.split()[2:])
            elif line.startswith("Encoding"):
                self.encoding = " ".join(line.split()[1:])
            elif line.startswith("Total Sequences"):
                self.total_seqs = line.split()[-1]
            elif line.startswith("Filtered Sequences"):
                self.filtered_seqs = line.split()[-1]
            elif line.startswith("Sequence length"):
                self.sequence_length = line.split()[-1]
            elif line.startswith("%GC"):
                self.GC_Content_Percent = line.split()[-1]
            else:
                pass

    def __getStats(self, lines):
        Module_headers = [line for line in lines if line.startswith(">>") and
                          not line.startswith(">>END_MODULE")]

        for line in Module_headers:
            if line.startswith(">>Basic Statistics"):
                self.stats.Overall = line.split()[-1]
            if line.startswith(">>Per base sequence quality"):
                self.stats.PerBaseSequenceQuality = line.split()[-1]
            if line.startswith(">>Per sequence quality"):
                self.stats.PerSequenceQuality = line.split()[-1]
            if line.startswith(">>Per base sequence content"):
                self.stats.PerBaseSequenceContentS = line.split()[-1]
            if line.startswith(">>Per base GC content"):
                self.stats.PerBaseGCContent = line.split()[-1]
            if line.startswith(">>Per sequence GC content"):
                self.stats.PerSequenceGCContent = line.split()[-1]

    def __getStats2(self, lines):
        Module_headers = [line for line in lines if line.startswith(">>") and
                          not line.startswith(">>END MODULE")]

        for line in Module_headers:
            if line.startswith(">>Per base N content"):
                self.stats.PerBaseNContent = line.split()[-1]
            if line.startswith(">>Sequence Length Distribution"):
                self.stats.SequenceLengthDistribution = line.split()[-1]
            if line.startswith(">>Sequence Duplication Levels"):
                self.stats.SequenceDuplicationLevels = line.split()[-1]
            if line.startswith(">>Overrepresented sequences"):
                self.stats.OverrepresentedSequences = line.split()[-1]
            if line.startswith(">>Kmer Content"):
                self.stats.KMerContent = line.split()[-1]

    def populate(self, fastqc_txt):
        try:
            file_handle = open(fastqc_txt, 'r+')
            lines = file_handle.readlines()
            self.__getInformation(lines)
            self.__getStats(lines)
            self.__getStats2(lines)
        except:
            raise
