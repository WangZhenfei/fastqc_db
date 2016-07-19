#!/usr/bin/env python3
from sys import argv
from sys import exit

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from FastqcDatabase import FastqcDatabase

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


if __name__ == '__main__':
    database = "fastqc.db"

    if len(argv) != 2:
        print("report.py <database>")
        exit()
    else:
        database = argv[1]

    app.fastqc_database = FastqcDatabase(database)
    app.fastqc_database.load_from_db()
    app.run('0.0.0.0')
