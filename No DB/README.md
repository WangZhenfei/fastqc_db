simply run ./fastqc_report.py <fastqc_directory>

This script will descend into the directory, collect the zipped fastqc directories and display the results and graphs in a simple Flask HTML report. So, this script requires that Flask (and Flask bootstrap) be installed.

The app will be served on 0.0.0.0 -- so it should be viewable on your LAN at your workstation's IP address, port 5000. You can perform some simple 'queries' (there is no database for this version, everything is stored in an ordered dictionary). This should give an overview of sequencing data for your project.
