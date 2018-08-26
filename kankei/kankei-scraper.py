import argparse

import web_scraper
from util.csv_util import stream_csv_data

parser = argparse.ArgumentParser(description='Web Scrapper for Kanji dictionary websites')
parser.add_argument("-sd", default=",", help="delimiter in the source csv")
parser.add_argument("-dd", default=",", help="delimiter in the destination csv")
parser.add_argument("-se", default="UTF-8", help="encoding of the source file")
parser.add_argument("-de", default="UTF-8", help="encoding of the destination file")

parser.add_argument("-a", action="store_true",
                    help="append data to csvs, else overwrite files")

parser.add_argument("scraper", choices=list(web_scraper.get_scrapers().keys()),
                    help="Name of the scraper to use")
parser.add_argument("src", help="source csv file")
parser.add_argument("dst", help="destination csv follder ")

if __name__ == "__main__":
    scrapers = web_scraper.get_scrapers()
    args = parser.parse_args()

    kanjis = list(stream_csv_data(args.src, args.se, delimiter=args.sd))
    scraper = scrapers[args.scraper]()
    scraper.mode = "a" if args.a else "w"
    scraper.encoding = args.de
    scraper.run(kanjis, args.dst)
