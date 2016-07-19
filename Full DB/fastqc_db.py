#!/usr/bin/env python3
from os.path import isfile
from sys import argv

from FastqcDatabase import FastqcDatabase


def main(db_path="../test_fastqc_data/fastqc.db",
         dir_path="../test_fastqc_data"):
    """
    Assemble a full database of the fastqc_data, with each module occupying its
    own table.
    :return:
    """
    # Check if database exists, and if it doesn't, then request create tables
    if isfile(db_path):
        print("Using existing database")
        database = FastqcDatabase(database_path=db_path, verbose=1)
        database.load_from_dir(dir_path, create=False)
    else:
        print("Creating database")
        database = FastqcDatabase(database_path=db_path, verbose=1)
        database.load_from_dir(dir_path, create=True)

if __name__ == "__main__":
    if len(argv) > 1:
        main(argv[1:])
    else:
        main()
