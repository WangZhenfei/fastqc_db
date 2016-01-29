#!/usr/bin/env python
import os
import sys
from sequence import Sequence


class Sample():
    def __init__(self, name, path):
        self.name = name
        self._path = path
        self._Sequences = None

    def __populate_sequences(self):
        self._Sequences = []

        for directory in os.listdir(self._path):
            full_dir = os.path.abspath(os.path.join(self._path, directory))

            if os.path.isdir(full_dir):
                try:
                    fastqc_txt = os.path.join(full_dir, "fastqc_data.txt")
                    assert(os.path.isfile(fastqc_txt))
                    sequence = Sequence()
                    sequence.populate(fastqc_txt)
                    self._Sequences.append(sequence)
                except:
                    sys.stderr.write("No fastqc_data.txt file in {},\n".format(
                        full_dir))
                    raise

    def getSequences(self):
        try:
            assert(self._Sequences is None)
            self.__populate_sequences()
        except:
            raise

    def sql_statement(self, table_basic, table_stats):
        sql = ""
        values = []

        for seq in self._Sequences:
            sql = sql + "insert into " + table_basic + " (filename, filetype, \
                encoding, total_sequences, filtered_sequences, sequence_length,\
                percentage_gc) values (%s,%s,%s,%s,%s,%s,%s);\ninsert into "\
                + table_stats + " (overall, per_base_sequence_quality, \
                per_sequence_quality_scores, per_base_sequence_content, \
                per_base_gc_content, per_sequence_gc_content, \
                per_base_n_content, sequence_length_distribution, \
                sequence_duplication_levels, overrepresented_sequences, \
                kmer_content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);\n"

            values.extend([seq.filename, seq.filetype, seq.encoding,
                           seq.total_seqs, seq.filtered_seqs,
                           seq.sequence_length,
                           seq.GC_Content_Percent, seq.stats.Overall,
                           seq.stats.PerBaseSequenceQuality,
                           seq.stats.PerSequenceQuality,
                           seq.stats.PerBaseSequenceContent,
                           seq.stats.PerBaseGCContent,
                           seq.stats.PerSequenceGCContent,
                           seq.stats.PerBaseNContent,
                           seq.stats.SequenceLengthDistribution,
                           seq.stats.SequenceDuplicationLevels,
                           seq.stats.OverrepresentedSequences,
                           seq.stats.KMerContent])

        return [sql, tuple(values)]
