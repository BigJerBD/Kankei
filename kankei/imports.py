import inspect
from collections import namedtuple
from pathlib import Path

from config import conf
from data_aggregator.combiner_aggr import CombinerAggr
from data_parsers import Character
from data_writers import csv_writer

ImportProc = namedtuple("ImportProc", ["aggregator", "aggr_args", "fetches", "writer", "writer_args"])

make_graphmodel = ...

make_monashkanji = ImportProc(
    aggregator=CombinerAggr,
    aggr_args={
        "combinable_types": [Character]
    },
    fetches=["monash_kanji", "monash_radicals", "kanjivg"],
    writer=csv_writer,
    writer_args={
        "path": Path(conf.data.output),
        "reset": True
    }
)

