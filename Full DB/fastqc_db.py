#!/usr/bin/env python3
from os.path import isfile
from sys import argv

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from FastqcDatabase import FastqcDatabase


def main(dir_path="../test_fastqc_data",
         db_path="../test_fastqc_data/fastqc.db"):
    """
    Assemble a full database of the fastqc_data, with each module occupying its
    own table.
    :return:
    """
    # Check if database exists, and if it doesn't, then request create tables
    database = FastqcDatabase(database_path=db_path, verbose=1)

    if isfile(db_path):
        database.load_from_dir(dir_path, create=False)
    else:
        database.load_from_dir(dir_path, create=True)

    app = Flask(__name__)
    Bootstrap(app)

    @app.route("/")
    def index():
        return render_template('main.html')

    @app.route("/all_results")
    def all():
        all_results = app.fastqc_database.get_all()
        return render_template('display.html',
                               title="All Results",
                               records=all_results)

    @app.route("/fail_results")
    def failed():
        failed_records = app.fastqc_database.get_failed()
        return render_template('display.html',
                               title="Failed Results",
                               records=failed_records)

    @app.route("/pass_results")
    def passed():
        pass_records = app.fastqc_database.get_passed()
        return render_template('display.html',
                               title="Passed Results",
                               records=pass_records)

    @app.route("/warn_results")
    def warned():
        warn_records = app.fastqc_database.get_warned()
        return render_template('display.html',
                               title="Warning Results",
                               records=warn_records)

    @app.route("/passed_modules")
    def modulepassed():
        only_passed = app.fastqc_database.get_only(result='pass')
        return render_template('display.html',
                               title="Only Passing Modules",
                               records=only_passed)

    @app.route("/warned_modules")
    def modulewarned():
        only_warned = app.fastqc_database.get_only(result='warn')
        return render_template('display.html',
                               title="Only Warning Modules",
                               records=only_warned)

    @app.route("/failed_modules")
    def modulefailed():
        only_failed = app.fastqc_database.get_only(result='fail')
        return render_template('display.html',
                               title="Only Failing Modules",
                               records=only_failed)

    app.fastqc_database = database
    app.run('0.0.0.0')


if __name__ == "__main__":
    if len(argv) > 1:
        main(argv[1:])
    else:
        main()
