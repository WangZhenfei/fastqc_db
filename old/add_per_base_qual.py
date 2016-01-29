#!/usr/bin/env python
import os
from fastqc_database import FastQC_Database


def find_fastqc_files(directory="fastqc_results"):
    paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith("fastqc_data.txt"):
                abs_path = os.path.join(root, filename)
                paths.append(abs_path)

    return paths


def find_indices(filename):
    with open(filename, 'r+') as fastqc_data:
        lines = fastqc_data.readlines()
        start_index = -1
        end_index = -1

        for index, line in enumerate(lines):
            if line.startswith(">>Per base sequence quality"):
                start_index = index
            if line.startswith(">>END_MODULE") and index != len(lines) and \
                lines[index + 1].startswith(">>Per sequence quality"):
                end_index = index
                break

        start_index = start_index + 2 # skip header and comments
        assert(start_index < end_index)
        return (start_index, end_index)


def count_lower_quartile_failures(filename, indices):
    with open(filename, "r+") as fastqc_data:
        lines = fastqc_data.readlines()

        count = 0
        for line in lines[indices[0]:indices[1]]:
            cols = line.split()
            if float(cols[3]) <= 20:  # lower quartile <= 20 phred
                count += 1

        return count

def get_filename(filename):
    # retrieving the fastq filename from a fastq_data.txt file
    with open(filename, "r+") as fastqc_data:
        lines = fastqc_data.readlines()
        for line in lines:
            if line.startswith("Filename"):
                return line.split()[-1]



def main(directory=".fastqc_results", database_name="Fastqc_Results"):
    database_name = os.getenv("FASTQC_DATABASE_NAME") or database_name
    database_user = os.getenv("FASTQC_DATABASE_USER")
    database_pass = os.getenv("FASTQC_DATABASE_PASS")
    db = FastQC_Database(database_name, database_user, database_pass)
    table_name = 'per_base_quality'
    create_table = "drop table if exists {tab}; create table {tab} \
        (id serial primary key, filename text, seq_count smallint, \
        per_base_sequence_quality text);".format(tab=table_name)
    db.exec_sql(create_table)
    fastqc_files = find_fastqc_files(directory=os.getenv("FASTQC_DIRECTORY"))

    for filename in fastqc_files:
        indices = find_indices(filename)
        count = count_lower_quartile_failures(filename, indices)
        result = 'pass' if (count <= 1) else 'fail'
        fastq_filename = get_filename(filename)
        sql = "insert into {tab} (filename, seq_count, \
            per_base_sequence_quality) values (%s, %s, %s)".format(
                tab=table_name)
        values = (fastq_filename, count, result)
        db.exec_sql(sql, values)


if __name__ == "__main__":
    main()
