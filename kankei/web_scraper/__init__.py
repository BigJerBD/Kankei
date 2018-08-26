import inspect
import sys

from web_scraper.kanji_dict_scraper import KanjiDictScraper
from web_scraper.kanjijiten_scrap import KanjitenonScraper
from web_scraper.kanjipedia_scrap import KanjipediaScraper


# todo investigate a lighter way to do class providing

def _get_classes(cls, from_module):
    return [
        (name, cur_cls) for name, cur_cls in inspect.getmembers(sys.modules[from_module],
                                                                inspect.isclass)
        if cls in cur_cls.__mro__[1:]
    ]


def get_scrapers():
    return {
        name: cls
        for module in sys.modules if "web_scraper" in module
        for name, cls in _get_classes(KanjiDictScraper, module)
    }
