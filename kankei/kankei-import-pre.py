import config
import data_fetcher
from csv_file_reset import csv_file_reset
from util.csv_util import write_in_csv, get_csv_header


def execute_data_fetches(*fetch_procedures):
    for fetch_proc, *args in fetch_procedures:
        fetch_proc(*args)


def data_to_csvs(base_path, data_sequence):
    for name, data in data_sequence:
        csv_data = [d.csv for d in data]
        write_in_csv((base_path / name).with_suffix(".csv"),
                     get_csv_header(csv_data),
                     csv_data)


if __name__ == "__main__":

    csv_file_reset()
    print("getting all datas")

    kankei_dict = data_fetcher.KankeiSmartDict()

    file_list = config.data_src
    execute_data_fetches(
        (data_fetcher.get_components, file_list["component"], kankei_dict),
        (data_fetcher.get_kanji, file_list["kanji"], kankei_dict),
        (data_fetcher.get_radicals, file_list["radical"], kankei_dict),
        (data_fetcher.get_word, file_list["word"], kankei_dict)
    )
    print("writing data into csv")
    data_to_csvs(config.node_path, kankei_dict.iter_node())
    data_to_csvs(config.link_path, kankei_dict.iter_link())
    print("transfering csv to graph_db")
    #import_to_database()
