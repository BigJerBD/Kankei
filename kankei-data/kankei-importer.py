import argparse
from functools import partial

import yaml

# - todo kankei-data csv parser folder parser
# - todo sql lite parser
# - todo meaning extractor for kanjipedia and kanjiten
# - todo kanjiten and kanjipedia parser

parser = argparse.ArgumentParser(description='Kankei Import Management Application')
parser.add_argument("configs", nargs="+",
                    help="configurations files containing the actions")
parser.add_argument("-a", "--actions", nargs="+",
                    help="name of the actions from the config files to execute")


def get_actions(yaml_path, action_field="actions"):
    with open(yaml_path) as f:
        data = yaml.load(f.read())
    return data[action_field]


def execute_action(action_conf):
    aggr = build_object(**action_conf["aggregator"]) if "aggregator" in action_conf else None
    writers = [partial(build_object, **writer) for writer in action_conf["writer"]]
    fetches = [build_object(**fetch) for fetch in action_conf["fetches"]]

    for fetch in fetches:
        for data in fetch:
            aggr.add(data)

    for writer in writers:
        execute_writer(writer)


def execute_writer(writer, write_input=None):
    if write_input:
        writer(write_input.iter())
    else:
        writer()


def build_object(obj, args, **extra_args):
    components = obj.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod(**args, **extra_args)


if __name__ == "__main__":
    cmd_args = parser.parse_args()
    actions_map = {act_name: action
                   for conf in cmd_args.configs
                   for act_name, action in get_actions(conf).items()}
    for action in cmd_args.actions:
        execute_action(actions_map[action])
