import data_fetcher
import data_fetcher.kankeismartdict
from config import conf
from csv_reset import csv_file_reset
from util.csv_util import write_in_csv, get_csv_header


def data_to_csv():
    kankei_dict = data_fetcher.kankeismartdict.KankeiSmartDict()

    execute_data_fetches(
        (data_fetcher.get_components, kankei_dict, conf.data.component),
        (data_fetcher.get_kanji, kankei_dict, conf.data.kanji),
        (data_fetcher.get_radicals, kankei_dict, conf.data.radical),
        (data_fetcher.get_word, kankei_dict, conf.data.word)
    )
    write_to_csv(conf.csv.node, kankei_dict.iter_node())
    write_to_csv(conf.csv.link, kankei_dict.iter_link())


def execute_data_fetches(*fetch_procedures):
    for fetch_proc, *args in fetch_procedures:
        fetch_proc(*args)


def write_to_csv(base_path, data_sequence):
    for name, data in data_sequence:
        csv_data = [d.csv for d in data]
        write_in_csv((base_path / name).with_suffix(".csv"),
                     get_csv_header(csv_data),
                     csv_data)


if __name__ == "__main__":
    csv_file_reset()
    print("getting all datas")
    data_to_csv()
