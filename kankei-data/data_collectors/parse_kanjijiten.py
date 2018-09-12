import re

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
misc_tag_regex = r"<misc:(?P<type>.)>"

#regex_misc_info = re.compile(
#    rf"(?P<interval>{regex_number}～{regex_number})?"
#    rf"(?P<enum>{regex_number}*)"
#    rf"(?P<misc>{regex_char_enum}*)"
#    rf"(?P<content>.*)"
#)


def remove_brackets(data_str):
    regex = r"\([^A-z()]*\)"
    return re.sub(regex, "", re.sub(regex, "", data_str))


def split_on_number(meaning_str):
    yield from (elem for elem in re.split(rf"{regex_number}", meaning_str) if elem)


def handle_meaning(kanji, meaning_str):
    meaning_groups = make_meaning_groups(meaning_str)

    if next((m for m in meaning_groups if
             '(A)' in m["content"] or '(B)' in m["content"]), None):
            yield "skips", [kanji]
    else:
        for meaning in get_meanings(meaning_groups):
            yield 'meanings', [kanji, *meaning]
        for misc in get_miscs(meaning_groups):
            yield 'miscs', [kanji, *misc]


def make_meaning_groups_redux(meaning_str):
    ...


def make_meaning_groups(meaning_str):

    first_part, *parts = re.split(misc_tag_regex, meaning_str)

    meaning_list = [
        {'interval': '', 'enum': '', 'misc': '', 'type': '',
         'content': remove_brackets(first_part or "")}
    ]
    misc_to_write = []
    for pos, misc in enumerate(parts):
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
