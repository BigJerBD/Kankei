from collections import defaultdict

from web_scrapers.kanji_dict_scraper import KanjiDictScraper


class KanjitenonScraper(KanjiDictScraper):
    # todo correct kanjijiten (forgot what was the problem, but must be revised)

    def __init__(self):
        super().__init__(
            url="https://kanji.jitenon.jp",
            mode="w+",
            encoding="UTF-8",
            result_files=["JIS水準", "Unicode", "学年",
                          "意味", "漢字検定", "画数", "異体字",
                          "種別", "訓読み", "部首", "音読み"],
            stream_write=True
        )

    def get_search_page(self, url, session, kanji):
        return session.get(
            url=url + '/cat/search.php',
            params={"getdata": kanji, "search": "fpart", "search2": "kanji"}
        )

    def get_kanji_page_link(self, page):
        kanji_table = page.html.xpath(
            "//body"
            "//div[@id='main2']"
            "/table[@class='searchtb']",
            first=True)
        if kanji_table:
            return list(kanji_table.links)[0].replace(self.url, "")

    def handle_page(self, page, kanji):
        info_page = page.xpath(
            "//body"
            "//div[@id='kanjiright']"
            "/table[@class='kanjirighttb']"
            "/*"
        )

        mapped_table = split_horizontal_table(info_page)

        for key, values in mapped_table.items():
            if not key:
                raise KeyError("Invalid parsing of kanjijitenon table")
            yield from [(key, (kanji, value)) for value in values if value]

    def post_processing(self, data_dict):
        pass


def split_horizontal_table(table):
    rows_dict = defaultdict(list)
    cur_list = []
    cur_header = None
    for line in table:
        header = line.xpath("//th/h3/text()|//th/text()", first=True)
        if header and header != "\xa0":
            if cur_list:
                rows_dict[cur_header] = cur_list
            cur_list = []
            cur_header = header

        cur_list.append("".join(line.xpath("//td/descendant-or-self::text()")))

    if cur_header == "異体字":
        rows_dict[cur_header] = [variant for variant in cur_list
                                 if variant
                                 and len(variant) == 1
                                 and variant[0] is not "\n"]
    else:
        rows_dict[cur_header] = cur_list
    return rows_dict
