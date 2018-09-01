import argparse

import admin

parser = argparse.ArgumentParser(description='Kankei Import Management Application')

parser.add_argument("-a", nargs="+", action="append", dest="actions",
                    help="name of the action, then its arguments."
                         " possible actions: " + ", ".join(admin.get_admin_actions()))

# todo :: to make a full proper import multiple things must be added

# todo :: verify unit test
# todo :: flatten data based on model input ?complex
# todo :: merge data in a proper way

# REALLY THINK ABOUT all this ~
# idea 1 : transform everything into json?
# idea 2 : the end goal would be to have both a key-value store + a graph dabase store good night

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
