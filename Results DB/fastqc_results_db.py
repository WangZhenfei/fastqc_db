#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, "..")
from Sqlite3DB import Sqlite3DB


def get_fastqc_files(directory=os.getcwd()):
    """
    Get fastqc files in the specified directory, by default, current directory
    :param directory: str: path to fastqc directory root
    :return: list<str>: list of file paths
    """
    fastqc_files = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith("fastqc_data.txt"):
                abs_path = os.path.join(root, filename)
                fastqc_files += [abs_path]

    return fastqc_files


def add_tables(database='fastqc.db'):
    """
    Add tables to the database (basic and module stats)
    :param database:
    :return:
    """
    db = Sqlite3DB(database_path=database)
    drop_basic = """DROP TABLE IF EXISTS basic;"""
    create_basic = """
    CREATE TABLE basic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filetype TEXT,
        encoding TEXT,
        total_sequences TEXT,
        filtered_sequences TEXT,
        sequence_length TEXT,
        percent_gc TEXT
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
        per_tile_sequence_quality TEXT,
        per_sequence_quality_scores TEXT,
        per_base_sequence_content TEXT,
        per_sequence_gc_content TEXT,
        per_base_n_content TEXT,
        sequence_length_distribution TEXT,
        sequence_duplication_levels TEXT,
        overrepresented_sequences TEXT,
        adapter_content TEXT,
        kmer_content TEXT
    );
    """
    db.execute(drop_module_stats)
    db.execute(create_module_stats)


def get_basic(fastqc_filename):
    """
    Gather basic information to the file
    :param fastqc_filename: filename for the fastqc data file
    :return: tuple(<str>): values
    """
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
                total_sequences = line.split()[-1]
                continue
            elif line.startswith("Filtered Sequences"):
                filtered_sequences = line.split()[-1]
                continue
            elif line.startswith("Sequence length"):
                sequence_length = line.split()[-1]
                continue
            elif line.startswith("%GC"):
                percent_gc = line.split()[-1]
                continue
            else:
                pass

        return (filename,
                filetype,
                encoding,
                total_sequences,
                filtered_sequences,
                sequence_length,
                percent_gc)


def get_module_stats(fastqc_filename):
    """
    Gather module statistics information
    :param fastqc_filename: fastqc_data file
    :return: tuple(<str>): values
    """
    overall = None
    per_base_sequence_quality = None
    per_tile_sequence_quality = None
    per_sequence_quality_scores = None
    per_base_sequence_content = None
    per_sequence_gc_content = None
    per_base_n_content = None
    sequence_length_distribution = None
    sequence_duplication_levels = None
    overrepresented_sequences = None
    adapter_content = None
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
            if line.startswith(">>Per tile sequence quality"):
                per_tile_sequence_quality = line.split()[-1]
                continue
            if line.startswith(">>Per sequence quality"):
                per_sequence_quality_scores = line.split()[-1]
                continue
            if line.startswith(">>Per base sequence content"):
                per_base_sequence_content = line.split()[-1]
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
            if line.startswith(">>Adapter Content"):
                adapter_content = line.split()[-1]
                continue
            if line.startswith(">>Kmer Content"):
                kmer_content = line.split()[-1]
                continue

        return (overall,
                per_base_sequence_quality,
                per_tile_sequence_quality,
                per_sequence_quality_scores,
                per_base_sequence_content,
                per_sequence_gc_content,
                per_base_n_content,
                sequence_length_distribution,
                sequence_duplication_levels,
                overrepresented_sequences,
                adapter_content,
                kmer_content)


def basic_sql(filelist):
    """
    For each fastqc file, get basic information
    :param filelist: fastqc_data file list
    :return: list<tuple<str>>: list of insertions
    """
    insertions = []
    for filename in filelist:
        insertions += [get_basic(filename)]
    return insertions


def module_stats_sql(filelist):
    """
    For each fastqc file, get module stats
    :param filelist: fastqc_data file list
    :return: list<tuple<str>>: list of insertions
    """
    insertions = []
    for filename in filelist:
        insertions.append(get_module_stats(filename))
    return insertions


def populate_db(basic, module_stats, database='fastqc.db'):
    """
    Populate the database using the values scraped from the fastqc_data files
    :param basic: <list>: list of basic sql values
    :param module_stats: <list>: list of module stats values
    :param database: <str>: name of databases (can be path)
    :return:
    """
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
            per_tile_sequence_quality,
            per_sequence_quality_scores,
            per_base_sequence_content,
            per_sequence_gc_content,
            per_base_n_content,
            sequence_length_distribution,
            sequence_duplication_levels,
            overrepresented_sequences,
            adapter_content,
            kmer_content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
    db = Sqlite3DB(database_path=database)
    db.execute(sql_basic, basic)
    db.execute(sql_module_stats, module_stats)


def main(args):
    """
    Create a database of the results of the fastqc_data files in the directory
    located at FASTQC_ROOT or the current working directory. The database name
    is FASTQC_DB_NAME or 'fastqc.db'. Makes tables, add module test results to
    the tables
    :return:
    """
    root_dir = ""
    fastqc_db = ""

    if len(args) != 3:
        print("fastqc_results_db.py <fastqc_root> <database_name>")
    else:
        root_dir = args[1]
        fastqc_db = args[2]
        print("Getting file list...\n", file=sys.stdout)
        filelist = get_fastqc_files(directory=root_dir)
        print("Creating tables 'basic' and 'module_stats'...\n",
              file=sys.stdout)
        add_tables(database=fastqc_db)
        print("Generating sql statements for 'basic'...\n", file=sys.stdout)
        basic = basic_sql(filelist)
        print("Generation sql statements for 'module_stats'...\n",
              file=sys.stdout)
        module_stats = module_stats_sql(filelist)
        print("Populating database...\n", file=sys.stdout)
        populate_db(basic, module_stats, database=fastqc_db)


if __name__ == "__main__":
    main(sys.argv)
