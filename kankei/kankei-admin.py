import argparse

import admin

parser = argparse.ArgumentParser(description='Kankei Import Management Application')

parser.add_argument("-a", nargs="+", action="append", dest="actions",
                    help="name of the action, then its arguments."
                         " possible actions: " + ", ".join(admin.get_admin_actions()))

if __name__ == "__main__":
    args = parser.parse_args()
    action_dict = admin.get_admin_actions()
    for actions in args.actions:
        name, *arguments = actions
        splitted_args = (arg.split("=") for arg in arguments)
        splitted_args = ((k, v.strip("[]").split(",")) if v.startswith("[") and v.endswith("]")
                         else (k, v)
                         for k, v in splitted_args)
        action_dict[name](**dict(splitted_args))
