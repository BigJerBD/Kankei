import re

from web_scrapers.kanji_dict_scraper import KanjiDictScraper

exception_list = [
    ('<img:/common/images/kanji/16/skj_8362.png>', '蝍'),
    ('<img:/common/images/kanji/16/skj_8376.png>', '蝑'),
    ('<img:/common/images/kanji/16/skj_8375.png>', '鉧'),
    ('<img:/common/images/kanji/16/skj_837E.png>', '鞺'),
    ('<img:/common/images/kanji/16/skj_8378.png>', '兕'),
    ('<img:/common/images/kanji/16/skj_837A.png>', '鯡'),
    ('<img:/common/images/kanji/16/skj_8373.png>', '丳'),
    ('<img:/common/images/kanji/16/skj_836F.png>', '墝'),
    ('<img:/common/images/kanji/16/skj_8380.png>', '艼'),
]


class KanjipediaScraper(KanjiDictScraper):

    def __init__(self):
        super().__init__(
            url="http://www.kanjipedia.jp",
            mode="w+",
            encoding="UTF-8",
            result_files=["meanings", "refs", "png_path"],
        )

    def get_search_page(self, url, session, kanji):
        return session.get(
            url=url + '/search',
            params={"k": kanji, "sk": "leftHand", "kt": "1"}
        )

    def get_kanji_page_link(self, page):
        return next((link for link in page.html.links if link.startswith("/kanji/")), None)

    def handle_page(self, page, kanji):
        yield from handle_kanji_meaning(page, kanji)
        yield from handle_kanji_refs(page, kanji)

    def post_processing(self, data_dict):
        replace_dict = {path.replace('/180/', '/16/'): kanji
                        for path, kanji in data_dict['png_path']}

        data_dict["meanings"] = [
            [kanji, replace_png_tags(line, replace_dict)]
            for kanji, line in data_dict["meanings"]
        ]
        data_dict["refs"] = [
            [kanji, kind, replace_png_tags(ref, replace_dict)]
            for kanji, kind, ref in data_dict["refs"]
        ]


def handle_kanji_meaning(page, kanji):
    meaning_node = page.xpath(
        "//body"
        "/div[@id='container']"
        "/div[@id='contentsWrapper']"
        "/div[@class='cf mt30']"
        "/div[@id='kanjiRightSection']"
        "/ul/li[1]/div/p[1]",
        first=True)

    result = meaning_node.element.text or ""
    for misc in meaning_node.element:
        if misc.tag == 'p':
            break
        text = misc.tail or ""
        attr = misc.attrib
        if misc.tag == "img":

            if "alt" not in attr:
                if "kan1.png" in attr['src']:
                    sub_info = "misc:二"
                elif "kan2.png" in attr['src']:
                    sub_info = "misc:二"
                else:
                    sub_info = f"img:{attr['src']}"
            else:
                sub_info = f"misc:{attr['alt']}"

            result += f'<{sub_info}>'
        result += text

    yield 'meanings', [kanji, result]


def handle_kanji_refs(page, kanji):
    left_part = page.xpath(
        "//body"
        "/div[@id='container']"
        "/div[@id='contentsWrapper']"
        "/div[@class='cf mt30']"
        "/div[@id='kanjiLeftSection']",
        first=True)
    refs = list(get_refs(left_part))
    img_link = get_png(left_part)
    if img_link:
        yield 'png_path', [img_link, kanji]

    for ref in ((t, v) for t, v in refs if v != kanji):
        yield 'refs', [kanji, *ref]


def get_refs(page):
    origin_kanjis = page.xpath("div/ul[@class='kanjiType']/li/div[@class='cf']")
    for origin_kanji in origin_kanjis:
        type_ref = origin_kanji.xpath('div/ul/li/img/@alt', first=True)
        ref_kanji = origin_kanji.xpath("div/div[1]/p/text()", first=True)
        if ref_kanji:
            if type_ref in ['旧字', "異体字"]:
                yield type_ref, ref_kanji
        elif origin_kanji.element.find('img') is not None:
            yield f"<{origin_kanjis[1].element.find('img').attrib['src']}>"


def get_png(page):
    kanji_box = page.xpath("div/div[1]/p[@id='kanjiOyaji']", first=True)
    if not kanji_box.text:
        return kanji_box.xpath('p/img/@src', first=True)
    return None


def replace_png_tags(line, replace_dct):
    try:
        match = re.search(r"<img:([^>]+)>", line)
        while match:
            begin, end = match.start(), match.end()
            line = line[:begin] + replace_dct[match.group(1)] + line[end:]
            match = re.search(r"<img:([^>]+)>", line)

    except KeyError:
        for search, replace in exception_list:
            if search in line:
                line = line.replace(search, replace)
        else:
            print(f"Exception replacement not found for line :\n\t- {line}")

    return line
