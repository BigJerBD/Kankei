import argparse
import inspect
import sys

import imports
from config import fetch_mapping

parser = argparse.ArgumentParser(description='Kankei Import Management Application')

# parser.add_argument("-a", nargs="+", action="append", dest="actions",
#                    help="name of the action, then its arguments."
#                         " possible actions: " + ", ".join(admin.get_admin_actions()))

# def execute_import(import_tu):
#    ...

# todo  the extra meaning tags doesnt show
# todo korean tags doesnt works

imports = {
    name: imp
    for name, imp in inspect.getmembers(sys.modules['imports'])
    if type(imp) == imports.ImportProc
}


def execute_imports(import_obj):
    aggregator = import_obj.aggregator(**import_obj.aggr_args)

    for fetch in import_obj.fetches:
        fetch_method, path = fetch_mapping[fetch]
        for data in fetch_method(path):
            aggregator.add(data)

    # Q: put the pathing here?
    # Q: does all data will be able to get categorised?
    import_obj.writer(aggregator.iter(), **import_obj.writer_args)


if __name__ == "__main__":
    # todo implement the cmd line interface
    # todo test ~
    execute_imports(imports["make_monashkanji"])
    # args = parser.parse_args()
    # action_dict = admin.get_admin_actions()
    # for actions in args.actions:
    #    name, *arguments = actions
    #    splitted_args = (arg.split("=") for arg in arguments)
    #    splitted_args = ((k, v.strip("[]").split(",")) if v.startswith("[") and v.endswith("]")
    #                     else (k, v)
    #                     for k, v in splitted_args)
    #    action_dict[name](**dict(splitted_args))
