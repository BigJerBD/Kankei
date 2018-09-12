import argparse
import csv

import web_scrapers

parser = argparse.ArgumentParser(description='Web Scrapper for Kanji dictionary websites')
parser.add_argument("-sd", default=",", help="delimiter in the source csv")
parser.add_argument("-dd", default=",", help="delimiter in the destination csv")
parser.add_argument("-se", default="UTF-8", help="encoding of the source file")
parser.add_argument("-de", default="UTF-8", help="encoding of the destination file")

parser.add_argument("-a", action="store_true",
                    help="append data to csvs, else overwrite files")

parser.add_argument("scraper", choices=list(web_scrapers.get_scrapers().keys()),
                    help="Name of the scraper to use")
parser.add_argument("src", help="source csv file")
parser.add_argument("dst", help="destination csv follder ")


def stream_csv_data(csv_path, encoding, delimiter=","):
    with open(csv_path, "r", encoding=encoding) as fs:
        reader = csv.reader(fs, delimiter=delimiter)
        for collumn in reader:
            yield from (cell for cell in collumn if cell)


if __name__ == "__main__":
    scrapers = web_scrapers.get_scrapers()
    args = parser.parse_args()

    kanjis = list(stream_csv_data(args.src, args.se, delimiter=args.sd))
    scraper = scrapers[args.scraper]()
    scraper.mode = "a" if args.a else "w"
    scraper.encoding = args.de
    scraper.run(kanjis, args.dst)
