import re
import sys

from util.csv_util import stream_csv_data
from web_scrapper.kanji_dict_scrapper import KanjiDictScrapper

regex_char_enum = r"[\u4E00-\u9FAF\u3040-\u30FF・]"
regex_number = r"[①-⑩⑪-⑳]"
regex_kanjidigit = r"[一-十]"
num_value = {
    "①": 1, "②": 2, "③": 3, "④": 4,
    "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8,
    "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12,
    "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16,
    "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20
}
regex_misc_info = re.compile(
    rf"(?P<interval>{regex_number}～{regex_number}|)"
    rf"(?P<enum>{regex_number}*)"
    rf"(?P<misc>{regex_char_enum}*)"
    rf"(?P<content>.*)"
)


class KanjipediaScrapper(KanjiDictScrapper):

    def __init__(self):
        super().__init__(
            url="http://www.kanjipedia.jp",
            mode="w",
            encoding="UTF-8",
            result_files=["meanings", "miscs", "refs", "png_path"]
        )

    def get_search_page(self, url, session, kanji):
        return session.get(
            url=url + '/search',
            params={"k": kanji, "sk": "leftHand", "kt": "1"}
        )

    def get_kanji_page_link(self, page):
        return next((link for link in page.html.links if link.startswith("/kanji/")), None)

    def handle_page(self, page, kanji, writers):
        handle_meaning(page, kanji, writers)
        handle_link(page, kanji, writers)


def remove_brackets(data_str):
    regex = r"\([^A-z()]*\)"
    return re.sub(regex, "", re.sub(regex, "", data_str))


def split_on_number(meaning_str):
    yield from (elem for elem in re.split(rf"{regex_number}", meaning_str) if elem)


def handle_meaning(page, kanji, writers):
    meaning_node = page.xpath(
        "//body"
        "/div[@id='container']"
        "/div[@id='contentsWrapper']"
        "/div[@class='cf mt30']"
        "/div[@id='kanjiRightSection']"
        "/ul/li[1]/div/p[1]",
        first=True)

    meaning_groups = make_meaning_groups(meaning_node)

    if next((m for m in meaning_groups if
             '(A)' in m["content"] or '(B)' in m["content"]), None):
        writers["skips"].writerow([kanji])
    else:
        for meaning in get_meanings(meaning_groups):
            writers['meanings'].writerow([kanji, *meaning])
        for misc in get_miscs(meaning_groups):
            writers['miscs'].writerow([kanji, *misc])


def handle_link(page, kanji, writers):
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
        writers['png_path'].writerow([img_link, kanji])

    for ref in ((t, v) for t, v in refs if v != kanji):
        writers['refs'].writerow([kanji, *ref])


def make_meaning_groups(meaning_node):
    meaning_list = [
        {'interval': '', 'enum': '', 'misc': '', 'type': '',
         'content': remove_brackets(meaning_node.element.text or "")}
    ]
    misc_to_write = []
    for pos, misc in enumerate(meaning_node.element):
        if misc.tag == 'p':
            break
        text = remove_brackets(misc.tail or "")
        # filter the the meaning string so it doesnt have miscanelous
        if misc_to_write:
            match_dct = regex_misc_info.match(text).groupdict()
            match_dct['misc'] = f'<{misc.attrib["src"]}>' + match_dct['misc']
            meaning_list.append({'type': misc_to_write.pop(), **match_dct})
        elif 'alt' not in misc.attrib:
            meaning_list[-1]['content'] += f'<{misc.attrib["src"]}>{text}' if misc.tag == "img" else text
        elif text:
            match = regex_misc_info.match(text)
            meaning_list.append({'type': misc.attrib['alt'], **match.groupdict()})
        else:
            misc_to_write.append(misc.attrib['alt'])

    return meaning_list


def get_meanings(meaning_parts):
    meaning_str = "".join(meaning['content'] for meaning in meaning_parts)

    for num, definitions in enumerate(split_on_number(meaning_str), 1):
        # the last element in the definitions are kanji-word definition in 「 」
        *str_means, keywords = definitions.split("。")
        for mean in str_means:
            yield num, "description", mean

        for close_word in (c for c in keywords.strip(" ").split('」「') if c):
            close_word = close_word.replace('」', '').replace('「', '')
            yield num, "word", close_word


def get_miscs(meaning_parts):
    cur_meaning = meaning_parts[0]['content']
    cur_num_meaning = len(list(split_on_number(cur_meaning)))
    cur_readings = []
    for mean_info in meaning_parts[1:]:
        affected_meanings = []

        if mean_info['interval']:
            interval = mean_info['interval']
            affected_meanings = range(num_value[interval[0]], num_value[interval[-1]] + 1)
        elif mean_info['enum']:
            affected_meanings = (num_value[num_ball] for num_ball in mean_info['enum'])
        elif mean_info['type'] in "対類":
            affected_meanings = [cur_num_meaning]
        elif re.search(regex_kanjidigit, mean_info['type']):
            cur_readings = mean_info['misc'].split('・')

        for meaning_num in affected_meanings:
            for misc_str in mean_info['misc'].split('・'):
                yield meaning_num, mean_info['type'], remove_brackets(misc_str)

        cur_meaning = mean_info['content']
        next_nums = list(split_on_number(cur_meaning))[1:]

        for reading in cur_readings:
            for num_meaning, _ in enumerate(next_nums, 1):
                yield cur_num_meaning + num_meaning, reading

        cur_num_meaning += len(next_nums)


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


if __name__ == "__main__":
    if len(sys.argv) == 3:
        KanjipediaScrapper().run(
            list(stream_csv_data(sys.argv[1], "UTF-8", delimiter=" ")),
            sys.argv[2]
        )
    else:
        print(f"usage: {sys.argv[0]} <kanji_path>, <result_path>")
