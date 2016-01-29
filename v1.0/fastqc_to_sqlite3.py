#!/usr/bin/env python
import os
import sys
from sqlite3_db import sqlite3_db


def get_fastqc_files(directory=os.getcwd()):
    fastqc_files = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith("fastqc_data.txt"):
                abs_path = os.path.join(root, filename)
                fastqc_files += [abs_path]

    return fastqc_files

def add_tables(database='fastqc.db'):
    db = sqlite3_db(database_path=database)
    drop_basic = """DROP TABLE IF EXISTS basic;"""
    create_basic= """
    CREATE TABLE basic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filetype TEXT,
        encoding TEXT,
        total_sequences INTEGER,
        filtered_sequences INTEGER,
        sequence_length INTEGER,
        percent_gc INTEGER
    );
    """
    db.execute(drop_basic)
    db.execute(create_basic)
    drop_module_stats = """DROP TABLE IF EXISTS module_stats;"""
    create_module_stats = """
    CREATE TABLE module_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        overall TEXT,
        per_base_sequence_quality TEXT,
        per_sequence_quality_scores TEXT,
        per_base_sequence_content TEXT,
        per_base_gc_content TEXT,
        per_sequence_gc_content TEXT,
        per_base_n_content TEXT,
        sequence_length_distribution TEXT,
        sequence_duplication_levels TEXT,
        overrepresented_sequences TEXT,
        kmer_content TEXT
    );
    """
    db.execute(drop_module_stats)
    db.execute(create_module_stats)


def get_basic(fastqc_filename):
    filename = None
    filetype = None
    encoding = None
    total_sequences = None
    filtered_sequences = None
    sequence_length = None
    percent_gc = None

    with open(fastqc_filename, "r+") as fastqc_h:
        lines = fastqc_h.readlines()
        for line in lines:
            if line.startswith("Filename"):
                filename = " ".join(line.split()[1:])
                continue
            elif line.startswith("File type"):
                filetype = " ".join(line.split()[2:])
                continue
            elif line.startswith("Encoding"):
                encoding = " ".join(line.split()[1:])
                continue
            elif line.startswith("Total Sequences"):
                total_sequences = int(line.split()[-1])
                continue
            elif line.startswith("Filtered Sequences"):
                filtered_seqsuences = int(line.split()[-1])
                continue
            elif line.startswith("Sequence length"):
                sequence_length = int(line.split()[-1])
                continue
            elif line.startswith("%GC"):
               percent_gc = int(line.split()[-1])
               continue
            else:
                pass

        return (filename, filetype, encoding, total_sequences,
                filtered_sequences, sequence_length, percent_gc)


def get_module_stats(fastqc_filename):
    overall = None
    per_base_sequence_quality = None
    per_sequence_quality_scores = None
    per_base_sequence_content = None
    per_base_gc_content = None
    per_sequence_gc_content = None
    per_base_n_content = None
    sequence_length_distribution = None
    sequence_duplication_levels = None
    overreprsented_sequences = None
    kmer_content = None

    with open(fastqc_filename, "r+") as fastqc_h:
        lines = fastqc_h.readlines()
        headers = [line for line in lines if line.startswith(">>") and not
                   line.startswith(">>END_MODULE")]
        for line in headers:
            if line.startswith(">>Basic Statistics"):
                overall = line.split()[-1]
                continue
            if line.startswith(">>Per base sequence quality"):
                per_base_sequence_quality = line.split()[-1]
                continue
            if line.startswith(">>Per sequence quality"):
                per_sequence_quality_scores = line.split()[-1]
                continue
            if line.startswith(">>Per base sequence content"):
                per_base_sequence_content = line.split()[-1]
                continue
            if line.startswith(">>Per base GC content"):
                per_base_gc_content = line.split()[-1]
                continue
            if line.startswith(">>Per sequence GC content"):
                per_sequence_gc_content = line.split()[-1]
                continue
            if line.startswith(">>Per base N content"):
                per_base_n_content = line.split()[-1]
                continue
            if line.startswith(">>Sequence Length Distribution"):
                sequence_length_distribution = line.split()[-1]
                continue
            if line.startswith(">>Sequence Duplication Levels"):
                sequence_duplication_levels = line.split()[-1]
                continue
            if line.startswith(">>Overrepresented sequences"):
                overrepresented_sequences = line.split()[-1]
                continue
            if line.startswith(">>Kmer Content"):
                kmer_content = line.split()[-1]
                continue

        return (overall, per_base_sequence_quality, per_sequence_quality_scores,
                per_base_sequence_content, per_base_gc_content,
                per_sequence_gc_content, per_base_n_content,
                sequence_length_distribution, sequence_duplication_levels,
                overrepresented_sequences, kmer_content)


def basic_sql(filelist, database='fastqc.db'):
    insertions = []
    for filename in filelist:
        insertions.append(get_basic(filename))
    return insertions


def module_stats_sql(filelist, database='fastqc.db'):
    insertions = []
    for filename in filelist:
        insertions.append(get_module_stats(filename))
    return insertions


def populate_db(basic, module_stats, database='fastqc.db'):
    sql_basic = """
        INSERT INTO basic (
            filename,
            filetype,
            encoding,
            total_sequences,
            filtered_sequences,
            sequence_length,
            percent_gc
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """

    sql_module_stats = """
        INSERT INTO module_stats (
            overall,
            per_base_sequence_quality,
            per_sequence_quality_scores,
            per_base_sequence_content,
            per_base_gc_content,
            per_sequence_gc_content,
            per_base_n_content,
            sequence_length_distribution,
            sequence_duplication_levels,
            overrepresented_sequences,
            kmer_content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
    db = sqlite3_db(database_path=database)
    db.execute(sql_basic, basic)
    db.execute(sql_module_stats, module_stats)

def main():
    root_dir = os.environ.get('FASTQC_ROOT') or os.getcwd()
    fastqc_db = os.environ.get('FASTQC_DB_NAME') or 'fastqc.db'
    sys.stdout.write("Getting file list...\n")
    filelist = get_fastqc_files(directory=root_dir)
    sys.stdout.write("Creating tables 'basic' and 'module_stats'...\n")
    add_tables(database=fastqc_db)
    sys.stdout.write("Generating sql statements for 'basic'...\n")
    basic = basic_sql(filelist, database=fastqc_db)
    sys.stdout.write("Generation sql statements for 'module_stats'...\n")
    module_stats = module_stats_sql(filelist, database=fastqc_db)
    sys.stdout.write("Populating database...\n")
    populate_db(basic, module_stats, database=fastqc_db)

if __name__ == "__main__":
    main()
