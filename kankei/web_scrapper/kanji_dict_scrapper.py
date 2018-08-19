import abc
import contextlib
from pathlib import Path

from progress.bar import Bar
from requests_html import HTMLSession

from util.csv_util import open_csvs


@contextlib.contextmanager
def logging_context(data_size, result_path):

    bar = Bar("Kanjipedia extraction progress", max=data_size)
    print("")
    print(f"staring kanjipedia fetching:")
    print(f"\t Number of kanji to fetch : {data_size}")
    print(f"\t Output directory: {result_path}")
    print("")
    yield bar
    bar.finish()
    print(f'Kanjipedia extraction completed')


class KanjiDictScrapper:
    """
    todo :: consider if the output should be parametrable
    todo :: -> (implies just pushing in a dict and the writing)

    todo :: soft fail or hard fail ....
    """
    def __init__(self, url, mode, encoding, result_files):
        self.url = url
        self.encoding = encoding
        self.mode = mode
        self.result_files = result_files + ["skips"]

    def run(self, kanjis_to_search, result_path):

        # note :: make i customisable
        if not Path(result_path).exists():
            Path(result_path).mkdir()

        writer_dict = open_csvs(result_path, self.result_files, self.mode, self.encoding)
        logging = logging_context(len(kanjis_to_search), result_path)

        with writer_dict as writers, logging as progress_handler:
            for kanji in kanjis_to_search:
                self.handle_kanji(kanji, writers)
                progress_handler.next()

    def handle_kanji(self, kanji, writers):
        try:
            page = self.handle_search_page(self.url, kanji)

            if page:
                self.handle_page(page, kanji, writers)
            else:
                writers['skips'].writerow([kanji])
        except Exception as e:
            print(f"\nexception occured on {kanji}: ", e)
            writers["skips"].writerow([kanji])

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
    def handle_page(self, page, kanji, writes):
        raise NotImplemented
