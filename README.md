This is a small project to read fastqc_files into a database and display the
results. Each current option makes a sqlite3 database of results.

The full version creates a DB with the following schema:

    CREATE TABLE fastqc_archive (id INTEGER PRIMARY KEY, file_name TEXT UNIQUE, version TEXT);
    CREATE TABLE basic_statistics (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE per_base_sequence_quality (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE per_tile_sequence_quality (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE per_sequence_quality_scores (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE per_base_sequence_content (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE per_sequence_gc_content (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE per_base_n_content (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE sequence_length_distribution (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE sequence_duplication_levels (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE overrepresented_sequences (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE adapter_content (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);
    CREATE TABLE kmer_content (id INTEGER PRIMARY KEY, result TEXT, raw_data TEXT, graph BLOB);

The results db creates a DB with the schema:

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


The full database also generates a simple Flask application that reads all
zipped files in a direcory and parses them into a table for display. As such,
this application requires Flask to be installed (either on the system, or using
a virtualenv).

Usage:

    python3 Full\ DB/fastqc_db.py <input_root> <database_name.db>

The results DB searches a directory for fastqc_data.txt files and reads them
into a database

Usage:

    python3 Results\ DB/fastqc_results_db.py <input_root> <database_name.db>