import config
import data_fetcher
import data_fetcher.kankeismartdict
from csv_reset import csv_file_reset
from csv_to_kankei import import_to_database
from data_to_csv import data_to_csv
from util.csv_util import write_in_csv, get_csv_header


if __name__ == "__main__":

    csv_file_reset()
    print("getting all datas")
    data_to_csv()
    print("importing csv to database")
    import_to_database()
