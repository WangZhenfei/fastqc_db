#!/usr/bin/env python
# Going to parse fastqc files individually and use them to build sqlite3
# compatible objects. The objects will take the place of direct parsing of the
# individual files and thus will eventually be responsible for a large change in
# the script that populates dbs. For now, an empty file. Hopefully, this will
# provide a way to look at the detail information for each fastqc module
# statistic while still maintaing the ability to get a good overview.

# The real challenge will be in writing queries that are informative to the
# underlying problem of assessing the data at the outset of the project. We all
# know how terrible biological data can be!


class Fastqc_data:
    def __init__(filename):
        pass
