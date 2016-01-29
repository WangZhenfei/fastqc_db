#!/usr/bin/env python
import psycopg2
import sys


class FastQC_Database:

    def __init__(self, database_name, database_user, database_pass,
                 Samples=None):
        self.database_name = database_name
        self.database_user = database_user
        self.database_pass = database_pass
        self.basic = "basic"
        self.stats = "advanced"
        self.Samples = Samples
        self.connection = None
        self.cursor = None

    def __connect(self):
        try:
            self.connection = psycopg2.connect("dbname={} \
                                               user={} \
                                               password={}".format(
                    self.database_name, self.database_user, self.database_pass))
            self.cursor = self.connection.cursor()
        except Exception as e:
            sys.stderr.write("Exception while connecting: %s\n" % str(e))
            self.__close()
            raise

    def __exec_sql(self, sql, values):
        try:
            self.__connect()
            self.cursor.execute(sql, values)
        except:
            sys.stderr.write("Could not execute sql statement.\n")
            raise
        finally:
            self.__close()

    def __close(self):
        if self.cursor is not None:
            try:
                self.cursor.close()
            except:
                sys.stdout.write("Could not close cursor object\n")
                raise

        if self.connection is not None:
            try:
                self.connection.commit()
                self.connection.close()
            except Exception as e:
                print str(e)
                raise

        self.cursor = None
        self.connection = None

    def exec_sql(self, sql, values=None):
        self.__exec_sql(sql, values)

    def Create_Tables(self):
        sql = "drop table if exists {basic};\ncreate table {basic} (id \
            serial primary key, filename text, filetype text, encoding \
            text, total_sequences text, filtered_sequences text, \
            sequence_length text, percentage_gc smallint);\n\
            drop table if exists {adv};\ncreate table {adv} (id serial \
            primary key, overall text, per_base_sequence_quality text, \
            per_sequence_quality_scores text, per_base_sequence_content \
            text, per_base_gc_content text, per_sequence_gc_content \
            text, per_base_n_content text, sequence_length_distribution \
            text, sequence_duplication_levels text, \
            overrepresented_sequences text, kmer_content text);".format(
                basic=self.basic, adv=self.stats)
        self.__exec_sql(sql, (None,))

    def Populate_Database(self):
        for sample in self.Samples:
            sql_values = sample.sql_statement(self.basic, self.stats)
            self.__exec_sql(sql_values[0], sql_values[1])
