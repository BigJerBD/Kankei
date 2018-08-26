import abc
import csv
from collections import defaultdict
from pathlib import Path

from progress.bar import Bar
from requests_html import HTMLSession

from util.csv_util import open_csvs


def webscrap_flow(data_size, result_path):
    bar = Bar("Kanjipedia extraction progress", max=data_size)
    print("")
    print(f"staring kanjipedia fetching:")
    print(f"\t Number of kanji to fetch : {data_size}")
    print(f"\t Output directory: {result_path}")
    print("")
    yield bar
    bar.finish()
    print("\nPost processing")
    yield
    print(f'Kanji extraction completed')
    yield


def serialize_csv(data, path, mode="w+", encoding="utf-8", delimiter=","):
    with open(path, mode, encoding=encoding) as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter)
        for elem in data:
            writer.writerow(elem)


def serialize_dct_in_csvs(basepath, data_dict):
    for name, data in data_dict.items():
        serialize_csv(data, Path(basepath, name).with_suffix('.csv'))


class KanjiDictScraper:
    """
    todo :: consider if the output should be parametrable
    todo :: -> (implies just pushing in a dict and the writing)

    todo :: soft fail or hard fail ....
    todo :: removing csv may be  a good way to avoid dependencies
    """

    def __init__(self, url, mode, encoding, result_files, stream_write=False):
        self.url = url
        self.encoding = encoding
        self.mode = mode
        # this comes from a different version, might be useful later
        self.data_categories = result_files + ["errors", "missings"]
        self.stream_write = stream_write

    def run(self, kanjis_to_search, result_path):

        # note :: make it customisable?
        if not Path(result_path).exists():
            Path(result_path).mkdir()

        webscrap_step = webscrap_flow(len(kanjis_to_search), result_path)
        progress_bar = next(webscrap_step)

        # to rework
        if self.stream_write:
            with open_csvs(result_path, self.data_categories, self.mode, self.encoding) as files_dict:
                for kanji in kanjis_to_search:
                    for group, datas in self.fetch_kanji_data(kanji):
                        files_dict[group].writerow(datas)
                    progress_bar.next()

            next(webscrap_step)
            next(webscrap_step)

        else:
            data_dict = defaultdict(list)
            for cat in self.data_categories:
                data_dict.setdefault(cat, [])

            for kanji in kanjis_to_search:
                for group, datas in self.fetch_kanji_data(kanji):
                    data_dict[group].append(datas)
                progress_bar.next()

            next(webscrap_step)
            self.post_processing(data_dict)
            serialize_dct_in_csvs(result_path, data_dict)
            next(webscrap_step)

    def fetch_kanji_data(self, kanji):
        try:
            page = self.handle_search_page(self.url, kanji)

            if page:
                yield from self.handle_page(page, kanji)
            else:
                yield 'missings', [kanji]
        except Exception as e:
            print(f"\nexception occured on {kanji}: ", e)
            yield "errors", [kanji]

    def handle_search_page(self, url, kanji):
        session = HTMLSession()
        page = self.get_search_page(url, session, kanji)
        link = self.get_kanji_page_link(page)
        if link:
            return session.get(url + link).html
        return link

    @abc.abstractmethod
    def get_kanji_page_link(self, page):
        raise NotImplemented

    @abc.abstractmethod
    def get_search_page(self, url, session, kanji):
        raise NotImplemented

    @abc.abstractmethod
    def handle_page(self, page, kanji):
        raise NotImplemented

    @abc.abstractmethod
    def post_processing(self, kanji_dict):
        raise NotImplemented
