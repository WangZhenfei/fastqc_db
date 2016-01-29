#!/usr/bin/env python
import os
import psycopg2
import sys
from sample import Sample
from fastqc_database import FastQC_Database


def Read_FastQC(directory):
    Samples = []

    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            try:
                path = os.path.join(os.path.abspath(directory), item)
                sample = Sample(item, path)
                sample.getSequences()
                Samples.append(sample)
            except:
                print "An error has occurred while processing dir: %s." % item
                continue
    return Samples


def main(directory="./fastqc_results", database_name="Fastqc_Results"):
    Samples = Read_FastQC(directory)
    database_name = os.getenv("FASTQC_DATABASE_NAME") or database_name
    database_user = os.getenv("FASTQC_DATABASE_USER")
    database_pass = os.getenv("FASTQC_DATABASE_PASS")
    database = FastQC_Database(database_name, database_user, database_pass,
                               Samples)
    database.Create_Tables()
    database.Populate_Database()


if __name__ == "__main__":
    main(os.environ.get("FASTQC_DIRECTORY"))
