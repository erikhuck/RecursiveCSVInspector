# RecursiveCSVInspector
* The purpose of this repository is to be able to recursively inspect the csv files in a data directory. Additionally it is capable of recursively extracting and compressed files and directories in a data directory.
* The ADNI data used to test this script was downloaded in December 2019
* It was downloaded at http://adni.loni.usc.edu/
* Command for recusrisvely extracting all compressed files and directories in your data directory:
python3 main.py extract --data-path /path/to/data/directory
* Currently can extract the following file extensions: .tgz, .tar, .gz, .tar.gz, and .zip

* Command for inspecting:
python3 main.py inspect --data-path /path/to/data/directory --key-words keyword1 keyword2 ...
* Use the --verbose option to print statistical information about the columns in the CSVs in addition to the column names
